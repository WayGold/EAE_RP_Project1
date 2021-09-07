#
# PYGAME TESTING DEMO - Tea Party Game Testing
# Author: Wei Zeng
# Date: Aug.24 2021
#

from main_menu import MainMenu, uiButton
from delivery_zone import *
from collision_container import *
from barrier import *
from barrier_parser import load_txt
from tea_bubble import *
from tea_drop import *
import os
import pygame
import logging

# from pygame.display import toggle_fullscreen
# from pygame.scrap import contains

# Init Root Directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Init Font Options
pygame.font.init()
myfont = pygame.font.SysFont('Showcard Gothic', 30)

# Macros
GAME_ON = False
DAMAGE_RECEIVING_CD = 3000  # milliseconds
FPS = 60
WHITE = (255, 255, 255)
WIDTH, HEIGHT = 1600, 900
HEALTH_UNIT_WIDTH = 40
HEALTH_UNIT_HEIGHT = 40
BACKGROUND_WIDTH = 4000
BACKGROUND_SPEED = 2
CONTAINER_WIDTH, CONTAINER_HEIGHT = 180, 180

TEA_CUP_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teacup.png'),
                                       (CONTAINER_WIDTH, CONTAINER_HEIGHT))
TEA_POT_IMAGE = pygame.transform.scale(pygame.image.load(ROOT_DIR + r'/image/teapot.png'),
                                       (CONTAINER_WIDTH, CONTAINER_HEIGHT))


class Health:
    def __init__(self, image_path):
        self.image = pygame.transform.scale(pygame.image.load(image_path),
                                            (HEALTH_UNIT_WIDTH, HEALTH_UNIT_HEIGHT)).convert_alpha()
        self.life_count = 3
        self.health_bar_pos_x = 70
        self.health_bar_pos_y = 70


def draw(window, map, obj_list, tea_drops, health, collected_tea, tea_bubbles, main_menu):
    """
    draw(window, obj_list, tea_drops):
    :param tea_bubbles:
    :param health:
    :param collected_tea:
    :param map:
    :param tea_drops:                   Qualified tea drops list to be drawn
    :param obj_list:                    Container list basically, containers to be drawn
    :param window:                      The main game window object
    :return:                            Void, draw all passed in objects
    """

    global GAME_ON
    # Setup White Background
    window.fill(WHITE)

    # Draw Background
    window.blit(map.image, (map.starting_dx, 0))

    # Draw barriers
    for barrier in map.barriers:
        window.blit(barrier.image,
                    (barrier.get_global_position(map.starting_dx), 0))
    # Draw delivery zones
    for zone in map.delivery_zones:
        window.blit(zone.image,
                    (zone.get_global_position(map.starting_dx), 0))

        window.blit(zone.image,
                    (zone.get_mirror_global_position(map.starting_dx), 0))

    deliver_here_image = pygame.image.load(ROOT_DIR + r'/image/deliver_here.png')
    # Draw delivery zones
    for zone in map.delivery_zones:
        window.blit(zone.image,
                    (zone.get_global_position(map.starting_dx), 0))

        window.blit(zone.image,
                    (zone.get_mirror_global_position(map.starting_dx), 0))

        window.blit(deliver_here_image,
                    (zone.get_global_position(map.starting_dx), 0))

        window.blit(deliver_here_image,
                    (zone.get_mirror_global_position(map.starting_dx), 0))

        text_surface = myfont.render(
            str(zone.tea_level) + ' / ' + str(zone.tea_requirement), False, (0, 0, 0))
        window.blit(text_surface, (zone.get_global_position(map.starting_dx) - 100, 35))
        window.blit(text_surface, (zone.get_mirror_global_position(map.starting_dx) - 100, 35))

    if GAME_ON:
        obj_index = 0
        for i in obj_list:
            window.blit(i.image, (i.position_rect.x, i.position_rect.y))
            if obj_index == 0:
                tea_pot_surface = myfont.render(str(i.tea_level), False, (0, 0, 0))
                window.blit(tea_pot_surface, (i.position_rect.x + 55, i.position_rect.y + 55))
            obj_index += 1

    # Display End Game Content or Main Menu
    if map.are_delivery_zones_full():
        window.blit(pygame.image.load(
            ROOT_DIR + r'/image/you_win.png'), (WIDTH / 3, HEIGHT / 3))
    elif health.life_count <= 0:
        window.blit(pygame.image.load(
            ROOT_DIR + r'/image/game_over.png'), (WIDTH / 4, HEIGHT / 6))
    elif not GAME_ON:
            main_menu.show_main_menu(window)

    # Draw tea drops
    for d in tea_drops:
        window.blit(d.image, (d.position_rect.x, d.position_rect.y))

    # Draw Healthbar
    if GAME_ON:
        i = 0
        while i < health.life_count:
            window.blit(health.image, (health.health_bar_pos_x +
                                       i * 60, health.health_bar_pos_y))
            i += 1

    # Draw Tea Bubbles
    draw_all_tea_bubble(window, tea_bubbles)

    # Init Collected Tea Display Text and Draw
    textsurface = myfont.render(
        'Tea Drops: ' + str(collected_tea), False, (0, 0, 0))
    window.blit(textsurface, (1200, 70))
    window.blit(pygame.image.load(
        ROOT_DIR + r'/image/teadrop.png'), (1410, 70))

    pygame.display.update()


