"""
===========================================
Space Invader V2
settings.py

Stores every configurable value in the game.

Nothing in this file should contain game logic.
It only contains constants.
===========================================
"""

# ===========================================
# Window
# ===========================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 630

WINDOW_TITLE = "Space Invader V2"

FPS = 60

BACKGROUND_COLOR = (255, 255, 255)

# ===========================================
# Player
# ===========================================

PLAYER_SPEED = 6

PLAYER_LIVES = 3

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60

# ===========================================
# Invaders
# ===========================================

INVADER_ROWS = 3
INVADER_COLUMNS = 10

INVADER_WIDTH = 42
INVADER_HEIGHT = 42

INVADER_SPACING_X = 70
INVADER_SPACING_Y = 70

INVADER_START_Y = 50

INVADER_STEP_DISTANCE = 20
INVADER_DROP_DISTANCE = 25

INVADER_STEP_DELAY = 500

# ===========================================
# Bullets
# ===========================================

BULLET_WIDTH = 6
BULLET_HEIGHT = 18

USER_BULLET_SPEED = 10
INVADER_BULLET_SPEED = 6

COOLDOWN = 333
INVADER_COOLDOWN = 1000

# ===========================================
# Shields
# ===========================================

SHIELD_COUNT = 4

SHIELD_WIDTH = 70
SHIELD_HEIGHT = 40

# Each shield is made from small blocks
SHIELD_BLOCK_SIZE = 5

# Distance from bottom of screen
SHIELD_Y_OFFSET = 170

# ===========================================
# Colours
# ===========================================

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 0, 255)

# ===========================================
# Supabase
# ===========================================
SUPABASE_URL = "https://bzrqnprelyfkxusehxcv.supabase.co"
SUPABASE_KEY = "sb_publishable_PQrA9UKUtruI1OkdrkC-rQ_lHWWVdbs"