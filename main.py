import random

import pyglet
from pyglet import image
from pyglet.window import Window

from piece import Piece
from tetris import Tetris

# Set up the window
window = Window(width=800, height=600)
window.set_location(0, 0)

# Load the image
sprite_sheet = pyglet.image.load('pixels.png')

# Create a texture grid
texture_grid = image.ImageGrid(sprite_sheet, 1, 6, item_width=8, item_height=8)

# Create a list of sprites
#sprites = [pyglet.sprite.Sprite(texture_grid[i]) for i in range(5)]

current_piece = Piece(0, 10)
a = 100
b = 100
tetris = Tetris(window, a, b, 8, texture_grid)
board = [[3 for _ in range(10)] for _ in range(20)]
board[0][0] = 1
board[1][1] = 2
board[9][9] = 3
board[0][1] = 3

def create_random_board(rows, cols):
    return [[random.randint(0, 4) for _ in range(cols)] for _ in range(rows)]
board = create_random_board(a, b)
print(board)

@window.event
def on_draw():
    window.clear()
    #tetris.draw_current_piece(current_piece)
    tetris.draw_board(board, 0)
    #for i, sprite in enumerate(sprites):
    #    sprite.x = i * 10  # Adjust the x position for each sprite
    #    sprite.y = window.height // 2  # Center the sprites vertically
    #    sprite.draw()

def update_board(dt):
    global board
    board = create_random_board(a, b)
    tetris.update_board(board, 0)

pyglet.clock.schedule_interval(update_board, 0.1)  # Update every 100ms

# Run the application
pyglet.app.run()
