from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets
import collision
import config
import level_1 as l1

# global variables
player_x = -500  # Initial x-coordinate of the player's head
player_y = -540  # Initial y-coordinate of the player's head
gravity = -300  # Acceleration due to gravity
player_speed = 300  # Speed of the player
player_health = 5
player_score = 0
player_immune = False  # Flag to indicate if the player is immune to damage
blinking = False  # Flag to indicate if the player model is blinking
last_hit_time = 0  # Timestamp of the last time the player was hit
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
bullet_cooldown = 1  # Cooldown period in seconds
fireball_cooldown = 2  # Cooldown period in seconds
bullets = []  # List to store active bullets as tuples (x, y, direction)
fireballs = []  # List to store active fireballs as tuples (x, y, direction)
invincible_time = 0  # Time remaining for invincibility
blink_interval = 0.1  # Interval for blinking effect
last_blink_time = 0  # Timestamp of the last blink

if config.level == 1:
    platforms = l1.platforms  # List of platforms as tuples (x1, y1, length, width)
    pickups = l1.pickups  # List of pickups as tuples (x, y)
    walls = l1.walls  # List of walls as tuples (x1, y1, height, width)
    spikes = l1.spikes  # List of spikes as tuples (x1, y1)
    cannons = l1.cannons  # List of cannons as tuples (x, y)


def updatePlayer(delta_time):
    global player_x, player_y, player_health, gravity, velocity_y, isJumping, move_left, move_right, fireballs
    global last_hit_time, isGameOver, invincible_time, blink_interval, last_blink_time, player_immune, blinking
    # Apply gravity
    velocity_y += gravity * 2 * delta_time
    new_y = player_y + int(velocity_y * 2 * delta_time)

    # Detect collisions
    if collision.platformCollision(player_x, new_y) or collision.wallCollision(player_x, new_y):
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
        fireballHit = False
        cur_time = time.time()
        if cur_time - last_hit_time > 2:
            player_health -= 1
            player_immune = True
            print(player_health)
            last_hit_time = cur_time
            if player_health == 0:
                isGameOver = True
        else:
            player_immune = False
                           
    # Check for collision with pickups
    collided_heart, index = collision.heartPickupCollision(player_x, player_y)
    if collided_heart:
        player_health += 1
        print(player_health)
        if index is not None:
            pickups.remove(pickups[index])
    
    # Change horizontal position
    if move_left:
        horz_collision_plat = collision.platformCollision(player_x - player_speed * delta_time, player_y)
        horz_collision_wall = collision.wallCollision(player_x - player_speed * delta_time, player_y)
        if not horz_collision_plat and not horz_collision_wall:
            player_x -= player_speed * delta_time if player_x - 12 > -800 else 0   
    if move_right:
        horz_collision_plat = collision.platformCollision(player_x + player_speed * delta_time, player_y)
        horz_collision_wall = collision.wallCollision(player_x + player_speed * delta_time, player_y)
        if not horz_collision_plat and not horz_collision_wall:
            player_x += player_speed * delta_time if player_x + 12 < 800 else 0
    

    # Keep player within screen bounds
    if player_y < -557:
        player_y = -557
        velocity_y = 0
        isJumping = False
      
        
def updateBullets(delta_time):
    global bullets, player_score
    new_bullets = []
    
    for bullet in bullets:
        x, y, direction = bullet
        x += bullet_speed * delta_time if direction == "right" else -bullet_speed * delta_time  # Move the bullet
        # Check for collision with platforms and enemies
        if not collision.bulletCollision(x, y) and not collision.enemyBulletCollision(x, y):
            if not collision.wallCollision(x, y):
                new_bullets.append((x, y, direction))

        elif collision.enemyBulletCollision(x, y):
            player_score += 1
            print(player_score)

    bullets = new_bullets
   

def shootFireball():
    global cannons, fireballs, last_fireball_time, fireball_cooldown
    for fireball in cannons:
        current_time = time.time()
        x, y = fireball
        if current_time - last_fireball_time >= fireball_cooldown:
            # Add a new bullet at the cannon's tip
            bullet_x = x
            bullet_y = y
            if x < 0:
                fireballs.append((bullet_x, bullet_y, "right"))
            elif x > 0:
                fireballs.append((bullet_x, bullet_y, "left"))
            last_fireball_time = current_time
        


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
    global player_x, player_y, velocity_y, isJumping, move_left, move_right, gun_side, isPaused, last_time
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
    glClear(GL_COLOR_BUFFER_BIT)
    shapes.MidpointLine(-800, -600, 800, -600)
    
    if config.level == 1:
        l1.drawPlatforms_l1()
        l1.drawPickups_l1()
        l1.drawWalls_l1()
        l1.drawSpikes_l1()
        l1.drawCannons_l1()
        
    assets.exitDoor(-200, 500)
    
    # Handle blinking effect
    if not player_immune:
        assets.player(player_x, player_y, gun_side)
    else:
        assets.player(player_x, player_y, gun_side, 1, (1, 0, 0))
    
    assets.runnerEnemy()
    
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
        glutLeaveMainLoop()
        return
    if not isGameOver and not isPaused:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        updatePlayer(delta_time)
        updateBullets(delta_time)
        shootFireball()
        updateFireballs(delta_time)
        assets.moveRunnerEnemies(delta_time, isPaused)

    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)
    
    
# Initialize the game
def initialize():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-800, 800, -800, 800)


# Driver code
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(1200, 900)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Platformer")
initialize()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutKeyboardUpFunc(keyboardUp)
glutMouseFunc(mouse)
glutTimerFunc(16, animate, 0)
glutMainLoop()