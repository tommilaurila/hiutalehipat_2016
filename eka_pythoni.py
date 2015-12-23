# -*- coding: utf-8 -*-
# snake game based on thenewboston's pygame tutorials (search on Youtube)
import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
skyblue = (40,195,255)
snow = (148,148,188)

display_width = 800
display_height = 600

apple_size = 30
apple_y_pos = 0

apple_value_plain = 10
apple_value_bonus = 50

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('FlakeSnake')

# graphics selfmade or taken from openclipart.org
game_icon = pygame.image.load('snowflake_white.png')
pygame.display.set_icon(game_icon)

img_snakehead = pygame.image.load('snakehead_green.png')
img_snakebody = pygame.image.load('snakebody_green.png')

img_snowflake_white = pygame.image.load('snowflake_white.png')
img_snowflake_golden = pygame.image.load('snowflake_golden.png')

img_background = pygame.image.load('background2.png')
img_fslogo = pygame.image.load('fslogo.png')
img_snowline = pygame.image.load('snowline.png')

img_moon = pygame.image.load('kuu_96.png')

# sound effect made on bfxr.net
snd_pickup = pygame.mixer.Sound('pickup.wav')
# sound effect from http://freesound.org/people/fins/sounds/171673/
snd_failure = pygame.mixer.Sound('failure.wav')

clock = pygame.time.Clock()

snake_dir = "right"

font_small = pygame.font.SysFont(None, 24)
font_medium = pygame.font.SysFont(None, 34)
font_large = pygame.font.SysFont(None, 44)

# () = tuple
# [] = list


def pause():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Paused",
                          black,
                          -100,
                          size="large")
        message_to_screen("Press C to continue or Q to quit",
                          black,
                          -70)
        pygame.display.update()
        clock.tick(5)


def score(score):
    text = font_small.render("Pisteet: " + str(score), True, white)
    gameDisplay.blit(text, [4,4])


def generate_apple():
    apple_value = apple_value_plain
    
    # generate new apple random position (at top half of screen)
    rand_apple_x = round(random.randrange(apple_size, display_width-apple_size))
    rand_apple_y = round(random.randrange(0, display_height/2-apple_size))

    # is the new apple a bonus apple?
    apple_type = round(random.randrange(1, 10))

    # lucky number is seven (7), chance 1 out of 10
    if apple_type == 7:
        apple_value = apple_value_bonus

    return rand_apple_x, rand_apple_y, apple_value


def snake(snake_move_speed, block_size, snakelist):
    if snake_dir == "right":
        head = pygame.transform.rotate(img_snakehead, 270)
    if snake_dir == "left":
        head = pygame.transform.rotate(img_snakehead, 90)
    if snake_dir == "up":
        head = img_snakehead
    if snake_dir == "down":
        head = pygame.transform.rotate(img_snakehead, 180)

    # draw snake head
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

##    multiplier = 1
##
    for x_y in snakelist[:-1]:
##        if snake_dir == "right":
##            x = x_y[0]-20 * multiplier
##            gameDisplay.blit(img_snakebody, (x, x_y[1]))
##        if snake_dir == "left":
##            x = x_y[0]+20 * multiplier
##            gameDisplay.blit(img_snakebody, (x, x_y[1]))
##        if snake_dir == "up":
##            y = x_y[1]+20 * multiplier
##            gameDisplay.blit(img_snakebody, (x_y[0], y))
##        if snake_dir == "down":
##            y = x_y[1]-20 * multiplier
##            gameDisplay.blit(img_snakebody, (x_y[0], y))
##
##        multiplier += 1
        
        gameDisplay.blit(img_snakebody, (x_y[0], x_y[1]))
        #pygame.draw.rect(gameDisplay, black, [x_y[0], x_y[1], block_size, block_size])


def text_objects(text, color, size):
    if size == "small":
        text_surface = font_small.render(text, True, color)
    if size == "medium":
        text_surface = font_medium.render(text, True, color)
    if size == "large":
        text_surface = font_large.render(text, True, color)
        
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    text_surf, text_rect = text_objects(msg, color, size)
    text_rect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(text_surf, text_rect)


def game_intro():
    # intro music by http://freesound.org/people/djgriffin/sounds/251289/
    pygame.mixer.music.load('djgriffin.wav')
    pygame.mixer.music.play(-1)   
    
    intro = True
    apple_fall_speed = 2

    # draw falling flakes
    rand_apple_x, rand_apple_y, apple_value = generate_apple()
    apple_y_pos = rand_apple_y + apple_fall_speed
    
    flake_dir = "right"
    flake_original_x = rand_apple_x
    flake_max_x_displacement = 30
    
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.blit(img_background, (0, 0))
        gameDisplay.blit(img_fslogo, (100, 10))      

        message_to_screen("Sieppaa lumihiutaleita ennen kun ne putoavat maahan ja",
                          white,
                          150,
                          "small")
        message_to_screen("kasvattavat lumihankea. Varo lumihankea ja ruudun reunoja.",
                          white,
                          180,
                          "small")
        message_to_screen("C = uusi peli, P = tauko, Q = lopetus",
                          yellow,
                          230,
                          "small")

        # draw apple zig-zag falling
        if flake_dir == "right" and rand_apple_x < flake_original_x + flake_max_x_displacement:
            rand_apple_x = rand_apple_x + apple_fall_speed
        elif flake_dir == "right" and rand_apple_x >= flake_original_x + flake_max_x_displacement:
            flake_dir = "left"
        elif flake_dir == "left" and rand_apple_x > flake_original_x - flake_max_x_displacement:
            rand_apple_x = rand_apple_x - apple_fall_speed
        elif flake_dir == "left" and rand_apple_x <= flake_original_x - flake_max_x_displacement:
            flake_dir = "right"

        # draw apple
        gameDisplay.blit(img_snowflake_white, (rand_apple_x, apple_y_pos))            
        apple_y_pos += apple_fall_speed
        
        # if apple falls out of screen, generate new apple
        if apple_y_pos > display_height:  
            rand_apple_x, apple_y_pos, apple_value = generate_apple()
            flake_original_x = rand_apple_x

        pygame.display.update()
        clock.tick(20)

    pygame.mixer.music.stop()


