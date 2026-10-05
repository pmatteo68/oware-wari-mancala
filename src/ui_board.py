"""
Canvas-based board widget.
Draws the Oware board, handles mouse events, and runs seed animations.
Completely decoupled from game logic: it only reads Board state and
calls a callback when the human has picked a valid move.
"""

import logging
import tkinter as tk
import math
from game_logic import Board, HUMAN, AI, player_pits, TOTAL_PITS
import config_ui   as C
import config_game as CG
import config_text as T

logger = logging.getLogger(__name__)


# -- Geometry helpers ----------------------------------------------------------

def _pit_center(col: int, row: int, board_x: int, board_y: int,
                board_w: int, board_h: int, n_cols: int) -> tuple[float, float]:
    """
    col  : 0-(num_pits_per_player-1) (left->right for both rows)
    row  : 0 = AI (top),  1 = Human (bottom)
    Returns absolute canvas (cx, cy).
    """
    usable_w = board_w - 2 * C.BOARD_SIDE_PAD
    cell_w   = usable_w / n_cols
    cx = board_x + C.BOARD_SIDE_PAD + col * cell_w + cell_w / 2

    usable_h = board_h - 2 * C.BOARD_VERT_PAD
    row_h    = usable_h / 2
    cy = board_y + C.BOARD_VERT_PAD + row * row_h + row_h / 2
    return cx, cy


def _pit_display_col(pit: int) -> int:
    """Map pit index -> display column 0-(PITS_PER_PLAYER-1)."""
    if pit < CG.PITS_PER_PLAYER:
        return pit                          # human: pit 0->col 0, pit N-1->col N-1
    return TOTAL_PITS - 1 - pit             # AI:    pit N->col N-1, pit 2N-1->col 0


def _pit_row(pit: int) -> int:
    return 1 if pit < CG.PITS_PER_PLAYER else 0


def _seed_positions(cx: float, cy: float, count: int,
                    radius: int) -> list[tuple[float, float]]:
    """
    Return up to *count* (cx, cy) positions for seeds inside a pit.
    Seeds are arranged in concentric rings so they never overlap.
    """
    if count == 0:
        return []
    positions = []
    # Ring 0: centre
    positions.append((cx, cy))
    if count == 1:
        return positions
    # Ring 1
    ring_r1 = radius * C.SEED_RING1_RADIUS_MUL
    for i in range(min(count - 1, C.SEED_RING1_CAPACITY)):
        angle = 2 * math.pi * i / C.SEED_RING1_CAPACITY - math.pi / 2
        positions.append((cx + ring_r1 * math.cos(angle),
                          cy + ring_r1 * math.sin(angle)))
    if count <= C.SEED_RING1_THRESHOLD:
        return positions[:count]
    # Ring 2: extras
    ring_r2 = radius * C.SEED_RING2_RADIUS_MUL
    for i in range(count - C.SEED_RING1_THRESHOLD):
        angle = 2 * math.pi * i / C.SEED_RING2_CAPACITY - math.pi / 2
        positions.append((cx + ring_r2 * math.cos(angle),
                          cy + ring_r2 * math.sin(angle)))
    return positions[:count]


# -- BoardCanvas ---------------------------------------------------------------

