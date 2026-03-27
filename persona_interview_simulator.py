#!/usr/bin/env python3
"""
Persona Interview Simulator for Ollama

Purpose
-------
Runs semi-structured interviews against multiple personas using an Ollama model.
Each persona gets a fresh session. The script asks one question at a time,
waits for the model's answer, then proceeds to the next question. When all
questions for a persona are finished, the transcript is saved as Markdown and,
optionally, PDF.

Requirements
------------
- Python 3.10+
- requests
- Optional for PDF export: reportlab

Install:
    pip install requests reportlab

Run:
    python scripts/persona_interview_simulator.py

Notes
-----
- The model name is configurable. If your local Ollama tag differs from
  "qwen3:8b", change MODEL_NAME below or set OLLAMA_MODEL.
- This script uses Ollama's /api/chat endpoint and manages conversation history
  locally per persona, which effectively gives each persona an isolated session.
"""

from __future__ import annotations

import json
import os
import re
import sys
import textwrap
from copy import deepcopy
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import requests

# Optional PDF export
try:
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

    PDF_AVAILABLE = True
except Exception:
    PDF_AVAILABLE = False


# =========================
# Configuration
# =========================

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3:8b")
OUTPUT_DIR = Path(os.getenv("INTERVIEW_OUTPUT_DIR", "persona_interviews"))
EXPORT_PDF = os.getenv("EXPORT_PDF", "1").lower() not in {"0", "false", "no"}
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "180"))
# Defaulting to False avoids blocking in non-interactive runs.
WAIT_FOR_ENTER_BETWEEN_QUESTIONS = os.getenv("WAIT_FOR_ENTER", "0").lower() in {
    "1",
    "true",
    "yes",
}
MAX_PERSONAS = int(os.getenv("MAX_PERSONAS", "0"))
MAX_QUESTIONS = int(os.getenv("MAX_QUESTIONS", "0"))
# Context controls for smaller models: include a short rolling Q/A memory
# directly in each new interviewer turn.
CONTEXT_WINDOW_QA = int(os.getenv("CONTEXT_WINDOW_QA", "4"))
CONTEXT_ANSWER_CHAR_LIMIT = int(os.getenv("CONTEXT_ANSWER_CHAR_LIMIT", "320"))


# =========================
# Input data
# =========================

PERSONAS = [
    {
        "persona": {
            "name": "Emily",
            "age": 34,
            "tech_experience": "moderate",
            "goals": [
                "play a strategy game that is easy to teach to friends and family",
                "fit a full game into a short evening slot",
                "find a game with high replayability and low setup effort",
            ],
            "constraints": [
                "mixed-skill household",
                "limited time for game nights",
                "prefers rules that can be explained in under a minute",
            ],
        }
    },
    {
        "persona": {
            "name": "Daniel",
            "age": 29,
            "tech_experience": "high",
            "goals": [
                "master a clean abstract strategy game",
                "outplay opponents through spatial reasoning and planning",
                "practice against digital opponents between in-person sessions",
            ],
            "constraints": [
                "friends may dislike strong skill imbalance",
                "2-player games can become predictable against weaker opponents",
                "wants depth without long playtime",
            ],
        }
    },
    {
        "persona": {
            "name": "Sophie",
            "age": 41,
            "tech_experience": "moderate",
            "goals": [
                "evaluate whether Blokus is worth buying for a hobby-gaming collection",
                "avoid games that feel too abstract or emotionally flat",
                "find interaction that feels more exciting than pure spatial optimization",
            ],
            "constraints": [
                "skeptical of games described as bland",
                "prefers stronger theme or more dramatic player interaction",
                "may reject titles that appear simple but do not create memorable moments",
            ],
        }
    },
    {
        "persona": {
            "name": "Andrea",
            "age": 63,
            "tech_experience": "limited",
            "goals": [
                "learn the rules before teaching the physical game to grandchildren",
                "use a digital version for guided practice",
                "receive visible move hints and clear onboarding",
            ],
            "constraints": [
                "can be confused by unclear first-move indicators",
                "needs high interface clarity",
                "prefers forgiving tutorials over trial-and-error",
            ],
        }
    },
    {
        "persona": {
            "name": "Lukas",
            "age": 22,
            "tech_experience": "high",
            "goals": [
                "play Blokus online with friends",
                "switch between same-device, local, and online multiplayer",
                "use hints, undo, and flexible board settings while learning",
            ],
            "constraints": [
                "expects modern app usability",
                "wants asynchronous-friendly or less restrictive online sessions",
                "becomes frustrated by camera, panning, or board-navigation limitations",
            ],
        }
    },
]


