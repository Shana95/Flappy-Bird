"""Global configuration settings for Flappy Bird."""

# =========================================
# DISPLAY & CORE MECHANICS
# =========================================
ORIGINAL_WIDTH = 288
ORIGINAL_HEIGHT = 512
FPS = 60
VELOCITY = 2
SPAWN_PIPE_TIMER = 2000

# =========================================
# ASSETS (IMAGES & FONTS)
# =========================================
FILE_SKY = "background-day.png"
FILE_GROUND = "base.png"
FILE_START = "message.png"
FILE_GAMEOVER = "gameover.png"
FONT_BORDER = "flappyborder.ttf"
FONT_FILL = "flappyfill.ttf"

# =========================================
# POSITIONS & ENTITIES
# =========================================
# Sky & Ground
SKY_POS_X = 0
SKY_POS_Y = 0
GROUND_POS_X = 0
GROUND_POS_Y = 560
GROUND_OFFSET = 560

# Bird
BIRD_START_X = 90
BIRD_START_Y = 220

# Pipes
PIPE_MIN_Y = 150
PIPE_MAX_Y = 350
PIPE_GAP_MIN = 75
PIPE_GAP_MAX = 100
PIPE_SPAWN_OFFSET = 50

# =========================================
# UI & SCORE SETTINGS
# =========================================
# Screens Positioning
START_SCREEN_X = 150
START_SCREEN_Y = 305
GAMEOVER_SCREEN_X = 150
GAMEOVER_SCREEN_Y = 200

# Score Positioning (X is calculated dynamically in main)
SCORE_POS_Y = 50

# Screen Transparency Logic
START_TRANSPARENCY_INIT = 255
START_TRANSPARENCY_TARGET = 0
GAMEOVER_TRANSPARENCY_INIT = 0
GAMEOVER_TRANSPARENCY_TARGET = 255
