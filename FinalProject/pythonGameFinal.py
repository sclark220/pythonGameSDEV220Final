import pygame, time, os, sys

# The Game (I think we lost) -----------------------------------------------------------------------------#
pygame.init() # chewsday init
pygame.font.init() 

# Create window and set screen size 
# TODO: Make resizable, but also scale everything else? 
# Not hard but just because you can doesn't mean you should
# 0,0 is top left so the y axis is down the screen.
DISPLAYWIDTH = 1280 # squares look best for background
DISPLAYHEIGHT = 720

# RESIZE STILL DOESN'T WORK
# displaysurface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT), pygame.RESIZABLE)
displaysurface = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT)) # I don't think we need resize anyway
window = pygame.Surface(displaysurface.get_size())
youWinScreen = pygame.Surface(displaysurface.get_size())


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

fontSize = 25
bigFontSize = 100
# Set Font - again grabbing it with the weird method, but it works so well.
font = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), fontSize)
bigFont = pygame.font.Font(os.path.join(__location__,'VT323.ttf'), bigFontSize)

# Variables ----------------------------------------------------------------------------------------------#
# CONSTANTS
# COLORS - rgb format
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKPURPLE = (128, 0, 128) # For player, but an option to customize shouldn't be hard

# WINDOW POSITIONS these are not constants anymore but I like them in all caps, because they should only ever change on window resize
# Careful not to change these it can be easy to do that when refrencing them for positions.
# Remember rectangle positions use the top left corner 
# so if you use a right or bottom positions it will be off screen
# SIDES
WINDOWTOP = 0 # this is just for continuity
WINDOWLEFT = 0
WINDOWRIGHT = pygame.display.get_window_size()[0]
WINDOWBOTTOM = pygame.display.get_window_size()[1]
WINDOWCENTER = [(WINDOWRIGHT / 2), (WINDOWBOTTOM / 2)]

# Time
clock = pygame.time.Clock()
desktopRefreshRate = pygame.display.get_current_refresh_rate()

# Player variables
playerStartPosition = WINDOWCENTER # (X, Y)
playerStartSpeed = 250 # pixels per loop but this will be multiplied by deltaTime so idk what it works out to
playerStartJumpStrength = 1500 # idk about this one chief
playerStartSize = [WINDOWBOTTOM / 20, WINDOWBOTTOM / 20] # (X, Y) # This makes the character scale to the height of the window
playerStartColor = DARKPURPLE # rgb format
deltaTime = clock.tick(desktopRefreshRate) / 1000

# Platform variables
platformStartSize = [50, 15] # (X, Y)
platformStartPosition = (WINDOWCENTER[0], WINDOWBOTTOM - platformStartSize[1]) # (X, Y)
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
        # boolin
        self.gravityEnabled = True
        self.inputsEnabled = True
        self.isGrounded = False
        self.canJump = True
        self.isJumping = False
        self.canMoveLeft = True
        self.canMoveRight = True
        # for coins
        self.score = 0
        
        # rect uses top left for x,y and then width height
        self.rectangle = pygame.Rect(self.startPosition, self.size) # (X,Y), (WIDTH,HEIGHT)

    # This is really bad and needs fixed
    def jump(self): # Really bad TODO: NEEDS FIXED (I have actually come to peace with it, )
        if self.canJump: # is that action blocked    
            if self.isGrounded:
                self.jumpVelocity = self.jumpStrength
                self.canJump = True

            if self.canJump:
                self.rectangle.y -= self.jumpVelocity * deltaTime # subtraction because the y axis is flipped

                if self.jumpVelocity > 0: # Stops the velocity becoming negative
                    self.jumpVelocity -= 25
                else:
                    self.canJump = False
    
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

        # the is for coins, but I put it here for false platforms idk
        self.deleteOnTouch = False
        
    def draw(self):
        self.rectangle.update(self.rectangle)
        pygame.draw.rect(window, self.color, self.rectangle) # (X,Y), (WIDTH,HEIGHT)

class Coin: # ([int,int], [int,int], (R,G,B), int)
    def __init__(self, coinPosition, coinSize, coinColor, coinValue):
        self.startPosition = coinPosition
        self.size = coinSize
        self.color = coinColor
        self.value = coinValue
        self.rectangle = pygame.Rect(self.startPosition, self.size) # (X,Y), (WIDTH,HEIGHT)
        # used to delete the coin on collision
        self.deleteOnTouch = True

    def draw(self):
        self.rectangle.update(self.rectangle)
        pygame.draw.rect(window, self.color, self.rectangle) # (X,Y), (WIDTH,HEIGHT)
        

