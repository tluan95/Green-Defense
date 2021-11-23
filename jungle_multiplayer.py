import pygame
from pygame import mixer
from pygame.locals import *
import random


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

#define screen size
screen_width = pygame.display.Info().current_w  # 1356
screen_height = pygame.display.Info().current_h
half_screen_width = int(screen_width/2)  # 768
screen = pygame.display.set_mode((screen_width, screen_height))

#background
middle_block = pygame.Rect(half_screen_width - 5, 0, 10, screen_height)

#background
#pl number bigger = higher pollution
pl1 = pygame.image.load('img/Forest-01.jpg')
pl2 = pygame.image.load('img/Forest-02.jpg')
pl3 = pygame.image.load('img/Forest-03.jpg')
pollution_lv1 = pygame.transform.scale(pl1, (screen_width, screen_height))
pollution_lv2 = pygame.transform.scale(pl2, (screen_width, screen_height))
pollution_lv3 = pygame.transform.scale(pl3, (screen_width, screen_height))

#Pollution Story Notice
s1 = pygame.image.load('img/jungle_start.png')
start_img = pygame.transform.scale(s1, (screen_width, screen_height))

#Ending slideshow
end_pic1 = pygame.image.load("img/jungle_result1.png")
end_pic2 = pygame.image.load("img/jungle_result2.png")
end_pic3 = pygame.image.load("img/jungle_result3.png")
rescaled_end_pic1 = pygame.transform.scale(end_pic1, (screen_width, screen_height))
rescaled_end_pic2 = pygame.transform.scale(end_pic2, (screen_width, screen_height))
rescaled_end_pic3 = pygame.transform.scale(end_pic3, (screen_width, screen_height))
display_ending_pic = pygame.display.set_mode((screen_width, screen_height))

#score image
star = pygame.image.load("img/star.png")
star_pic = pygame.transform.scale(star, (80, 80))

#pause
pause_pic = pygame.image.load('img/Button-Pause.png')
bt_Pause = pygame.transform.scale(pause_pic, (200, 200))
small_Pause = pygame.transform.scale(pause_pic, (40, 40))

#Button
btCout = pygame.image.load('img/Button-Continue.png')
btQuit = pygame.image.load('img/Button-Quit.png')
btReturn = pygame.image.load('img/Button-MainMenu.png')
btStart = pygame.image.load('img/Button-Start.png')
bt_Cout = pygame.transform.scale(btCout, (180, 120))
bt_Quit = pygame.transform.scale(btQuit, (180, 120))
bt_Return = pygame.transform.scale(btReturn, (180, 120))
bt_Start = pygame.transform.scale(btStart, (180, 120))

#player 1
left_bin_pic = pygame.image.load("img/green_left_trash_bin.png")
right_bin_pic = pygame.image.load("img/green_right_trash_bin.png")
speed_left_bin_pic = pygame.image.load("img/green_left_trash_bin_speed.png")
speed_right_bin_pic = pygame.image.load("img/green_right_trash_bin_speed.png")

#player 2
left_bin_pic2 = pygame.image.load("img/blue_left_trash_bin.png")
right_bin_pic2 = pygame.image.load("img/blue_right_trash_bin.png")
speed_left_bin_pic2 = pygame.image.load("img/blue_left_trash_bin_speed.png")
speed_right_bin_pic2 = pygame.image.load("img/blue_right_trash_bin_speed.png")


#define game varibale
rows = 2            # No. cloud rows
cols = 2            # No. cloud colum
box_width = 120  # single box width
score = 0
score2 = 0
collection = 0
collection2 = 0
speed = 6
speed2 = 6


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
dust_sound = pygame.mixer.Sound('sound/dust_drop.wav')
water_sound = pygame.mixer.Sound('sound/water_bubble.wav')
special_sound = pygame.mixer.Sound('sound/special_power.wav')


