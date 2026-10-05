"""
Default skin.
Warm cream tones with terracotta and sky-blue accents.
"""

SKIN_NAME = "Default"

# -- Window --------------------------------------------------------------------
WINDOW_WIDTH  = 920
WINDOW_HEIGHT = 580
WINDOW_RESIZABLE     = False  # set True to allow free resize
LAYOUT_INIT_DELAY_MS = 10    # ms before the first layout pass fires after widget creation

# -- Background & board -------------------------------------------------------
BG_COLOR          = "#fdf6ee"   # warm cream canvas background
BOARD_COLOR       = "#f0d9b5"   # light tan board fill
BOARD_BORDER      = "#c8a870"   # board border / outline
BOARD_RADIUS      = 24          # corner rounding of the board rectangle
BOARD_CANVAS_PAD  = 24          # gap from canvas edge to board rectangle
BOARD_OUTLINE_WIDTH = 3         # stroke width for the board polygon outline
BOARD_DIVIDER_WIDTH = 2         # stroke width for the horizontal divider between player sides
BOARD_SIDE_PAD    = 40          # horizontal padding inside board edges
BOARD_VERT_PAD    = 30          # vertical padding inside board edges

# Player-side tint strips (subtle colour band for each side)
HUMAN_SIDE_TINT   = "#ffe8d6"   # soft peach for human side
AI_SIDE_TINT      = "#daeaf7"   # soft sky-blue for AI side

# -- Pits ---------------------------------------------------------------------
PIT_SHAPE          = "oval"     # "oval"  or  "rect" (rounded rectangle)
PIT_W              = 92         # pit width  (for "rect") / horizontal diameter (for "oval")
PIT_H              = 92         # pit height / vertical diameter
PIT_SPACING        = 10         # gap between adjacent pits

PIT_COLOR_IDLE     = "#e8956d"  # human pit - warm terracotta pastel
PIT_COLOR_HOVER    = "#f4b08a"  # mouse-over highlight
PIT_COLOR_SELECTED = "#ffe066"  # after double-click (source pit, before animation)
PIT_COLOR_EMPTY    = "#e0cdb8"  # pit with 0 seeds
PIT_COLOR_AI_IDLE  = "#7ab8d9"  # AI pit - soft sky blue
PIT_COLOR_CAPTURE  = "#f06090"  # pit about to be captured (flash)
PIT_RECT_RADIUS    = 10         # corner radius for "rect" pit shape
PIT_OUTLINE        = "#b8956a"
PIT_OUTLINE_WIDTH  = 2

# -- Seeds ---------------------------------------------------------------------
SEED_RADIUS = 7                # radius of each seed circle drawn inside a pit

# Cheerful pastel seed palette
SEED_PALETTE = [
    "#ff8fa3",  # pastel rose
    "#ffb347",  # pastel orange
    "#ffe066",  # pastel yellow
    "#90ee90",  # pastel green
    "#87ceeb",  # pastel sky blue
    "#c9a0dc",  # pastel lavender
    "#f4a0c0",  # pastel pink
    "#80ded9",  # pastel mint
]

SEED_OUTLINE       = "#888888"    # outline on seeds (tkinter: 6-digit hex only)
SEED_OUTLINE_WIDTH = 1

# -- Scores & labels ----------------------------------------------------------
SCORE_INSET        = 18          # inset of score text from board edges
SCORE_FONT         = ("Helvetica", 22, "bold")
SCORE_COLOR        = "#a0521c"   # warm brown - readable on light board
LABEL_FONT         = ("Helvetica", 11)
LABEL_COLOR        = "#7a5c3a"
TURN_FONT          = ("Helvetica", 13, "bold")
TURN_COLOR_HUMAN   = "#2a72b0"   # deep sky blue
TURN_COLOR_AI      = "#c0402a"   # warm coral red
TURN_COLOR_NONE    = "#888888"

# Pit index labels (show pit number, useful for debugging; set False to hide)
SHOW_PIT_LABELS    = False
PIT_LABEL_FONT     = ("Helvetica", 8)
PIT_LABEL_COLOR    = "#aaaaaa"
PIT_LABEL_GAP      = 8          # pixels above pit top edge where the debug label sits

