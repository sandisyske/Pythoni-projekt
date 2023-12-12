import sys
import random
import pygame
import math

from skriptid.utils import load_image, load_images, Animation
from skriptid.entities import PhysicsEntity, Player, Karu, Konn
from skriptid.tilemap import Tilemap
from skriptid.particles import Particle

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Aardejaht')#ekraani nimi
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()
        
        self.movement = [False, False]
        self.alert_flag = False
        # ANIMATSIOONID -------------------------------------------------------------------------->
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'spawners': load_images('tiles/spawners'),
            'background': load_image('background.png'),
            'karu/idle': Animation(load_images('entities/tegelane/karu/idle'), img_dur=12),
            'karu/talk': Animation(load_images('entities/tegelane/karu/talk'), img_dur=12),
            #'karu/happy': Animation(load_images('entities/tegelane/karu/idle'), img_dur=12),
            'konn/idle': Animation(load_images('entities/tegelane/konn/idle')),
            #'konn/talk': Animation(load_images('entities/tegelane/konn/idle')),
            #'konn/happy': Animation(load_images('entities/tegelane/konn/idle')),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=9, loop=False),
            'player/dig': Animation(load_images('entities/player/dig'), img_dur=12, loop=False),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/aare_1': Animation(load_images('particles/aare_1'), img_dur=14, loop=False),
            'particle/aare_2': Animation(load_images('particles/aare_2'), img_dur=14, loop=False),
            'particle/button': Animation(load_images('particles/button'), img_dur=10),
            #siia lisada aare particle lisana aare_1 ja aare_2
            #            'tegelane_konn/idle': Animation(load_images('entities/tegelane/konn/idle')),
            
        }
        # MÄNGU TEGELASED ------------------------------------------------------------------------------------->
        self.player = Player(self, (50, 50), (8, 15))
        self.karu = Karu(self, (145, -63), (8, 15), self.alert_flag)
        
        
        # MAP ------------------------------------------------------------------------------------------------->
        self.tilemap = Tilemap(self, tile_size=16)
        self.tilemap.load('map.json')

        #SPAWNERID -------------------------------------------------------------------------------------------->
        #lehtede tekitamine
        self.leaf_spawner = []
        for tree in self.tilemap.extract([('large_decor', 5)], keep=True):
            self.leaf_spawner.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13)) # lisab lehe_spawner listi puu Recti

        # tegelaste ja playeri spawnerite tekitamine tekitamine
        self.tegelased = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            elif spawner['variant'] == 1:
                self.tegelased.append(Konn(self, spawner['pos'], (8, 15)))
            else:
                self.tegelased.append(Karu(self, spawner['pos'], (8, 15), self.alert_flag))
        

        self.particles = []
        self.aare1 = [Particle(self, 'aare_1', (760, 279), velocity=[0, -0.08], frame=0)] #aarete asukohad
        self.aare2 = [Particle(self, 'aare_2', (-700, -665), velocity=[0, -0.08], frame=0)]
        self.button = [Particle(self, 'button', (self.player.pos[0], self.player.pos[1] - 30), velocity=[0, 0], frame=0)] # talk button for clickbait

        # scroll variable et liigutada ekraani
        self.scroll = [0, 0]

    # M2NGU LOOP ---------------------------------------------------------------------------------------------->
    def run(self):
        while True:

            #TAUST -------------------------------------------------------------------------------------------->
            self.display.blit(self.assets['background'], (0, 0))

            # MUUTUJAD ---------------------------------------------------------------------------------------->
            aare_1_leitud = 1
            aare_2_leitud = 1
            show_button = False
            karu_talk = False
            self.alert_flag = self.karu.alert(self.player.pos)

            # kaamera liigutamine tegelase ligidal ----------------------------------------------------------->
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # et tegelane ei põrkaks ringi, kui talle määrataske float asukoht

            # osakeste spawner ------------------------------------------------------------------------------->
            for rect in self.leaf_spawner:
                if random.random() * 49999 < rect.width *rect.height: # random.random() on suvaline arv 0 kuni 1, kontrollime kas see on väiksem kui meie piksel ruut alas # suure numbriga korrutamisel saame kindlad olla et lehti ei teki iga frame lõpmatuseni
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20))) # osakeste tekitamine toimub siin

            self.tilemap.render(self.display, offset=render_scroll)
            
            # tegelaste renderimine -------------------------------------------------------------------------->
            
            for tegelane in self.tegelased.copy():
                tegelane.update(self.tilemap, (0, 0))
                tegelane.render(self.display, offset=render_scroll)
            
             

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)
            
            #kontrollida, mis ruudud playeri ümber on
            #print(self.tilemap.physics_rects_around(self.player.pos))
            

            # puulehtede renderimine ------------------------------------------------------------------------->
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            
                
            # karu ja konna aarde asukohad ------------------------------------------------------------------->
            #karu aare
            if 730 <= self.player.pos[0] <= 780 and 280 <= self.player.pos[1] <= 290:
                if self.player.dig_time > 0:
                    aare_1_leitud -= 1

            #konna aare
            if -730 <= self.player.pos[0] <= -670 and -660 <= self.player.pos[1] <= -650:
                if self.player.dig_time > 0:
                    aare_2_leitud -= 1

            #karu aarde leidmine
            if aare_1_leitud == 0:        
                for aare in self.aare1:
                    kill = aare.update()
                    aare.render(self.display, offset=render_scroll)
                    if kill:
                        self.aare1.remove(aare)

            #konna aarde leimine
            if aare_2_leitud == 0:
                for aare in self.aare2:
                    kill = aare.update()
                    aare.render(self.display, offset=render_scroll)
                    if kill:
                        self.aare2.remove(aare)    
            
            #print(alert)
            # karu alert 2kki teisest kohast?
            #print(self.alert_flag)
            self.alert_flag = self.karu.alert(self.player.pos) # kui player on karu juures, siis on True
                
                #self.karu.talk()
                
            

            
            


            #  KEY EVENTS ------------------------------------------------------------------------------------>
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
                    if event.key == pygame.K_DOWN:
                        self.player.dig()
                    if event.key == pygame.K_z:
                        #self.player.talk() - vaja veel kirjutada funktsioon
                        print(self.player.pos)
                    if event.key == pygame.K_ESCAPE:
                        print("Mäng on sulgunud!")
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False       

            # EKRAANILE KUVAMINE JA UUENDAMINE ---------------------------------------------------------------->
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #erkaan ekraani sees ja scaleimine
            pygame.display.update()
            self.clock.tick(60)  #FPS

Game().run()
