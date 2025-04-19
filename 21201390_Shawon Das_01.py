#Task-1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random


window_width = 700 
window_height = 600 


raindrops = [] 
day=False
current_x_position = 0
background_color = [0.0, 0.0, 0.0] 
target_color = [0.0, 0.0, 0.0]
color_change_speed = 0.1 



def draw_line(x1, y1, x2, y2):

    if day==False:
        glColor3f(1, 1, 1)  
    elif day==True:
        glColor3f(0,0,0)

    glBegin(GL_LINES) 
    glVertex2f(x1, y1) 
    glVertex2f(x2, y2) 
    glEnd() 



def draw_rain():
    glColor3f(0.0, 0.0, 1.0) 
    glLineWidth(2.0)          

    glBegin(GL_LINES)
    for x, y in raindrops:
        glVertex2f(x - current_x_position, y)
        glVertex2f(x + current_x_position, y - 10)
    glEnd()



def generate_rain():
    x = random.randint(0, 1000)  
    y = 600                      
    raindrops.append((x, y))     



def animate_rain():
    for i in range(len(raindrops)):
        x, y = raindrops[i]
        y-= 10
        raindrops[i] = (x, y)

    raindrops[:] = [raindrop for raindrop in raindrops if raindrop[1] >=110] 



def change_background_color():
    global background_color, target_color

    for i in range(3):
        if background_color[i] < target_color[i]:
            background_color[i] += color_change_speed
        elif background_color[i] > target_color[i]:
            background_color[i] -= color_change_speed


def iterate():
    glViewport(0, 0, window_width, window_height) 
    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity() 
    glOrtho(0.0, window_width, 0.0, window_height, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(*background_color, 0.0)


def house():
    #wall
    draw_line(200, 100, 400, 100)
    draw_line(200, 100, 200, 250)
    draw_line(200, 250, 400, 250)
    draw_line(400, 100, 400, 250)
    glColor3f(0.0, 0.0, 1.0)  

    #roof
    draw_line(200, 250, 300, 300)
    draw_line(400, 250, 300, 300)

    #door
    draw_line(240, 100, 240, 175)   
    draw_line(290, 100, 290, 175)
    draw_line(240, 175, 290, 175)

    #window
    draw_line(330, 150, 330, 190)
    draw_line(330, 190, 370, 190)
    draw_line(370, 190, 370, 150)
    draw_line(370, 150, 330, 150)



def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_rain()
    animate_rain()
    generate_rain()
    change_background_color()
    house()
    glutSwapBuffers()


def specialKeyListener(key, x, y):
    global current_x_position

    if key == GLUT_KEY_RIGHT:
        current_x_position += 1 
    elif key == GLUT_KEY_LEFT:
        current_x_position -= 1 

    glutPostRedisplay() 

def keyboardListener(key, x, y):
    global target_color,day

    if key == b'd':
        if day==False:
            target_color = [1, 1, 1]  
            day= True

    elif key == b'n':
        if day==True:
            target_color = [0.0, 0.0, 0.0] 
            day=False
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 1) 
wind = glutCreateWindow(b"Task 1: Building a House in Rainfall")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutKeyboardFunc(keyboardListener)
glutIdleFunc(showScreen) 
glutMainLoop()










#Task-2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width = 500 
window_height = 500

balls = []
speed = 0.2
freeze = False
blink = False


speed_direction_of_balls = {
    0: [speed, speed],
    1: [speed, -speed],
    2: [-speed, speed],
    3: [-speed, -speed]}

def draw_points(x, y):
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def addSpeed(i):
    global balls, window_width, window_height
    if balls[i][0] >= window_width / 2 or balls[i][0] <= -window_width / 2:
        balls[i][3] = [-balls[i][3][0], balls[i][3][1]]

    if balls[i][1] >= window_height / 2 or balls[i][1] <= -window_height / 2:
        balls[i][3] = [balls[i][3][0], -balls[i][3][1]]

    balls[i][0] += balls[i][3][0] * speed
    balls[i][1] += balls[i][3][1] * speed


def animate():
    if freeze == False:
        glutPostRedisplay()

def convert_coordinate(x, y):
    global window_width, window_height
    a = x - (window_width / 2)
    b = (window_height / 2) - y
    return a, b


def mouseListener(button, state, x, y): 
    global balls, blink, speed_direction_of_balls, blinkFlag
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            blink = not blink

    if button == GLUT_RIGHT_BUTTON:
        if state == GLUT_DOWN:
            c_x, c_y = convert_coordinate(x, y)
            r = random.uniform(0.1, 1.0)
            g = random.uniform(0.1, 1.0)
            b = random.uniform(0.1, 1.0)
            dir = random.randrange(0, 4)
            balls.append([c_x, c_y, [r, g, b], speed_direction_of_balls[dir]])
    glutPostRedisplay()


def keyboardListener(key, x, y):
    global speed, freeze
    if key == b" ":
        freeze = not freeze
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global speed
    if key == GLUT_KEY_UP and freeze == False:
        speed *= 2
        print("Speed Increased")
    if key == GLUT_KEY_DOWN and freeze == False: 
        speed /= 2
        print("Speed Decreased")
    glutPostRedisplay()


def display():
    global balls
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    glMatrixMode(GL_MODELVIEW)
    drawRandomPoints()
    glutSwapBuffers()


def drawRandomPoints():
    global balls, blink
    for i in range(len(balls)):
        x = balls[i][0]
        y = balls[i][1]

        if blink and freeze:
            glColor3f(0, 0, 0)
        else:
            glColor3f(balls[i][2][0], balls[i][2][1], balls[i][2][2])
        draw_points(x, y)
        addSpeed(i)


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB) 
wind = glutCreateWindow(b"Task 2: Building the Amazing Box")
init()
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutMainLoop()
