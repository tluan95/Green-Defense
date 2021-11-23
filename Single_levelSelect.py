from pygame.locals import *
import pygame
import sys


clock = pygame.time.Clock()
pygame.init()

screen_width = pygame.display.Info().current_w  # 1356
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

#background
picture = pygame.image.load('img/level_bg.jpg')
background = pygame.transform.scale(picture, (screen_width, screen_height))

instruction1 = pygame.image.load('img/river_Intro.png')
intro1 = pygame.transform.scale(instruction1, (screen_width -100, int(screen_height/1.4)))
instruction2= pygame.image.load('img/jungle_Intro.png')
intro2 = pygame.transform.scale(instruction2, (screen_width - 100, int(screen_height/1.4)))

bt1 = pygame.image.load('img/Button-01.png')
bt2 = pygame.image.load('img/Button-02.png')
bt3 = pygame.image.load('img/Button-Play.png')
bt_img1 = pygame.transform.scale(bt1, (100, 100))
bt_img2 = pygame.transform.scale(bt2, (100, 100))
bt_imgPlay = pygame.transform.scale(bt3, (150, 150))

font20 = pygame.font.SysFont('freesansbold.ttf', 20)
font32 = pygame.font.Font('freesansbold.ttf', 32)
font45 = pygame.font.Font('freesansbold.ttf',45)
font80 = pygame.font.Font('freesansbold.ttf', 80)


def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    surface.blit(textObj, textRect)


def draw_small_text(text, font, color, surface, x, y, j, k):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.center = ((x+(j/2)), (y+(k/2)))
    surface.blit(textObj, textRect)



def main_menu():
    levelSelected = 0
    running = True

    while running:

        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()
        font80.set_underline(True)
        draw_text('Select Level To Play', font80, (0, 0, 0), screen, screen_width/2 -380, 20)


        button_1 = screen.blit(bt_img1, (screen_width/2 - 250, 120))
        button_2 = screen.blit(bt_img2, (screen_width/2 + 120, 120))
        button_3 = screen.blit(bt_imgPlay, (screen_width/2 + 500, 70))

        if button_1.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                levelSelected = 1
            else:
                pass
        if button_2.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                levelSelected = 2
            else:
                pass

        if button_3.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                if levelSelected == 1:
                    level1()
                if levelSelected == 2:
                    level2()



        if levelSelected == 1:
            showLV1()
        elif levelSelected == 2:
            showLV2()


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()
        clock.tick(60)

def showLV1():
    screen.blit(intro1, (50, screen_height/2 - 200))


def showLV2():
    screen.blit(intro2, (50, screen_height/2 - 200))

def level1():
    import riverStage
    riverStage.game()


def level2():
    import jungleStage
    jungleStage.game()


main_menu()
