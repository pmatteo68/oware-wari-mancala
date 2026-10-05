"""
Save and load Board state to/from a human-readable JSON file.
No UI imports - pure I/O logic.

File format (example):
{
    "format_version": 1,
    "pits": [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    "captured": [0, 0],
    "current_player": 0,
    "no_capture_streak": 0
}
"""

import json
import logging
from game_logic import Board

logger = logging.getLogger(__name__)
from config_game import NUM_PLAYERS, PITS_PER_PLAYER

FORMAT_VERSION = 1
FILE_ENCODING = "utf-8"

num_of_players = NUM_PLAYERS
pits_per_player = PITS_PER_PLAYER

def save_game(board: Board, path: str) -> None:
    """Serialize *board* to a JSON file at *path*. Raises on I/O error."""
    logger.debug("Saving game to '%s'", path)
    data = {
        "format_version":    FORMAT_VERSION,
        "pits":              board.pits[:],
        "captured":          board.captured[:],
        "current_player":    board.current_player,
        "no_capture_streak": board.no_capture_streak,
    }
    logger.debug("Save payload: pits=%s | captured=%s | player=%d | streak=%d",
                 data["pits"], data["captured"],
                 data["current_player"], data["no_capture_streak"])
    try:
        with open(path, "w", encoding=FILE_ENCODING) as f:
            json.dump(data, f, indent=2)
        logger.debug("Game saved successfully to '%s'", path)
    except Exception as e:
        logger.error("Failed to save game to '%s': %s", path, e)
        raise


def load_game(path: str) -> Board:
    """
    Deserialize a Board from *path*.
    Raises ValueError on schema mismatch, OSError on I/O error.
    """
    logger.debug("Loading game from '%s'", path)
    try:
        with open(path, "r", encoding=FILE_ENCODING) as f:
            data = json.load(f)
    except Exception as e:
        logger.error("Failed to read file '%s': %s", path, e)
        raise

    try:
        _validate(data)
    except ValueError as e:
        logger.error("Validation failed for '%s': %s", path, e)
        raise

    board = Board.__new__(Board)
    board.pits               = list(data["pits"])
    board.captured           = list(data["captured"])
    board.current_player     = int(data["current_player"])
    board.no_capture_streak  = int(data["no_capture_streak"])
    board.game_over          = False
    board.winner             = None
    logger.debug("Game loaded from '%s' | pits=%s | captured=%s | player=%d | streak=%d",
                path, board.pits, board.captured,
                board.current_player, board.no_capture_streak)
    return board


def _validate(data: dict) -> None:
    if data.get("format_version") != FORMAT_VERSION:
        raise ValueError(
            f"Unsupported save format (version {data.get('format_version')})"
        )
    if not isinstance(data.get("pits"), list) or len(data["pits"]) != (num_of_players * pits_per_player):
        raise ValueError("Invalid 'pits' field")
    if not isinstance(data.get("captured"), list) or len(data["captured"]) != num_of_players:
        raise ValueError("Invalid 'captured' field")
    #if data.get("current_player") not in (0, 1):
    if data.get("current_player") not in range(num_of_players):
        raise ValueError("Invalid 'current_player' field")