#create player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.transform.scale(left_bin_pic, (int(screen_width/15), int(screen_height/8)))
       self.rect = self.image.get_rect()
       self.rect.center = [x, y]
       self.score = score
       self.collection = collection
       self.speed = speed

    def update(self):
        #set game over
        game_over = 0
        level = 0

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            if self.rect.left > 0:
                self.rect.x -= self.speed
                if self.speed == speed + 4:
                   self.image = pygame.transform.scale(speed_left_bin_pic, (int(screen_width/15), int(screen_height/8)))  # speed buff
                else:
                    self.image = pygame.transform.scale(left_bin_pic, (int(screen_width/15), int(screen_height/8)))  # move effect

        if key[pygame.K_d]:
            if self.rect.right < half_screen_width:
                self.rect.x += self.speed
                if self.speed == speed + 4:
                   self.image = pygame.transform.scale(speed_right_bin_pic, (int(screen_width/15), int(screen_height/8)))  # speed buff
                else:
                    self.image = pygame.transform.scale(right_bin_pic, (int(screen_width/15), int(screen_height/8)))  # move effect
      
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        #draw player1
        p1 = "Player 1"
        p1_img = font30.render(p1, True, black)
        screen.blit(p1_img, (half_screen_width/2, 0))

        #draw score box
        screen.blit(star_pic, (5, 5))
        score_txt = ": " + str(self.score) + "/80"
        score_img = font40.render(score_txt, True, black)
        screen.blit(score_img, (100, 15))

        if self.score == -1:
            game_over = -1
        if self.score == 80:
            game_over = 1

        if self.collection == 45:
            posX = self.rect.x
            posY = 0

            createPower = SpecialPower(posX, posY)
            power_group.add(createPower)
            player.collection += 1

        #the background change arrcording different level of rubish collected
        if self.score > 1 and self.score < 40:
            level = 3
        if self.score > 41 and self.score < 66:
            level = 2
        if self.score > 67:
            level = 1

        return game_over, level

#create player class2
#create player class


class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       self.image = pygame.transform.scale(left_bin_pic2, (int(screen_width/15), int(screen_height/8)))
       self.rect = self.image.get_rect()
       self.rect.center = [x, y]
       self.score2 = score2
       self.collection2 = collection2
       self.speed2 = speed2

    def update(self):
        #set game over
        game_over2 = 0
        level2 = 0

        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            if self.rect.left > half_screen_width:
                self.rect.x -= self.speed2
                if self.speed2 == speed + 4:
                   self.image = pygame.transform.scale(speed_left_bin_pic2, (int(screen_width/15), int(screen_height/8)))  # speed buff
                else:
                    self.image = pygame.transform.scale(left_bin_pic2, (int(screen_width/15), int(screen_height/8)))  # move effect

        if key[pygame.K_RIGHT]:
            if self.rect.right < screen_width:
                self.rect.x += self.speed2
                if self.speed2 == speed + 4:
                   self.image = pygame.transform.scale(speed_right_bin_pic2, (int(screen_width/15), int(screen_height/8)))  # speed buff
                else:
                    self.image = pygame.transform.scale(right_bin_pic2, (int(screen_width/15), int(screen_height/8)))  # move effect
      
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        #draw player1
        p2 = "Player 2"
        p2_img = font30.render(p2, True, black)
        screen.blit(p2_img, (half_screen_width + half_screen_width/2, 0))

        #draw score box
        screen.blit(star_pic, (half_screen_width + 5, 5))
        score_txt = ": " + str(self.score2) + "/80"
        score_img = font40.render(score_txt, True, black)
        screen.blit(score_img, (half_screen_width+ 100, 15))

        if self.score2 == -1:
            game_over2 = -1
        if self.score2 == 80:
            game_over2 = 1

        if self.collection2 == 45:
            posX = self.rect.x
            posY = 0

            createPower = SpecialPower(posX, posY)
            power_group.add(createPower)
            player2.collection2 += 1

        #the background change arrcording different level of rubish collected
        if self.score2 > 1 and self.score2 < 40:
            level = 3
        if self.score2 > 41 and self.score2 < 66:
            level = 2
        if self.score2 > 67:
            level = 1

        return game_over2, level2

