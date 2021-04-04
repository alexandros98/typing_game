import sys,pygame
from pygame.constants import KSCAN_BACKSPACE, K_ESCAPE, MOUSEBUTTONDOWN, TEXTINPUT
from wordGenerator import WordGenerator,Word,Anouncer
from random import randint

#inits
pygame.init()
clk =  pygame.time.Clock()
screenWidth = 1000
screenHeight = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Typing Game")
windowIcon = pygame.image.load("window_icon.jpg")
pygame.display.set_icon(windowIcon)
mainfont = pygame.font.SysFont(None,40)
wg =  WordGenerator()

#Target Text Related
texts = []
wordSpeed = 15
wordsonscreen = len(texts) #Amount of words displayed on screen.
wordsTotal = 3 #Total number of words allowed to be displayed on screen.
spawnFlag = True


#User input related
userinputColor = (255, 255, 84)
keyPressed = ''
userinputStaticColor = (0, 120, 215)
userinputText = ""
userInputFont = pygame.font.SysFont(None,50)
userinputStatic = userInputFont.render(">", True, userinputStaticColor)
userinput = userInputFont.render(userinputText, True, userinputColor)
userinputPos = (screenWidth/2-(screenWidth/10)+userinputStatic.get_size()[0],screenHeight-(screenHeight/9))
userinputStaticPos = (screenWidth/2-(screenWidth/10),screenHeight-(screenHeight/9))
counter = 0
inputHidden = ""
focusWord = None
resetFlag = False
swapFlag = False
userInput_ghost = ""
usrincolor_ghost = (179,179,179)
usrinfont_ghost = pygame.font.SysFont(None,50)
usrintxt_ghost = usrinfont_ghost.render("" + userInput_ghost, True, usrincolor_ghost)
usrintxt_ghost.set_alpha(127)

#Score realted
botGap = 30 #Gap between the elements on the bottom infos.
points = 0
timeTemp = 0
mins = 0
secs = 0
bottomInfosHeight = 40
bottomTextColor = (179,179,179)
bottomFont = pygame.font.SysFont(None,30)
correctWords = bottomFont.render("Score: " + str(points), True, bottomTextColor)
time = bottomFont.render("Time: " + str(timeTemp) + ":" +str(int(timeTemp)), True, bottomTextColor)
level = 1
levelAdv = 0
levelText = bottomFont.render("Level: " + str(int(level)), True, bottomTextColor)
wpm = 0
wpmTemp = 0
wpmFormat = "{0:.2f}"
wordsperMin = bottomFont.render("WPM: " + str(wpm), True, bottomTextColor)
wordsMissed = 0
wordsMissedTxt = bottomFont.render("Missed: " + str(wordsMissed), True, bottomTextColor)

#Anouncer related
anouncerFont = pygame.font.SysFont(None,100)
anouncer = Anouncer(anouncerFont,screenWidth,screenHeight,bottomInfosHeight)
alpha = 0


