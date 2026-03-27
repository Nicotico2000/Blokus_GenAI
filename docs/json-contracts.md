# JSON Contracts

This project defines JSON contracts for state exchange, move operations, and mode configuration.

## Schema files

- `schemas/game_state.schema.json`: Full serialized game state used by CLI load/show/apply/suggest flows and fixtures.
- `schemas/move.schema.json`: One move proposal/result used by validate/apply/legal-moves/suggest operations.
- `schemas/mode_config.schema.json`: Mode definition contract for shared-engine configuration (Classic now, Duo planned).

## Why these schemas exist

- Keep CLI inputs/outputs predictable.
- Keep fixtures reproducible and reviewable.
- Make Classic and Duo mode differences explicit in data contracts.
- Support traceability from requirements to tests and artifacts.

## Example valid objects

### Valid move

```json
{
  "player": "blue",
  "piece": "T4",
  "x": 3,
  "y": 2,
  "rotation": 1,
  "flipped": false
}
```

### Valid mode config (Classic)

```json
{
  "name": "classic",
  "board_size": 20,
  "players": ["blue", "yellow", "red", "green"],
  "start_corners": {
    "blue": [0, 0],
    "yellow": [19, 0],
    "red": [19, 19],
    "green": [0, 19]
  },
  "piece_ids": ["I1", "I2", "I3", "V3", "I4", "O4", "T4", "L4", "Z4", "F5", "I5", "L5", "N5", "P5", "T5", "U5", "V5", "W5", "X5", "Y5", "Z5"],
  "starting_rule": "must-cover-start-corner",
  "continuation_rule": "corner-touch-no-edge-touch",
  "termination_rule": "all-players-blocked"
}
```

### Valid game state

`fixtures/states/classic_initial.json` is the canonical valid example for Phase 1.

## Example invalid objects

### Invalid move

```json
{
  "player": "blue",
  "piece": "I2",
  "x": 1,
  "y": 1,
  "rotation": 5
}
```

Reason: `rotation` must be one of `0`, `1`, `2`, `3`.

### Invalid mode config

```json
{
  "name": "duo",
  "board_size": 20,
  "players": ["blue", "orange"],
  "start_corners": {
    "blue": [0, 0],
    "orange": [19, 19]
  },
  "piece_ids": ["I1"]
}
```

Reason: Duo contract requires `board_size = 14` with Duo-specific coordinate range.

### Invalid game state

```json
{
  "mode": "classic",
  "board_size": 20,
  "players": ["blue", "yellow", "red", "green"],
  "board": ["..................."],
  "remaining_pieces": {},
  "history": [],
  "current_player": "purple",
  "consecutive_passes": 0,
  "finished": false,
  "controller_types": {},
  "controller_strategies": {}
}
```

Reasons:

- Missing required fields (`start_corners`).
- Board dimensions and symbols are invalid.
- `current_player` is not a valid player ID.

## Relationship to CLI operations, tests, and fixtures

- CLI operations:
  - `new`, `show`, `validate`, `apply`, `legal-moves`, `suggest` exchange objects conforming to `game_state` and `move` contracts.
- Tests:
  - `tests/test_serialization.py` verifies round-trip behavior for `GameState`.
  - `tests/test_cli.py` verifies command behavior with fixture-backed state input.
- Fixtures:
  - `fixtures/states/*.json` should conform to `game_state.schema.json`.
  - `fixtures/scenarios/*.json` embed move-like objects compatible with `move.schema.json`.