#create cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       cloud_pic = pygame.image.load("img/cloud1.png")
       self.image = pygame.transform.scale(cloud_pic, (int(screen_width/15), int(screen_height/8)))
       self.rect = self.image.get_rect()
       self.rect.center = [x, y]
       self.move_counter = 0
       self.move_direction = 1  # move right at speed 1

    def update(self):
        edge_couter = (half_screen_width/2) - ((cols/2)* box_width) - 10  # 20 id middle block amount

        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > edge_couter:
            self.move_direction *= -1
            self.move_counter *= self.move_direction


#create rain class
class Rain(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Rain_picture = pygame.image.load("img/sky_resource" + str(random.randint(1, 3))+".png")
        self.image = pygame.transform.scale(Rain_picture, (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.score = 0
        self.x = x

    def update(self):
        self.rect.y += 3
        if self.rect.top > screen_height:
            self.kill()
            if self.x < half_screen_width:
                player.collection += 1  # minus mark
            else:
                player2.collection2 += 1  # minus mark


        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            water_sound.play()
            self.kill()

        if pygame.sprite.spritecollide(self, player_group2, False, pygame.sprite.collide_mask):
            water_sound.play()
            self.kill()


class AcidRain(pygame.sprite.Sprite):
    def __init__(self, x, y):
       pygame.sprite.Sprite.__init__(self)
       acidRain_picture = pygame.image.load("img/acid_rain" + str(random.randint(1, 2))+".png")
       self.image = pygame.transform.scale(acidRain_picture, (70, 70))
       self.rect = self.image.get_rect()
       self.rect.center = [x, y]
       self.x = x

    def update(self):
        self.rect.y += 4
        if self.rect.top > screen_height:
            self.kill()
            if self.x < half_screen_width:
                player.score -= 1  # minus mark
            else:
                player2.score2 -= 1  # minus mark

            pos1 = self.rect.x, self.rect.y
            m = MinusText('-1',  score_font, pos1, screen)
            minus_group.add(m)

        if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
            dust_sound.play()
            self.kill()
            player.score += 1
            pos = self.rect.x, self.rect.y
            s = PlusText('+1',  score_font, pos, screen)
            plus_group.add(s)

        if pygame.sprite.spritecollide(self, player_group2, False, pygame.sprite.collide_mask):
            dust_sound.play()
            self.kill()
            player2.score2 += 1
            pos = self.rect.x, self.rect.y
            s = PlusText('+1',  score_font, pos, screen)
            plus_group.add(s)

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
		self.rect.y = pos[1] - 80
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
            water_sound.play()  # play sound effect
            self.kill()
            player.speed += 4
        if pygame.sprite.spritecollide(self, player_group2, False, pygame.sprite.collide_mask):
            special_sound.play()  # play sound effect
            self.kill()
            player2.speed2 += 4

        self.screen.blit(self.image, self.rect)


#create sprite group
player_group = pygame.sprite.Group()
player_group2 = pygame.sprite.Group()
cloud_group = pygame.sprite.Group()
cloud_group2 = pygame.sprite.Group()
rain_group = pygame.sprite.Group()
acid_rain_group = pygame.sprite.Group()
plus_group = pygame.sprite.Group()
minus_group = pygame.sprite.Group()
power_group = pygame.sprite.Group()

#create boxs
def create_clouds():
    cloud_spawn_location = (half_screen_width/2) - 120 + 60

    for row in range(rows):
        for item in range(cols):
            cloud = Cloud(cloud_spawn_location + item * 120,100 + row * 70)  # width diff =120
            cloud_group.add(cloud)


def create_2nd_clouds():
    cloud_spawn_location2 = (half_screen_width/2) + half_screen_width - 120 + 60

    for row in range(rows):
        for item in range(cols):
            cloud = Cloud(cloud_spawn_location2 + item * 120,100 + row * 70)  # width diff =120
            cloud_group2.add(cloud)


#create player
player = Player(int(half_screen_width / 2), screen_height - 80)
player_group.add(player)

player2 = Player2(int(half_screen_width / 2) +half_screen_width, screen_height - 80)
player_group2.add(player2)

def emptyGroup():
    player_group.remove()
    player_group2.remove()
    cloud_group.remove()
    cloud_group2.remove()

def draw_bg(screenNum, screenNum2):

    if screenNum == 3:
        screen.blit(pollution_lv3, (0, 0))
    if screenNum == 2:
        screen.blit(pollution_lv2, (0, 0))
    if screenNum == 1:
        screen.blit(pollution_lv1, (0, 0))

    if screenNum2 == 3:
        screen.blit(pollution_lv3, (half_screen_width, 0))
    if screenNum2 == 2:
        screen.blit(pollution_lv2, (half_screen_width, 0))
    if screenNum2 == 1:
        screen.blit(pollution_lv1, (half_screen_width, 0))
    
    pygame.draw.rect(screen, (0, 0, 0), middle_block)

#define for create text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()


def img_button(img, x, y, action=None):
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
    pygame.draw.rect(screen, white, pygame.Rect(int(screen_width / 2 - 190), int(screen_height/2-50), 380, 120))
    screen.blit(TextSurf, TextRect)
    screen.blit(bt_Pause, (screen_width/2 - 100, screen_height/2 - 300))

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    unpause()

        img_button(bt_Cout, screen_width/2 - 350, screen_height - 250, unpause)
        img_button(bt_Quit, screen_width/2 + 200,screen_height - 250, quitgame)

        pygame.display.update()
        clock.tick(60)

def startPage():

    screen.blit(start_img, (0, 0))
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    unpause()

        draw_text("Click Start Or Press 'Space Bar' To  Continue ", font30, black, int(screen_width / 2 - 220), int(screen_height- 25))
        img_button(bt_Start, screen_width/2 - 100, screen_height - 150, unpause)

        pygame.display.update()
        clock.tick(60)

def MP_game():

    #define initial game varibale
    drop_intervel = 1000
    last_item_drop = pygame.time.get_ticks()
    countdown = 3
    last_count = pygame.time.get_ticks()
    game_over = 0
    game_over2 = 0
    level = 0
    level2 = 0
    defaultScreen = 3
    defaultScreen2 = 3  # Set default start screen

    emptyGroup()
    create_clouds()
    create_2nd_clouds()

    run = True
    first = True
    global pause
    global play

    while run:

        clock.tick(fps)

        #draw background
        draw_bg(defaultScreen, defaultScreen2)
        Event1 = pygame.event.Event(pygame.USEREVENT, attr1='Event1')

        if first:  # only run one time
            pygame.event.post(Event1)

        if countdown == 0:

            #create rubish drop
            acid_rain_fall = random.choice(cloud_group.sprites())
            acid_rain_fall2 = random.choice(cloud_group2.sprites())
            acid_rain = AcidRain(acid_rain_fall.rect.centerx, acid_rain_fall.rect.bottom)
            acid_rain2 = AcidRain(acid_rain_fall2.rect.centerx, acid_rain_fall2.rect.bottom)

            #create rain drop
            rain_drop = random.choice(cloud_group.sprites())
            rain_drop2 = random.choice(cloud_group2.sprites())
            rain = Rain(rain_drop.rect.centerx, rain_drop.rect.bottom) or Rain(rain_drop2.rect.centerx, rain_drop2.rect.bottom)
            rain2 = Rain(rain_drop2.rect.centerx, rain_drop2.rect.bottom)

            #create random drop
            #record current time
            time_now = pygame.time.get_ticks()
            #drop
            if time_now - last_item_drop > drop_intervel and len(acid_rain_group) < 3 and len(cloud_group) > 0:
                if (acid_rain_fall != rain_drop):
                    if (acid_rain_fall2 != rain_drop2):
                        acid_rain_group.add(acid_rain)
                        acid_rain_group.add(acid_rain2)
                        rain_group.add(rain)
                        rain_group.add(rain2)

                        last_item_drop = time_now

            if game_over == 0 and game_over2 == 0:


                #update player
                game_over, level = player.update()
                game_over2, level2 = player2.update()

                #update sprite groups
                cloud_group.update()
                cloud_group2.update()
                acid_rain_group.update()
                rain_group.update()
                plus_group.update()
                minus_group.update()
                power_group.update()

                #draw sprite groups
                player_group.draw(screen)
                player_group2.draw(screen)
                cloud_group.draw(screen)                    
                cloud_group2.draw(screen)
                acid_rain_group.draw(screen)
                rain_group.draw(screen)
                plus_group.draw(screen) 
                minus_group.draw(screen) 
                power_group.draw(screen)

            else:
                if (game_over == -1 or game_over2 == 1):
                    draw_text("Player 2 Win!", font40, black, int(half_screen_width / 2 - 80), int(screen_height/2))  # player 1 screen
                    draw_text("You Win!", font40, black, (int(half_screen_width / 2 - 80) +half_screen_width), int(screen_height/2))  # player2 screen
                    img_button(bt_Return, screen_width/2 - 350, screen_height - 250, returnMain)
                    img_button(bt_Quit, screen_width/2 + 200, screen_height - 250, quitgame)
        
                if (game_over == 1 or game_over2 == -1):
                    draw_text("You Win!", font40, black, int(half_screen_width / 2 - 80), int(screen_height/2))  # player 1 screen
                    draw_text("Player 1 Win!", font40, black, (int(half_screen_width / 2 - 80) + half_screen_width), int(screen_height/2))  # player2 screen
                    img_button(bt_Return, screen_width/2 - 350, screen_height - 250, returnMain)
                    img_button(bt_Quit, screen_width/2 + 200, screen_height - 250, quitgame)
        
            if level == 3:
                defaultScreen = 3
                if level2 == 3:
                    defaultScreen2 = 3
                if level2 == 2:
                    defaultScreen2 = 2
                if level2 == 1:
                    defaultScreen2 = 1

            if level == 2:
                defaultScreen = 2
                if level2 == 3:
                    defaultScreen2 = 3
                if level2 == 2:
                    defaultScreen2 = 2
                if level2 == 1:
                    defaultScreen2 = 1

            if level == 1:
                defaultScreen = 1
                if level2 == 3:
                    defaultScreen2 = 3
                if level2 == 2:
                    defaultScreen2 = 2
                if level2 == 1:
                    defaultScreen2 = 1

        if countdown > 0:
            # Player1
            pygame.draw.rect(screen, white, pygame.Rect(int(half_screen_width / 2 - 180), int(screen_height/2-100), 360, 160))
            draw_text("Get Ready", font80, black, int(half_screen_width / 2 - 140), int(screen_height/2- 100))
            draw_text(str(countdown), font40, black, int(half_screen_width / 2), int(screen_height/2 ))

            # Player 2
            pygame.draw.rect(screen, white, pygame.Rect(int(half_screen_width / 2 - 180)+ half_screen_width, int(screen_height/2-100), 360, 160))
            draw_text("Get Ready", font80, black, (int(half_screen_width / 2 - 140) + half_screen_width), int(screen_height/2- 100))
            draw_text(str(countdown), font40, black, (int(half_screen_width / 2 ) + half_screen_width), int(screen_height/2 ))

            count_timer = pygame.time.get_ticks()
            if count_timer - last_count > 1000:
                countdown -= 1
                last_count = count_timer

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == KEYDOWN :
                if event.key == K_ESCAPE or event.key == pygame.K_p:
                    pause = True
                    paused()

            if event == Event1:
                first = False  # stop the event only run 1 time
                pause = True
                countdown = 3
                startPage()

        pygame.display.update()


MP_game()
