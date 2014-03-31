''' 
CS307 Final Project Version 1
Hanhong Lu
5/2/2012

This program creates an animation of a karaoke room. The camera starts at the right upper, moves towards the door, and enters the room. There are a tv, a cabinet, and some sofas. Two spotlights flashes inside the room.
'''

import sys
from TW import *

import Door
import Sofa
import TV

##===================================================

openDegree = 0
textureIDs = None
numCushion1 = 4
numCushion2 = 2
screenId = 1
Time = 0
DeltaT = 1

##===================================================
SaveFrames = False
FrameNumber = 1
FrameFileTemplate = "/tmp/hluFinal/Karaoke%03d.ppm"

def saveFrame():
    global FrameNumber, SaveFrames
    if not SaveFrames:
        return
    file = FrameFileTemplate % (FrameNumber)
    FrameNumber += 1
    if FrameNumber > 999:
        print "Sorry, this program assumes 3 digit numbers.  Please update it"
        sys.exit(1)
    glFlush()
    twSaveFrame(file, False)

##===================================================
## Some helper methods
def quad(color, position, r_angle, r_axis, length, width):
    '''Draws a length*width rectangle of given color on x=0 plane,
    and then rotate it by given angle and coordinate'''
    twColor(color,0.1,2)
    glPushMatrix()
    glTranslate(*position)
    glRotate(r_angle,*r_axis)
    glScale(length,1,width)
    twDrawUnitSquare(200,200)
    glPopMatrix()

def texWall(texInt,position, r_angle, r_axis, length, width):
    '''Draws a wall with the given texture.'''
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[texInt]))
    glPushMatrix()
    glTranslate(*position)
    glRotate(r_angle,*r_axis)
    glScale(length,width,1)
    Sofa.texQuad() # the the texQuad method in Sofa.py
    glPopMatrix()

def furnitures():
    '''Places two sofas and a tv with a cabinet in the room'''
    ## place the first sofa, which has 4 cushions
    glPushMatrix()
    glTranslate(75,0,-23)
    glRotate(180,0,1,0)
    Sofa.draw(numCushion1,textureIDs)
    glPopMatrix()
    ## place the second sofa, which has 3 cushions
    glPushMatrix()
    glTranslate(25,0,-25)
    glRotate(90,0,1,0)
    Sofa.draw(numCushion2,textureIDs)
    glPopMatrix()
    ## place the cabinet and the tv
    glPushMatrix()
    glTranslate(35,0,-40)
    # use screenId+6 
    # since there are 6 other textures before screen textures
    TV.draw(textureIDs,screenId+6)
    glPopMatrix()

def walls():
    '''Draws the wall. The front wall has the karaoke signs.'''
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_TEXTURE_2D)
    
    # front wall. Needs two quads 
    # because there is no wall where the door is drawn
    glNormal3f(0,0,1)
    texWall(4,(30,0,-10),0,(1,0,0),50,50)
    glNormal3f(0,0,1)
    texWall(5,(0,30,-10),0,(1,0,0),30,20)
    # left
    glNormal3f(-1,0,0)
    texWall(6,(0,0,-10),90,(0,1,0),50,50)
    # right
    glNormal3f(1,0,0)
    texWall(6,(80,0,-10),90,(0,1,0),50,50)
    # back
    glNormal3f(0,0,1)
    texWall(6,(0,0,-60),0,(1,0,0),80,50)
    glPopAttrib()

def init():
    '''Initial three textures for Door'''
    global textureIDs
    textureIDs = glGenTextures(13) # get all the texture ids
    
    twLoadTexture(textureIDs[0],twPathname("wood256.ppm"))
    twLoadTexture(textureIDs[1],twPathname("metal256.ppm"))
    twLoadTexture(textureIDs[2],twPathname("rock256.ppm"))
    twLoadTexture(textureIDs[3],twPathname("sofa.ppm"))
    twLoadTexture(textureIDs[4],twPathname("karaokeSign.ppm"))
    twLoadTexture(textureIDs[5],twPathname("karaoke.ppm"))
    twLoadTexture(textureIDs[6],twPathname("wall.ppm"))
    twLoadTexture(textureIDs[7],twPathname("screen1.ppm"))
    twLoadTexture(textureIDs[8],twPathname("screen2.ppm"))
    twLoadTexture(textureIDs[9],twPathname("screen3.ppm"))
    twLoadTexture(textureIDs[10],twPathname("screen4.ppm"))
    twLoadTexture(textureIDs[11],twPathname("screen5.ppm"))
    twLoadTexture(textureIDs[12],twPathname("screen6.ppm"))

##===================================================
## Draw the scene

# Initial values for arguments in lookAt
eye_x = 0
eye_y = 40
eye_z = 50 # the camera starts at upper left
at_x = 15
at_y = 10
at_z = -30 # the camera initially looks at the center behind the door

# Initial light directions and status for the two spotlights
lightDirection0 = [(-0.2,-1,0),(0,-1,-0.3)]
lightDirection1 = [(0.3,-1,0.2),(-0.3,-1,0.2)]
directionId = 0
Light1 = True
Light2 = True # the two spotlights are initially turned on

def myCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90,1,5,200)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x,eye_y,eye_z,at_x,at_y,at_z,0,1,0)

def display():
    twDisplayInit()
    myCamera() # set my own camera

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    
    ## set a light from upper light
    lightPos0 = (-10,70,-10,0)
    twGrayLight(GL_LIGHT0,lightPos0,0.3,0.6,0.6)
    
    ## set karaoke's two flashlights which share the same position
    lightPos1 = (40,50,-35,1)
    twGraySpotlight(GL_LIGHT1,lightPos1,0.7,1,0.9,
                    lightDirection0[directionId],
                    15,
                    5)
    twGraySpotlight(GL_LIGHT2,lightPos1,1,1,0.8,
                    lightDirection1[directionId],
                    12,
                    5)
    if not Light1:
        glDisable(GL_LIGHT1)
    if not Light2: # if Light1 and Light2 are false, turn off the light
        glDisable(GL_LIGHT2) 
    
    ## draw the ceiling and the floor
    floor = (0.18,0.31,0.31) #dark slate gray
    ceiling = (0.94,0.97,1) #alice blue
    quad(floor,(-10,0,-70),0,(1,0,0),100,80) #floor
    quad(ceiling,(0,50,-60),0,(1,0,0),80,50) #ceiling
    
    ## draw the walls. The front wall has the karaoke sign. 
    ## Use wall texture
    walls()
    
    ## draw the door
    Door.draw(openDegree,textureIDs)
    
    ## place the furnitures
    furnitures()

    glFlush()
    glutSwapBuffers()

    if SaveFrames:
        saveFrame()

##===================================================
## Animate the scene and set keyboard callbacks

Animating = False

def keys(key,x,y):
    global Time,Animating,openDegree,eye_x,eye_y,eye_z,at_x,SaveFrames
    if key == '0':
        # if press '0', reset the animation
        Animating = False
        Time = 0
        openDegree = 0
        eye_x = 0
        eye_y = 40
        eye_z = 50
        at_x = 15
        glutPostRedisplay()
    elif key == '1':
        # if press '1', open the door, 
        # directly set the camera inside of the room 
        # and look at the center of the room
        openDegree = 90
        eye_x = 12
        eye_y = 16
        eye_z = -11
        at_x = 30
        glutPostRedisplay()
    elif key == 'a':
        # if press 'a', start animation if it was not animating;
        # stop animation if it was animating
        Animating = not Animating
        print "start animation"
        glutIdleFunc(update if Animating else None)
    elif key == 's':
        SaveFrames = not SaveFrames
        print "the program %s save frames in %s" % (
            "will" if SaveFrames else "won't",
            FrameFileTemplate )

def update():
    '''idle callback for animation'''
    global Time, openDegree, eye_x, eye_y, eye_z, at_x
    global directionId, Light1, Light2
    Time += DeltaT # update time
    openDoor()
    if openDegree > 60:
        moveCamera()
    updateScreen() # tv screen
    flash() # flashlight effect
    glutPostRedisplay()

def openDoor():
    '''Opens the door 1 degrees per second until it is fully opened.'''
    global openDegree
    if openDegree < 90:
        openDegree += 1

def moveCamera():
    '''Moves the camera 1 unit along the axises each time, 
    until it's inside the room.
    Then turn the camera rightwards 
    until it looks at the center of the room '''
    global eye_x, eye_y, eye_z, at_x
    if eye_x < 13:
        eye_x += 1
    if eye_y > 15:
        eye_y -= 1
    if eye_z > -12:
        eye_z -= 1
    elif at_x < 30:
        at_x += 1

def updateScreen():
    '''Changes to the next karaoke screenshot. 
    There are 6 screenshots in total. 
    Each screenshots holds for 3 seconds.'''
    global screenId
    if Time%3 == 1:
        if screenId != 6:
            screenId += 1
        else: # if it's the last screenshot, start from the first one
            screenId = 1 
    
def flash():
    '''Swith spotlights status every 4 second,
    (tried change status every second, 
    but was too fast after converting to a movie)
    and change their direction everytime ther are on
    For example:
    1~4 second: on, pointing towards direction 1
    5~8 second: off
    9~12 second: on, pointing towards direction 2
    13~16 second: off '''
    global directionId, Light1, Light2
    if Time%8 == 1:
        # when time is 1,9,17 etc, turn the spotlights on 
        # and hold for the next 4 seconds
        Light1 = True
        Light2 = True
        directionId = 1 - directionId # change the direction of the spotlights
    elif Time%8 == 5: 
        # when Time is 5,13,21 etc, turn the spotlights off
        # and hold for the next 4 seconds
        Light1 = False
        Light2 = False
            
##===================================================
## Run the program

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-10,90,0,50,-70,10)
    twInitWindowSize(700,700)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    init()
    twMainInit()
    # Keyboard Callbacks
    twKeyCallback('0',keys,"Reset Animation")
    twKeyCallback('1',keys,"Inside View")
    twKeyCallback('a',keys,"Toggle Animation") 
    twKeyCallback('s',keys,"Toggle Saving Frames")
    glutMainLoop()
    
if __name__ == '__main__':
    main()
