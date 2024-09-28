import random
import sys
import pygame
from pygame import *
from pygame.locals import *

window_width = 600
window_height = 400
window = pygame.display.set_mode((window_width, window_height))

offset = window_height / 3

elevation = window_height * 0.8
framepersecond = 32

game_images = {}
pipe_image = "C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\pipe.png"
background_image = "C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\background.jpg"
bird_image = "C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\bird.png"
gameOver_image = "C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\gameover.png"

black = (0, 0, 0)


def main():
    pygame.init()
    framePerSecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    game_images['score'] = (
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\0.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\1.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\2.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\3.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\4.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\5.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\6.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\7.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\8.png").convert_alpha(),
        pygame.image.load("C:\\Users\\Rene Algrably\\Desktop\\ME\\Projects\\Flappy Bird\\pics\\9.png").convert_alpha()
    )

    bird_size = (50, 30)
    game_images['bird'] = pygame.transform.scale(pygame.image.load(bird_image).convert_alpha(), bird_size)

    # game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()

    background = pygame.image.load(background_image).convert_alpha()
    game_images['background'] = pygame.transform.scale(background, (window_width, window_height))

    # puts the 2 pipes together, one above the other
    original_pipe = pygame.image.load(pipe_image).convert_alpha()
    resized_pipe = pygame.transform.scale(original_pipe, (80, 200))
    game_images['pipe'] = (pygame.transform.rotate(resized_pipe, 180), resized_pipe)

    gameOver = pygame.image.load(gameOver_image).convert_alpha()
    game_images['gameOver'] = pygame.transform.scale(gameOver, (window_width, window_height))

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    running = True

    while running:
        xBird = int(window_width / 5)  # horizontal
        yBird = int((window_height - game_images['bird'].get_height()) / 2)  # vertical

        for event in pygame.event.get():
            # if user clicks on cross button or escape, close the game
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # If the user presses space or up key, start the game
            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                startGame(framePerSecond_clock, xBird, yBird)

            # if user doesn't press any key we go back to main screen
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['bird'], (xBird, yBird))
                # window.blit(game_images['sea_level'], (ground, elevation))

                # to refresh the screen
                pygame.display.update()

                # set the rate of frame per second
                framePerSecond_clock.tick(framepersecond)

    pygame.quit()
    sys.exit()


def changeGap():
    # newGap = random.randint(50, 150)
    newGap = random.randrange(70, 150, 10)
    print(newGap)
    return newGap


# def gameOver(xBird, yBird, pipeX, pipeY):
def gameOver(xBird, yBird, pipeTop, pipeBottom):
    # pipeX = pipeTop[0]
    # pipeY = pipeTop[1]
    # rotatePipeY = pipeBottom[1]

    pipesX = pipeTop[0]
    pipeTopY = pipeTop[1]
    pipeBottomY = pipeBottom[1]

    # rotatePipeY = -1 * (game_images['pipe'][0].get_height() - pipeY + offset)

    # if the bird touched the top or the bottom of the window
    if yBird < 0 or yBird > elevation:
        print("first condition")
        return True

    if ((xBird + game_images['bird'].get_width() >= pipesX and
         xBird <= pipesX + game_images['pipe'][0].get_width()) and
            yBird <= pipeTopY + game_images['pipe'][0].get_height()):
        print("second condition")
        return True

    # if the bird touched the bottom pipe
    # if ((xBird + game_images['bird'].get_width() >= pipesX and
    #         xBird <= pipesX + game_images['pipe'][0].get_width()) and
    #         yBird >= pipeBottomY + game_images['pipe'][0].get_height()):
    if ((xBird + game_images['bird'].get_width() >= pipesX and
         xBird <= pipesX + game_images['pipe'][0].get_width()) and
            yBird >= pipeBottomY):
        print("third condition")
        return True

    return False


def startGame(framePerSecond_clock, xBird, yBird):
    playing = True
    score = 0
    speedPipe = -5
    gravity = 3
    speedBird = 0

    myFont = pygame.font.Font(None, 30)  # None uses the default font, 74 is the font size

    x = window_width + 10  # now the pipes will come from outside the window
    gap = changeGap()

    pipeTop = [x, 0 - int(gap / 2)]
    pipeBottom = [x, window_height - game_images['pipe'][0].get_height() + int(gap / 2)]

    while playing:
        for event in pygame.event.get():

            # if quit the game
            if event.type == pygame.QUIT:
                playing = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                playing = False

            # if play the game
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                speedBird = -5  # bird moves up
            elif event.type == pygame.KEYUP and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                speedBird = gravity  # bird falls down

        yBird += speedBird
        # move the pipes to the bird
        pipeTop[0] += speedPipe
        pipeBottom[0] += speedPipe

        if score > 4:
            gravity = 6
        elif score > 9:
            gravity = 9

        # if game over
        if gameOver(xBird, yBird, pipeTop, pipeBottom):
            playing = False
            print("game over, score: ", score)
            gameOverPage(score)

        # Ensured the pipes move left and reset their position when they move out of
        if xBird > pipeTop[0] + game_images['pipe'][0].get_width():
            score += 1
            gap = changeGap()
            pipeTop = [x, 0 - int(gap / 2)]
            pipeBottom = [x, window_height - game_images['pipe'][0].get_height() + int(gap / 2)]

        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['bird'], (xBird, yBird))
        window.blit(game_images['pipe'][0], (pipeTop[0], pipeTop[1]))
        window.blit(game_images['pipe'][1], (pipeBottom[0], pipeBottom[1]))

        scoreText = myFont.render(f'Score: {score}', True, black)
        window.blit(scoreText, (20, 20))

        pygame.display.update()
        framePerSecond_clock.tick(framepersecond)


def gameOverPage(score):
    window.blit(game_images['gameOver'], (0, 0))
    myFont = pygame.font.Font(None, 75)  # Use default font with size 75
    scoreText = myFont.render(f'Score: {score}', True, black)
    window.blit(scoreText, (200, 20))
    pygame.display.update()
    pygame.time.wait(2000)  # Display for 2 seconds before exiting


main()
