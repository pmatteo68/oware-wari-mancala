"""
Main application window: start screen, game screen, end screen.
Coordinates BoardCanvas, game logic, and AI strategy.
"""

import logging
import time
import tkinter as tk
from tkinter import messagebox, filedialog
import threading

from game_logic import Board, HUMAN, AI, opponent, player_pits
import ai_engine
from ui_board import BoardCanvas
from game_persistence import save_game, load_game
from game_stats import GameStats
from ui_stats import StatsWindow
import config_ui   as C
import config_game as CG
import config_text as T

logger = logging.getLogger(__name__)


class MancalaApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(T.WINDOW_TITLE)
        self.root.configure(bg=C.BG_COLOR)
        self.root.resizable(C.WINDOW_RESIZABLE, C.WINDOW_RESIZABLE)
        self.root.geometry(f"{C.WINDOW_WIDTH}x{C.WINDOW_HEIGHT}")

        self._board:    Board | None       = None
        self._canvas:   BoardCanvas | None = None
        self._hint_btn: tk.Button | None   = None
        self._status_var = tk.StringVar(value="")
        self._stats:    GameStats | None   = None

        logger.debug("MancalaApp initialising | size=%dx%d | autoplay=%s",
                     C.WINDOW_WIDTH, C.WINDOW_HEIGHT, CG.AUTOPLAY)
        self._build_menu()
        if CG.AUTOPLAY:
            self._start_game(AI)
        else:
            self._show_start_screen()

    # -- Menu -----------------------------------------------------------------

    def _build_menu(self):
        menu_kw = dict(bg=C.STATUS_BG, fg=C.STATUS_COLOR,
                       activebackground=C.BTN_ACTIVE_BG,
                       activeforeground=C.BTN_FG)
        menubar = tk.Menu(self.root, relief="flat", bd=C.MENU_BD, **menu_kw)

        file_menu = tk.Menu(menubar, tearoff=False, **menu_kw)
        file_menu.add_command(label=T.MENU_NEW_GAME_LABEL, command=self._show_start_screen)
        file_menu.add_separator()
        file_menu.add_command(label=T.MENU_LOAD_LABEL, command=self._load_game)
        file_menu.add_command(label=T.MENU_SAVE_LABEL, command=self._save_game)
        file_menu.add_separator()
        file_menu.add_command(label=T.MENU_EXIT_LABEL, command=self.root.destroy)
        menubar.add_cascade(label=T.MENU_FILE_LABEL, menu=file_menu)

        utilities_menu = tk.Menu(menubar, tearoff=False, **menu_kw)
        utilities_menu.add_command(label=T.MENU_GET_HINT_LABEL,
                                   command=self._handle_get_hint)
        menubar.add_cascade(label=T.MENU_UTILITIES_LABEL, menu=utilities_menu)

        help_menu = tk.Menu(menubar, tearoff=False, **menu_kw)
        help_menu.add_command(label=T.MENU_ABOUT_LABEL, command=self._show_about)
        menubar.add_cascade(label=T.MENU_HELP_LABEL, menu=help_menu)

        self.root.config(menu=menubar)

    def _save_game(self):
        if self._board is None or self._board.game_over:
            logger.debug("Save requested but no active game to save")
            return
        path = filedialog.asksaveasfilename(
            title=T.SAVE_DIALOG_TITLE,
            defaultextension=".mancala",
            filetypes=[(T.SAVE_FILETYPE_DESC, T.SAVE_FILETYPE_EXT)],
        )
        if not path:
            logger.debug("Save cancelled by user")
            return
        try:
            save_game(self._board, path)
        except Exception as e:
            logger.error("Save error for '%s': %s", path, e)
            messagebox.showerror(T.SAVE_ERROR_TITLE,
                                 T.SAVE_ERROR_MSG.format(error=e))

    def _load_game(self):
        path = filedialog.askopenfilename(
            title=T.LOAD_DIALOG_TITLE,
            filetypes=[(T.LOAD_FILETYPE_DESC, T.LOAD_FILETYPE_EXT)],
        )
        if not path:
            logger.debug("Load cancelled by user")
            return
        try:
            board = load_game(path)
        except Exception as e:
            logger.error("Load error for '%s': %s", path, e)
            messagebox.showerror(T.LOAD_ERROR_TITLE,
                                 T.LOAD_ERROR_MSG.format(error=e))
            return
        self._start_game_with_board(board)

    def _show_about(self):
        dlg = tk.Toplevel(self.root)
        dlg.title(T.ABOUT_TITLE)
        dlg.resizable(False, False)
        dlg.configure(bg=C.BG_COLOR)
        dlg.grab_set()                   # modal

        # Centre over main window
        self.root.update_idletasks()
        rx = self.root.winfo_x() + self.root.winfo_width()  // 2
        ry = self.root.winfo_y() + self.root.winfo_height() // 2
        dlg.geometry(f"+{rx - C.ABOUT_OFFSET_X}+{ry - C.ABOUT_OFFSET_Y}")

        pad = dict(padx=C.ABOUT_PADX, pady=C.ABOUT_PADY)

        tk.Label(dlg, text=T.ABOUT_GAME_NAME,
                 font=C.START_TITLE_FONT, fg=C.START_TITLE_COLOR,
                 bg=C.BG_COLOR).pack(pady=(C.ABOUT_TITLE_PADY_TOP, 0))

        tk.Label(dlg, text=T.ABOUT_VERSION,
                 font=C.LABEL_FONT, fg=C.LABEL_COLOR,
                 bg=C.BG_COLOR).pack()

        tk.Frame(dlg, bg=C.BOARD_BORDER, height=1).pack(
            fill="x", padx=C.ABOUT_DIVIDER_PADX, pady=C.ABOUT_HEADER_DIVIDER_PADY)

        tk.Label(dlg, text=T.ABOUT_DESCRIPTION,
                 font=C.LABEL_FONT, fg=C.STATUS_COLOR,
                 bg=C.BG_COLOR, justify="left").pack(**pad)

        tk.Frame(dlg, bg=C.BOARD_BORDER, height=1).pack(
            fill="x", padx=C.ABOUT_DIVIDER_PADX, pady=C.ABOUT_BODY_DIVIDER_PADY)

        tk.Label(dlg, text=T.ABOUT_AI_NOTE,
                 font=C.LABEL_FONT, fg=C.LABEL_COLOR,
                 bg=C.BG_COLOR, wraplength=C.ABOUT_WRAP_WIDTH, justify="center").pack(**pad)

        tk.Label(dlg, text=T.ABOUT_TECH,
                 font=C.LABEL_FONT, fg=C.LABEL_COLOR,
                 bg=C.BG_COLOR).pack(**pad)

        self._make_btn(dlg, T.ABOUT_CLOSE_BTN, dlg.destroy).pack(
            pady=(C.ABOUT_CLOSE_PADY_TOP, C.ABOUT_CLOSE_PADY_BOT))

    # -- Start screen ----------------------------------------------------------

    def _show_start_screen(self):
        logger.debug("Showing start screen")
        self._clear_window()
        frame = tk.Frame(self.root, bg=C.BG_COLOR)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=T.START_TITLE, font=C.START_TITLE_FONT,
                 fg=C.START_TITLE_COLOR, bg=C.BG_COLOR).pack(pady=(0, C.START_TITLE_PADY))

        tk.Label(frame, text=T.START_SUBTITLE, font=C.START_SUBTITLE_FONT,
                 fg=C.START_SUBTITLE_COLOR, bg=C.BG_COLOR).pack(pady=(0, C.START_SUBTITLE_PADY))

        info_row = tk.Frame(frame, bg=C.BG_COLOR)
        info_row.pack(pady=(0, C.START_ENGINE_PADY))
        tk.Label(info_row,
                 text=f"{T.START_AI_ENGINE_PREFIX} {ai_engine.get_name()}",
                 font=C.LABEL_FONT, fg=C.LABEL_COLOR,
                 bg=C.BG_COLOR).pack(side="left", padx=(0, C.START_INFO_GAP))
        tk.Label(info_row,
                 text=f"{T.START_SKIN_PREFIX} {C.get_name()}",
                 font=C.LABEL_FONT, fg=C.LABEL_COLOR,
                 bg=C.BG_COLOR).pack(side="left")

        tk.Label(frame, text=T.START_WHO_FIRST, font=C.TURN_FONT,
                 fg=C.LABEL_COLOR, bg=C.BG_COLOR).pack(pady=(0, C.START_WHO_FIRST_PADY))

        btn_row = tk.Frame(frame, bg=C.BG_COLOR)
        btn_row.pack()

        self._make_btn(btn_row, T.START_BTN_HUMAN,
                       lambda: self._start_game(HUMAN)).pack(side="left", padx=C.START_BTN_PADX)
        self._make_btn(btn_row, T.START_BTN_AI,
                       lambda: self._start_game(AI)).pack(side="left", padx=C.START_BTN_PADX)

        tk.Label(frame, text=T.START_RULES_HINT, font=C.LABEL_FONT,
                 fg=C.LABEL_COLOR, bg=C.BG_COLOR,
                 justify="center").pack(pady=(C.START_RULES_PADY, 0))

        bottom_row = tk.Frame(frame, bg=C.BG_COLOR)
        bottom_row.pack(pady=(C.START_BOTTOM_ROW_PADY, 0))
        self._make_btn(bottom_row, T.START_BTN_LOAD,
                       self._load_game).pack(side="left", padx=C.START_BTN_PADX)
        self._make_btn(bottom_row, T.BTN_EXIT,
                       self.root.destroy).pack(side="left", padx=C.START_BTN_PADX)

    # -- Game screen -----------------------------------------------------------

    def _start_game(self, first_player: int):
        logger.debug("New game | first_player=%s", "Human" if first_player == HUMAN else "AI")
        board = Board()
        board.current_player = first_player
        self._start_game_with_board(board)

    def _start_game_with_board(self, board: Board):
        logger.debug("Starting game | player=%s | pits=%s | captured=%s | streak=%d",
                    "Human" if board.current_player == HUMAN else "AI",
                    board.pits, board.captured, board.no_capture_streak)
        self._clear_window()
        self._board = board
        self._stats = GameStats()

        # Status bar
        status_bar = tk.Frame(self.root, bg=C.STATUS_BG,
                               height=C.STATUS_BAR_HEIGHT)
        status_bar.pack(side="bottom", fill="x")
        status_bar.pack_propagate(False)

        self._make_btn(status_bar, T.BTN_EXIT,
                       self.root.destroy).pack(side="right", padx=C.STATUS_BTN_PADX_END, pady=C.STATUS_BTN_PADY)
        self._make_btn(status_bar, T.BTN_NEW_GAME,
                       self._show_start_screen).pack(side="right", padx=C.STATUS_BTN_PADX, pady=C.STATUS_BTN_PADY)
        self._make_btn(status_bar, T.BTN_SAVE_GAME,
                       self._save_game).pack(side="right", padx=C.STATUS_BTN_PADX, pady=C.STATUS_BTN_PADY)
        self._make_btn(status_bar, T.BTN_LOAD_GAME,
                       self._load_game).pack(side="right", padx=C.STATUS_BTN_PADX, pady=C.STATUS_BTN_PADY)
        self._hint_btn = self._make_btn(status_bar, T.BTN_GET_HINT,
                                        self._handle_get_hint)
        self._hint_btn.pack(side="right", padx=C.STATUS_BTN_PADX, pady=C.STATUS_BTN_PADY)

        tk.Label(status_bar, textvariable=self._status_var,
                 font=C.STATUS_FONT, fg=C.STATUS_COLOR,
                 bg=C.STATUS_BG).pack(side="left", padx=C.STATUS_LABEL_PADX, pady=C.STATUS_BTN_PADY)

        # Board canvas
        self._canvas = BoardCanvas(
            self.root, self._board,
            on_human_move=self._handle_human_move,
        )
        self._canvas.pack(side="top", fill="both", expand=True)

        self._update_status()

        if self._board.current_player == AI:
            self._schedule_ai_move()
        elif CG.AUTOPLAY:
            self.root.after(CG.AUTOPLAY_HINT_DELAY_MS, self._handle_get_hint)

    # -- Human move ------------------------------------------------------------

    def _handle_human_move(self, pit: int):
        logger.debug("Human plays pit %d | seeds_in_pit=%d | captured_before=%s",
                    pit, self._board.pits[pit], self._board.captured)

        # Stats: detect grand-slam rule trigger before applying move
        if self._stats is not None:
            all_own = [p for p in player_pits(HUMAN) if self._board.pits[p] > 0]
            legal_now = self._board.get_legal_moves(HUMAN)
            if (self._board.seeds_on_side(AI) > 0
                    and len(legal_now) < len(all_own)):
                self._stats.record_grand_slam_trigger()

        new_board, result = self._board.apply_move(pit)
        logger.debug("Human move result | distribution=%s | captures=%s | captured_count=%d | game_over=%s",
                     result.distribution, result.captures,
                     result.captured_count, result.game_over)

        # Stats: record the human move
        if self._stats is not None:
            played_eval = ai_engine.evaluate(new_board)
            self._stats.record_human_move(
                pit=pit,
                captures=result.captured_count,
                played_eval=played_eval,
                score_snap=(new_board.captured[HUMAN], new_board.captured[AI]),
            )

        def after_animation():
            self._board = new_board
            self._canvas.board = new_board
            self._update_status()
            if new_board.game_over:
                self._show_game_over(new_board.winner, result.end_reason)
            else:
                self._schedule_ai_move()

        self._canvas.animate_move(
            source_pit=pit,
            distribution=result.distribution,
            captures=result.captures,
            new_board=new_board,
            on_done=after_animation,
        )

    # -- AI move ---------------------------------------------------------------

    def _schedule_ai_move(self):
        if self._board.current_player != AI:
            return
        logger.debug("Scheduling AI move computation")
        self._set_status(T.STATUS_AI_THINKING)
        self._canvas.lock()

        def think():
            all_moves = self._board.get_legal_moves(AI)
            was_forced = len(all_moves) == 1

            # Stats: detect grand-slam trigger
            grand_slam = False
            if self._stats is not None:
                all_ai_own = [p for p in player_pits(AI) if self._board.pits[p] > 0]
                if (self._board.seeds_on_side(HUMAN) > 0
                        and len(all_moves) < len(all_ai_own)):
                    grand_slam = True

            t0 = time.monotonic()
            try:
                pit, ai_score = ai_engine.get_best_move(self._board, all_moves)
            except Exception as e:
                logger.error("get_best_move raised unexpectedly: %s  -  falling back to first legal move", e)
                pit = all_moves[0] if all_moves else None
                ai_score = None
            think_time = time.monotonic() - t0

            logger.debug("AI thinking done | chosen_pit=%s | think_time=%.2fs | scheduling in %d ms",
                         pit, think_time, CG.AI_DELAY_MS)
            self.root.after(
                CG.AI_DELAY_MS,
                lambda: self._execute_ai_move(pit, ai_score, think_time,
                                               was_forced, grand_slam),
            )

        threading.Thread(target=think, daemon=True).start()

    def _execute_ai_move(self, pit: int, ai_score=None,
                          think_time: float = 0.0, was_forced: bool = False,
                          grand_slam: bool = False):
        if self._board.game_over:
            logger.debug("AI move execution skipped  -  game already over")
            return
        logger.debug("AI plays pit %d | seeds_in_pit=%d | captured_before=%s",
                    pit, self._board.pits[pit], self._board.captured)
        new_board, result = self._board.apply_move(pit)
        logger.debug("AI move result | distribution=%s | captures=%s | captured_count=%d | game_over=%s",
                     result.distribution, result.captures,
                     result.captured_count, result.game_over)

        # Stats: record AI move
        if self._stats is not None:
            if grand_slam:
                self._stats.record_grand_slam_trigger()
            self._stats.record_ai_move(
                captures=result.captured_count,
                score=ai_score,
                think_time=think_time,
                was_forced=was_forced,
            )

        def after_animation():
            self._board = new_board
            self._canvas.board = new_board
            self._update_status()
            if new_board.game_over:
                self._show_game_over(new_board.winner, result.end_reason)
            elif CG.AUTOPLAY:
                self.root.after(CG.AUTOPLAY_HINT_DELAY_MS, self._handle_get_hint)

        self._canvas.animate_move(
            source_pit=pit,
            distribution=result.distribution,
            captures=result.captures,
            new_board=new_board,
            on_done=after_animation,
        )

    # -- Hint ------------------------------------------------------------------

    def _handle_get_hint(self):
        if self._board is None or self._board.game_over:
            logger.debug("Hint requested but no active game")
            return
        if self._board.current_player != HUMAN:
            logger.debug("Hint requested but it is not the human's turn")
            return
        if self._hint_btn is None:
            return
        logger.debug("Hint requested | human_captured=%d | ai_captured=%d | board=%s",
                    self._board.captured[HUMAN], self._board.captured[AI], self._board.pits)
        self._hint_btn.config(state="disabled")
        self._canvas.lock()

        board_snapshot = self._board   # capture state before thread runs

        def think():
            try:
                pit, rationale = ai_engine.get_hint_move(
                    board_snapshot, board_snapshot.get_legal_moves(HUMAN))
            except Exception as e:
                logger.error("get_hint_move raised unexpectedly: %s", e)
                self.root.after(0, self._canvas.unlock)
                self.root.after(0, lambda: self._hint_btn and
                                self._hint_btn.config(state="normal"))
                return
            logger.debug("Hint ready | pit=%d | rationale='%s'", pit, rationale)
            self.root.after(0, lambda: self._show_hint(pit, rationale))

        threading.Thread(target=think, daemon=True).start()

    def _show_hint(self, pit: int, rationale: str):
        logger.debug("Displaying hint animation | pit=%d | tooltip='%s'", pit, rationale)

        # Stats: record the hint and the eval of the suggested position
        if self._stats is not None:
            hint_board, _ = self._board.apply_move(pit)
            hint_eval = ai_engine.evaluate(hint_board)
            self._stats.record_hint(pit, hint_eval)

        def on_hint_done():
            logger.debug("Hint animation complete")
            if self._hint_btn is not None:
                self._hint_btn.config(state="normal")
            if CG.AUTOPLAY:
                logger.debug("Autoplay: auto-playing hinted pit %d", pit)
                self._handle_human_move(pit)
        self._canvas.hint_pit(pit, rationale, on_hint_done)

    # -- Game-over overlay -----------------------------------------------------

    def _show_game_over(self, winner: int | None, end_reason: str | None = None):
        winner_name = "Human" if winner == HUMAN else "AI" if winner == AI else "Draw"
        logger.debug("Game over | winner=%s | human=%d | ai=%d | reason=%s",
                    winner_name, self._board.captured[HUMAN], self._board.captured[AI],
                    end_reason)

        if winner == HUMAN:
            msg, col = T.GAMEOVER_HUMAN_WIN, C.TURN_COLOR_HUMAN
        elif winner == AI:
            msg, col = T.GAMEOVER_AI_WIN, C.TURN_COLOR_AI
        else:
            msg, col = T.GAMEOVER_DRAW, C.TURN_COLOR_NONE

        b = self._board
        detail = T.GAMEOVER_DETAIL.format(
            human=b.captured[HUMAN], ai=b.captured[AI]
        )
        self._set_status(f"{msg}   ({detail})")

        canvas = self._canvas
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        canvas.create_rectangle(0, 0, w, h, fill="#000000",
                                 stipple="gray50", outline="", tags="overlay")
        canvas.create_text(w // 2, h // 2 + C.GAMEOVER_MSG_OFFSET_Y,
                            text=msg, font=C.START_TITLE_FONT,
                            fill=col, tags="overlay")
        canvas.create_text(w // 2, h // 2 + C.GAMEOVER_DETAIL_OFFSET_Y,
                            text=detail, font=C.START_SUBTITLE_FONT,
                            fill=C.LABEL_COLOR, tags="overlay")

        tag = "play_again"
        canvas.create_text(w // 2, h // 2 + C.GAMEOVER_ACTION_OFFSET_Y,
                            text=T.GAMEOVER_PLAY_AGAIN, font=C.TURN_FONT,
                            fill=C.SCORE_COLOR, tags=(tag, "overlay"))
        canvas.tag_bind(tag, "<Button-1>", lambda _: self._show_start_screen())
        canvas.tag_bind(tag, "<Enter>",    lambda _: canvas.config(cursor="hand2"))
        canvas.tag_bind(tag, "<Leave>",    lambda _: canvas.config(cursor=""))

        # Finalise and show stats after a short pause (lets overlay render first)
        if self._stats is not None:
            board_snap = self._board
            stats_snap = self._stats
            self._stats = None   # prevent double-show if _show_game_over is re-entered
            stats_snap.finalise(winner, end_reason or "unknown", board_snap)
            self.root.after(
                C.STATS_DELAY_MS,
                lambda: StatsWindow(self.root, stats_snap, board_snap),
            )

    # -- Helpers ---------------------------------------------------------------

    def _update_status(self):
        b = self._board
        if b.game_over:
            return
        if b.current_player == HUMAN:
            self._set_status(T.STATUS_SCORES_TEMPLATE.format(
                human=b.captured[HUMAN], ai=b.captured[AI]
            ))
        else:
            self._set_status(T.STATUS_AI_SCORES_TEMPLATE.format(
                human=b.captured[HUMAN], ai=b.captured[AI]
            ))

    def _set_status(self, text: str):
        self._status_var.set(text)

    def _make_btn(self, parent, text: str, command) -> tk.Button:
        btn = tk.Button(
            parent, text=text, command=command,
            font=C.BTN_FONT, bg=C.BTN_BG, fg=C.BTN_FG,
            activebackground=C.BTN_ACTIVE_BG, activeforeground=C.BTN_FG,
            relief=C.BTN_RELIEF, cursor="hand2",
            padx=C.BTN_PADX, pady=C.BTN_PADY, bd=C.BTN_BD,
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=C.BTN_ACTIVE_BG))
        btn.bind("<Leave>", lambda e: btn.configure(bg=C.BTN_BG))
        return btn

    def _clear_window(self):
        for w in self.root.winfo_children():
            if not isinstance(w, tk.Menu):
                w.destroy()
        self._hint_btn = None
