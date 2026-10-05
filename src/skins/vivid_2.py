"""
Vivid-2 skin.
High-energy blue palette: electric cobalt human pits, vivid cyan AI pits,
deep-blue board, bright-blue buttons.
"""

SKIN_NAME = "Vivid-2"

# -- Window --------------------------------------------------------------------
WINDOW_WIDTH  = 920
WINDOW_HEIGHT = 580
WINDOW_RESIZABLE     = False
LAYOUT_INIT_DELAY_MS = 10

# -- Background & board -------------------------------------------------------
BG_COLOR          = "#eef4ff"   # very pale blue canvas
BOARD_COLOR       = "#6090d8"   # vivid medium blue board fill
BOARD_BORDER      = "#0040b0"   # deep vivid blue border
BOARD_RADIUS      = 24
BOARD_CANVAS_PAD  = 24
BOARD_OUTLINE_WIDTH = 3
BOARD_DIVIDER_WIDTH = 2
BOARD_SIDE_PAD    = 40
BOARD_VERT_PAD    = 30

# Player-side tint strips
HUMAN_SIDE_TINT   = "#cce0ff"   # light cobalt for human side
AI_SIDE_TINT      = "#c0f0fc"   # light cyan for AI side

# -- Pits ---------------------------------------------------------------------
PIT_SHAPE          = "oval"
PIT_W              = 92
PIT_H              = 92
PIT_SPACING        = 10

PIT_COLOR_IDLE     = "#1c6ee8"  # vivid cobalt blue - human pits
PIT_COLOR_HOVER    = "#4898f8"  # lighter cobalt on hover
PIT_COLOR_SELECTED = "#80d8ff"  # bright cyan - selected pit
PIT_COLOR_EMPTY    = "#a8c4e8"  # muted steel blue - empty pit
PIT_COLOR_AI_IDLE  = "#00aadd"  # vivid cyan - AI pits
PIT_COLOR_CAPTURE  = "#ff2828"  # vivid red capture flash (kept vivid for clarity)
PIT_RECT_RADIUS    = 10
PIT_OUTLINE        = "#003088"  # deep navy outline
PIT_OUTLINE_WIDTH  = 2

# -- Seeds ---------------------------------------------------------------------
SEED_RADIUS = 7

SEED_PALETTE = [
    "#1060e8",  # vivid cobalt
    "#00aadd",  # vivid cyan
    "#40d0f0",  # bright sky blue
    "#8060e8",  # vivid indigo
    "#0088bb",  # vivid teal-blue
    "#60a0ff",  # bright periwinkle
    "#00ccee",  # vivid light cyan
    "#a080ff",  # vivid violet-blue
]

SEED_OUTLINE       = "#002266"
SEED_OUTLINE_WIDTH = 1

# -- Scores & labels ----------------------------------------------------------
SCORE_INSET        = 18
SCORE_FONT         = ("Helvetica", 22, "bold")
SCORE_COLOR        = "#002888"   # deep vivid blue scores
LABEL_FONT         = ("Helvetica", 11)
LABEL_COLOR        = "#003a8a"   # dark blue label text
TURN_FONT          = ("Helvetica", 13, "bold")
TURN_COLOR_HUMAN   = "#0040cc"   # vivid deep cobalt for human turn
TURN_COLOR_AI      = "#0099cc"   # vivid cyan for AI turn
TURN_COLOR_NONE    = "#7090b0"

# Pit index labels
SHOW_PIT_LABELS    = False
PIT_LABEL_FONT     = ("Helvetica", 8)
PIT_LABEL_COLOR    = "#80a8cc"
PIT_LABEL_GAP      = 8

# -- Status bar ---------------------------------------------------------------
STATUS_BAR_HEIGHT   = 36
STATUS_BG           = "#d8eaff"  # pale blue status bar
STATUS_FONT         = ("Helvetica", 12)
STATUS_COLOR        = "#003070"  # dark blue text
STATUS_BTN_PADX     = 4
STATUS_BTN_PADX_END = 8
STATUS_BTN_PADY     = 4
STATUS_LABEL_PADX   = 12

# -- Buttons ------------------------------------------------------------------
BTN_BG             = "#1060e0"   # vivid blue
BTN_FG             = "#ffffff"
BTN_ACTIVE_BG      = "#3080f8"   # lighter vivid blue on hover
BTN_FONT           = ("Helvetica", 12, "bold")
BTN_RELIEF         = "flat"
BTN_PADX           = 18
BTN_PADY           = 7
BTN_BD             = 0
MENU_BD            = 0

# -- Start screen -------------------------------------------------------------
START_TITLE_FONT      = ("Helvetica", 30, "bold")
START_TITLE_COLOR     = "#0040cc"   # vivid deep blue title
START_SUBTITLE_FONT   = ("Helvetica", 14)
START_SUBTITLE_COLOR  = "#003a8a"
START_ENGINE_PADY     = 8
START_TITLE_PADY      = 6
START_SUBTITLE_PADY   = 30
START_WHO_FIRST_PADY  = 14
START_BTN_PADX        = 10
START_RULES_PADY      = 30
START_BOTTOM_ROW_PADY = 16
START_INFO_GAP        = 30

# -- Animation blink colours --------------------------------------------------
BLINK_COLOR_A      = "#80d8ff"   # bright cyan blink for human
BLINK_COLOR_B      = PIT_COLOR_SELECTED
AI_BLINK_COLOR_A   = "#40f0f8"   # vivid aqua blink for AI
AI_BLINK_COLOR_B   = "#00aadd"

RECEIVE_FLASH_COLOR = "#ffffff"

# -- Seed count font inside pits ----------------------------------------------
SEED_COUNT_FONT    = ("Helvetica", 16, "bold")
SEED_COUNT_COLOR   = "#ffffff"
SEED_COUNT_SHADOW  = "#001844"

# -- Hint animation ------------------------------------------------------------
HINT_BLINK_COUNT       = 4
HINT_BLINK_INTERVAL_MS = 250
HINT_BLINK_COLOR_A     = "#40e8ff"   # vivid cyan lit state
HINT_BLINK_COLOR_B     = "#b0f0ff"   # pale cyan dim state
HINT_TOOLTIP_BG        = "#e0f4ff"   # very pale blue tooltip background
HINT_TOOLTIP_FG        = "#001844"   # deep navy tooltip text
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
STATS_CHART_GRID_COLOR  = "#c0d8f0"
STATS_CHART_FILL_ALPHA  = 0.30
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
