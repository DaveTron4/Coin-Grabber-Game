import pygame, random

def draw_ellipse_angle(surface, color, rect, angle, image=None, width=0):
    target_rect = pygame.Rect(rect)
    shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
    pygame.draw.ellipse(shape_surf, color, (0, 0, *target_rect.size), width)
    rotated_surf = pygame.transform.rotate(shape_surf, angle)
    
    rotated_rect = rotated_surf.get_rect(center=target_rect.center)
    surface.blit(rotated_surf, rotated_rect.topleft)
    
    if image is not None:
        rotated_image = pygame.transform.rotate(image, angle)
        surface.blit(rotated_image, rotated_rect.topleft)

def random_coin(first_time):
    # coins Images
    #   Silver
    coin_image_silver = pygame.image.load("assets/coin_silver.png")
    coin_image_silver = pygame.transform.scale(coin_image_silver, (64, 100))
    coin_rect_silver = coin_image_silver.get_rect()
    #   Gold
    coin_image_gold = pygame.image.load("assets/coin_gold.png")
    coin_image_gold = pygame.transform.scale(coin_image_gold, (64, 100))
    coin_rect_gold = coin_image_gold.get_rect()
    #   Emerald
    coin_image_emerald = pygame.image.load("assets/coin_emerald.png")
    coin_image_emerald = pygame.transform.scale(coin_image_emerald, (64, 100))
    coin_rect_emerald = coin_image_emerald.get_rect()
    #   Diamond
    coin_image_diamond = pygame.image.load("assets/coin_diamond.png")
    coin_image_diamond = pygame.transform.scale(coin_image_diamond, (64, 100))
    coin_rect_diamond = coin_image_diamond.get_rect()

    if first_time == True:
        #   silver
        coin_rect_silver.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        #   gold
        coin_rect_gold.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        #   emerald
        coin_rect_emerald.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        #   diamond
        coin_rect_diamond.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

    materials = ["silver", "gold", "emerald", "diamond"]
    coins_image = {"silver" : coin_image_silver, "gold" : coin_image_gold, "emerald" : coin_image_emerald, "diamond" : coin_image_diamond}
    coins_rect = {"silver" : coin_rect_silver, "gold" : coin_rect_gold, "emerald" : coin_rect_emerald, "diamond" : coin_rect_diamond}
    coins_value = {"silver" : 1, "gold" : 2, "emerald" : 3, "diamond" : 4}
    coin_material_random = random.choice(materials)

    return coins_image[coin_material_random], coins_rect[coin_material_random], coins_value[coin_material_random]


#Initialize pygame
pygame.init()

#Set display surface
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
BLACK = (0,0,0)
WHITE = (255,255,255)
GOLD = (127,127,0) 
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed the Dragon")

#Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

angle = 0
object_rect = [WINDOW_WIDTH-50, 50, 50, 75] 

star_locs, star_rads = [], []
for i in range(175):
    star_locs.append((random.randint(0,WINDOW_WIDTH),
           random.randint(0,WINDOW_HEIGHT)))
    star_rads.append(random.randint(1,2))

#Set game values
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 10
COIN_ACCELERATION = .5
BUFFER_DISTANCE = 100

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

#Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#Set fonts
font = pygame.font.SysFont(None, 30)

#Set text
score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Feed the Dragon", True, GREEN, WHITE)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)
lives_rect = lives_text.get_rect()
lives_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any key to play again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

#Set sounds and music
coin_sound = pygame.mixer.Sound("assets/coin_sound.mp3")
coin_sound.set_volume(0.3)
miss_sound = pygame.mixer.Sound("assets/coin_sound.mp3")
miss_sound.set_volume(.1)
pygame.mixer.music.load("assets/mario_galaxy_ost.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

#Set images
player_image = pygame.image.load("assets/eye.png")
player_image = pygame.transform.scale(player_image, (64, 64))
player_rect = player_image.get_rect()
player_rect.left = 32
player_rect.centery = WINDOW_HEIGHT//2


coin_image, coin_rect, value = random_coin(True)


#The main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    #Check to see if user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    display_surface.fill(BLACK)

    for index, loc in enumerate(star_locs):
        if(random.random() <= 0.996):
            pygame.draw.circle(display_surface, WHITE, loc, star_rads[index])

    #Check to see if the user wants to move
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y -= PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y += PLAYER_VELOCITY

    #Move the coin
    if coin_rect.x < 0:
        #Player missed the coin
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        #Move the coin
        coin_rect.x -= coin_velocity

    #Check for collisions
    if player_rect.colliderect(coin_rect):
        score += value
        pygame.mixer.Sound.play(coin_sound)
        coin_image, coin_rect, value = random_coin(False)
        coin_velocity += COIN_ACCELERATION
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    #Update HUD
    score_text = font.render("Score: " + str(score), True, GREEN, DARKGREEN)
    lives_text = font.render("Lives: " + str(player_lives), True, GREEN, DARKGREEN)

    #Check for game over
    if player_lives == 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        #Pause the game until player presses a key, then reset the game
        pygame.mixer.music.stop()
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                #The player wants to play again
                if event.type == pygame.KEYDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                #The player wants to quit
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False


    #Blit the HUD to screen
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(lives_text, lives_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    #Blit assets to screen
    display_surface.blit(player_image, player_rect)

    #Class funtion to make coin and rect rotate
    draw_ellipse_angle(display_surface, GOLD, coin_rect, angle, coin_image,width=3)

    #Update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)
    angle += 3
    object_rect[0] -= 2

#End the game
pygame.quit()