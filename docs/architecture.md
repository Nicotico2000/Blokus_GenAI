# Architecture Baseline

## Intent

The project uses a shared plain-Python engine with mode-specific configuration. Phase 1 delivers Classic. Phase 2 should add Duo by extending configuration and tests, not by creating a second engine.

## Configurable engine concept

- Rules execution lives in shared engine code (`src/blokus/engine.py`).
- Mode-specific parameters live in `ModeConfig` (`src/blokus/config.py`).
- Game state is serializable and independent of interface (`src/blokus/models.py`).
- CLI, tests, fixtures, and scripts call the same engine APIs.

## Shared engine vs mode configuration

- Shared engine responsibilities:
  - Validate move legality.
  - Apply valid moves.
  - Enumerate legal moves.
  - Handle turn progression and termination checks.
- Mode configuration responsibilities:
  - Board size.
  - Player set and turn order.
  - Start corner coordinates.
  - Future mode-specific constraints.

## Core domain model

- `Board`: represented as a 2D grid in `GameState.board` (`list[list[str | None]]`).
- `Piece`: canonical cells plus unique transforms (`src/blokus/pieces.py`).
- `Player`: string identifiers such as `blue`, `yellow`, `red`, `green`, and planned `orange` for Duo.
- `Move`: placement intent with player, piece, origin, rotation, and flip (`Move` dataclass).
- `GameState`: mode, board, players, remaining pieces, history, active turn, and completion flags.
- `ModeConfig`: static per-mode config with board dimensions, players, and start corners.

## Separation of concerns

- Engine: `src/blokus/engine.py`
- CLI and rendering: `src/blokus/cli.py`, `src/blokus/render.py`
- Tests: `tests/`
- Fixtures: `fixtures/`
- Reproducibility scripts: `scripts/`
- Schemas/contracts and process docs: `schemas/`, `docs/`

## Phase 1 and Phase 2 boundary

- Phase 1 baseline target: Classic 4-player support and stable CLI+JSON operations.
- Phase 2 target: Duo support by config extension and additional tests/fixtures.
- Constraint: do not fork engine logic into separate Classic/Duo engines.
