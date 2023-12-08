import pygame, time, os, sys

# The Game (I think we lost) -----------------------------------------------------------------------------#
pygame.init() # chewsday init
pygame.font.init() 

# Create window and set screen size 
# TODO: Make resizable, but also scale everything else? 
# Not hard but just because you can doesn't mean you should
# 0,0 is top left so the y axis is down the screen.
DISPLAYWIDTH = 700 # squares look best for background
DISPLAYHEIGHT = 700

window = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), pygame.RESIZABLE) # This does not stech objects and is currently useless

# Thanks to Andre Caron on stackoverflow. https://stackoverflow.com/a/4060259
# I guess this is how you always get the path next to the python File
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Set Icon
iconPath = os.path.join(__location__,'pythonStar.png')
pygame.display.set_icon(pygame.image.load(iconPath))

# Set Title
pygame.display.set_caption("Final Project Game Title Here")

# Set Background - scaled to window size
bg = pygame.image.load(os.path.join(__location__,'spaceBG.png'))
background = pygame.transform.scale(bg, pygame.display.get_window_size())


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
# Careful not to change these it can be easy to do that when refrencing them for positions.
# Remember rectangle positions use the top left corner 
# so if you use a right or bottom positions it will be off screen
# SIDES
WINDOWTOP = 0 # this is just for continuity
WINDOWLEFT = 0
WINDOWRIGHT = pygame.display.get_window_size()[0]
WINDOWBOTTOM = pygame.display.get_window_size()[1]
WINDOWCENTER = [(WINDOWRIGHT / 2), (WINDOWBOTTOM / 2)]

# COORDINATE PAIRS!
WINDOWTOPLEFT = [0, 0] # this is just for continuity
WINDOWTOPCENTER = [(WINDOWRIGHT / 2), 0]
WINDOWTOPRIGHT = [WINDOWRIGHT, 0] # Subtract object width from WINDOWTOPRIGHT[0]
WINDOWCENTERLEFT = [0, (WINDOWBOTTOM / 2)]
WINDOWCENTER = [(WINDOWRIGHT / 2), (WINDOWBOTTOM / 2)]
WINDOWCENTERRIGHT = [WINDOWRIGHT, (WINDOWBOTTOM / 2)]
WINDOWBOTTOMLEFT = [0, WINDOWBOTTOM] # Subtract object height from WINDOWBOTTOMLEFT[1]
WINDOWBOTTOMCENTER = [(WINDOWRIGHT / 2), WINDOWBOTTOM]
WINDOWBOTTOMRIGHT = [WINDOWRIGHT, WINDOWBOTTOM] # Do both!

# Time
clock = pygame.time.Clock()
desktopRefreshRate = pygame.display.get_current_refresh_rate()

# Player variables
playerStartPosition = WINDOWCENTER # (X, Y)
playerStartSpeed = 250 # pixels per loop but this will be multiplied by deltaTime so idk what it works out to
playerStartJumpStrength = 1000 # idk about this one chief
playerStartSize = [WINDOWRIGHT / 20, WINDOWBOTTOM / 20] # (X, Y)
playerStartColor = DARKPURPLE # rgb format
deltaTime = clock.tick(desktopRefreshRate) / 1000

# Platform variables
platformStartSize = [50, 15] # (X, Y)
platformStartPosition = (WINDOWBOTTOMCENTER[0], WINDOWBOTTOMCENTER[1] - platformStartSize[1]) # (X, Y)
platformStartColor = RED # rgb format

# Needs orginizing
gravityStrength = 500


