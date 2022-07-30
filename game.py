import pygame as pg
from car import Car

HORIZONTAL = pg.image.load("images/horizontal.png")
VERTICAL = pg.image.load("images/vertical.png")
TOP_LEFT = pg.image.load("images/topleft.png")
TOP_RIGHT = pg.image.load("images/topright.png")
BOTTOM_LEFT = pg.image.load("images/bottomleft.png")
BOTTOM_RIGHT = pg.image.load("images/bottomright.png")

HORIZONTAL_MASK = pg.mask.from_surface(pg.image.load("images/horizontalmask.png"))
VERTICAL_MASK = pg.mask.from_surface(pg.image.load("images/verticalmask.png"))
TOP_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/topleftmask.png"))
TOP_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/toprightmask.png"))
BOTTOM_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/bottomleftmask.png"))
BOTTOM_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/bottomrightmask.png"))

GRASS = pg.image.load("images/grass.png")
CAR = pg.transform.scale(pg.image.load("images/car.png"), (60, 48))

track = [
    [TOP_LEFT, HORIZONTAL, HORIZONTAL, TOP_RIGHT],
    [VERTICAL, GRASS, GRASS, VERTICAL],
    [BOTTOM_LEFT, HORIZONTAL, HORIZONTAL, BOTTOM_RIGHT]
    ]
track_mask = []

for i in range(len(track)):
    row = []
    for j in range(len(track[i])):
        if track[i][j] == TOP_LEFT:
            row.append(TOP_LEFT_MASK)
        elif track[i][j] == TOP_RIGHT:
            row.append(TOP_RIGHT_MASK)
        elif track[i][j] == BOTTOM_LEFT:
            row.append(BOTTOM_LEFT_MASK)
        elif track[i][j] == BOTTOM_RIGHT:
            row.append(BOTTOM_RIGHT_MASK)
        elif track[i][j] == HORIZONTAL:
            row.append(HORIZONTAL_MASK)
        elif track[i][j] == VERTICAL:
            row.append(VERTICAL_MASK)
        else:
            row.append(None)
    track_mask.append(row)

IMAGE_WIDTH, IMAGE_HEIGHT = HORIZONTAL.get_width(), HORIZONTAL.get_height()

WINDOW = pg.display.set_mode((IMAGE_WIDTH * len(track[0]), IMAGE_HEIGHT * len(track)))
pg.display.set_caption("Racecar Simulator")

clock = pg.time.Clock()

FPS = 60

run = True

car = Car(5, 0.1, 10, (32, 32, 0))

collision = False

lin = 0
ang = 0

while run:

    clock.tick(FPS)

    for i in range(len(track)):
        for j in range(len(track[i])):
            WINDOW.blit(track[i][j], (j * IMAGE_WIDTH, i * IMAGE_HEIGHT))

    pose = car.get_pose()


    rotated_car = pg.transform.rotate(CAR, pose[2])

    new_rect = rotated_car.get_rect(
        center=CAR.get_rect(topleft=pose[0:2]).center)

    WINDOW.blit(rotated_car, new_rect.topleft)

    pg.display.update()

    for event in pg.event.get():
        if event == pg.QUIT:
            run = False
            break
    
    if not collision:

        keys = pg.key.get_pressed()

        lin = 0
        ang = 0

        if keys[pg.K_w]:
            lin += 1
        if keys[pg.K_s]:
            lin -= 1
        if keys[pg.K_a]:
            ang += 1
        if keys[pg.K_d]:
            ang -= 1


    collision = False

    gridx = int(pose[0] // IMAGE_WIDTH)
    gridy = int(pose[1] // IMAGE_HEIGHT)
    car_mask = pg.mask.from_surface(rotated_car)

    for i in range(gridx, gridx + 2):
        for j in range(gridy, gridy + 2):
            if gridx == len(track[0]) or gridy == len(track) or track_mask[gridy][gridx] == None:
                continue
            offset = (pose[0] - gridx * IMAGE_WIDTH, pose[1] - gridy * IMAGE_HEIGHT)
            temp = track_mask[gridy][gridx].overlap(car_mask, offset)
            if temp != None:
                collision = True

    print(lin, ang)

    car.update(lin, ang, collision)

pg.quit()