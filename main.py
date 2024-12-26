from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes
import assets
import collision

# global variables
player_x = -500  # Initial x-coordinate of the player's head
player_y = -540  # Initial y-coordinate of the player's head
gravity = -300  # Acceleration due to gravity
player_speed = 300  # Speed of the player
player_health = 5
player_score = 0
player_immune = 1
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
bullet_cooldown = 1  # Cooldown period in seconds
bullets = []  # List to store active bullets as tuples (x, y, direction)
platforms = collision.platforms  # List of platforms as tuples (x1, y1, length, width)


def updatePlayer(delta_time):
    global player_x, player_y, player_health, gravity, velocity_y, isJumping, move_left, move_right, last_hit_time

    # Apply gravity
    velocity_y += gravity * 2 * delta_time
    new_y = player_y + int(velocity_y * 2 * delta_time)

    # Detect collisions
    if collision.platformCollision(player_x, new_y):
        velocity_y = 0
        isJumping = False
    else:
        player_y = new_y
        
    if move_left and not collision.platformCollision(player_x - player_speed * delta_time, player_y):
        player_x -= player_speed * delta_time if player_x - 12 > -800 else 0
    if move_right and not collision.platformCollision(player_x + player_speed * delta_time, player_y):
        player_x += player_speed * delta_time if player_x + 12 < 800 else 0


    if collision.enemyCollision(player_x - player_speed * delta_time, player_y):
        cur_time = time.time()
        if cur_time - last_hit_time > 1:
            player_health -= 1
            player_x += 10
            print(player_health)
            last_hit_time = cur_time
    

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
            new_bullets.append((x, y, direction))

        elif collision.enemyBulletCollision(x, y):
            player_score += 1
            print(player_score)

    bullets = new_bullets
           


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
    
    for platform in platforms:
        x1, y1, length, width, isBrittle, isMoving = platform
        assets.normalPlatform(x1, y1, length, width)
        
    assets.exitDoor(-200, -200)
    assets.player(player_x, player_y, gun_side)
    
    assets.runnerEnemy()
    
    for bullet in bullets:
        x, y, _ = bullet
        shapes.drawPixel(x, y, bullet_size, (1, 1, 0))
        
    glutSwapBuffers()
    
    
def animate(value):
    global last_time, isGameOver, isPaused
    if not isGameOver and not isPaused:
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        updatePlayer(delta_time)
        updateBullets(delta_time)
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