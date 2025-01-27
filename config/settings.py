from config.colors import *

# DEBUG SETTINGS
SHOW_CHUNK_BORDERS = True

# WINDOW SETTINGS
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60

# CAMERA SETTINGS
CAMERA_X_OFFSET = 200
CAMERA_Y_OFFSET = 200

# GRID SETTINGS
TILE_SIZE = 128
CHUNK_SIZE = 5
MIN_OPEN_AREA_SIZE = 5

# PLAYER SETTINGS
PLAYER_SPEED = 6
PLAYER_TILE_OFFSET = TILE_SIZE // 4

# ENEMY SETTINGS
ENEMY_SPEED = 6
ENEMY_TILE_OFFSET = TILE_SIZE // 4

# OBJECT COLORS
BACKGROUND_COLOR = BLUE
CHUNK_BORDER_COLOR = RED

# NOISE SETTINGS
NOISE_SCALE = 5
NOISE_OCTAVES = 6
NOSIE_PERSISTENCE = 0.5
NOISE_LACUNARITY = 2
SEED = 12