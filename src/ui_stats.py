"""
Game summary modal window shown at game end.
Reads from a GameStats instance; all text and visual parameters come from config files.
"""

import tkinter as tk
from game_logic import HUMAN, AI
from game_stats import GameStats
import config_ui   as C
import config_text as T
import config_game as CG


class StatsWindow:
    """Create and display a modal game-summary dialog over *parent*."""

    def __init__(self, parent: tk.Tk, stats: GameStats, board):
        self._dlg = tk.Toplevel(parent)
        self._dlg.title(T.STATS_TITLE)
        self._dlg.resizable(False, False)
        self._dlg.configure(bg=C.BG_COLOR)
        self._dlg.grab_set()

        self._dlg.minsize(C.STATS_WINDOW_WIDTH, 1)

        self._build(stats, board)

        # Centre over parent after content is laid out
        self._dlg.update_idletasks()
        w = self._dlg.winfo_width()
        h = self._dlg.winfo_height()
        rx = parent.winfo_x() + parent.winfo_width()  // 2
        ry = parent.winfo_y() + parent.winfo_height() // 2
        self._dlg.geometry(f"+{rx - w // 2}+{ry - h // 2}")

    # -- Build -------------------------------------------------------------------

    def _build(self, stats: GameStats, board):
        outer = tk.Frame(self._dlg, bg=C.BG_COLOR,
                         padx=C.STATS_PADDING, pady=C.STATS_PADDING)
        outer.pack(fill="both", expand=True)

        # Title
        tk.Label(
            outer, text=T.STATS_TITLE,
            font=C.STATS_TITLE_FONT, fg=C.STATS_TITLE_COLOR,
            bg=C.BG_COLOR,
        ).pack(pady=(0, C.STATS_TITLE_PADY_BOT))

        # Horizontal rule under title
        tk.Frame(outer, bg=C.STATS_DIVIDER_COLOR, height=1).pack(
            fill="x", padx=0, pady=(0, 8))

        # Build formatted value strings
        winner_str = (T.STATS_WINNER_HUMAN if stats.winner == HUMAN
                      else T.STATS_WINNER_AI if stats.winner == AI
                      else T.STATS_WINNER_DRAW)

        end_map = {
            "win_threshold": T.STATS_ENDED_WIN.format(n=CG.WIN_THRESHOLD),
            "cycle_limit":   T.STATS_ENDED_CYCLE,
            "no_legal_moves": T.STATS_ENDED_NO_MOVES,
        }
        ended_str = end_map.get(stats.end_reason, stats.end_reason or "-")

        hints_pct = (round(100 * stats.hints_followed / stats.hint_requests)
                     if stats.hint_requests else 0)

        slowest_t, slowest_n = stats.slowest_ai_move

        dur = stats.game_duration
        m, s = divmod(int(dur), 60)
        dur_str = (T.STATS_DURATION_FMT_M.format(m=m, s=s) if m
                   else T.STATS_DURATION_FMT_S.format(s=s))

        sections = [
            (T.STATS_SECTION_OUTCOME, [
                (T.STATS_LBL_WINNER,
                 winner_str),
                (T.STATS_LBL_FINAL_SCORE,
                 T.STATS_SCORE_FMT.format(h=board.captured[HUMAN],
                                           a=board.captured[AI])),
                (T.STATS_LBL_ENDED_BY,
                 ended_str),
                (T.STATS_LBL_HALF_MOVES,
                 str(stats.half_moves)),
                (T.STATS_LBL_LEAD_CHANGES,
                 str(stats.lead_changes)),
                (T.STATS_LBL_MAX_HUMAN,
                 T.STATS_SEEDS_FMT.format(n=stats.max_human_lead)),
                (T.STATS_LBL_MAX_AI,
                 T.STATS_SEEDS_FMT.format(n=stats.max_ai_lead)),
            ]),
            (T.STATS_SECTION_MOVE_QA, [
                (T.STATS_LBL_HINT_REQ,
                 str(stats.hint_requests)),
                (T.STATS_LBL_HINTS_FOLLOW,
                 T.STATS_HINTS_FMT.format(f=stats.hints_followed,
                                           t=stats.hint_requests,
                                           p=hints_pct)),
                (T.STATS_LBL_MISSED,
                 T.STATS_MISSED_FMT.format(n=stats.missed_opportunities,
                                            gap=stats.avg_missed_gap)),
                (T.STATS_LBL_AVG_CAPTURES,
                 T.STATS_CAPTURES_FMT.format(h=stats.avg_captures_human,
                                              a=stats.avg_captures_ai)),
            ]),
            (T.STATS_SECTION_AI, [
                (T.STATS_LBL_AVG_MINIMAX,
                 T.STATS_MINIMAX_FMT.format(s=stats.avg_ai_score)),
                (T.STATS_LBL_GRAND_SLAM,
                 str(stats.grand_slam_triggers)),
                (T.STATS_LBL_FORCED,
                 str(stats.forced_moves)),
            ]),
            (T.STATS_SECTION_TEMPORAL, [
                (T.STATS_LBL_AVG_THINK,
                 T.STATS_THINK_FMT.format(t=stats.avg_ai_think)),
                (T.STATS_LBL_SLOWEST,
                 T.STATS_SLOWEST_FMT.format(t=slowest_t, n=slowest_n)),
                (T.STATS_LBL_DURATION,
                 dur_str),
            ]),
        ]

        for section_title, rows in sections:
            self._add_section(outer, section_title, rows)

        # Optional trajectory chart
        if C.STATS_SHOW_CHART:
            diffs = stats.differential_trajectory
            if diffs:
                self._add_chart(outer, diffs)

        # Close button
        tk.Frame(outer, bg=C.BG_COLOR, height=C.STATS_CLOSE_SPACER_H).pack()
        close_btn = tk.Button(
            outer, text=T.STATS_CLOSE_BTN, command=self._dlg.destroy,
            font=C.BTN_FONT, bg=C.BTN_BG, fg=C.BTN_FG,
            activebackground=C.BTN_ACTIVE_BG, activeforeground=C.BTN_FG,
            relief=C.BTN_RELIEF, cursor="hand2",
            padx=C.BTN_PADX, pady=C.BTN_PADY, bd=C.BTN_BD,
        )
        close_btn.bind("<Enter>", lambda e: close_btn.configure(bg=C.BTN_ACTIVE_BG))
        close_btn.bind("<Leave>", lambda e: close_btn.configure(bg=C.BTN_BG))
        close_btn.pack(pady=(0, 4))

    def _add_section(self, parent, title: str, rows: list):
        # Section header bar (full-width coloured label)
        tk.Label(
            parent, text=f"  {title}",
            font=C.STATS_SECTION_FONT,
            fg=C.STATS_SECTION_FG, bg=C.STATS_SECTION_BG,
            anchor="w",
        ).pack(fill="x", pady=(C.STATS_SECTION_PADY, 0))

        # Data rows
        for label, value in rows:
            row = tk.Frame(parent, bg=C.BG_COLOR)
            row.pack(fill="x", padx=C.STATS_ROW_PADX, pady=C.STATS_ROW_PADY)
            tk.Label(
                row, text=label,
                font=C.STATS_ROW_LABEL_FONT, fg=C.STATS_ROW_LABEL_COLOR,
                bg=C.BG_COLOR, anchor="w",
            ).pack(side="left")
            tk.Label(
                row, text=value,
                font=C.STATS_ROW_VALUE_FONT, fg=C.STATS_ROW_VALUE_COLOR,
                bg=C.BG_COLOR, anchor="e",
            ).pack(side="right")

        # Thin divider below section
        tk.Frame(parent, bg=C.STATS_DIVIDER_COLOR, height=1).pack(
            fill="x", padx=C.STATS_ROW_PADX, pady=(C.STATS_ROW_PADY, 0))

    def _add_chart(self, parent, diffs: "list[int]"):
        """Embed a matplotlib trajectory chart below the stats sections."""
        try:
            from matplotlib.figure import Figure
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError:
            return  # matplotlib unavailable - silently skip

        # Section header (matches the other four section headers)
        tk.Label(
            parent, text=f"  {T.STATS_SECTION_TRAJECTORY}",
            font=C.STATS_SECTION_FONT,
            fg=C.STATS_SECTION_FG, bg=C.STATS_SECTION_BG,
            anchor="w",
        ).pack(fill="x", pady=(C.STATS_SECTION_PADY, 0))

        # Figure dimensions derived from config
        fig_w = (C.STATS_WINDOW_WIDTH - 2 * C.STATS_PADDING) / C.STATS_CHART_DPI
        fig = Figure(figsize=(fig_w, C.STATS_CHART_HEIGHT_IN),
                     dpi=C.STATS_CHART_DPI, facecolor=C.STATS_CHART_BG)
        ax = fig.add_subplot(111, facecolor=C.STATS_CHART_BG)

        moves = list(range(1, len(diffs) + 1))

        # Filled areas above/below zero
        ax.fill_between(moves, diffs, 0,
                        where=[d >= 0 for d in diffs],
                        color=C.STATS_CHART_HUMAN_COLOR, alpha=C.STATS_CHART_FILL_ALPHA,
                        interpolate=True)
        ax.fill_between(moves, diffs, 0,
                        where=[d <= 0 for d in diffs],
                        color=C.STATS_CHART_AI_COLOR, alpha=C.STATS_CHART_FILL_ALPHA,
                        interpolate=True)

        # Main line and zero reference
        ax.plot(moves, diffs, color=C.STATS_CHART_LINE_COLOR,
                linewidth=C.STATS_CHART_LINE_WIDTH, zorder=3)
        ax.axhline(0, color=C.STATS_CHART_ZERO_COLOR,
                   linewidth=C.STATS_CHART_ZERO_WIDTH, linestyle="--", zorder=2)

        # Axis labels and tick styling
        ax.set_xlabel(T.STATS_CHART_XLABEL, fontsize=C.STATS_CHART_FONT_SIZE,
                      color=C.STATS_ROW_LABEL_COLOR, labelpad=C.STATS_CHART_LABEL_PAD)
        ax.set_ylabel(T.STATS_CHART_YLABEL, fontsize=C.STATS_CHART_FONT_SIZE,
                      color=C.STATS_ROW_LABEL_COLOR, labelpad=C.STATS_CHART_LABEL_PAD)
        ax.tick_params(labelsize=C.STATS_CHART_FONT_SIZE, colors=C.STATS_ROW_LABEL_COLOR,
                       length=C.STATS_CHART_TICK_LENGTH, pad=C.STATS_CHART_TICK_PAD)
        ax.set_xlim(1, max(len(diffs), 2))

        # Spine styling
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        for side in ("bottom", "left"):
            ax.spines[side].set_color(C.STATS_CHART_ZERO_COLOR)
            ax.spines[side].set_linewidth(C.STATS_CHART_SPINE_WIDTH)

        ax.grid(True, color=C.STATS_CHART_GRID_COLOR,
                linewidth=C.STATS_CHART_GRID_WIDTH, linestyle="-", zorder=1)

        fig.tight_layout(pad=C.STATS_CHART_LAYOUT_PAD)

        canvas_widget = FigureCanvasTkAgg(fig, master=parent)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().pack(
            fill="x", padx=C.STATS_ROW_PADX,
            pady=(0, C.STATS_ROW_PADY))
