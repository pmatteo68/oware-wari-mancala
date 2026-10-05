"""
Game logic configuration for the game.
All gameplay-affecting parameters live here.
"""

# -- Board setup --------------------------------------------------------------
NUM_PLAYERS     = 2          # Not modifiable. This is REALLY a hardcoding.
PITS_PER_PLAYER = 6          # pits on each side of the board
SEEDS_PER_PIT   = 4          # seeds per pit at game start
WIN_THRESHOLD = (NUM_PLAYERS * PITS_PER_PLAYER * SEEDS_PER_PIT) // 2 + 1 # seeds needed to win outright (25 of 48 total in case of standard 6 pits and 4 seeds per pit)

# -- AI engine selection ------------------------------------------------------
# Name of the plugin module inside the ai_engines/ package to load.
# To switch engine: drop a new module in ai_engines/ and change this value.
AI_ENGINE = "minimax_alphabeta"

# -- AI configuration ---------------------------------------------------------
AI_DELAY_MS     = 900        # ms to wait before AI plays (lets human see board)

# -- Capture thresholds -------------------------------------------------------
# A pit on the opponent's side triggers a capture if, AFTER the last seed is
# placed in it, its total seed count is in this set.
# Standard Oware rule: {2, 3}  (i.e. 1 or 2 seeds were there before -> after = 2 or 3)
# Some regional variants use {2} only, or {1, 2, 3}.
CAPTURE_THRESHOLDS = frozenset({2, 3})

# -- Cycle / no-progress detection --------------------------------------------
CYCLE_NO_CAPTURE_LIMIT = 50  # if no capture in this many half-moves -> game ends
                              # remaining seeds split by side rule

# -- Move animation timing (used by the game engine, not the UI) ---------------
# The UI reads these to pace its step-by-step seed-placement animation.
ANIM_STEP_DELAY_MS    = 220  # delay between placing each individual seed
ANIM_CAPTURE_PAUSE_MS = 500  # pause on captured pits before removing seeds
ANIM_BLINK_INTERVAL_MS = 180 # blink half-period for source-pit highlight
ANIM_BLINK_COUNT       = 4   # how many times source pit blinks before distributing
ANIM_FINISH_DELAY_MS      = 80  # brief pause before animation on_done callback fires
ANIM_PRE_CAPTURE_PAUSE_MS = 100 # pause after seed distribution before capture flash starts
ANIM_CAPTURE_FLASH_COUNT  = 4   # number of blink half-cycles for the capture flash

# -- Stats / hint quality -----------------------------------------------------
# Minimum eval-score gap (AI perspective) between hint move and played move
# for the played move to be counted as a "missed opportunity".
MISSED_OPPORTUNITY_THRESHOLD = 50

# -- Autoplay (testing / demo) ------------------------------------------------
# When True: skips the intro screen, starts immediately with the machine going
# first, and the human turn is played automatically by following the hint every
# time.  Set False (default) for normal interactive play.
AUTOPLAY               = False
AUTOPLAY_HINT_DELAY_MS = 300   # ms to wait before auto-requesting a hint
