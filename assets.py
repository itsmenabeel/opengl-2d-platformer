from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import midpoint_line_circle as shapes
import config
import level_1 as l1
import random, math

if config.level == 1:
    platforms = config.platform1

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

def mud(x1, y1, size = 8):
    shapes.MidpointCircle(x1 + 10, y1, 10, [0,1,2,3], size, (0.77, 0.64, 0.52))
    shapes.MidpointCircle(x1 + 20, y1, 10, [0,1,2,3], size, (0.5, 0.3, 0))
    shapes.MidpointCircle(x1 + 30, y1, 10, [0,1,2,3], size, (0.5, 0.3, 0))    

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
for i in platforms:
    if random.choice(["do", "continue"]) == "continue":
        continue
    print(i)
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

def moveFlyingEnemies(dt, isPaused):
    global flyingEnemies
    if not isPaused:
        for i in range(len(flyingEnemies)):
            initx, x, y, move = flyingEnemies[i]
            if x-20 <= -740:
                move = -1 * move
            elif x+20 >= 740:
                move = -1 * move
            x += move * dt * 250
            x = int(x)
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


def moveTankEnemies(dt, isPaused):
    global tankEnemies
    if not isPaused:
        for i in range(len(tankEnemies)):
            initx, x, y, body_size, arm_size, length, move, health = tankEnemies[i]
            if x - body_size  <= initx:
                move = -1 * move
            elif x + body_size + arm_size + 20 >= initx + length:
                move = -1 * move
            x += move * dt * 30
            x = int(x)
            tankEnemies[i] = (initx, x, y, body_size, arm_size, length, move, health)



def drawHealth_Score(health, score):
    x, y = -750, 750

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







#Atik 


movingPlatforms = []

def initializeMovingPlatforms(platform_list):
    """Initialize moving platforms from a list of tuples."""
    global movingPlatforms
    for platform in platform_list:
        x, y, length, width, isBrittle, isMoving = platform
        if isMoving:  # Only include moving platforms
            movingPlatforms.append({
                'init_x': x,       # Initial x-coordinate
                'x': x,            # Current x-coordinate
                'y': y,            # Current y-coordinate
                'length': length,  # Platform length
                'width': width,    # Platform width
                'bound': 500,      # Example movement boundary
                'speed': 2         # Example movement speed
            })

def movePlatforms(dt):
    """Update the positions of moving platforms."""
    global movingPlatforms
    for platform in movingPlatforms:
        init_x, x, y, length, bound, speed = (
            platform['init_x'],
            platform['x'],
            platform['y'],
            platform['length'],
            platform['bound'],
            platform['speed'],
        )

        # Reverse direction at the boundaries
        if x <= init_x:
            speed = abs(speed)  # Move to the right
        elif x + length >= init_x + bound:
            speed = -abs(speed)  # Move to the left

        # Update position
        x += speed * dt
        platform['x'] = x
        platform['speed'] = speed
        
def drawMovingPlatforms():
    """Draw all moving platforms."""
    global movingPlatforms
    for platform in movingPlatforms:
        x, y, length = platform['x'], platform['y'], platform['length']
        shapes.MidpointLine(x, y, x + length, y, 10, (0.2, 0.8, 0.8))  # Light blue for moving platforms