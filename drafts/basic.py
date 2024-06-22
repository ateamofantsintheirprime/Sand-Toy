def sand_count(pixels):
    count = 0
    for row in pixels:
        for cell in row:
            if any(cell):
                count +=1
    return count

def print_pixels(pixels):
    result = [[0 for y in range(len(pixels[0]))] for x in range(len(pixels))]
    for x in range(len(pixels)):
        for y in range(len(pixels[0])):
            if pixels[x][y][0]:
                result[y][x] = '@'
            else:
                result[y][x] = ' '

    print([' ']+[str(x) for x in range(len(pixels))])
    for y in range(len(result[0])):
        print([str(y)] + result[y])
    print()

def add_sand(mouse_pos, radius, pixels):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    for y_offset in range(-radius, radius):
        for x_offset in range(-radius, radius):
            if y_offset+mouse_y < 0 or y_offset+mouse_y >= len(pixels[0]):
                continue
            if x_offset+mouse_x < 0 or x_offset+mouse_x >= len(pixels):
                continue
            if pow(y_offset,2) + pow(x_offset,2) > pow(radius,2):
                continue
            
            draw_sand(1, x_offset+mouse_x, y_offset+mouse_y, pixels)
            # pixels[x_offset+mouse_x][y_offset+mouse_y] = 255

def draw_sand(on_off, x,y,pixels):
    pixels[x][y] = [on_off*255 for i in range(3)]

def move_sand(src, dest, pixels):
    draw_sand(0,src[0],src[1],pixels)
    draw_sand(1,dest[0],dest[1],pixels)
