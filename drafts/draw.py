import pygame
from math import pow
import random
from concurrent.futures import ThreadPoolExecutor
from basic import draw_sand

def simulate_grain(x,y,pixels):
    left, right, below, bottom_right, bottom_left= 0,0,0,0,0

    if x+1 >= len(pixels) or pixels[x+1][y][0]:
        right = 1
    if x-1 < 0 or pixels[x-1][y][0]:
        left = 1
    if pixels[x][y+1][0]:
        below = 1
    if x+1 >= len(pixels) or pixels[x+1][y+1][0]:
        bottom_right = 1
    if x-1 < 0 or pixels[x-1][y+1][0]:
        bottom_left = 1
    # print(f"x:{x},y:{y}, l:{left},r:{right},b:{below},bl:{bottom_left},br:{bottom_right}")
    # print_pixels(pixels)

    if not below:
        draw_sand(0,x,y,pixels)
        draw_sand(1,x,y+1,pixels)
        return
    if (bottom_left or left) and (bottom_right or right):
        draw_sand(1,x,y,pixels)
        return
    if not (left or right or bottom_left or bottom_right):
        # There is no direction of flow we can garner
        left_over_right = y%2
        if left_over_right:
            draw_sand(0,x,y,pixels)
            draw_sand(1,x-1,y+1,pixels)
        else:
            draw_sand(0,x,y,pixels)
            draw_sand(1,x+1,y+1,pixels)
        return
    if not bottom_left and not left:
        # nothing on the left => something on the right
        draw_sand(0,x,y,pixels)
        draw_sand(1,x-1,y+1,pixels)
        return
    else:
        # something on the left => nothing on the right
        draw_sand(0,x,y,pixels)
        draw_sand(1,x+1,y+1,pixels)

def step_simulation(pixels):

    assert len(pixels) % 2 == 0
    assert len(pixels[0]) % 2 == 0

    for y_i in range(len(pixels[0])):
        for x_i in range(len(pixels)):
            if random.random() > .5:
                continue
            y = len(pixels[0])-1-y_i
            if x_i % 2:
                x = len(pixels)-x_i
            else:
                x = x_i
            if y >= len(pixels[0])-1:
                continue
            pixels[x][y]
            if pixels[x][y][0]:
                simulate_grain(x,y,pixels)

def threaded_simulation_step(pixels):
    assert len(pixels) % 2 == 0
    assert len(pixels[0]) % 2 == 0
    with ThreadPoolExecutor(max_workers=50) as executor:
        for y_i in range(len(pixels[0])):
            for x_i in range(len(pixels)):
                if random.random() > .5:
                    continue
                y = len(pixels[0])-1-y_i
                if x_i % 2:
                    x = len(pixels)-x_i
                else:
                    x = x_i
                if y >= len(pixels[0])-1:
                    continue
                pixels[x][y]
                if pixels[x][y][0]:
                    executor.submit(simulate_grain, x, y, pixels)
        executor.shutdown()