# -- Status bar ---------------------------------------------------------------
STATUS_BAR_HEIGHT   = 36
STATUS_BG           = "#f5e8d0"  # light warm beige
STATUS_FONT         = ("Helvetica", 12)
STATUS_COLOR        = "#7a4a1a"  # dark warm brown text
STATUS_BTN_PADX     = 4          # horizontal padding inside each status bar button
STATUS_BTN_PADX_END = 8          # extra horizontal gap before the rightmost status bar button
STATUS_BTN_PADY     = 4          # vertical padding inside each status bar button
STATUS_LABEL_PADX   = 12         # horizontal inset for the status text label on the left

# -- Buttons ------------------------------------------------------------------
BTN_BG             = "#e07840"   # warm pumpkin orange
BTN_FG             = "#ffffff"
BTN_ACTIVE_BG      = "#f09050"
BTN_FONT           = ("Helvetica", 12, "bold")
BTN_RELIEF         = "flat"
BTN_PADX           = 18
BTN_PADY           = 7
BTN_BD             = 0          # border width for all game buttons (flat, no visible border)
MENU_BD            = 0          # border width for the menu bar (flat appearance)

# -- Start screen -------------------------------------------------------------
START_TITLE_FONT      = ("Helvetica", 30, "bold")
START_TITLE_COLOR     = "#c05020"  # warm rust / burnt orange
START_SUBTITLE_FONT   = ("Helvetica", 14)
START_SUBTITLE_COLOR  = "#7a5c3a"
START_ENGINE_PADY     = 8          # gap below the AI engine / skin info row
START_TITLE_PADY      = 6          # gap below the main title
START_SUBTITLE_PADY   = 30         # gap below the subtitle text
START_WHO_FIRST_PADY  = 14         # gap below the "who goes first?" prompt
START_BTN_PADX        = 10         # horizontal spacing between the player-choice buttons
START_RULES_PADY      = 30         # top gap above the rules hint text
START_BOTTOM_ROW_PADY = 16         # top gap above the bottom row (Load / Exit buttons)
START_INFO_GAP        = 30         # horizontal gap between AI engine label and skin label on start screen

# -- Animation blink colours --------------------------------------------------
BLINK_COLOR_A      = "#ffe066"   # bright yellow blink for human
BLINK_COLOR_B      = PIT_COLOR_SELECTED
AI_BLINK_COLOR_A   = "#b0d8f0"   # light blue blink for AI
AI_BLINK_COLOR_B   = "#7ab8d9"

# Highlight colour for the pit that just received a seed
RECEIVE_FLASH_COLOR = "#ffffff"

# -- Seed count font inside pits ----------------------------------------------
SEED_COUNT_FONT    = ("Helvetica", 16, "bold")
SEED_COUNT_COLOR   = "#ffffff"
SEED_COUNT_SHADOW  = "#666666"

# -- Hint animation ------------------------------------------------------------
HINT_BLINK_COUNT       = 4      # number of blink half-cycles shown for the hint pit
HINT_BLINK_INTERVAL_MS = 250    # ms between blink state changes
HINT_BLINK_COLOR_A     = "#7de87d"  # bright green - lit state
HINT_BLINK_COLOR_B     = "#c8f5c8"  # pale green - dim state
HINT_TOOLTIP_BG        = "#fffacd"  # lemon chiffon tooltip background
HINT_TOOLTIP_FG        = "#4a3a00"  # dark warm tooltip text
HINT_TOOLTIP_GAP       = 36         # pixels above pit top edge where tooltip appears
HINT_TOOLTIP_PADX      = 8          # internal horizontal padding of the tooltip label
HINT_TOOLTIP_PADY      = 5          # internal vertical padding of the tooltip label
HINT_TOOLTIP_BD        = 1          # border width of the tooltip frame (thin visible outline)

# -- Stats window --------------------------------------------------------------
STATS_WINDOW_WIDTH      = 460           # minimum width of the stats dialog
STATS_PADDING           = 18            # outer padding around content
STATS_TITLE_PADY_BOT    = 10            # gap below the stats window title
STATS_CLOSE_SPACER_H    = 6             # height of the spacer frame above the close button
STATS_SECTION_BG        = BTN_BG        # section header background (warm orange)
STATS_SECTION_FG        = BTN_FG        # section header text (white)
STATS_SECTION_FONT      = ("Helvetica", 10, "bold")
STATS_SECTION_PADY      = 6             # top gap before each section header
STATS_ROW_LABEL_FONT    = ("Helvetica", 11)
STATS_ROW_VALUE_FONT    = ("Helvetica", 11, "bold")
STATS_ROW_LABEL_COLOR   = STATUS_COLOR  # dark warm brown
STATS_ROW_VALUE_COLOR   = SCORE_COLOR   # warm brown bold
STATS_ROW_PADX          = 14            # left/right row inset
STATS_ROW_PADY          = 2             # top/bottom row padding
STATS_DIVIDER_COLOR     = BOARD_BORDER  # thin separator line after each section
STATS_TITLE_FONT        = START_TITLE_FONT
STATS_TITLE_COLOR       = START_TITLE_COLOR
STATS_DELAY_MS          = 500           # delay before stats window appears after game ends

