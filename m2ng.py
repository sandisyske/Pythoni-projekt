import pygame
import sys

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('aardejaht') #ekraani nimi
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock() # ekraani nimi

        self.img = pygame.image.load("data/images/clouds/cloud_1")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
    
            pygame.display.update()
            self.clock.tick(60)  #FPS

Game().run()
