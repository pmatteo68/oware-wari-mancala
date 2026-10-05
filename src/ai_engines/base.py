"""
Abstract base class for all AI engine plugins.
Every engine module inside this package must:
  - define a class that subclasses AIEngine and implements all four methods
  - export a module-level factory:  def create() -> AIEngine
"""

from abc import ABC, abstractmethod
from game_logic import Board


class AIEngine(ABC):
    """Contract that every AI engine plugin must satisfy."""

    @abstractmethod
    def get_name(self) -> str:
        """
        Short one-liner that identifies this engine.
        Shown on the start screen and written to the log at engine load time.
        Example: "Minimax / Alpha-Beta  depth 6"
        """

    @abstractmethod
    def get_best_move(self, board: Board,
                      legal_moves: "list[int]") -> "tuple[int, float]":
        """
        Choose the strongest move for the AI (maximising player).

        Parameters
        ----------
        board       : current game state; board.current_player is AI
        legal_moves : pre-computed list of legal pit indices for AI;
                      the engine must not call get_legal_moves at the top level

        Returns
        -------
        (pit_index, eval_score)
            pit_index  - the chosen pit (must be in legal_moves)
            eval_score - static evaluation of the resulting position from
                         the AI perspective (positive = AI advantaged)
        """

    @abstractmethod
    def get_hint_move(self, board: Board,
                      legal_moves: "list[int]") -> "tuple[int, str]":
        """
        Suggest the best move for the human (minimising AI advantage).

        Parameters
        ----------
        board       : current game state; board.current_player is HUMAN
        legal_moves : pre-computed list of legal pit indices for HUMAN

        Returns
        -------
        (pit_index, rationale)
            pit_index - the recommended pit (must be in legal_moves)
            rationale - short human-readable explanation shown as a tooltip
        """

    @abstractmethod
    def evaluate(self, board: Board) -> float:
        """
        Static board evaluation from the AI perspective.
        Positive values mean the AI is ahead; negative means the human is ahead.
        Called on non-terminal nodes during search and for missed-opportunity
        detection in GameStats.
        """
