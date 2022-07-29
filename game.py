import pygame as pg
from car import Car

HORIZONTAL = pg.image.load("images/horizontal.png")
VERTICAL = pg.image.load("images/vertical.png")
TOP_LEFT = pg.image.load("images/topleft.png")
TOP_RIGHT = pg.image.load("images/topright.png")
BOTTOM_LEFT = pg.image.load("images/bottomleft.png")
BOTTOM_RIGHT = pg.image.load("images/bottomright.png")
GRASS = pg.image.load("images/grass.png")
CAR = pg.image.load("images/car.png")

track = [
    [TOP_LEFT, HORIZONTAL, HORIZONTAL, TOP_RIGHT],
    [VERTICAL, GRASS, GRASS, VERTICAL],
    [BOTTOM_LEFT, HORIZONTAL, HORIZONTAL, BOTTOM_RIGHT]
    ]
track_mask = []

IMAGE_WIDTH, IMAGE_HEIGHT = HORIZONTAL.get_width(), HORIZONTAL.get_height()

WINDOW = pg.display.set_mode((IMAGE_WIDTH * len(track[0]), IMAGE_HEIGHT * len(track)))
pg.display.set_caption("Racecar Simulator")

clock = pg.time.Clock()

FPS = 60

run = True

car = Car(3, 0.05, 3, (32, 32, 0))


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
    
    keys = pg.key.get_pressed()

    lin = 0
    ang = 0

    if keys[pg.K_w]:
        lin -= 1
    if keys[pg.K_s]:
        lin += 1
    if keys[pg.K_a]:
        ang -= 1
    if keys[pg.K_d]:
        ang += 1

    print(lin, ang)
    
    car.update(lin, ang)

pg.quit()