CORE_QUESTIONS = [
    "Describe the situation in which you would use a digital version of Blokus.",
    "What main value would you expect from such a game?",
    "What would make the first experience successful for you?",
    "What would frustrate you most in the first session?",
    "Which features would be essential for you?",
    "Which features would be useful but not essential?",
    "What kind of learning support would you expect?",
    "What kind of multiplayer, if any, would you expect?",
    "What would make you continue using the game over time?",
    "What would make you reject it after trying it?",
]

PERSONA_QUESTIONS = {
    "Emily": [
        "What makes a strategy game easy to teach in your household?",
        "What do you mean when you say rules should be explainable in under a minute?",
        "What makes a game feel replayable for you?",
        "Why is low setup effort important in your case?",
        "What usually goes wrong when players have different skill levels?",
        "How should a tutorial work for a mixed-skill group?",
        "Would legal move hints or mistake explanations be useful?",
        "How should the game help beginners without slowing down experienced players?",
        "Which three features would be most important in a first release?",
    ],
    "Daniel": [
        "What does mastering a game like Blokus mean to you?",
        "Which aspects of spatial reasoning and planning are most satisfying for you?",
        "What makes a game strategically deep rather than merely complicated?",
        "What kind of AI opponents would you expect from a strong digital version?",
        "Would move analysis, replay review, or post-game statistics be useful to you?",
        "How important are ranking, matchmaking, or competitive systems?",
        "Should the game provide legal move highlighting, or would that reduce the challenge?",
        "What would make a two-player version stay interesting over time?",
        "Which features are essential for an advanced player like you?",
    ],
    "Sophie": [
        "What kinds of games usually earn a place in your collection?",
        "What would make a game like Blokus feel worth owning?",
        "What kind of player interaction do you find exciting?",
        "What makes a session memorable for you?",
        "What makes an abstract game feel bland or emotionally flat to you?",
        "Would presentation, animation, or sound design influence your opinion here?",
        "Should the digital version highlight blocking, tension, or clever plays?",
        "Would variant modes or alternative board setups increase its appeal?",
        "What would definitely make you reject the game?",
    ],
    "Andrea": [
        "What kinds of instructions help you learn a new game best?",
        "Why would guided practice be useful for you?",
        "What kind of move hints would help you most?",
        "What should happen in the tutorial so learning feels easy rather than stressful?",
        "What would help you understand the first move immediately?",
        "What makes an interface feel clear and reassuring to you?",
        "Should the game explain why a move is invalid?",
        "Would an undo button or practice mode make learning easier?",
        "What would make you feel ready to teach the physical game to your grandchildren?",
    ],
    "Lukas": [
        "What multiplayer modes do you expect in a modern digital board game?",
        "In which situations would you use same-device, local, or online play?",
        "Why is flexible online play with friends important to you?",
        "What makes an online session feel flexible rather than restrictive?",
        "What usability issues frustrate you most in similar apps?",
        "How should asynchronous play work?",
        "Which board settings should be customizable?",
        "How should camera movement, panning, and board navigation behave?",
        "What would make the app feel modern and polished to you?",
    ],
}


# =========================
# Data structures
# =========================


@dataclass
class TranscriptEntry:
    role: str
    content: str


# =========================
# Utility functions
# =========================


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")


def timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def build_system_prompt(persona: Dict[str, Any]) -> str:
    return textwrap.dedent(
        f"""
    You are participating in a requirements elicitation interview simulation.

    You must answer strictly as the following persona and remain consistent throughout:
    Name: {persona['name']}
    Age: {persona['age']}
    Technical experience: {persona['tech_experience']}

    Goals:
    {chr(10).join(f"- {g}" for g in persona['goals'])}

    Constraints:
    {chr(10).join(f"- {c}" for c in persona['constraints'])}

    Interview context:
    - The product is a digital version of Blokus.
    - Answer as a realistic human participant in a semi-structured interview.
    - Give clear, concrete, experience-based answers.
    - Prefer practical needs, frustrations, expectations, and trade-offs.
    - Do not mention that you are an AI or a model.
    - Do not answer in bullet points unless the question naturally calls for enumeration.
    - Keep answers substantive but not excessively long.
    - If a question is unclear, make the most reasonable assumption and answer naturally from the persona's perspective.
    """
    ).strip()


