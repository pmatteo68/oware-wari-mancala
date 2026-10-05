"""
Forest skin.
Deep greens and earthy bark browns - like looking down at a forest floor.
"""

SKIN_NAME = "Forest"

# -- Window --------------------------------------------------------------------
WINDOW_WIDTH  = 920
WINDOW_HEIGHT = 580
WINDOW_RESIZABLE     = False
LAYOUT_INIT_DELAY_MS = 10

# -- Background & board -------------------------------------------------------
BG_COLOR          = "#eaf2e4"   # pale leafy green canvas
BOARD_COLOR       = "#2a5028"   # deep forest green board fill
BOARD_BORDER      = "#4a3018"   # dark bark brown border
BOARD_RADIUS      = 24
BOARD_CANVAS_PAD  = 24
BOARD_OUTLINE_WIDTH = 3
BOARD_DIVIDER_WIDTH = 2
BOARD_SIDE_PAD    = 40
BOARD_VERT_PAD    = 30

# Player-side tint strips
HUMAN_SIDE_TINT   = "#d8ecd0"   # light fern for human side
AI_SIDE_TINT      = "#e0dcc8"   # light sandy earth for AI side

# -- Pits ---------------------------------------------------------------------
PIT_SHAPE          = "oval"
PIT_W              = 92
PIT_H              = 92
PIT_SPACING        = 10

PIT_COLOR_IDLE     = "#4a8830"  # vivid moss green - human pits
PIT_COLOR_HOVER    = "#68a848"  # lighter green on hover
PIT_COLOR_SELECTED = "#c8e880"  # bright lime - selected pit
PIT_COLOR_EMPTY    = "#c0b890"  # dry earth - empty pit
PIT_COLOR_AI_IDLE  = "#7a5028"  # bark brown - AI pits
PIT_COLOR_CAPTURE  = "#c02820"  # deep red capture flash
PIT_RECT_RADIUS    = 10
PIT_OUTLINE        = "#2a3810"  # very dark forest outline
PIT_OUTLINE_WIDTH  = 2

# -- Seeds ---------------------------------------------------------------------
SEED_RADIUS = 7

SEED_PALETTE = [
    "#3a7820",  # deep leaf green
    "#7a5020",  # bark brown
    "#5a9030",  # vivid moss
    "#c8a040",  # golden acorn
    "#284018",  # very dark forest
    "#a07838",  # warm chestnut
    "#90b840",  # lime-green leaf
    "#603818",  # deep bark
]

SEED_OUTLINE       = "#1a2808"
SEED_OUTLINE_WIDTH = 1

# -- Scores & labels ----------------------------------------------------------
SCORE_INSET        = 18
SCORE_FONT         = ("Helvetica", 22, "bold")
SCORE_COLOR        = "#2a3810"   # very dark forest green scores
LABEL_FONT         = ("Helvetica", 11)
LABEL_COLOR        = "#3a4820"   # dark forest label text
TURN_FONT          = ("Helvetica", 13, "bold")
TURN_COLOR_HUMAN   = "#2a6018"   # deep forest green for human turn
TURN_COLOR_AI      = "#6a3810"   # bark brown for AI turn
TURN_COLOR_NONE    = "#7a8870"

# Pit index labels
SHOW_PIT_LABELS    = False
PIT_LABEL_FONT     = ("Helvetica", 8)
PIT_LABEL_COLOR    = "#88a870"
PIT_LABEL_GAP      = 8

# -- Status bar ---------------------------------------------------------------
STATUS_BAR_HEIGHT   = 36
STATUS_BG           = "#d8e8d0"  # light fern status bar
STATUS_FONT         = ("Helvetica", 12)
STATUS_COLOR        = "#2a3810"  # dark forest text
STATUS_BTN_PADX     = 4
STATUS_BTN_PADX_END = 8
STATUS_BTN_PADY     = 4
STATUS_LABEL_PADX   = 12

# -- Buttons ------------------------------------------------------------------
BTN_BG             = "#3a6820"   # deep forest green
BTN_FG             = "#e8f0d8"
BTN_ACTIVE_BG      = "#508830"   # lighter green on hover
BTN_FONT           = ("Helvetica", 12, "bold")
BTN_RELIEF         = "flat"
BTN_PADX           = 18
BTN_PADY           = 7
BTN_BD             = 0
MENU_BD            = 0

# -- Start screen -------------------------------------------------------------
START_TITLE_FONT      = ("Helvetica", 30, "bold")
START_TITLE_COLOR     = "#2a4810"   # deep dark forest title
START_SUBTITLE_FONT   = ("Helvetica", 14)
START_SUBTITLE_COLOR  = "#3a4820"
START_ENGINE_PADY     = 8
START_TITLE_PADY      = 6
START_SUBTITLE_PADY   = 30
START_WHO_FIRST_PADY  = 14
START_BTN_PADX        = 10
START_RULES_PADY      = 30
START_BOTTOM_ROW_PADY = 16
START_INFO_GAP        = 30

# -- Animation blink colours --------------------------------------------------
BLINK_COLOR_A      = "#c8e880"   # bright lime blink for human
BLINK_COLOR_B      = PIT_COLOR_SELECTED
AI_BLINK_COLOR_A   = "#c0a060"   # warm amber blink for AI
AI_BLINK_COLOR_B   = "#7a5028"

RECEIVE_FLASH_COLOR = "#f0f8e8"

# -- Seed count font inside pits ----------------------------------------------
SEED_COUNT_FONT    = ("Helvetica", 16, "bold")
SEED_COUNT_COLOR   = "#e8f0d8"
SEED_COUNT_SHADOW  = "#101808"

# -- Hint animation ------------------------------------------------------------
HINT_BLINK_COUNT       = 4
HINT_BLINK_INTERVAL_MS = 250
HINT_BLINK_COLOR_A     = "#a8e060"   # vivid lime-green lit state
HINT_BLINK_COLOR_B     = "#d8f0a0"   # pale green dim state
HINT_TOOLTIP_BG        = "#f0f8e0"   # pale leafy tooltip background
HINT_TOOLTIP_FG        = "#1a2808"   # very dark forest tooltip text
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
STATS_CHART_GRID_COLOR  = "#c8d8b8"
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
