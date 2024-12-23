from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import midpoint_line_circle as shapes

def keyboard(key, x, y):
    pass

def mouse(button, state, x, y):
    pass

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    shapes.MidpointLine(0, 0, 100, 100)
    shapes.MidpointLine(-100, -50, 100, 200)
    shapes.MidpointCircle(0, 0, 50, [1,3,5,7])
    shapes.MidpointCircle(500, 500, 50, [0,2,4,6])
    shapes.MidpointCircle(0, -100, 50)
    glFlush()
    
# Initialize the game
def initialize():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-800, 800, -800, 800)

# Driver code
glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1200, 900)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Platformer")
initialize()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
# glutTimerFunc(16, update, 0)
glutMainLoop()