def build_questionnaire(persona_name: str) -> List[str]:
    questionnaire = CORE_QUESTIONS + PERSONA_QUESTIONS.get(persona_name, [])
    if MAX_QUESTIONS > 0:
        return questionnaire[:MAX_QUESTIONS]
    return questionnaire


def build_contextual_question(question: str, transcript: List[TranscriptEntry]) -> str:
    if CONTEXT_WINDOW_QA <= 0:
        return question

    qa_pairs: List[tuple[str, str]] = []
    pending_question: str | None = None
    for entry in transcript:
        if entry.role == "user":
            pending_question = entry.content.strip()
        elif entry.role == "assistant" and pending_question:
            qa_pairs.append((pending_question, entry.content.strip()))
            pending_question = None

    if not qa_pairs:
        return question

    recent_pairs = qa_pairs[-CONTEXT_WINDOW_QA:]
    context_lines = [
        "Previous interview context (stay consistent with it unless you explicitly explain a change):"
    ]
    for idx, (prev_q, prev_a) in enumerate(recent_pairs, start=1):
        cleaned_answer = re.sub(r"\s+", " ", prev_a).strip()
        if len(cleaned_answer) > CONTEXT_ANSWER_CHAR_LIMIT:
            cleaned_answer = cleaned_answer[:CONTEXT_ANSWER_CHAR_LIMIT].rstrip() + "..."
        context_lines.append(f"{idx}. Q: {prev_q}")
        context_lines.append(f"   A: {cleaned_answer}")

    context_block = "\n".join(context_lines)
    return (
        f"{context_block}\n\n"
        f"Current interviewer question:\n{question}\n\n"
        "Answer naturally as the same persona."
    )


def ollama_chat(messages: List[Dict[str, str]]) -> str:
    payload = {"model": MODEL_NAME, "messages": messages, "stream": False}
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise RuntimeError(f"Failed calling Ollama at {OLLAMA_URL}: {exc}") from exc

    data = response.json()

    # Common Ollama chat structure:
    # { "message": { "role": "assistant", "content": "..." }, ... }
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"].strip()

    raise RuntimeError(
        f"Unexpected Ollama response format: {json.dumps(data, indent=2)}"
    )


def save_markdown(
    persona: Dict[str, Any], questionnaire: List[str], transcript: List[TranscriptEntry]
) -> Path:
    file_path = OUTPUT_DIR / f"{slugify(persona['name'])}_{timestamp()}.md"

    lines = []
    lines.append(f"# Interview Transcript: {persona['name']}")
    lines.append("")
    lines.append("## Persona")
    lines.append("")
    lines.append(f"- **Name:** {persona['name']}")
    lines.append(f"- **Age:** {persona['age']}")
    lines.append(f"- **Technical experience:** {persona['tech_experience']}")
    lines.append(f"- **Goals:** {', '.join(persona['goals'])}")
    lines.append(f"- **Constraints:** {', '.join(persona['constraints'])}")
    lines.append("")
    lines.append("## Questionnaire")
    lines.append("")
    for i, q in enumerate(questionnaire, start=1):
        lines.append(f"{i}. {q}")
    lines.append("")
    lines.append("## Transcript")
    lines.append("")

    question_counter = 0
    for entry in transcript:
        if entry.role == "user":
            question_counter += 1
            lines.append(f"### Question {question_counter}")
            lines.append(entry.content)
            lines.append("")
        elif entry.role == "assistant":
            lines.append("**Answer**")
            lines.append(entry.content)
            lines.append("")

    file_path.write_text("\n".join(lines), encoding="utf-8")
    return file_path


