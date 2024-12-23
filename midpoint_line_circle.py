from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Draws a pixel at the specified coordinates
def drawPixel(x, y):
    glBegin(GL_POINTS)
    glVertex2i(int(x), int(y))
    glEnd()

# Draws a line using the Midpoint Line Drawing algorithm
class MidpointLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        zone = self.findZone(self.x1, self.y1, self.x2, self.y2)  # Find the zone of the line
        x1_z0, y1_z0 = self.convert_to_zone_0(self.x1, self.y1, zone)  # Convert the coordinates to zone 0
        x2_z0, y2_z0 = self.convert_to_zone_0(self.x2, self.y2, zone)

        dx = x2_z0 - x1_z0
        dy = y2_z0 - y1_z0
        d = 2 * dy - dx
        deltaE = 2 * dy
        deltaNE = 2 * (dy - dx)

        if x1_z0 > x2_z0:  # If the initial x-point is greater than the final x-point, swap them due to loop structure
            x1_z0, x2_z0 = x2_z0, x1_z0
            y1_z0, y2_z0 = y2_z0, y1_z0

        x, y = x1_z0, y1_z0
        while x <= x2_z0:  # Going only from initial x-point to final one, as final y-point will be reached automatically
            orig_x, orig_y = self.convert_from_zone_0(x, y, zone)  # Convert the coordinates back to the original zone
            drawPixel(orig_x, orig_y)  # Draw the original pixel
            if d > 0:
                y += 1
                d += deltaNE  # Going NE
            else:
                d += deltaE  # Going E
            x += 1

    def convert_to_zone_0(self, x, y, zone):  # Converts coordinates from any zone to zone 0
        if zone == 0:
            return x, y
        elif zone == 1:
            return y, x
        elif zone == 2:
            return y, -x
        elif zone == 3:
            return -x, y
        elif zone == 4:
            return -x, -y
        elif zone == 5:
            return -y, -x
        elif zone == 6:
            return -y, x
        elif zone == 7:
            return x, -y

    def convert_from_zone_0(self, x, y, zone):  # Converts coordinates from zone 0 to the original zone
        if zone == 0:
            return x, y
        elif zone == 1:
            return y, x
        elif zone == 2:
            return -y, x
        elif zone == 3:
            return -x, y
        elif zone == 4:
            return -x, -y
        elif zone == 5:
            return -y, -x
        elif zone == 6:
            return y, -x
        elif zone == 7:
            return x, -y

    def findZone(self, x1, y1, x2, y2):  # Finds the zone of the line
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) >= abs(dy):  # Slanty lines
            if dx >= 0 and dy >= 0:
                return 0
            elif dx >= 0 and dy < 0:
                return 7
            elif dx < 0 and dy >= 0:
                return 3
            else:
                return 4
        else:  # Steep lines
            if dx >= 0 and dy >= 0:
                return 1
            elif dx >= 0 and dy < 0:
                return 6
            elif dx < 0 and dy >= 0:
                return 2
            else:
                return 5

# Draws a circle using the Midpoint Circle Drawing algorithm
class MidpointCircle:
    def __init__(self, x_center, y_center, radius, zones = None):
        self.x_center = x_center
        self.y_center = y_center
        self.radius = radius
        self.zones = zones

        x = 0
        y = radius
        d = 1 - radius

        self.draw_circle_symmetric_points(self.x_center, self.y_center, x, y, self.zones)  # Draw the first point and its reflections

        while x < y:
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * x - 2 * y + 5
                y -= 1
            x += 1
            self.draw_circle_symmetric_points(self.x_center, self.y_center, x, y, self.zones)  # Once a point is found, draw all its reflections

    def draw_circle_symmetric_points(self, x_center, y_center, x, y, zones):
        # Takes a certain pixel and draws all the reflections in all zones simultaneously
        if zones is None:
            drawPixel(int(x_center + y), int(y_center + x))  # Zone - 0 (y, x)
            drawPixel(int(x_center + x), int(y_center + y))  # Zone - 1 (x, y)
            drawPixel(int(x_center - x), int(y_center + y))  # Zone - 2 (-x, y)
            drawPixel(int(x_center - y), int(y_center + x))  # Zone - 3 (-y, x)
            drawPixel(int(x_center - y), int(y_center - x))  # Zone - 4 (-y, -x)
            drawPixel(int(x_center - x), int(y_center - y))  # Zone - 5 (-x, -y)
            drawPixel(int(x_center + x), int(y_center - y))  # Zone - 6 (x, -y)
            drawPixel(int(x_center + y), int(y_center - x))  # Zone - 7 (y, -x)
        else:
            for zone in zones:
                if zone == 0:
                    drawPixel(int(x_center + y), int(y_center + x))  # Zone - 0 (y, x)
                elif zone == 1:
                    drawPixel(int(x_center + x), int(y_center + y))  # Zone - 1 (x, y)
                elif zone == 2:
                    drawPixel(int(x_center - x), int(y_center + y))  # Zone - 2 (-x, y)
                elif zone == 3:
                    drawPixel(int(x_center - y), int(y_center + x))  # Zone - 3 (-y, x)
                elif zone == 4:
                    drawPixel(int(x_center - y), int(y_center - x))  # Zone - 4 (-y, -x)
                elif zone == 5:
                    drawPixel(int(x_center - x), int(y_center - y))  # Zone - 5 (-x, -y)
                elif zone == 6:
                    drawPixel(int(x_center + x), int(y_center - y))  # Zone - 6 (x, -y)
                elif zone == 7:
                    drawPixel(int(x_center + y), int(y_center - x))  # Zone - 7 (y, -x)
                    