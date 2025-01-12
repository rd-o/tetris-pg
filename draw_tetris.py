import glfw
import numpy as np
from PIL import Image
from OpenGL.GL import *

class DrawTetris:
    def __init__(self, screen_width, screen_height, block_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size
        self.blocks = self.load_and_slice_png("pixels.png")  # Replace with the correct path
        self.canvas = None
        self.texture_id = None
        self.window = None
        self.init_opengl(screen_width, screen_height)
        self.game_instance = None


#    def init_opengl(self, screen_width, screen_height):
#        if not glfw.init():
#            raise Exception("Failed to initialize GLFW")
#
#        # Create a window
#        self.window = glfw.create_window(screen_width, screen_height, "OpenGL Canvas", None, None)
#        if not self.window:
#            glfw.terminate()
#            raise Exception("Failed to create GLFW window")
#
#        # Make the OpenGL context current
#        glfw.make_context_current(self.window)
#        glClearColor(0.0, 0.0, 0.0, 1.0)
#        glViewport(0, 0, 200, 200)
#        glOrtho(0, 100, 100, 0, -1, 1)
#
#        # Create texture and canvas
#        self.texture_id = self.create_texture()
#        self.canvas = np.zeros((200, 200, 3), dtype=np.uint8)  # 100x100 blocks
#        self.update_texture(self.texture_id, self.canvas)
#        glfw.set_key_callback(self.window, self.key_events)

    def init_opengl(self, screen_width, screen_height):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        # Create a window
        self.window = glfw.create_window(screen_width, screen_height, "OpenGL Canvas", None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        # Make the OpenGL context current
        glfw.make_context_current(self.window)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, screen_width, screen_height)
        glOrtho(0, screen_width, screen_height, 0, -1, 1)

        # Create texture and canvas
        self.texture_id = self.create_texture()
        self.canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)  # Adjust canvas size
        self.update_texture(self.texture_id, self.canvas)
        glfw.set_key_callback(self.window, self.key_events)

    def create_texture(self):
        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return texture_id

    def update_texture_2(self, texture_id, canvas):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas.shape[1], canvas.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, canvas)

        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(0, 0)
        glTexCoord2f(1, 0); glVertex2f(100, 0)
        glTexCoord2f(1, 1); glVertex2f(100, 100)
        glTexCoord2f(0, 1); glVertex2f(0, 100)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def update_texture(self, texture_id, canvas):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, canvas.shape[1], canvas.shape[0], 0, GL_RGB, GL_UNSIGNED_BYTE, canvas)

        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.screen_width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.screen_width, self.screen_height)
        glTexCoord2f(0, 1)
        glVertex2f(0, self.screen_height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glfw.swap_buffers(self.window)
        glfw.poll_events()

    def load_and_slice_png(self, file_path, block_size=8):
        image = Image.open(file_path).convert('RGB')
        img_width, img_height = image.size
        assert img_width % block_size == 0 and img_height % block_size == 0, \
            "Image dimensions must be a multiple of block size"

        blocks = []
        for y in range(0, img_height, block_size):
            for x in range(0, img_width, block_size):
                block = np.array(image.crop((x, y, x + block_size, y + block_size)), dtype=np.uint8)
                blocks.append(block)
        return blocks

    def index_to_coordinates(self, index, width):
        x = index % width
        y = index // width
        return x, y

#    def draw_grid(self, grid, draw_index):
#        for y, row in enumerate(grid):
#            for x, cell in enumerate(row):
#                color = cell if isinstance(cell, tuple) else (0, 0, 0)
#                pygame.draw.rect(self.screen, color, (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 0)
#                pygame.draw.rect(self.screen, (128, 128, 128), (x * self.block_size, y * self.block_size, self.block_size, self.block_size), 1)

    def draw_grid(self, grid, draw_index):
        """
        Draws a grid at a specific position determined by draw_index.

        :param grid: The grid data (2D list) to be drawn.
        :param draw_index: The index determining the grid's position on the screen.
        """

        x_start, y_start = self.calculate_coord_start(grid, draw_index)

        # Draw the grid at the calculated position
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                #color = cell if isinstance(cell, tuple) else (0, 0, 0)  # Default to black if not a tuple
                #rect = (x_start + x * self.block_size, y_start + y * self.block_size, self.block_size, self.block_size)
                #pygame.draw.rect(self.screen, color, rect, 0)  # Draw cell
                #pygame.draw.rect(self.screen, (128, 128, 128), rect, 1)  # Draw grid outline
                block = self.blocks[cell]
                y1 = y * self.block_size
                y2 = (y + 1) * self.block_size
                x1 = x * self.block_size
                x2 = (x + 1) * self.block_size
                self.canvas[y * self.block_size:(y + 1) * self.block_size,
                x * self.block_size:(x + 1) * self.block_size] = block
        #self.update_texture(self.texture_id, self.canvas)

#    def draw_current_piece(self, game_instance, draw_index):
#            for y, row in enumerate(game_instance.current_piece.shape):
#                for x, cell in enumerate(row):
#                    if cell:
#                        pygame.draw.rect(self.screen, game_instance.current_piece.color, (game_instance.current_piece.x * self.block_size + x * self.block_size, game_instance.current_piece.y * self.block_size + y * self.block_size, self.block_size, self.block_size), 0)
    def calculate_coord_start(self, grid, draw_index):
        # Determine grid position based on draw_index
        cols_per_screen = self.screen_width // (len(grid[0]) * self.block_size)
        x_offset, y_offset = self.index_to_coordinates(draw_index, cols_per_screen)

        # Calculate top-left corner of the grid
        x_start = x_offset * len(grid[0]) * self.block_size
        y_start = y_offset * len(grid) * self.block_size

        return x_start, y_start

    def draw_current_piece(self, game_instance, draw_index):
        """
        Draws the current piece of a Tetris game at a position determined by draw_index.

        :param game_instance: The game instance containing the current piece.
        :param draw_index: The index determining the position of the game on the screen.
        """
        x_start, y_start = self.calculate_coord_start(game_instance.grid, draw_index)

        # Draw the current piece at the calculated position
        for y, row in enumerate(game_instance.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    block = self.blocks[game_instance.current_piece.type]
                    #self.canvas[y * self.block_size:(y + 1) * self.block_size,
                    #x * self.block_size:(x + 1) * self.block_size] = block
                    self.canvas[(y_start + game_instance.current_piece.y + y) * self.block_size:
                                (y_start + game_instance.current_piece.y + y + 1) * self.block_size,
                    (x_start + game_instance.current_piece.x + x) * self.block_size:
                    (x_start + game_instance.current_piece.x + x + 1) * self.block_size] = block


        self.update_texture(self.texture_id, self.canvas)



    def draw_splash_screen(self):
        pass
#        self.screen.fill((0, 0, 0))  # Fill background with black before blitting the image
#        splash_rect = self.splash_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
#        self.screen.blit(self.splash_image, splash_rect)
#        pygame.display.update()
#
#        waiting = True
#        while waiting:
#            for event in pygame.event.get():
#                if event.type == pygame.QUIT:
#                    pygame.quit()
#                    quit()
#                if event.type == pygame.KEYDOWN:
#                    waiting = False

    def draw_text(self, text, size, color, x, y):
        pass
        #label = self.font.render(text, 1, color)
        #self.screen.blit(label, (x, y))

    def exit(self):
        pass
        #self.screen.fill((0, 0, 0))  # Fill the screen with black before showing "Game Over"
        #self.draw_text("Game Over", 60, (255, 0, 0), self.screen_width // 2 - 150, self.screen_height // 2 - 30)
        #pygame.display.update()
        #pygame.time.delay(2000)
        #pygame.quit()

    def key_events(self, window, key, scancode, action, mods):
        if action == glfw.PRESS:
            if key == glfw.KEY_ESCAPE:
                print("Escape key pressed. Exiting...")
                glfw.set_window_should_close(window, True)
            elif key == glfw.KEY_W:
                self.game_instance.rotate_piece()
            elif key == glfw.KEY_A:
                self.game_instance.move_piece_left()
            elif key == glfw.KEY_S:
                self.game_instance.move_piece_down()
            elif key == glfw.KEY_D:
                self.game_instance.move_piece_right()
        elif action == glfw.RELEASE:
            print(f"Key {key} released")

    def update(self):
        pass
        #pygame.display.update()

    #def get_clock(self):
    #    return self.

    #def get_free_space():
        

            
