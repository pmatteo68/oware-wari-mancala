"""
Entry point - run this file to start Oware / Wari (Mancala).

    python main.py

Python 3.8+ required.  tkinter must be available (it is bundled with the
standard CPython installer on Windows and macOS; on Linux install
python3-tk via your package manager).
"""

import sys
import os

# Ensure the mancala package dir is on the path regardless of where we launch from
sys.path.insert(0, os.path.dirname(__file__))

import log_config
log_config.setup()

import logging
logger = logging.getLogger(__name__)


def _check_config():
    from config_game import NUM_PLAYERS
    if NUM_PLAYERS != 2:
        msg = (
            f"CONFIG ERROR: NUM_PLAYERS={NUM_PLAYERS} is not supported. "
            "This game is designed for exactly 2 players. "
            "Set again the number of players to 2 (TWO) in the configuration file."
        )
        logger.error(msg)
        sys.exit(msg)

import tkinter as tk
from ui_main import MancalaApp
from sw_metadata import getSWName, getVersion, getRulesDesc
import ai_engine
import config_ui

def main():
    _check_config()
    logger.info("=== %s v. %s (rules: %s), AI: %s, Skin: %s ===",
                 getSWName(), getVersion(), getRulesDesc(),
                 ai_engine.get_name(), config_ui.get_name())

    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
        logger.debug("DPI awareness configured (Windows)")
    except Exception as e:
        logger.debug("DPI awareness setup failed: [%s] %s"
                     " (expected and harmless on non-Windows platforms)", type(e).__name__, e)
        # pass

    logger.debug("Creating MancalaApp")
    app = MancalaApp(root)

    root.update_idletasks()
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = root.winfo_width()
    wh = root.winfo_height()
    x, y = (sw - ww) // 2, (sh - wh) // 2
    root.geometry(f"+{x}+{y}")
    logger.debug("Window centered at (%d, %d) on %dx%d screen", x, y, sw, sh)

    logger.debug("Entering main event loop")
    root.mainloop()
    logger.info("=== Application exited ===")


if __name__ == "__main__":
    main()
