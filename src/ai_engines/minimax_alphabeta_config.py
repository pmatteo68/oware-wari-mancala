# Minimax Alpha-Beta AI Engine configuration

# -- AI evaluation weights ----------------------------------------------------
# Positive = good for AI (maximising player)
EVAL_SEED_DIFF_WEIGHT      = 100   # weight for (ai_captured - human_captured)
EVAL_THREATENED_WEIGHT     = 8     # weight per seed the AI can capture next turn
EVAL_OPPONENT_THREAT_WEIGHT = 6    # penalty per seed human can capture next turn
EVAL_BOARD_CONTROL_WEIGHT  = 2     # weight for seeds on AI's own side
EVAL_MOBILITY_WEIGHT       = 3     # weight for number of available moves (AI)

# -- AI Depth
AI_DEPTH        = 6          # minimax search depth (higher = stronger, slower)
