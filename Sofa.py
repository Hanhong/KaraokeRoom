import sys
from TW import *

'''
This program creates a sofa by given width (number of cushions).
'''

def surface():
    '''Draws a triangular surface, but the center is arched.'''
    control_points = (
        ((0,0,0),
         (0,0,0),
         (0,0,0),
         (0,0,0)),
        ((2.5,0,2.5),
         (2.5,2.5,1.2),
         (2.5,2.5,-1.2),
         (2.5,0,-2.5)),
        ((5,0,5),
         (5,0,2.5),
         (5,0,-2.5),
         (5,0,-5)))
    twDrawBezierSurface(control_points,20,20)

def cushion():
    '''Draws the cushion of the sofa, which consists of four arched triangular surfaces.
    Each of the four arched surfaces has a different color.
    There is a white button in the center, which is also the origin.'''
    twColor((1,0,1),1,1)
    surface() # first arched surface
    twColor((0,0,1),1,1)
    glPushMatrix()
    glRotatef(90,0,1,0)
    surface() # second arched surface
    twColor((0,1,0),1,1)
    glRotatef(90,0,1,0)
    surface() # third arched surface
    twColor((1,0,0),1,1)
    glRotatef(90,0,1,0)
    surface() # fourth arched surface
    glPopMatrix()
    twColor((1,1,1),1,1)
    glutSolidSphere(0.5,20,20) # white button

def texQuad():
    '''Draws a textured quad.'''
    #twPPM_Tex2D(twPathname("sofa.ppm",False))
    glBegin(GL_QUADS)
    glTexCoord2f(0,0); glVertex3f(0,1,0)
    glTexCoord2f(0,1); glVertex3f(0,0,0)
    glTexCoord2f(1,1); glVertex3f(1,0,0)
    glTexCoord2f(1,0); glVertex3f(1,1,0)
    glEnd()

def texCube(textureIDs):
    '''Draws a textured unit cube. Use the sofa texture.
    Will be used as the handles, the base, and the back of the sofa'''
    twColor((0.41,0.41,0.41),1,0.7) # dim gray. make the texture darker
    ## front
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(0,0,1)
    texQuad()
    ## back
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(0,0,-1)
    glPushMatrix()
    glTranslate(0,0,-1)
    texQuad()
    glPopMatrix()
    ## left
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(-1,0,0)
    glPushMatrix()
    glRotate(90,0,1,0)
    texQuad()
    ## right
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(0,0,1)
    glTranslate(0,0,1)
    texQuad()
    glPopMatrix()
    ## bottom
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(0,-1,0)
    glPushMatrix()
    glRotate(-90,1,0,0)
    texQuad()
    ## top
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[3]))
    glNormal3f(0,0,1)
    glTranslate(0,0,1)
    texQuad()
    glPopMatrix()

#numCushion = 2
#cushionLength = 10*numCushion

def draw(numCushion,textureIDs):
    '''Draw the sofa. 
    The given numCushion determines the length of the sofa, i.e., if numCushion is 1, then the sofa has one cushion; if numCushion is 2, then the sofa has two cushions.  
    The origin is the left front corner of the sofa.'''
    cushionLength = 10*numCushion
    
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    
    glPushMatrix()
    glScale(2,8,10)
    texCube(textureIDs) # draw the left handle
    glTranslate((2+cushionLength)/2,0,0) # divided by 2 because we changed x-axis in glScale
    texCube(textureIDs) # draw the right handle
    glPopMatrix()
    glPushMatrix()
    glTranslate(-8,0,0) # move to a point so that we can use the for loop to draw the cushions and the bases
    for i in range(numCushion):
        glTranslate(15,5,-5)
        glDisable(GL_TEXTURE_2D) # don't use texture for the cushion
        cushion()
        glEnable(GL_TEXTURE_2D)
        glTranslate(-5,-5,5)
        glPushMatrix()
        glScale(10,5,10)
        texCube(textureIDs)
        glPopMatrix() # only change the scale while drawing the base
    glPopMatrix() # draw the cushion and the base under it
    glPushMatrix()
    glTranslate(0,0,-10)
    glScale(4+cushionLength,10,2)
    texCube(textureIDs)
    glPopMatrix() # draw the back
    
    glPopAttrib() # from here, stop using texture

''' TEST
def display():
    twDisplayInit()
    twCamera()
    
    glEnable(GL_TEXTURE_2D)
    
    draw()
    #texCube()
    
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(0,4+cushionLength,0,10,-12,0)
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
'''