# Initialize objects -------------------------------------------------------------------------------------#
player1 = Player(playerStartPosition, playerStartSize, playerStartColor, playerStartSpeed, playerStartJumpStrength)

# Add players here (idk seems like a good idea)
playerList = [player1]

# Platforms - DON'T FORGET TO PUT THEM IN THE PLATFORM LIST!!! I have made this mistake too much
# First uses variables set before, lookes better obviously but then you have to look for the variables
platform1 = Platform(platformStartPosition, platformStartSize, platformStartColor)
# Hard coded, not great, position won't scale but nothing wrong with it
platform2 = Platform([50, 600], [100, 125], WHITE)
# same as first but one giant line without variables, it works but super long
platform3 = Platform([WINDOWRIGHT - 100, WINDOWBOTTOM - 100], [75, 20], WHITE)
# So just do whatever none of it matters
platform4 = Platform([(WINDOWLEFT + 100), WINDOWCENTER[1] + 100], [(WINDOWRIGHT - 200), 50], WHITE)
platform5 = Platform([(WINDOWLEFT + 150), WINDOWCENTER[1] - 150], [(WINDOWRIGHT - 300), 20], WHITE)

# All plaforms need to go in here to be drawn on screen in the drawThings() function
platformList = [platform1, platform2, platform3, platform4, platform5] # <-------DON'T FORGET------- HERE!!!!!

# Coins
coin1 = Coin((WINDOWCENTER[0] + 50, 50), (15,15), (255,255,0), 1)
coin2 = Coin((WINDOWLEFT + 50 , WINDOWCENTER[1]), (15,15), (255,255,0), 1)
coin3 = Coin((WINDOWRIGHT - 100, WINDOWBOTTOM - 50), (15,15), (255,255,0), 1)
coinList = [coin1, coin2, coin3]

# Get Rect, used in collision 
objectList = [] # LEAVE THIS EMPTY
rectangleList = [] # LEAVE THIS EMPTY
for platform in platformList:
    objectList.append(platform)
    rectangleList.append(platform.rectangle)
    

for coin in coinList:
    objectList.append(coin)
    rectangleList.append(coin.rectangle)
    


#  Funk(tions) -------------------------------------------------------------------------------------------#
def playerInput(player): # Gets player input then moves player
    # Lord please forgive me for what I am about to do
    keysPressed = pygame.key.get_pressed()
    if player.inputsEnabled: # Checks if player has inputs enabled
        if keysPressed[pygame.K_w]: # Check which key is pressed
            if player.rectangle.top >= WINDOWTOP: # checks if you are within the screen
                player.jump()

        # This looks bad but hang with me:
        # it stops the player from pressing both jump buttons, and makes it so you only get 1 jump 
        if not keysPressed[pygame.K_w] and not player.isGrounded:
            player.canJump = False
        
        if keysPressed[pygame.K_a]:
            if player.canMoveLeft: # is that action blocked
                if player.rectangle.left >= WINDOWLEFT: # checks for sides
                    player.rectangle.x -= player.speed * deltaTime

        if keysPressed[pygame.K_d]:
            if player.canMoveRight: # is that action blocked
                if player.rectangle.right <= WINDOWRIGHT: # checks for sides
                    # idk what happend but you move faster right than left
                    # google says it could be a floating point error but I think it is something else hidden in this mess
                    player.rectangle.x += player.speed * deltaTime * 1.2 # this is the temporary fix
def gravity(player): # Pulls player down
        #print(player.gravityEnabled) # for testing
        if player.gravityEnabled == True:
            player.rectangle.y += gravityStrength * deltaTime

            # stops player from going below screen
            if player.rectangle.bottom >= (WINDOWBOTTOM):
                player.gravityEnabled = False
                player.isGrounded = True
                print("Below Screen!!!!!")           

def drawFrameRate(): # counts the frames per second
    # Text for fps values
    averageFPS = str(round(clock.get_fps(), 2)) # get_fps averages the last 10 calls to clock.tick

    fpsText = font.render(f"FPS: {averageFPS}", False, WHITE) 

    # blit draws the image.
    window.blit(fpsText, (5,0)) # 5 is the pixel border

