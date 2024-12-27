from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import midpoint_line_circle as shapes
import collision
import random, math


isBreaking = False  # Flag to indicate if the brittle platform is breaking
platforms = [
    (-800, 700, 800, 700, 2, False, False, False),
    (-790, -200, 300, 5, False, False, False),
    (150, 50, 500, 5, True, False, False),
    (80, 225, 300, 5, False, False, False),
    (150, -280, 400, 5, False, False, False),
    (-150, 350, 700, 5, False, False, False),
]  # List of platforms as tuples (x1, y1, length, width, isBrittle, isMoving, hasEnemy)


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
for i in platforms:
    if random.choice(["do", "continue"]) == "continue":
        continue

    x, y, length, width, isBrittle, isMoving, hasEnemy = i

    if not hasEnemy and length <= 400:
        runnerEnemies.append((x, x + 10 , y + 50 , length, 5))
        platforms[platforms.index(i)] = (x, y, length, width, isBrittle, isMoving, True)

def runnerEnemy():

    for initx, x, y, _, move in runnerEnemies:
        shapes.MidpointCircle(x, y, 10) # head
        if move < 0:
            shapes.MidpointLine(x - 12, y + 6, x - 12, y - 6)
            shapes.MidpointLine(x - 18, y , x - 12, y + 6) # body top line
            shapes.MidpointLine(x - 18, y , x - 12, y - 6) # body top line
        else:
            shapes.MidpointLine(x + 12, y + 6, x + 12, y - 6)
            shapes.MidpointLine(x + 18, y , x + 12, y + 6) # body top line
            shapes.MidpointLine(x + 18, y , x + 12, y - 6) # body top line

        shapes.MidpointCircle(x - 10, y - 35, 4) # left leg
        shapes.MidpointCircle(x + 9, y - 35, 4) # right leg

# runnerEnemy moves left to right


def moveRunnerEnemies(dt):
    global runnerEnemies
    for i in range(len(runnerEnemies)):
        initx, x, y, bound, move = runnerEnemies[i]
        

        if x <= initx:
            move = -1 * move  # move to the left
               # move to the right
        elif x+20 >= initx+bound:  # assuming the screen width is 800
            move = -1 * move  # move to the left
        
        x += move * dt * 20
        
        runnerEnemies[i] = (initx, x, y, bound, move)



flyingEnemies = []
for i in range(random.randint(2, 6)):
    x = random.randint(-760, 760)
    y = random.randint(-300, 600)
    move = random.choice([-1, 1])

    flyingEnemies.append((x, x, y, move))
def flyingEnemy():
    for initx, x, y, _ in flyingEnemies:
        shapes.MidpointCircle(x, y, 12) # body
        shapes.MidpointLine(x - 15, y + 5, x - 15, y - 5) # left wing
        shapes.MidpointLine(x + 15, y + 5, x + 15, y - 5) # right wing
        shapes.MidpointCircle(x - 20, y, 4) # left propeller
        shapes.MidpointCircle(x + 20, y, 4) # right propeller
        shapes.MidpointLine(x - 20, y - 5, x - 20, y + 5) # left propeller axis
        shapes.MidpointLine(x + 20, y - 5, x + 20, y + 5) # right propeller axis

def moveFlyingEnemies(dt):
    global flyingEnemies

    for i in range(len(flyingEnemies)):
        initx, x, y, move = flyingEnemies[i]
        if x-20 <= -740:
            move = -1 * move
        elif x+20 >= 740:
            move = -1 * move
        x += move * dt * 250

        flyingEnemies[i] = (initx, x, y, move)


tankEnemies = []
for i in range(random.randint(2, 3)):

    temp = random.choice(platforms)
    x, y, length, width, isBrittle, isMoving, hasEnemy = temp
    if not hasEnemy and length > 400:
        bodysize = 40
        armSize = 50
        health = 5
        move = 4
        tankEnemies.append((x, x +bodysize + armSize , y + 60, bodysize, armSize, length, move, health))
        platforms[platforms.index(temp)] = (x, y, length, width, isBrittle, isMoving, True)
def tankEnemy():

    for initx, x, y, body_size, arm_size, _, move, _ in tankEnemies:
          # You can adjust these values to position the enemy
        
        
        # Draw the body
        shapes.MidpointCircle(x, y, body_size)

        # Draw the left arm
        if move > 0:
            
            shapes.MidpointLine(x - 5, y, x + arm_size//2, y-30)
            shapes.MidpointLine(x + arm_size//2, y-30, x + arm_size, y-30)
            shapes.MidpointCircle(x + arm_size, y-30, 15)

            # Draw the right arm
            shapes.MidpointLine(x + body_size, y, x + body_size + arm_size, y)
            shapes.MidpointCircle(x + body_size + arm_size, y, 15)
        elif move < 0:
            
            shapes.MidpointLine(x - 5, y, x - arm_size//2, y-30)
            shapes.MidpointLine(x - arm_size//2, y-30, x - arm_size, y-30)
            shapes.MidpointCircle(x - arm_size, y-30, 15)

            # Draw the right arm
            shapes.MidpointLine(x - body_size, y, x - body_size - arm_size, y)
            shapes.MidpointCircle(x - body_size - arm_size, y, 15)


def moveTankEnemies(dt):
    global tankEnemies

    for i in range(len(tankEnemies)):
        initx, x, y, body_size, arm_size, length, move, health = tankEnemies[i]
        if x - body_size  <= initx:
            move = -1 * move
        elif x + body_size + arm_size + 20 >= initx + length:
            move = -1 * move
        x += move * dt * 30

        tankEnemies[i] = (initx, x, y, body_size, arm_size, length, move, health)



# def rotateTankEnemy(angle):
#     # Define the position and size of the tank
#     x, y = 0, -200  # You can adjust these values to position the tank
#     body_size = 50
#     turret_size = 
# 20
#     cannon_size = 30

#     # Calculate the new positions of the tank's parts based on the rotation angle
#     turret_x = x + math.cos(math.radians(angle)) * turret_size
#     turret_y = y + math.sin(math.radians(angle)) * turret_size
#     cannon_x = turret_x + math.cos(math.radians(angle)) * cannon_size
#     cannon_y = turret_y + math.sin(math.radians(angle)) * cannon_size

#     # Draw the tank's body
#     shapes.MidpointCircle(x, y, body_size)

#     # Draw the turret
#     shapes.MidpointCircle(turret_x, turret_y, 10)

#     # Draw the cannon
#     shapes.MidpointLine(turret_x, turret_y, cannon_x, cannon_y)
#     shapes.MidpointCircle(cannon_x, cannon_y, 5)

def drawHealth_Score(x, y, health, score):
    space = 0
    for i in range(health):
        shapes.MidpointCircle(x-10 + space, y, 8, [0, 1, 2, 3], 2, [1, 0, 0])
        shapes.MidpointCircle(x+10 + space, y, 8, [0, 1, 2, 3], 2, [1, 0, 0])
        shapes.MidpointLine(x-18 + space, y-2, x + space, y-25, 2, [1, 0, 0])
        shapes.MidpointLine(x+18 + space, y-2, x + space, y-25, 2, [1, 0, 0])
        
        space += 50

    

    glColor3f(1, 1, 0)
    glRasterPos2f(600, 730)
    for char in "SCORE: " + str(score):
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))