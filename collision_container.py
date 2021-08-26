#
#   collision_container.py
#   Description:            Collision Detector Functionalities for Containers(Pot/Cup)
#   Author:                 Wei Zeng
#   Date:                   Aug.26 2021
#
from barrier import Barrier
import os
from main import Container

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def collision_detector(pot: Container, cup: Container):
    """
    collision_detector(pot: Container, cup: Container):
    :param pot:     Pot Container Obj
    :param cup:     Cup Container Obj
    :return:        False if no collision happens, true otherwise
    """

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

    # Check each pot vertex, if any goes within the cup range, return false
    for vertex in pot_vertices:
        if cup_vertices[0][0] <= vertex[0] <= cup_vertices[1][0] \
                and cup_vertices[0][1] <= vertex[1] <= cup_vertices[2][1]:
            print('cup and pot collided')
            return True

    return False


def barrier_collision_detector(container: Container, barrier: Barrier):
    """
    collision_detector(pot: Container, cup: Container):
    :param container:   Container Obj (either cup or pot)
    :param barrier:     Barrier Obj
    :return:        False if no collision happens, true otherwise
    """

    # if container is no where near the barrier horizontally, there is no collision so return true immidiately to save power
    if barrier.pos_x >= container.position_rect.x and barrier.pos_x <= container.position_rect.x + container.position_rect.width:
        # get barrier tip points array
        barrier_tip_points = barrier.tip_points
        # get container top and bottom y coordinates
        container_top_pos_y = container.position_rect.y
        container_bottom_pos_y = container.position_rect.y + container.position_rect.height

        if len(barrier_tip_points) == 2:
            if container_top_pos_y <= barrier_tip_points[0] or container_bottom_pos_y >= barrier_tip_points[1]:
                print('collided with barrier')
                return True
        # else condition is == 4
        else:
            if (container_top_pos_y > barrier_tip_points[0] and container_bottom_pos_y < barrier_tip_points[1]) or (container_top_pos_y > barrier_tip_points[2] and container_bottom_pos_y < barrier_tip_points[3]):
                return False
            else:
                print('collided with barrier')
                return True
    else:
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
