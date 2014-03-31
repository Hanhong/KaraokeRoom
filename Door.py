import sys
from TW import *

##===================================================

#textureIDs = None

##===================================================

def polygon(vertices, a, b, c, d):
    '''Draw one part of the door, given vertex indices.
    Vertex a is the upper left which corresponds to the upper left of the texture, and then go counterclockwise.
    '''
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex3fv(vertices[a])
    glTexCoord2f(0,1)
    glVertex3fv(vertices[b])
    glTexCoord2f(1,1)
    glVertex3fv(vertices[c])
    glTexCoord2f(1,0)
    glVertex3fv(vertices[d])
    glEnd()

##=============INNER================================= 

def face(doorWidth, doorHeight,
         sunkenWidth, sunkenHeight, sunkenDepth,
         doorSide1, doorSide2, textureIDs):
    ''' Draw one side of the doorWidth*doorHeight rectangular door 
    with a sunkenWidth*sunkenHeight*sunkenDepth sunken in the center'''
    doorV1 = ( (0,0,0), (0,doorHeight,0), 
               (-doorWidth,doorHeight,0), (-doorWidth,0,0),
               (-doorSide1,doorSide2,0), (-doorSide1,doorSide2+sunkenHeight,0), 
               (-(doorSide1+sunkenWidth),doorSide2+sunkenHeight,0), (-(doorSide1+sunkenWidth),doorSide2,0),
               (-doorSide1,doorSide2,-sunkenDepth), (-doorSide1,doorSide2+sunkenHeight,-sunkenDepth), 
               (-(doorSide1+sunkenWidth),doorSide2+sunkenHeight,-sunkenDepth), (-(doorSide1+sunkenWidth),doorSide2,-sunkenDepth) )
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,0,1)
    polygon(doorV1,7,3,0,4)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,0,1)
    polygon(doorV1,5,4,0,1)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,0,1)
    polygon(doorV1,2,6,5,1)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,0,1)
    polygon(doorV1,2,3,7,6) # door surface
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[1]))
    glNormal3f(0,0,1)
    polygon(doorV1,10,11,8,9) # different texture for sunken
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,1,0)
    polygon(doorV1,7,4,8,11)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(-1,0,0)
    polygon(doorV1,9,8,4,5)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,-1,0)
    polygon(doorV1,10,9,5,6)
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(1,0,0)
    polygon(doorV1,6,7,11,10) # surfaces connecting door and sunken surfaces   

def handle(color, handleRadius, handleDepth, handleWidth, handleSide):
    '''Draw the handle which is consist of a cylinder and a cuboid'''
    twColor(color,0,0.9)
    glPushMatrix()
    twCylinder(handleRadius, handleRadius, handleDepth, 20,1)
    glPopMatrix() #cylinder
    glPushMatrix()
    glTranslatef((handleWidth-0.6)/2,0,handleDepth) # '-0.6' to make it look better
    glScalef(handleWidth,handleSide,handleSide)
    glutSolidCube(1)
    glPopMatrix() #cuboid

def drawInnerDoor(doorWidth, doorHeight, doorDepth,
                  sunkenWidth, sunkenHeight, sunkenDepth,
                  doorSide1, doorSide2,
                  color, handleRadius, handleDepth, handleWidth, handleSide,
                  textureIDs):
    '''Draw the doorWidth*doorHeight*doorDepth door. The origin is at the right front vertex.
    There is a sunkenWidth*sunkenHeight*sunkenDepth sunken in the center on each side.
    The door is wooden texture, and the sunken is metal texture'''

    # draw the front and back face of the door
    face(doorWidth,doorHeight,
         sunkenWidth,sunkenHeight,sunkenDepth,
         doorSide1,doorSide2,textureIDs)
    glPushMatrix()
    glTranslatef(-doorWidth,0,-doorDepth) # the back face is 3 units away in z-axis
    glRotatef(180,0,1,0)
    face(doorWidth,doorHeight,
         sunkenWidth,sunkenHeight,sunkenDepth,
         doorSide1,doorSide2,textureIDs)
    glPopMatrix()

    # draw left, right, top, bottom faces which connect the front and back faces
    doorV2 = ( (0,0,0), (0,doorHeight,0), 
               (-doorWidth,doorHeight,0), (-doorWidth,0,0),
               (0,0,-doorDepth), (0,doorHeight,-doorDepth), 
               (-doorWidth,doorHeight,-doorDepth), (-doorWidth,0,-doorDepth) )
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(-1,0,0)
    polygon(doorV2,6,7,3,2) # left
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(1,0,0)
    polygon(doorV2,1,0,4,5) # right
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,1,0)
    polygon(doorV2,6,2,1,5) # top
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[0]))
    glNormal3f(0,-1,0)
    polygon(doorV2,7,3,0,4) # bottom
    
    # add door handle
    # don't use texture for the handle
    glPopAttrib()
    glPushMatrix()
    glTranslate((doorSide1/2)-doorWidth,doorHeight/2,0)
    handle(color,handleRadius,handleDepth,handleWidth,handleSide)
    glPopMatrix()
    # use texture after adding the handle
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_TEXTURE_2D)

