"""
Logging configuration for the game.
Edit the three settings below  -  no other file needs changing.
"""

import logging

# -- User-editable settings ----------------------------------------------------
LOG_LEVEL   = logging.INFO   # DEBUG / INFO / WARNING / ERROR / CRITICAL
LOG_FILE    = "mancala.log"   # relative path for the log file; None = no file output
LOG_CONSOLE = True           # True = also echo log lines to stderr

# -- Internal ------------------------------------------------------------------
_FMT = (
    "%(asctime)s.%(msecs)03d "
    "[%(threadName)s] "
    "%(levelname)s "
    "%(name)s:%(lineno)d - "
    "%(message)s"
)
_DATE = "%Y-%m-%d %H:%M:%S"


def setup() -> None:
    """Configure the root logger.  Call once at application startup."""
    root = logging.getLogger()
    if root.handlers:           # guard against double-init
        return
    root.setLevel(LOG_LEVEL)
    fmt = logging.Formatter(_FMT, datefmt=_DATE)
    if LOG_FILE:
        fh = logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
        fh.setFormatter(fmt)
        root.addHandler(fh)
    if LOG_CONSOLE:
        import sys
        ch = logging.StreamHandler(sys.stderr)
        ch.setFormatter(fmt)
        root.addHandler(ch)
