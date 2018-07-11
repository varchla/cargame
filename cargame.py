
import pygame
import time
import random
pygame.init()

crash_sound = pygame.mixer.Sound("music\crash.wav")
pygame.mixer.music.load("music\car.wav")

display_width=1000
display_height=600

black=(0,0,0)
white=(255,255,255)
red=(200,0,0)
green=(0,200,0)
bright_red=(255,0,0)
bright_green=(0,255,0)
blue=(0,0,255)
car_width=87
car_height=100

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A Bit Racey')
clock=pygame.time.Clock()

carImg=pygame.image.load('image\car1.png')
gameIcon=pygame.image.load('image\gameicon.png')
pygame.display.set_icon(gameIcon)

pause=False

def things_dodged(count):
    font=pygame.font.SysFont(None,29)
    text=font.render("Dodged: "+str(count),True,black)
    gameDisplay.blit(text,(0,0))

def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text,font):
    textSurface=font.render(text,True,blue)
    return textSurface,textSurface.get_rect()

def message_display(text):
    largeText=pygame.font.SysFont("comicsansms",100)
    TextSurf,TextRect=text_objects(text,largeText)
    TextRect.center=((display_width/2.0),(display_height/7.0))
    gameDisplay.blit(TextSurf,TextRect)

    pygame.display.update()

    time.sleep(2)
    game_loop()

def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    largeText = pygame.font.SysFont("comicsansms", 100)
    TextSurf, TextRect = text_objects('paused', largeText)
    TextRect.center = ((display_width / 2.0), (display_height / 7.0))
    gameDisplay.blit(TextSurf, TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #gameDisplay.fill(black)

        button1('Play Again', 200, 450, 100, 50, green, bright_green,game_loop)
        button1('STOP!', 700, 450, 100, 50, red, bright_red,quit)
        pygame.display.update()
        clock.tick(15)

def unpaused():
    global pause
    pygame.mixer.music.unpause()
    pause=False

def paused():
    pygame.mixer.music.pause()
    largeText = pygame.font.SysFont("comicsansms", 100)
    TextSurf, TextRect = text_objects('paused', largeText)
    TextRect.center = ((display_width / 2.0), (display_height / 7.0))
    gameDisplay.blit(TextSurf, TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)

        button1('Continue', 200, 450, 100, 50, green, light_green,unpaused)
        button1('STOP!', 700, 450, 100, 50, red, light_red,quit)
        pygame.display.update()
        clock.tick(15)

def button1(msg,wb,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click=pygame.mouse.get_pressed()
    if wb + w > mouse[0] > wb and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay,ac,(wb, y, w, h))
        if click[0]==1 and action!=None:
            action()
    else:
        pygame.draw.rect(gameDisplay,ic,(wb, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((wb + (w / 2)),(y + (h / 2)))
    gameDisplay.blit(TextSurf, TextRect)


def game_intro():
    intro=True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(black)

        largeText = pygame.font.SysFont("comicsansms", 100)
        TextSurf, TextRect = text_objects('Race', largeText)
        TextRect.center = ((display_width / 2.0), (display_height / 7.0))
        gameDisplay.blit(TextSurf, TextRect)

        button1('GO!', 200, 450, 100, 50, green, bright_green,game_loop)
        button1('STOP!', 700, 450, 100, 50, red, bright_red,quit)
        pygame.display.update()
        clock.tick(15)


def game_loop():
    global pause
    pygame.mixer.music.play(-1)
    x=(display_width*0.45)
    y=(display_height*0.8)
    x_change=0
    y_change=0

    thing_startx=random.randrange(0,display_width)
    thing_starty=-600
    thing_speed=7
    thing_width=70
    thing_height=80

    def things1(thingsx,thingsy,thingsw,thingsh,color):
        pygame.draw.rect(gameDisplay,color,[thingsx,thingsy,thingsw,thingsh])

    things_startx = 460
    things_starty = 0
    things_speed = 10
    things_width = 30
    things_height = 300

    dodged=0

    gameExit=False

    while not gameExit:

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_change=-5
                if event.key==pygame.K_RIGHT:
                    x_change=5
                if event.key==pygame.K_UP:
                    y_change=-5
                if event.key==pygame.K_DOWN:
                    y_change=5
                if event.key == pygame.K_p:
                    pause=True
                    paused()
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    x_change=0
                if event.key==pygame.K_UP or event.key==pygame.K_DOWN:
                    y_change=0
        x+=x_change
        y+=y_change

        gameDisplay.fill(white)

        things(thing_startx,thing_starty,thing_width,thing_height,blue)
        thing_starty+=thing_speed

        things1(things_startx, things_starty, things_width, things_height, black)
        things_starty += things_speed

        car(x,y)
        things_dodged(dodged)

        if x>display_width-car_width or x<1:
            crash()

        if thing_starty>display_height:
            thing_starty=0-thing_height
            thing_startx=random.randrange(0,display_width-thing_width)
            dodged+=1
            thing_speed+=1

        if y<thing_starty+thing_height:
            print('y crossover')

            if x>thing_startx and x<thing_startx+thing_width or x+car_width>thing_startx and x+car_width<thing_startx+thing_width:
                print('x crossover')
                crash()

        if y > display_height - car_height or y <1:
            crash()

            #if y > thing_startx and y < thing_startx + thing_height or y + car_height > thing_startx and y + car_height < thing_startx + thing_height:
                #print('yesssss')

        pygame.display.update()
        clock.tick(60)
game_intro()
game_loop()
pygame.quit()
quit()