#Full name and initials of each of the group members
#Angela Meiqi Shen; Initials: AMS
#Tony Ye; Initials: TY
#Bidyutporna Shee; Initials: BS

#AMS: Different styles of importing are utilized
import random, sys, time, pygame
from pygame.locals import * #Then the module pygame and its variable locals has everything imported, that is what the “*” means

#BS:initial values of each of the variables is set which would be modified later    
FPS = 30
WINDOWWIDTH = 700 #AMS
WINDOWHEIGHT = 600 #AMS
FLASHSPEED = 500 # in milliseconds
FLASHDELAY = 200 # in milliseconds
BUTTONSIZE = 200 #AMS
BUTTONGAPSIZE = 100 #AMS
TIMEOUT = 10#seconds before game over if no button is pushed. #AMS
#AMS: variable's purpose is the same as the name of the variable
#BS: RGB values for each of the colours (this comment is what AMS noticed too)
#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
MUSTYPURPLE  = ( 72,  61, 139)#AMS
RED          = (155,   0,   0)
BRIGHTORANGE = (255, 125,  64)#AMS
GREEN        = (  0, 155,   0)
LIGHTSEA     = ( 32, 178, 170)#AMS
BLUE         = (  0,   0, 155)
LIGHTPINK    = (255, 192, 203)#AMS
YELLOW       = (155, 155,  0)
LIGHTPINK    = (255, 204, 204) #BS
MAROON       = (102,   0,  51) #BS
bgColor = BLACK

#BS: XMARGIN and YMARGIN are defined using the pre-declared variables (this comment is what AMS noticed too)
XMARGIN = int((WINDOWWIDTH - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)
YMARGIN = int((WINDOWHEIGHT - (2 * BUTTONSIZE) - BUTTONGAPSIZE) / 2)

#BS: Rect objects for each of the four buttons are set using appropriate coordinates and sizes (this comment is what AMS noticed too)
YELLOWRECT = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
BLUERECT   = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
REDRECT    = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
GREENRECT  = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)

# Distracting box colors - TY
yel_box = pygame.image.load('yel_box.png')
red_box = pygame.image.load('red_box.png')
gre_box = pygame.image.load('gre_box.png')
blu_box = pygame.image.load('blu_box.png')

# Distracting box variables - TY
box1_x = WINDOWWIDTH/2
box1_y = WINDOWHEIGHT/2
box1_xdir = -15 # Initial x and y speeds
box1_ydir = 15

box2_x = WINDOWWIDTH/2
box2_y = WINDOWHEIGHT/2
box2_xdir = 15
box2_ydir = -15

box3_x = WINDOWWIDTH/2
box3_y = WINDOWHEIGHT/2
box3_xdir = -13
box3_ydir = 11

box4_x = WINDOWWIDTH/2
box4_y = WINDOWHEIGHT/2
box4_xdir = -19
box4_ydir = -15

