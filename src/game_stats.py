"""
In-game statistics collector for Oware/Wari.
Instantiated once per game in ui_main.py; consumed by ui_stats.py at game end.
"""

import math
import time
import logging
from game_logic import HUMAN, AI, opponent
from config_game import MISSED_OPPORTUNITY_THRESHOLD

logger = logging.getLogger(__name__)


class GameStats:
    """Accumulate per-game statistics during play."""

    def __init__(self):
        self._start_time        = time.monotonic()
        self.half_moves         = 0
        self.winner             = None
        self.end_reason         = None

        self._human_captures    = []    # seeds captured per human half-move
        self._ai_captures       = []    # seeds captured per AI half-move
        self._ai_scores         = []    # minimax score per AI move (may contain inf)
        self._ai_think_times    = []    # wall-clock seconds per AI move
        self._score_trajectory  = []    # (human_cap, ai_cap) snapshot after each half-move

        self.hint_requests      = 0
        self._pending_hint_pit  = None
        self._pending_hint_eval = None
        self._hints_followed    = 0
        self._missed_opps       = 0
        self._missed_gaps       = []

        self._grand_slam_triggers = 0
        self._forced_moves        = 0

        self._game_duration = None

    # -- Recording ---------------------------------------------------------------

    def record_hint(self, pit: int, eval_after: float) -> None:
        """Call when a hint has been computed for the current human turn."""
        self.hint_requests     += 1
        self._pending_hint_pit  = pit
        self._pending_hint_eval = eval_after
        logger.debug("Stats: hint recorded | pit=%d | eval=%.1f", pit, eval_after)

    def record_human_move(self, pit: int, captures: int,
                          played_eval: float, score_snap: tuple) -> None:
        """
        Call after the human plays.
        played_eval: evaluate(new_board) for the actual move.
        score_snap:  (human_captured, ai_captured) from the resulting board.
        """
        self.half_moves += 1
        self._human_captures.append(captures)
        self._score_trajectory.append(score_snap)

        if self._pending_hint_pit is not None:
            if pit == self._pending_hint_pit:
                self._hints_followed += 1
                logger.debug("Stats: human followed hint (pit %d)", pit)
            else:
                # Missed opportunity: only count when both evals are finite
                if (math.isfinite(played_eval)
                        and math.isfinite(self._pending_hint_eval)):
                    gap = played_eval - self._pending_hint_eval
                    logger.debug(
                        "Stats: human ignored hint | hint_pit=%d played_pit=%d gap=%.1f",
                        self._pending_hint_pit, pit, gap,
                    )
                    if gap > MISSED_OPPORTUNITY_THRESHOLD:
                        self._missed_opps += 1
                        self._missed_gaps.append(gap)
                        logger.debug(
                            "Stats: missed opportunity #%d (gap=%.1f)",
                            self._missed_opps, gap,
                        )
            self._pending_hint_pit  = None
            self._pending_hint_eval = None

    def record_ai_move(self, captures: int, score,
                       think_time: float, was_forced: bool) -> None:
        """Call after the AI plays."""
        self.half_moves += 1
        self._ai_captures.append(captures)
        if score is not None:
            self._ai_scores.append(score)
        self._ai_think_times.append(think_time)
        if was_forced:
            self._forced_moves += 1
        logger.debug(
            "Stats: AI move | captures=%d score=%s think=%.2fs forced=%s",
            captures,
            f"{score:.1f}" if score is not None else "n/a",
            think_time, was_forced,
        )

    def record_grand_slam_trigger(self) -> None:
        self._grand_slam_triggers += 1
        logger.debug("Stats: grand-slam trigger #%d", self._grand_slam_triggers)

    def finalise(self, winner, end_reason: str, board) -> None:
        self._game_duration = time.monotonic() - self._start_time
        self.winner     = winner
        self.end_reason = end_reason
        logger.debug(
            "Stats: game finalised | winner=%s | reason=%s | duration=%.1fs",
            winner, end_reason, self._game_duration,
        )
        self._log_summary(board)

    # -- Computed properties -----------------------------------------------------

    @property
    def lead_changes(self) -> int:
        """Number of times the captured-seed lead changed hands."""
        changes = 0
        prev = 0   # 0=tied, 1=human ahead, -1=ai ahead
        for h, a in self._score_trajectory:
            cur = 1 if h > a else (-1 if a > h else 0)
            if cur != 0 and cur != prev:
                if prev != 0:
                    changes += 1
                prev = cur
        return changes

    @property
    def max_human_lead(self) -> int:
        return max((h - a for h, a in self._score_trajectory), default=0)

    @property
    def max_ai_lead(self) -> int:
        return max((a - h for h, a in self._score_trajectory), default=0)

    @property
    def avg_captures_human(self) -> float:
        return (sum(self._human_captures) / len(self._human_captures)
                if self._human_captures else 0.0)

    @property
    def avg_captures_ai(self) -> float:
        return (sum(self._ai_captures) / len(self._ai_captures)
                if self._ai_captures else 0.0)

    @property
    def hints_followed(self) -> int:
        return self._hints_followed

    @property
    def missed_opportunities(self) -> int:
        return self._missed_opps

    @property
    def avg_missed_gap(self) -> float:
        return (sum(self._missed_gaps) / len(self._missed_gaps)
                if self._missed_gaps else 0.0)

    @property
    def avg_ai_score(self) -> float:
        finite = [s for s in self._ai_scores if math.isfinite(s)]
        return sum(finite) / len(finite) if finite else 0.0

    @property
    def avg_ai_think(self) -> float:
        return (sum(self._ai_think_times) / len(self._ai_think_times)
                if self._ai_think_times else 0.0)

    @property
    def slowest_ai_move(self) -> "tuple[float, int]":
        if not self._ai_think_times:
            return 0.0, 0
        t = max(self._ai_think_times)
        return t, self._ai_think_times.index(t) + 1

    @property
    def grand_slam_triggers(self) -> int:
        return self._grand_slam_triggers

    @property
    def forced_moves(self) -> int:
        return self._forced_moves

    @property
    def game_duration(self) -> float:
        return self._game_duration or 0.0

    @property
    def differential_trajectory(self) -> "list[int]":
        """Seed differential (human - machine captured) after each half-move."""
        return [h - a for h, a in self._score_trajectory]

    # -- INFO-level summary log --------------------------------------------------

    def _log_summary(self, board) -> None:
        w = ("Human" if self.winner == HUMAN
             else "Machine" if self.winner == AI
             else "Draw")
        hints_pct = (round(100 * self._hints_followed / self.hint_requests)
                     if self.hint_requests else 0)
        slowest_t, slowest_n = self.slowest_ai_move
        dur = self.game_duration
        m, s = divmod(int(dur), 60)
        dur_str = f"{m}m{s:02d}s" if m else f"{s}s"

        logger.info("=== GAME SUMMARY ===")
        logger.info(
            "[OUTCOME] winner=%s | score=You:%d Machine:%d | ended_by=%s"
            " | half_moves=%d | lead_changes=%d"
            " | max_human_lead=+%d | max_ai_lead=+%d",
            w,
            board.captured[HUMAN], board.captured[AI],
            self.end_reason,
            self.half_moves, self.lead_changes,
            self.max_human_lead, self.max_ai_lead,
        )
        logger.info(
            "[MOVE QUALITY] hint_requests=%d | hints_followed=%d/%d (%d%%)"
            " | missed_opportunities=%d | avg_score_gap=%.1fpts"
            " | avg_captures_human=%.1f | avg_captures_ai=%.1f",
            self.hint_requests,
            self._hints_followed, self.hint_requests, hints_pct,
            self._missed_opps, self.avg_missed_gap,
            self.avg_captures_human, self.avg_captures_ai,
        )
        logger.info(
            "[AI BEHAVIOUR] avg_minimax_score=%+.1f"
            " | grand_slam_triggers=%d | forced_moves=%d",
            self.avg_ai_score,
            self._grand_slam_triggers, self._forced_moves,
        )
        logger.info(
            "[TEMPORAL] avg_ai_think=%.2fs | slowest_move=%.2fs (move #%d)"
            " | game_duration=%s",
            self.avg_ai_think, slowest_t, slowest_n, dur_str,
        )
        diffs = [h - a for h, a in self._score_trajectory]
        logger.info(
            "[TRAJECTORY] seed_differential_per_half_move (human minus machine): %s",
            diffs,
        )
