import pygame
import random
from objects import Player, Platform, Lava, FallingLava


pygame.init()


WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)

FIRST_LEVEL_SPAWN_POINT = (75, 400)
FPS = 60

RESET_FLAG = pygame.USEREVENT + 1


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("blok gam")
clock = pygame.time.Clock()


current_level = 1


player = Player(*FIRST_LEVEL_SPAWN_POINT) 


lava = Lava(0, 580, 600, 600)

falling_lava_blocks = []

#todo: sensibly randomize platform gen
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

    Platform(0, 560, 600, 20, GREEN),
    Platform(300, 510, 80, 20, GREEN),
    Platform(375, 460, 80, 20, GREEN),
    Platform(450, 410, 80, 20, GREEN),
    Platform(525, 360, 100, 20, MAGENTA),


]

platforms_level_6 = [

    Platform(0, 360, 80, 20, MAGENTA)

]

level_5_start_time = None
staircase_appeared = False

#might want to make as a class when you add more than just platforms
levels = {
    1: {
        "platforms": platforms_level1,
        
    },

    2: {
        "platforms": platforms_level2,

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
        "platforms" : platforms_level_6
    }

}


running = True

while running:

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
            pygame.time.set_timer(pygame.USEREVENT, 0) 
      

        if event.type == RESET_FLAG:
            player.recently_on_last_platform = False
            pygame.time.set_timer(RESET_FLAG, 0) 


    screen.fill(BLACK)


    if current_level == 4:
        lava.rising_speed = 1  
        lava.update()
    else:
        lava.rising_speed = 0  
        lava.reset()  

    if player.check_lava_collision(lava) and not player.waiting_to_respawn:
        player.lava_collide()  
        pygame.time.set_timer(pygame.USEREVENT, 500)  


    elif player.rect.left > WIDTH:

        if player.standing_on_platform or player.recently_on_last_platform:
            current_level += 1
            player.rect.x = 0
            player.recently_on_last_platform = False


        else:

            player.rect.x, player.rect.y = -100, -100
            player.waiting_to_respawn = True
            pygame.time.set_timer(pygame.USEREVENT, 500)


    keys = pygame.key.get_pressed()

    if not player.waiting_to_respawn:

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velocity[0] = -5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velocity[0] = 5
        else:
            player.velocity[0] = 0


    if current_level == 5:

        if level_5_start_time is None:
            level_5_start_time = pygame.time.get_ticks()


        levels[5]["platforms"][0].update()
        levels[5]["platforms"][0].render(screen)


        if pygame.time.get_ticks() - level_5_start_time > 13000 and not staircase_appeared:
            falling_lava_blocks.clear()
            staircase_appeared = True


        if not staircase_appeared:
            if random.randint(0, 100) < 5:
                new_lava_x = random.randint(0, WIDTH - 30)
                falling_lava_blocks.append(FallingLava(new_lava_x, 0, 30))

            for lava_block in falling_lava_blocks[:]:
                lava_block.update()
                lava_block.render(screen)


                if player.rect.colliderect(lava_block.rect):
                    falling_lava_blocks.clear()
                    player.waiting_to_respawn = True
                    pygame.time.set_timer(pygame.USEREVENT, 500)
                    break 


                if lava_block.rect.y > 560:
                    falling_lava_blocks.remove(lava_block)


        if staircase_appeared:
            for i in range(1, len(levels[5]["platforms"])):
                levels[5]["platforms"][i].update()
                levels[5]["platforms"][i].render(screen)


        if not staircase_appeared:
            if player.rect.right > WIDTH:
                player.rect.right = WIDTH
            

    current_platforms = levels[current_level]["platforms"]

    if current_level != 5:

        for platform in current_platforms:
            platform.update()
            platform.render(screen)

    player.update(current_platforms, RESET_FLAG)
    player.check_lava_collision(lava)
    player.render(screen)

    lava.render(screen)
 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

