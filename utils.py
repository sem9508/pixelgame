import pygame
import noise
from config.settings import *

def get_player_chunk_and_tile(player_x, player_y, chunk_size, tile_size):
    # Calculate chunk coordinates
    chunk_x = player_x // (chunk_size * tile_size)
    chunk_y = player_y // (chunk_size * tile_size)

    # Calculate tile coordinates within the chunk
    row = (player_y // tile_size) % chunk_size  # Use integer division
    col = (player_x // tile_size) % chunk_size  # Use integer division

    return int(chunk_x), int(chunk_y), int(row), int(col)
