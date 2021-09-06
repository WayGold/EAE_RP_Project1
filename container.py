#
# container.py      -   Container Obj Class, used for creating tea pot and tea cup
# Author: Wei Zeng
# Date: Aug.24 2021
#

import pygame

CONTAINER_WIDTH, CONTAINER_HEIGHT = 180, 180
MOVING_SPEED = 7


class Container:
    """
    Container Class     -
    Description:        Container Obj Class for Teapot and Teacup
    Class Vars:         position_rect       -   The bounding rect representing the container png
                        image               -   The transformed image object from inputted image path
                        tea_drop_position   -   The tea drop pouring start point
                        tea_level            -   The level(amount) of tea currently being held in the container
    """

    # 143 106

    def __init__(self, pos_x, pos_y, image_path, tea_level, h, w):
        self.position_rect = pygame.Rect(
            pos_x, pos_y, h, w)
        self.image = pygame.image.load(
            image_path)
        self.tea_drop_position = (
            self.position_rect.x, self.position_rect.y + CONTAINER_HEIGHT / 2)
        self.tea_level = tea_level
        self.can_receive_damage = True

    def tea_drop_position_update(self):
        """
        tea_drop_position_update    -   Arbitrary Function to update the tea drop pouring start point according to the
                                        (updated) position of the container
        :return:                    -   void
        """
        self.tea_drop_position = (
            self.position_rect.x + self.position_rect.width - 3, self.position_rect.y + 18)


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