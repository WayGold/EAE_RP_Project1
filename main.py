#
# PYGAME TESTING DEMO - Tea Party Game Testing
# Author: Wei Zeng
# Date: Aug.24 2021
#

import os
import pygame
from pygame.display import toggle_fullscreen
from pygame.scrap import contains

# Init Root Directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Macros
MOVING_SPEED = 7
FPS = 60
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1600, 900
CONTAINER_WIDTH, CONTAINER_HEIGHT = 180, 180
TEA_DROP_WIDTH, TEA_DROP_HEIGHT = 100, int(CONTAINER_HEIGHT / 2)
TEA_CUP_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teacup.png'),
                                       (CONTAINER_WIDTH, CONTAINER_HEIGHT))
TEA_POT_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teapot.png'),
                                       (CONTAINER_WIDTH, CONTAINER_HEIGHT))


class Container:
    """
    Container Class     -
    Description:        Container Obj Class for Teapot and Teacup
    Class Vars:         position_rect       -   The bounding rect representing the container png
                        image               -   The transformed image object from inputted image path
                        tea_drop_position   -   The tea drop pouring start point
                        teaLevel            -   The level(amount) of tea currently being held in the container
    """
    def __init__(self, pos_x, pos_y, image_path, tea_level):
        self.position_rect = pygame.Rect(pos_x, pos_y, CONTAINER_WIDTH, CONTAINER_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (CONTAINER_WIDTH, CONTAINER_HEIGHT))
        self.tea_drop_position = (self.position_rect.x, self.position_rect.y + CONTAINER_HEIGHT / 2)
        self.teaLevel = tea_level

    def tea_drop_position_update(self):
        """
        tea_drop_position_update    -   Arbitrary Function to update the tea drop pouring start point according to the
                                        (updated) position of the container
        :return:                    -   void
        """
        self.tea_drop_position = (self.position_rect.x + 108, self.position_rect.y + 35)


class TeaDrop:
    """
    TeaDrop Class   -
    Description:    Tea Drop Object representing each drop of tea
    Class Vars:     position_rect   -   The bounding rect representing the drop png
                    image           -   The transformed image object from inputted image path
    """
    def __init__(self, pos_x, pos_y, image_path):
        self.position_rect = pygame.Rect(pos_x, pos_y, TEA_DROP_WIDTH, TEA_DROP_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (TEA_DROP_WIDTH, TEA_DROP_HEIGHT))


def drop_tea(tea_drops, cup):
    """
    drop_tea(tea_drops, cup):
    :param tea_drops:           List of qualified drops(drops that should be drawn)
    :param cup:                 Cup Object that could be filled up be catching tea drops
    :return:                    Void, for each previously qualified drop, this function move them downward by 3 pixels
                                and check whether any drop enter the tea cup. If any does, cup's tea level will go up
                                by one and that specific tea drop would be considered not qualified(not to be drawn)
    """
    qualified = []

    for teaDrop in tea_drops:
        teaDrop.position_rect.y += 3
        # Check whether tea drops goes beyond boundary and whether it is contained by the tea cup rect
        if teaDrop.position_rect.y < HEIGHT - 1 and not cup.position_rect.contains(teaDrop.position_rect):
            qualified.append(teaDrop)
        else:
            cup.teaLevel += 1

    return qualified


def draw(window, obj_list, tea_drops):
    """
    draw(window, obj_list, tea_drops):
    :param tea_drops:                   Qualified tea drops list to be drawn
    :param obj_list:                    Container list basically, containers to be drawn
    :param window:                      The main game window object
    :return:                            Void, draw all passed in objects
    """
    # Setup White Background
    window.fill(WHITE)

    # Draw containers
    for i in obj_list:
        window.blit(i.image, (i.position_rect.x, i.position_rect.y))

    # Draw tea drops
    for d in tea_drops:
        window.blit(d.image, (d.position_rect.x, d.position_rect.y))

    pygame.display.update()


def pot_control_listener(keys, pot):
    """
    pot_control_listener(keys, pot):
    :param keys:                        Obj returned by pygame.key.get_pressed(), keys pressed basically
    :param pot:                         Pot obj to be controlled
    :return:                            Void, update position data of pot according to key input
    """
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
    """
    cup_control_listener(keys, cup):
    :param keys:                        Obj returned by pygame.key.get_pressed(), keys pressed basically
    :param cup:                         Cup obj to be controlled
    :return:                            Void, update position data of pot according to key input
    """
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
    main():                             This is the game main execution function, including the main execution loop and
                                        game logic.
    :return:                            Void
    """

    # Initialize the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PYGAME TESTER")

    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    run = True

    cup = Container(0, 600, ROOT_DIR + r'/image/teacup.png', 0)
    pot = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 50)

    qualified_drops = []
    # Main Execution Loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        now = pygame.time.get_ticks()
        print(cup.teaLevel)
        if now - start_time > 400 and pot.teaLevel > 0:
            qualified_drops.append(
                TeaDrop(pot.tea_drop_position[0], pot.tea_drop_position[1], ROOT_DIR + r'/image/teadrop.png'))
            pot.teaLevel -= 1
            start_time = now

        qualified_drops = drop_tea(qualified_drops, cup)
        keys_pressed = pygame.key.get_pressed()
        pot_control_listener(keys_pressed, pot)
        cup_control_listener(keys_pressed, cup)

        # Update TeaDrop Position
        pot.tea_drop_position_update()
        draw(window, [cup, pot], qualified_drops)

    pygame.quit()


if __name__ == '__main__':
    main()