class BoardCanvas(tk.Canvas):
    """
    Tkinter Canvas that renders the Oware board and handles input.

    Callbacks (set by the parent window):
        on_human_move(pit_index)   - called when human double-clicks a valid pit
    """

    def __init__(self, parent, board: Board, on_human_move, **kwargs):
        super().__init__(
            parent,
            width=C.WINDOW_WIDTH,
            height=C.WINDOW_HEIGHT - C.STATUS_BAR_HEIGHT,
            bg=C.BG_COLOR,
            highlightthickness=0,
            **kwargs,
        )
        self.board          = board
        self.on_human_move  = on_human_move
        self._hover_pit: int | None = None
        self._locked        = False        # True while animation running
        self._anim_after_id = None

        # Board rectangle (computed once in _layout)
        self._bx = self._by = self._bw = self._bh = 0

        self.bind("<Motion>",         self._on_mouse_move)
        self.bind("<Double-Button-1>", self._on_double_click)
        self.bind("<Configure>",      lambda _: self._layout())
        self.after(C.LAYOUT_INIT_DELAY_MS, self._layout)

    # -- Layout & draw ---------------------------------------------------------

    def _layout(self):
        w = self.winfo_width()  or C.WINDOW_WIDTH
        h = self.winfo_height() or (C.WINDOW_HEIGHT - C.STATUS_BAR_HEIGHT)
        pad = C.BOARD_CANVAS_PAD
        self._bx = pad
        self._by = pad
        self._bw = w - 2 * pad
        self._bh = h - 2 * pad
        self.draw_board()

    def draw_board(self, highlight_pits: dict[int, str] | None = None):
        """
        Full redraw.  *highlight_pits* maps pit_index -> override_color.
        """
        self.delete("all")
        if highlight_pits is None:
            highlight_pits = {}
        self._draw_background()
        self._draw_side_tints()
        self._draw_pits(highlight_pits)
        self._draw_scores()
        self._draw_turn_indicator()

    def _draw_background(self):
        bx, by, bw, bh = self._bx, self._by, self._bw, self._bh
        r = C.BOARD_RADIUS
        # Rounded rectangle (approximated with 8 points)
        pts = _rounded_rect_points(bx, by, bx + bw, by + bh, r)
        self.create_polygon(pts, fill=C.BOARD_COLOR,
                            outline=C.BOARD_BORDER, width=C.BOARD_OUTLINE_WIDTH, smooth=True)

    def _draw_side_tints(self):
        bx, by, bw, bh = self._bx, self._by, self._bw, self._bh
        mid_y = by + bh / 2
        # AI tint (top half)
        self.create_rectangle(bx + C.BOARD_RADIUS, by + C.BOARD_RADIUS,
                               bx + bw - C.BOARD_RADIUS, mid_y,
                               fill=C.AI_SIDE_TINT, outline="")
        # Human tint (bottom half)
        self.create_rectangle(bx + C.BOARD_RADIUS, mid_y,
                               bx + bw - C.BOARD_RADIUS,
                               by + bh - C.BOARD_RADIUS,
                               fill=C.HUMAN_SIDE_TINT, outline="")
        # Divider line
        self.create_line(bx + C.BOARD_RADIUS, mid_y,
                         bx + bw - C.BOARD_RADIUS, mid_y,
                         fill=C.BOARD_BORDER, width=C.BOARD_DIVIDER_WIDTH)

    def _draw_pits(self, highlight_pits: dict[int, str]):
        for pit in range(TOTAL_PITS):
            col = _pit_display_col(pit)
            row = _pit_row(pit)
            cx, cy = _pit_center(col, row,
                                  self._bx, self._by, self._bw, self._bh, CG.PITS_PER_PLAYER)
            count = self.board.pits[pit]

            # Determine fill colour
            if pit in highlight_pits:
                fill = highlight_pits[pit]
            elif count == 0:
                fill = C.PIT_COLOR_EMPTY
            elif pit == self._hover_pit and not self._locked:
                fill = C.PIT_COLOR_HOVER
            elif pit < CG.PITS_PER_PLAYER:
                fill = C.PIT_COLOR_IDLE
            else:
                fill = C.PIT_COLOR_AI_IDLE

            self._draw_pit_shape(cx, cy, fill)

            # Seeds
            if count > 0:
                self._draw_seeds(cx, cy, count, pit)

            if C.SHOW_PIT_LABELS:
                self.create_text(cx, cy - C.PIT_H // 2 - C.PIT_LABEL_GAP,
                                  text=str(pit),
                                  font=C.PIT_LABEL_FONT,
                                  fill=C.PIT_LABEL_COLOR)

    def _draw_pit_shape(self, cx: float, cy: float, fill: str):
        hw = C.PIT_W / 2
        hh = C.PIT_H / 2
        x0, y0, x1, y1 = cx - hw, cy - hh, cx + hw, cy + hh
        if C.PIT_SHAPE == "oval":
            self.create_oval(x0, y0, x1, y1, fill=fill,
                             outline=C.PIT_OUTLINE, width=C.PIT_OUTLINE_WIDTH)
        else:
            r = C.PIT_RECT_RADIUS
            pts = _rounded_rect_points(x0, y0, x1, y1, r)
            self.create_polygon(pts, fill=fill,
                                outline=C.PIT_OUTLINE,
                                width=C.PIT_OUTLINE_WIDTH, smooth=True)

    def _draw_seeds(self, cx: float, cy: float, count: int, pit: int):
        positions = _seed_positions(cx, cy, count, C.SEED_RADIUS)
        for idx, (sx, sy) in enumerate(positions):
            color = C.SEED_PALETTE[idx % len(C.SEED_PALETTE)]
            r = C.SEED_RADIUS
            self.create_oval(sx - r, sy - r, sx + r, sy + r,
                             fill=color,
                             outline=C.SEED_OUTLINE,
                             width=C.SEED_OUTLINE_WIDTH)

    def _draw_scores(self):
        bx, by, bw, bh = self._bx, self._by, self._bw, self._bh
        self.create_text(bx + C.SCORE_INSET, by + bh - C.SCORE_INSET,
                         text=f"{T.SCORE_HUMAN_LABEL}: {self.board.captured[HUMAN]}",
                         font=C.SCORE_FONT, fill=C.SCORE_COLOR,
                         anchor="sw")
        self.create_text(bx + C.SCORE_INSET, by + C.SCORE_INSET,
                         text=f"{T.SCORE_AI_LABEL}: {self.board.captured[AI]}",
                         font=C.SCORE_FONT, fill=C.SCORE_COLOR,
                         anchor="nw")

    def _draw_turn_indicator(self):
        bx, by, bw, bh = self._bx, self._by, self._bw, self._bh
        if self.board.game_over:
            w = self.board.winner
            if w == HUMAN:
                txt, col = T.TURN_LABEL_HUMAN_WIN, C.TURN_COLOR_HUMAN
            elif w == AI:
                txt, col = T.TURN_LABEL_AI_WIN,    C.TURN_COLOR_AI
            else:
                txt, col = T.TURN_LABEL_DRAW,      C.TURN_COLOR_NONE
        elif self.board.current_player == HUMAN:
            txt, col = T.TURN_LABEL_HUMAN, C.TURN_COLOR_HUMAN
        else:
            txt, col = T.TURN_LABEL_AI,    C.TURN_COLOR_AI

        self.create_text(bx + bw / 2, by + bh / 2,
                         text=txt, font=C.TURN_FONT, fill=col,
                         anchor="center")

    # -- Mouse events ----------------------------------------------------------

    def _pit_at(self, x: float, y: float) -> int | None:
        """Return pit index under mouse, or None."""
        for pit in range(TOTAL_PITS):
            col = _pit_display_col(pit)
            row = _pit_row(pit)
            cx, cy = _pit_center(col, row,
                                  self._bx, self._by, self._bw, self._bh, CG.PITS_PER_PLAYER)
            hw, hh = C.PIT_W / 2, C.PIT_H / 2
            if abs(x - cx) <= hw and abs(y - cy) <= hh:
                return pit
        return None

    def _on_mouse_move(self, event):
        pit = self._pit_at(event.x, event.y)
        if pit != self._hover_pit:
            self._hover_pit = pit
            if not self._locked:
                self.draw_board()

    def _on_double_click(self, event):
        if self._locked or self.board.game_over:
            return
        if self.board.current_player != HUMAN:
            return
        pit = self._pit_at(event.x, event.y)
        if pit is None or pit >= CG.PITS_PER_PLAYER:
            return   # must click own pit
        legal = self.board.get_legal_moves(HUMAN)
        if pit not in legal:
            return
        self.on_human_move(pit)

    # -- Animation API (called by ui_main) -------------------------------------

    def lock(self):
        self._locked = True

    def unlock(self):
        self._locked = False
        self.draw_board()

    def animate_move(self, source_pit: int, distribution: list[int],
                     captures: list[int], new_board: Board,
                     on_done):
        """
        Run the full visual sequence for one move:
          1. Blink source pit
          2. Place seeds one by one (each receiving pit briefly flashes)
          3. Flash captured pits red
          4. Update board state, call on_done()
        """
        logger.debug("Animation start | source_pit=%d | distribution=%s | captures=%s",
                     source_pit, distribution, captures)
        self.lock()
        self._cancel_anim()
        self._run_blink(source_pit, distribution, captures, new_board, on_done,
                        blink_n=CG.ANIM_BLINK_COUNT)

    def _cancel_anim(self):
        if self._anim_after_id is not None:
            try:
                self.after_cancel(self._anim_after_id)
            except Exception:
                pass
            self._anim_after_id = None

    # -- Blink phase -----------------------------------------------------------

    def _run_blink(self, source_pit, distribution, captures, new_board, on_done,
                   blink_n: int, bright=True):
        if blink_n <= 0:
            self._distribute_step(source_pit, distribution, captures,
                                   new_board, on_done, step=0, highlights={})
            return
        is_ai = source_pit >= CG.PITS_PER_PLAYER
        color = (C.AI_BLINK_COLOR_A if is_ai else C.BLINK_COLOR_A) if bright \
                else (C.AI_BLINK_COLOR_B if is_ai else C.BLINK_COLOR_B)
        self.draw_board(highlight_pits={source_pit: color})
        self._anim_after_id = self.after(
            CG.ANIM_BLINK_INTERVAL_MS,
            lambda: self._run_blink(source_pit, distribution, captures,
                                    new_board, on_done,
                                    blink_n - 1, not bright)
        )

    # -- Distribute phase ------------------------------------------------------

    def _distribute_step(self, source_pit, distribution, captures,
                          new_board, on_done, step: int, highlights: dict):
        """Place seeds one at a time, flashing each receiving pit briefly."""
        if step >= len(distribution):
            # Distribution done - now show final board then capture flash
            self.board = new_board
            self.draw_board()
            if captures:
                self._anim_after_id = self.after(
                    CG.ANIM_PRE_CAPTURE_PAUSE_MS,
                    lambda: self._flash_captures(captures, new_board, on_done,
                                                  flash_n=CG.ANIM_CAPTURE_FLASH_COUNT, bright=True)
                )
            else:
                self._anim_after_id = self.after(CG.ANIM_FINISH_DELAY_MS, lambda: self._finish(on_done))
            return

        target_pit = distribution[step]
        # Temporarily draw with flash highlight on the receiving pit
        flash_h = dict(highlights)
        flash_h[target_pit] = C.RECEIVE_FLASH_COLOR

        # Also grey out the source pit (empty now)
        flash_h[source_pit] = C.PIT_COLOR_EMPTY

        # Simulate intermediate board state for this step
        temp_board = self._intermediate_board(source_pit, distribution, step)
        old_board  = self.board
        self.board = temp_board
        self.draw_board(highlight_pits=flash_h)
        self.board = old_board

        self._anim_after_id = self.after(
            CG.ANIM_STEP_DELAY_MS,
            lambda: self._distribute_step(source_pit, distribution, captures,
                                           new_board, on_done, step + 1,
                                           highlights)
        )

    def _intermediate_board(self, source_pit: int,
                             distribution: list[int], steps_done: int):
        """Clone board reflecting *steps_done* seeds placed."""
        import copy
        b = self.board.clone()
        b.pits[source_pit] = 0
        for i in range(steps_done + 1):
            b.pits[distribution[i]] += 1
        return b

    # -- Capture flash phase ---------------------------------------------------

    def _flash_captures(self, captures, new_board, on_done,
                         flash_n: int, bright: bool):
        if flash_n <= 0:
            self.board = new_board
            self._anim_after_id = self.after(CG.ANIM_FINISH_DELAY_MS, lambda: self._finish(on_done))
            return
        hl = {p: C.PIT_COLOR_CAPTURE if bright else C.PIT_COLOR_IDLE
              for p in captures}
        self.draw_board(highlight_pits=hl)
        self._anim_after_id = self.after(
            CG.ANIM_BLINK_INTERVAL_MS,
            lambda: self._flash_captures(captures, new_board, on_done,
                                          flash_n - 1, not bright)
        )

    # -- Done ------------------------------------------------------------------

    def _finish(self, on_done):
        logger.debug("Animation complete")
        self.unlock()
        on_done()

    # -- Hint animation --------------------------------------------------------

    def hint_pit(self, pit: int, tooltip_text: str, on_done):
        """Blink *pit* as a move hint with a tooltip; call on_done when finished."""
        logger.debug("Hint animation start | pit=%d | tooltip='%s' | blink_count=%d",
                     pit, tooltip_text, C.HINT_BLINK_COUNT)
        self.lock()
        self._cancel_anim()
        tip = self._make_hint_tooltip(pit, tooltip_text)
        self._run_hint_blink(pit, C.HINT_BLINK_COUNT, True, on_done, tip)

    def _make_hint_tooltip(self, pit: int, text: str):
        col = _pit_display_col(pit)
        row = _pit_row(pit)
        cx, cy = _pit_center(col, row, self._bx, self._by, self._bw, self._bh, CG.PITS_PER_PLAYER)
        sx = self.winfo_rootx() + int(cx)
        sy = self.winfo_rooty() + int(cy) - C.PIT_H // 2 - C.HINT_TOOLTIP_GAP
        tip = tk.Toplevel(self)
        tip.overrideredirect(True)
        tip.attributes("-topmost", True)
        tk.Label(tip, text=text, font=C.LABEL_FONT,
                 bg=C.HINT_TOOLTIP_BG, fg=C.HINT_TOOLTIP_FG,
                 relief="solid", bd=C.HINT_TOOLTIP_BD,
                 padx=C.HINT_TOOLTIP_PADX, pady=C.HINT_TOOLTIP_PADY).pack()
        tip.update_idletasks()
        tip.geometry(f"+{sx - tip.winfo_width() // 2}+{sy}")
        return tip

    def _run_hint_blink(self, pit: int, blink_n: int, bright: bool,
                        on_done, tooltip):
        if blink_n <= 0:
            try:
                tooltip.destroy()
            except Exception:
                pass
            self._anim_after_id = self.after(CG.ANIM_FINISH_DELAY_MS, lambda: self._finish(on_done))
            return
        color = C.HINT_BLINK_COLOR_A if bright else C.HINT_BLINK_COLOR_B
        self.draw_board(highlight_pits={pit: color})
        self._anim_after_id = self.after(
            C.HINT_BLINK_INTERVAL_MS,
            lambda: self._run_hint_blink(pit, blink_n - 1, not bright, on_done, tooltip)
        )


# -- Utility: rounded-rect polygon points -------------------------------------

def _rounded_rect_points(x0: float, y0: float, x1: float, y1: float,
                          r: float) -> list[float]:
    """Return flat list of (x, y, ...) for a rounded rectangle."""
    pts = []
    pts += [x0 + r, y0,   x1 - r, y0]
    pts += [x1, y0,       x1, y0 + r]
    pts += [x1, y1 - r,   x1, y1]
    pts += [x1 - r, y1,   x0 + r, y1]
    pts += [x0, y1,       x0, y1 - r]
    pts += [x0, y0 + r,   x0, y0]
    return pts