# =============== MAIN GAME LOOP ==================
def gameLoop():
    # music by: https://www.freesound.org/people/joshuaempyre/sounds/251461/
    pygame.mixer.music.load('joshuaempyre.wav')
    pygame.mixer.music.play(-1)
    
    tick_rate = 30

    moon_x = 96

    snow_grow_height = 20
    bottom_line = display_height
    
    global snake_dir
    snake_dir = "right"
    snake_move_speed = 4

    block_size = 20

    apple_fall_speed = 3
    missed_apples = 0
    
    gameExit = False
    gameOver = False

    score_points = 0

    lead_x = display_width/2
    lead_y = display_height/2
    # starting direction for movement
    lead_x_change = snake_move_speed
    lead_y_change = 0

    snakelist = []
    snake_length = 1

    # rand_apple_x, rand_apple_y = rand_apple_gen()
    rand_apple_x, rand_apple_y, apple_value = generate_apple()
    apple_y_pos = rand_apple_y + apple_fall_speed

    flake_dir = "right"
    flake_original_x = rand_apple_x
    flake_max_x_displacement = 30
    
    while not gameExit:
        while gameOver == True:
            gameDisplay.fill(white)
            message_to_screen("Game Over",
                              red,
                              y_displace = -50,
                              size="large")
            message_to_screen("Press C to play again or Q to quit",
                              black,
                              -10,
                              size="small")
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_dir = "left"
                    lead_x_change = -snake_move_speed
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_dir = "right"
                    lead_x_change = snake_move_speed
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_dir = "up"
                    lead_y_change = -snake_move_speed
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_dir = "down"
                    lead_y_change = snake_move_speed
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
                elif event.key == pygame.K_z:
                    print("snakelist: " + str(snakelist))

        # snake crosses boundaries (2x block size because we are using the old bottom line value)
        if lead_x >= display_width or lead_x < 0 or lead_y >= bottom_line - block_size or lead_y < 0:
            snd_failure.play()
            pygame.mixer.music.stop()
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        # draw apple zig-zag falling
        if flake_dir == "right" and rand_apple_x < flake_original_x + flake_max_x_displacement:
            rand_apple_x = rand_apple_x + apple_fall_speed
        elif flake_dir == "right" and rand_apple_x >= flake_original_x + flake_max_x_displacement:
            flake_dir = "left"
        elif flake_dir == "left" and rand_apple_x > flake_original_x - flake_max_x_displacement:
            rand_apple_x = rand_apple_x - apple_fall_speed
        elif flake_dir == "left" and rand_apple_x <= flake_original_x - flake_max_x_displacement:
            flake_dir = "right"

        # draw background
        gameDisplay.blit(img_background, (0,0))

        # draw slowly moving moon
        gameDisplay.blit(img_moon, (moon_x, 48))
        moon_x += 0.016

        # change apple image according to value
        if apple_value == apple_value_plain:
            gameDisplay.blit(img_snowflake_white, (rand_apple_x, apple_y_pos))
        elif apple_value == apple_value_bonus:
            gameDisplay.blit(img_snowflake_golden, (rand_apple_x, apple_y_pos))
            
        apple_y_pos += apple_fall_speed
        
        # if apple falls out of screen
        if apple_y_pos > bottom_line:
            missed_apples += 1

            # every fifth apple makes the bottom line snow grow upwards
            if missed_apples % 5 == 0:
                bottom_line -= snow_grow_height
                
            # generate new apple
            rand_apple_x, apple_y_pos, apple_value = generate_apple()
            flake_original_x = rand_apple_x

        # draw bottom line snow and snow edge graphics
        pygame.draw.rect(gameDisplay, snow, [0, bottom_line, display_width, display_height-bottom_line])
        gameDisplay.blit(img_snowline, (0, bottom_line))
        
        # the snake
        snake_head = []                    
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snakelist.append(snake_head)
        if len(snakelist) > snake_length:
            del snakelist[0]

        # snake crash into itself, head it at end of list
        for each_segment in snakelist[:-1]:
            if each_segment == snake_head:
                snd_failure.play()
                pygame.mixer.music.stop()
                gameOver = True

        # draw snake
        snake(snake_move_speed, block_size, snakelist)

        # eat apple = move it to new position
        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_size or lead_x + apple_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_size:
            if lead_y > apple_y_pos and lead_y < apple_y_pos + apple_size:
                snd_pickup.play()
                score_points += apple_value
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                flake_original_x = rand_apple_x               
                snake_length += 1
                #tick_rate += 1
            elif lead_y + block_size > apple_y_pos and lead_y + block_size < apple_y_pos + apple_size:
                snd_pickup.play()
                score_points += apple_value
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                flake_original_x = rand_apple_x               
                snake_length += 1
                #tick_rate += 1

        # calculate and display score based on snake length
        score(score_points)

        pygame.display.update()
        clock.tick(tick_rate)

    # Here ends while not gameExit
    
    pygame.mixer.music.stop()
    pygame.quit()
    quit()

game_intro()
gameLoop()
