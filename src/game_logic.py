"""
Core game logic.
No UI imports - pure game state and rules.

Board layout (indices):
    AI side (player 1):   [11][10][ 9][ 8][ 7][ 6]   (displayed right->left)
    Human side (player 0): [ 0][ 1][ 2][ 3][ 4][ 5]   (displayed left->right)

Counter-clockwise seed distribution: 0->1->2->3->4->5->6->7->8->9->10->11->0-> ...
In display terms that means: right along bottom row, then left along top row.
"""

import copy
import logging
from config_game import (
    NUM_PLAYERS, PITS_PER_PLAYER, SEEDS_PER_PIT, WIN_THRESHOLD,
    CYCLE_NO_CAPTURE_LIMIT, CAPTURE_THRESHOLDS,
)

logger = logging.getLogger(__name__)

TOTAL_PITS   = PITS_PER_PLAYER * NUM_PLAYERS          # 12
HUMAN        = 0
AI           = 1


# -- Helpers -------------------------------------------------------------------

def player_pits(player: int) -> range:
    """Return the range of pit indices owned by *player*."""
    if player == HUMAN:
        return range(0, PITS_PER_PLAYER)
    return range(PITS_PER_PLAYER, TOTAL_PITS)


def opponent(player: int) -> int:
    return (NUM_PLAYERS - 1) - player


def next_pit(pit: int) -> int:
    """Counter-clockwise successor (wraps 0-11)."""
    return (pit + 1) % TOTAL_PITS


def prev_pit(pit: int) -> int:
    """Clockwise predecessor - used only for capture back-tracking."""
    return (pit - 1) % TOTAL_PITS


# -- MoveResult ----------------------------------------------------------------

class MoveResult:
    """Returned by Board.apply_move - describes what happened."""
    __slots__ = ("distribution", "captures", "captured_count",
                 "fed_opponent", "game_over", "winner", "end_reason")

    def __init__(self):
        self.distribution: list[int] = []   # pits in order that received a seed
        self.captures:     list[int] = []   # pits whose seeds were captured
        self.captured_count: int = 0
        self.fed_opponent:  bool = False
        self.game_over:     bool = False
        self.winner: int | None  = None     # HUMAN / AI / None (draw)
        self.end_reason: str | None = None  # "win_threshold" / "cycle_limit" / "no_legal_moves"


# -- Board ---------------------------------------------------------------------

