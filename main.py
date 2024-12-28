from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets
import collision
import config, end
import level_1 as l1
import level_2 as l2

import menu  # Import the menu module
from menu import diff_health

# global variables
player_x = -500  # Initial x-coordinate of the player's head
player_y = -540  # Initial y-coordinate of the player's head
gravity = -500  # Acceleration due to gravity
player_speed = 300  # Speed of the player
player_health = 0  # Initialize player health with diff_health
player_score = 0
player_immune = False  # Flag to indicate if the player is immune to damage
last_hit_time = 0  # Timestamp of the last time the player was hit
hit_flash_duration = 0.2  # Duration for which the player flashes red when hit
isPaused = False  # Flag to indicate if the game is paused
isGameOver = False  # Flag to indicate if the game is over

velocity_y = 0  # Initial vertical velocity of the player
isJumping = False  # Flag to indicate if the player is jumping
jump_strength = 500  # Strength of the jump
move_left, move_right = False, False  # Flags to indicate if the player is moving left or right
isBreaking = False  # Flag to indicate if the brittle platform is breaking
last_time = time.time()  # Time variable to calculate delta time
gun_side = "right"  # Direction of the gun, can be 'left' or 'right'
bullet_speed = 500  # Speed of the bullet
bullet_size = 8  # Size of the bullet
last_bullet_time = 0  # Timestamp of the last fired bullet
last_fireball_time = 0  # Timestamp of the last fired fireball
bullet_cooldown = 0.8  # Cooldown period in seconds
fireball_cooldown = 2  # Cooldown period in seconds
bullets = []  # List to store active bullets as tuples (x, y, direction)
fireballs = []  # List to store active fireballs as tuples (x, y, direction)

if config.level == 1:
    platforms = l1.platforms  # List of platforms as tuples (x1, y1, length, width)
    pickups = l1.pickups  # List of pickups as tuples (x, y)
    walls = l1.walls  # List of walls as tuples (x1, y1, height, width)
    spikes = l1.spikes  # List of spikes as tuples (x1, y1)
    cannons = l1.cannons  # List of cannons as tuples (x, y)
    muds = l1.muds  # List of mud as tuples (x, y)
elif config.level == 2:
    platforms = l2.platforms  # List of platforms as tuples (x1, y1, length, width)
    pickups = l2.pickups  # List of pickups as tuples (x, y)
    walls = l2.walls  # List of walls as tuples (x1, y1, height, width)
    spikes = l2.spikes  # List of spikes as tuples (x1, y1)
    cannons = l2.cannons  # List of cannons as tuples (x, y)
    muds = l2.muds  # List of mud as tuples (x, y)
cannon_last_fireball_time = [0] * len(cannons)  # List to store the last fireball time for each cannon


def updatePlayer(delta_time):
    global player_x, player_y, player_health, gravity, velocity_y, isJumping, move_left, move_right, fireballs, hit_flash_duration
    global last_hit_time, isGameOver, invincible_time, blink_interval, last_blink_time, player_immune, inMud

    #mud collision
    inMud = collision.mudCollision(player_x, player_y)
    if not inMud:
        velocity_y += gravity * 2 * delta_time
        new_y = player_y + int(velocity_y * 2 * delta_time)
    else:
        velocity_y += (gravity * delta_time) / 2
        new_y = player_y + int((velocity_y * delta_time) / 2)

    # Detect collisions
    if collision.platformCollision(player_x, new_y) or collision.wallCollision(player_x, new_y) or collision.ceilingCollision(player_x, new_y):
        velocity_y = 0
        isJumping = False
    else:
        player_y = new_y
    
    # Check for collision with enemies or hazards
    enemyHit = collision.enemyCollision(player_x - player_speed * delta_time, player_y)
    spikeHit = collision.spikeCollision(player_x - player_speed * delta_time, player_y)
    fireballHit = False
    for fireball in fireballs:
        x, y, _ = fireball
        fireballHit = collision.fireballCollision(player_x - player_speed * delta_time, player_y, x, y)
    if enemyHit or spikeHit or fireballHit:

        cur_time = time.time()
        if cur_time - last_hit_time > 2:
            player_health -= 1
            player_immune = True
            print("Player Health: ", player_health)
            last_hit_time = cur_time
            if player_health == 0:
                isGameOver = True
        else:
            player_immune = False
                           
    # Check for collision with pickups
    collided_heart, index = collision.heartPickupCollision(player_x, player_y)
    if collided_heart:
        player_health += 1
        print("Player Health: ", player_health)
        if index is not None:
            pickups.remove(pickups[index])
    
    # Change horizontal position
    if move_left:
        horz_collision_plat = collision.platformCollision(player_x - player_speed * delta_time, player_y)
        horz_collision_wall = collision.wallCollision(player_x - player_speed * delta_time, player_y)
        if not horz_collision_plat and not horz_collision_wall:
            if not inMud:
                player_x -= player_speed * delta_time if player_x - 12 > -800 else 0
            else:
                player_x -= (player_speed / 2) * delta_time if player_x - 12 > -800 else 0 
    if move_right:
        horz_collision_plat = collision.platformCollision(player_x + player_speed * delta_time, player_y)
        horz_collision_wall = collision.wallCollision(player_x + player_speed * delta_time, player_y)
        if not horz_collision_plat and not horz_collision_wall:
            if not inMud:
                player_x += player_speed * delta_time if player_x + 12 < 800 else 0
            else:
                player_x += (player_speed / 2) * delta_time if player_x + 12 < 800 else 0
    

    # Keep player within screen bounds
    if player_y < -557:
        player_y = -557
        velocity_y = 0
        isJumping = False
        
    # Reset player color after hit flash duration
    if player_immune and (time.time() - last_hit_time > hit_flash_duration):
        player_immune = False
        
    if collision.exitDoorCollision(player_x, player_y):
        if config.level == 1:
            config.level += 1
            player_x, player_y = -540, -540
            glFlush()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            print("level: ", config.level)
        elif config.level == 2:
            config.level = 1
            end.show_end_screen(player_score, "CONGRATS!")
      
        
