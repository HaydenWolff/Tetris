#########################################
# Programmer: Hayden Wolff
# Date: 04/7/2019
# File Name: tetris_classes.py
#########################################
import pygame

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255)
#############################
# Declaration of the images #
#############################
REDI = pygame.image.load("Red-2-1-2.png")                    
GREENI = pygame.image.load("Green-2-1-2.png")                    
BLUEI = pygame.image.load("Blue-L.png")                      
ORANGEI = pygame.image.load("Orange-L.png")                
CYANI = pygame.image.load("Blue-Long.png")                 
MAGENTAI = pygame.image.load("Purple-T.png")                   
YELLOWI = pygame.image.load("Yellow-Square.png")
REDI = pygame.transform.scale(REDI,(25,25))
GREENI = pygame.transform.scale(GREENI,(25,25))
BLUEI = pygame.transform.scale(BLUEI,(25,25))
ORANGEI = pygame.transform.scale(ORANGEI,(25,25))
CYANI = pygame.transform.scale(CYANI,(25,25))
MAGENTAI = pygame.transform.scale(MAGENTAI,(25,25))
YELLOWI = pygame.transform.scale(YELLOWI,(25,25))

COLOURIMAGES = [BLACK, REDI, GREENI, BLUEI, ORANGEI, CYANI, MAGENTAI, YELLOWI]          # List for the images and their respected colours
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface, CLR,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)
        
    def drawImages(self,surface,gridsize=20):                           #  Draws the images instead of a colour block
        x = self.col * gridsize
        y = self.row * gridsize
        CLR = COLOURIMAGES[self.clr]
        surface.blit(CLR,(x,y))
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)
        
    def fill(self, surface, gridsize=20):                               # Draws the shadow to be the inverse of the shape colours 
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,BLACK,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface, CLR,(x,y,gridsize+1,gridsize+1), 1)

    def move_down(self):                
        self.row = self.row + 1   
               
#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo
        self._rowOffsets = [0]*blocksNo

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i]
            blockROW = self.row+self._rowOffsets[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)
            
    def drawImages(self, surface, gridsize):    # allows the command drawImages to be used in the template         
        for block in self.blocks:
            block.drawImages(surface, gridsize)
            
    def fill(self, surface, gridsize):          # allows the command fill to be used in the template         
        for block in self.blocks:
            block.fill(surface, gridsize)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
        for block in other.blocks:
            self.blocks.append(block)

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print (block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns-1:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
   
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1]
        self._rowOffsets = [-1,-1, 0, 0]
        self._rotate()
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]


    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [1, 1, 0, -1], [0, 0, 0, 1], [-1, 1, 0,-1]] #
            _rowOffsets = [[-1,-1, 0, 1], [-1, 0, 0, 0], [1,-1, 0, 1], [ 0, 0, 0, 1]] #
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() 

    def move_left(self):                
        self.col = self.col - 1                   
        self._update() 
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() 
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() 
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() 

    def rotateClkwise(self):
        self._rot = (self._rot + 1)%4
        self._rotate()

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1)%4
        self._rotate()
        
    def moveShadow(self,other,another,three):                            # Controls the movement of the shadow and makes sure there are no collisions
        self.row = three.row                                             # with other obstacles already on the board
        self._update()
        while not self.collides(other) and not self.collides(another):
            self.move_down()
        self.move_up()

#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i  
        self._update()        
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update() 
#---------------------------------------#
class Score(object):                                                     # Score class that is in charge of checking the score of the object
    def __init__(self,score,doubleTetris,level,delay):                   # and determining the levels and the speed of the game. Also in charge
        self._score = score                                              # of adding score based on what is scored, i.e Double Tetris = 1200 Points
        self._doubleTetris = doubleTetris
    def scoreSystem(self,other,sound1,sound2):
        if self._doubleTetris == True and len(other) == 4:
            sound2.play()
            self._score+=1200
            self.doubleTetris = False
        elif len(other) == 4:
            sound2.play()
            self._score+=800
            self._doubleTetris = True
        elif other:
            sound1.play()
            self._score+=100*len(other)
            self._doubleTetris = False
        return self._score
    def changeSpeed(self):
        if self._score < 500:
            self._level = 1
            self._delay = 100
        elif 500<=self._score<1000:
            self._level = 2
            self._delay = 75
        elif self._score >= 1000:
            self._level = 3
            self._delay = 50
        return self._level, self._delay
