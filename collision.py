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


def platformCollision(player_x, player_y):
    # Define the player's bounding box
    
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for platform in assets.platforms:
        x1, y1, length, width, isBrittle, isMoving, hasEnemy = platform
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
   
    for i in range(len(assets.flyingEnemies)):
        initx, x, y, _ = assets.flyingEnemies[i]
        x1 , y1 = x - 22, y - 15
        x2 = x + 22
        y2 = y + 15

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
    
    for i in range(len(assets.tankEnemies)):
        initx, x, y, body_size, arm_size, length, move, health = assets.tankEnemies[i]
        x1, y1 = x - body_size, y - 30
        x2 = x + body_size
        y2 = y + 30
        
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
    for platform in assets.platforms:
        x1, y1, length, width, _, _, _ = platform
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
            

            return True, "runner", assets.runnerEnemies[i], 1
    
    for i in range(len(assets.flyingEnemies)):
        initx, x, y, _ = assets.flyingEnemies[i]
        x1 , y1 = x - 22, y - 15
        x2 = x + 22
        y2 = y + 15

        if x1 <= bullet_x <= x2 and y1 <= bullet_y <= y2:
            
        
            return True, "flying", assets.flyingEnemies[i], 1
    
    for i in range(len(assets.tankEnemies)):
        initx, x, y, body_size, arm_size, length, move, health = assets.tankEnemies[i]
        x1, y1 = x - body_size, y - 30
        x2 = x + body_size
        y2 = y + 30
        
        if x1 <= bullet_x <= x2 and y1 <= bullet_y <= y2:
            
            return True, "tank", assets.tankEnemies[i], 1
    

        
    return False, "none", -1, 0

