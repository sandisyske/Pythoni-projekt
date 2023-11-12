import os
from typing import Any, Self
import pygame
import random
import math
from os import listdir
from os.path import isfile, join




pygame.init()

pygame.display.set_caption("Aardejaht")


# Set colors
WHITE = (255, 255, 255)

#gravitatsioon, kui tahta kiiremini, siis saab seda väärtust tõsta
GRAVITY = 2

#screen
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 4

window = pygame.display.set_mode((WIDTH, HEIGHT))

idle = True

# funktsioon, mis keerab tegelase pildi
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("Assets", dir1, dir2)
    # laeb iga faili mis on selles kaustas
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width () // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA,32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            #suurenda pilti
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "") + ""] = sprites

    return all_sprites

# bloki asukoht ja suurus
def get_block(size):
    path = join("Assets", "Backround", "terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    # 0, 0 näitab vasakust äärest, kui kaugel on soovitud rect antud pildil
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
"""
# trepi asukoht ja suurus
def get_trepp(size):
    path = join("Assets", "Backround", "terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(48, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
"""

#player
class Tegelane(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    #gravitatsioon, kui tahta kiiremini, siis saab seda väärtust tõsta
    GRAVITY = 1
    # kasuta sprite pilte
    SPRITES = load_sprite_sheets("Tegelased", "Rebane", 32, 32, True)
    # delay between sprites
    ANIMATION_DELAY = 6

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
         
    def jump(self):
        self.y_vel = -self.GRAVITY * 6
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0


    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0
    
    
    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0


    def loop(self, fps):
        #gravitatsion
        self.y_vel += min(1, self.fall_count/ fps) * self.GRAVITY
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    # funktsioonid landed ja hit_head blockiga collide'ides

    def landed(self):
        self.fall_count = 0 # stop adding gravity
        self.y_vel = 0
        self.jump_count = 0 #double jump reset


    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    # animatsiooni uuendamine iga frame
    def update_sprite(self):
        sprite_sheet = "idle"

    
        if self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2: # also i could add a cool salto triple jump animation
                # double jump animation NEED HERE
                sprite_sheet = "fall"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"

        elif self.x_vel != 0:
            sprite_sheet = "run"
      
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            sprite_sheet = "dig" 
            

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // 
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()
        return sprites


    # update the retangle
    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

# Tausta objektide parent klass
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


 # blokki child klass 
class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

#taustapildid
pine1 = pygame.image.load("Assets/Backround/pine1.png").convert_alpha()
pine2 = pygame.image.load("Assets/Backround/pine2.png").convert_alpha()
mountain = pygame.image.load("Assets/Backround/mountain.png").convert_alpha()
sky = pygame.image.load("Assets/Backround/sky.png").convert_alpha()



scroll = 0
#taust
def draw_bg():
    width_bg = sky.get_width()
    for x in range(4):

        window.blit(sky, (scroll, 0))
        window.blit(mountain, (scroll, HEIGHT - mountain.get_height() - 180))
        window.blit(pine1, (scroll, HEIGHT - pine1.get_height() - 80))
        window.blit(pine2, (scroll, HEIGHT - pine2.get_height()))




def draw(window, rebane, objects, offset_x):
    draw_bg()
    for obj in objects:
        obj.draw(window, offset_x)
    
    rebane.draw(window, offset_x)
    

    pygame.display.update()
"""
    for tile in backround:
        window.blit(bg_image, tile)
"""
    
def handle_vertical_collision(rebane, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(rebane, obj):
            #hitting top of bottom of the object differently
            if dy > 0:
                rebane.rect.bottom = obj.rect.top
                rebane.landed()
            elif dy < 0:
                rebane.rect.top = obj.rect.bottom
                rebane.hit_head()
        collided_objects.append(obj)

    return collided_objects

def collide(rebane, objects, dx):
    rebane.move(dx, 0)
    rebane.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(rebane, obj):
            collided_object = obj
            break

    rebane.move(-dx, 0)
    rebane.update()
    return collided_object


#move ja collision
def handle_move(rebane, objects):
    keys = pygame.key.get_pressed()

    rebane.x_vel = 0
    # kui hakkab glitchima vastu blokki saab lisada PLAYER_VEL * 2
    collide_left = collide(rebane, objects, -PLAYER_VEL*2)
    collide_right = collide(rebane, objects, PLAYER_VEL*2)

    if keys[pygame.K_LEFT] and not collide_left:
        rebane.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        rebane.move_right(PLAYER_VEL)
    ###### aaaaaaa   

    vertical_collide = handle_vertical_collision(rebane, objects, rebane.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]


def main (window):
    clock = pygame.time.Clock()
    

    #backround, bg_image = taust("taust.png")

    #blokid
    block_size = 48

#rebase asukoht !!!
    rebane = Tegelane(100, 632, 50, 50)

    # blokkide asukohad # seda saab kindlasti paremini teha, saab ka csv failiga sisse lugeda mapi, later to do
    floor = [Block(i*block_size, HEIGHT - block_size, block_size) 
             for i in range (-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(block_size, HEIGHT - block_size * 4, block_size), 
               Block(block_size * (13), HEIGHT - block_size * 6, block_size),
               Block(block_size * (14), HEIGHT - block_size * 6, block_size),
               Block(block_size * (15), HEIGHT - block_size * 6, block_size),
               Block(block_size * (15), HEIGHT - block_size * 7, block_size),
               Block(block_size * (14), HEIGHT - block_size * 7, block_size),
               Block(block_size * (16), HEIGHT - block_size * 7, block_size),
               Block(block_size * (7), HEIGHT - block_size * 7, block_size), 
               Block(block_size * (8), HEIGHT - block_size * 7, block_size), 
               Block(block_size * (4), HEIGHT - block_size * 6, block_size),
               Block(block_size * (3), HEIGHT - block_size * 6, block_size),
               Block(block_size * (-2), HEIGHT - block_size * 2, block_size)]
    offset_x = 0
    scroll_area_width = 200
    


    run = True
    while run:
        clock.tick(FPS)

    

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and rebane.jump_count < 2:
                    rebane.jump()
        

        

        rebane.loop(FPS)
        handle_move(rebane, objects)
        #draw_bg()
        draw(window, rebane, objects, offset_x)

      

        
        if ((rebane.rect.right - offset_x >= WIDTH - scroll_area_width) and rebane.x_vel > 0) or (
                (rebane.rect.left - offset_x <= scroll_area_width) and rebane.x_vel < 0):
            offset_x += rebane.x_vel
        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
