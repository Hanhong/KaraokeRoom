import sys
from TW import *

'''
This program createa a TV, and places it on a cabinet.
The TV is 10*10*5, and the cabinet is 20*10*10.
The origin is the front left corner of the cabinet.
'''

def screen(textureIDs,texInt):
    '''Textures the tv sreen, 
    so it looks like the tv is playing something'''
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL)
    
    #twPPM_Tex2D(twPathname("screen1.ppm",False))
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[texInt]))
    glNormal3f(0,0,1)
    glBegin(GL_QUADS)
    # since the tv screen is not a square, 
    # don't use (0,0),(0,1),(1,0),(1,1) which would stretch the texture
    glTexCoord2f(0.02,0.12); glVertex3f(0,1,0)
    glTexCoord2f(0.02,0.88); glVertex3f(0,0,0)
    glTexCoord2f(0.98,0.88); glVertex3f(1,0,0)
    glTexCoord2f(0.98,0.12); glVertex3f(1,1,0)
    glEnd()
    
    glPopAttrib()

def drawTV(textureIDs,texInt):
    '''Draws a TV which is 10*10*5. The origin is the center of the base.'''
    # base
    glPushMatrix()
    glTranslate(0,0.25,0)
    glScale(7,0.5,5)
    glutSolidCube(1)
    glPopMatrix()
    # the connection between the base and the tv
    glPushMatrix()
    glRotate(-90,1,0,0)
    twCylinder(0.5,0.5,2,20,20)
    glPopMatrix()
    # tv
    glPushMatrix()
    glTranslate(0,6,0)
    glScale(10,8,1)
    glutSolidCube(1)
    glPopMatrix()
    # screen
    glPushMatrix()
    glTranslate(-4.8,2.2,0.6)
    glScale(9.6,7.6,0)
    screen(textureIDs,texInt)
    glPopMatrix()

def drawCabinet():
    '''Draws a cabinet which is 20*10*10. There are two doors on the front.
    The origin is the left front corner.'''
    glPushMatrix()
    glTranslate(10,5,-5)
    glScale(20,10,10)
    glutSolidCube(1)
    glPopMatrix()
    # draw a line to seperate two doors
    twColor((0.83,0.83,0.83),1,1) #light gray
    glBegin(GL_LINES)
    glVertex3f(10,0,0)
    glVertex3f(10,10,0)
    glEnd()
    # draw two round door handles
    twColor((0.55,0,0),1,1) #dark red
    glPushMatrix()
    glTranslate(9,5,0)
    glutSolidSphere(0.5,20,20) # left handle
    glTranslate(2,0,0)
    glutSolidSphere(0.5,20,20) # right handle
    glPopMatrix()

def draw(textureIDs,texInt):
    # use chrome material for the tv
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.25,0.25,0.25))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.4,0.4,0.4))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.774597,0.774597,0.774597))
    glMaterialfv(GL_FRONT, GL_SHININESS, 76.8)
    glPushMatrix()
    glTranslate(10,10,-5) # place the tv on the cabinet
    drawTV(textureIDs,texInt)
    glPopMatrix()
    
    # use black plastic material for the cabinet
    glMaterialfv(GL_FRONT, GL_AMBIENT, (0.0,0.0,0.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.01,0.01,0.01))
    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.5,0.5,0.5))
    glMaterialfv(GL_FRONT, GL_SHININESS, 32)
    drawCabinet()
    
'''
def display():
    twDisplayInit()
    twCamera()
    
    draw()
    
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(0,20,0,20,-10,0)
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
'''
