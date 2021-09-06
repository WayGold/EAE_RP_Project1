import pygame
import os


WIDTH = 1600
BLACK = (0, 0, 0) 
MAIN_MENU_WIDTH = 600
MAIN_MENU_HEIGHT = 900
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.font.init()
myfont = pygame.font.SysFont('Showcard Gothic', 30)

class uiButton:
   def __init__(self, function, text, pos_x, pos_y):
       self.function = function
       self.surface = myfont.render(text, False, (255, 255, 255))
       self.pos_y = pos_y
       self.pos_x = pos_x
       self.collision_rect = pygame.Rect(pos_x, pos_y, 100, 30 )

class MainMenu:
    def __init__(self, buttons):
        self.pos_x = WIDTH / 4
        self.pos_y = 0
        self.background_surface = pygame.Surface((WIDTH / 4, 900))
        self.buttons = buttons
    
    def show_main_menu(self, window):
        window.blit(self.background_surface, (WIDTH / 3, 0))
        for button in self.buttons:
           window.blit(button.surface, (self.pos_x + WIDTH / 5.5, self.pos_y + button.pos_y))

        

