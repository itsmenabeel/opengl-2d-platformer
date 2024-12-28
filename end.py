from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from midpoint_line_circle import midpoint_line_8way
import os
import menu
score = 0
end_text= "GAME OVER"
def initialize_end_screen():
    """Initialize OpenGL settings for the end screen."""
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Black background
    glMatrixMode(GL_PROJECTION)  # Set projection matrix mode
    glLoadIdentity()  # Reset any existing transformations
    gluOrtho2D(-800, 800, -800, 800)  # Set orthographic projection
    glMatrixMode(GL_MODELVIEW)  # Switch back to modelview mode

def draw_end_screen():
    """Draws the Game Over screen."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear the screen

    # Draw large "Game Over" title
    glColor3f(1.0, 0.0, 0.0)  # Red color for "Game Over"
    glPushMatrix()
    glTranslatef(-370, 300, 0)  # Position at the top center
    glScalef(1.0, 1.0, 1.0)  # Scale to make it large
    glLineWidth(2)  # Set line width for the stroke font

    for char in end_text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()

    # Draw "Your score" text
    glColor3f(1.0, 1.0, 1.0)  # White color for the score
    glRasterPos2f(-90, 100)  # Position below "Game Over"
    for char in f"Your score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Draw Restart button
    glColor3f(0.0, 1.0, 0.0)  # Green color for the Restart button
    midpoint_line_8way(-200, -50, 200, -50, 3, (0, 1, 0))  # Bottom
    midpoint_line_8way(-200, 50, 200, 50, 3, (0, 1, 0))    # Top
    midpoint_line_8way(-200, -50, -200, 50, 3, (0, 1, 0))  # Left
    midpoint_line_8way(200, -50, 200, 50, 3, (0, 1, 0))    # Right

    # Draw "Restart" text
    glColor3f(1.0, 1.0, 1.0)  # White color for "Restart"
    glRasterPos2f(-50, 0)  # Centered inside the Restart button
    for char in "Restart":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    # Draw Exit button
    glColor3f(1.0, 0.0, 0.0)  # Red color for the Exit button
    midpoint_line_8way(-200, -200, 200, -200, 3, (1, 0, 0))  # Bottom
    midpoint_line_8way(-200, -100, 200, -100, 3, (1, 0, 0))  # Top
    midpoint_line_8way(-200, -200, -200, -100, 3, (1, 0, 0))  # Left
    midpoint_line_8way(200, -200, 200, -100, 3, (1, 0, 0))    # Right

    # Draw "Exit" text
    glColor3f(1.0, 1.0, 1.0)  # White color for "Exit"
    glRasterPos2f(-30, -150)  # Centered inside the Exit button
    for char in "Exit":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glutSwapBuffers()  # Swap buffers for display

def end_screen_mouse(button, state, x, y):
    """Handles mouse clicks on the end screen."""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        window_width = glutGet(GLUT_WINDOW_WIDTH)
        window_height = glutGet(GLUT_WINDOW_HEIGHT)

        # Convert mouse coordinates to OpenGL coordinates
        ogl_x = (x - window_width / 2) * (1600.0 / window_width)
        ogl_y = (window_height / 2 - y) * (1600.0 / window_height)

        # Check if the Restart button is clicked
        if -200 <= ogl_x <= 200 and -50 <= ogl_y <= 50:
            print("Restart clicked - restarting game")
            menu.show_menu() # Restart the game by re-executing the script (Did not work)

        # Check if the Exit button is clicked
        elif -200 <= ogl_x <= 200 and -200 <= ogl_y <= -100:
            print("Exit clicked - exiting game")
            os._exit(0)  # Exit the program

def show_end_screen(final_score, end):

    """Displays the end screen."""
    global score, end_text
    end_text = end
    score = final_score
    initialize_end_screen()
    glutDisplayFunc(draw_end_screen)
    glutMouseFunc(end_screen_mouse)
    glutPostRedisplay()