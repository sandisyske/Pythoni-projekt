import sys
import random
import pygame
import math

from skriptid.utils import load_image, load_images, Animation
from skriptid.entities import PhysicsEntity, Player, Karu, Konn
from skriptid.tilemap import Tilemap
from skriptid.particles import Particle
#from skriptid.dialoog import Font

# Funcs/Classes ---------------------------------------------- #
def clip(surf, x, y, x_size, y_size):
   handle_surf = surf.copy()
   clipR = pygame.Rect(x, y, x_size, y_size)
   handle_surf.set_clip(clipR)
   image = surf.subsurface(handle_surf.get_clip())
   return image.copy()
class Font():
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        font_img.set_colorkey((0, 0, 0))
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x, 0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()   

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing





# klass GAME ----------------------------------------------------------------------------------->
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Aardejaht')#ekraani nimi
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        
        self.movement = [False, False]
        self.alert_flag = False
        self.alert_flag_konn = False
        self.post = False

        self.talk_karu = False
        self.talk_konn = False
        self.happy_karu = False
        self.happy_konn = False

        click = False
        
        # ANIMATSIOONID -------------------------------------------------------------------------->
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'spawners': load_images('tiles/spawners'),
            'background': load_image('background.png'),
            'menu': load_image('menu.png'),
            'text_box': load_image('text_box.png'),
            'karu/idle': Animation(load_images('entities/tegelane/karu/idle'), img_dur=12),
            'karu/talk': Animation(load_images('entities/tegelane/karu/talk'), img_dur=12),
            'karu/wave': Animation(load_images('entities/tegelane/karu/wave'), img_dur=12),
            'karu/happy': Animation(load_images('entities/tegelane/karu/happy'), img_dur=12),
            'konn/idle': Animation(load_images('entities/tegelane/konn/idle'), img_dur=12),
            'konn/wave': Animation(load_images('entities/tegelane/konn/wave'), img_dur=12),
            'konn/talk': Animation(load_images('entities/tegelane/konn/talk'), img_dur=15),
            'konn/happy': Animation(load_images('entities/tegelane/konn/happy'), img_dur=18),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/player/jump'), img_dur=9, loop=False),
            'player/dig': Animation(load_images('entities/player/dig'), img_dur=12, loop=False),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/aare_1': Animation(load_images('particles/aare_1'), img_dur=14, loop=False),
            'particle/aare_2': Animation(load_images('particles/aare_2'), img_dur=14, loop=False),
            'particle/button': Animation(load_images('particles/button'), img_dur=20),
            #siia lisada aare particle lisana aare_1 ja aare_2
            #            'tegelane_konn/idle': Animation(load_images('entities/tegelane/konn/idle')),
            
        }
        # MÄNGU TEGELASED ------------------------------------------------------------------------------------->
        self.player = Player(self, (50, 50), (8, 15))
        self.karu = Karu(self, (145, -63), (8, 15), self.alert_flag)
        self.konn = Konn(self, (50, 50), (8, 15), self.alert_flag_konn)
        
        

        
        # MAP ------------------------------------------------------------------------------------------------->
        self.tilemap = Tilemap(self, tile_size=16)
        #self.tilemap.load('map.json')
        self.load_level(0)
        

        # OSAKESED -------------------------------------------------------------------------------------------->
        self.particles = []
        self.aare1 = [Particle(self, 'aare_1', (760, 279), velocity=[0, -0.08], frame=0)] #aarete asukohad
        self.aare2 = [Particle(self, 'aare_2', (-700, -665), velocity=[0, -0.08], frame=0)]
        # nupud 
        self.nupp_karu = [Particle(self, 'button', (500, -80), velocity=[0, 0], frame=0)] # talk button for clickbait
        self.nupp_konn = [Particle(self, 'button', (-412, 145), velocity=[0, 0], frame=0)]
        self.nupp_post = [Particle(self, 'button', (120, 45), velocity=[0, 0], frame=0)]

    # MENÜÜ LOOP
    def main_menu(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.assets['menu'], (0, 0))

            mx, my = pygame.mouse.get_pos()
            nupp_1 = pygame.Rect(224, 248, 192, 64)
            nupp_2 = pygame.Rect(224, 346, 192, 64)

            if nupp_1.collidepoint((mx, my)):
                if click:
                    self.run()
            if nupp_2.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()



            click = False
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit() 
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            print("Mäng on sulgunud!")
                            pygame.quit() 
                            sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True




            pygame.display.update()
            self.clock.tick(60)

    def load_level(self, level): # mapi laadimine
        self.tilemap.load('data/maps/' + str(level) + '.json')

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
                self.tegelased.append(Konn(self, spawner['pos'], (8, 15), self.alert_flag_konn))
            else:
                self.tegelased.append(Karu(self, spawner['pos'], (8, 15), self.alert_flag))

        self.kutu = 0
        
        # scroll variable et liigutada ekraani
        self.scroll = [0, 0]
        self.ekraani_vahetus = -30
        click = False
    
    # M2NGU ENDA LOOP ---------------------------------------------------------------------------------------------->
    def run(self):
        run = True
        #self.talk = False
        aare_1_leitud = 1
        aare_2_leitud = 1
        post_aktiivne = False
        
        while run:

            #TAUST -------------------------------------------------------------------------------------------->
            self.display.blit(self.assets['background'], (0, 0))
            
            # ANIMATSIOON M2NGU ja suremine

            if self.happy_konn and self.happy_karu:
                self.ekraani_vahetus += 1
                if self.ekraani_vahetus > 30:
                    self.load_level(0)
            if self.ekraani_vahetus < 0:
                self.ekraani_vahetus += 1
            

            if self.player.pos[1] > 500:
                self.kutu += 1
                if self.kutu >= 10:
                    self.ekraani_vahetus = min(30, self.ekraani_vahetus + 1)
                if self.kutu > 40:
                    self.load_level(0)
            # MUUTUJAD ---------------------------------------------------------------------------------------->
            my_font = Font('data/images/small_font.png')

            # alert on True, kui player on tegelase lähedal
            self.alert_flag = self.karu.alert(self.player.pos)
            self.alert_flag_konn = self.konn.alert(self.player.pos)


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
                    aare_1_leitud = 0

            #konna aare
            if -730 <= self.player.pos[0] <= -670 and -660 <= self.player.pos[1] <= -650:
                if self.player.dig_time > 0:
                    aare_2_leitud = 0

            #karu aarde leidmine
            if aare_1_leitud < 1:        
                for aare in self.aare1:
                    kill = aare.update()
                    aare.render(self.display, offset=render_scroll)
                    if kill:
                        self.aare1.remove(aare)

            #konna aarde leidmine
            if aare_2_leitud < 1:
                for aare in self.aare2:
                    kill = aare.update()
                    aare.render(self.display, offset=render_scroll)
                    if kill:
                        self.aare2.remove(aare)    

            # post juhatuseks ---------------------------------------------------------------------------------->

            if 105 <= self.player.pos[0] <= 125 and 64 <= self.player.pos[1] <= 66:
                if not post_aktiivne:
                    for post in self.nupp_post:
                        post.update()
                        post.render(self.display, offset=render_scroll)
                else:
                    self.display.blit(self.assets['text_box'], (0, 0))
                    my_font.render(self.display, '                            Karu maja  -->', (25, 205))
                    my_font.render(self.display, '                        <-- Konna maja ', (25, 215))
            else:
                post_aktiivne = False
                    


            # karu ja konna ylesanded ------------------------------------------------------------------------->
       
            # karu ylesanne
            if self.alert_flag: # on True kui player on karu juures
                if not self.talk_karu:
                    for nupp in self.nupp_karu:
                        nupp.update()
                        nupp.render(self.display, offset=render_scroll)
                else:
                    if aare_1_leitud < 1: # kuidas nyyd muuta animatsiooni
                        self.happy_karu = True
                        self.display.blit(self.assets['text_box'], (0, 0))
                        my_font.render(self.display, 'Sa leidsid minu kadunud saapa!', (25, 205))
                    elif aare_1_leitud == 1:
                        self.display.blit(self.assets['text_box'], (0, 0))
                        my_font.render(self.display, 'Palun aita leida minu kadunud saabas! See kadus idapoolses koopas, ', (25, 205))
                        my_font.render(self.display, 'kus ma otsisin head kohta magamiseks.', (25, 215))
            else:
                self.talk_karu = False
                #self.happy_karu = False kui tahame et ta j2tkaks enda idle animatsiooni siis saab selle tagasi panna              
                    
            # konna ylesanne
            if self.alert_flag_konn: # on True kui player on karu juures
                if not self.talk_konn:
                    for nupp in self.nupp_konn:
                        nupp.update()
                        nupp.render(self.display, offset=render_scroll)
                else:
                    if aare_2_leitud < 1: # kuidas nyyd muuta animatsiooni
                        self.happy_konn = True
                        self.display.blit(self.assets['text_box'], (0, 0))
                        my_font.render(self.display, 'Minu vanaema kaelakee! mmmm aitah', (25, 205))
                    elif aare_2_leitud == 1:
                        self.display.blit(self.assets['text_box'], (0, 0))
                        my_font.render(self.display, 'Kuidas see juhtus! Ma ronisin ja ronisin ... krooksusin suure kivi juures', (25, 205))
                        my_font.render(self.display, 'kuid tagasi tulles avastasin, et kaotasin vanaema kaelakee', (25, 215))
            else:
                self.talk_konn = False    


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
                    if event.key == pygame.K_a:
                        self.talk_karu = True
                        self.talk_konn = True
                        post_aktiivne = True
                    if event.key == pygame.K_z: # ajutine, ei j22 m2ngu sisse
                        print(self.player.pos)    
                        
                        
                    if event.key == pygame.K_ESCAPE:
                        run = False

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False       

            # EKRAANILE KUVAMINE JA UUENDAMINE ---------------------------------------------------------------->
            if self.ekraani_vahetus:
                vahetus_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(vahetus_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() //2), (30 - abs(self.ekraani_vahetus)) * 8)
                vahetus_surf.set_colorkey((255, 255, 255))
                self.display.blit(vahetus_surf, (0, 0))
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #erkaan ekraani sees ja scaleimine
            
            pygame.display.update()
            self.clock.tick(60)  #FPS


Game().main_menu() #run
