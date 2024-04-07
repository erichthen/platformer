import pygame
from objects import Player, Platform, Lava


pygame.init()


WIDTH, HEIGHT = 600, 600
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)

FIRST_LEVEL_SPAWN_POINT = (75, 400)
FPS = 60

RESET_FLAG = pygame.USEREVENT + 1
LAVA_RISE = pygame.USEREVENT + 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("blok gam")
clock = pygame.time.Clock()


current_level = 1


player = Player(*FIRST_LEVEL_SPAWN_POINT) 


lava = Lava(0, 580, 600, 600)

#for rising lava lvls
lava_rise_set = False
lava_warning = pygame.image.load('warning.png')
arrow_width, arrow_height = lava_warning.get_size()
lava_warning = pygame.transform.scale(lava_warning, (arrow_width // 10, arrow_height // 10))

show_arrow = False


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
    Platform(100, 500, 80, 20, GREEN),
    Platform(225, 400, 80, 20, GREEN),
    Platform(300, 300, 80, 20, GREEN),
    Platform(225, 200, 80, 20, GREEN, x_speed = 2, x_distance = 150),
    Platform(300, 125, 80, 20, GREEN, x_speed = 1, x_distance = 100),
    Platform(500, 50, 100, 20, MAGENTA)
    
]

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
            player.respawn(FIRST_LEVEL_SPAWN_POINT)
            lava.reset()
            lava_rise_set = False
            pygame.time.set_timer(pygame.USEREVENT, 0) 

        if event.type == RESET_FLAG:
            player.recently_on_last_platform = False
            pygame.time.set_timer(RESET_FLAG, 0) 

        if event.type == LAVA_RISE:
            lava.rising_speed = 2
            pygame.time.set_timer(LAVA_RISE, 0)
            show_arrow = False

    screen.fill(BLACK)


    if player.check_lava_collision(lava) and not player.waiting_to_respawn:
        player.lava_collide()  
        pygame.time.set_timer(pygame.USEREVENT, 1000)  
        lava_rise_set = False
        show_arrow = False


    elif player.rect.left > WIDTH:

        if player.standing_on_platform or player.recently_on_last_platform:
            current_level += 1
            player.rect.x = 0
            player.recently_on_last_platform = False
            lava_rise_set = False
            show_arrow = False

        else:

            player.rect.x, player.rect.y = -100, -100
            player.waiting_to_respawn = True
            pygame.time.set_timer(pygame.USEREVENT, 1000)


    keys = pygame.key.get_pressed()

    if not player.waiting_to_respawn:

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.velocity[0] = -5
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.velocity[0] = 5
        else:
            player.velocity[0] = 0
    

    current_platforms = levels[current_level]["platforms"]

    for platform in current_platforms:
        platform.update()
        platform.render(screen)

    player.update(current_platforms, RESET_FLAG)
    player.check_lava_collision(lava)
    player.render(screen)


    #todo: optimize this stuff for more levels
    if current_level == 4 and not lava_rise_set:
        pygame.time.set_timer(LAVA_RISE, 3000)  
        arrow_timer = pygame.time.get_ticks()
        show_arrow = True
        lava_rise_set = True 

    elif current_level != 4 and lava_rise_set:
        lava_rise_set = False
        show_arrow = False 

    if show_arrow:
        
        current_time = pygame.time.get_ticks()
        if current_time - arrow_timer <= 2000: 
            if (current_time // 500) % 2 == 0:
                screen.blit(lava_warning, (450, 500))
        else:
            show_arrow = False

   

    if current_level == 4:
        lava.update()

    lava.render(screen)
 
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

