# -*- coding: utf-8 -*-
# by thenewboston pygame tutorials 1-42
import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
skyblue = (40,195,255)

display_width = 800
display_height = 600

block_size = 20

apple_size = 30
apple_y_pos = 0
apple_fall_speed = 5

apple_value_plain = 10
apple_value_bonus = 50

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Matopeli')

game_icon = pygame.image.load('snowflake.png')
pygame.display.set_icon(game_icon)

img_snakehead = pygame.image.load('snakehead.png')
img_snakebody = pygame.image.load('snakebody.png')

img_snowflake_white = pygame.image.load('snowflake_white.png')
img_snowflake_golden = pygame.image.load('snowflake_golden.png')

clock = pygame.time.Clock()

snake_dir = "right"

font_small = pygame.font.SysFont(None, 24)
font_medium = pygame.font.SysFont(None, 34)
font_large = pygame.font.SysFont(None, 44)

# () = tuple
# [] = list

def game_intro():
    intro = True
    
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
            
        gameDisplay.fill(white)
        message_to_screen("Tervetuloa Matopeliin",
                          green,
                          -50,
                          "large")
        message_to_screen("Syo omenoita",
                          red,
                          -20,
                          "medium")
        message_to_screen("Press C to play, P to pause, Q to quit.",
                          red,
                          10,
                          "medium")
        pygame.display.update()


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
    text = font_small.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])


def rand_apple_gen():
    rand_apple_x = round(random.randrange(0, display_width-apple_size))
    rand_apple_y = round(random.randrange(0, display_height-apple_size))

    return rand_apple_x, rand_apple_y


def generate_apple():
    apple_value = apple_value_plain
    
    # generate new apple position
    rand_apple_x = round(random.randrange(0, display_width-apple_size))
    rand_apple_y = round(random.randrange(0, display_height-apple_size))

    # is the new apple a bonus apple?
    apple_type = round(random.randrange(1, 10))

    # lucky number is seven (7), chance 1 out of 10
    if apple_type == 7:
        apple_value = apple_value_bonus

    return rand_apple_x, rand_apple_y, apple_value


def snake(block_size, snakelist):
    if snake_dir == "right":
        head = pygame.transform.rotate(img_snakehead, 270)
    if snake_dir == "left":
        head = pygame.transform.rotate(img_snakehead, 90)
    if snake_dir == "up":
        head = img_snakehead
    if snake_dir == "down":
        head = pygame.transform.rotate(img_snakehead, 180)
        
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    # for-loop up to the next to second last element [:-2]
    for x_y in snakelist[:-1]:
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


# =============== MAIN GAME LOOP ==================
def gameLoop():
    tick_rate = 10
    
    global snake_dir
    snake_dir = "right"
    
    gameExit = False
    gameOver = False

    score_points = 0

    lead_x = display_width/2
    lead_y = display_height/2
    # starting direction for movement
    lead_x_change = tick_rate
    lead_y_change = 0

    snakelist = []
    snake_length = 1

    # rand_apple_x, rand_apple_y = rand_apple_gen()
    rand_apple_x, rand_apple_y, apple_value = generate_apple()
    apple_y_pos = rand_apple_y + apple_fall_speed
    
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
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    snake_dir = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    snake_dir = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    snake_dir = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        # fill background
        gameDisplay.fill(skyblue)

        # draw apple
        if apple_value == apple_value_plain:
            gameDisplay.blit(img_snowflake_white, (rand_apple_x, apple_y_pos))
        elif apple_value == apple_value_bonus:
            gameDisplay.blit(img_snowflake_golden, (rand_apple_x, apple_y_pos))
            
        apple_y_pos += apple_fall_speed
        
        # if apple falls out of screen
        if apple_y_pos > display_height:
            # generate new apple
            rand_apple_x, apple_y_pos, apple_value = generate_apple()

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
                gameOver = True

        # draw snake
        snake(block_size, snakelist)

        # calculate and display score based on snake length
        score(score_points)
        
        pygame.display.update()

        # eat apple = move it to new position
        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_size or lead_x + block_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_size:
            if lead_y > apple_y_pos and lead_y < apple_y_pos + apple_size:
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                score_points += apple_value
                snake_length += 1
                tick_rate += 1
            elif lead_y + block_size > apple_y_pos and lead_y + block_size < apple_y_pos + apple_size:
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                score_points += apple_value
                snake_length += 1
                tick_rate += 1
            
        clock.tick(tick_rate)

    # Here ends while not gameExit

    pygame.quit()
    quit()

game_intro()
gameLoop()
