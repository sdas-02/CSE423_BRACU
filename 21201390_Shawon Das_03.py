from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math 

W_Width, W_Height = 1000, 800

# Camera-related variables
camera_pos = (0,500,500)
camera_angle = 0
camera_height = 500
camera_mode = False

#Player-related variables
player_pos = [0,0,10]
player_angle = 0
life = 5
score = 0

game_over = False
bullets_missed = 0
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423

#Enemy-related variables
bullets = []
enemies = []
enemy_count = 5
bullet_speed = 10
enemy_speed = .5
enemy_scale_min = 0.5
enemy_scale_max = 1.5
enemy_scale_speed = 0.05


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800) 
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)
    if game_over:
        glRotatef(90, 1, 0, 0) 

    # Head 
    glPushMatrix()
    glTranslatef(0, 0, 40) 
    glColor3f(0, 0, 0)  
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

    # Main body
    glPushMatrix()
    glTranslatef(0, 0, 20) 
    glScalef(20, 10, 20)  
    glColor3f(1, 0.5, 1)  
    glutSolidCube(1)
    glPopMatrix()

    # Gun
    glPushMatrix()
    glTranslatef(10, 0, 30)  
    glRotatef(90, 0, 1, 0) 
    glColor3f(0.5, 0.5, 0.5)  
    gluCylinder(gluNewQuadric(), 3, 3, 20, 10, 10)  
    glPopMatrix()

    # Arms
    glPushMatrix()
    glTranslatef(-15, 0, 30)  
    glRotatef(45, 0, 1, 0)  
    glColor3f(0, 0.5, 1)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(15, 0, 30)  
    glRotatef(-45, 0, 1, 0)  
    glColor3f(0, 0.5, 1)
    gluCylinder(gluNewQuadric(), 3, 3, 15, 10, 10)
    glPopMatrix()

    # Legs
    glPushMatrix()
    glTranslatef(-5, 0, 0) 
    glColor3f(0.2, 0, 0.2)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 10, 10)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5, 0, 0)  
    glColor3f(0.2, 0, 0.2)
    gluCylinder(gluNewQuadric(), 4, 4, 20, 10, 10)
    glPopMatrix()
    glPopMatrix()

def draw_enemy(x, y, z, scale):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glTranslatef(0, 0, 15)
    gluSphere(gluNewQuadric(), 10, 10, 10)
    glPopMatrix()

def draw_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 0.75, 0)
    glutSolidCube(5)
    glPopMatrix()

def draw_grid():
    glBegin(GL_QUADS)
    step = GRID_LENGTH // 10
    for i in range(-10, 11):
        for j in range(-10, 11):
            x1 = i * step
            x2 = (i + 1) * step
            y1 = j * step
            y2 = (j + 1) * step
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)

    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)
 
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 100)

    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 100)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 100)
    glEnd()

def init_enemies():
    global enemies
    enemies = []
    for _ in range(enemy_count):
        x = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        scale = random.uniform(enemy_scale_min, enemy_scale_max)
        enemies.append([x, y, 10, scale])

