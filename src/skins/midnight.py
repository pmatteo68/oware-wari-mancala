"""
Midnight skin.
Full dark mode: near-black canvas with electric purple and indigo accents.
"""

SKIN_NAME = "Midnight"

# -- Window --------------------------------------------------------------------
WINDOW_WIDTH  = 920
WINDOW_HEIGHT = 580
WINDOW_RESIZABLE     = False
LAYOUT_INIT_DELAY_MS = 10

# -- Background & board -------------------------------------------------------
BG_COLOR          = "#0c0c18"   # near-black with a breath of indigo
BOARD_COLOR       = "#14142a"   # very dark indigo board fill
BOARD_BORDER      = "#7030d8"   # electric purple border
BOARD_RADIUS      = 24
BOARD_CANVAS_PAD  = 24
BOARD_OUTLINE_WIDTH = 3
BOARD_DIVIDER_WIDTH = 2
BOARD_SIDE_PAD    = 40
BOARD_VERT_PAD    = 30

# Player-side tint strips
HUMAN_SIDE_TINT   = "#18102a"   # very dark purple for human side
AI_SIDE_TINT      = "#101820"   # very dark blue-black for AI side

# -- Pits ---------------------------------------------------------------------
PIT_SHAPE          = "oval"
PIT_W              = 92
PIT_H              = 92
PIT_SPACING        = 10

PIT_COLOR_IDLE     = "#8030f0"  # electric violet - human pits
PIT_COLOR_HOVER    = "#a060f8"  # lighter violet on hover
PIT_COLOR_SELECTED = "#e0a0ff"  # pale violet - selected pit
PIT_COLOR_EMPTY    = "#1a1830"  # very dark indigo - empty pit
PIT_COLOR_AI_IDLE  = "#3030a0"  # deep indigo - AI pits
PIT_COLOR_CAPTURE  = "#ff2060"  # vivid hot-pink capture flash
PIT_RECT_RADIUS    = 10
PIT_OUTLINE        = "#c060ff"  # bright electric purple outline
PIT_OUTLINE_WIDTH  = 2

# -- Seeds ---------------------------------------------------------------------
SEED_RADIUS = 7

SEED_PALETTE = [
    "#a040ff",  # electric violet
    "#6030d0",  # deep indigo
    "#d060ff",  # bright purple
    "#4040c0",  # royal indigo
    "#ff40e0",  # vivid magenta
    "#8060e8",  # soft violet
    "#c080ff",  # pale electric purple
    "#2040a8",  # deep blue-indigo
]

SEED_OUTLINE       = "#200840"
SEED_OUTLINE_WIDTH = 1

# -- Scores & labels ----------------------------------------------------------
SCORE_INSET        = 18
SCORE_FONT         = ("Helvetica", 22, "bold")
SCORE_COLOR        = "#c060ff"   # electric purple scores
LABEL_FONT         = ("Helvetica", 11)
LABEL_COLOR        = "#a080d0"   # muted lavender labels
TURN_FONT          = ("Helvetica", 13, "bold")
TURN_COLOR_HUMAN   = "#c060ff"   # electric purple for human turn
TURN_COLOR_AI      = "#6060e0"   # deep indigo for AI turn
TURN_COLOR_NONE    = "#505068"

# Pit index labels
SHOW_PIT_LABELS    = False
PIT_LABEL_FONT     = ("Helvetica", 8)
PIT_LABEL_COLOR    = "#504870"
PIT_LABEL_GAP      = 8

# -- Status bar ---------------------------------------------------------------
STATUS_BAR_HEIGHT   = 36
STATUS_BG           = "#0a0a18"  # near-black status bar
STATUS_FONT         = ("Helvetica", 12)
STATUS_COLOR        = "#a080d0"  # muted lavender text
STATUS_BTN_PADX     = 4
STATUS_BTN_PADX_END = 8
STATUS_BTN_PADY     = 4
STATUS_LABEL_PADX   = 12

# -- Buttons ------------------------------------------------------------------
BTN_BG             = "#6020c0"   # deep electric purple
BTN_FG             = "#f0e0ff"
BTN_ACTIVE_BG      = "#8040e0"   # lighter purple on hover
BTN_FONT           = ("Helvetica", 12, "bold")
BTN_RELIEF         = "flat"
BTN_PADX           = 18
BTN_PADY           = 7
BTN_BD             = 0
MENU_BD            = 0

# -- Start screen -------------------------------------------------------------
START_TITLE_FONT      = ("Helvetica", 30, "bold")
START_TITLE_COLOR     = "#c060ff"   # electric purple title
START_SUBTITLE_FONT   = ("Helvetica", 14)
START_SUBTITLE_COLOR  = "#a080d0"
START_ENGINE_PADY     = 8
START_TITLE_PADY      = 6
START_SUBTITLE_PADY   = 30
START_WHO_FIRST_PADY  = 14
START_BTN_PADX        = 10
START_RULES_PADY      = 30
START_BOTTOM_ROW_PADY = 16
START_INFO_GAP        = 30

