# Typing Game
A very basic typing game.


## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. Since the game is written in Python only
a few modules are required,check the **Installing** section for information on how to do this.


## Things you will need
You will need the following software installed in your computer:

* Python 3.7.4
* Pygame 2.0.1


## Installing
A step by step series of examples that tell you how to get the game running.

**[Python:](https://www.python.org/downloads/)**
```
Download the latest version and install it on your computer.
```
**[Pygame:](https://www.pygame.org/wiki/GettingStarted)**
```
python pip install pygame*
```

## About
The game generates random words taken from a .txt file(words.txt) taken from [here](https://github.com/dwyl/english-words).
At the bottom of the page usefull(?) information is displayed:
* Score(Total words typed before exiting the screen.)
* Time (Displays how many ~~hours~~minutes you wasted on this game.)
* Level (The current level.)
* WPM (Words per minute)
* Missed (How many words you missed.)

**Gameplay(?)**
* Pressing a a letter will "focus" on a word.
* Pressing all the correct letters,in sequence,you complete the focused word and earn a point.
* If you miss a word,it will disapear taking it's point with it.
* By typing all the words on the screen will advance you to the next level.
* Each level will add an extra word and increase the text speed slightly.
* Pressing the Escape button will "un-focus" the word you are typing and let you select a new one.
* Pressing the Tab button will change focus (It will cycle between the current words on the screen).

## A screenshot of the game:
![screenshot](/screenshot.PNG)