# Objects ------------------------------------------------------------------------------------------------#
class Player: # ([int,int], [int,int], RGB, int, int)
    def __init__(self, startPosition, playerSize, playerColor, playerSpeed, jumpStrength): 
        # Player position is just a tuple for X Y
        self.startPosition = list(startPosition)
        self.size = list(playerSize)
        self.color = list(playerColor)
        self.speed = playerSpeed
        self.jumpStrength = jumpStrength
        self.jumpVelocity = jumpStrength # used for jump function
        self.gravityEnabled = True
        self.inputsEnabled = True
        self.isGrounded = False
        self.canJump = True
        self.isJumping = False
        self.canMoveLeft = True
        self.canMoveRight = True
        
        # rect uses top left for x,y and then width height
        self.rectangle = pygame.Rect(self.startPosition, self.size) # (X,Y), (WIDTH,HEIGHT)

    # This is really bad and needs fixed
    def jump(self): # Really bad TODO: NEEDS FIXED (I have actually come to peace with it, )
        if self.isGrounded:
            self.jumpVelocity = self.jumpStrength
            self.canJump = True

        if self.canJump:
            self.rectangle.y -= self.jumpVelocity * deltaTime # subtraction because the y axis is flipped

            if self.jumpVelocity > 0: # Stops the velocity becoming negative
                self.jumpVelocity -= 5
    
    def draw(self):
        self.rectangle.update(self.rectangle)
        pygame.draw.rect(window, self.color, self.rectangle) # (X,Y), (WIDTH,HEIGHT)

class Platform: # ([int,int], [int,int], RGB)
    def __init__(self, platformPosition, platformSize, platformColor):
        self.startPosition = platformPosition
        self.size = platformSize
        self.color = platformColor
        
        # rect uses top left for x,y and then width height
        self.rectangle = pygame.Rect(self.startPosition, self.size) # (X,Y), (WIDTH,HEIGHT)
        
    def draw(self):
        self.rectangle.update(self.rectangle)
        pygame.draw.rect(window, self.color, self.rectangle) # (X,Y), (WIDTH,HEIGHT)
        

# Initialize objects -------------------------------------------------------------------------------------#
player1 = Player(playerStartPosition, playerStartSize, playerStartColor, playerStartSpeed, playerStartJumpStrength)

# Platforms - DON'T FORGET TO PUT THEM IN THE PLATFORM LIST!!! I have made this mistake too much
# First uses variables set before, lookes better obviously but then you have to look for the variables
platform1 = Platform(platformStartPosition, platformStartSize, platformStartColor)
# Hard coded, not great, position won't scale but nothing wrong with it
platform2 = Platform([50, 600], [100, 125], (128, 128, 128))
# same as first but one giant line without variables, it works but super long
platform3 = Platform([WINDOWBOTTOMRIGHT[0] - 100, WINDOWBOTTOMRIGHT[1] - 50], [75, 20], (150, 225, 100))
# So just do whatever none of it matters
platform4 = Platform([(WINDOWLEFT + 100), WINDOWCENTER[1] + 75], [(WINDOWRIGHT - 200), 50], GREEN)
platform5 = Platform([(WINDOWLEFT + 150), WINDOWCENTER[1] - 150], [(WINDOWRIGHT - 300), 20], WHITE)

# Tiny platform to test stepping up (it doesn't work, my current idea is more if statments, we don't have enough)
platform6 = Platform((WINDOWCENTER[0] + 150, WINDOWBOTTOM - 5), (50, 5), platformStartColor)

# All plaforms need to go in here to be drawn on screen in the drawThings() function
platformList = [platform1, platform2, platform3, platform4, platform5, platform6] # <-------DON'T FORGET------- HERE!!!!!

# Get Rect, used in collision 
platformRectList = [] # LEAVE THIS EMPTY
for platform in platformList:
    platformRectList.append(platform.rectangle)


#  Funk(tions) -------------------------------------------------------------------------------------------#
def playerInput(player): # Gets player input then moves player
    # Lord please forgive me for what I am about to do
    keysPressed = pygame.key.get_pressed()
    if player.inputsEnabled: # Checks if player has inputs enabled
        if keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]: # Check which key is pressed
            if player.canJump: # is that action blocked
                if player.rectangle.y >= WINDOWTOP: # checks if you are within the screen
                    player.jump()
                    
        if not keysPressed[pygame.K_w] and not keysPressed[pygame.K_UP] and not player.isGrounded:
            player.canJump = False
        
        if keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]: # repeat
            if player.canMoveLeft: # is that action blocked
                if player.rectangle.x >= WINDOWLEFT: # checks for sides
                    player.rectangle.x -= player.speed * deltaTime

        if keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]: # repeat
            if player.canMoveRight: # is that action blocked
                if player.rectangle.x <= WINDOWRIGHT - player.size[0]: # checks for sides
                    player.rectangle.x += player.speed * deltaTime

