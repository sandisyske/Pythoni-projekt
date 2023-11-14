import pygame
import sys
from skriptid.entities import PhysicsEntity #võtame skriptide kasutast teise .py faili
from skriptid.utils import load_image, load_images

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('aardejaht') #ekraani nimi
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock() # ekraani nimi

        self.movement = [False, False]

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            "player": load_image("entities/player.png")
        }

        print(self.assets)

        # TEGELANE
        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
        


    def run(self):
        while True:

            #clear backround
            self.display.fill((180, 240, 230))

            self.player.update((self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            #COLLISIONS
       

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

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False       

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)) #erkaan ekraani sees ja scaleimine
            pygame.display.update()
            self.clock.tick(60)  #FPS

Game().run()
