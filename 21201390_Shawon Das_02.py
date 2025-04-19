from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500

# Catcher parameters
trayX1, trayX2 = -75, 75
trayY1 = trayY2 = -230
traySpeed = 6

# Diamond parameters
diaX1 = diaX2 = random.randrange(-250, 250, 1)
diaY1 = 190
diaY2 = 160
fall_speed = 0.75

# Flags and counters
pause_flag = False
over_flag = False
score_count = 0

r = random.uniform(0.4, 1)
g = random.uniform(0.4, 1)
b = random.uniform(0.4, 1)

# Function to find zone for line drawing
def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0

    if dx == 0:
        if dy > 0:
            zone = 1
        else:
            zone = 6
    elif dy == 0:
        if dx > 0:
            zone = 7
        else:
            zone = 3
    else:
        if abs(dx) >= abs(dy):
            if dx > 0 and dy > 0:
                zone = 0
            if dx < 0 and dy > 0:
                zone = 3
            if dx < 0 and dy < 0:
                zone = 4
            if dx > 0 and dy < 0:
                zone = 7
        else:
            if dx > 0 and dy > 0:
                zone = 1
            if dx < 0 and dy > 0:
                zone = 2
            if dx < 0 and dy < 0:
                zone = 5
            if dx > 0 and dy < 0:
                zone = 6
    return zone

# Function to convert coordinates based on zone
def convert(fromZone, X, Y):
    x = 0
    y = 0

    if fromZone == 0:
        x = X
        y = Y
    if fromZone == 1:
        x = Y
        y = X
    if fromZone == 2:
        x = Y
        y = -X
    if fromZone == 3:
        x = -X
        y = Y
    if fromZone == 4:
        x = -X
        y = -Y
    if fromZone == 5:
        x = -Y
        y = -X
    if fromZone == 6:
        x = -Y
        y = X
    if fromZone == 7:
        x = X
        y = -Y

    return x, y

# Function to convert back to original coordinates based on zone
def convert_original(toZone, X, Y):
    x = 0
    y = 0
    if toZone == 0:
        x = X
        y = Y
    if toZone == 1:
        x = Y
        y = X
    if toZone == 2:
        x = -Y
        y = X
    if toZone == 3:
        x = -X
        y = Y
    if toZone == 4:
        x = -X
        y = -Y
    if toZone == 5:
        x = -Y
        y = -X
    if toZone == 6:
        x = Y
        y = -X
    if toZone == 7:
        x = X
        y = -Y

    return x, y

# Midpoint line drawing algorithm
def midpoint(x0, y0, x1, y1, currentZone, pointSize):
    dx = x1 - x0
    dy = y1 - y0
    d = (2 * dy) - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x = x0
    y = y0

    while x <= x1:
        org_x, org_y = convert_original(currentZone, x, y)
        draw_points(org_x, org_y, pointSize)
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1

# Eight-way symmetry for line drawing
def drawLine(x0, y0, x1, y1, pointSize=2):
    currentZone = find_zone(x0, y0, x1, y1)
    conv_x0, conv_y0 = convert(currentZone, x0, y0)
    conv_x1, conv_y1 = convert(currentZone, x1, y1)
    midpoint(conv_x0, conv_y0, conv_x1, conv_y1, currentZone, pointSize)

# Function to draw points
def draw_points(x, y, pointSize):
    glPointSize(pointSize)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


# Special key listener for movement
def specialKeyListener(key, x, y):
    global trayX1, trayX2, traySpeed, pause_flag

    if key == GLUT_KEY_RIGHT:
        if trayX2 <= 250 and not over_flag and not pause_flag:
            trayX1 += traySpeed
            trayX2 += traySpeed

    if key == GLUT_KEY_LEFT:
        if trayX1 >= -250 and not over_flag and not pause_flag:
            trayX1 -= traySpeed
            trayX2 -= traySpeed
    glutPostRedisplay()

# Function to draw the catcher
def draw_catcher():
    global trayX1, trayY1, trayX2, trayY2, over_flag

    if not over_flag:
        glColor(1, 1, 1)
    else:
        glColor(1, 0, 0)

    drawLine(trayX1, trayY1, trayX2, trayY2)
    drawLine(trayX1, trayY1, trayX1 + 20, trayY1 - 20)
    drawLine(trayX2, trayY2, trayX2 - 20, trayY1 - 20)
    drawLine(trayX1 + 20, trayY1 - 20, trayX2 - 20, trayY1 - 20)