class Board:
    """
    Immutable-ish board state.  Call apply_move() to get a *new* Board.
    Use clone() for the AI search tree.
    """

    def __init__(self):
        self.pits:    list[int] = [SEEDS_PER_PIT] * TOTAL_PITS
        self.captured: list[int] = [0] * NUM_PLAYERS  # [human_captured, ai_captured]
        self.current_player: int = HUMAN
        self.no_capture_streak: int = 0             # half-moves without a capture
        self.game_over:  bool = False
        self.winner: int | None = None
        logger.debug("Board created | pits=%s | total_seeds=%d", self.pits, sum(self.pits))

    # -- Cloning --------------------------------------------------------------

    def clone(self) -> "Board":
        b = Board.__new__(Board)
        b.pits               = self.pits[:]
        b.captured           = self.captured[:]
        b.current_player     = self.current_player
        b.no_capture_streak  = self.no_capture_streak
        b.game_over          = self.game_over
        b.winner             = self.winner
        return b

    # -- Queries --------------------------------------------------------------

    def seeds_on_side(self, player: int) -> int:
        return sum(self.pits[i] for i in player_pits(player))

    def opponent_has_seeds(self) -> bool:
        return self.seeds_on_side(opponent(self.current_player)) > 0

    def total_seeds(self) -> int:
        return sum(self.pits)

    # -- Legal move generation -------------------------------------------------

    def get_legal_moves(self, player: int | None = None) -> list[int]:
        """
        Return pit indices that are legal for *player* (defaults to current_player).
        Enforces:
          1. Must be player's own non-empty pit.
          2. Feeding rule: if opponent has 0 seeds, must pick a pit whose
             distribution reaches the opponent. If no such pit exists, any
             non-empty pit is allowed.
          3. Grand-slam rule: must not capture ALL opponent's seeds when
             another move that leaves opponent with >=1 seed exists.
        """
        if player is None:
            player = self.current_player

        own_pits  = [i for i in player_pits(player) if self.pits[i] > 0]
        opp_seeds = self.seeds_on_side(opponent(player))

        if not own_pits:
            return []

        # Feeding rule
        if opp_seeds == 0:
            feeding = [p for p in own_pits if self._would_feed(p, player)]
            if feeding:
                return feeding
            return own_pits   # can't feed - any move is legal

        # Grand-slam rule: filter out moves that capture every opponent seed
        # but only when an alternative move exists
        safe = [p for p in own_pits if not self._is_grand_slam(p, player)]
        return safe if safe else own_pits

    def _would_feed(self, pit: int, player: int) -> bool:
        """True if playing *pit* causes at least one seed to land on opponent's side."""
        seeds = self.pits[pit]
        opp_range = player_pits(opponent(player))
        cur = pit
        for _ in range(seeds):
            cur = next_pit(cur)
            if cur == pit:          # skip source pit on wrap-around
                cur = next_pit(cur)
            if cur in opp_range:
                return True
        return False

    def _is_grand_slam(self, pit: int, player: int) -> bool:
        """True if playing *pit* would capture ALL seeds from opponent's side."""
        b = self.clone()
        b._distribute(pit, player)
        caps = b._get_capture_list(b._last_pit, player)
        seeds_left = b.seeds_on_side(opponent(player))
        captured_here = sum(b.pits[c] for c in caps)
        return (seeds_left - captured_here) == 0 and seeds_left > 0

    # -- Move execution --------------------------------------------------------

    def apply_move(self, pit: int) -> "tuple[Board, MoveResult]":
        """
        Apply *pit* for current_player.  Returns (new_board, MoveResult).
        Does NOT mutate self.
        """
        result = MoveResult()
        b      = self.clone()
        player = b.current_player

        # Distribute seeds
        dist = b._distribute(pit, player)
        result.distribution = dist

        # Capture
        caps = b._get_capture_list(b._last_pit, player)
        # Grand-slam guard already applied at move generation; honour it here too
        opp_total = b.seeds_on_side(opponent(player))
        captured_here = sum(b.pits[c] for c in caps)
        if caps and captured_here >= opp_total:
            # Would leave opponent empty - only allow if no other legal move
            legal = self.get_legal_moves(player)
            alternatives = [m for m in legal if m != pit]
            if alternatives:
                caps = []   # revoke capture

        for c in caps:
            result.captured_count += b.pits[c]
            b.captured[player]    += b.pits[c]
            b.pits[c]              = 0
        result.captures = caps

        # No-capture streak
        if caps:
            b.no_capture_streak = 0
        else:
            b.no_capture_streak += 1

        # Check immediate win
        for p in (HUMAN, AI):
            if b.captured[p] >= WIN_THRESHOLD:
                b.game_over = True
                b.winner    = p
                result.game_over  = True
                result.winner     = p
                result.end_reason = "win_threshold"
                return b, result

        # Cycle / no-progress end
        if b.no_capture_streak >= CYCLE_NO_CAPTURE_LIMIT:
            b._end_with_remaining()
            b.game_over  = True
            b.winner     = b._compute_winner()
            result.game_over  = True
            result.winner     = b.winner
            result.end_reason = "cycle_limit"
            return b, result

        # Switch player
        b.current_player = opponent(player)

        # If next player has no legal moves
        if not b.get_legal_moves():
            b._end_with_remaining()
            b.game_over = True
            b.winner    = b._compute_winner()
            result.game_over  = True
            result.winner     = b.winner
            result.end_reason = "no_legal_moves"

        return b, result

    # -- Internal helpers ------------------------------------------------------

    def _distribute(self, pit: int, player: int) -> list[int]:
        """
        Sow seeds from *pit* counter-clockwise (skipping source pit on wrap).
        Stores last landing pit in self._last_pit.
        Returns ordered list of pits that received a seed.
        """
        seeds    = self.pits[pit]
        self.pits[pit] = 0
        cur      = pit
        sequence = []
        for _ in range(seeds):
            cur = next_pit(cur)
            if cur == pit:          # skip source pit on second+ lap
                cur = next_pit(cur)
            self.pits[cur] += 1
            sequence.append(cur)
        self._last_pit = cur
        return sequence

    def _get_capture_list(self, last_pit: int, player: int) -> list[int]:
        """
        Return list of opponent pits to capture, starting from *last_pit*
        going backwards (clockwise) while count in CAPTURE_THRESHOLDS (typically: 2, 3).
        Only captures opponent's pits.
        """
        opp_range = player_pits(opponent(player))
        if last_pit not in opp_range:
            return []
        captures = []
        pit = last_pit
        while pit in opp_range and self.pits[pit] in CAPTURE_THRESHOLDS:
            captures.append(pit)
            pit = prev_pit(pit)
        return captures

    def _end_with_remaining(self):
        """Each player takes seeds remaining on their own side."""
        for p in (HUMAN, AI):
            for i in player_pits(p):
                self.captured[p] += self.pits[i]
                self.pits[i]      = 0

    def _compute_winner(self) -> int | None:
        h = self.captured[HUMAN]   # NUM_PLAYERS=2: exactly two counters
        a = self.captured[AI]
        if   h > a: return HUMAN
        elif a > h: return AI
        return None   # draw

    # -- Representation -------------------------------------------------------

    def __repr__(self) -> str:
        ai_row    = " ".join(f"{self.pits[i]:2d}" for i in range(TOTAL_PITS-1, PITS_PER_PLAYER-1, -1))
        human_row = " ".join(f"{self.pits[i]:2d}" for i in range(PITS_PER_PLAYER))
        return (
            f"AI   ({self.captured[AI]:2d}): [{ai_row}]\n"
            f"Human({self.captured[HUMAN]:2d}): [{human_row}]\n"
            f"Turn: {'Human' if self.current_player == HUMAN else 'AI'}"
        )
