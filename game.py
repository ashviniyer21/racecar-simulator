import pygame as pg
from car import Car

HORIZONTAL = pg.image.load("images/horizontal.png")
VERTICAL = pg.image.load("images/vertical.png")
TOP_LEFT = pg.image.load("images/topleft.png")
TOP_RIGHT = pg.image.load("images/topright.png")
BOTTOM_LEFT = pg.image.load("images/bottomleft.png")
BOTTOM_RIGHT = pg.image.load("images/bottomright.png")
FINISH_LINE = pg.image.load("images/finishline.png")

HORIZONTAL_MASK = pg.mask.from_surface(pg.image.load("images/horizontalmask.png"))
VERTICAL_MASK = pg.mask.from_surface(pg.image.load("images/verticalmask.png"))
TOP_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/topleftmask.png"))
TOP_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/toprightmask.png"))
BOTTOM_LEFT_MASK = pg.mask.from_surface(pg.image.load("images/bottomleftmask.png"))
BOTTOM_RIGHT_MASK = pg.mask.from_surface(pg.image.load("images/bottomrightmask.png"))

GRASS = pg.image.load("images/grass.png")
CAR = pg.transform.scale(pg.image.load("images/car.png"), (60, 48))

def get_next(pos, dir):
    new = [pos[0], pos[1]]
    if dir == 0:
        new[0] += 1
    elif dir == 90:
        new[1] -= 1
    elif dir == 180:
        new[0] -= 1
    else:
        new[1] += 1
    return new

start = [0, 2, 90] #Grid space, angle for starting driving

track = [
    [TOP_LEFT, HORIZONTAL, HORIZONTAL, TOP_RIGHT],
    [VERTICAL, GRASS, GRASS, VERTICAL],
    [BOTTOM_LEFT, HORIZONTAL, HORIZONTAL, BOTTOM_RIGHT]
    ]
track_mask = []

checkpoints = []

pos = start[0:2]
dir = start[2]

pos = get_next(pos, dir)
while pos[0] != start[0] or pos[1] != start[1]:
    checkpoints.append(pos)
    if track[pos[1]][pos[0]] == TOP_LEFT:
        if(dir == 90):
            dir = 0
        else:
            dir = 270
    if track[pos[1]][pos[0]] == TOP_RIGHT:
        if(dir == 90):
            dir = 180
        else:
            dir = 270
    if track[pos[1]][pos[0]] == BOTTOM_LEFT:
        if(dir == 270):
            dir = 0
        else:
            dir = 90
    if track[pos[1]][pos[0]] == BOTTOM_RIGHT:
        if(dir == 270):
            dir = 180
        else:
            dir = 90
    pos = get_next(pos, dir)

checkpoints.append(pos)
checkpoints.append(checkpoints[0])

print(checkpoints)

laps = 1
cp_counter = 0

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

WINDOW = pg.display.set_mode((IMAGE_WIDTH * len(track[0]), IMAGE_HEIGHT * len(track)), pg.RESIZABLE)
pg.display.set_caption("Racecar Simulator")

clock = pg.time.Clock()

FPS = 60

run = True

car = Car(5, 0.05, 3, (IMAGE_WIDTH / 4 + start[0] * IMAGE_WIDTH, IMAGE_HEIGHT / 4 + start[1] * IMAGE_HEIGHT, start[2]))

collision = False

finishlineloc = [0, 0]

finish1 = checkpoints[0]
finish2 = pos
if finish1[0] == finish2[0]:
    finishlineloc[0] = finish1[0] * IMAGE_WIDTH + 16
    finishlineloc[1] = max(finish1[1], finish2[1]) * IMAGE_HEIGHT - 8
else:
    finishlineloc[1] = finish1[0] * IMAGE_HEIGHT + 16
    finishlineloc[0] = max(finish1[0], finish2[0]) * IMAGE_HEIGHT - 8
    FINISH_LINE = pg.transform.rotate(FINISH_LINE, 90)

def check_collision(pose, rotated_car, new_rect):
    gridx = int(pose[0] // IMAGE_WIDTH)
    gridy = int(pose[1] // IMAGE_HEIGHT)
    car_mask = pg.mask.from_surface(rotated_car)
    for i in range(gridx, gridx + 2):
        for j in range(gridy, gridy + 2):
            if i == len(track[0]) or j == len(track) or track_mask[j][i] == None:
                continue
            offset = (new_rect.topleft[0] - i * IMAGE_WIDTH, new_rect.topleft[1] - j * IMAGE_HEIGHT)
            temp = track_mask[j][i].overlap(car_mask, offset)
            if temp != None:
                return temp
    return None

lin = 0
ang = 0

while run:


    clock.tick(FPS)

    car.update(lin, ang)

    pose = car.get_pose()


    rotated_car = pg.transform.rotate(CAR, pose[2])

    new_rect = rotated_car.get_rect(
        center=CAR.get_rect(topleft=pose[0:2]).center)


    pg.display.update()

    for event in pg.event.get():
        if event == pg.QUIT:
            run = False
            break

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

    collision = check_collision(pose, rotated_car, new_rect)


    # print(lin, ang)



    while collision != None:
        xshift = 0
        yshift = 0
        if(collision[0] < 20):
            xshift = 1
        elif(collision[0] > 100):
            xshift = -1
        if(collision[1] < 20):
            yshift = 1
        elif(collision[1] > 100):
            yshift = -1
        
        car.shift(xshift, yshift)

        pose = car.get_pose()


        rotated_car = pg.transform.rotate(CAR, pose[2])

        new_rect = rotated_car.get_rect(
            center=CAR.get_rect(topleft=pose[0:2]).center)
        
        collision = check_collision(pose, rotated_car, new_rect)

    center = WINDOW.get_rect().center

    offset = (-pose[0] + center[0], -pose[1] + center[1])

    gridx = int(pose[0] // IMAGE_WIDTH)
    gridy = int(pose[1] // IMAGE_HEIGHT)

    if checkpoints[cp_counter][0] == gridx and checkpoints[cp_counter][1] == gridy:
        cp_counter += 1
        if cp_counter == len(checkpoints):
            cp_counter = 0
            laps -= 1
            if laps == 0:
                print("You won!")
                break

    WINDOW.fill((0, 192, 0))

    for i in range(len(track)):
        for j in range(len(track[i])):
            WINDOW.blit(track[i][j], (j * IMAGE_WIDTH + offset[0], i * IMAGE_HEIGHT + offset[1]))

    WINDOW.blit(FINISH_LINE, (finishlineloc[0] + offset[0], finishlineloc[1] + offset[1]))
    
    WINDOW.blit(rotated_car, (new_rect.topleft[0] + offset[0], new_rect.topleft[1] + offset[1]))


pg.quit()