# BS: main function is created to run the bulk of the program and call the other functions if needed 
def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BEEP1, BEEP2, BEEP3, BEEP4 #BS: global variables are declared so that they can be called in other functions

    pygame.init() #BS: initialize all imported pygame modules
    FPSCLOCK = pygame.time.Clock() #BS: a clock object is created
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) #BS: a display surface is created
    pygame.display.set_caption('Simon Says!') #BS: a caption different from the original one is set

    BASICFONT = pygame.font.SysFont('Segoe UI',18, bold=True) #BS: a font object using a different method is created to display the score and the instructions
    infoSurf = BASICFONT.render('Match pattern -> click on button or use K, L, N, M keys or score = 0', 1, WHITE) #***AMS
    infoRect = infoSurf.get_rect() #BS: a rectangular object is created
    infoRect.topleft = (70, WINDOWHEIGHT - 35) #AMS

    #BS: load the sound files to play sound effect as the player clicks on each button (this comment is what AMS noticed too)
    #BS: returns a sound object stored in the global variables BEEP1 to BEEP4 (this comment is what AMS noticed too)
    BEEP1 = pygame.mixer.Sound('beep1.ogg')
    BEEP2 = pygame.mixer.Sound('beep2.ogg')
    BEEP3 = pygame.mixer.Sound('beep3.ogg')
    BEEP4 = pygame.mixer.Sound('beep4.ogg')

    #BS: Initialize some variables for a new game
    pattern = [] #BS: stores the pattern of colors that the player must memorize
    currentStep = 0 #BS: the color that the player must click next
    lastClickTime = 0 #BS: timestamp of the player's last button click
    score = 0 #BS: stores the player's score 
    #BS: When False, the pattern of colour is playing. When True, waiting for the player to click a colored button:
    waitingForInput = False

    while True: #BS: start of the main game loop
        clickedButton = None # #BS: will be None at the start of each iteration; if a button is clicked during the iteration, resets to the color value of that button
        drawButtons() #BS: four colored buttons are drawn when the function is called
        
        pygame.draw.circle(DISPLAYSURF, LIGHTPINK, (WINDOWWIDTH - 345, 300),55) #BS: a circle is drawn which was not present in the original code
        
        scoreSurf = BASICFONT.render('Score: ' + str(score), 4, MAROON) #BS: a new text is rendered to the surface to display the score 
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (WINDOWWIDTH - 380, 290) #BS: position of the scoreboard is changed in the personalized code
        DISPLAYSURF.blit(scoreSurf, scoreRect) #BS: the contents of one surface is copied onto another surface

        DISPLAYSURF.blit(infoSurf, infoRect)
        
        # Distracting box loops - TY
        calc_distracting_box1() 
        distracting_box1()
        calc_distracting_box2() 
        distracting_box2()
        calc_distracting_box3() 
        distracting_box3()
        calc_distracting_box4() 
        distracting_box4()
        
        #BS: checking for mouse clicks
        checkForQuit()
        for event in pygame.event.get(): #BS: start of the event handling loop
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos #BS: stores the (x,y) coordinates of any mouse clicks
                clickedButton = getButtonClicked(mousex, mousey) #BS: when clicked over one of the buttons, returns the color object associated with the button, otherwise returns None
           
            #BS: chceking for keyboard presses
            #BS: K,L,N,M keys correspond the buttons (keys are changed from the original code)
            elif event.type == KEYDOWN: 
                if event.key == K_k:
                    clickedButton = YELLOW
                elif event.key == K_l:
                    clickedButton = BLUE
                elif event.key == K_n:
                    clickedButton = RED
                elif event.key == K_m:
                    clickedButton = GREEN



        if not waitingForInput:
            # play the pattern
            pygame.display.update()
            pygame.time.wait(500) #BS: wait time is changed from the original code
            pattern.append(random.choice((YELLOW, BLUE, RED, GREEN)))
            for button in pattern:
                flashButtonAnimation(button)
                pygame.time.wait(FLASHDELAY)
            waitingForInput = True
        else:
            #BS: wait for the player to click on buttons
            if clickedButton and clickedButton == pattern[currentStep]:
                #BS: when player clicks the correct button
                flashButtonAnimation(clickedButton)
                currentStep += 1
                lastClickTime = time.perf_counter()

                if currentStep == len(pattern):
                    #BS: pushed the last button in the pattern
                    changeBackgroundAnimation()
                    score += 1
                    waitingForInput = False
                    currentStep = 0 #BS: reset back to first step

            elif (clickedButton and clickedButton != pattern[currentStep]) or (currentStep != 0 and time.perf_counter() - TIMEOUT > lastClickTime):
                #BS: pushed the incorrect button, or has timed out
                gameOverAnimation()
                #BS: reset the variables for a new game:
                pattern = []
                currentStep = 0
                waitingForInput = False
                score = 0
                pygame.time.wait(500) #BS: wait time is changed from the original code
                changeBackgroundAnimation()

        pygame.display.update()
        FPSCLOCK.tick(FPS)