def save_pdf(
    persona: Dict[str, Any], questionnaire: List[str], transcript: List[TranscriptEntry]
) -> Path | None:
    if not PDF_AVAILABLE or not EXPORT_PDF:
        return None

    file_path = OUTPUT_DIR / f"{slugify(persona['name'])}_{timestamp()}.pdf"

    doc = SimpleDocTemplate(
        str(file_path),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    heading_style = styles["Heading2"]
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=8,
    )

    story = []
    story.append(Paragraph(f"Interview Transcript: {persona['name']}", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Persona", heading_style))
    story.append(Paragraph(f"<b>Name:</b> {persona['name']}", body_style))
    story.append(Paragraph(f"<b>Age:</b> {persona['age']}", body_style))
    story.append(
        Paragraph(f"<b>Technical experience:</b> {persona['tech_experience']}", body_style)
    )
    story.append(Paragraph(f"<b>Goals:</b> {', '.join(persona['goals'])}", body_style))
    story.append(
        Paragraph(f"<b>Constraints:</b> {', '.join(persona['constraints'])}", body_style)
    )
    story.append(Spacer(1, 10))

    story.append(Paragraph("Questionnaire", heading_style))
    for i, q in enumerate(questionnaire, start=1):
        story.append(Paragraph(f"{i}. {q}", body_style))
    story.append(PageBreak())

    story.append(Paragraph("Transcript", heading_style))
    question_counter = 0
    for entry in transcript:
        text = (
            entry.content.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\n", "<br/>")
        )
        if entry.role == "user":
            question_counter += 1
            story.append(Paragraph(f"<b>Question {question_counter}</b>", body_style))
            story.append(Paragraph(text, body_style))
            story.append(Spacer(1, 6))
        elif entry.role == "assistant":
            story.append(Paragraph("<b>Answer</b>", body_style))
            story.append(Paragraph(text, body_style))
            story.append(Spacer(1, 10))

    doc.build(story)
    return file_path


def run_interview_for_persona(persona_wrapper: Dict[str, Any]) -> Dict[str, Path | None]:
    persona = deepcopy(persona_wrapper["persona"])
    questionnaire = build_questionnaire(persona["name"])
    system_prompt = build_system_prompt(persona)

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    transcript: List[TranscriptEntry] = []

    print("=" * 80)
    print(f"Starting interview for persona: {persona['name']}")
    print("=" * 80)

    for idx, question in enumerate(questionnaire, start=1):
        print(f"\n[{persona['name']}] Question {idx}/{len(questionnaire)}")
        print(f"Q: {question}")

        contextual_question = build_contextual_question(question, transcript)
        messages.append({"role": "user", "content": contextual_question})
        transcript.append(TranscriptEntry(role="user", content=question))

        answer = ollama_chat(messages)
        messages.append({"role": "assistant", "content": answer})
        transcript.append(TranscriptEntry(role="assistant", content=answer))

        print(f"A: {answer}")

        if WAIT_FOR_ENTER_BETWEEN_QUESTIONS and sys.stdin.isatty():
            input("\nPress Enter to continue to the next question...")

    md_path = save_markdown(persona, questionnaire, transcript)
    pdf_path = save_pdf(persona, questionnaire, transcript)

    print(f"\nSaved Markdown: {md_path}")
    if pdf_path:
        print(f"Saved PDF:      {pdf_path}")
    elif EXPORT_PDF:
        print("PDF export skipped because reportlab is not available.")

    return {"markdown": md_path, "pdf": pdf_path}


def main() -> None:
    ensure_output_dir()

    selected_personas = PERSONAS[:MAX_PERSONAS] if MAX_PERSONAS > 0 else PERSONAS

    print(f"Using model: {MODEL_NAME}")
    print(f"Ollama URL: {OLLAMA_URL}")
    print(f"Output directory: {OUTPUT_DIR.resolve()}")
    print(f"PDF export enabled: {EXPORT_PDF} | Available: {PDF_AVAILABLE}")
    print(
        "Wait-for-Enter between questions: "
        f"{WAIT_FOR_ENTER_BETWEEN_QUESTIONS and sys.stdin.isatty()}"
    )
    print(f"Context window (Q/A pairs): {CONTEXT_WINDOW_QA}")
    print(f"Persona limit: {MAX_PERSONAS if MAX_PERSONAS > 0 else 'all'}")
    print(f"Question limit: {MAX_QUESTIONS if MAX_QUESTIONS > 0 else 'all'}")

    results = []
    for persona in selected_personas:
        try:
            result = run_interview_for_persona(persona)
            results.append(result)
        except KeyboardInterrupt:
            print("\nExecution interrupted by user.")
            break
        except Exception as exc:
            print(f"\nError while processing persona {persona['persona']['name']}: {exc}")

    print("\nAll personas processed. Program exiting.")


if __name__ == "__main__":
    main()
