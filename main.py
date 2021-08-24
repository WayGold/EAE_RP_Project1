#
# PYGAME TESTING DEMO - Tea Party Game Testing
# Author: Wei Zeng
# Date: Aug.24 2021
#

import os
import pygame

# Macros
FPS = 60
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1280, 960
CONTAINER_WIDTH, CONTAINER_HEIGHT = 80, 60
TEA_CUP_IMAGE = pygame.transform.scale(pygame.image.load(r'image/teacup.png'), (CONTAINER_WIDTH, CONTAINER_HEIGHT))
TEA_POT_IMAGE = pygame.transform.scale(pygame.image.load(r'image/teapot.png'), (CONTAINER_WIDTH, CONTAINER_HEIGHT))


class Container:
    def __init__(self, pos_x, pos_y, image_path):
        self.position_rect = pygame.Rect(pos_x, pos_y, CONTAINER_WIDTH, CONTAINER_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(image_path), (CONTAINER_WIDTH, CONTAINER_HEIGHT))

    def get_pos_rect(self):
        return self.position_rect

    def get_image(self):
        return self.image


def draw(window, obj_list):
    """

    :param obj_list:
    :param window:
    :return:
    """
    # Setup White Background
    window.fill(WHITE)

    # Draw the Objects in List
    for i in obj_list:
        window.blit(i.image, (i.position_rect.x, i.position_rect.y))

    pygame.display.update()


def pot_control_listener(keys, pot_rect):
    # Go Up
    if keys[pygame.K_w]:
        pot_rect.y -= 1
    # Go Down
    if keys[pygame.K_s]:
        pot_rect.y += 1
    # Go Left
    if keys[pygame.K_a]:
        pot_rect.x -= 1
    # Go Right
    if keys[pygame.K_d]:
        pot_rect.x += 1


def cup_control_listener(keys, cup_rect):
    # Go Up
    if keys[pygame.K_UP]:
        cup_rect.y -= 1
    # Go Down
    if keys[pygame.K_DOWN]:
        cup_rect.y += 1
    # Go Left
    if keys[pygame.K_LEFT]:
        cup_rect.x -= 1
    # Go Right
    if keys[pygame.K_RIGHT]:
        cup_rect.x += 1


def main():
    """

    :return:
    """

    # Initialize the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PYGAME TESTER")

    clock = pygame.time.Clock()
    run = True

    cup = Container(0, 800, r'image/teacup.png')
    pot = Container(0, 0, r'image/teapot.png')

    # Main Execution Loop
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        pot_control_listener(keys_pressed, pot.position_rect)
        cup_control_listener(keys_pressed, cup.position_rect)

        draw(window, [cup, pot])

    pygame.quit()


if __name__ == '__main__':
    main()
