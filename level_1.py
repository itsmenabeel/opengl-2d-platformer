from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets

platforms = [
    (-790, -280, 300, 5, False, False, False),  # bot 1
    (150, 50, 320, 5, False, False, False),  # mid 1
    (-300, 135, 230, 5, False, False, False),  # mid 3 (no enemy)
    (-550, 325, 200, 5, False, False, False),  # mid 5
    (-450, -80, 80, 5, False, False, False),  # mid 4
    (550, -240, 100, 5, False, False, False),  # bot 3
    (660, -100, 70, 5, False, False, False),  # bot 4 (no enemy)
    (120, 225, 265, 5, False, False, False),  #mid 2
    (90, -280, 250, 5, False, False, False),  # bot 2
    (-300, 480, 200, 5, False, False, False),  # Door
]  # List of platforms as tuples (x1, y1, length, width, isBrittle, isMoving, hasEnemy)
pickups = [
    (600, -550)
]  # List of pickups as tuples (x, y, size, color)
walls = [
    (-200, -600, 50, 180),
    (-300, -600, 50, 120),
    (-100, 135, 30, 80)
]  # List of walls as tuples (x1, y1, height, width)
spikes = [
    (-245, -600),  # 40 pixel across
    (60, -600),
    (20, -600),
    (430, 55),
    (-300, 135)
]  # List of spikes as tuples (x1, y1)
cannons = [
    (-770, 530),
    (770, 100)
]
muds = [
    (500, -600),  # 30 pixel across
    (540, -600),
    (450, -600),
    (120, 225),
    (-520, -280)
]
exitDoor = (-200, 530)
ground = (-800, -600, 800, -600)
ceiling = (-800, 700, 800, 700)

def drawPlatforms_l1():
    for platform in platforms:
        x1, y1, length, width, isBrittle, isMoving, hasEnemy = platform
        assets.normalPlatform(x1, y1, length, width)

def drawPickups_l1():
    for pickup in pickups:
        x, y = pickup
        assets.drawHeartPickup(x, y)
        
def drawWalls_l1():
    for wall in walls:
        x1, y1, width, height = wall
        assets.wall(x1, y1, height, width)
        
def drawSpikes_l1():
    for spike in spikes:
        x1, y1 = spike
        assets.spike(x1, y1)
        
def drawCannons_l1():
    for cannon in cannons:
        x, y = cannon
        assets.cannon(x, y)
        
def drawMud_l1():
    for mud in muds:
        x, y = mud
        assets.mud(x, y)
        
def drawExitDoor_l1():
    x, y = exitDoor
    assets.exitDoor(x, y)

def drawGround_l1():
    x1, y1, x2, y2 = ground
    shapes.MidpointLine(x1, y1, x2, y2)
    
def drawCeiling_l1():
    x1, y1, x2, y2 = ceiling
    shapes.MidpointLine(x1, y1, x2, y2)


def drawEnemy_l1():
    assets.runnerEnemy()
    assets.flyingEnemy()
    assets.tankEnemy()
    