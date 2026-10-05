"""
AI engine facade.
Loads the plugin named by config_game.AI_ENGINE and re-exports its contract
methods.  The rest of the codebase imports only this module and never depends
on a specific engine implementation.
"""

import importlib
import logging
import config_game as CG
from game_logic import Board

logger = logging.getLogger(__name__)

_engine = None


def _get():
    global _engine
    if _engine is None:
        module_path = f"ai_engines.{CG.AI_ENGINE}"
        logger.debug("Loading AI engine | module=%s", module_path)
        module  = importlib.import_module(module_path)
        _engine = module.create()
        logger.debug("AI engine ready | name='%s'", _engine.get_name())
    return _engine


def get_name() -> str:
    return _get().get_name()


def get_best_move(board: Board,
                  legal_moves: "list[int]") -> "tuple[int, float]":
    return _get().get_best_move(board, legal_moves)


def get_hint_move(board: Board,
                  legal_moves: "list[int]") -> "tuple[int, str]":
    return _get().get_hint_move(board, legal_moves)


def evaluate(board: Board) -> float:
    return _get().evaluate(board)
