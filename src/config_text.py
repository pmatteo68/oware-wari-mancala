"""
All user-visible text for the game.
Change any value here to localise or rebrand the game.
"""
from sw_metadata import getSWName, getVersion, getRulesDesc
from config_game import NUM_PLAYERS, PITS_PER_PLAYER, SEEDS_PER_PIT, WIN_THRESHOLD, CAPTURE_THRESHOLDS

# Evaluated pre-config - begin
num_of_players = NUM_PLAYERS
pits_per_player = PITS_PER_PLAYER #6
seeds_per_pits = SEEDS_PER_PIT #4
min_to_win = WIN_THRESHOLD #25
capt_thresh_desc = "-".join(map(str, sorted(CAPTURE_THRESHOLDS)))

tot_seeds = num_of_players * pits_per_player * seeds_per_pits
# Evaluated pre-config - end

# -- Window --------------------------------------------------------------------

# -- Start screen -------------------------------------------------------------
START_AI_ENGINE_PREFIX = "AI engine:"
START_SKIN_PREFIX      = "Skin:"
START_WHO_FIRST        = "Who goes first?"
START_BTN_HUMAN     = "  ME  "
START_BTN_AI        = "  THE MACHINE  "
START_RULES_HINT    = (
    str(tot_seeds) + " seeds - " + str(pits_per_player) + " pits each - First to capture " + str(min_to_win) + "+ seeds wins\n"
    "Double-click one of your pits to play"
)

# -- In-game buttons -----------------------------------------------------------
BTN_NEW_GAME        = "New Game"
BTN_GET_HINT        = "Get Hint"
BTN_SAVE_GAME       = "Save Game"
BTN_LOAD_GAME       = "Load Game"
BTN_EXIT            = "Exit"

# -- Turn / status messages ----------------------------------------------------
STATUS_YOUR_TURN        = "Your turn"
STATUS_AI_TURN          = "Machine's turn"
STATUS_AI_THINKING      = "The machine is thinking..."

# Status bar format strings  (use {human} and {ai} as placeholders)
STATUS_SCORES_TEMPLATE  = "Your turn  -  You: {human}  -  Machine: {ai}"
STATUS_AI_SCORES_TEMPLATE = "Machine's turn  -  You: {human}  -  Machine: {ai}"

# -- Score labels on the board ------------------------------------------------
SCORE_HUMAN_LABEL   = "You"      # shown as "You: 12"
SCORE_AI_LABEL      = "Machine"  # shown as "Machine: 8"

# -- Game-over overlay ---------------------------------------------------------
GAMEOVER_HUMAN_WIN  = "YOU WIN!"
GAMEOVER_AI_WIN     = "THE MACHINE WINS"
GAMEOVER_DRAW       = "DRAW"

# Detail line template (use {human} and {ai})
GAMEOVER_DETAIL     = "You: {human} seeds  -  Machine: {ai} seeds"

# Clickable replay text
GAMEOVER_PLAY_AGAIN = "[ Play Again ]"

# -- Menu bar -----------------------------------------------------------------
MENU_FILE_LABEL         = "File"
MENU_NEW_GAME_LABEL     = "New Game"
MENU_LOAD_LABEL         = "Load Game..."
MENU_SAVE_LABEL         = "Save Game..."
MENU_EXIT_LABEL         = "Exit"
MENU_UTILITIES_LABEL    = "Utilities"
MENU_GET_HINT_LABEL     = "Get Hint"
MENU_HELP_LABEL         = "Help"
MENU_ABOUT_LABEL        = "About..."

# -- Save / Load dialogs -------------------------------------------------------
SAVE_DIALOG_TITLE       = "Save Game"
SAVE_FILETYPE_DESC      = "Game saved files"
GAME_FILETYPE_EXT       = "mancala"
SAVE_SUCCESS_MSG        = "Game saved."
SAVE_ERROR_TITLE        = "Save error"
SAVE_ERROR_MSG          = "Could not save the game:\n{error}"

LOAD_DIALOG_TITLE       = "Load Saved Game"
LOAD_FILETYPE_DESC      = "Game saved files"
LOAD_ERROR_TITLE        = "Load error"
LOAD_ERROR_MSG          = "Could not load the game:\n{error}"

# -- Start screen - load button ------------------------------------------------
START_BTN_LOAD          = "  Load Saved Game  "

