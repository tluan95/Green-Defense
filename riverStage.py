import pygame
from pygame import mixer
from pygame.locals import *
import random


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()


clock = pygame.time.Clock()
fps = 60

#set up screen
screen_width = pygame.display.Info().current_w  # 1356
screen_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((screen_width, screen_height))

#background
#pl number bigger = higher pollution
pl1 = pygame.image.load('img/river_PL0.jpg')
pl2 = pygame.image.load('img/river_PL50.jpg')
pl3 = pygame.image.load('img/river_PL100.jpg')
pollution_lv1 = pygame.transform.scale(pl1, (screen_width, screen_height))
pollution_lv2 = pygame.transform.scale(pl2, (screen_width, screen_height))
pollution_lv3 = pygame.transform.scale(pl3, (screen_width, screen_height))

#Ending slideshow
end_pic1 = pygame.image.load("img/result1.png")
end_pic2 = pygame.image.load("img/result2.png")
end_pic3 = pygame.image.load("img/result3.png")
rescaled_end_pic1 = pygame.transform.scale(end_pic1, (screen_width, screen_height))
rescaled_end_pic2 = pygame.transform.scale(end_pic2, (screen_width, screen_height))
rescaled_end_pic3 = pygame.transform.scale(end_pic3, (screen_width, screen_height))
display_ending_pic = pygame.display.set_mode((screen_width, screen_height))

#player
left_net_pic = pygame.image.load("img/yellownetLeft.png")
right_net_pic = pygame.image.load("img/yellownetRight.png")
speed_left_net_pic = pygame.image.load("img/yellow_speed_netLeft.png")
speed_right_net_pic = pygame.image.load("img/yellow_speed_netRight.png")
star = pygame.image.load("img/star.png")
star_pic = pygame.transform.scale(star, (80, 80))

#pause
pause_pic = pygame.image.load('img/Button-Pause.png')
bt_Pause = pygame.transform.scale(pause_pic, (200, 200))
small_Pause = pygame.transform.scale(pause_pic, (40, 40))

#Button
btCout = pygame.image.load('img/Button-Continue.png')
btQuit = pygame.image.load('img/Button-Quit.png')
btReturn = pygame.image.load('img/Button-Continue.png')
btStart = pygame.image.load('img/Button-Start.png')
bt_Cout = pygame.transform.scale(btCout, (180, 120))
bt_Quit = pygame.transform.scale(btQuit, (180, 120))
bt_Return = pygame.transform.scale(btReturn, (180, 120))
bt_Start = pygame.transform.scale(btStart, (180, 120))


#Pollution Story Notice
s1 =pygame.image.load('img/river_start.png')
start_img = pygame.transform.scale(s1, (screen_width, screen_height))

#define game varibale
rows = 1  # No. cloud rows
cols = 4  # No. cloud colum
score = 0
collection = 0
speed = 6

#define colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)

#define fonts
font30 = pygame.font.SysFont('Fonts/PatrickHand-Regular.ttf', 30)
font40 = pygame.font.SysFont('Fonts/PatrickHand-Regular.ttf', 40)
font45 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 45)
font80 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 80)
font120 = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 120)
score_font = pygame.font.Font('Fonts/PatrickHand-Regular.ttf', 50)


#define sound
pull_object = pygame.mixer.Sound('sound/water_pulling.wav')
pull_water = pygame.mixer.Sound('sound/water_bubble.wav')
river_run = pygame.mixer.Sound('sound/river_drop.wav')
special_sound = pygame.mixer.Sound('sound/special_power.wav')
# player_move = pygame.mixer.Sound("sound/player_move.mp3")