def updateBullets(delta_time):
    global bullets, player_score
    new_bullets = []
    
    for bullet in bullets:
        x, y, direction = bullet
        x += bullet_speed * delta_time if direction == "right" else -bullet_speed * delta_time  # Move the bullet
        # Check for collision with platforms and enemies

        enemyCollision, enemy, i, hit = collision.enemyBulletCollision(x, y)

        if not collision.bulletCollision(x, y) and not enemyCollision:
            if not collision.wallCollision(x, y):
                new_bullets.append((x, y, direction))

        if enemyCollision:
            player_score += 1
            
            if enemy == "runner":
                print(assets.runnerEnemies)
                print(i)
                assets.runnerEnemies.remove(i)

            elif enemy == "flying":
                print(assets.flyingEnemies)
                assets.flyingEnemies.remove(i)
            
            elif enemy == "tank":
                initx, x, y, body_size, arm_size, length, move, health = i
                if health > 0:
                    health -= hit
                    assets.tankEnemies[assets.tankEnemies.index(i)] = (initx, x, y, body_size, arm_size, length, move, health)
                elif health == 0:
                    assets.tankEnemies.remove(i)
        

    bullets = new_bullets
   
   

def shootFireball():
    global cannons, fireballs, last_fireball_time, fireball_cooldown, cannon_last_fireball_time
    current_time = time.time()
    for i, cannon in enumerate(cannons):
        x, y = cannon
        if current_time - cannon_last_fireball_time[i] >= fireball_cooldown:
            # Add a new fireball at the cannon's tip
            fireball_x = x
            fireball_y = y
            if x < 0:
                fireballs.append((fireball_x, fireball_y, "right"))
            elif x > 0:
                fireballs.append((fireball_x, fireball_y, "left"))
            cannon_last_fireball_time[i] = current_time
        


def updateFireballs(delta_time):
    global fireballs, bullet_speed, player_x, player_y
    new_fireballs = []
    
    for fireball in fireballs:
        x, y, direction = fireball
        if direction == "right":
            x += bullet_speed * delta_time if x < 800 else 0
        else:
            x += -bullet_speed * delta_time if x > -800 else 0
        # Check for collision with platforms and enemies
        if not collision.bulletCollision(x, y):
            if not collision.wallCollision(x, y):
                if not collision.fireballCollision(player_x, player_y, x, y):
                    if x < 800 and x > -800:
                        new_fireballs.append((x, y, direction))

    fireballs = new_fireballs
           

def keyboard(key, x, y):
    global player_x, player_y, velocity_y, isJumping, move_left, move_right, gun_side, isPaused, last_time, player_health

    if key == b'a' or key == b'A':
        move_left = True
        gun_side = "left"
    elif key == b'd' or key == b'D':
        move_right = True
        gun_side = "right"
    elif key == b' ' and not isJumping:
        velocity_y = jump_strength
        isJumping = True
    elif key == b'q' or key == b'Q':
        isPaused = not isPaused
        print("Game Paused") if isPaused else print("Game Resumed")
        last_time = time.time()
   
    elif key == b'r' or key == b'R':
        player_x = -500
        player_y = -540
        player_health = 5
    
        
