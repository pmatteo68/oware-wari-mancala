# Oware / Wari - Mancala

> **Version:** 2.0.0<br>
> **Date:** Oct. 4, 2026<br>
> **Author:** Matteo P.
> **URL:** https://github.com/pmatteo68/oware-wari-mancala

---

## Abstract

A desktop implementation of Oware (also known as Wari), the classic West-African two-player
Mancala strategy game. The player competes against a minimax AI with alpha-beta pruning. The
game runs fully offline with no external dependencies beyond Python and a few python libraries.

---

## Setup

### 1. Configure the environment

Open `bin/env` and set `PYTHON_HOME` to the directory that contains your Python 3.8+ executable. Check tech notes if something goes wrong.

### 2. Create the virtual environment

Run the `create_env` script once to create the `myenv` virtual environment and install dependencies:

This creates the `myenv` folder, activates it, and runs `pip install -r requirements.txt`.
If `myenv` already exists the script simply activates it.

### 3. Launch the game

Run the `play` script

---

## Configuration

All user-tunable parameters are isolated in dedicated files under `src/`. No other file
needs to be edited for typical customisation.

| File | Purpose |
|---|---|
| `src/config_game.py` | Gameplay rules: board size, seed counts, win threshold, capture thresholds, cycle limit, AI search depth, animation timing, missed-opportunity threshold, autoplay mode |
| `src/config_ui.py` | All visual parameters: window size, colors, fonts, pit dimensions, animation colors, hint blink style, stats window layout, trajectory chart options |
| `src/config_text.py` | Every user-visible string: button labels, menu items, status messages, game-over text, stats window labels and format strings |
| `src/log_config.py` | Logging: output file path, console echo toggle, global log level |
| `bin/env` | Python home path, virtual environment name |

---

## Tech Notes

- **Language / GUI**: Python 3.8+, tkinter (bundled with CPython). No installation required
  for tkinter on Windows and macOS; on Linux install `python3-tk` via the package manager.

- **AI**: Minimax with alpha-beta pruning, configurable search depth (default 6).
  Move ordering by immediate capture count improves pruning efficiency. At depth 6 the AI
  evaluates roughly 280,000 board positions per move; no logging is done inside the search
  hot path for this reason.

- **Immutable board**: `Board.apply_move()` never mutates its receiver; it returns a new
  `Board` and a `MoveResult`. The AI search tree exploits this via `Board.clone()`.

- **Hint engine**: reuses the identical minimax tree from the AI side, but from the human
  perspective (minimising the AI score). Zero duplicated search logic.

- **Stats collection**: `GameStats` accumulates per-move data throughout the game. At game
  end a summary is logged at INFO level and a modal window is shown with four sections
  (Outcome, Move Quality, AI Behaviour, Temporal) plus an optional trajectory chart.

- **Trajectory chart**: embedded matplotlib figure (`matplotlib.backends.backend_tkagg`).
  Controlled by `STATS_SHOW_CHART` in `config_ui.py`. Set to `False` to remove the chart
  without affecting the rest of the stats window.

- **Platform scripts**: both Windows (`.cmd`) and Unix/macOS (`.sh`) variants exist for
  `bin/env`, `create_env`, and `play`. The Windows `play.cmd` launches the game in a
  detached process (`start python ...`) so the terminal window does not block.

- **Non-ASCII policy**: all source files are strict 7-bit ASCII. No Unicode characters
  appear in code, comments, or string literals.

- **Single-file logging config**: `src/log_config.py` is the only file that configures
  logging. `setup()` is called as the very first action in `main.py` before any other
  import. A double-init guard (`if root.handlers`) makes it safe to call multiple times.

---

## AI Engine Plugin System

The AI logic is fully encapsulated behind a plugin interface. The active engine
is selected with a single line in `src/config_game.py`:

```
AI_ENGINE = "minimax_alphabeta"
```

The value is the name of a module inside `src/ai_engines/`. The facade
`src/ai_engine.py` loads it at runtime and re-exports its methods. The rest of
the codebase never references a specific engine directly.

### Contract (src/ai_engines/base.py)

Every engine module must contain a class that subclasses `AIEngine` and
implements all four methods, plus a module-level factory `create() -> AIEngine`.

| Method | Signature | Returns | Purpose |
|---|---|---|---|
| `get_name` | `() -> str` | Short one-liner | Engine identifier shown on the start screen and in logs |
| `get_best_move` | `(board, legal_moves) -> (pit, score)` | Chosen pit + eval score | Selects the strongest move for the AI (maximising player) |
| `get_hint_move` | `(board, legal_moves) -> (pit, rationale)` | Suggested pit + tooltip text | Suggests the best move for the human (minimising AI advantage) |
| `evaluate` | `(board) -> float` | Float score | Static board evaluation: positive = AI ahead, negative = human ahead |

`legal_moves` is always pre-computed by the caller and passed in; the engine
does not call `get_legal_moves` at its entry points (it may call it internally
during tree search).

### Writing a new engine

1. Create `src/ai_engines/my_engine.py`.
2. Import `AIEngine` from `ai_engines.base` and subclass it.
3. Implement all four methods. The `get_name` return value will appear on the
   start screen automatically.
4. Add a module-level factory:
   ```python
   def create() -> AIEngine:
       return MyEngine()
   ```
5. Set `AI_ENGINE = "my_engine"` in `src/config_game.py`.
6. No other file needs to change.

### Available engines

| Name (get_name) | Module | Features |
|---|---|---|
| Minimax / Alpha-Beta  depth N | `minimax_alphabeta` | Classic minimax search with alpha-beta pruning and capture-first move ordering. Depth configurable via `AI_DEPTH` in the engine's configuration file. Evaluation weighs captured-seed difference, immediate capture threats, board control, and mobility. |

