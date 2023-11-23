import pygame, time, os, sys

# The Game (I think we lost) -----------------------------------------------------------------------------#
pygame.init() # chewsday init
pygame.font.init() 

# Create window and set screen size - TODO: Make resizable
# 0,0 is top left so the y axis is down the screen.
DISPLAYWIDTH = 1000
DISPLAYHEIGHT = 500

window = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))

# Set Icon
# Thanks to Andre Caron on stackover flow. 
# I guess this is how you always get the path next to the python File
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
pygame.display.set_icon(pygame.image.load(os.path.join(__location__,'pythonStar.png')))

# Set Title
pygame.display.set_caption("Final Project Game Title Here")


# Variables ----------------------------------------------------------------------------------------------#
# CONSTANTS
# COLORS - rgb format
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKPURPLE = (128, 0, 128) # For player, but an option to customize shouldn't be hard

# WINDOW POSITIONS
# Remember rectangle positions use the top left corner 
# so if you use a right or bottom position it will be off screen
# SIDES
WINDOWTOP = 0 # this is just for continuity
WINDOWLEFT = 0
WINDOWRIGHT = pygame.display.get_window_size()[0]
WINDOWBOTTOM = pygame.display.get_window_size()[1]

# COORDINATE PAIRS!
WINDOWTOPLEFT = [0, 0] # this is just for continuity
WINDOWTOPCENTER = [(pygame.display.get_window_size()[0] / 2), 0]
WINDOWTOPRIGHT = [pygame.display.get_window_size()[0], 0] # Try subtracting object width from WINDOWTOPRIGHT[0]
WINDOWCENTERLEFT = [0, (pygame.display.get_window_size()[1] / 2)]
WINDOWCENTER = [(pygame.display.get_window_size()[0] / 2), (pygame.display.get_window_size()[1] / 2)]
WINDOWCENTERRIGHT = [pygame.display.get_window_size()[0], (pygame.display.get_window_size()[1] / 2)]
WINDOWBOTTOMLEFT = [0, pygame.display.get_window_size()[1]] # Subtract object height from WINDOWBOTTOMLEFT[1]
WINDOWBOTTOMCENTER = [(pygame.display.get_window_size()[0] / 2), pygame.display.get_window_size()[1]]
WINDOWBOTTOMRIGHT = [pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]] # Do both!

# Time
clock = pygame.time.Clock()
desktopRefreshRate = pygame.display.get_current_refresh_rate()

# Player variables
playerStartPosition = WINDOWCENTER # (X, Y)
playerSpeed = 250 # pixels per loop but this will be multiplied by deltaTime so idk what it works out to
jumpStrength = 20 # idk about this one chief
playerSize = [10, 10] # (X, Y)
playerColor = DARKPURPLE # rgb format
deltaTime = clock.tick(desktopRefreshRate) / 1000

# Platform variables
platformSize = [50, 10] # (X, Y)
platformPosition = (WINDOWBOTTOMCENTER[0], WINDOWBOTTOMCENTER[1] - platformSize[1]) # (X, Y)
platformColor = RED # rgb format

# Needs orginizing
gravityStrength = 500


# Objects ------------------------------------------------------------------------------------------------#
class Player:
    def __init__(self, startPosition, playerSize, playerColor, playerSpeed, jumpStrength): 
        # Player position is just a tuple for x y
        self.position = startPosition
        self.size = playerSize
        self.color = playerColor
        self.speed = playerSpeed
        self.jumpStrength = jumpStrength
        self.jumpVelocity = jumpStrength
        self.isJumping = False
        self.rectangle = pygame.Rect(self.position, self.size) # (X,Y), (WIDTH,HIEGHT)

    def jump(self):
        if not self.isJumping:
            self.isJumping = True
            self.jumpVelocity = self.jumpStrength

        if self.isJumping:
            self.position[1] -= self.jumpVelocity
            self.jumpVelocity -= 1

            if (self.position[1] + self.size[1]) >= WINDOWBOTTOM:
                self.isJumping = False
                self.jumpVelocity = self.jumpStrength



    def draw(self):
        self.rectangle.update(self.position, self.size)
        pygame.draw.rect(window, self.color, self.rectangle)


class Platform:
    def __init__(self, platformPosition, platformSize, platformColor):
        self.position = platformPosition
        self.size = platformSize
        self.color = platformColor
        
    def draw(self):
        # rect using top left for x,y and then width height
        pygame.draw.rect(window, self.color, (self.position, self.size)) # (X,Y), (WIDTH,HIEGHT)
        


# Initialize objects -------------------------------------------------------------------------------------#
player1 = Player(playerStartPosition, playerSize, playerColor, playerSpeed, jumpStrength)
platform1 = Platform(platformPosition, platformSize, platformColor)

platformList = [platform1]


#  Funk(tions) -------------------------------------------------------------------------------------------#
def playerInput(): # Gets player input then does something
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player1.jump()
        #player1.position[1] -= player1.speed * deltaTime # y axis upside down so these are inverted

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player1.position[1] += player1.speed * deltaTime # y axis upside down so these are inverted

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player1.position[0] -= player1.speed * deltaTime

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player1.position[0] += player1.speed * deltaTime

def gravity(player, gravityStrength): # Pulls player down
        # stops player from going below screen, this is temporary since collision is a thing
        if player.position[1] < (pygame.display.get_window_size()[1] - player.size[1]):
            player.position[1] += gravityStrength * deltaTime

def drawFrameRate(): # counts the frames per second
    # Text for fps values --------------------------------------------------------------------------------#
    averageFPS = str(round(clock.get_fps(), 2)) # get_fps averages the last 10 calls to clock.tick

    # Set Font - again grabbing it with the weird method, but it works so well.
    font = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), 20)
    fpsText = font.render(f"FPS: {averageFPS}", False, WHITE) 

    # blit draws the image.
    window.blit(fpsText, (5,0)) # 5 is the pixel border

def drawThings():
    # Draw things. Order matters, things drawn last get put on top
    # This is the only way to layer things that I know of
    player1.draw()

    platform1.draw()

    # UI should go below this so objects don't obscure the view
    drawFrameRate()

def collision():
    player1.draw
# Stuff that should be called once before the game starts can go here ------------------------------------#


# Main Loop ----------------------------------------------------------------------------------------------#
while True:
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Wipe screen every frame so things don't overlap
    window.fill(BLACK)

    # Funk(tions) ----------------------------------------------------------------------------------------#
    playerInput()
    gravity(player1, gravityStrength)

    # This should be at the bottom but before the screen update. I think.
    drawThings()

    # Updates window -------------------------------------------------------------------------------------#
    pygame.display.flip()

    # Frame rate independence ----------------------------------------------------------------------------#
    # Limit frame rate to desktop refresh rate, pretty sure clock.tick just waits to slow down the loop
    deltaTime = clock.tick(desktopRefreshRate) / 1000
    
    # Testing --------------------------------------------------------------------------------------------#
    # print(deltaTime)
    # print(desktopRefreshRate)