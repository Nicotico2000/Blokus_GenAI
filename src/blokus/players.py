"""Simple computer-player helpers."""

from blokus.engine import list_legal_moves
from blokus.models import GameState, Move
from blokus.pieces import PIECES

DEFAULT_STRATEGY = "default"


def choose_simple_move(state: GameState, player: str | None = None) -> Move | None:
    """Pick a deterministic legal move, preferring larger pieces first."""

    active_player = player or state.current_player
    legal_moves = list_legal_moves(state, player=active_player)
    if not legal_moves:
        return None
    return min(
        legal_moves,
        key=lambda move: (
            -PIECES[move.piece].size,
            move.y,
            move.x,
            move.piece,
            move.rotation,
            move.flipped,
        ),
    )


def available_strategies() -> tuple[str, ...]:
    """Return the currently supported computer-player strategy ids."""

    return (DEFAULT_STRATEGY,)


def choose_move(
    state: GameState,
    player: str | None = None,
    strategy: str = DEFAULT_STRATEGY,
) -> Move | None:
    """Dispatch move choice to the requested strategy implementation."""

    if strategy != DEFAULT_STRATEGY:
        raise ValueError(f"Unsupported strategy '{strategy}'.")
    return choose_simple_move(state, player=player)