# -- Stats trajectory chart (matplotlib) ---------------------------------------
STATS_SHOW_CHART        = True          # set False to hide the trajectory chart entirely
STATS_CHART_HEIGHT_IN   = 2.8           # chart height in inches
STATS_CHART_DPI         = 88            # chart resolution (dots per inch)
STATS_CHART_BG          = BG_COLOR      # chart + axes background (matches window)
STATS_CHART_HUMAN_COLOR = BTN_BG        # fill color when human is leading
STATS_CHART_AI_COLOR    = PIT_COLOR_AI_IDLE  # fill color when machine is leading
STATS_CHART_LINE_COLOR  = SCORE_COLOR   # main differential line
STATS_CHART_ZERO_COLOR  = BOARD_BORDER  # zero reference dashed line
STATS_CHART_GRID_COLOR  = "#e8d8c0"     # subtle grid lines
STATS_CHART_FILL_ALPHA  = 0.30          # opacity of the shaded fill areas above and below zero
STATS_CHART_LINE_WIDTH  = 1.6           # stroke width of the main differential line
STATS_CHART_ZERO_WIDTH  = 1.0           # stroke width of the zero reference dashed line
STATS_CHART_FONT_SIZE   = 7             # font size for axis labels and tick mark numbers
STATS_CHART_LABEL_PAD   = 2             # gap in points between axis label text and the axis
STATS_CHART_TICK_LENGTH = 3             # length of tick marks on both axes
STATS_CHART_TICK_PAD    = 2             # gap between tick marks and their label text
STATS_CHART_SPINE_WIDTH = 0.8           # stroke width for the visible bottom and left spines
STATS_CHART_GRID_WIDTH  = 0.5           # stroke width for the background grid lines
STATS_CHART_LAYOUT_PAD  = 0.6           # figure border padding passed to tight_layout (inches)

# -- Game-over overlay text offsets (pixels relative to canvas centre) --------
GAMEOVER_MSG_OFFSET_Y    = -20   # winner message: above centre
GAMEOVER_DETAIL_OFFSET_Y =  28   # detail line: below centre
GAMEOVER_ACTION_OFFSET_Y =  80   # "play again" text: further below

# -- About dialog position and layout -----------------------------------------
ABOUT_OFFSET_X            = 220  # horizontal offset used to centre the dialog over the main window
ABOUT_OFFSET_Y            = 170  # vertical offset used to centre the dialog over the main window
ABOUT_PADX                = 24   # horizontal padding for content labels
ABOUT_PADY                = 6    # vertical padding for content labels
ABOUT_TITLE_PADY_TOP      = 20   # top gap above the about dialog title
ABOUT_DIVIDER_PADX        = 20   # horizontal inset for the divider lines
ABOUT_HEADER_DIVIDER_PADY = 10   # vertical gap around the divider below the version label
ABOUT_BODY_DIVIDER_PADY   = 6    # vertical gap around the divider between content sections
ABOUT_WRAP_WIDTH          = 400  # text wrap width for the AI note label
ABOUT_CLOSE_PADY_TOP      = 10   # top gap above the close button
ABOUT_CLOSE_PADY_BOT      = 20   # bottom gap below the close button

# -- Seed ring geometry (visual layout, not game rules) -----------------------
SEED_RING1_CAPACITY   = 6    # positions in ring 1 (hexagonal neighbour ring)
SEED_RING1_THRESHOLD  = 7    # ring 1 full: 1 centre + SEED_RING1_CAPACITY
SEED_RING2_CAPACITY   = 8    # positions in ring 2
SEED_RING1_RADIUS_MUL = 1.6  # ring 1 radius as a multiple of SEED_RADIUS
SEED_RING2_RADIUS_MUL = 3.1  # ring 2 radius as a multiple of SEED_RADIUS
