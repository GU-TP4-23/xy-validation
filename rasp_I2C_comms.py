# I2C here
ratio = 1
iter = 2

def XY_up(coor_x, coor_y):
    print("\t\tup")
    return coor_x, coor_y + iter*ratio

def XY_down(coor_x, coor_y):
    print("\t\tdown")
    return coor_x, coor_y - iter*ratio

def XY_left(coor_x, coor_y):
    print("\t\tleft")
    return coor_x - iter*ratio, coor_y

def XY_right(coor_x, coor_y):
    print("\t\tright")
    return coor_x + iter*ratio, coor_y

def Z_up(coor_x, coor_y):
    print("\t\tlift")
    pass

def Z_down(coor_x, coor_y):
    print("\t\tlower")
    pass

def move_to(x, y):
    pass
