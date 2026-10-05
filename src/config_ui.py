"""
UI skin selector.
Set SKIN to the name of a module inside src/skins/ to switch the active skin.
If the specified module cannot be loaded, the default skin is used as fallback.
"""

import importlib
import logging
import random

logger = logging.getLogger(__name__)

# All available skin modules inside the skins/ package.
SKINS = (
    "default",           # Default        - warm cream, terracotta, sky-blue
    "mint_gray",         # Mint-Gray       - light gray canvas, mint-green accents
    "vivid_1",           # Vivid-1         - vivid yellow/orange/pink/green
    "vivid_2",           # Vivid-2         - electric cobalt and cyan on pale blue
    "black_and_white",   # Black-and-White - fully monochrome, pure gray tones
    "deep_ocean",        # Deep-Ocean      - dark navy canvas, bioluminescent teal/cyan
    "sunset",            # Sunset          - amber canvas, crimson board, coral and gold
    "forest",            # Forest          - pale leafy green, deep greens and bark browns
    "candy",             # Candy           - blush white, bubble-gum pink, lavender, mint
    "midnight",          # Midnight        - near-black dark mode, electric purple/indigo
)

# Active skin: 
# To pin a specific skin, replace the line below with one of the ones listed above, e.g.: SKIN = "default"
# If you set the value as "random", then it's picked randomly.
#SKIN = "random"
SKIN = "default"

try:
    SKIN = random.choice(SKINS) if (SKIN == "random") else SKIN
    _skin = importlib.import_module(f"skins.{SKIN}")
except (ImportError, ValueError) as _err:
    logger.error("Skin '%s' could not be loaded (%s) - falling back to default", SKIN, _err)
    from skins import default as _skin


def get_name() -> str:
    """Return the display name of the active skin."""
    return _skin.SKIN_NAME


def __getattr__(name: str):
    return getattr(_skin, name)
