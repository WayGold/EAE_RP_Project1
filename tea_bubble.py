#
#   tea_bubble.py
#   Description:            Tea Bubble Class and Related Methods to Support Bubble Functionalities
#   Author:                 Wei Zeng
#   Date:                   Aug.31 2021
#
import os
import logging
import random
import collision_container as cd
from container import *

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
        sorted_img = os.listdir(image_path)
        sorted_img.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        logging.info(sorted_img)
        for image in sorted_img:
            self.image_list.append(pygame.image.load(os.path.join(image_path, image)).convert_alpha())
        self.refill_amount = refill_amount
        self.draw_index = 0

    def rand_tea_bub_pos(self):
        """
        rand_tea_bub_pos(self):
        :return:    Randomly update the position rect position with a randomly 2D coord. 800 <= X < 1600, 0 <= Y < 800
        """
        random.seed(pygame.time.get_ticks())
        rand_x = random.randrange(800 - self.position_rect.width, 1599 - self.position_rect.height, 1)
        rand_y = random.randrange(0, 899, 1)

        self.position_rect.x = rand_x
        self.position_rect.y = rand_y

        logging.info('Randomized Position at: ' + str(self.position_rect.x) + ', ' + str(self.position_rect.y))


def gen_rand_tea_bubble_per_n_second(n: int, last_bubble_gen_time: list, bubble_image_path: str):
    """
    gen_rand_tea_bubble_per_n_second(n: int, last_bubble_gen_time: list, bubble_image_path: str):
    :param n:                       Num of second to spawn a new tea bubble
    :param last_bubble_gen_time:    List type for data modification, update to the time when new bubble got made
    :param bubble_image_path:       Path to the tea bubble animation png directory
    :return:                        TeaBubble Object being constructed or None
    """
    now = pygame.time.get_ticks()

    # Every n Seconds
    if now - last_bubble_gen_time[0] > n * 1000:
        tea_bub = TeaBubble(800, 450, bubble_image_path, 20, 46, 51)
        tea_bub.rand_tea_bub_pos()
        last_bubble_gen_time[0] = now
        return tea_bub
    else:
        return None


def refill_tea(pot: Container, tea_bub: TeaBubble):
    """
    def refill_tea(pot: Container, tea_bub: TeaBubble):
    :param pot:         The Pot to be Refilled
    :param tea_bub:     The Tea Bubble Being Caught By the Pot
    :return:            Update Pot Tea Level According to Refill Amount of the Bubble
    """
    pot.tea_level += tea_bub.refill_amount


def draw_all_tea_bubble(window, tea_bubble_list: list):
    """
    draw_all_tea_bubble(window, tea_bubble_list: list):
    :param window:              Window To Draw Bubble Onto
    :param tea_bubble_list:     List With All Bubbles To Be Displayed
    :return:                    Draw All Bubbles
    """
    for bub in tea_bubble_list:
        draw_bubble_animation(window, bub)


def draw_bubble_animation(window, tea_bub: TeaBubble):
    """
    draw_bubble_animation(window, tea_bub: TeaBubble, last_update_bubble_time):
    :param window:      Window To Draw Bubble Onto
    :param tea_bub:     Tea Bubble Object To Be Drawn
    :return:            None
    """
    # logging.info('Drawing bubble with image at index: ' + str(tea_bub.draw_index))
    window.blit(tea_bub.image_list[tea_bub.draw_index].convert_alpha(),
                (tea_bub.position_rect.x, tea_bub.position_rect.y))
    if tea_bub.draw_index == len(tea_bub.image_list) - 1:
        tea_bub.draw_index = 0
    else:
        tea_bub.draw_index += 1


def get_qualified_tea_bubble(tea_bubbles, pot):
    """
    get_qualified_tea_bubble(tea_bubbles, pot):
    :param tea_bubbles:
    :param pot:
    :return:
    """
    qualified = []

    for bub in tea_bubbles:
        if not cd.tea_bubble_collision_detector(pot, bub):
            qualified.append(bub)
        else:
            print('REFILLED')
            refill_tea(pot, bub)

    return qualified


def test():
    """
    test():     Tester Function for Tea Bubble Functionalities
    :return:    None
    """
    # Initialize the game window
    window = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("Tea-Mates")
    image_path = os.path.join(ROOT_DIR, 'image/tea_bubble')
    tea_bub = TeaBubble(800, 450, image_path, 20, 46, 51)
    pot = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 50, 143, 106)

    run = True
    clock = pygame.time.Clock()
    game_start_time = pygame.time.get_ticks()
    last_bubble_gen_time = [game_start_time]
    all_bubble_list = []

    while run:
        clock.tick(30)

        # Check For Window Close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()
        pot_control_listener(keys_pressed, pot)

        # Setup White Background
        window.fill((255, 255, 255))
        window.blit(pot.image, (pot.position_rect.x, pot.position_rect.y))
        new_bubble = gen_rand_tea_bubble_per_n_second(5, last_bubble_gen_time, image_path)
        if new_bubble is not None:
            all_bubble_list.append(new_bubble)

        all_bubble_list = get_qualified_tea_bubble(all_bubble_list, pot)
        draw_all_tea_bubble(window, all_bubble_list)
        pygame.display.update()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    test()