#AMS: This function serves the purpose of terminating the game in python pygame
def terminate():
    pygame.quit()
    sys.exit()

#TY: Checks for the pygame event QUIT or escape key and quits pygame if activated
def checkForQuit():
    for event in pygame.event.get(QUIT): #TY: Terminates if quit event is present
        terminate() 
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE: #TY: Terminates if esc key event is present
            terminate()
        pygame.event.post(event) #TY: Puts the other KEYUP event objects back

#TY: Animations for the buttons
def flashButtonAnimation(color, animationSpeed=50):
    L1 = [BEEP1,BEEP2,BEEP3,BEEP4] #AMS
    if color == YELLOW:
        sound = random.choice(L1)#AMS
        flashColor = LIGHTPINK #AMS
        rectangle = YELLOWRECT
    elif color == BLUE:
        sound = random.choice(L1)#AMS
        flashColor = LIGHTSEA #AMS
        rectangle = BLUERECT
    elif color == RED:
        sound = random.choice(L1)#AMS
        flashColor = MUSTYPURPLE #AMS
        rectangle = REDRECT
    elif color == GREEN:
        sound = random.choice(L1)#AMS
        flashColor = BRIGHTORANGE #AMS
        rectangle = GREENRECT

    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE)) #TY: Creates new box on top with the flash color
    flashSurf = flashSurf.convert_alpha()
    r, g, b = flashColor
    sound.play()
    for start, end, step in ((0, 255, 1), (255, 0, -1)): #TY: Fading animation loop with changing alpha
        for alpha in range(start, end, animationSpeed * step):
            checkForQuit()
            DISPLAYSURF.blit(origSurf, (0, 0))
            flashSurf.fill((r, g, b, alpha))
            DISPLAYSURF.blit(flashSurf, rectangle.topleft)
            pygame.display.update()
            FPSCLOCK.tick(FPS)
    DISPLAYSURF.blit(origSurf, (0, 0))

#TY: Draws buttons with color
def drawButtons():
    pygame.draw.rect(DISPLAYSURF, YELLOW, YELLOWRECT)
    pygame.draw.rect(DISPLAYSURF, BLUE,   BLUERECT)
    pygame.draw.rect(DISPLAYSURF, RED,    REDRECT)
    pygame.draw.rect(DISPLAYSURF, GREEN,  GREENRECT)

#TY: Chooses a random color to change the background to and plays an animation
def changeBackgroundAnimation(animationSpeed=40):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))#AMS


    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): #TY: Animation loop from 0 alpha (transparent) to 255 alpha (opaque) 
        checkForQuit()
        DISPLAYSURF.fill(bgColor)

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        drawButtons() #TY: Redraw the buttons on top of the new color background tint

        pygame.display.update() #TY: Updates display
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

#TY: Animation for end of game
def gameOverAnimation(color=WHITE, animationSpeed=50):
    origSurf = DISPLAYSURF.copy()
    flashSurf = pygame.Surface(DISPLAYSURF.get_size())
    flashSurf = flashSurf.convert_alpha()
    BEEP1.play() #TY: Play all the beeps at nearly the same time
    BEEP2.play()
    BEEP3.play()
    BEEP4.play()
    r, g, b = color
    for i in range(3): #TY: Flash 3 times
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            #TY: Loop goes from transparent to opaque then back to transparent
            for alpha in range(start, end, animationSpeed * step):
                checkForQuit()
                flashSurf.fill((r, g, b, alpha))
                DISPLAYSURF.blit(origSurf, (0, 0))
                DISPLAYSURF.blit(flashSurf, (0, 0))
                drawButtons()
                pygame.display.update()
                FPSCLOCK.tick(FPS)


