# config.py
# ==========================================
# CONFIGURATION & CONSTANTS
# ==========================================

SCREEN_W, SCREEN_H = 1280, 720
FPS = 120

# World Settings
TILE_W_BASE, TILE_H_BASE = 96, 48
MAP_W, MAP_H = 40, 40

# Zoom Limits
ZOOM_MIN = 0.5
ZOOM_MAX = 1.5

# Player Defaults
PLAYER_BASE_SPEED = 5.0
PLAYER_START_HP = 100
PLAYER_START_GRENADES = 3

# Physics Constants
GRAVITY = 20.0
FRICTION = 0.9

# Colors
COL_BG = (10, 10, 15)
COL_UI_BG = (20, 20, 30)
COL_UI_BORDER = (80, 80, 100)
COL_TEXT = (220, 220, 220)
COL_MONEY = (255, 215, 0)
COL_GRENADE = (50, 100, 50)
COL_EXPLOSION = (255, 100, 50)