while True:
    #Display the text for the first level anouncer(uses the initialprint variable to check,should oly happen once)
    if anouncer.initialPrint:
        anouncer.changeText("Level: " + str(level),2)
        anouncer.initialPrint = False
    frameTime = clk.tick(60) / 1000
    wordsonscreen = len(texts)
    wpmTemp += frameTime
    timeTemp += frameTime
    if int(timeTemp) == secs:
        if secs <= 9 and mins <= 9:
            time = bottomFont.render("Time: 0" + str(mins) + ":0" +str(secs), True, bottomTextColor)
        elif secs >= 9 and mins >= 9:
            time = bottomFont.render("Time: " + str(mins) + ":" +str(secs), True, bottomTextColor)
        else:
            time = bottomFont.render("Time: 0" + str(mins) + ":" +str(secs), True, bottomTextColor)
        secs+=1
    if secs == 60:
        mins += 1
        secs = 0
        timeTemp = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                resetFlag = True
            elif event.key == pygame.K_BACKSPACE: #Delete last cahracter wehn pressign backspace,does nothing for now.
                pass
                """
                inputHidden = inputHidden[:-1:]
                userinputText = ">" + inputHidden
                userinput = userInputFont.render(userinputText, True, userinputColor)
                """
            elif event.key == pygame.K_TAB:
                swapFlag = True
        elif event.type == pygame.TEXTINPUT:
            keyPressed = event.text.lower()
    
    for x in texts:
        if focusWord and focusWord.getWord() != x.getWord():
            x.focusColor(mainfont,False)
        if focusWord != None and resetFlag and focusWord.getWord() == x.getWord():
            focusWord = None
            inputHidden = ''
            userinputText = ""
            userinput = userInputFont.render(userinputText, True, userinputColor)
            counter = 0
            x.focusColor(mainfont,False)
            userInput_ghost = ""
            usrintxt_ghost = usrinfont_ghost.render("" + userInput_ghost, True, usrincolor_ghost)
            usrintxt_ghost.set_alpha(127)
            resetFlag = False
        if swapFlag and focusWord != None: #Target word focus change.
            indexTemp = texts.index(focusWord) + 1
            if indexTemp >= len(texts):
                indexTemp = 0
            counter = 0
            inputHidden = ""
            userinputText = ""
            userinput = userInputFont.render(userinputText, True, userinputColor)
            focusWord = texts[indexTemp]
            focusWord.focusColor(mainfont,True)
            userInput_ghost = focusWord.getWord()
            usrintxt_ghost = usrinfont_ghost.render("" + userInput_ghost, True, usrincolor_ghost)
            usrintxt_ghost.set_alpha(127)
            swapFlag = False
        if counter < len(x.getWord()) and keyPressed == x.getWord()[counter] and x.getPosY() >= 0:
            if focusWord == None or focusWord.getWord() == x.getWord():
                x.focusColor(mainfont,True)
                focusWord = x
                userInput_ghost = x.getWord()
                usrintxt_ghost = usrinfont_ghost.render("" + userInput_ghost, True, usrincolor_ghost)
                usrintxt_ghost.set_alpha(127)
                userinputText += keyPressed
                userinput = userInputFont.render(userinputText, True, userinputColor)
                counter += 1
                inputHidden += keyPressed
                keyPressed = ''
        
        if x.getPosY() >= screenHeight - bottomInfosHeight:
            texts.remove(x)
            wordsMissed += 1
            wordsMissedTxt = bottomFont.render("Missed: " + str(wordsMissed), True, bottomTextColor)
            userInput_ghost = ""
            usrintxt_ghost = usrinfont_ghost.render("" + userInput_ghost, True, usrincolor_ghost)
            if x == focusWord:
                focusWord = None
                userinputText = ""
                userinput = userInputFont.render(userinputText, True, userinputColor)
                counter = 0
                inputHidden = ""
            #spawnFlag = True
            levelAdv -= 1
            
            
    if focusWord != None and inputHidden == focusWord.getWord():
        inputHidden = ''
        userinputText = ""
        counter = 0
        texts.remove(focusWord)
        focusWord = None
        points += 1
        correctWords = bottomFont.render("Score: " + str(points), True, bottomTextColor)

    #-----------------------------
    if wordsonscreen < wordsTotal and spawnFlag:
        wordTemp = Word(wg.generateWord(),randint(0,screenWidth),mainfont,wordSpeed)
        if (screenWidth - wordTemp.getPosX()) < wordTemp.getWordWidth():
            wordTemp.adjustWord(screenWidth - wordTemp.getWordWidth())
        texts.append(wordTemp)
        levelAdv += 1
    else:
        spawnFlag = False

    if points == levelAdv:
        wordSpeed += 1
        wordsTotal += 1
        level += 1
        levelText = bottomFont.render("Level: " + str(int(level)), True, bottomTextColor)
        anouncer.changeText("Level: " + str(level),2)
        spawnFlag = True


    wpm = points/wpmTemp
    wordsperMin = bottomFont.render("WPM: " + str(wpmFormat.format(wpm)), True, bottomTextColor)

    #blits etc..
    screen.fill((18,18,18))
    screen.blit(usrintxt_ghost,userinputPos)
    screen.blit(userinput,userinputPos)
    screen.blit(userinputStatic,userinputStaticPos)
    for x in texts:
        if x.getPosY() >= screenHeight:
            texts.remove(x)
        speedTemp = (x.wordSpeed() + wordSpeed)*frameTime
        x.addWordY(speedTemp)
        screen.blit(x.getWordObj(),(x.getPosX(),x.getPosY()))
    pygame.draw.rect(screen,(64,64,64),pygame.Rect(0,screenHeight-bottomInfosHeight, screenWidth, bottomInfosHeight))
    screen.blit(correctWords,(botGap,screenHeight-(bottomInfosHeight-correctWords.get_size()[1]/2)))
    screen.blit(time,(correctWords.get_size()[0] + botGap*2,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    screen.blit(levelText,(correctWords.get_size()[0] + time.get_size()[0] + botGap*3,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    screen.blit(wordsperMin,(correctWords.get_size()[0] + time.get_size()[0] + levelText.get_size()[0] + botGap*4,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    screen.blit(wordsMissedTxt,(correctWords.get_size()[0] + time.get_size()[0] + levelText.get_size()[0] + wordsperMin.get_size()[0] + botGap*5,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    if anouncer.fadeFlag and anouncer.fade == 0:
        anouncer.display(screen,alpha)
        alpha += anouncer.fadeSpeed
        if alpha >= 255:
            anouncer.fade = 255
    elif anouncer.fadeFlag and anouncer.fade == 255:
        anouncer.display(screen,alpha)
        alpha -= anouncer.fadeSpeed
        if alpha == 0:
            anouncer.fadeFlag = False
    
    pygame.display.update()