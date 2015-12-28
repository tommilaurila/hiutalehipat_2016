# snake game based on thenewboston's pygame tutorials (search on Youtube)
import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
yellow = (255,255,0)
snow = (115,115,167)

display_width = 800
display_height = 600

apple_size = 30
apple_y_pos = 0

apple_value_plain = 10
apple_value_bonus = 50

gameDisplay = pygame.display.set_mode((display_width, display_height)) #, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
pygame.display.set_caption('FlakeSnake')

# a 'clean' copy of the background
copy_of_gd = gameDisplay.copy()

# graphics selfmade or taken from openclipart.org
game_icon = pygame.image.load('snowflake_white.png')
pygame.display.set_icon(game_icon)

img_snakehead = pygame.image.load('snakehead_green.png')
img_snakebody = pygame.image.load('snakebody_green.png')

img_snowflake_white = pygame.image.load('snowflake_white.png')
img_snowflake_golden = pygame.image.load('snowflake_golden.png')

img_background = pygame.image.load('background4.png')
img_fslogo = pygame.image.load('logosnake_500.png')
img_fslogo_text = pygame.image.load('fslogo_text.png')
img_snowline = pygame.image.load('snowline.png')

img_moon = pygame.image.load('kuu_96.png')

btn_play = pygame.image.load('btn_play.png')
btn_stop = pygame.image.load('btn_stop.png')
btn_credits = pygame.image.load('btn_credits.png')

# sound effect made on bfxr.net
snd_pickup = pygame.mixer.Sound('pickup.wav')

# sound effect from http://freesound.org/people/jivatma07/sounds/173858/
snd_pickup_bonus = pygame.mixer.Sound('bonusflake.wav')

# sound effect from http://freesound.org/people/fins/sounds/171673/
snd_failure = pygame.mixer.Sound('failure.wav')

clock = pygame.time.Clock()

snake_dir = "right"

# font by Joanne Taylor (qabbojo@yahoo.com)
font_small = pygame.font.Font('Qarmic_sans_Abridged.ttf',20)
font_medium = pygame.font.Font('Qarmic_sans_Abridged.ttf',34)
font_large = pygame.font.Font('Qarmic_sans_Abridged.ttf',54)

# () = tuple
# [] = list


def score(score):
    text_surf, text_rect = text_objects("Score: " + str(score), white, "small")
    gameDisplay.blit(text_surf, text_rect)


def generate_apple():
    apple_value = apple_value_plain
    
    # generate new apple random position (at top half of screen)
    rand_apple_x = round(random.randrange(apple_size, display_width-apple_size))
    rand_apple_y = round(random.randrange(0, display_height/2))

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

    # use [1:-1] if drawing snake butt
    for x_y in snakelist[:-1]:        
        gameDisplay.blit(img_snakebody, (x_y[0], x_y[1]))
        #pygame.draw.rect(gameDisplay, snakegreen, [x_y[0], x_y[1], block_size, block_size])



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