def keyboardListener(key, x, y):
    global player_pos, player_angle, life, score, bullets_missed, game_over
    if game_over and key != b'r':
        return
    if key == b'w':
        rad = math.radians(player_angle)
        player_pos[0] += 5 * math.cos(rad)
        player_pos[1] += 5 * math.sin(rad)
        player_pos[0] = max(-GRID_LENGTH + 20, min(GRID_LENGTH - 20, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 20, min(GRID_LENGTH - 20, player_pos[1]))
    if key == b's':
        rad = math.radians(player_angle)
        player_pos[0] -= 5 * math.cos(rad)
        player_pos[1] -= 5 * math.sin(rad)
        player_pos[0] = max(-GRID_LENGTH + 20, min(GRID_LENGTH - 20, player_pos[0]))
        player_pos[1] = max(-GRID_LENGTH + 20, min(GRID_LENGTH - 20, player_pos[1]))
    if key == b'a':
        player_angle += 5
    if key == b'd':
        player_angle -= 5
    if key == b'r':
        player_pos = [0, 0, 10]
        player_angle = 0
        life = 5
        score = 0
        bullets_missed = 0
        game_over = False
        camera_mode = False
        bullets.clear()
        init_enemies()


def specialKeyListener(key, x, y):
    global camera_height, camera_angle
    if game_over:
        return
    if key == GLUT_KEY_UP:
        camera_height = min(1000, camera_height + 10)
    if key == GLUT_KEY_DOWN:
        camera_height = max(100, camera_height - 10)
    if key == GLUT_KEY_LEFT:
        camera_angle += 5
    if key == GLUT_KEY_RIGHT:
        camera_angle -= 5


def mouseListener(button, state, x, y):
    global camera_mode, bullets
    if game_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        rad = math.radians(player_angle)
        bullets.append([player_pos[0], player_pos[1], player_pos[2] + 20, player_angle])
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = not camera_mode


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500) 
    glMatrixMode(GL_MODELVIEW)  
    glLoadIdentity()  
    if camera_mode:
        rad = math.radians(player_angle)
        x = player_pos[0] - 50 * math.cos(rad)
        y = player_pos[1] - 50 * math.sin(rad)
        z = player_pos[2] + 50
        center_x = player_pos[0] + 100 * math.cos(rad)
        center_y = player_pos[1] + 100 * math.sin(rad)
        center_z = player_pos[2] + 20
        gluLookAt(x, y, z, 
                  center_x, center_y, center_z, 
                  0, 0, 1)
    else:
        rad = math.radians(camera_angle)
        x = camera_height * math.cos(rad)
        y = camera_height * math.sin(rad)
        z = camera_height
        gluLookAt(x, y, z,  
                  0, 0, 0,  
                  0, 0, 1) 

def main_game():
    global bullets, enemies, life, score, bullets_missed, game_over
    if game_over:
        return

    new_bullets = []
    for k in bullets:
        rad = math.radians(k[3])
        k[0] += bullet_speed * math.cos(rad)
        k[1] += bullet_speed * math.sin(rad)
        if abs(k[0]) > GRID_LENGTH or abs(k[1]) > GRID_LENGTH:
            bullets_missed += 1
        else:
            new_bullets.append(k)
    bullets = new_bullets

    for l in enemies:
        dx = player_pos[0] - l[0]
        dy = player_pos[1] - l[1]
        dist = math.sqrt(dx**2 + dy**2)
        if dist > 0:
            l[0] += enemy_speed * dx / dist
            l[1] += enemy_speed * dy / dist
       
        l[3] += enemy_scale_speed
        if l[3] > enemy_scale_max:
            l[3] = enemy_scale_min
        
        if math.sqrt((l[0] - player_pos[0])**2 + (l[1] - player_pos[1])**2) < 35:
            life -= 1
            l[0] = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            l[1] = random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            l[3] = random.uniform(enemy_scale_min, enemy_scale_max)
 
    new_enemies = enemies.copy()
    for k in bullets:
        for l in enemies:
            if math.sqrt((k[0] - l[0])**2 + (k[1] - l[1])**2) < 25 * l[3]:
                score += 1
                new_enemies.remove(l)
                new_enemies.append([random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50),
                                    random.uniform(-GRID_LENGTH + 50, GRID_LENGTH - 50),
                                    10, random.uniform(enemy_scale_min, enemy_scale_max)])
                bullets.remove(k)
                break
    enemies = new_enemies
  
    if life <= 0 or bullets_missed >= 10:
        game_over = True


def idle():
    if not game_over:
        main_game()
    glutPostRedisplay()


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity() 
    glViewport(0, 0, 1000, 800) 
    setupCamera()
    draw_grid()
    draw_player()
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1], enemy[2], enemy[3])
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])
    draw_text(10, 770, f"Player Life Remaining: {life}")
    draw_text(10, 740, f"Game Score: {score}")
    draw_text(10, 710, f"Player Bullet Missed: {bullets_missed}")
    if game_over:
        draw_text(400, 400, "Game Over! Press R to Restart")
    glutSwapBuffers()


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  
    glutInitWindowSize(W_Width, W_Height)  
    glutInitWindowPosition(0, 0)  
    wind = glutCreateWindow(b"3D GAME!")
    glEnable(GL_DEPTH_TEST)  
    init_enemies()  
    glutDisplayFunc(showScreen)  
    glutKeyboardFunc(keyboardListener) 
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle) 
    glutMainLoop()  

if __name__ == "__main__":
    main()
