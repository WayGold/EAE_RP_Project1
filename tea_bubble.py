import os
import logging
import pygame
import random

from container import Container

# Init Root Directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class TeaBubble:
    """
    TeaBubble Class     -
    Description:        Tea Bubble Obj Class for Tea Refilling
    Class Vars:         position_rect       -   The bounding rect representing the tea bubble png
                        image               -   The image object from inputted image path
                        refill_amount       -   The level(amount) of tea in the bubble
    """

    def __init__(self, pos_x, pos_y, image_path, refill_amount, width, height):
        self.position_rect = pygame.Rect(pos_x, pos_y, width, height)
        self.image_list = []
        for image in os.listdir(image_path):
            self.image_list.append(pygame.image.load(os.path.join(image_path, image)).convert_alpha())
        self.refill_amount = refill_amount
        self.draw_index = 0

    def generate_rand_tea_bub(self):
        """
        generate_rand_tea_bub(self):

        :return:    Update the position rect position with a randomly 2D coord. 800 <= X < 1600, 0 <= Y < 800
        """
        random.seed(pygame.time.get_ticks())
        rand_x = random.randrange(800, 1599, 1)
        rand_y = random.randrange(0, 899, 1)

        self.position_rect.x = rand_x
        self.position_rect.y = rand_y

        logging.info('Randomized Position at: ' + str(self.position_rect.x) + ', ' + str(self.position_rect.y))


def refill_tea(pot: Container, tea_bub: TeaBubble):
    """
    def refill_tea(pot: Container, tea_bub: TeaBubble):
    :param pot:         The Pot to be Refilled
    :param tea_bub:     The Tea Bubble Being Caught By the Pot
    :return:            Update Pot Tea Level According to Refill Amount of the Bubble
    """
    pot.tea_level += tea_bub.refill_amount


def draw_bubble_animation(window, tea_bub: TeaBubble, last_update_bubble_time):
    now = pygame.time.get_ticks()
    if now - last_update_bubble_time > 30:
        logging.info('Drawing bubble with image at index: ' + str(tea_bub.draw_index))
        window.blit(tea_bub.image_list[tea_bub.draw_index].convert_alpha(),
                    (tea_bub.position_rect.x, tea_bub.position_rect.y))
        if tea_bub.draw_index == len(tea_bub.image_list) - 1:
            tea_bub.draw_index = 0
        else:
            tea_bub.draw_index += 1
    return now


def test():
    # Initialize the game window
    window = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Tea-Mates")
    image_path = os.path.join(ROOT_DIR, 'image/tea_bubble')
    tea_bub = TeaBubble(800, 800, image_path, 20, 46, 51)

    run = True
    clock = pygame.time.Clock()
    last_update_bubble_time = pygame.time.get_ticks()

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Setup White Background
        window.fill((255, 255, 255))
        last_update_bubble_time = draw_bubble_animation(window, tea_bub, last_update_bubble_time)
        pygame.display.update()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    test()
