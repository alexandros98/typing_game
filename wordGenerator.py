from random import choice,randint

class WordGenerator:
    def __init__(self):
        self.f = open("words.txt", "r")
        self.allText = self.f.read().lower()
        self.words = list(map(str,self.allText.split()))

    def generateWord(self):
        return choice(self.words)


class Word:
    def __init__(self,word,x,font,globalSpeed):
        self.wordX = x
        self.wordY = randint(-200,0)
        self.text = word
        self.wordObj = font.render(self.text, True, (179,179,179))
        self.WordWidth = font.size(self.text)[0]
        self.speed = len(self.text)
        
        if self.speed >= 15:
            self.speed = -globalSpeed/2#+ randint(0,font.size(self.text)[1])

        elif self.speed >5:
            self.speed = 0 #+ randint(font.size(self.text)[1],font.size(self.text)[1]*2)

        else:
            self.speed = globalSpeed/2# + randint(0,font.size(self.text)[1])

    def getWordObj(self):
        return self.wordObj

    def getWord(self):
        return self.text
    
    def getPosX(self):
        return self.wordX

    def getPosY(self):
        return self.wordY

    def getWordWidth(self):
        return self.WordWidth

    def adjustWord(self,y):
        self.wordX = y

    def wordSpeed(self):
        return self.speed
    
    def addWordY(self,amount):
        self.wordY += amount

    def focusColor(self,font,flag):
        if flag:
            self.wordObj = font.render(self.text, True, (0, 120, 215))
        elif not flag:
            self.wordObj = font.render(self.text, True, (179,179,179))

class Anouncer:
    def __init__(self,anouncerFont,swidth,sheight,botheight):
        self.initialPrint = True
        self.scrwidth = swidth
        self.scrheight = sheight
        self.botomheight = botheight
        self.font = anouncerFont
        self.anouncerColor = (179,179,179)
        self.anouncerMessage = ""
        self.anouncerPos = 0
        self.anouncerTxt = self.font.render(self.anouncerMessage,True, self.anouncerColor)
        self.fadeFlag = True
        self.fade = 0
        self.fadeSpeed = 2
        self.anouncerTime = 0
        self.anouncertimeTotal = 3

    def changeText(self,text,fadeSpeed):
        self.fadeFlag = True
        self.fade = 0
        self.fadeSpeed = fadeSpeed
        self.anouncerMessage = text
        self.anouncerTxt = self.font.render(self.anouncerMessage,True, self.anouncerColor)
        self.anouncerPos = ((self.scrwidth-self.anouncerTxt.get_size()[0])/2,(self.scrheight-self.anouncerTxt.get_size()[1]-self.botomheight)/2)

    def display(self,screen,alpha):
        self.anouncerTxt.set_alpha(alpha)
        if self.anouncerTxt:
            if self.anouncerTime == self.anouncertimeTotal:
                self.anouncerMessage = ""
                self.anouncerTime = 0
            screen.blit(self.anouncerTxt,self.anouncerPos)