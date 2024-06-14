import pygame
from objects import Player, Platform, Lava, FallingLava, Boss


#=======setting up ========

#todo, boost platforms and circular movements

pygame.init()
pygame.font.init() 

pygame.mixer.init()
pygame.mixer.music.load("stuff/background_music.wav")

pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.33)

oof = pygame.mixer.Sound("stuff/died.wav")
jump_sound = pygame.mixer.Sound("stuff/jump.mp3")


#for easier testing, var to spawn at any level and to respawn at the same level
#will make the game annoying by taking this away when finished ;<)
initial_level = 1
current_level = initial_level

#for easier testing, set starting lvl to any lvl assigned to initial_level
#but 30 20 is kinda off on level 1
if current_level == 1:
    SPAWN_POINT = (60, 20)
else:
    SPAWN_POINT = (30, 20)

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
HOT_PINK = (255, 0, 127)

text = 'JUMP: spacebar\nMOVE: arrows or <a,d> or <j,l>\n'
new_lines = text.split('\n') 
font = pygame.font.Font('stuff/chosen_font.otf', 30) 

#FIRST_LEVEL_SPAWN_POINT = (75, 400)
FPS = 60

RESET_FLAG = pygame.USEREVENT + 1

RESPAWN_TIME = 500

continue_arrow = pygame.image.load("stuff/green_arrow.png")
continue_arrow_rect = continue_arrow.get_rect()
arrow_scaled_size = (int(continue_arrow_rect.width * 0.2), int(continue_arrow_rect.height * 0.2))
continue_arrow = pygame.transform.scale(continue_arrow, arrow_scaled_size)

#todo put in function
dead_one = pygame.image.load("stuff/characters/dead_one.jpg")
dead_two = pygame.image.load("stuff/characters/dead_two.jpg")

dead_one_rect = dead_one.get_rect()
dead_two_rect = dead_two.get_rect()
dead_one_scaled = (int(dead_one_rect.width * 0.18), int(dead_one_rect.height * 0.18))
dead_two_scaled = (int(dead_two_rect.width * 0.18), int(dead_two_rect.height * 0.18))

dead_one = pygame.transform.scale(dead_one, dead_one_scaled)
dead_two = pygame.transform.scale(dead_two, dead_two_scaled)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("blok gam")

clock = pygame.time.Clock()

#current_level = 1

#player = Player(*FIRST_LEVEL_SPAWN_POINT) 
player = Player(*SPAWN_POINT)

lava = Lava(0, 580, 600, 600)

falling_lava_blocks_level5 = []
falling_lava_blocks_level8 = []


platforms_level1 = [
    Platform(50, 500, 80, 20, MAGENTA),
    Platform(200, 440, 80, 20, GREEN),
    Platform(400, 350, 80, 20, GREEN),
    Platform(550, 325, 80, 20, MAGENTA),
]
platforms_level2 = [

    Platform(0, 325, 80, 20, MAGENTA),
    Platform(150, 300, 100, 20, GREEN),
    Platform(325, 200, 100, 20, GREEN, y_speed = 2, y_distance = 150),
    Platform(525, 150, 100, 20, MAGENTA),

]
platforms_level3 = [

    Platform(0, 150, 80, 20, MAGENTA),
    Platform(300, 550, 100, 20, GREEN, x_speed = 3, x_distance = 150),
    Platform(425, 450, 80, 20, GREEN),
    Platform(350, 375, 80, 20, GREEN),
    Platform(450, 300, 150, 20, MAGENTA),

]
platforms_level4 = [

    Platform(0, 300, 80, 20, MAGENTA),
    Platform(300, 400, 80, 20, GREEN, x_speed = 4, x_distance = 150),
    Platform(500, 325, 80, 20, GREEN),
    Platform(400, 250, 80, 20, GREEN),
    Platform(300, 175, 80, 20, GREEN),
    Platform(500, 125, 100, 20, MAGENTA)

]
platforms_level5 = [

    Platform(0, 530, 600, 20, GREEN)

]
platforms_level6 = [

    Platform(0, 530, 100, 20, MAGENTA),
    Platform(100, 450, 80, 20, GREEN),
    Platform(200, 370, 80, 20, GREEN),
    Platform(300, 290, 80, 20, HOT_PINK, disappear = True, diss_time = 1000),
    Platform(400, 210, 80, 20, GREEN),
    Platform(500, 130, 80, 20, HOT_PINK, disappear = True, diss_time = 2000),
    Platform(560, 50, 50, 20, MAGENTA)

]
platforms_level7 = [

    Platform(0, 50, 100, 20, MAGENTA),
    Platform(100, 130, 80, 20, GREEN),
    Platform(200, 210, 80, 20, GREEN),
    Platform(400, 370, 80, 20, HOT_PINK, disappear = True, diss_time = 1500),
    Platform(560, 530, 50, 20, MAGENTA)

]

platforms_level8 = [
    
    Platform(0, 530, 80, 20, MAGENTA),
    Platform(220, 480, 180, 20, GREEN, x_speed = 3, x_distance = 125), 
    Platform(475, 390, 80, 20, GREEN),
    Platform(180, 300, 180, 20, GREEN, x_speed = 5, x_distance = 125), 
    Platform(475, 210, 125, 20, MAGENTA)

]

platforms_level9 = [

    Platform(0, 400, 80, 20, MAGENTA),
   

]

platforms_level10 = [

    Platform(0, 210, 100, 20, MAGENTA),
    Platform(150, 310, 500, 20, MAGENTA)

]

