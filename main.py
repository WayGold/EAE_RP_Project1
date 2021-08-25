#
# PYGAME TESTING DEMO - Tea Party Game Testing
# Author: Wei Zeng
# Date: Aug.24 2021
#

import os
import pygame
from pygame.display import toggle_fullscreen
from pygame.scrap import contains

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Macros
MOVING_SPEED = 7
FPS = 60
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1600, 900
CONTAINER_WIDTH, CONTAINER_HEIGHT = 180 , 180
TEA_DROP_WIDTH, TEA_DROP_HEIGHT = 100, int(CONTAINER_HEIGHT/2)
TEA_CUP_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teacup.png'), (CONTAINER_WIDTH, CONTAINER_HEIGHT))
TEA_POT_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teapot.png'), (CONTAINER_WIDTH, CONTAINER_HEIGHT))


class Container:
    def __init__(self, pos_x, pos_y, image_path, teaLevel):
        self.position_rect = pygame.Rect(pos_x, pos_y, CONTAINER_WIDTH, CONTAINER_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (CONTAINER_WIDTH, CONTAINER_HEIGHT))
        self.tea_drop_position = (self.position_rect.x, self.position_rect.y + CONTAINER_HEIGHT / 2)
        self.teaLevel = teaLevel

    def get_pos_rect(self):
        return self.position_rect

    def get_image(self):
        return self.image

    def tea_drop_position_update(self):
        self.tea_drop_position = (self.position_rect.x + 108, self.position_rect.y + 35)
        
class TeaDrop:
    def __init__(self, pos_x, pos_y, image_path):
        self.position_rect = pygame.Rect(pos_x, pos_y, TEA_DROP_WIDTH, TEA_DROP_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (TEA_DROP_WIDTH, TEA_DROP_HEIGHT))

    def get_pos_rect(self):
        return self.position_rect

    def get_image(self):
        return self.image

def dropTea(teaDrops, cup):
    qualified = []
    for teaDrop in teaDrops:
        teaDrop.position_rect.y += 3
        if teaDrop.position_rect.y < HEIGHT - 1 and not cup.position_rect.contains(teaDrop.position_rect):
            qualified.append(teaDrop)
        else:
            cup.teaLevel += 1

    return qualified

def draw(window, obj_list, teaDrops):
    """

    :param obj_list:
    :param window:
    :return:
    """
    # Setup White Background
    window.fill(WHITE)

    for i in obj_list:
        window.blit(i.image, (i.position_rect.x, i.position_rect.y))

    for d in teaDrops:
        window.blit(d.image, (d.position_rect.x, d.position_rect.y))

    pygame.display.update()


def pot_control_listener(keys, pot):
    # Go Up
    if keys[pygame.K_w]:
        pot.position_rect.y -= MOVING_SPEED
    # Go Down
    if keys[pygame.K_s]:
        pot.position_rect.y += MOVING_SPEED
    # Go Left
    if keys[pygame.K_a]:
        pot.position_rect.x -= MOVING_SPEED
    # Go Right
    if keys[pygame.K_d]:
        pot.position_rect.x += MOVING_SPEED

def cup_control_listener(keys, cup):
    # Go Up
    if keys[pygame.K_UP]:
        cup.position_rect.y -= MOVING_SPEED
    # Go Down
    if keys[pygame.K_DOWN]:
        cup.position_rect.y += MOVING_SPEED
    # Go Left
    if keys[pygame.K_LEFT]:
         cup.position_rect.x -= MOVING_SPEED
    # Go Right
    if keys[pygame.K_RIGHT]:
         cup.position_rect.x += MOVING_SPEED


def main():
    """

    :return:
    """

    # Initialize the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PYGAME TESTER")

    clock = pygame.time.Clock()
    startTime = pygame.time.get_ticks()
    run = True

    cup = Container(0, 600, ROOT_DIR + r'/image/teacup.png', 0)
    pot = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 50)
    
    qualifiedDrops = []
    # Main Execution Loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        now = pygame.time.get_ticks()
        print(cup.teaLevel)
        if now - startTime > 400 and pot.teaLevel > 0:
            qualifiedDrops.append(TeaDrop(pot.tea_drop_position[0], pot.tea_drop_position[1], ROOT_DIR + r'/image/teadrop.png'))
            pot.teaLevel -= 1
            startTime = now
    
        qualifiedDrops = dropTea(qualifiedDrops, cup)
        keys_pressed = pygame.key.get_pressed()
        pot_control_listener(keys_pressed, pot)
        cup_control_listener(keys_pressed, cup)

        # Update TeaDrop Position
        pot.tea_drop_position_update()             
        draw(window, [cup, pot], qualifiedDrops)
        
    pygame.quit()


if __name__ == '__main__':
    main()
