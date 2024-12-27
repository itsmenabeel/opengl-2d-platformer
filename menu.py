# menu.py
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import os
from midpoint_line_circle import midpoint_line_8way
easy_stage = False
hard_stage = False
menu_active = True
play_clicked = False
diff_health = 5
selected_mode = ""  # Add a global variable to store the selected mode

def initialize_menu():
    global diff_health
    """Initialize OpenGL settings for menu"""
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-800, 800, -800, 800)

def draw_menu():
    """Draws the main menu."""
    global menu_active, selected_mode
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

        # Display selected mode
        if selected_mode:
            glColor3f(1.0, 1.0, 1.0)
            glRasterPos2f(-100, -500)
            for char in selected_mode:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

        glutSwapBuffers()

def menu_mouse(button, state, x, y):
    """Handles mouse clicks on the menu."""
    global play_clicked, menu_active, diff_health, easy_stage, hard_stage, selected_mode
    
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        window_width = glutGet(GLUT_WINDOW_WIDTH)
        window_height = glutGet(GLUT_WINDOW_HEIGHT)
        
        ogl_x = (x - window_width/2) * (1600.0 / window_width)
        ogl_y = (window_height/2 - y) * (1600.0 / window_height)
        
        if -200 <= ogl_x <= 200 and 50 <= ogl_y <= 150:
            # print("Play clicked - setting flag to True")  # Debug print
            play_clicked = True
            menu_active = False
            # print(f"play_clicked is now: {play_clicked}")  # Debug print
            
        elif -200 <= ogl_x <= 200 and -150 <= ogl_y <= -50:
            os._exit(0)
        
        elif -200 <= ogl_x <= 200 and -350 <= ogl_y <= -250:
            # print("Easy clicked - setting difficulty to Easy")  # Debug print
            easy_stage = True
            hard_stage = False
            diff_health = 5
            selected_mode = "Easy Mode Selected"
            # print(f"diff_health set to: {diff_health}")  # Debug print
            glutPostRedisplay() # Request a redraw to update the display
            
        elif -200 <= ogl_x <= 200 and -450 <= ogl_y <= -350:
            # print("Hard clicked - setting difficulty to Hard")  # Debug print
            easy_stage = False
            hard_stage = True
            diff_health = 3
            selected_mode = "Hard Mode Selected"
            # print(f"diff_health set to: {diff_health}")  # Debug print
            glutPostRedisplay()  # Request a redraw to update the display
def show_menu():
    """Displays the menu."""
    initialize_menu()
    glutDisplayFunc(draw_menu)
    glutMouseFunc(menu_mouse)