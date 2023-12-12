import pygame
from skriptid.utils import load_images

# dialoogi kasti omadused
dialogue_box_width = 400
dialogue_box_height = 200
dialogue_box_x = (320 - dialogue_box_width) // 2
dialogue_box_y = (240 - dialogue_box_height) // 2
dialoogi_kast = False

class Dialoog():
   def __init__(self, player, col_type, interact=False):
      self.player = player
      self.col_type = col_type # kas character collidib karu või konnaga

   #def 

