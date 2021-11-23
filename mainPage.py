import pygame, sys
from pygame import mixer
from pygame.locals import *


clock = pygame.time.Clock()

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#Background music
mixer.music.load("sound/background.mp3")
mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

pygame.init()

pygame.display.set_caption("Green Defense")
icon = pygame.image.load('img/planet.png')
pygame.display.set_icon(icon)


screen_width = pygame.display.Info().current_w  # 1356
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

#background
picture = pygame.image.load('img/GreenDefense.jpg')
background = pygame.transform.scale(picture, (screen_width, screen_height))

font100 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 80)
font80 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 80)

bt1 = pygame.image.load('img/Button-Singleplayer.png')
bt2 = pygame.image.load('img/Button-Multiplayer.png')
bt3 = pygame.image.load('img/Button-Option.png')
bt4 = pygame.image.load('img/Button-Quit.png')
bt_Single = pygame.transform.scale(bt1, (180, 100))   
bt_Multi = pygame.transform.scale(bt2, (180, 100))
bt_Option = pygame.transform.scale(bt3, (180, 100))
bt_Quit = pygame.transform.scale(bt4, (180, 100))

soundOn = pygame.image.load('img/sound-on.png')
soundOff = pygame.image.load('img/sound-off.png')
bt_On = pygame.transform.scale(soundOn, (180, 100))
bt_Off = pygame.transform.scale(soundOff, (180, 100))



def draw_text(text, font, color, surface, x, y):
    textObj = font.render(text, 1, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x,y)
    surface.blit(textObj,textRect)



def main_menu():
    
    while True:

        screen.blit(background, (0, 0))

        mx, my = pygame.mouse.get_pos()

        button_1 = screen.blit(bt_Single, (screen_width/2 + 180 , screen_height/2 - 250))
        button_2 = screen.blit(bt_Multi, (screen_width/2 + 180, screen_height/2 -100 ))
        button_3 = screen.blit(bt_Option, (screen_width/2 + 180, screen_height/2 +50))
        button_4 = screen.blit(bt_Quit, (screen_width/2 + 180, screen_height/2 + 200))

        if button_1.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                singleplayer()
            else:
                pass
        if button_2.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                multiplayer()
            else:
                pass
        if button_3.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                option()
            else:
                pass
        if button_4.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                quit()
            else:
                pass
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                  pygame.quit()
                  sys.exit()

        
        pygame.display.update()
        clock.tick(60)

def singleplayer():
    import Single_levelSelect
    Single_levelSelect.main_menu()


def multiplayer():
    import Multi_levelSelect
    Multi_levelSelect.main_menu()
    

def option():
    running = True
    music_paused = False
    font100.set_underline(True)
    textUnderline = font100.render("OPTION", True, (255, 128, 0))
    

    while running:

        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(int(screen_width / 2  +50), 200, screen_width/3, screen_height/3))
        screen.blit(textUnderline, (screen_width/2 +200, 220))
        draw_text('Music :', font80, (0, 0, 0), screen, screen_width/2 + 80, 350)

        button = screen.blit(bt_Off, (screen_width/2 + 320, 360))

        if music_paused:
            button = screen.blit(bt_Off, (screen_width/2 + 320 , 360))
        else:
            button = screen.blit(bt_On, (screen_width/2 + 320, 360  ))


        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    # Toggle the boolean variable.
                    music_paused = not music_paused
                    if music_paused:
                        pygame.mixer.music.pause()
                        
                    else:
                        pygame.mixer.music.unpause()

        pygame.display.update()
        clock.tick(60)



main_menu()