def timer(): # counts up
    currentTime = round((pygame.time.get_ticks() / 1000), 3)

    timerText = font.render(f"Time: {currentTime}", False, WHITE) 

    # blit draws the image again from top left.
    window.blit(timerText, (WINDOWCENTER[0] - fontSize * 2, WINDOWTOP)) # trys to center, good enough

    return currentTime # used for the win screen

def drawScore(player):
    scoreText = font.render(f"score: {player.score}", False, WHITE) 

    # blit draws the image again from top left.
    window.blit(scoreText, (WINDOWRIGHT - fontSize * 4, WINDOWTOP)) # trys to stay right, good enough

def drawThings():
    # Draw things. Order matters, things drawn last get put on top
    # This is the only way to layer things that I know of
    for player in playerList:
        player.draw()

    for object in objectList:
        object.draw()

    # UI should go below this so objects don't obscure the view
    timer()
    drawFrameRate()
    drawScore(player1)

def collision(player): # TODO: clean up this mess
    # collidelist() checks a list of rectangles (platforms) and returns the index of the one that gets hit
    index = player.rectangle.collidelist(rectangleList)
    if index > -1:
        player.color = RED # for testing

        if (objectList[index].deleteOnTouch):
            rectangleList.pop(index)
            objectList.pop(index)
            player.score += 1 # gives that player a point
            return None # leave before the game break because we destoryed the object we are touching.

        # This one is X,Y and the direct center calculated nicely for us
        playerCenter = player.rectangle.center 
        playerTop = player.rectangle.top # These are ints or floats
        playerLeft = player.rectangle.left
        playerRight = player.rectangle.right
        playerBottom = player.rectangle.bottom
       
        # checks if you are above a platform (remember reversed Y axis)
        if playerBottom > rectangleList[index].top and playerCenter[1] < rectangleList[index].top:
            player.gravityEnabled = False
            player.canJump = True
            player.isGrounded = True
            player.rectangle.y = rectangleList[index].top - player.size[1] + 1 # This puts you 1 pixel in the object but it works

         # checks if you are below a platform (remember reversed Y axis)
        if playerTop < rectangleList[index].bottom and playerCenter[1] > rectangleList[index].bottom:
            player.rectangle.y = rectangleList[index].bottom
            
        # checks if player is to the left of a platform and not on top
        if playerCenter[0] < rectangleList[index].left and (playerCenter[1] > rectangleList[index].top):
            player.canMoveRight = False 

        # checks if player is to the right of a platform and not on top
        if playerCenter[0] > rectangleList[index].right and (playerCenter[1] > rectangleList[index].top):
            player.canMoveLeft = False

        if player.rectangle.bottom <= WINDOWBOTTOM:
            player.canJump = True
            
    # -1 is returned when there is no collision, so we reset controls and gravity
    elif index == -1:
        player.color = DARKPURPLE
        player.canMoveRight = True
        player.canMoveLeft = True

        if player.rectangle.bottom <= WINDOWBOTTOM:
            player.gravityEnabled = True
            player.isGrounded = False
        else:
            player.isGrounded = True
            player.canJump = True
       

# Main Loop ----------------------------------------------------------------------------------------------#
isRunning = True
while isRunning:
    # Check for quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.VIDEORESIZE:
            WINDOWRIGHT = pygame.display.get_window_size()[0]
            WINDOWBOTTOM = pygame.display.get_window_size()[1]
            WINDOWCENTER = [(WINDOWRIGHT / 2), (WINDOWBOTTOM / 2)]
            
    # scale window to resize
    scaledWindow = pygame.transform.scale(window, displaysurface.get_size())
    if(player1.score < 3):
        # Then wipe screen with the background so things dont overlap
        window.blit(background, (0,0))
        displaysurface.blit(scaledWindow, (0,0))
    else:
        youWinText = bigFont.render("You Win!", False, WHITE)
        timerText = font.render(f"Time: {timer()}", False, WHITE)
        youWinScreen.blit(youWinText, (WINDOWCENTER[0] - bigFontSize, WINDOWCENTER[1]))
        youWinScreen.blit(timerText, (WINDOWCENTER[0] - fontSize, WINDOWCENTER[1] - bigFontSize))
        displaysurface.blit(youWinScreen, (0,0))
        isRunning = False


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

waitForExit = True
while(waitForExit):
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                waitForExit = False