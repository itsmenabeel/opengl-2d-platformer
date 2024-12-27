from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets

platforms = [
    (-790, -200, 300, 5, False, False),
    (150, 50, 400, 5, True, False),
    (80, 225, 300, 5, False, False),
    (150, -280, 250, 5, False, False),
    (-300, 450, 200, 5, False, False),
]  # List of platforms as tuples (x1, y1, length, width, isBrittle, isMoving)
pickups = [
    (500, 500)
]  # List of pickups as tuples (x, y, size, color)
walls = [
    (-200, -600, 50, 100),
    (-300, -600, 50, 120)
]  # List of walls as tuples (x1, y1, height, width)
spikes = [
    (-245, -600)
]  # List of spikes as tuples (x1, y1)
cannons = [
    (-770, 500)
]

def drawPlatforms_l1():
    for platform in platforms:
        x1, y1, length, width, isBrittle, isMoving = platform
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