#TY: If mouse coordinates collides with a colored box, returns that color
def getButtonClicked(x, y):
    if YELLOWRECT.collidepoint( (x, y) ):
        return YELLOW
    elif BLUERECT.collidepoint( (x, y) ):
        return BLUE
    elif REDRECT.collidepoint( (x, y) ):
        return RED
    elif GREENRECT.collidepoint( (x, y) ):
        return GREEN
    return None
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Distracting box functions - TY
def distracting_box1():
    DISPLAYSURF.blit(yel_box, (box1_x, box1_y)) # Display the image with coordinates x and y
    
def calc_distracting_box1():
    global box1_x
    global box1_y
    global box1_xdir
    global box1_ydir
    if box1_x == 1: # If the image coordinate gets near any edge, its direction is reversed
        box1_xdir *= -1
    elif box1_x == WINDOWWIDTH-200:
        box1_xdir *= -1
    elif box1_y == 1:
        box1_ydir *= -1
    elif box1_y == WINDOWHEIGHT-200:
        box1_ydir *= -1
        
    box1_x += box1_xdir #TY: Adds the direction value every loop
    box1_y += box1_ydir
    box1_x = min(box1_x, WINDOWWIDTH-200) # Constrains the image coordinate within the window
    box1_x = max(box1_x, 1)
    box1_y = min(box1_y, WINDOWHEIGHT-200)
    box1_y = max(box1_y, 1)
    
def distracting_box2():
    DISPLAYSURF.blit(red_box, (box2_x, box2_y))
    
def calc_distracting_box2():
    global box2_x
    global box2_y
    global box2_xdir
    global box2_ydir
    if box2_x == 1:
        box2_xdir *= -1
    elif box2_x == WINDOWWIDTH-200:
        box2_xdir *= -1
    elif box2_y == 1:
        box2_ydir *= -1
    elif box2_y == WINDOWHEIGHT-200:
        box2_ydir *= -1
        
    box2_x += box2_xdir
    box2_y += box2_ydir
    box2_x = min(box2_x, WINDOWWIDTH-200)
    box2_x = max(box2_x, 1)
    box2_y = min(box2_y, WINDOWHEIGHT-200)
    box2_y = max(box2_y, 1)
    
def distracting_box3():
    DISPLAYSURF.blit(gre_box, (box3_x, box3_y))
    
def calc_distracting_box3():
    global box3_x
    global box3_y
    global box3_xdir
    global box3_ydir
    if box3_x == 1:
        box3_xdir *= -1
    elif box3_x == WINDOWWIDTH-200:
        box3_xdir *= -1
    elif box3_y == 1:
        box3_ydir *= -1
    elif box3_y == WINDOWHEIGHT-200:
        box3_ydir *= -1
        
    box3_x += box3_xdir
    box3_y += box3_ydir
    box3_x = min(box3_x, WINDOWWIDTH-200)
    box3_x = max(box3_x, 1)
    box3_y = min(box3_y, WINDOWHEIGHT-200)
    box3_y = max(box3_y, 1)
    
def distracting_box4():
    DISPLAYSURF.blit(blu_box, (box4_x, box4_y))
    
def calc_distracting_box4():
    global box4_x
    global box4_y
    global box4_xdir
    global box4_ydir
    if box4_x == 1:
        box4_xdir *= -1
    elif box4_x == WINDOWWIDTH-200:
        box4_xdir *= -1
    elif box4_y == 1:
        box4_ydir *= -1
    elif box4_y == WINDOWHEIGHT-200:
        box4_ydir *= -1
        
    box4_x += box4_xdir
    box4_y += box4_ydir
    box4_x = min(box4_x, WINDOWWIDTH-200)
    box4_x = max(box4_x, 1)
    box4_y = min(box4_y, WINDOWHEIGHT-200)
    box4_y = max(box4_y, 1)

if __name__ == '__main__': #BS: When the module is executed as a scipt, do this
    main()

