import pyglet


class Tetris:
    def __init__(self, window, screen_width, screen_height, cell_size, texture_grid):
        self.window = window
        self.cell_size = cell_size
        self.image = texture_grid[0]
        #self.sprites = sprites
        #tetris pixels, not real pixels
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.texture_grid = texture_grid
        self.batch = pyglet.graphics.Batch()
        self.sprites = []

        for y in range(screen_height):
            row = []
            for x in range(screen_width):
                sprite = pyglet.sprite.Sprite(texture_grid[-1], x=x * cell_size, y=y * cell_size, batch=self.batch)
                row.append(sprite)
            self.sprites.append(row)

    def index_to_coordinates(self, index, width):
        x = index % width
        y = index // width
        return x, y

    def calculate_coord_start(self, grid, draw_index):
        # Determine grid position based on draw_index
        cols_per_screen = self.screen_width // (len(grid[0]) * self.cell_size)
        x_offset, y_offset = self.index_to_coordinates(draw_index, cols_per_screen)

        # screen_space = 0
        # if draw_index >= 0:
        x_screen_space = self.cell_size * draw_index

        # Calculate top-left corner of the grid
        x_start = x_offset * len(grid[0]) * self.cell_size + x_screen_space
        y_start = y_offset * len(grid) * self.cell_size

        return x_start, y_start

    def draw_current_piece(self, current_piece):
        for y, row in enumerate(current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    screen_x = (current_piece.x + x) * self.cell_size
                    screen_y = (current_piece.y + y) * self.cell_size
                    sprite = self.sprites[current_piece.type]
                    sprite.x = screen_x
                    sprite.y = screen_y
                    sprite.draw()

    def draw_board(self, board, draw_index):
        self.batch.draw()

    def update_board(self, board, draw_index):
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell != -1:  # Assuming -1 represents an empty cell
                    self.sprites[y][x].image = self.texture_grid[cell]
                else:
                    self.sprites[y][x].image = self.texture_grid[-1]
        self.batch.draw()