# -- Animation blink colours --------------------------------------------------
BLINK_COLOR_A      = "#e0a0ff"   # pale violet blink for human
BLINK_COLOR_B      = PIT_COLOR_SELECTED
AI_BLINK_COLOR_A   = "#6060e0"   # indigo blink for AI
AI_BLINK_COLOR_B   = "#3030a0"

RECEIVE_FLASH_COLOR = "#e0c0ff"

# -- Seed count font inside pits ----------------------------------------------
SEED_COUNT_FONT    = ("Helvetica", 16, "bold")
SEED_COUNT_COLOR   = "#f0e0ff"
SEED_COUNT_SHADOW  = "#100020"

# -- Hint animation ------------------------------------------------------------
HINT_BLINK_COUNT       = 4
HINT_BLINK_INTERVAL_MS = 250
HINT_BLINK_COLOR_A     = "#e040ff"   # vivid magenta lit state
HINT_BLINK_COLOR_B     = "#a020c0"   # deep purple dim state
HINT_TOOLTIP_BG        = "#18102a"   # very dark purple tooltip background
HINT_TOOLTIP_FG        = "#e0c0ff"   # pale lavender tooltip text
HINT_TOOLTIP_GAP       = 36
HINT_TOOLTIP_PADX      = 8
HINT_TOOLTIP_PADY      = 5
HINT_TOOLTIP_BD        = 1

# -- Stats window --------------------------------------------------------------
STATS_WINDOW_WIDTH      = 460
STATS_PADDING           = 18
STATS_TITLE_PADY_BOT    = 10
STATS_CLOSE_SPACER_H    = 6
STATS_SECTION_BG        = BTN_BG
STATS_SECTION_FG        = BTN_FG
STATS_SECTION_FONT      = ("Helvetica", 10, "bold")
STATS_SECTION_PADY      = 6
STATS_ROW_LABEL_FONT    = ("Helvetica", 11)
STATS_ROW_VALUE_FONT    = ("Helvetica", 11, "bold")
STATS_ROW_LABEL_COLOR   = STATUS_COLOR
STATS_ROW_VALUE_COLOR   = SCORE_COLOR
STATS_ROW_PADX          = 14
STATS_ROW_PADY          = 2
STATS_DIVIDER_COLOR     = BOARD_BORDER
STATS_TITLE_FONT        = START_TITLE_FONT
STATS_TITLE_COLOR       = START_TITLE_COLOR
STATS_DELAY_MS          = 500

# -- Stats trajectory chart (matplotlib) ---------------------------------------
STATS_SHOW_CHART        = True
STATS_CHART_HEIGHT_IN   = 2.8
STATS_CHART_DPI         = 88
STATS_CHART_BG          = BG_COLOR
STATS_CHART_HUMAN_COLOR = BTN_BG
STATS_CHART_AI_COLOR    = PIT_COLOR_AI_IDLE
STATS_CHART_LINE_COLOR  = SCORE_COLOR
STATS_CHART_ZERO_COLOR  = BOARD_BORDER
STATS_CHART_GRID_COLOR  = "#1a1830"
STATS_CHART_FILL_ALPHA  = 0.35
STATS_CHART_LINE_WIDTH  = 1.6
STATS_CHART_ZERO_WIDTH  = 1.0
STATS_CHART_FONT_SIZE   = 7
STATS_CHART_LABEL_PAD   = 2
STATS_CHART_TICK_LENGTH = 3
STATS_CHART_TICK_PAD    = 2
STATS_CHART_SPINE_WIDTH = 0.8
STATS_CHART_GRID_WIDTH  = 0.5
STATS_CHART_LAYOUT_PAD  = 0.6

# -- Game-over overlay text offsets -------------------------------------------
GAMEOVER_MSG_OFFSET_Y    = -20
GAMEOVER_DETAIL_OFFSET_Y =  28
GAMEOVER_ACTION_OFFSET_Y =  80

# -- About dialog position and layout -----------------------------------------
ABOUT_OFFSET_X            = 220
ABOUT_OFFSET_Y            = 170
ABOUT_PADX                = 24
ABOUT_PADY                = 6
ABOUT_TITLE_PADY_TOP      = 20
ABOUT_DIVIDER_PADX        = 20
ABOUT_HEADER_DIVIDER_PADY = 10
ABOUT_BODY_DIVIDER_PADY   = 6
ABOUT_WRAP_WIDTH          = 400
ABOUT_CLOSE_PADY_TOP      = 10
ABOUT_CLOSE_PADY_BOT      = 20

# -- Seed ring geometry (visual layout, not game rules) -----------------------
SEED_RING1_CAPACITY   = 6
SEED_RING1_THRESHOLD  = 7
SEED_RING2_CAPACITY   = 8
SEED_RING1_RADIUS_MUL = 1.6
SEED_RING2_RADIUS_MUL = 3.1