def keyboardUp(key, x, y):
    global move_left, move_right
    if key == b'a' or key == b'A':
        move_left = False
    elif key == b'd' or key == b'D':
        move_right = False


def mouse(button, state, x, y):
    global bullets, gun_side, player_x, player_y, last_bullet_time

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        current_time = time.time()
        if current_time - last_bullet_time >= bullet_cooldown:
            # Add a new bullet at the gun's position
            bullet_x = player_x - 20 if gun_side == "left" else player_x + 20
            bullet_y = player_y - 12
            bullets.append((bullet_x, bullet_y, gun_side))
            last_bullet_time = current_time



def display():
    global gun_side, player_x, player_y, platforms
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen
    glLoadIdentity()  # Reset the transformation matrix
    # shapes.MidpointLine(-800, -600, 800, -600)
    # shapes.MidpointLine(-800, 700, 800, 700)
    
    if config.level == 1:
        l1.drawGround_l1()
        l1.drawPlatforms_l1()
        l1.drawPickups_l1()
        l1.drawWalls_l1()
        l1.drawSpikes_l1()
        l1.drawCannons_l1()
        l1.drawMud_l1()
        l1.drawExitDoor_l1()
        l1.drawCeiling_l1()
        l1.drawEnemy_l1()
    elif config.level == 2:
        l2.drawGround_l2()
        l2.drawPlatforms_l2()
        l2.drawPickups_l2()
        l2.drawWalls_l2()
        l2.drawSpikes_l2()
        l2.drawCannons_l2()
        l2.drawMud_l2()
    

        l2.drawExitDoor_l2()
        l2.drawCeiling_l2()
        l2.drawEnemy_l2()
    
    
    # Handle blinking effect
    if not player_immune:
        assets.player(player_x, player_y, gun_side)
    else:
        assets.player(player_x, player_y, gun_side, 1, (1, 0, 0))
    
    assets.drawHealth_Score(player_health, player_score)
    
    for bullet in bullets:
        x, y, _ = bullet
        shapes.drawPixel(x, y, bullet_size, (1, 1, 0))
    
    for fireball in fireballs:
        x, y, _ = fireball
        shapes.drawPixel(x, y, bullet_size, (1, 0.5, 0))
        
    glutSwapBuffers()
    
    
def animate(value):
    global last_time, isGameOver, isPaused, player_score
    if isGameOver:
        print(f"Game Over! Your score is {player_score}")
        end.show_end_screen(player_score, "GAME OVER")  # Show the end screen
        
        return
    if not isGameOver and not isPaused:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        updatePlayer(delta_time)
        updateBullets(delta_time)
        shootFireball()
        updateFireballs(delta_time)
        if config.level == 1:
            assets.moveRunnerEnemies(delta_time, isPaused)
            assets.moveFlyingEnemies(delta_time, isPaused)
        elif config.level == 2:
            assets.moveRunnerEnemies(delta_time, isPaused)
            assets.moveTankEnemies(delta_time, isPaused)

    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)
    

def initialize():
    """Initialize OpenGL settings for the game."""
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Set the background color to black
    glMatrixMode(GL_PROJECTION)  # Set the projection matrix
    glLoadIdentity()
    gluOrtho2D(-800, 800, -800, 800)  # Set up a 2D orthographic projection
    glMatrixMode(GL_MODELVIEW)  # Switch back to the modelview matrix

# GLUT Initialization
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1200, 900)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Platformer")

# Show the menu initially
menu.show_menu()

def check_menu(value=0):
    global player_health
    """Checks if the menu is active and transitions to the game if needed."""
    # print(f"Checking menu - play_clicked is: {menu.play_clicked}")
    if menu.play_clicked:
        print("Starting game...")
        player_health = menu.diff_health

        initialize()  # Initialize game OpenGL settings
        glutDisplayFunc(display)  # Set the game display function
        glutKeyboardFunc(keyboard)
        glutKeyboardUpFunc(keyboardUp)
        glutMouseFunc(mouse)
        glutTimerFunc(16, animate, 0)  # Start game animation loop
        glutPostRedisplay()
    else:
        glutTimerFunc(16, check_menu, 0)

# Start the timer to check the menu state
glutTimerFunc(16, check_menu, 0)  # Check every 16ms

# Start the main loop
glutMainLoop()