def gravity(player): # Pulls player down
        #print(player.gravityEnabled) # for testing
        if player.gravityEnabled == True:
            player.rectangle.y += gravityStrength * deltaTime

            # stops player from going below screen
            if player.rectangle.y >= (pygame.display.get_window_size()[1] - player.size[1]):
                player.gravityEnabled = False
                player.isGrounded = True
                print("Below Screen!!!!!")           

def drawFrameRate(): # counts the frames per second
    # Text for fps values
    averageFPS = str(round(clock.get_fps(), 2)) # get_fps averages the last 10 calls to clock.tick
    
    fontSize = 25
    # Set Font - again grabbing it with the weird method, but it works so well.
    font = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), fontSize)
    fpsText = font.render(f"FPS: {averageFPS}", False, WHITE) 

    # blit draws the image.
    window.blit(fpsText, (5,0)) # 5 is the pixel border

def timer(): # counts up
    currentTime = round((pygame.time.get_ticks() / 1000), 3)

    fontSize = 25
    # Set Font - again grabbing it with the weird method, but it works so well.
    font = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), fontSize)
    timerText = font.render(f"Time: {currentTime}", False, WHITE) 

    # blit draws the image again from top left.
    window.blit(timerText, (WINDOWCENTER[0] - fontSize * 2, WINDOWTOP)) # trys to center, good enough

def drawThings():
    # Draw things. Order matters, things drawn last get put on top
    # This is the only way to layer things that I know of
    player1.draw()

    # draws all platforms
    for platform in platformList:
        platform.draw()

    # UI should go below this so objects don't obscure the view
    timer()
    drawFrameRate()

def collision(player): # TODO: detect collision on bottoms of platforms and fix this garbage
    # collidelist() checks a list of rectangles (platforms) and returns the index of the one that gets hit
    index = player.rectangle.collidelist(platformRectList)
    if index > -1:
        player.color = RED # for testing

        # This one is X,Y and the direct center calculated nicely for us
        playerCenter = player.rectangle.center 
        playerTop = player.rectangle.top # These are ints or floats
        playerLeft = player.rectangle.left
        playerRight = player.rectangle.right
        playerBottom = player.rectangle.bottom
       
        # checks if you are above a platform (remember reversed Y axis)
        if playerBottom > platformRectList[index].top and playerCenter[1] < platformRectList[index].top:
            player.gravityEnabled = False
            player.isJumping = False
            player.canJump = True
            player.isGrounded = True
            player.rectangle.y = platformRectList[index].top - player.size[1] + 1 # This puts you 1 pixel in the object but it works
            
        
        # checks if player is to the left of a platform and not on top
        if playerCenter[0] < platformRectList[index].left and (playerCenter[1] > platformRectList[index].top):
            player.canMoveRight = False 

        # checks if player is to the right of a platform and not on top
        if playerCenter[0] > platformRectList[index].right and (playerCenter[1] > platformRectList[index].top):
            player.canMoveLeft = False

        # if player.rectangle.y <= (pygame.display.get_window_size()[1] - player.size[1]):
        #     player.gravityEnabled = True
        #     player.isGrounded = False
        # else:
        #     player.isGrounded = True
        #     player.canJump = True
    
    # -1 is returned when there is no collision, so we reset controls and gravity
    elif index == -1:
        player.color = DARKPURPLE
        player.canMoveRight = True
        player.canMoveLeft = True

        
        if player.rectangle.bottom <= pygame.display.get_window_size()[1]:
            player.gravityEnabled = True
            player.isGrounded = False
        else:
            player.isGrounded = True
            player.canJump = True
         

# Main Loop ----------------------------------------------------------------------------------------------#
while True:
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Wipe screen every frame so things don't overlap
    window.fill(BLACK)
    window.blit(background, (0, 0))

    # Funk(tions) ----------------------------------------------------------------------------------------#
    gravity(player1)
    playerInput(player1)
    collision(player1)
    

    # This should be at the bottom but before the screen update. I think.
    drawThings()

    # Updates window -------------------------------------------------------------------------------------#
    pygame.display.flip()

    # Frame rate independence ----------------------------------------------------------------------------#
    # Limit frame rate to desktop refresh rate, clock.tick just waits to slow down the loop
    # Also clock.tick() returns the time in milliseconds per frame
    deltaTime = clock.tick(desktopRefreshRate) / 1000 # dividing by 1000 gives use a decimal in seconds