def game_credits():
    # intro music by http://freesound.org/people/djgriffin/sounds/251289/
    pygame.mixer.music.load('djgriffin.wav')
    pygame.mixer.music.play(-1)   
    
    show_credits = True

    while show_credits:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    show_credits = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # play button
                if pos[0] > 410 and pos[0] < 410+96 and pos[1] > 515 and pos[1] < 515+57:
                    gameLoop()
                # stop button
                if pos[0] > 285 and pos[0] < 285+96 and pos[1] > 515 and pos[1] < 515+57:
                    pygame.quit()
                    quit()
                
        # draw background
        gameDisplay.blit(img_background, (0, 0))

        # draw credits
        message_to_screen("Thanks to",
                          red,
                          -250,
                          size="large")
        message_to_screen("Openclipart.org (most of the graphics)",
                          yellow,
                          -210,
                          size="small")
        message_to_screen("DJGriffin/Freesound.org (intro music)",
                          yellow,
                          -180,
                          size="small")
        message_to_screen("Joshuaempyre/Freesound.org (game music)",
                          yellow,
                          -150,
                          size="small")
        message_to_screen("Jivatma07/Freesound.org (sound effect)",
                          yellow,
                          -120,
                          size="small")
        message_to_screen("Joanne Taylor / qabbojo@yahoo.com (game font)",
                          yellow,
                          -90,
                          size="small")
        message_to_screen("Harrison/sentdex (snake game idea)",
                          yellow,
                          -60,
                          size="small")
        message_to_screen("Bfxr.net (for sound effects)",
                          yellow,
                          -30,
                          size="small")

        # draw buttons
        gameDisplay.blit(btn_play, (410, 515))
        gameDisplay.blit(btn_stop, (285, 515))

        pygame.display.update()
        clock.tick(20)

    pygame.mixer.music.stop()


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

    # draw background
    gameDisplay.blit(img_background, (0, 0))

    # draw snake image
    gameDisplay.blit(img_fslogo, (150, 150))
    gameDisplay.blit(img_fslogo_text, (330, 85))

    # draw buttons
    gameDisplay.blit(btn_play, (410, 515))
    gameDisplay.blit(btn_stop, (285, 515))

    # store a 'clean' image of the background
    copy_of_gd = gameDisplay.copy()

    # update whole screen only once here
    pygame.display.update()

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
                if event.key == pygame.K_z:
                    print("fps " + str(clock.get_fps()))
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                # play button
                if pos[0] > 410 and pos[0] < 410+96 and pos[1] > 515 and pos[1] < 515+57:
                    intro = False
                # stop button
                if pos[0] > 285 and pos[0] < 285+96 and pos[1] > 515 and pos[1] < 515+57:
                    pygame.quit()
                    quit()

        # draw apple zig-zag falling
        if flake_dir == "right" and rand_apple_x < flake_original_x + flake_max_x_displacement:
            rand_apple_x = rand_apple_x + apple_fall_speed
        elif flake_dir == "right" and rand_apple_x >= flake_original_x + flake_max_x_displacement:
            flake_dir = "left"
        elif flake_dir == "left" and rand_apple_x > flake_original_x - flake_max_x_displacement:
            rand_apple_x = rand_apple_x - apple_fall_speed
        elif flake_dir == "left" and rand_apple_x <= flake_original_x - flake_max_x_displacement:
            flake_dir = "right"

        # take a copy from a 'clean' background (copy_of_gd) and blit it to cover old apple image
        dest_rect = pygame.Rect(rand_apple_x-apple_fall_speed, apple_y_pos-apple_fall_speed, apple_size+2*apple_fall_speed, apple_size+2*apple_fall_speed)
        gameDisplay.blit(copy_of_gd, dest_rect, dest_rect)

        # draw new apple image
        gameDisplay.blit(img_snowflake_white, (rand_apple_x, apple_y_pos))
        
        # update only drawn area
        pygame.display.update(dest_rect)

        clock.tick(20)

        apple_y_pos += apple_fall_speed
        
        # if apple falls out of screen, generate new apple
        if apple_y_pos > display_height:  
            rand_apple_x, apple_y_pos, apple_value = generate_apple()
            flake_original_x = rand_apple_x

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
    snake_move_speed = 5

    block_size = 20

    apple_fall_speed = 3
    missed_apples = 0
    
    gameExit = False
    gameOver = False

    score_points = 0
    score_popup_time = 0
    score_popup_value = 0
    score_popup_x = 395
    score_popup_y = 5
    popup_erased = False

    # snake starting point
    lead_x = display_width/4
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

    # draw background
    gameDisplay.blit(img_background, (0,0))

    # take a 'clean' copy of the background
    copy_of_gd = gameDisplay.copy()

    # update whole screen only once here
    pygame.display.update()
    
    while not gameExit:
        while gameOver == True:
            # draw background
            # gameDisplay.blit(img_background, (0, 0))

            # draw buttons
            gameDisplay.blit(btn_play, (410, 360))
            gameDisplay.blit(btn_stop, (285, 360))
            gameDisplay.blit(btn_credits, (352, 450))
            
            message_to_screen("Game Over",
                              red,
                              y_displace = -130,
                              size="large")
            message_to_screen("Your score: " + str(score_points),
                              yellow,
                              -70,
                              size="medium")

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
                    if event.key == pygame.K_z:
                        print("fps " + str(clock.get_fps()))
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    # play button
                    if pos[0] > 410 and pos[0] < 410+96 and pos[1] > 360 and pos[1] < 360+57:
                        gameLoop()
                    # stop button
                    if pos[0] > 285 and pos[0] < 285+96 and pos[1] > 360 and pos[1] < 360+57:
                        gameOver = False
                        gameExit = True
                    # credits button
                    if pos[0] > 352 and pos[0] < 352+96 and pos[1] > 450 and pos[1] < 450+57:
                        game_credits()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_dir != "right":
                    snake_dir = "left"
                    lead_x_change = -snake_move_speed
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT and snake_dir != "left":
                    snake_dir = "right"
                    lead_x_change = snake_move_speed
                    lead_y_change = 0
                elif event.key == pygame.K_UP and snake_dir != "down":
                    snake_dir = "up"
                    lead_y_change = -snake_move_speed
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN and snake_dir != "up":
                    snake_dir = "down"
                    lead_y_change = snake_move_speed
                    lead_x_change = 0
                elif event.key == pygame.K_z:
                    print("fps " + str(clock.get_fps()))
                    
        # snake crosses boundaries
        if lead_x >= display_width or lead_x < 0 or lead_y >= bottom_line - block_size or lead_y < 0:
            snd_failure.play()
            pygame.mixer.music.stop()
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        # draw slowly moving moon
        # take a copy from a 'clean' background (copy_of_gd) and blit it to cover old moon image
        # moon y is hardcoded to 48
