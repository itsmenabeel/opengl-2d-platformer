# menu.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
from midpoint_line_circle import midpoint_line_8way

menu_active = True
play_clicked = False

def initialize_menu():
    """Initialize OpenGL settings for menu"""
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-800, 800, -800, 800)

def draw_menu():
    """Draws the main menu."""
    global menu_active
    if menu_active:
        glClear(GL_COLOR_BUFFER_BIT)

        # Draw button outlines using midpoint line algorithm
        # Play Button
        midpoint_line_8way(-200, 50, 200, 50, 3, (0, 1, 0))   # Bottom
        midpoint_line_8way(-200, 150, 200, 150, 3, (0, 1, 0)) # Top
        midpoint_line_8way(-200, 50, -200, 150, 3, (0, 1, 0)) # Left
        midpoint_line_8way(200, 50, 200, 150, 3, (0, 1, 0))   # Right

        # Exit Button
        midpoint_line_8way(-200, -150, 200, -150, 3, (1, 0, 0)) # Bottom
        midpoint_line_8way(-200, -50, 200, -50, 3, (1, 0, 0))   # Top
        midpoint_line_8way(-200, -150, -200, -50, 3, (1, 0, 0)) # Left
        midpoint_line_8way(200, -150, 200, -50, 3, (1, 0, 0))   # Right

        # Add text
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2f(-200, 200)
        for char in "The American Mario":
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
            
        glRasterPos2f(-40, 90)
        for char in "PLAY":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18 , ord(char))
            
        glRasterPos2f(-40,-110)
        for char in "EXIT":
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18 , ord(char))

        glutSwapBuffers()

def menu_mouse(button, state, x, y):
    """Handles mouse clicks on the menu."""
    global play_clicked, menu_active
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        window_width = glutGet(GLUT_WINDOW_WIDTH)
        window_height = glutGet(GLUT_WINDOW_HEIGHT)
        
        ogl_x = (x - window_width/2) * (1600.0 / window_width)
        ogl_y = (window_height/2 - y) * (1600.0 / window_height)
        
        if -200 <= ogl_x <= 200 and 50 <= ogl_y <= 150:
            print("Play clicked - setting flag to True")  # Debug print
            play_clicked = True
            menu_active = False
            print(f"play_clicked is now: {play_clicked}")  # Debug print
            
        elif -200 <= ogl_x <= 200 and -150 <= ogl_y <= -50:
            os._exit(0)
def show_menu():
    """Displays the menu."""
    initialize_menu()
    glutDisplayFunc(draw_menu)
    glutMouseFunc(menu_mouse)