from config.colors import *

DEBUG_SETTINGS = False


# DEBUG SETTINGS
if DEBUG_SETTINGS:
    SHOW_CHUNK_BORDERS = True
    LIMITED_VISION = False

else:
    SHOW_CHUNK_BORDERS = False
    LIMITED_VISION = True

# WINDOW SETTINGS
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# CAMERA SETTINGS
CAMERA_X_OFFSET = 200
CAMERA_Y_OFFSET = 200

# GRID SETTINGS
TILE_SIZE = 132
CHUNK_SIZE = 6
MIN_OPEN_AREA_SIZE = 5

# PLAYER SETTINGS
PLAYER_SPEED = 6
PLAYER_TILE_OFFSET = TILE_SIZE // 4
VISION_RADIUS = 4

# ENEMY SETTINGS
MIN_ENEMY_SPEED = 4
MAX_ENEMY_SPEED = 8
ENEMY_TILE_OFFSET = TILE_SIZE // 4
ENEMY_SPAWN_RATE = 2
MIN_ENEMIES_PER_CHUNK = 0
MAX_ENEMIES_PER_CHUNK = 5

# OBJECT COLORS
BACKGROUND_COLOR = BLUE
CHUNK_BORDER_COLOR = RED

# NOISE SETTINGS
NOISE_SCALE = 5
NOISE_OCTAVES = 6
NOSIE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2
SEED = 12

# MENU SETTINGS
MENU_COLOR = BLACK