def semicircle(doorWidth, archHeight):
    '''One side of the semi-circle part on top of the door.
    Use rock texture.'''
    control_points = (
        ((0,0,0),
         (doorWidth/2,archHeight*2,0),
         (doorWidth,0,0)),
        ((0,0,0),
         (doorWidth/2,0,0),
         (doorWidth,0,0)))
    twDrawBezierSurface(control_points,2,20)
    
def dec(color, doorWidth, doorDepth, archHeight):
    '''Draw the semi-circle structure on top of the door.
    Don't use texture, use RGB color'''
    twColor(color,0,0)
    # draw the front semi-circle
    semicircle(doorWidth,archHeight)
    # the back is 3 units away in z-axis
    glPushMatrix()
    glTranslatef(0,0,-doorDepth)
    semicircle(doorWidth,archHeight)
    glPopMatrix()
    # draw the base which is a doorWidth*doorDepth quad
    glBegin(GL_QUADS)
    glVertex3fv((0,0,0))
    glVertex3fv((doorWidth,0,0))
    glVertex3fv((doorWidth,0,-doorDepth))
    glVertex3fv((0,0,-doorDepth))
    glEnd()

##=============OUTER================================= 
def arch(doorWidth, archHeight, wallDepth, textureIDs):
    '''Draw the doorWidth*archHeight*wallDepth arch which is around the semi-circle derection on top of the door.
    Use rock texture.'''
    control_points = (
        ((0,0,0),
         (0,0,-wallDepth)),
        ((doorWidth/2,archHeight*2,0),
         (doorWidth/2,archHeight*2,-wallDepth)),
        ((doorWidth,0,0),
         (doorWidth,0,-wallDepth)))
    tcp = (((0,1),
            (0,0)),
           ((1,1),
            (1,0)))
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[2]))
    twDrawBezierSurfaceTextured(control_points,tcp,20,20,GL_FILL)

def oneSideWall(wallWidth, wallHeight, wallSide,
                doorWidth, doorHeight, archHeight,
                textureIDs):
    '''Draw one side of the outer wall.
    This consists of two wallSide*wallHeight quads
    connected by a bridge-like surface which is doorWidth*(wallHeight-doorHeight).
    Use rock texture.'''
    # first draw two quads
    wallV1 = ( (0,0,0), (wallSide,0,0), 
               (wallSide,wallHeight,0), (0,wallHeight,0),
               (wallSide+doorWidth,0,0), (wallWidth,0,0), 
               (wallWidth,wallHeight,0), (wallSide+doorWidth,wallHeight,0) )
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(0,0,1)
    polygon(wallV1,3,0,1,2)
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(0,0,1)
    polygon(wallV1,7,4,5,6)
    # then draw the part connecting two quads
    glPushMatrix()
    glTranslate(wallSide,doorHeight,0)
    control_points = (
        ((0,wallHeight-doorHeight,0),
         (doorWidth/2,wallHeight-doorHeight,0),
         (doorWidth,wallHeight-doorHeight,0)),
        ((0,0,0),
         (doorWidth/2,archHeight*2,0),
         (doorWidth,0,0)))
    tcp = (((0,1),
            (0,0)),
           ((1,1),
            (1,0)))
    glBindTexture(GL_TEXTURE_2D,int(textureIDs[2]))
    twDrawBezierSurfaceTextured(control_points,tcp,2,20,GL_FILL)
    glPopMatrix()
   