#create player class
class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        left_net_pic = pygame.image.load("img/yellownetLeft.png")
        self.image = pygame.transform.scale(left_net_pic, (int(screen_width/10), int(screen_height/6)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.score = score
        self.collection = collection
        self.speed = speed

    def update(self):

        game_over = 0
        level = 0

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
                if self.speed == speed + 4:
                   self.image = pygame.transform.scale(speed_left_net_pic, (int(screen_width/10), int(screen_height/6)))  # speed buff 
                else:
                    self.image = pygame.transform.scale(left_net_pic, (int(screen_width/10), int(screen_height/6)))  # move effect
            
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.rect.right < screen_width:
                self.rect.x += self.speed
                if self.speed == speed+ 4:
                   self.image = pygame.transform.scale(speed_right_net_pic, (int(screen_width/10), int(screen_height/6)))  # speed buff 
                else:
                    self.image = pygame.transform.scale(right_net_pic, (int(screen_width/10), int(screen_height/6)))  # move effect
    
        #update mask
        self.mask = pygame.mask.from_surface(self.image)


        #draw score box
        screen.blit(star_pic,(5, 5))
        score_txt = ": " + str(self.score) + "/50"
        score_img = font40.render(score_txt, True, black)
        screen.blit(score_img, (100, 15))

        pause_txt = "Press 'P' To"
        pause_img = font40.render(pause_txt, True, black)
        screen.blit(pause_img, (screen_width - 210, 15))
        screen.blit(small_Pause,(screen_width -50, 5))

        if self.score == -1:
            game_over = -1
        if self.score == 50:
            game_over = 1

        if self.collection == 3:
            posX = self.rect.x
            posY = 0

            createPower = SpecialPower(posX, posY)
            power_group.add(createPower)
            player.collection += 1

        #the background change arrcording different level of rubish collected
        if self.score > 1 and self.score < 22:
            level = 3 
        if self.score > 23 and self.score < 37:
            level = 2
        if self.score > 38:
            level = 1

        return game_over, level;


#create box class
class Box(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        waterfall_picture = pygame.image.load('img/waterfall.png')
        self.image = pygame.transform.scale(waterfall_picture, (int(screen_width/10), int(screen_height/4)))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1  # move right at speed 1


    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > screen_width/4:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


#create rubish class
class Rubish(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        rubish_picture = pygame.image.load("img/rubish" + str(random.randint(1, 3))+".png")  # random from 3 rubish pic
        self.image = pygame.transform.scale(rubish_picture, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        self.rect.y += 3
        if self.rect.top > screen_height:
            self.kill()
            player.score -= 1 #minus mark
            pos1 = self.rect.x, self.rect.y
            m = MinusText('-1',  score_font, pos1, screen)
            minus_group.add(m)

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            pull_object.play() #play sound effect
            self.kill()
            player.score += 1
            pos = self.rect.x, self.rect.y
            s = PlusText('+1',  score_font, pos, screen)
            plus_group.add(s)



#create water class
class Water(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        resource_picture = pygame.image.load("img/resource" + str(random.randint(1, 4))+".png")  # random from 3 rubish pic
        self.image = pygame.transform.scale(resource_picture, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):

        self.rect.y += 2 
        if self.rect.top > screen_height:
            self.kill()
            player.collection += 1

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            pull_water.play() #play sound effect
            self.kill()
            # player.score += 1  # increase mark


class PlusText(pygame.sprite.Sprite):
	def __init__(self, text, font, pos, screen):
		super(PlusText, self).__init__()
		self.screen = screen
		self.image = font.render(text, True, (0, 100, 0))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 30:
			self.kill()

		self.screen.blit(self.image, self.rect)


class MinusText(pygame.sprite.Sprite):
	def __init__(self, text, font, pos, screen):
		super(MinusText, self).__init__()
		self.screen = screen
		self.image = font.render(text, True, red)
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1] -80
		self.counter = 0

	def update(self):
		self.counter += 1
		if self.counter >= 30:
			self.kill()

		self.screen.blit(self.image, self.rect)


class SpecialPower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        potion_picture = pygame.image.load("img/love-potion.png")  
        self.image = pygame.transform.scale(potion_picture, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.screen = screen

    def update(self):

        self.rect.y += 4
        if self.rect.top > screen_height:
            self.kill()

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            special_sound.play()  # play sound effect
            self.kill()
            player.speed += 4
        
        self.screen.blit(self.image, self.rect)



#create sprite group
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
rubish_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
plus_group = pygame.sprite.Group()
minus_group = pygame.sprite.Group()
power_group = pygame.sprite.Group()

#create player
player = Player(int(screen_width / 2), screen_height - 80)
player_group.add(player)


def create_boxs():
    for row in range(rows):
        for item in range(cols):
            # box = Box(450 + item * 150, 100 + row * 70)
            box = Box(int(screen_width/3) + item * screen_width/10,
                      int(screen_height/6) + row * int(screen_height/10))
            box_group.add(box)


def emptyGroup():
    player_group.remove()
    box_group.remove()

def draw_bg(screenNum):
    if screenNum == 3:
        screen.blit(pollution_lv3, (0, 0))
    if screenNum == 2:
        screen.blit(pollution_lv2, (0, 0))
    if screenNum == 1:
        screen.blit(pollution_lv1, (0, 0))
    # screen.blit(pollution_lv2, (0, 0))

#define for create text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

# def button(msg, x, y, w, h, ic, ac, action=None):
#     pygame.mouse.set_visible(True)
#     mouse = pygame.mouse.get_pos()
#     click = pygame.mouse.get_pressed()

#     if x+w > mouse[0] > x and y+h > mouse[1] > y:
#         pygame.draw.rect(screen, ac, (x, y, w, h))

#         if click[0] == 1 and action != None:
#             action()
#     else:
#         pygame.draw.rect(screen, ic, (x, y, w, h))

#     smallText = pygame.font.SysFont("comicsansms", 20)
#     textSurf, textRect = text_objects(msg, smallText)
#     textRect.center = ((x+(w/2)), (y+(h/2)))
#     screen.blit(textSurf, textRect)


def img_button(img,x,y,action=None):
    pygame.mouse.set_visible(True)
    button = screen.blit(img, (x, y))

    mx, my = pygame.mouse.get_pos()

    if button.collidepoint((mx, my)):
        if pygame.mouse.get_pressed()[0] == 1:
            action()
        else:
            pass


def quitgame():
    pygame.quit()
    quit()
    
    
def returnMain():
    global play
    play = False
    import mainPage
    mainPage.main_menu()

def unpause():
    global pause
    pause = False
    pygame.mouse.set_visible(False)



def paused():

    TextSurf, TextRect = text_objects("Paused", font120)
    TextRect.center = ((screen_width/2), (screen_height/2))
    screen.blit(TextSurf, TextRect)
    screen.blit(bt_Pause, (screen_width/2 -100, screen_height/2 - 300))

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        img_button(bt_Cout, screen_width/2 - 350, screen_height - 250, unpause)
        img_button(bt_Quit, screen_width/2 + 200, screen_height - 250, quitgame)


        pygame.display.update()
        clock.tick(60)


def replay():

    TextSurf, TextRect = text_objects("Game Over", font120)
    TextRect.center = ((screen_width/2), (screen_height/2))
    screen.blit(TextSurf, TextRect)


    while play:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    

        img_button(bt_Return, screen_width/2 - 350, screen_height - 250, returnMain)
        img_button(bt_Quit, screen_width/2 + 200, screen_height - 250, quitgame)
        

        pygame.display.update()
        clock.tick(60)
    


def story1():

    screen.blit(start_img, (0,0))

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    unpause()

        img_button( bt_Start, screen_width/2 -100 , screen_height -150, unpause)
        draw_text("Click Start Or Press 'Space Bar' To  Continue ", font30, black, int(screen_width / 2 - 220), int(screen_height- 25))

        pygame.display.update()
        clock.tick(60)


        
def game():


    #define game varibale
    drop_intervel = 1000
    last_item_drop = pygame.time.get_ticks()
    countdown = 3
    last_count = pygame.time.get_ticks()
    game_over = 0
    level = 0
    defaultScreen = 3  # Set default start screen

    emptyGroup()
    create_boxs()

    #Start the program
    run = True
    first = True
    global pause
    global play
  
    while run:

        clock.tick(fps)

        #draw background
        draw_bg(defaultScreen)
        Event1 = pygame.event.Event(pygame.USEREVENT, attr1='Event1')
        Event2 = pygame.event.Event(pygame.USEREVENT, attr1='Event2')

        if first:  # only run one time
            pygame.event.post(Event1)

        if countdown == 0:

            #create random drop
            #record current time
            time_now = pygame.time.get_ticks()

            #drop
            #create rubish drop
            rubish_fall = random.choice(box_group.sprites())
            rubish = Rubish(rubish_fall.rect.centerx, rubish_fall.rect.bottom)

            #create rain drop
            water_drop = random.choice(box_group.sprites())
            water = Water(water_drop.rect.centerx, water_drop.rect.bottom)


            if time_now - last_item_drop > drop_intervel and len(rubish_group) < 3  and len(box_group) > 0:
                if (rubish_fall != water_drop):
                    rubish_group.add(rubish)
                    water_group.add(water)
                    river_run.play()
                    last_item_drop = time_now

            if game_over == 0:


                #update player
                game_over, level = player.update()  # tuple

                #update sprite groups
                box_group.update()
                rubish_group.update()
                water_group.update()
                plus_group.update()
                minus_group.update()
                power_group.update()

                #draw sprite groups
                player_group.draw(screen)
                box_group.draw(screen)
                rubish_group.draw(screen)
                water_group.draw(screen)
                plus_group.draw(screen)
                minus_group.draw(screen)
                power_group.draw(screen)
                # pygame.mouse.set_visible(False)


            else:
                if game_over == -1:
                    pygame.event.post(Event2)

                if game_over == 1:
                    pygame.mouse.set_visible(True)

                    if player.collection < 66:
                        # a end slide to show result/ story  
                        display_ending_pic.blit(rescaled_end_pic1, (0, 0))
                        draw_text("Well Done! You Keep The River Clean! Thank You. ", font40, white, int(screen_width / 2 - 300), 2)
                        img_button(bt_Quit, screen_width/2 -130, screen_height - 120, quitgame)

                    elif player.collection < 80:
                        # a end slide to show result/ story
                        display_ending_pic.blit(rescaled_end_pic2, (0, 0))
                        draw_text("Well Done! You Keep The River Clean! Thank You. ", font40, white, int(screen_width / 2 - 300), 2)
                        img_button(bt_Quit, screen_width/2 - 130,screen_height - 150, quitgame)

                    elif player.collection > 81:
                        # a end slide to show result/ story
                        display_ending_pic.blit(rescaled_end_pic3, (0, 0))
                        draw_text("Well Done! You Keep The River Clean! Thank You. ", font40, white, int(screen_width / 2 - 300), 2)
                        img_button(bt_Quit, screen_width/2 - 130,screen_height - 150, quitgame)


            # if level == 101:
            #     # if first: #only run one time                
            #     #     pygame.event.post(Event1)

            if level == 3:
                defaultScreen = 3
            if level == 2:
                defaultScreen = 2
            if level == 1:
                defaultScreen = 1


        if countdown > 0:
            draw_text("GET READY", font80, black, int(screen_width / 2 - 150), int(screen_height/2-100))
            draw_text(str(countdown), font45, black, int(screen_width / 2 -20), int(screen_height/2 ))
            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer



        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == pygame.K_p:
                    pause = True
                    paused()

            if event == Event1:
                first = False #stop the event only run 1 time
                pause = True
                countdown = 3
                story1()
            elif event == Event2:
                play = True
                game_over = 0
                replay()
                

        pygame.display.update()
 

game()
