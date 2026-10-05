"""
Minimax with alpha-beta pruning AI engine.
Search depth and all evaluation weights are read from config_game.py.
"""

import math
import logging
from game_logic import Board, HUMAN, AI
from .minimax_alphabeta_config import (
    AI_DEPTH,
    EVAL_SEED_DIFF_WEIGHT,
    EVAL_THREATENED_WEIGHT,
    EVAL_OPPONENT_THREAT_WEIGHT,
    EVAL_BOARD_CONTROL_WEIGHT,
    EVAL_MOBILITY_WEIGHT,
)
from ai_engines.base import AIEngine

logger = logging.getLogger(__name__)


# -- Internal helpers ----------------------------------------------------------

def _evaluate(board: Board) -> float:
    """Static evaluation from AI perspective (positive = good for AI)."""
    if board.game_over:
        if board.winner == AI:    return math.inf
        if board.winner == HUMAN: return -math.inf
        return 0.0

    score = 0.0

    # 1. Captured seed difference - most important signal
    score += (board.captured[AI] - board.captured[HUMAN]) * EVAL_SEED_DIFF_WEIGHT

    # 2. Seeds AI can capture in next move (opportunity)
    score += _seeds_threatened(board, AI)    * EVAL_THREATENED_WEIGHT

    # 3. Seeds human can capture next move (threat penalty)
    score -= _seeds_threatened(board, HUMAN) * EVAL_OPPONENT_THREAT_WEIGHT

    # 4. Board control: seeds on own side give more future options
    score += board.seeds_on_side(AI)    * EVAL_BOARD_CONTROL_WEIGHT
    score -= board.seeds_on_side(HUMAN) * EVAL_BOARD_CONTROL_WEIGHT

    # 5. Mobility: more legal moves = more flexibility
    score += (len(board.get_legal_moves(AI)) -
              len(board.get_legal_moves(HUMAN))) * EVAL_MOBILITY_WEIGHT

    return score


def _seeds_threatened(board: Board, attacker: int) -> int:
    """Maximum seeds *attacker* could capture in a single move right now."""
    best = 0
    for pit in board.get_legal_moves(attacker):
        b = board.clone()
        b.current_player = attacker
        _, result = b.apply_move(pit)
        best = max(best, result.captured_count)
    return best


def _order_moves(board: Board, moves: list, player: int) -> list:
    """Heuristic move ordering: capturing moves first for better pruning."""
    def move_score(pit: int) -> int:
        b = board.clone()
        b.current_player = player
        _, r = b.apply_move(pit)
        return r.captured_count
    return sorted(moves, key=move_score, reverse=True)


def _minimax(board: Board, depth: int, alpha: float, beta: float,
             maximising: bool) -> float:
    if board.game_over or depth == 0:
        return _evaluate(board)

    player = AI if maximising else HUMAN
    moves  = board.get_legal_moves(player)
    if not moves:
        return _evaluate(board)

    moves = _order_moves(board, moves, player)

    if maximising:
        value = -math.inf
        for pit in moves:
            child, _ = board.apply_move(pit)
            value = max(value, _minimax(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = math.inf
        for pit in moves:
            child, _ = board.apply_move(pit)
            value = min(value, _minimax(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


def _hint_rationale(board: Board, pit: int) -> str:
    """Build a short tooltip explaining why *pit* is the recommended move."""
    clone = board.clone()
    _, result = clone.apply_move(pit)
    if result.captured_count > 0:
        s = "seed" if result.captured_count == 1 else "seeds"
        return f"Captures {result.captured_count} {s}"
    delta = _evaluate(board) - _evaluate(clone)  # positive = AI score dropped = good for human
    if delta > EVAL_SEED_DIFF_WEIGHT:
        return "Strongly improves your position"
    if delta > 0:
        return "Improves your position"
    return "Best available move - limits the machine's options"


# -- Engine class --------------------------------------------------------------

class MinimaxAlphaBetaEngine(AIEngine):

    def get_name(self) -> str:
        return f"Minimax/Alpha-Beta (local; depth: {AI_DEPTH})"

    def evaluate(self, board: Board) -> float:
        return _evaluate(board)

    def get_best_move(self, board: Board,
                      legal_moves: "list[int]") -> "tuple[int, float]":
        if not legal_moves:
            logger.error("get_best_move called with no legal moves")
            raise ValueError("No legal moves available for AI")

        logger.debug("AI: computing best move | depth=%d | candidates=%s",
                     AI_DEPTH, legal_moves)

        if len(legal_moves) == 1:
            logger.debug("AI: only one legal move | pit=%d", legal_moves[0])
            child, _ = board.apply_move(legal_moves[0])
            return legal_moves[0], _evaluate(child)

        ordered   = _order_moves(board, legal_moves, AI)
        best_val  = -math.inf
        best_move = ordered[0]
        scores    = {}

        logger.debug("AI: move order after capture-first heuristic: %s", ordered)
        for pit in ordered:
            child, result = board.apply_move(pit)
            val     = _minimax(child, AI_DEPTH - 1, -math.inf, math.inf, False)
            scores[pit] = val
            is_best = val > best_val
            logger.debug(
                "AI:   pit %d | immediate_capture=%d | minimax_score=%.1f%s",
                pit, result.captured_count, val,
                " <- new best" if is_best else "",
            )
            if is_best:
                best_val  = val
                best_move = pit

        logger.debug(
            "AI: selected pit %d | score=%.1f | all_scores=%s",
            best_move, best_val,
            {p: round(s, 1) for p, s in scores.items()},
        )
        return best_move, best_val

    def get_hint_move(self, board: Board,
                      legal_moves: "list[int]") -> "tuple[int, str]":
        if not legal_moves:
            logger.error("get_hint_move called with no legal moves")
            raise ValueError("No legal moves available for Human")

        logger.debug("Hint: computing best human move | depth=%d | candidates=%s",
                     AI_DEPTH, legal_moves)

        if len(legal_moves) == 1:
            rationale = _hint_rationale(board, legal_moves[0])
            logger.debug("Hint: only one legal move | pit=%d | rationale='%s'",
                         legal_moves[0], rationale)
            return legal_moves[0], rationale

        ordered   = _order_moves(board, legal_moves, HUMAN)
        best_val  = math.inf   # human minimises AI-perspective score
        best_move = ordered[0]
        scores    = {}

        logger.debug("Hint: move order after capture-first heuristic: %s", ordered)
        for pit in ordered:
            child, result = board.apply_move(pit)
            val     = _minimax(child, AI_DEPTH - 1, -math.inf, math.inf, True)
            scores[pit] = val
            is_best = val < best_val
            logger.debug(
                "Hint:   pit %d | immediate_capture=%d | minimax_score=%.1f%s",
                pit, result.captured_count, val,
                " <- new best (lower = better for human)" if is_best else "",
            )
            if is_best:
                best_val  = val
                best_move = pit

        rationale = _hint_rationale(board, best_move)
        logger.debug(
            "Hint: selected pit %d | score=%.1f | rationale='%s' | all_scores=%s",
            best_move, best_val, rationale,
            {p: round(s, 1) for p, s in scores.items()},
        )
        return best_move, rationale


def create() -> AIEngine:
    """Factory called by ai_engine.py when this plugin is loaded."""
    return MinimaxAlphaBetaEngine()
