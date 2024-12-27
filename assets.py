from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import midpoint_line_circle as shapes
import config
import level_1 as l1
if config.level == 1:
    platforms = l1.platforms

def exitDoor(center_x, center_y):
    shapes.MidpointCircle(center_x, center_y, 20, [0,1,2,3])
    shapes.MidpointLine(center_x - 20, center_y, center_x - 20, center_y - 40)
    shapes.MidpointLine(center_x + 20, center_y, center_x + 20, center_y - 40)
    shapes.MidpointLine(center_x - 20, center_y - 40, center_x + 20, center_y - 40)
    
def normalPlatform(x1, y1, length, size = 10):
    shapes.MidpointLine(x1, y1, x1 + length, y1, size)

def wall(x1, y1, height = 20, width = 15, size = 5):
    shapes.MidpointLine(x1, y1, x1, y1 + height, size)
    shapes.MidpointLine(x1, y1 + height, x1 + width, y1 + height, size)
    shapes.MidpointLine(x1 + width, y1 + height, x1 + width, y1, size)
    shapes.MidpointLine(x1 + width, y1, x1, y1, size)
    
def cannon(center_x, center_y, radius = 8, size = 1, color = (1, 0.5, 0)):
    shapes.MidpointCircle(center_x, center_y, radius, [3,4], size, color)
    shapes.MidpointLine(center_x - 30, center_y - 30, center_x - 8, (center_y - 8), size, color)
    shapes.MidpointLine(center_x - 30, center_y + 30, center_x - 8, (center_y + 8), size, color)
    
def spike(x1, y1, size = 1):
    shapes.MidpointLine(x1, y1, x1 + 10, y1, size)
    shapes.MidpointLine(x1, y1, x1 + 5, y1 + 20, size)
    shapes.MidpointLine(x1 + 10, y1, x1 + 5, y1 + 20, size)
    
    shapes.MidpointLine(x1 + 10, y1, x1 + 20, y1, size)
    shapes.MidpointLine(x1 + 10, y1, x1 + 15, y1 + 20, size)
    shapes.MidpointLine(x1 + 20, y1, x1 + 15, y1 + 20, size)
    
    shapes.MidpointLine(x1 + 20, y1, x1 + 30, y1, size)
    shapes.MidpointLine(x1 + 20, y1, x1 + 25, y1 + 20, size)
    shapes.MidpointLine(x1 + 30, y1, x1 + 25, y1 + 20, size)
    
    shapes.MidpointLine(x1 + 30, y1, x1 + 40, y1, size)
    shapes.MidpointLine(x1 + 30, y1, x1 + 35, y1 + 20, size)
    shapes.MidpointLine(x1 + 40, y1, x1 + 35, y1 + 20, size)
    

def player(x, y, gun_side, size = 1, color = (1, 1, 1)):
    shapes.MidpointCircle(x, y, 8, [0,1,2,3,4,5,6,7], size, color) # head
    shapes.MidpointLine(x - 12, y - 12, x + 12, y - 12, size, color) # body top line
    shapes.MidpointLine(x - 12, y - 12, x, y - 30, size, color) # body left line
    shapes.MidpointLine(x + 12, y - 12, x, y - 30, size, color) # body right line
    shapes.MidpointCircle(x - 10, y - 35, 4, [0,1,2,3,4,5,6,7], size, color) # left leg
    shapes.MidpointCircle(x + 9, y - 35, 4, [0,1,2,3,4,5,6,7], size, color) # right leg
    
    # Draw the gun
    gun_x = x - 20 if gun_side == "left" else x + 20
    gun_y = y - 12
    shapes.MidpointCircle(gun_x, gun_y, 6)  # Gun is a small circle


def drawHeartPickup(x, y, size = 2, color = (1, 0.56, 0.63)):  # x, y are the coordinates of the top middle point of the heart
    shapes.MidpointCircle(x - 10, y, 10, [0,1,2,3], size, color)
    shapes.MidpointCircle(x + 10, y, 10, [0,1,2,3], size, color)
    shapes.MidpointLine(x + 20, y, x, y - 20, size, color)
    shapes.MidpointLine(x - 20, y, x, y - 20, size, color)


runnerEnemies = []
for i in platforms[ : len(platforms) - 1]:
    x, y, length, width, isBrittle, isMoving = i
    runnerEnemies.append((x, x + 10 , y + 50 , length, 5))

def runnerEnemy():

    for initx, x, y, _, _ in runnerEnemies: 
        shapes.MidpointCircle(x, y, 10) # head
        
        shapes.MidpointLine(x - 12, y + 6, x - 12, y - 6)
        shapes.MidpointLine(x - 18, y , x - 12, y + 6) # body top line
        shapes.MidpointLine(x - 18, y , x - 12, y - 6) # body top line

        shapes.MidpointCircle(x - 10, y - 35, 4) # left leg
        shapes.MidpointCircle(x + 9, y - 35, 4) # right leg

# runnerEnemy moves left to right


def moveRunnerEnemies(dt, isPaused):
    global runnerEnemies, enemyMove
    if not isPaused:
        for i in range(len(runnerEnemies)):
            initx, x, y, bound, move = runnerEnemies[i]
            

            if x <= initx:
                move = abs(move)  # move to the left
                # move to the right
            elif x+20 >= initx+bound:  # assuming the screen width is 800
                move = -abs(move)  # move to the left
            
            x += move * dt * 20
            
            runnerEnemies[i] = (initx, x, y, bound, move)