##        dest_rect = pygame.Rect(moon_x-1, 48-1, 96+2, 96+2)
##        gameDisplay.blit(copy_of_gd, dest_rect, dest_rect)
##        gameDisplay.blit(img_moon, (moon_x, 48))
##        moon_x += 0.016
        
        # update only drawn area
##        pygame.display.update(dest_rect)

        # draw apple zig-zag falling
        if flake_dir == "right" and rand_apple_x < flake_original_x + flake_max_x_displacement:
            rand_apple_x = rand_apple_x + apple_fall_speed
        elif flake_dir == "right" and rand_apple_x >= flake_original_x + flake_max_x_displacement:
            flake_dir = "left"
        elif flake_dir == "left" and rand_apple_x > flake_original_x - flake_max_x_displacement:
            rand_apple_x = rand_apple_x - apple_fall_speed
        elif flake_dir == "left" and rand_apple_x <= flake_original_x - flake_max_x_displacement:
            flake_dir = "right"

        # take a copy from a 'clean' background (copy_of_gd) and blit it to cover old apple image
        dest_rect = pygame.Rect(rand_apple_x-apple_fall_speed, apple_y_pos-apple_fall_speed, apple_size+2*apple_fall_speed, apple_size+2*apple_fall_speed)
        gameDisplay.blit(copy_of_gd, dest_rect, dest_rect)

        # draw new apple image according to value
        if apple_value == apple_value_plain:
            gameDisplay.blit(img_snowflake_white, (rand_apple_x, apple_y_pos))
        elif apple_value == apple_value_bonus:
            gameDisplay.blit(img_snowflake_golden, (rand_apple_x, apple_y_pos))
        
        # update only drawn area
        pygame.display.update(dest_rect)

        # move apple down according to fall speed
        apple_y_pos += apple_fall_speed
        
        # if apple falls out of screen, erase the apple
        if apple_y_pos+apple_size > bottom_line:
            apple_erase_rect = pygame.Rect(rand_apple_x-apple_fall_speed, apple_y_pos-apple_fall_speed, apple_size+apple_fall_speed, apple_size+apple_fall_speed)
            gameDisplay.blit(copy_of_gd, apple_erase_rect, apple_erase_rect)
            pygame.display.update(apple_erase_rect)
            
            missed_apples += 1

            # every fifth apple makes the bottom line snow grow upwards
            if missed_apples % 5 == 0:
                bottom_line -= snow_grow_height

                # draw bottom line snow and snow edge graphics
                snow_rect = pygame.Rect(0, bottom_line, display_width, display_height-bottom_line)
                gameDisplay.fill(snow, snow_rect)
                # draw snow edge image
                gameDisplay.blit(img_snowline, (0, bottom_line))
                pygame.display.update(snow_rect)

                # copy updated snow edge from gameDisplay to copy_of_gd
                copy_of_gd.blit(gameDisplay, snow_rect, snow_rect)
                
            # generate new apple
            rand_apple_x, apple_y_pos, apple_value = generate_apple()
            flake_original_x = rand_apple_x

        # the snake
        snake_head = []                    
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snakelist.append(snake_head)
        if len(snakelist) > snake_length:
            del snakelist[0]

        # snake crash into itself, head at end of list
        for each_segment in snakelist[:-1]:
            if each_segment == snake_head:
                snd_failure.play()
                pygame.mixer.music.stop()
                gameOver = True