def is_game_on(life_count, map):
    """
    is_game_on(life_count, map):
    :param life_count:
    :param map:
    :return:
    """
    global GAME_ON
    if life_count > 0 and not map.are_delivery_zones_full() and GAME_ON:
        return True
    else:
        return False


def main():
    """
    main():                             This is the game main execution function, including the main execution loop and
                                        game logic.
    :return:                            Void
    """

    # Initialize the game window
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tea-Mates")

    # Fetch Barrier and Delivery Zone data
    data = load_txt(os.path.join(ROOT_DIR, 'barrier_data.txt'))
    barriers_data = data[0]
    delivery_zone_data = data[1]

    barriers = []
    delivery_zones = []

    for bNode in barriers_data:
        barriers.append(Barrier(bNode))

    for bNode in delivery_zone_data:
        delivery_zones.append(DeliveryZone(bNode))

    # Start game clock
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    last_tea_drop_time = start_time
    damage_timer = None
    run = True

    # Initialize Health Bar
    health = Health(ROOT_DIR + r'/image/teacup.png')

    # Initialize game objects
    game_map = Map(ROOT_DIR + r'/image/Background.png',
                   barriers, delivery_zones)
    cup = Container(0, 600, ROOT_DIR + r'/image/teacup.png', 0, 101, 87)
    pot = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 20, 143, 106)

    collected_tea = 0
    tea_bub_image_path = os.path.join(ROOT_DIR, 'image/tea_bubble')

    qualified_drops = []
    last_bubble_gen_time = [start_time]
    all_bubble_list = []
    
    # Create Main Menu Components
    game_over_timer = 0
    def start_game(game_map: Map , healt_count):
        global GAME_ON

        if healt_count == 3:
            if not GAME_ON:
                GAME_ON = True
                game_map.starting_dx = 0

    main_menu = MainMenu([]) 
    start_button = uiButton(start_game, 'Start', main_menu.pos_x + WIDTH / 5.5, 400)
    main_menu.buttons.append(start_button)

    # Main Execution Loop
    while run:
        global GAME_ON
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_click_pos = pygame.mouse.get_pos()
                print(mouse_click_pos)
                if start_button.collision_rect.collidepoint(mouse_click_pos):
                    start_game(game_map, health.life_count)

        now = pygame.time.get_ticks()

        if is_game_on(health.life_count, game_map):
            pot.tea_drop_position_update()
            # Randomly Generate Tea Bubbles Every 5 Seconds
            new_bubble = gen_rand_tea_bubble_per_n_second(5, last_bubble_gen_time, tea_bub_image_path)
            if new_bubble is not None:
                all_bubble_list.append(new_bubble)

            for zone in delivery_zones:
                zone.detect_collision(cup, game_map)
                zone.detect_mirror_collision(cup, game_map)

            # Drop a unit of tea every 0.4 seconds
            if now - last_tea_drop_time > 400 and pot.tea_level > 0:
                qualified_drops.append(
                    TeaDrop(pot.tea_drop_position[0], pot.tea_drop_position[1], ROOT_DIR + r'/image/teadrop.png'))
                pot.tea_level -= 1
                last_tea_drop_time = now

            collected_tea = cup.tea_level

            # Check Collision To Determine Whether to Draw
            qualified_drops = drop_tea(qualified_drops, cup)
            all_bubble_list = get_qualified_tea_bubble(all_bubble_list, pot)

            keys_pressed = pygame.key.get_pressed()
            pot_control_listener(keys_pressed, pot)
            cup_control_listener(keys_pressed, cup)

            # for bub in all_bubble_list:
            #     if tea_bubble_collision_detector(pot, bub):
            #         refill_tea(pot, bub)

            # Using the new can_receive_damage bosol of containers to give some breathing room after taking a damage
            # DAMAGE_RECEIVING_CD is set to 3000 milliseconds (3 seconds) Damage timer starts immediately after a
            # collision happens and counts to 3 and then can_receive_damage is set back to True
            if cup.can_receive_damage and pot.can_receive_damage:
                draw(window, game_map, [pot, cup], qualified_drops, health, collected_tea, all_bubble_list, main_menu)
                if collision_detector(pot, cup):
                    damage_timer = now
                    health.life_count = 0
                    game_over_timer = now
                    GAME_ON = False
                for barrier in barriers:
                    if barrier.detect_collision(pot, game_map) or barrier.detect_collision(cup, game_map):
                        damage_timer = now
                        health.life_count -= 1
                        if not health.life_count > 0:
                            game_over_timer = now
                            GAME_ON = False
            else:
                time_passed = now - damage_timer
                if time_passed < 500 or (1000 < time_passed < 1500) or (2000 < time_passed < 2500):
                    draw(window, game_map, [], qualified_drops,
                         health, collected_tea, all_bubble_list, main_menu)
                else:
                    draw(window, game_map, [
                        pot, cup], qualified_drops, health, collected_tea, all_bubble_list, main_menu)
                # Reset the damage timer 3 seconds after getting damaged
                if now - damage_timer > DAMAGE_RECEIVING_CD:
                    pot.can_receive_damage = True
                    cup.can_receive_damage = True
                    damage_timer = None
            # Update TeaDrop Position
            if game_map.are_delivery_zones_full():
                game_over_timer = now
                GAME_ON = False
        else:
            draw(window, game_map, [], [], health,
                 collected_tea, all_bubble_list, main_menu)
        game_map.slideMap()
        if ((not GAME_ON and health.life_count <= 0) or game_map.are_delivery_zones_full()) and now - game_over_timer > 4000:
                main()

    pygame.quit()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    main()
