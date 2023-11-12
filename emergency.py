import pygame
import sys

# Variables
WIDTH = 1000
HEIGHT = 800
FPS = 60
VELOCITY = 4


# Mang ise
class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Aardejaht")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load("Assets/Backround/sky.png")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()
            self.clock.tick(60)

Game().run()