# Function to draw a diamond
def draw_diamond():
    global r, g, b, diaX1, diaY1, diaX2, diaY2
    glColor(r, g, b)

    drawLine(diaX1, diaY1, diaX1 - 10, diaY1 - 15)
    drawLine(diaX1, diaY1, diaX1 + 10, diaY1 - 15)
    drawLine(diaX1 - 10, diaY1 - 15, diaX2, diaY2)
    drawLine(diaX1 + 10, diaY1 - 15, diaX2, diaY2)

# Function to draw left arrow
def left_arrow():
    glColor(0.21, 0.74, 0.97)
    drawLine(-220, 240, -240, 220, 1)
    drawLine(-240, 220, -220, 200, 1)
    drawLine(-240, 220, -200, 220, 1)

# Function to draw cross
def cross():
    glColor(1, 0, 0)
    drawLine(240, 240, 200, 200, 1)
    drawLine(200, 240, 240, 200, 1)

# Function to draw play button
def play():
    glColor(0.98, 0.82, 0.3)
    drawLine(-20, 200, -20, 240, 1)
    drawLine(-20, 200, 20, 220, 1)
    drawLine(-20, 240, 20, 220, 1)

# Function to draw pause button
def pause():
    glColor(0.98, 0.82, 0.3)
    drawLine(-10, 200, -10, 240, 1)
    drawLine(10, 200, 10, 240, 1)

def pauseGame():
    global pause_flag
    pause_flag = True

def resumeGame():
    global pause_flag
    pause_flag = False

def restartGame():
    global over_flag, score_count, fall_speed, r, g, b, diaX1, diaY1, diaX2, diaY2

    over_flag = False
    score_count = 0

    r = random.uniform(0.4, 1.0)
    g = random.uniform(0.4, 1.0)
    b = random.uniform(0.4, 1.0)

    diaY1 = 190
    diaY2 = 160
    diaX1 = diaX2 = random.randrange(-250, 250, 1)
    fall_speed = 0.5
    print("Starting Over!")

def exitGame():
    global score_count
    print(f"Goodbye! Score: {score_count}")

    glutLeaveMainLoop()

# Mouse listener for button clicks
def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b

def mouseListener(button, state, x, y):
    global pause_flag

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            c_x, c_y = convert_coordinate(x, y)

            if (-240 <= c_x <= -200) and (200 <= c_y <= 240):
                restartGame()

            if (-10 <= c_x <= 10) and (200 <= c_y <= 240) and not pause_flag:
                pauseGame()
            elif (-20 <= c_x <= 20) and (200 <= c_y <= 240) and pause_flag:
                resumeGame()

            if (200 <= c_x <= 240) and (200 <= c_y <= 240):
                exitGame()

    glutPostRedisplay()

# Check collision between catcher and diamond
def check_collision():
    global trayX1, trayX2, trayY1, diaY1, diaX1, diaY2

    box1x = trayX1
    box1y = trayY1 - 20

    box2x = diaX1 - 10
    box2y = diaY2

    box1Width = abs(trayX2 - trayX1)
    box2Width = 20
    box1Height = 20
    box2Height = abs(diaY1 - diaY2)

    return (
        box1x < box2x + box2Width
        and box1x + box1Width > box2x
        and box1y < box2y + box2Height
        and box1y + box1Height > box2y
    )

def checkScore():
    global trayX1, trayX2, trayY1, diaY2, diaX1, score_count, r, g, b, diaY1, diaX2, fall_speed, over_flag

    if check_collision():
        score_count += 1

        if fall_speed <= 2:
            fall_speed += 0.05

        r = random.uniform(0.4, 1.0)
        g = random.uniform(0.4, 1.0)
        b = random.uniform(0.4, 1.0)

        diaY1 = 190
        diaY2 = 160
        diaX1 = diaX2 = random.randrange(-250, 250, 1)

        print(f"Score: {score_count}")

    if diaY1 <= -251:
        print(f"Game Over! Score: {score_count}")
        score_count = 0
        over_flag = True
        diaY1 = 290
        diaY2 = 260

# Main display function
def showScreen():
    global pause_flag
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)

    # draw functions
    left_arrow()
    cross()

    if pause_flag:
        play()
    else:
        pause()

    draw_catcher()
    draw_diamond()

    glutSwapBuffers()

# Animation function
def animation():
    global diaY1, diaY2, fall_speed, over_flag, pause_flag
    if pause_flag:
        return

    if not over_flag:
        checkScore()
        diaY1 -= fall_speed
        diaY2 -= fall_speed

    glutPostRedisplay()

def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Catch the Diamonds!")
init()
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(animation)
glutMainLoop()
