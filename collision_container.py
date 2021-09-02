#
#   collision_container.py
#   Description:            Collision Detector Functionalities for Containers(Pot/Cup)
#   Author:                 Wei Zeng
#   Date:                   Aug.26 2021
#
from tea_bubble import TeaBubble
import os
import logging
from main import Container

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def collision_detector(pot: Container, cup: Container):
    """
    collision_detector(pot: Container, cup: Container):
    :param pot:     Pot Container Obj
    :param cup:     Cup Container Obj
    :return:        False if no collision happens, True otherwise
    """

    if not pot.can_receive_damage or not cup.can_receive_damage or (pot.position_rect.y +
                                                                    pot.position_rect.height < cup.position_rect.y) or (
            cup.position_rect.y +
            cup.position_rect.height < pot.position_rect.y) or (pot.position_rect.x +
                                                                pot.position_rect.width < cup.position_rect.x) or (
            cup.position_rect.x +
            cup.position_rect.width < pot.position_rect.x):
        return False

    # Init Pot and Cup Vertices
    pot_vertices = [(pot.position_rect.x, pot.position_rect.y),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y),
                    (pot.position_rect.x, pot.position_rect.y +
                     pot.position_rect.height),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y + pot.position_rect.height)]
    cup_vertices = [(cup.position_rect.x, cup.position_rect.y),
                    (cup.position_rect.x + cup.position_rect.width, cup.position_rect.y),
                    (cup.position_rect.x, cup.position_rect.y +
                     cup.position_rect.height),
                    (cup.position_rect.x + cup.position_rect.width, cup.position_rect.y + cup.position_rect.height)]

    # Check each pot vertex, if any goes within the cup range, return True
    for vertex in pot_vertices:
        if cup_vertices[0][0] <= vertex[0] <= cup_vertices[1][0] \
                and cup_vertices[0][1] <= vertex[1] <= cup_vertices[2][1]:
            logging.info('cup and pot collided')
            cup.can_receive_damage = False
            pot.can_receive_damage = False
            return True

    return False


def tea_bubble_collision_detector(pot: Container, tea_bubble: TeaBubble):
    """
    collision_detector(pot: Container, cup: Container):
    :param pot:     Pot Container Obj
    :param tea_bubble:     TeaBubble Obj
    :return:        False if no collision happens, True otherwise
    """

    if (pot.position_rect.y + pot.position_rect.height < tea_bubble.position_rect.y) or \
            (tea_bubble.position_rect.y + tea_bubble.position_rect.height < pot.position_rect.y) or \
            (pot.position_rect.x + pot.position_rect.width < tea_bubble.position_rect.x) or \
            (tea_bubble.position_rect.x + tea_bubble.position_rect.width < pot.position_rect.x):
        return False

    # Init Pot and tea_bubble Vertices
    pot_vertices = [(pot.position_rect.x, pot.position_rect.y),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y),
                    (pot.position_rect.x, pot.position_rect.y +
                     pot.position_rect.height),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y + pot.position_rect.height)]
    tea_bubble_vertices = [(tea_bubble.position_rect.x, tea_bubble.position_rect.y),
                           (tea_bubble.position_rect.x +
                            tea_bubble.position_rect.width, tea_bubble.position_rect.y),
                           (tea_bubble.position_rect.x, tea_bubble.position_rect.y +
                            tea_bubble.position_rect.height),
                           (tea_bubble.position_rect.x + tea_bubble.position_rect.width, tea_bubble.position_rect.y +
                            tea_bubble.position_rect.height)]

    logging.info('Pot Vertex' + str(pot_vertices))
    logging.info('Bub Vertex' + str(tea_bubble_vertices))

    # Check each bubble vertex, if any goes within the pot range, return True
    for vertex in tea_bubble_vertices:
        if pot_vertices[0][0] <= vertex[0] <= pot_vertices[1][0] \
                and pot_vertices[0][1] <= vertex[1] <= pot_vertices[2][1]:
            logging.info('tea_bubble and pot collided')
            return True

    return False
