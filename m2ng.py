import sys
import random
import pygame
import math

from skriptid.utils import load_image, load_images, Animation
from skriptid.entities import PhysicsEntity, Player
from skriptid.tilemap import Tilemap
from skriptid.particles import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('aardejaht')#ekraani nimi
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
        }

        # PEATEGELANE
        self.player = Player(self, (50, 50), (8, 15))
        
        # MÄNGU TEGELASED
        
        
        # MAP
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        #osakeste tekitamine
        self.leaf_spawner = []
        for tree in self.tilemap.extract([('large_decor', 5)], keep=True):
            self.leaf_spawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) # lisab lehe_spawner listi puu Recti


        self.particles = []

        # scroll variable et liigutada ekraani
        self.scroll = [0, 0]

    def run(self):
        while True:
            #tausta värvus
            self.display.blit(self.assets['background'], (0, 0))

            # kaamera liigutamine tegelase ligidal
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # et tegelane ei põrkaks ringi, kui talle määrataske float asukoht

            # osakeste spawner
            for rect in self.leaf_spawner:
                if random.random() * 49999 < rect.width *rect.height: # random.random() on suvaline arv 0 kuni 1, kontrollime kas see on väiksem kui meie piksel ruut alas # suure numbriga korrutamisel saame kindlad olla et lehti ei teki iga frame lõpmatuseni
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20))) # osakeste tekitamine toimub siin
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            #kontrollida, mis ruudud playeri ümber on
            #print(self.tilemap.physics_rects_around(self.player.pos))

            #osakesed
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            # EVENTS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if event.key == pygame.K_ESCAPE:
                        print("Mäng on sulgunud!")
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False       

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #erkaan ekraani sees ja scaleimine
            pygame.display.update()
            self.clock.tick(60)  #FPS

Game().run()
