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
        self.wordY = randint(-100,0)
        self.text = word
        self.wordObj = font.render(self.text, True, (66, 255, 79))
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
            self.wordObj = font.render(self.text, True, (255, 255, 0))
        elif not flag:
            self.wordObj = font.render(self.text, True, (66, 255, 79))