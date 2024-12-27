from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets
import config
import level_1 as l1


# global variables
player_x = -500  # Initial x-coordinate of the player's head
player_y = -540  # Initial y-coordinate of the player's head
isBreaking = False  # Flag to indicate if the brittle platform is breaking
if config.level == 1:
    platforms = l1.platforms  # List of platforms as tuples (x1, y1, length, width, isBrittle, isMoving)
    pickups = l1.pickups  # List of pickups as tuples (x, y, size, color)
    walls = l1.walls  # List of walls as tuples (x1, y1, height, width)
    spikes = l1.spikes  # List of spikes as tuples (x1, y1)
    muds = l1.muds  # List of muds as tuples (x1, y1)
    exitDoor = l1.exitDoor  # Tuple of exit door as (x, y)
    ceiling = l1.ceiling  # Tuple of ceiling as (x1, y1, x2, y2)


def platformCollision(player_x, player_y):
    # Define the player's bounding box
    global platforms
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for platform in platforms:
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


def wallCollision(player_x, player_y):
    # Define the player's bounding box
    global walls
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for wall in walls:
        x1, y1, length, width = wall
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


def ceilingCollision(player_x, player_y):
    global ceiling
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    x1, y1, _, _ = ceiling
    x2 = x1 + 1600
    y2 = y1 + 3

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


def spikeCollision(player_x, player_y):
    # Define the player's bounding box
    global spikes
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for spike in spikes:
        x1, y1 = spike
        x2 = x1 + 40
        y2 = y1 + 20

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


def mudCollision(player_x, player_y):
    global muds
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for mud in muds:
        x1, y1 = mud
        x2 = x1 + 40
        y2 = y1 + 10

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
    
    #flying enemies
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
    

    #tank enemies
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
    for platform in platforms:
        x1, y1, length, width, _, _, _ = platform
        x2 = x1 + length
        y2 = y1 + width

        # Check if bullet hits the platform
        if x1 <= bullet_x <= x2 and y1 <= bullet_y <= y2:
            return True
        
    return False


def fireballCollision(player_x, player_y, fireball_x, fireball_y):
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39
    
    if player_left <= fireball_x <= player_right and player_bottom <= fireball_y <= player_top:
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


def exitDoorCollision(player_x, player_y):
    # Define the player's bounding box
    global exitDoor
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    x1, y1 = exitDoor
    x1, y1 = x1 - 15, y1 - 35
    x2 = x1 + 15
    y2 = y1 + 55

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



def heartPickupCollision(player_x, player_y):
    # Define the player's bounding box
    global pickups
    player_left = player_x - 12
    player_right = player_x + 12
    player_top = player_y + 8
    player_bottom = player_y - 39 

    for pickup in pickups:
        x1, y1 = pickup
        x1, y1 = x1 - 20, y1 - 20
        x2 = x1 + 30
        y2 = y1 + 10

        # Check for collisions with the top edge
        if (player_bottom <= y1 <= player_top and
                player_right > x1 and player_left < x2):
            return True, pickups.index(pickup)

        # Check for collisions with the bottom edge
        if (player_bottom <= y2 <= player_top and
                player_right > x1 and player_left < x2):
            return True, pickups.index(pickup)

        # Check for collisions with the left edge
        if (player_left <= x1 <= player_right and
                player_bottom < y2 and player_top > y1):
            return True, pickups.index(pickup)

        # Check for collisions with the right edge
        if (player_left <= x2 <= player_right and
                player_bottom < y2 and player_top > y1):
            return True, pickups.index(pickup)
    
    return False, None






# #atik

# def movingPlatformCollision(player_x, player_y, moving_platforms):
#     """
#     Detects if the player is colliding with any moving platform.

#     Parameters:
#     - player_x: float - The player's x-coordinate.
#     - player_y: float - The player's y-coordinate.
#     - moving_platforms: list - List of moving platforms with their attributes.

#     Returns:
#     - dict or None: Returns the collided platform's data if collision occurs, otherwise None.
#     """
#     player_left = player_x - 12
#     player_right = player_x + 12
#     player_top = player_y + 8
#     player_bottom = player_y - 39

#     for platform in moving_platforms:
#         platform_x = platform['x']
#         platform_y = platform['y']
#         platform_length = platform['length']

#         # Adjust height alignment
#         platform_top = platform_y + 10  # Top surface of the platform
#         if (
#             platform_x <= player_x <= platform_x + platform_length  # Horizontal collision
#             and player_bottom <= platform_top <= player_top         # Vertical collision
#         ):
#             return platform  # Return the platform data

#     return None  # No collision detected