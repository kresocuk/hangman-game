import pygame, sys, random


mainClock = pygame.time.Clock()
from pygame.locals import *
from timeit import default_timer as timer

pygame.init()
pygame.display.set_caption('TEK Hangman')
screen = pygame.display.set_mode((800, 600), 0, 32)

font = pygame.font.SysFont(None, 60)
sfont = pygame.font.SysFont(None, 40)



def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


logoImg = pygame.image.load("output-onlinepngtools.png").convert_alpha()
logoX = 40
logoY = 50

dashesImg= pygame.image.load("dashes.png").convert_alpha()
dashesX = 130
dashesY = 475

def logo():
    screen.blit(logoImg, (logoX, logoY))
    screen.blit(dashesImg, (dashesX, dashesY))

    


def main_menu():
    while True:

        screen.fill((176, 224, 230))
        logo()
        draw_text(' Main menu', font, (0, 0, 0), screen, 260, 50)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 120, 175, 50)
        draw_text('Start game', sfont, (30,144,255), screen, 315, 130)
        

        if button_1.collidepoint((mx, my)):
            if click:
                game()
        
        pygame.draw.rect(screen, (0, 0, 0), button_1, 4)
        

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    fps = 30
    width = 800
    height = 600

    black = (0, 0, 0)
    white = (255, 255, 255)
    lightred = (255, 165, 145)
    darklightred = (255, 97, 81)
    red = (230 , 0, 0)
    lightblue = (126, 178, 255)
    darklightblue = (42, 129, 255)
    lightgrey = (192, 192, 192)

    textBoxSpace = 5
    textBoxNumber = 0

    def button(word, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, w, h))
            if click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(screen, ic, (x, y, w, h))

        buttonText = pygame.font.Font("freesansbold.ttf", 20)
        buttonTextSurf = buttonText.render(word, True, white)
        buttonTextRect = buttonTextSurf.get_rect()
        buttonTextRect.center = ((x + (w / 2)), (y + (h / 2)))
        screen.blit(buttonTextSurf, buttonTextRect)

    def endGame():
        global textBoxSpace, textBoxNumber, end, start
        end = timer()
        print("Time it took: ", end - start)
        timeTaken = (end - start)
        textBoxSpace = 5
        textBoxNumber = 0
        message = "Vrijeme: " + str(round(timeTaken)) + "s"
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            button("Da", (width / 2) - 50, 420, 100, 50, darklightred, lightred, quitGame)
            button("Ne", (width / 2) - 50, 500, 100, 50, darklightred, lightred, hangman)

            largeText = pygame.font.SysFont("comicsansms", 115)
            TextSurf = largeText.render("Završiti igru?", True, darklightred)
            TextRect = TextSurf.get_rect()
            TextRect.center = (width / 2, height / 2)
            screen.blit(TextSurf, TextRect)

            textSurf = largeText.render(message, True, darklightred)
            textRect = textSurf.get_rect()
            textRect.center = (width / 2, 200)
            screen.blit(textSurf, textRect)

            pygame.display.update()
            clock.tick(fps)

    def quitGame():
        pygame.quit()
        sys.exit()

    def unpause():
        global pause
        pause = False

    def pause():
        largeText = pygame.font.SysFont("comicsansms", 115)
        TextSurf = largeText.render("Paused", True, black)
        TextRect = TextSurf.get_rect()
        TextRect.center = (width / 2, height / 2)
        screen.blit(TextSurf, TextRect)

        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((176, 224, 230))

            button("Continue", 150, 450, 100, 50, darklightred, lightred, unpause)
            button("Quit", 550, 450, 100, 50, darklightblue, lightblue, quitgame)

            pygame.display.update()
            clock.tick(fps)

    def textObjects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def main():
        global clock, screen, play
        play = True
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TEK Hangman")

        while True:
            hangman()

    def placeLetter(letter):
        global pick, pickSplit
        space = 10
        wordSpace = 0
        while wordSpace < len(pick):
            text = pygame.font.Font('freesansbold.ttf', 40)
            if letter in pickSplit[wordSpace]:
                textSurf = text.render(letter, True, black)
                textRect = textSurf.get_rect()
                textRect.center = (((150) + space), (200))
                screen.blit(textSurf, textRect)
            wordSpace += 1
            space += 60

        pygame.display.update()
        clock.tick(fps)

    def textBoxLetter(letter):
        global textBoxSpace, textBoxNumber
        if textBoxNumber <= 5:
            text = pygame.font.Font("freesansbold.ttf", 40)
            textSurf = text.render(letter, True, red)
            textRect = textSurf.get_rect()
            textRect.center = (((105) + textBoxSpace), (350))
            screen.blit(textSurf, textRect)

        elif textBoxNumber <= 10:
            text = pygame.font.Font("freesansbold.ttf", 40)
            textSurf = text.render(letter, True, red)
            textRect = textSurf.get_rect()
            textRect.center = (((105) + textBoxSpace), (400))
            screen.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(fps)

    def hangman():
        global textBoxSpace, textBoxNumber
        textBoxSpace = 5
        textBoxNumber = 0
        while play == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill((176, 224, 230))
            space = 10
            textBoxSpace = 5
            button("Back", 50, 50, 100, 50, black, lightgrey, main_menu)

            text = pygame.font.Font("freesansbold.ttf", 40)
            textSurf = text.render("Choose a category", True, black)
            textRect = textSurf.get_rect()
            textRect.center = ((width / 2), (height / 2))
            screen.blit(textSurf, (225, 50))

            button("Countries", 300, 150, 200, 75, black, lightgrey, Countries)
            button("Cars", 300, 240, 200, 75, black, lightgrey, Vehicles)
            button("Food", 300, 330, 200, 75, black, lightgrey, Foods)
            button("Sport", 300, 420, 200, 75, black, lightgrey, Sports)

            pygame.display.update()
            clock.tick(fps)

    def hangmanGame(catagory, title):
        global pause, pick, pickSplit, textBoxSpace, textBoxNumber, start
        start = timer()
        chances = 7
        pick = random.choice(catagory)
        pickSplit = [pick[i:i + 1] for i in range(0, len(pick), 1)]

        screen.fill((176, 224, 230))

        wordSpace = 0
        space = 10
        while wordSpace < len(pick):
            text = pygame.font.Font("freesansbold.ttf", 40)
            textSurf1 = text.render("_", True, black)
            textRect1 = textSurf1.get_rect()
            textRect1.center = (((150) + space), (200))
            screen.blit(textSurf1, textRect1)
            space = space + 60
            wordSpace += 1

        guesses = ''
        gamePlay = True
        while gamePlay == True:
            guessLett = ''

            if textBoxNumber == 5:
                textBoxSpace = 5
            if textBoxNumber == 10:
                textBoxSpace = 5
            if textBoxNumber == 15:
                textBoxSpace = 5

            screen.fill((176,224, 230), (650, 50, 690, 40))
            #pygame.draw.rect(screen, white, [550, 20, 200, 20])
            text = pygame.font.Font("freesansbold.ttf", 20)
            textSurf = text.render(("Tries: %s" % chances), False, black)
            textRect = textSurf.get_rect()
            textRect.topright = (700, 50)
            screen.blit(textSurf, textRect)

            textTitle = pygame.font.Font("freesansbold.ttf", 40)
            textTitleSurf = textTitle.render(title, True, black)
            textTitleRect = textTitleSurf.get_rect()
            textTitleRect.center = ((width / 2), 50)
            screen.blit(textTitleSurf, textTitleRect)

            threeImg = pygame.image.load("3.png")
            fourImg = pygame.image.load("4.png")
            fiveImg = pygame.image.load("5.png")
            sixImg = pygame.image.load("6.png")
            sevenImg = pygame.image.load("7.png")
            eightImg = pygame.image.load("8.png")
            nineImg = pygame.image.load("9.png")

            finalX = 400
            finalY = 280

            screen.blit(threeImg, (finalX, finalY))

            if chances == 6:
                screen.blit(fourImg, (finalX, finalY))

            elif chances == 5:
                screen.blit(fiveImg, (finalX, finalY))
            elif chances == 4:
                screen.blit(sixImg, (finalX, finalY))
            elif chances == 3:
                screen.blit(sevenImg, (finalX, finalY))
            elif chances == 2:
                screen.blit(eightImg, (finalX, finalY))
            elif chances == 1:
                screen.blit(nineImg, (finalX, finalY))

            button("Back", 50, 50, 100, 50, black, lightgrey, hangman)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    failed = 0
                    print("Failed", failed)
                    print("Chance", chances)

                    if event.key == pygame.K_SPACE:
                        pause()

                    if event.key == pygame.K_ESCAPE:
                        gamePlay = False

                    if event.key == pygame.K_a:
                        # letter a
                        guessLett = guessLett + 'a'
                        guesses += guessLett
                        print("letter a guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('a')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('a')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_b:
                        # letter b
                        guessLett = guessLett + 'b'
                        guesses += guessLett
                        print("letter b guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('b')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('b')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_c:
                        # letter c
                        guessLett = guessLett + 'c'
                        guesses += guessLett
                        print("letter c guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('c')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('c')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_d:
                        # letter d
                        guessLett = guessLett + 'd'
                        guesses += guessLett
                        print("letter d guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('d')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('d')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_e:
                        # letter e
                        guessLett = guessLett + 'e'
                        guesses += guessLett
                        print("letter e guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('e')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('e')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_f:
                        # letter f
                        guessLett = guessLett + 'f'
                        guesses += guessLett
                        print("letter f guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('f')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('f')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_g:
                        # letter g
                        guessLett = guessLett + 'g'
                        guesses += guessLett
                        print("letter g guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('g')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('g')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_h:
                        # letter h
                        guessLett = guessLett + 'h'
                        guesses += guessLett
                        print("letter h guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('h')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('h')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_i:
                        # letter i
                        guessLett = guessLett + 'i'
                        guesses += guessLett
                        print("letter i guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('i')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('i')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_j:
                        # letter j
                        guessLett = guessLett + 'j'
                        guesses += guessLett
                        print("letter j guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('j')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            # gamePlay = False
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('j')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            # gamePlay = False
                            endGame()

                    if event.key == pygame.K_k:
                        # letter k
                        guessLett = guessLett + 'k'
                        guesses += guessLett
                        print("letter k guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('k')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('k')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_l:
                        # letter l
                        guessLett = guessLett + 'l'
                        guesses += guessLett
                        print("letter l guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('l')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('l')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_m:
                        # letter m
                        guessLett = guessLett + 'm'
                        guesses += guessLett
                        print("letter m guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('m')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('m')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_n:
                        # letter n
                        guessLett = guessLett + 'n'
                        guesses += guessLett
                        print("letter n guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('n')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            # gamePlay = False
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('n')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            # gamePlay = False
                            endGame()

                    if event.key == pygame.K_o:
                        # letter o
                        guessLett = guessLett + 'o'
                        guesses += guessLett
                        print("letter o guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('o')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('o')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_p:
                        # letter p
                        guessLett = guessLett + 'p'
                        guesses += guessLett
                        print("letter p guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('p')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('p')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_q:
                        # letter q
                        guessLett = guessLett + 'q'
                        guesses += guessLett
                        print("letter q guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('a')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('q')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_r:
                        # letter r
                        guessLett = guessLett + 'r'
                        guesses += guessLett
                        print("letter r guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('r')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('r')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_s:
                        # letter s
                        guessLett = guessLett + 's'
                        guesses += guessLett
                        print("letter s guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('s')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('s')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_t:
                        # letter t
                        guessLett = guessLett + 't'
                        guesses += guessLett
                        print("letter t guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('t')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('t')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_u:
                        # letter u
                        guessLett = guessLett + 'u'
                        guesses += guessLett
                        print("letter u guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1
                        if guessLett in pick:
                            placeLetter('u')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('u')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_v:
                        # letter v
                        guessLett = guessLett + 'v'
                        guesses += guessLett
                        print("letter v guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('v')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('v')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_w:
                        # letter w
                        guessLett = guessLett + 'w'
                        guesses += guessLett
                        print("letter w guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('w')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('w')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_x:
                        # letter x
                        guessLett = guessLett + 'x'
                        guesses += guessLett
                        print("letter x guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1
                        if guessLett in pick:
                            placeLetter('x')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('x')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_y:
                        # letter y
                        guessLett = guessLett + 'y'
                        guesses += guessLett
                        print("letter y guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('y')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('y')

                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

                    if event.key == pygame.K_z:
                        # letter z
                        guessLett = guessLett + 'z'
                        guesses += guessLett
                        print("letter z guessed")
                        print("")
                        for char in pick:
                            if char in guesses:
                                print(char)
                            else:
                                print("_")
                                failed += 1

                        if guessLett in pick:
                            placeLetter('z')

                        if failed == 0:
                            print("You got the word")
                            print(pick)
                            endGame()

                        if guessLett not in pick:
                            textBoxSpace += 40
                            textBoxNumber += 1
                            chances = chances - 1
                            print("")
                            print(textBoxNumber)
                            print("")
                            print("That letter is not in the word")
                            textBoxLetter('z')


                        if chances == 0:
                            print("Sorry you have lost")
                            print("The word was", pick)
                            endGame()

            pygame.display.update()
            clock.tick(fps)

        pygame.display.update()
        clock.tick(fps)

    def Countries():
        country = ['croatia', 'russia', 'usa', 'serbia', 'germany', 'italy', 'france', 'netherlands', 'japan', 'china', 'thailand', 'iran', 'iraq', 'brazil', 'chile', 'mexico', 'argentina', 'colombia', 'bolivia', 'venezuela', 'congo', 'cameroon', 'uganda', 'rwanda', 'madagascar', 'australia']
        print("country")
        title = "Countries"
        hangmanGame(country, title)

    def Vehicles():
        vehicle = ['bmw', 'volkswagen', 'audi', 'ford', 'toyota', 'renault', 'opel', 'seat', 'ferrari', 'porsche', 'lamborghini', 'kia', 'nissan', 'peugeot', 'mazda', 'hyundai', 'honda', 'bugatti', 'bentley', 'jaguar']
        print("vehicle")
        title = "Cars"
        hangmanGame(vehicle, title)

    def Foods():
        food = ['apple', 'pear', 'orange', 'plum', 'banana', 'cherry', 'potato', 'onion', 'pickle', 'pumpkin', 'lettuce', 'strawberry', 'pineapple', 'peanuts', 'pizza', 'hamburger', 'eggs', 'cheeseburger', 'sandwich']
        print("food")
        title = "Food"
        hangmanGame(food, title)

    def Sports():
        sport = ['football', 'basketball', 'tennis', 'volleyball', 'swimming', 'running', 'hockey', 'golf', 'karate', 'judo', 'boxing', 'cricket', 'racing' ]
        print("sport")
        title = "Sports"
        hangmanGame(sport, title)

    if __name__ == '__main__':
        main()





main_menu()
