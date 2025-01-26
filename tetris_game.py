import random
import copy

from piece import Piece
import time

shapes = [
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]]  # J
]


class TetrisGame:
    def __init__(self, width, height):
        # self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = Piece(random.choice(shapes), width)
        self.next_piece = Piece(random.choice(shapes), width)
        self.game_over = False
        self.score = 0
        self.width = width
        self.height = height
        self.locked_positions = [[0 for _ in range(width)] for _ in range(height)]
        self.manual_instance = False
        self.lines = 0
        self.level = 0
        # self.initialize_game()

    def lock(self):
        self.current_piece.lock(self.locked_positions)

    def initialize_game(self):
        # Initialize the grid, current piece, and other game state variables
        self.grid = [[0 for _ in range(10)] for _ in range(20)]  # Example 10x20 grid
        self.spawn_new_piece()

    def spawn_new_piece(self):
        # Logic to add a new piece to the grid

        self.current_piece = Piece(random.choice(shapes), self.width)

    def __move_piece_left(self, grid, current_piece):
        if not current_piece.collision(-1, 0, grid):
            current_piece.x -= 1

    def move_piece_left(self):
        self.__move_piece_left(self.grid, self.current_piece)

    def __move_piece_right(self, grid, current_piece):
        if not current_piece.collision(1, 0, grid):
            current_piece.x += 1

    def move_piece_right(self):
        self.__move_piece_right(self.grid, self.current_piece)

    def __move_piece_down(self, grid, current_piece):
        i = 0
        while (not current_piece.collision(0, i + 1, grid)):
            i += 1

        current_piece.y += i

    def move_piece_down(self):
        self.__move_piece_down(self.grid, self.current_piece)

    #    def __rotate_piece(self, grid, current_piece):
    #        if not current_piece.collision(0, 0, grid):
    #            for _ in range(3):
    #                current_piece.rotate()

    def __rotate_piece(self, grid, current_piece):
        original_shape = current_piece.shape[:]
        current_piece.rotate()

        # Check if the rotated piece is out of bounds or collides
        if current_piece.collision(0, 0, grid):
            # Try shifting left
            if not current_piece.collision(-1, 0, grid):
                current_piece.x -= 1
            # Try shifting right
            elif not current_piece.collision(1, 0, grid):
                current_piece.x += 1
            # If both fail, revert rotation
            else:
                current_piece.shape = original_shape

    def rotate_piece(self):
        self.__rotate_piece(self.grid, self.current_piece)

    def drop_piece(self):
        # Logic to drop the piece down
        pass

    def collision(self, dx, dy):
        self.current_piece.collision(dx, dy, self.grid)

    def update_game_state(self):
        if not self.current_piece.collision(0, 1, self.grid):
            print("move piece")
            self.current_piece.y += 1
        else:
            self.current_piece.lock(self.locked_positions)
            self.current_piece = self.next_piece
            self.next_piece = Piece(random.choice(shapes), self.width)
            if self.current_piece.collision(0, 0, self.locked_positions):
                return False
        return True

    def __calculate_score(self, grid, locked_positions, score):
        cleared = 0
        full_rows = []
        for y in range(len(grid) - 1, -1, -1):
            row = grid[y]
            if 0 not in row:
                cleared += 1
                full_rows.append(y)

        for row in full_rows:
            for move_y in range(row, 0, -1):
                for x in range(len(grid[move_y])):
                    grid[move_y][x] = grid[move_y - 1][x]
                    locked_positions[move_y][x] = locked_positions[move_y - 1][x]
            grid[0] = [0 for _ in range(self.width)]
            locked_positions[0] = [0 for _ in range(self.width)]

        score += cleared * 100  # Update score based on cleared rows
        self.lines += cleared
        return score

    def calculate_score(self):
        self.score = self.__calculate_score(self.grid, self.locked_positions, self.score)
        return self.score

    def create_grid(self):
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y, row in enumerate(self.locked_positions):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[y][x] = cell
        return self.grid

    def get_current_piece(self):
        return self.current_piece

    def get_possible_moves(self):
        # Returns a list of all valid moves
        return ['left', 'right', 'rotate', 'down']
        # return ['left', 'right', 'rotate']

    def move(self, move):
        if move == "Left":
            self.move_piece_left()
        elif move == "Right":
            self.move_piece_right()
        elif move == "Rotate":
            self.rotate_piece()
        elif move == "Down":
            self.move_piece_down()

    def copy_variables_for_simulation(self):
        self.simulated_piece = copy.deepcopy(self.current_piece)
        self.simulated_locked_positions = copy.deepcopy(self.locked_positions)  # [row[:] for row in self.locked_positions]

    def simulate_move(self, move, simulated_grid):
        # simulated_grid = [row[:] for row in self.grid]
        #simulated_piece = copy.deepcopy(self.current_piece)  # Assume this is an object with piece shape data
        #simulated_locked_positions = copy.deepcopy(self.locked_positions)  # [row[:] for row in self.locked_positions]
        simulated_score = 0

        if move == "Left":
            self.__move_piece_left(simulated_grid, self.simulated_piece)
        elif move == "Right":
            self.__move_piece_right(simulated_grid, self.simulated_piece)
        elif move == "Rotate":
            self.__rotate_piece(simulated_grid, self.simulated_piece)
        elif move == "Down":
            self.__move_piece_down(simulated_grid, self.simulated_piece)

        self.simulated_piece.lock(self.simulated_locked_positions)

        #just to test simulation
        #self.draw_tetris_instance.draw_grid(self.grid, self.draw_index)
        #self.draw_tetris_instance.draw_current_piece(self.grid, self.simulated_piece, self.draw_index)
        #self.__calculate_score(simulated_grid, simulated_locked_positions, simulated_score)

        # lines_cleared = self.__calculate_lines_cleared(simulated_grid)
        # height = self.__calculate_height(simulated_grid)
        # holes = self.__calculate_holes(simulated_grid)
        # wells = self.__calculate_wells(simulated_grid)
        #lines_cleared = self.__calculate_lines_cleared(simulated_locked_positions)
        #height = self.__calculate_height(simulated_locked_positions)
        #holes = self.__calculate_holes(simulated_locked_positions)
        #wells = self.__calculate_wells(simulated_locked_positions)

        #return {
        #    "lines_cleared": lines_cleared,
        #    "height": height,
        #    "holes": holes,
        #    "wells": wells,
        #}

    def __calculate_lines_cleared(self, grid):
        """Count the number of full lines cleared."""
        return sum(1 for row in grid if all(row))

    def __calculate_height(self, grid):
        """Find the maximum height of the columns."""
        for y, row in enumerate(grid):
            if any(row):
                return len(grid) - y
        return 0

    def __calculate_holes(self, grid):
        """Count the number of holes in the grid."""
        holes = 0
        for x in range(len(grid[0])):  # Iterate over each column
            found_filled = False
            for y in range(len(grid)):  # Top to bottom
                if grid[y][x]:
                    found_filled = True
                elif found_filled and not grid[y][x]:
                    holes += 1
        return holes

    def __calculate_wells(self, grid):
        """Count the number of wells in the grid."""
        wells = 0
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if grid[y][x] == 0:
                    if (x == 0 or grid[y][x - 1] != 0) and (x == len(grid[0]) - 1 or grid[y][x + 1] != 0):
                        wells += 1
        return wells

    def setup_nn_ga_instance(self, draw_tetris_instance, draw_index):
        self.score = 0
        self.draw_tetris_instance = draw_tetris_instance
        self.draw_tetris_instance.game_instance = self
        # self.clock = self.draw_tetris_instance.clock()
        self.run = True
        self.draw_index = draw_index

    def setup_instance(self, draw_tetris_instance, draw_index, chromosome):
        self.fall_time = 0
        self.score = 0
        self.draw_tetris_instance = draw_tetris_instance
        self.draw_tetris_instance.game_instance = self
        # self.clock = self.draw_tetris_instance.clock()
        self.run = True
        self.fall_speed = 0.27
        # self.fall_speed = 0.03
        # self.fall_speed = 0.01
        # self.fall_speed = 0.005
        self.fall_time = 0

        self.move_time = 0
        # self.move_speed = 1
        # self.move_speed = 0.1
        self.move_speed = 0.005
        self.draw_index = draw_index
        self.fall_last_time = time.time()
        self.move_last_time = self.fall_last_time
        self.chromosome = chromosome

    def check_movement(self, chromosome):
        #self.move_time += time.time() - self.last_time
        current_time = time.time()
        elapsed_time = current_time - self.fall_last_time
        if elapsed_time >= self.move_speed:
            self.fall_last_time = current_time
            move = chromosome.choose_move(self, self.grid)  # Implement `choose_move` in chromosome
            # print('move: ')
            # print(move)
            self.move(move)

    def update_with_single_graphic(self):
        self.create_grid()

        #self.run = self.update_game_state()

        self.draw_tetris_instance.draw_grid(self.grid, self.draw_index)
        self.draw_tetris_instance.draw_current_piece(self.grid, self.current_piece, self.draw_index)

        score = self.calculate_score()
        self.draw_tetris_instance.draw_text(f"Score: {score}", 30, (255, 255, 255), 10, 10)
        print("Score: ", score)
        self.draw_tetris_instance.update()
        return self.run

    def stop(self):
        pass

    def reset_game(self):
        self.current_piece = Piece(random.choice(shapes), self.width)
        self.next_piece = Piece(random.choice(shapes), self.width)
        self.game_over = False
        self.score = 0
        self.locked_positions = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.manual_instance = False
        self.lines = 0
        self.level = 0

    def update_with_multiple_graphics(self):
        self.create_grid()
        #self.fall_time += time.time() - self.last_time
        current_time_1 = time.time()
        fall_elapsed_time = current_time_1 - self.fall_last_time
        move_elapsed_time = current_time_1 - self.move_last_time
        #print(self.fall_time)
        #self.draw_tetris_instance.clock.tick()

        if fall_elapsed_time >= self.fall_speed:
            self.fall_last_time = current_time_1
            #self.fall_time = 0
            self.run = self.update_game_state()
            self.game_over = not self.run
            send_draw_grid = True

        # draw_tetris_instance.key_events(self)
        #self.grid[0][0] = 1
        if not self.manual_instance and move_elapsed_time >= self.move_speed:
            self.move_last_time = current_time_1
            #move = self.chromosome.choose_move(self, self.grid)  # Implement `choose_move` in chromosome
            #print('move: ')
            #print(move)
            #self.move(move)
            send_draw_piece = True

        self.draw_tetris_instance.draw_background()
        self.draw_tetris_instance.draw_number(self.score, 100, 4)
        self.draw_tetris_instance.draw_number(0, 100, 25)
        self.draw_tetris_instance.draw_number(self.lines, 100, 44)
        self.draw_tetris_instance.draw_grid(self.grid, self.draw_index)
        self.draw_tetris_instance.draw_current_piece(self.grid, self.current_piece, self.draw_index)

        score = self.calculate_score()
        self.draw_tetris_instance.draw_text(f"Score: {score}", 30, (255, 255, 255), 10, 10)
        self.draw_tetris_instance.update()
        return self.run
