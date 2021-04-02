import sys,pygame
from pygame.constants import KSCAN_BACKSPACE, K_ESCAPE, MOUSEBUTTONDOWN, TEXTINPUT
from wordGenerator import WordGenerator,Word
from random import randint

#inits
pygame.init()
clk =  pygame.time.Clock()
screenWidth = 1000
screenHeight = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
mainfont = pygame.font.SysFont(None,40)
wg =  WordGenerator()

#Target Text Related
texts = []
wordSpeed = 20
wordsonscreen = len(texts) #Amount of words displayed on screen.
wordsTotal = 1 #Total number of words allowed to be displayed on screen.

#User input related
userinputColor = (50,0,100)
keyPressed = ''
userinputText = ">"
userInputFont = pygame.font.SysFont(None,50)
userinput = userInputFont.render(userinputText, True, userinputColor)
userinputPos = screenWidth/2-(screenWidth/10),screenHeight-(screenHeight/9)
counter = 0
inputHidden = ""
focusWord = None
focusFlag = False #Probably a useless variable...
resetFlag = False
swapFlag = False

#Score realted
botGap = 30 #Gap between the elements on the bottom infos.
points = 0
timeTemp = 0
mins = 0
secs = 0
bottomInfosHeight = 40
bottomTextColor = (0,0,0)
bottomFont = pygame.font.SysFont(None,30)
correctWords = bottomFont.render("Score: " + str(points), True, bottomTextColor)
time = bottomFont.render("Time: " + str(timeTemp) + ":" +str(int(timeTemp)), True, bottomTextColor)
level = 1
levelAdv = 5 #Every 5 correct words,+1 word on screen.
levelText = bottomFont.render("Level: " + str(int(level)), True, bottomTextColor)
wpm = 0
wpmTemp = 0
wpmFormat = "{0:.2f}"
wordsperMin = bottomFont.render("WPM: " + str(wpm), True, bottomTextColor)



while True:
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
    print(timeTemp)
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
            userinputColor = (50,0,100)
            userinputText = ">"
            userinput = userInputFont.render(userinputText, True, userinputColor)
            counter = 0
            print("changed focus")
            x.focusColor(mainfont,False)
            resetFlag = False
        if swapFlag and focusWord != None: #Target word focus change.
            indexTemp = texts.index(focusWord) + 1
            if indexTemp >= len(texts):
                indexTemp = 0
            counter = 0
            inputHidden = ''
            userinputText = ">"
            userinput = userInputFont.render(userinputText, True, userinputColor)
            focusWord = texts[indexTemp]
            focusWord.focusColor(mainfont,True)
            swapFlag = False
        if counter < len(x.getWord()) and keyPressed == x.getWord()[counter] and x.getPosY() >= 0:
            if focusWord == None or focusWord.getWord() == x.getWord():
                x.focusColor(mainfont,True)
                focusWord = x
                focusFlag = True
                userinputColor = (50,0,100)
                userinputText += keyPressed
                userinput = userInputFont.render(userinputText, True, userinputColor)
                counter += 1
                inputHidden += keyPressed
                keyPressed = ''
        
        if x.getPosY() >= screenHeight - bottomInfosHeight:
            texts.remove(x)
            print("word missed")
            if x == focusWord:
                focusWord = None
                userinputText = ">"
                userinput = userInputFont.render(userinputText, True, userinputColor)
                counter = 0
                inputHidden = ""
            
    if focusWord != None and inputHidden == focusWord.getWord():
        wordSpeed += 2
        focusFlag = False
        #print(focusWord.getWord())
        inputHidden = ''
        userinputColor = (0,255,0)
        userinput = userInputFont.render(userinputText, True, userinputColor)
        userinputText = ">"
        counter = 0
        texts.remove(focusWord)
        #print("Word Completed")
        focusWord = None
        points += 1
        correctWords = bottomFont.render("Score: " + str(points), True, bottomTextColor)
        

    if wordsonscreen < wordsTotal:
        wordTemp = Word(wg.generateWord(),randint(0,screenWidth),mainfont,wordSpeed)
        if (screenWidth - wordTemp.getPosX()) < wordTemp.getWordWidth():
            wordTemp.adjustWord(screenWidth - wordTemp.getWordWidth())
        texts.append(wordTemp)

    if points == levelAdv:
        wordsTotal += 1
        levelAdv += 5
        level += 1
        levelText = bottomFont.render("Level: " + str(int(level)), True, bottomTextColor)
    wpm = points/wpmTemp
    wordsperMin = bottomFont.render("WPM: " + str(wpmFormat.format(wpm)), True, bottomTextColor)
    #blits etc..
    screen.fill((0,0,0))
    screen.blit(userinput,(userinputPos))
    for x in texts:
        if x.getPosY() >= screenHeight:
            texts.remove(x)
        speedTemp = (x.wordSpeed() + wordSpeed)*frameTime
        x.addWordY(speedTemp)
        screen.blit(x.getWordObj(),(x.getPosX(),x.getPosY()))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(0,screenHeight-bottomInfosHeight, screenWidth, bottomInfosHeight))
    screen.blit(correctWords,(botGap,screenHeight-(bottomInfosHeight-correctWords.get_size()[1]/2)))
    screen.blit(time,(correctWords.get_size()[0] + botGap*2,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    screen.blit(levelText,(correctWords.get_size()[0] + time.get_size()[0] + botGap*3,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    screen.blit(wordsperMin,(correctWords.get_size()[0] + time.get_size()[0] + levelText.get_size()[0] + botGap*4,screenHeight-(bottomInfosHeight-time.get_size()[1]/2)))
    pygame.display.update()