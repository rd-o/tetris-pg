from tetris_game import TetrisGame
from draw_tetris import DrawTetris

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 8

# Game variables
fall_time = 0
score = 0
draw_tetris_instance = DrawTetris(screen_width, screen_height, block_size)


def main():

    run = True
    game_instance = TetrisGame(10, 20)
    game_instance.setup_instance(draw_tetris_instance, 0, None)

    while run:
        run = game_instance.update_with_multiple_graphics()

    draw_tetris_instance.exit()

main()