## -------------- begin draw snake ----------------------
##        snake(snake_move_speed, block_size, snakelist)
        if snake_dir == "right":
            head = pygame.transform.rotate(img_snakehead, 270)
        elif snake_dir == "left":
            head = pygame.transform.rotate(img_snakehead, 90)
        elif snake_dir == "up":
            head = img_snakehead
        elif snake_dir == "down":
            head = pygame.transform.rotate(img_snakehead, 180)

        # erase old snake
        for x_y in snakelist[:-1]:
            dest_rect = pygame.Rect(x_y[0]-snake_move_speed, x_y[1]-snake_move_speed, block_size+2*snake_move_speed, block_size+2*snake_move_speed)
            gameDisplay.blit(copy_of_gd, dest_rect, dest_rect)
            #gameDisplay.blit(img_snakebody, (x_y[0], x_y[1]))

        snake_rects = []

        # draw snake head
        # take a copy from a 'clean' background (copy_of_gd) and blit it to cover old apple image
        if snake_dir == "right":
            dest_rect = pygame.Rect(snakelist[-1][0]-snake_move_speed, snakelist[-1][1], block_size+snake_move_speed, block_size)
        elif snake_dir == "left":
            dest_rect = pygame.Rect(snakelist[-1][0], snakelist[-1][1], block_size+snake_move_speed, block_size)
        elif snake_dir == "up":
            dest_rect = pygame.Rect(snakelist[-1][0], snakelist[-1][1], block_size, block_size+snake_move_speed)
        elif snake_dir == "down":
            dest_rect = pygame.Rect(snakelist[-1][0], snakelist[-1][1]-snake_move_speed, block_size, block_size+snake_move_speed)
            
        gameDisplay.blit(copy_of_gd, dest_rect, dest_rect)
        gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

        # add head to snake rects list
        snake_rects.append(dest_rect)

        # draw new snake body parts
        for x_y in snakelist[:-1]:
            snake_rects.append(pygame.Rect(x_y[0]-snake_move_speed, x_y[1]-snake_move_speed, block_size+2*snake_move_speed, block_size+2*snake_move_speed))
            gameDisplay.blit(img_snakebody, (x_y[0], x_y[1]))

        # update drawn snake on screen
        pygame.display.update(snake_rects)

