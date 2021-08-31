#
#   collision_container.py
#   Description:            Collision Detector Functionalities for Containers(Pot/Cup)
#   Author:                 Wei Zeng
#   Date:                   Aug.26 2021
#
import os
from main import Container

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def collision_detector(pot: Container, cup: Container):
    """
    collision_detector(pot: Container, cup: Container):
    :param pot:     Pot Container Obj
    :param cup:     Cup Container Obj
    :return:        False if no collision happens, True otherwise
    """

    # Init Pot and Cup Vertices
    pot_vertices = [(pot.position_rect.x, pot.position_rect.y),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y),
                    (pot.position_rect.x, pot.position_rect.y + pot.position_rect.height),
                    (pot.position_rect.x + pot.position_rect.width, pot.position_rect.y + pot.position_rect.height)]
    cup_vertices = [(cup.position_rect.x, cup.position_rect.y),
                    (cup.position_rect.x + cup.position_rect.width, cup.position_rect.y),
                    (cup.position_rect.x, cup.position_rect.y + cup.position_rect.height),
                    (cup.position_rect.x + cup.position_rect.width, cup.position_rect.y + cup.position_rect.height)]

    # Check each pot vertex, if any goes within the cup range, return True
    for vertex in pot_vertices:
        if cup_vertices[0][0] <= vertex[0] <= cup_vertices[1][0] \
                and cup_vertices[0][1] <= vertex[1] <= cup_vertices[2][1]:
            return True

    return False


def test():
    cup1 = Container(0, 100, ROOT_DIR + r'/image/teacup.png', 0)
    pot1 = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 50)
    cup2 = Container(0, 500, ROOT_DIR + r'/image/teacup.png', 0)
    pot2 = Container(0, 100, ROOT_DIR + r'/image/teapot.png', 50)
    print(collision_detector(pot1, cup1))
    print(collision_detector(pot2, cup2))


if __name__ == '__main__':
    test()