# -- About dialog --------------------------------------------------------------
ABOUT_DESCRIPTION   = (
    "A classic West-African strategy game.\n"
    "Capture " + str(min_to_win) + " or more seeds to win.\n\n"
    "Rules used: " + getRulesDesc() + "\n"
    "  - " + str(tot_seeds) + " seeds, " + str(pits_per_player) + " pits per player\n"
    "  - Counter-clockwise sowing\n"
    "  - Capture on " + str(capt_thresh_desc) + " seeds\n"
    "  - Feeding rule enforced\n"
    "  - Grand-slam rule enforced"
)
ABOUT_AI_NOTE       = "AI: minimax + alpha-beta pruning (depth configurable in config_game.py)"
ABOUT_TECH          = "Built with Python + tkinter/matplotlib"
ABOUT_CLOSE_BTN     = "Close"

# -- Board turn indicator (centre of board) -----------------------------------
TURN_LABEL_HUMAN    = "Your turn"
TURN_LABEL_AI       = "The machine is thinking..."
TURN_LABEL_HUMAN_WIN = "YOU WIN!"
TURN_LABEL_AI_WIN   = "THE MACHINE WINS"
TURN_LABEL_DRAW     = "DRAW"


# Evaluated after config
ABOUT_TITLE         = "About " + getSWName()
ABOUT_GAME_NAME     = getSWName()
ABOUT_VERSION       = "v. " + getVersion()
START_TITLE         = getSWName()
START_SUBTITLE      = "The " + getSWName() + " Game"
WINDOW_TITLE        = getSWName() + " " + ABOUT_VERSION

SAVE_FILETYPE_EXT       = "*." + GAME_FILETYPE_EXT
LOAD_FILETYPE_EXT       = "*." + GAME_FILETYPE_EXT

# -- Stats window --------------------------------------------------------------

STATS_TITLE              = "Game Summary"

STATS_SECTION_OUTCOME    = "OUTCOME"
STATS_SECTION_MOVE_QA    = "MOVE QUALITY"
STATS_SECTION_AI         = "AI BEHAVIOUR"
STATS_SECTION_TEMPORAL   = "TEMPORAL"

STATS_LBL_WINNER         = "Winner"
STATS_LBL_FINAL_SCORE    = "Final score"
STATS_LBL_ENDED_BY       = "Game ended by"
STATS_LBL_HALF_MOVES     = "Total half-moves"
STATS_LBL_LEAD_CHANGES   = "Seed lead changes"
STATS_LBL_MAX_HUMAN      = "Max human lead"
STATS_LBL_MAX_AI         = "Max machine lead"

STATS_LBL_HINT_REQ       = "Hint requests"
STATS_LBL_HINTS_FOLLOW   = "Hints followed"
STATS_LBL_MISSED         = "Missed opportunities"
STATS_LBL_AVG_CAPTURES   = "Avg captures / move"

STATS_LBL_AVG_MINIMAX    = "Avg minimax score"
STATS_LBL_GRAND_SLAM     = "Grand-slam triggers"
STATS_LBL_FORCED         = "Forced moves (1 option)"

STATS_LBL_AVG_THINK      = "Avg AI compute time"
STATS_LBL_SLOWEST        = "Slowest AI move"
STATS_LBL_DURATION       = "Game duration"

STATS_WINNER_HUMAN       = "Human"
STATS_WINNER_AI          = "Machine"
STATS_WINNER_DRAW        = "Draw"

STATS_SCORE_FMT          = "You {h}  -  Machine {a}"
STATS_SEEDS_FMT          = "+{n} seeds"
STATS_HINTS_FMT          = "{f} / {t}  ({p}%)"
STATS_MISSED_FMT         = "{n}  (avg gap: {gap:.0f} pts)"
STATS_CAPTURES_FMT       = "You {h:.1f}  -  Machine {a:.1f}"
STATS_MINIMAX_FMT        = "{s:+.1f}  (>0 = machine advantaged)"
STATS_THINK_FMT          = "{t:.2f} s"
STATS_SLOWEST_FMT        = "{t:.2f} s  (move #{n})"
STATS_DURATION_FMT_S     = "{s} s"
STATS_DURATION_FMT_M     = "{m} min {s:02d} s"

STATS_ENDED_WIN          = "Win threshold (>= {n} seeds)"
STATS_ENDED_CYCLE        = "Cycle limit reached"
STATS_ENDED_NO_MOVES     = "No legal moves"

STATS_CLOSE_BTN          = "  Close  "

STATS_SECTION_TRAJECTORY = "TRAJECTORY"
STATS_CHART_XLABEL       = "Half-move"
STATS_CHART_YLABEL       = "Differential (human - machine)"
