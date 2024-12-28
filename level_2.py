from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets



platforms = [
    
    (500, -200, 300, 5, False, False, False), # right first
    (-350, -300, 700, 5, False, False, False), #big firs tank1
    (-790, -130, 450, 5, False, False, False), #left big tank2
    (-250, 40, 200, 5, False, False, False), #left mid 4 
    (20, -10, 100, 5, False, False, False), 
    (-500, 120, 180, 5, False, False, False),
    (180, -60, 250, 5, False, False, False), 

    (-400, 420, 500, 5, False, False, False), #tank3



    (40, 225, 300, 5, False, False, False),


    (220, 500, 180, 5, False, False, False), #door


    
]

pickups = [
    # (-475, 330)
]  # List of pickups as tuples (x, y, size, color)
walls = [
    (500, -600, 50, 180),
    (400, -600, 50, 90),

    (-420, -600, 50, 160),
    (-480, -600, 50, 80),

    (-500, 120, 50, 160),
    (-450, 120, 50, 80),
]  # List of walls as tuples (x1, y1, height, width)
spikes = [
    (-350, -300),
    (-310, -300),

    (455, -600),  # 40 pixel across
    (60, -600),
    (20, -600),

    (80, 225),
    (120, 225),
    (240, 225),
    (280, 225),

    (-200, 40),
    (-160, 40),
]  # List of spikes as tuples (x1, y1)
cannons = [
    (-770, 550),
    (770, 300),
    # (790, -50)
]
muds = [
    (20, -600),
    (60, -600),


    (-140, -300),
    (-100, -300),
    (-60, -300),
    (-20, -300),

    (-480, -130),
    (-440, -130),
]
exitDoor = (300, 550)
ground = (-800, -600, 800, -600)
ceiling = (-800, 700, 800, 700)


# runnerEnemies = []

# for i in platforms[ : len(platforms) -1]:
#     if platforms.index(i) in [2, 4, 5]:
#         continue
#     x, y, length, width, isBrittle, isMoving, hasEnemy = i

#     if not hasEnemy and length <= 400:
#         runnerEnemies.append((x, x + 10 , y + 50 , length, 5))
#         platforms[platforms.index(i)] = (x, y, length, width, isBrittle, isMoving, True)


# tankEnemies = []
# for i in range(random.randint(2, 3)):

#     for platform in platforms:
#         x, y, length, width, isBrittle, isMoving, hasEnemy = platform
#         if not hasEnemy and length > 400:
#             bodysize = 40
#             armSize = 50
#             health = 5
#             move = 4
#             tankEnemies.append((x, x +bodysize + armSize , y + 60, bodysize, armSize, length, move, health))
#             platforms[platforms.index(platform)] = (x, y, length, width, isBrittle, isMoving, True)



# def drawBrittlePlatforms_l2():
#     for platform in platforms:
#         x1, y1, length, width, isBrittle, isMoving, hasEnemy = platform
#         if isBrittle:
#             assets.normalPlatform(x1, y1, length, 5)

def drawPlatforms_l2():
    for platform in platforms:
        x1, y1, length, width, isBrittle, isMoving, hasEnemy = platform
        assets.normalPlatform(x1, y1, length, width)

def drawPickups_l2():
    for pickup in pickups:
        x, y = pickup
        assets.drawHeartPickup(x, y)
        
def drawWalls_l2():
    for wall in walls:
        x1, y1, width, height = wall
        assets.wall(x1, y1, height, width)
        
def drawSpikes_l2():
    for spike in spikes:
        x1, y1 = spike
        assets.spike(x1, y1)
        
def drawCannons_l2():
    for cannon in cannons:
        x, y = cannon
        assets.cannon(x, y)
        
def drawMud_l2():
    for mud in muds:
        x, y = mud
        assets.mud(x, y)
        
def drawExitDoor_l2():
    x, y = exitDoor
    assets.exitDoor(x, y)

def drawGround_l2():
    x1, y1, x2, y2 = ground
    shapes.MidpointLine(x1, y1, x2, y2)

def drawCeiling_l2():
    x1, y1, x2, y2 = ceiling
    shapes.MidpointLine(x1, y1, x2, y2)


def drawEnemy_l2():
    assets.runnerEnemy()
    
    assets.tankEnemy()