platforms_level11 = [
    Platform(0, 310, 100, 20, GREEN),
    Platform(50, 490, 80, 20, GREEN),
    Platform(420, 485, 80, 20, GREEN),
    Platform(150, 390, 80, 20, GREEN),
    Platform(300, 444, 80, 20, GREEN),
    Platform(500, 395, 80, 20, GREEN)
]

level_5_start_time = None
show_arrow = False
space_bar_pressed = False

#map current level var to platforms list 
#todo prob a better way to map this
levels = {
    1: {
        "platforms": platforms_level1
    },
    2: {
        "platforms": platforms_level2
    },
    3: {
        "platforms": platforms_level3
    },
    4: {
        "platforms" : platforms_level4
    },
    5: {
        "platforms" : platforms_level5
    },
    6: {
        "platforms" : platforms_level6
    },
    7: {
        "platforms" : platforms_level7
    },
    8: {
        "platforms" : platforms_level8
    },
    9: {
        "platforms" : platforms_level9
    },
    10: {
        "platforms" : platforms_level10
    },
    11: {
        "platforms" : platforms_level11
    }
}

boss = Boss(250, 410)

#=================== game loop =====================

running = True
while running:

    screen.fill(BLACK)
    

    #====== event handling ========

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_bar_pressed = False

        
        if event.type == pygame.USEREVENT and player.waiting_to_respawn:

            current_level = 1
            lava.reset()
            player.respawn(SPAWN_POINT)
            show_arrow = False
            falling_lava_blocks_level5.clear()
            falling_lava_blocks_level8.clear()
            level_5_start_time = None
            pygame.time.set_timer(pygame.USEREVENT, 0) 

      
        if event.type == RESET_FLAG:
            player.recently_on_last_platform = False
            pygame.time.set_timer(RESET_FLAG, 0) 


    #======= level specific logic =========
    #you NEED to get this shit out of the game loop and put it into functions
    #goal: this section should be consisted of way more function calls and way less direct logic
            
    if current_level == 1:
        y_off = 50
        for line in new_lines:
            intro_text = font.render(line, True, MAGENTA)
            screen.blit(intro_text, (99, y_off))
            y_off += 35

    if current_level == 4:
        lava.rising_speed = 1  
        lava.update()
    else:
        lava.rising_speed = 0  
        lava.reset()  


    if current_level == 5:

        if level_5_start_time == None:

            level_5_start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - level_5_start_time > 13000:
            falling_lava_blocks_level5.clear()
            show_arrow = True
            screen.blit(continue_arrow, (240, 250))


        if not show_arrow:
            FallingLava.spawn_falling_blocks(falling_lava_blocks_level5, spawn_chance = 7,
                width = WIDTH, min_size = 20, max_size = 40, y_start = 0
            )

            collided = FallingLava.update_falling_blocks(falling_lava_blocks_level5, screen, player,
                pygame.USEREVENT, RESPAWN_TIME, y_limit=510
            )
            if collided:

                continue

    elif current_level == 8:

        FallingLava.spawn_falling_blocks(falling_lava_blocks_level8, spawn_chance = 3, 
        width = WIDTH, min_size = 10, max_size = 20, y_start=0
        )

        collided =  FallingLava.update_falling_blocks(falling_lava_blocks_level8, screen, player,
            pygame.USEREVENT, RESPAWN_TIME, y_limit = 580
        )

        if collided:
            
            continue

    if current_level == 10:

        screen.blit(boss.image, (250, 410))
        screen.blit(dead_one, (100, 540))
        screen.blit(dead_two, (480, 540))

    if current_level == 11:

        target_x = 410
        target_y = 25
        boss.update(target_x, target_y)
        boss.render(screen)

    #======= collision handling, level advancement  =========
                    

    if player.check_lava_collision(lava) and not player.waiting_to_respawn:
        oof.play()
        player.lava_collide()  
        pygame.time.set_timer(pygame.USEREVENT, RESPAWN_TIME)


    if current_level == 5 and not show_arrow:
        if player.rect.right >= WIDTH:
            player.rect.right = WIDTH

    elif player.rect.left > WIDTH:

        if player.standing_on_platform or player.recently_on_last_platform or show_arrow:

                current_level += 1
                player.rect.x = 0
                player.recently_on_last_platform = False


        else:

            oof.play()
            player.rect.x, player.rect.y = -100, -100
            player.waiting_to_respawn = True
            pygame.time.set_timer(pygame.USEREVENT, RESPAWN_TIME)


    #=== key binding ===
            
    keys = pygame.key.get_pressed()

    if not player.waiting_to_respawn:


        if keys[pygame.K_SPACE]:
            if not space_bar_pressed:
                jump_sound.play()
                player.jump()
                space_bar_pressed = True

        if keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_j]:
            player.velocity[0] = -5
            if not player.on_ground:
                player.update_image('left', jumping = True)
            else:
                player.update_image('left', jumping = False)

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or keys[pygame.K_l]:
            player.velocity[0] = 5
            if not player.on_ground:
                player.update_image('right', jumping = True)
            else:
                player.update_image('right', jumping = False)

        else:
            player.velocity[0] = 0
            if not player.on_ground:
                player.update_image('still', jumping = True)
            else:
                player.update_image('still', jumping = False)


    #===== updating and rendering ===== 

    current_platforms = levels[current_level]["platforms"]


    for platform in current_platforms:
        platform.update()
        if platform.disappear:
            platform.disappear_platform()
        platform.render(screen)

    player.update(current_platforms, RESET_FLAG)
    player.check_lava_collision(lava)

    #we need to get the lava †
    player.render(screen)

    lava.render(screen)
 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

