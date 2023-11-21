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
# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKPURPLE = (128, 0, 128) # For player, but an option to customize shouldn't be hard

# WINDOW POSITIONS
# Remember most positions use the top left corner so if you use a right position it will be off screen
WINDOWTOPLEFT = [0, 0] # this is just for continuity
WINDOWTOPCENTER = [(pygame.display.get_window_size()[0] / 2), 0]
WINDOWTOPRIGHT = [pygame.display.get_window_size()[0], 0]
WINDOWCENTERLEFT = [0, (pygame.display.get_window_size()[1] / 2)]
WINDOWCENTER = [(pygame.display.get_window_size()[0] / 2), (pygame.display.get_window_size()[1] / 2)]
WINDOWCENTERRIGHT = [pygame.display.get_window_size()[0], (pygame.display.get_window_size()[1] / 2)]
WINDOWBOTTOMLEFT = [0, pygame.display.get_window_size()[1]]
WINDOWBOTTOMCENTER = [(pygame.display.get_window_size()[0] / 2), pygame.display.get_window_size()[1]]
WINDOWBOTTOMRIGHT = [pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]]

# Time
clock = pygame.time.Clock()
desktopRefreshRate = pygame.display.get_current_refresh_rate()

# Player variables
playerSpeed = 250
playerRadius = 50
playerColor = DARKPURPLE # rgb format
deltaTime = clock.tick(desktopRefreshRate) / 1000


# Objects ------------------------------------------------------------------------------------------------#
class Player:
    def __init__(self, playerRadius, playerColor, speed): 
        # Player position is just a tuple for x y
        self.playerPosition = WINDOWCENTER
        self.playerRadius = playerRadius
        self.playerColor = playerColor
        self.speed = speed
   
    def draw(self):
        pygame.draw.circle(window, self.playerColor, self.playerPosition, self.playerRadius)


class Platform:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color
        pass
    def draw(self):
        # rect using top left for x,y and then width height
        pygame.draw.rect(window, self.color, (self.position, self.size)) # ((X,Y),(WIDTH,HIEGHT))
        pass


# Initialize objects -------------------------------------------------------------------------------------#
player1 = Player(playerRadius, playerColor, playerSpeed)
platform1 = Platform((WINDOWBOTTOMCENTER[0], WINDOWBOTTOMCENTER[1] - 10), (100, 10), DARKPURPLE)


#  Funk(tions) -------------------------------------------------------------------------------------------#
def playerInput(): # Gets player input then does something
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player1.playerPosition[1] -= player1.speed * deltaTime # y axis upside down so these are inverted

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player1.playerPosition[1] += player1.speed * deltaTime # y axis upside down so these are inverted

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player1.playerPosition[0] -= player1.speed * deltaTime

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player1.playerPosition[0] += player1.speed * deltaTime

def gravity(player, gravityStrength): # Pulls player down
        # stops player from going below screen, this is temporary since collision is a thing
        if player.playerPosition[1] < (pygame.display.get_window_size()[1] - player.playerRadius):
            player.playerPosition[1] += gravityStrength * deltaTime

def drawFrameRate():
    # Text for fps values --------------------------------------------------------------------------------#
    averageFPS = str(round(clock.get_fps(), 2)) # get_fps averages the last 10 calls to clock.tick

    # Set Font - again grabbing it with the weird method, but it works so well.
    font = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), 20)
    fpsText = font.render(f"FPS: {averageFPS}", False, WHITE) 

    # blit draws the image.
    window.blit(fpsText, (5,0))

def drawThings():
    # Draw things. Order matters, things drawn last get put on top
    # This is the only way to layer things that I know of
    player1.draw()

    platform1.draw()

    # UI should go below this so objects don't obscure the view
    drawFrameRate()


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
    gravity(player1, 25)

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