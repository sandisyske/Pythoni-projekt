import os
from typing import Any
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
GRAVITY = 1

#screen
WIDTH, HEIGHT = 1000, 800
FPS = 60
PLAYER_VEL = 4

window = pygame.display.set_mode((WIDTH, HEIGHT))


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



#player
class Tegelane(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    #gravitatsioon, kui tahta kiiremini, siis saab seda väärtust tõsta
    GRAVITY = 1
    # kasuta sprite pilte
    SPRITES = load_sprite_sheets("Tegelased", "Rebane", 32, 32, True)
    # delay between sprites
    ANIMATION_DELAY = 10

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
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
        #self.y_vel += min(1, self.fall_count/ fps) * self.GRAVITY
        self.move(self.x_vel, self.y_vel)

        self.fall_count += 1
        self.update_sprite()


    # animatsiooni uuendamine iga frame
    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1





    def draw(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))



#taust
def taust(name):
    image = pygame.image.load(join("Assets", "Backround", name))
    _, _, width, height = image.get_rect()
    tiles =[]

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i*width, j*height)
            tiles.append(pos)
    return tiles, image



def draw(window, backround, bg_image, rebane):

    for tile in backround:
        window.blit(bg_image, tile)

    rebane.draw(window)

    pygame.display.update()

def handle_move(rebane):
    keys = pygame.key.get_pressed()

    rebane.x_vel = 0
    if keys[pygame.K_LEFT]:
        rebane.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT]:
        rebane.move_right(PLAYER_VEL)


def main (window):
    clock = pygame.time.Clock()
    backround, bg_image = taust("taust.png")

    rebane = Tegelane(100, 100, 50, 50)

    run = True
    while run:
        clock.tick(FPS)


        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        rebane.loop(FPS)
        handle_move(rebane)
        draw(window, backround, bg_image, rebane)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)
