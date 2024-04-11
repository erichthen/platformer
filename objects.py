import pygame
import random

class Player:

    def __init__(self, x, y):

        self.rect = pygame.Rect(x, y, 40, 40)
        self.velocity = [0,0]
        self.on_ground = False
        self.waiting_to_respawn = False
        self.standing_on_platform = None
        self.recently_on_last_platform = False # if you are on last platform and jump, this should be valid 
        #to advance to the next level, it is only if you are falling and reach the egde that should trigger a respawn



    def move(self, dx, dy, platforms):
        
        self.standing_on_platform = None

        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0


        self.rect.y += dy

        for platform in platforms:
            
            if self.rect.colliderect(platform.rect) and platform.visible:

                if dx > 0:  # Moving right
                    self.rect.right = platform.rect.left

                elif dx < 0:  # Moving left
                    self.rect.left = platform.rect.right


                if dy > 0:  # Moving down
                    self.rect.bottom = platform.rect.top
                    self.velocity[1] = 0
                    self.on_ground = True
                    self.standing_on_platform = platform

                elif dy < 0:  # Moving up
                    self.rect.top = platform.rect.bottom
                    self.velocity[1] = 0

        

    def update(self, platforms, event):
        

        if not self.waiting_to_respawn:
        
            self.velocity[1] += 1 
            self.on_ground = False
            self.move(self.velocity[0], 0, platforms) 
            self.move(0, self.velocity[1], platforms)
        

            if self.rect.y > 555:
                self.rect.y = 555
                self.velocity[1] = 0
                self.on_ground = True

            if self.standing_on_platform:
            
                if self.standing_on_platform.x_move_speed != 0:
                    self.rect.x += self.standing_on_platform.x_move_speed * self.standing_on_platform.x_direction
            
                if self.standing_on_platform.y_move_speed != 0:
                    self.rect.y += self.standing_on_platform.y_move_speed * self.standing_on_platform.y_direction

                # If on the last platform, if you jump you can still
                #go to the next level despite !standing_on_platform    
                
                if self.standing_on_platform == platforms[-1]: 
                    
                    self.recently_on_last_platform = True     
                    pygame.time.set_timer(event, 1000)  #temporarily activate recently flag
            

        

    def check_lava_collision(self, lava):
        
        return self.rect.colliderect(lava.rect)


    def lava_collide(self):
        
        if not self.waiting_to_respawn:

            self.rect.x, self.rect.y = -100, -100 #get it offscreen
            self.waiting_to_respawn = True    

           
    def respawn(self, spawn_point):
        
       
        self.rect.x, self.rect.y = spawn_point 
        self.waiting_to_respawn = False
        self.velocity = [0, 0]  
    


    def jump(self):
        if self.on_ground:
            self.velocity[1] -= 15
            self.on_ground = False
        

    def render(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)




class Platform:


    def __init__(self, x, y, width, height, color, 
                 x_speed = 0, x_distance = 0, y_speed = 0, y_distance = 0, disappear = False, diss_time = 0):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.color = color
        self.x_move_speed = x_speed
        self.x_distance = x_distance
        self.y_move_speed = y_speed
        self.y_distance = y_distance
        self.x_direction = 1
        self.y_direction = 1
        self.disappear = disappear
        self.visible = True
        self.last_toggle_time = pygame.time.get_ticks() if disappear else None #only matters if its a disappearing platform
        self.diss_time = diss_time #time in between appearing



    def update(self):

        if self.visible:
        
            if self.x_move_speed != 0:
                self.rect.x += self.x_move_speed * self.x_direction
                if abs(self.rect.x - self.start_x) > self.x_distance:
                    self.x_direction *= -1

            if self.y_move_speed != 0:
                self.rect.y += self.y_move_speed * self.y_direction
                if abs(self.rect.y - self.start_y) > self.y_distance:
                    self.y_direction *= -1
    

    def render(self, screen): 
            if self.visible:
                pygame.draw.rect(screen, self.color, self.rect) #pass in an rgb val

    def toggle_visibility(self):
        self.visible = not self.visible
        self.last_toggle_time = pygame.time.get_ticks()


    def disappear_platform(self):
       if self.disappear and pygame.time.get_ticks() - self.last_toggle_time > self.diss_time:  # 2 seconds
            self.toggle_visibility()
            self.last_toggle_time = pygame.time.get_ticks()



class Lava:
    
    def __init__(self, x, y, w, h, rising_speed = 0):
        self.rect = pygame.Rect(x, y, w, h)
        self.rising_speed = rising_speed

    def update(self):
        self.rect.y -= self.rising_speed

    def render(self, screen):
        pygame.draw.rect(screen, (255,0,0), self.rect)

    def reset(self):
        self.rect.x, self.rect.y = 0, 580



class FallingLava:

    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.fall_speed = random.randint(3, 7)

    def update(self):
        self.rect.y += self.fall_speed

    def render(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)