def wall(wallWidth, wallHeight, wallDepth, wallSide,
         doorWidth, doorHeight, archHeight, textureIDs):
    '''Draw the entire wallWidth*wallHeight*wallDepth outer wall.
    Use rock texture.'''
    oneSideWall(wallWidth,wallHeight,wallSide,
                doorWidth,doorHeight,archHeight,textureIDs)
    # draw back wall which is wallDepth away from the front wall in z-axis
    glPushMatrix()
    glTranslatef(0,0,-wallDepth)
    oneSideWall(wallWidth,wallHeight,wallSide,
                doorWidth,doorHeight,archHeight,textureIDs)
    glPopMatrix()
    # draw the arch
    glPushMatrix()
    glTranslatef(wallSide,doorHeight,0)
    arch(doorWidth,archHeight,wallDepth,textureIDs)
    glPopMatrix()
    # draw faces to connect front wall, back wall, and the arch
    wallV2 = [ [0,0,0], [wallWidth,0,0], 
               [wallWidth,wallHeight,0], [0,wallHeight,0],
               [wallSide,0,0], [wallSide+doorWidth,0,0], 
               [wallSide+doorWidth,doorHeight,0], [wallSide,doorHeight,0] ]
    wallV2back = [[v[0],v[1],-10] for v in wallV2]
    wallV2.extend(wallV2back)
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(-1,0,0)
    polygon(wallV2,11,8,0,3) #left wall
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(0,1,0)
    polygon(wallV2,11,3,2,10) #top wall
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(1,0,0)
    polygon(wallV2,2,1,9,10) #right wall
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(0,-1,0)
    polygon(wallV2,8,0,4,12)
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(0,-1,0)
    polygon(wallV2,13,5,1,9) #bottom walls
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(1,0,0)
    polygon(wallV2,7,4,12,15) #inner left wall
    glBindTexture(GL_TEXTURE_2D, int(textureIDs[2]))
    glNormal3f(-1,0,0)
    polygon(wallV2,6,5,13,14) #inner right wall

##=================================================== 
'''
def init():
    ''Initial three textures''
    global textureIDs
    textureIDs = glGenTextures(3) # get all the texture ids
    
    twLoadTexture(textureIDs[0],twPathname("wood256.ppm"))
    twLoadTexture(textureIDs[1],twPathname("metal256.ppm"))
    twLoadTexture(textureIDs[2],twPathname("rock256.ppm"))
   ''' 
##=================================================== 

def draw(openDegree,textureIDs):
    '''Draw the object. Input 'openDegree' determines how the door is opened.'''
    ##-----------------------------
    ## Set constants and variables
    goldenrod = (0.85,0.65,0.13)
    darkSlateGray = (0.18,0.31,0.31)
    
    doorWidth = 15
    doorHeight = 20
    doorDepth = 3
    
    sunkenWidth = 7
    sunkenHeight = 10
    sunkenDepth = 1
    doorSide1 = (doorWidth-sunkenWidth)/2 # distance between left/right surface of the door and left/right surface of the sunken
    doorSide2 = (doorHeight-sunkenHeight)/2 # distance between top/bottom surface of the door and top/bottom surface of the sunken
    
    wallWidth = 30
    wallHeight = 30
    wallDepth = 10
    wallSide = (wallWidth-doorWidth)/2 # distance between left/right surface of the wall and left/right surface of the door
    
    archHeight = 7.5
    
    lightRadius = 1
    
    handleRadius = 0.4
    handleDepth = 1
    handleWidth = 2.2
    handleSide = handleRadius*2

    lightPos1 = (wallWidth/2, doorHeight+archHeight, (doorDepth-wallDepth)/2, 1)
    lightPos2 = (wallWidth+5, wallHeight+5, 0, 0)
    ##-----------------------------

    # set the lighting
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    twGraySpotlight(GL_LIGHT1, lightPos1, 
                    0.5,0.7,0.7,
                    (0,-1,0),
                    15, # cut-off angle
                    5) # spot light fron the center of the arch
    twGrayLight(GL_LIGHT0, lightPos2, 0.3, 0.6, 0.3) # light from the right
    
    # Draw door and wall
    # from here use textures
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
    
    twColorName(TW_SILVER)
    glPushMatrix()
    glTranslatef(wallSide+doorWidth, 0, doorDepth-wallDepth)
    glRotatef(openDegree,0,1,0) # the door is opened by given degree
    drawInnerDoor(doorWidth,doorHeight,doorDepth,
                  sunkenWidth,sunkenHeight,sunkenDepth,
                  doorSide1,doorSide2,
                  goldenrod,handleRadius,handleDepth,handleWidth,handleSide,
                  textureIDs)
    glPopMatrix() # draw the door
    twColorName(TW_WHITE) 
    wall(wallWidth,wallHeight,wallDepth,wallSide,
         doorWidth,doorHeight,archHeight,textureIDs) # draw the wall
    glPopAttrib() # from here, stop using texture

    # add a light to the center of the arch
    twColorName(TW_YELLOW)
    glPushMatrix()
    glTranslate(wallWidth/2, doorHeight+archHeight, (doorDepth-wallDepth)/2)
    glutSolidSphere(lightRadius,10,10)
    glPopMatrix()
    # add the semi-circle decoration on top of the door
    glPushMatrix()
    glTranslatef(wallSide,doorHeight,doorDepth-wallDepth)
    dec(darkSlateGray,doorWidth,doorDepth,archHeight)
    glPopMatrix()
