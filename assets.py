from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import midpoint_line_circle as shapes
import collision

def exitDoor(center_x, center_y):
    shapes.MidpointCircle(center_x, center_y, 20, [0,1,2,3])
    shapes.MidpointLine(center_x - 20, center_y, center_x - 20, center_y - 40)
    shapes.MidpointLine(center_x + 20, center_y, center_x + 20, center_y - 40)
    shapes.MidpointLine(center_x - 20, center_y - 40, center_x + 20, center_y - 40)
    
def normalPlatform(x1, y1, length, size = 10):
    shapes.MidpointLine(x1, y1, x1 + length, y1, size)

def brittlePlatform(x1, y1, length, size = 10, isBreaking = False):
    if isBreaking:
        shapes.MidpointLine(x1, y1, x1 + length, y1, size, (1, 1, 1))
    shapes.MidpointLine(x1, y1, x1 + length, y1, size, (0.77, 0.65, 0.52))

def player(x, y, gun_side):
    shapes.MidpointCircle(x, y, 8) # head
    shapes.MidpointLine(x - 12, y - 12, x + 12, y - 12) # body top line
    shapes.MidpointLine(x - 12, y - 12, x, y - 30) # body left line
    shapes.MidpointLine(x + 12, y - 12, x, y - 30) # body right line
    shapes.MidpointCircle(x - 10, y - 35, 4) # left leg
    shapes.MidpointCircle(x + 9, y - 35, 4) # right leg
    
    # Draw the gun
    gun_x = x - 20 if gun_side == "left" else x + 20
    gun_y = y - 12
    shapes.MidpointCircle(gun_x, gun_y, 6)  # Gun is a small circle




runnerEnemies = []
for i in collision.platforms:
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


def moveRunnerEnemies(dt):
    global runnerEnemies, enemyMove
    for i in range(len(runnerEnemies)):
        initx, x, y, bound, move = runnerEnemies[i]
        

        if x <= initx:
            move = -1 * move  # move to the left
               # move to the right
        elif x+20 >= initx+bound:  # assuming the screen width is 800
            move = -1 * move  # move to the left
        
        x += move * dt * 20
        
        runnerEnemies[i] = (initx, x, y, bound, move)
