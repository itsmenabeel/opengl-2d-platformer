from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets


# global variables
player_x = -500  # Initial x-coordinate of the player's head
player_y = -540  # Initial y-coordinate of the player's head
isBreaking = False  # Flag to indicate if the brittle platform is breaking
platforms = [
    (-790, -200, 300, 5, False, False),
    (150, 50, 400, 5, True, False),
    (80, 225, 300, 5, False, False),
    (150, -280, 250, 5, False, False),
]  # List of platforms as tuples (x1, y1, length, width, isBrittle, isMoving)


def platformCollision(player_x, player_y):
    # Define the player's bounding box
    global platforms
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for platform in platforms:
        x1, y1, length, width, isBrittle, isMoving = platform
        x2 = x1 + length
        y2 = y1 + width

        # Check for collisions with the top edge
        if (player_bottom <= y1 <= player_top and
                player_right > x1 and player_left < x2):
            return True

        # Check for collisions with the bottom edge
        if (player_bottom <= y2 <= player_top and
                player_right > x1 and player_left < x2):
            return True

        # Check for collisions with the left edge
        if (player_left <= x1 <= player_right and
                player_bottom < y2 and player_top > y1):
            return True

        # Check for collisions with the right edge
        if (player_left <= x2 <= player_right and
                player_bottom < y2 and player_top > y1):
            return True
    
    
    
    return False

def enemyCollision(player_x, player_y):
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for i in range(len(assets.runnerEnemies)):
        initx, x, y, _, _ = assets.runnerEnemies[i]
        x1 , y1 = x - 20, y - 40
        x2 = x + 15
        y2 = y + 10

        # Check for collisions with the top edge
        if (player_bottom <= y1 <= player_top and
                player_right > x1 and player_left < x2):
            
            return True

        # Check for collisions with the bottom edge
        if (player_bottom <= y2 <= player_top and
                player_right > x1 and player_left < x2):
            
            return True

        # Check for collisions with the left edge
        if (player_left <= x1 <= player_right and
                player_bottom < y2 and player_top > y1):
            
            return True

        # Check for collisions with the right edge
        if (player_left <= x2 <= player_right and
                player_bottom < y2 and player_top > y1):
            
            return True

    return False


def bulletCollision(bullet_x, bullet_y):
    for platform in platforms:
        x1, y1, length, width, _, _ = platform
        x2 = x1 + length
        y2 = y1 + width

        # Check if bullet hits the platform
        if x1 <= bullet_x <= x2 and y1 <= bullet_y <= y2:
            return True
        
    return False


def enemyBulletCollision(bullet_x, bullet_y):

    for i in range(len(assets.runnerEnemies)):
        initx, x, y, _, _ = assets.runnerEnemies[i]
        x1 , y1 = x - 20, y - 40
        x2 = x + 15
        y2 = y + 10

        # Check if bullet hits the platform
        if x1 <= bullet_x <= x2 and y1 <= bullet_y <= y2:
            assets.runnerEnemies.remove(assets.runnerEnemies[i])
        
            return True

    return False






#atik
