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

# ...existing code...

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

            # Draw Play Button Text
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-30, 90)
            for char in "Play":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            # Exit Button
            midpoint_line_8way(-200, -150, 200, -150, 3, (1, 0, 0)) # Bottom
            midpoint_line_8way(-200, -50, 200, -50, 3, (1, 0, 0))   # Top
            midpoint_line_8way(-200, -150, -200, -50, 3, (1, 0, 0)) # Left
            midpoint_line_8way(200, -150, 200, -50, 3, (1, 0, 0))   # Right

            # Draw Exit Button Text
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-30, -110)
            for char in "Exit":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            # Draw Difficulty Text
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-50, -210)
            for char in "Difficulty":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            # Easy Button
            midpoint_line_8way(-200, -350, 200, -350, 3, (0, 0, 1)) # Bottom
            midpoint_line_8way(-200, -250, 200, -250, 3, (0, 0, 1)) # Top
            midpoint_line_8way(-200, -350, -200, -250, 3, (0, 0, 1)) # Left
            midpoint_line_8way(200, -350, 200, -250, 3, (0, 0, 1))   # Right

            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-50, -300)
            for char in "Easy":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            # Hard Button
            midpoint_line_8way(-200, -450, 200, -450, 3, (0, 0, 1)) # Bottom
            midpoint_line_8way(-200, -350, 200, -350, 3, (0, 0, 1)) # Top
            midpoint_line_8way(-200, -450, -200, -350, 3, (0, 0, 1)) # Left
            midpoint_line_8way(200, -450, 200, -350, 3, (0, 0, 1))   # Right

            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-50, -400)
            for char in "Hard":
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

            glutSwapBuffers()
# ...existing code...

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
        
        elif -200 <= ogl_x <= 200 and -350 <= ogl_y <= -250:
            print("Easy clicked - setting difficulty to Easy")  # Debug print
            # Set difficulty to Easy
            # Add your logic here
            
        elif -200 <= ogl_x <= 200 and -450 <= ogl_y <= -350:
            print("Hard clicked - setting difficulty to Hard")  # Debug print
            # Set difficulty to Hard
            # Add your logic here
def show_menu():
    """Displays the menu."""
    initialize_menu()
    glutDisplayFunc(draw_menu)
    glutMouseFunc(menu_mouse)