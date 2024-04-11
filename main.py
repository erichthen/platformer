import pygame
import random
from objects import Player, Platform, Lava, FallingLava


#=======setting up ========
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
HOT_PINK = (255, 0, 127)

text = 'JUMP: spacebar\nMOVE: arrows or <w,a,s,d>\n'
new_lines = text.split('\n')
font = pygame.font.Font('chosen_font.otf', 30) 

FIRST_LEVEL_SPAWN_POINT = (75, 400)
FPS = 60

RESET_FLAG = pygame.USEREVENT + 1

RESPAWN_TIME = 500

continue_arrow = pygame.image.load("green_arrow.png")
continue_arrow_rect = continue_arrow.get_rect()
arrow_scaled_size = (int(continue_arrow_rect.width * 0.2), int(continue_arrow_rect.height * 0.2))
continue_arrow = pygame.transform.scale(continue_arrow, arrow_scaled_size)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("blok gam")

clock = pygame.time.Clock()

current_level = 1

player = Player(*FIRST_LEVEL_SPAWN_POINT) 

lava = Lava(0, 580, 600, 600)

falling_lava_blocks = []

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
    Platform(0, 530, 80, 20, MAGENTA)
]

level_5_start_time = None
show_arrow = False

#might want to make as a class when you add more than just platforms
#this mapping is to easily correspond platforms to current_level var
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
    }
}

#=================== game loop =====================

running = True
while running:

    screen.fill(BLACK)

    #====== event handling ========

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
        
        if event.type == pygame.USEREVENT and player.waiting_to_respawn:
            current_level = 1
            lava.reset()
            player.respawn(FIRST_LEVEL_SPAWN_POINT)
            show_arrow = False
            falling_lava_blocks.clear()
            level_5_start_time = None
            pygame.time.set_timer(pygame.USEREVENT, 0) 
      

        if event.type == RESET_FLAG:
            player.recently_on_last_platform = False
            pygame.time.set_timer(RESET_FLAG, 0) 


    #======= level specific logic =========
            
    if current_level == 1:
        y_off = 50
        for line in new_lines:
            intro_text = font.render(line, True, MAGENTA)
            screen.blit(intro_text, (111, y_off))
            y_off += 35

    if current_level == 4:
        lava.rising_speed = 1  
        lava.update()
    else:
        lava.rising_speed = 0  
        lava.reset()  

    if current_level == 5:

        if level_5_start_time is None:
            level_5_start_time = pygame.time.get_ticks()


        if pygame.time.get_ticks() - level_5_start_time > 13000:
            falling_lava_blocks.clear()
            show_arrow = True
            screen.blit(continue_arrow, (240, 250))


        if not show_arrow:

            if player.rect.right > WIDTH:   #can only progress when falling is done (arrow isnt shown)
                player.rect.right = WIDTH

            if random.randint(0, 100) < 7: # change this val for fall frequency
                new_lava_x = random.randint(0, WIDTH - 30)
                falling_lava_blocks.append(FallingLava(new_lava_x, 0, random.randint(20, 40))) #change rand range for size

            for lava_block in falling_lava_blocks[:]:
                lava_block.update()
                lava_block.render(screen)


                if player.rect.colliderect(lava_block.rect):
                    falling_lava_blocks.clear()
                    player.waiting_to_respawn = True
                    pygame.time.set_timer(pygame.USEREVENT, RESPAWN_TIME)
                    break 

                if lava_block.rect.y > 510:
                    falling_lava_blocks.remove(lava_block)



    #======= collision handling, level advancement  =========
                    

    if player.check_lava_collision(lava) and not player.waiting_to_respawn:
        player.lava_collide()  
        pygame.time.set_timer(pygame.USEREVENT, RESPAWN_TIME)

    elif player.rect.left > WIDTH:

        if player.standing_on_platform or player.recently_on_last_platform:
            current_level += 1
            player.rect.x = 0
            player.recently_on_last_platform = False

        else:

            player.rect.x, player.rect.y = -100, -100
            player.waiting_to_respawn = True
            pygame.time.set_timer(pygame.USEREVENT, RESPAWN_TIME)


    #=== key binding ===
            
    keys = pygame.key.get_pressed()

    if not player.waiting_to_respawn:

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velocity[0] = -5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velocity[0] = 5
        else:
            player.velocity[0] = 0


    #===== updating and rendering ===== 

    current_platforms = levels[current_level]["platforms"]


    for platform in current_platforms:
        platform.update()
        if platform.disappear:
            platform.disappear_platform()
        platform.render(screen)

    player.update(current_platforms, RESET_FLAG)
    player.check_lava_collision(lava)
    player.render(screen)

    lava.render(screen)
 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