## ---------------- end draw snake ---------------------

        # eat apple = move it to new position
        if lead_x > rand_apple_x and lead_x < rand_apple_x + apple_size or lead_x + apple_size > rand_apple_x and lead_x + block_size < rand_apple_x + apple_size:
            if lead_y > apple_y_pos and lead_y < apple_y_pos + apple_size:
                # erase eaten apple
                apple_erase_rect = pygame.Rect(rand_apple_x-apple_fall_speed, apple_y_pos-apple_fall_speed, apple_size+2*apple_fall_speed, apple_size+2*apple_fall_speed)
                gameDisplay.blit(copy_of_gd, apple_erase_rect, apple_erase_rect)
                pygame.display.update(apple_erase_rect)
                
                if apple_value == apple_value_plain:
                    snd_pickup.play()
                elif apple_value == apple_value_bonus:
                    snd_pickup_bonus.play()
                
                score_points += apple_value
                score_popup_value = apple_value
                score_popup_x = lead_x
                score_popup_y = lead_y
                # 30 is about 1 sec. at 30 fps
                score_popup_time = 30
                popup_erased = False
                
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                apple_y_pos = rand_apple_y
                flake_original_x = rand_apple_x               
                snake_length += 1
                print("snake length: " + str(snake_length) + " fps: " + str(clock.get_fps()))
                if snake_move_speed <= block_size:
                    snake_move_speed += 0.5

            elif lead_y + block_size > apple_y_pos and lead_y + block_size < apple_y_pos + apple_size:
                # erase eaten apple
                apple_erase_rect = pygame.Rect(rand_apple_x-apple_fall_speed, apple_y_pos-apple_fall_speed, apple_size+2*apple_fall_speed, apple_size+2*apple_fall_speed)
                gameDisplay.blit(copy_of_gd, apple_erase_rect, apple_erase_rect)
                pygame.display.update(apple_erase_rect)
                
                if apple_value == apple_value_plain:
                    snd_pickup.play()
                elif apple_value == apple_value_bonus:
                    snd_pickup_bonus.play()
                
                score_points += apple_value
                score_popup_value = apple_value
                score_popup_x = lead_x
                score_popup_y = lead_y
                # 30 is about 1 sec. at 30 fps
                score_popup_time = 30
                popup_erased = False
                
                rand_apple_x, rand_apple_y, apple_value = generate_apple()
                apple_y_pos = rand_apple_y
                flake_original_x = rand_apple_x               
                snake_length += 1
                print("snake length: " + str(snake_length) + " fps: " + str(clock.get_fps()))
                if snake_move_speed < block_size:
                    snake_move_speed += 0.5

        # display eaten apple value in popup
        if score_popup_time > 0:
            if score_popup_value == apple_value_plain:
                # generate surface from score text
                score_surf, score_surf_rect = text_objects(str(apple_value_plain), white, "small")
                gameDisplay.blit(score_surf, [score_popup_x, score_popup_y])
                # update score to screen, [2] and [3] are the score rect's width and height
                pygame.display.update(pygame.Rect(score_popup_x, score_popup_y, score_surf_rect[2], score_surf_rect[3]))

            elif score_popup_value == apple_value_bonus:
                score_surf, score_surf_rect = text_objects(str(apple_value_bonus), yellow, "small")
                gameDisplay.blit(score_surf, [score_popup_x, score_popup_y])
                pygame.display.update(pygame.Rect(score_popup_x, score_popup_y, score_surf_rect[2], score_surf_rect[3]))           
            
        # reduce one from popup display time (stop at -100 to not continue forever)
        if score_popup_time > -100:
            score_popup_time -= 1

        # when popup display time hits zero, erase the popup
        if popup_erased == False and score_popup_time < 1:
            score_surf, score_surf_rect = text_objects(str(apple_value_bonus), white, "small")
            popup_erase_rect = pygame.Rect(score_popup_x, score_popup_y, score_surf_rect[2], score_surf_rect[3])
            gameDisplay.blit(copy_of_gd, popup_erase_rect, popup_erase_rect)
            pygame.display.update(pygame.Rect(score_popup_x, score_popup_y, score_surf_rect[2], score_surf_rect[3]))
            popup_erased = True
            
        # calculate and display score based on snake length (this is done every frame!)
        text_surf, text_rect = text_objects("Score: " + str(score_points), white, "small")
        gameDisplay.blit(copy_of_gd, text_rect, text_rect)
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update(text_rect)
        #score(score_points)

        clock.tick(tick_rate)

    # Here ends while not gameExit
    
    pygame.mixer.music.stop()
    pygame.quit()
    quit()

game_intro()
gameLoop()
