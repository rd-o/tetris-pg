import pygame
from OpenGL.GL import *
import numpy as np
from PIL import Image
import time

# Initialize pygame and OpenGL
pygame.init()
screen = pygame.display.set_mode((800, 800), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(0.0, 0.0, 0.0, 1.0)

# Setup Orthographic Projection
glOrtho(0, 100, 100, 0, -1, 1)

def load_and_slice_png(file_path, block_size=8):
    # Load image with Pillow
    image = Image.open(file_path).convert('RGB')
    img_width, img_height = image.size
    print(img_width, img_height)
    assert img_width % block_size == 0 and img_height % block_size == 0, \
        "Image dimensions must be a multiple of block size"

    # Slice into blocks
    blocks = []
    for y in range(0, img_height, block_size):
        for x in range(0, img_width, block_size):
            block = np.array(image.crop((x, y, x + block_size, y + block_size)))
            blocks.append(block)
    return blocks

def create_texture():
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return texture_id

def update_texture(texture_id, canvas):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, canvas.shape[1], canvas.shape[0], GL_RGB, GL_UNSIGNED_BYTE, canvas)

# Load 8x8 images from PNG
blocks = load_and_slice_png("pixels.png")
block_size = 8

# Create OpenGL texture
texture_id = create_texture()
canvas = np.zeros((800, 800, 3), dtype=np.uint8)  # 800x800 for 100x100 blocks
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 800, 800, 0, GL_RGB, GL_UNSIGNED_BYTE, canvas)

last_time = time.time()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    current_time = time.time()
    if current_time - last_time >= 0.05:  # 100 ms
        # Randomly assign a block to each position in the canvas
        for i in range(100):  # 100 rows
            for j in range(100):  # 100 columns
                block = blocks[np.random.randint(0, len(blocks))]
                canvas[i * block_size:(i + 1) * block_size,
                       j * block_size:(j + 1) * block_size] = block
        update_texture(texture_id, canvas)
        last_time = current_time

    glClear(GL_COLOR_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0, 0)
    glTexCoord2f(1, 0); glVertex2f(100, 0)
    glTexCoord2f(1, 1); glVertex2f(100, 100)
    glTexCoord2f(0, 1); glVertex2f(0, 100)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    pygame.display.flip()