---

## Skin Plugin System

The visual appearance is fully encapsulated behind a skin plugin interface. The
active skin is selected with a single line in `src/config_ui.py`:

```
SKIN = ...
```

The value is the name of a module inside `src/skins/`. The facade
`src/config_ui.py` loads it at runtime and re-exports all its constants. The
rest of the codebase never references a specific skin directly. If the specified
module cannot be loaded, the default skin is used as fallback (look at the section 'Available skins' below for full list).

### Contract (src/skins/\<name\>.py)

Every skin module must define all UI constants used by the application, plus the
`SKIN_NAME` identifier.

| Attribute | Type | Purpose |
|---|---|---|
| `SKIN_NAME` | `str` | Short display name shown on the start screen alongside the AI engine name |
| *(all other constants)* | various | Every constant defined in `skins/default.py` must be present with the same name and compatible type |

### Writing a new skin

1. Copy `src/skins/default.py` to `src/skins/my_skin.py`.
2. Change `SKIN_NAME` to a short descriptive label.
3. Edit colours, fonts, and layout values to taste.
4. Set `SKIN = "my_skin"` in `src/config_ui.py`.
5. No other file needs to change.

### Available skins

| Name (SKIN_NAME) | Module | Features |
|---|---|---|
| Default | `default` | Warm cream background with terracotta human pits, sky-blue AI pits, and pastel seed palette. |
| Mint-Gray | `mint_gray` | Light gray canvas with mint-green pits, muted gray AI pits, and a sage-and-seafoam seed palette. |
| Vivid-1 | `vivid_1` | High-energy palette: bright yellow canvas, vivid orange buttons, hot-pink human pits, vivid green AI pits, fully saturated seed colors. |
| Vivid-2 | `vivid_2` | Electric blue palette: pale blue canvas, vivid cobalt human pits, vivid cyan AI pits, all-blue seed spectrum from cobalt to violet. |
| Black-and-White | `black_and_white` | Fully monochrome: near-white canvas, dark-gray human pits, medium-gray AI pits, gray-scale seed palette. No color anywhere. |
| Deep-Ocean | `deep_ocean` | Dark navy canvas with bioluminescent teal human pits, deep ocean-teal AI pits, and a glowing cyan/aqua seed palette. |
| Sunset | `sunset` | Warm amber canvas, deep crimson board, vivid coral human pits, dark-gold AI pits, and a seed palette of reds, oranges, and golds. |
| Forest | `forest` | Pale leafy-green canvas, deep forest-green board, moss-green human pits, bark-brown AI pits, and a seed palette of greens and chestnuts. |
| Candy | `candy` | Soft blush-white canvas, bubble-gum pink human pits, lavender AI pits, pastel seed palette of pinks, mints, and lemons. |
| Midnight | `midnight` | Full dark mode: near-black canvas, electric violet human pits, deep indigo AI pits, neon purple/magenta seed palette. |
| Random | `random` | Randomly rotates among all the ones above. |
---

## Debugging

### Log levels

Logging is configured in `src/log_config.py`.

Set `LOG_LEVEL = logging.DEBUG` to see full per-move AI candidate scores, hint reasoning, animation lifecycle events, and grand-slam / forced-move detections.

Set `LOG_LEVEL = logging.INFO` to see only the game-summary block logged at game end:

### Autoplay mode

`AUTOPLAY` in `src/config_game.py` (default `False`) runs the game without human interaction, useful for quickly reaching the end-of-game stats window:

When enabled: the intro screen is skipped, the machine goes first, and every human turn is played automatically by requesting a hint and immediately following it. All stats are collected normally so the stats window at game end is fully populated. Set back to `False` for normal interactive play.

## Open Points
* Still there are a few hardcdings in `ui_main.py` (not sure if also in `ui_board.py` and `ui_stats.py`).

---

## Changelog

### 2.0.0 - 2026-10-04
- The AI logic is now pluggable.
- The color/layout attributes are now pluggable as SKINS.
- Added **New Game** as first item in the File menu
- Added **Get Hint** button and Utilities menu: runs minimax from the human perspective,
  blinks the suggested pit with a tooltip rationale, no move applied automatically
- Added **Load Game** and **Save Game** buttons to the status bar; Load Game added to the
  File menu
- Added **Exit** button to status bar and to the start screen
- Added **standard logging** with isolated single-file config (`log_config.py`): timestamp
  to the millisecond, thread, level, module and line; configurable level, file, and console
  output; all internal events at DEBUG, all errors at ERROR
- Enforced **strict ASCII policy** across all source files (no Unicode in code, comments,
  or strings)
- Implemented full **end-of-game statistics**: `GameStats` collector, `StatsWindow` modal
  dialog with four sections (Outcome, Move Quality, AI Behaviour, Temporal), all text and
  layout configurable in config files, stats logged at INFO level at game end
- Added **seed differential trajectory**: per-half-move list logged at INFO; stored in
  `GameStats.differential_trajectory`
- Added **trajectory chart**: matplotlib line chart embedded in the stats window via
  `FigureCanvasTkAgg`, fill color distinguishes human-leading vs machine-leading stretches;
  toggled by `STATS_SHOW_CHART` in `config_ui.py`
- Added **autoplay mode**: `AUTOPLAY` flag in `config_game.py` skips intro, auto-follows
  hint every human turn, drives the game to completion for testing
- Added `matplotlib>=3.7` to `requirements.txt`.
- Removed some hardcodings.
- Added license file.

### 1.0.0 - 2026-10-03
First created. Core Oware / Wari game: board rendering, seed animation, minimax AI,
save/load, start screen.
