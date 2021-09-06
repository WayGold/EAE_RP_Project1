#
# container.py      -   Container Obj Class, used for creating tea pot and tea cup
# Author:           -   Wei Zeng
#                       Ogulcan Buyuksandalyaci
# Date:             -   Aug.24 2021
#
from container import *


WIDTH, HEIGHT = 1600, 900
TEA_DROP_WIDTH, TEA_DROP_HEIGHT = 9, 23


class TeaDrop:
    """
    TeaDrop Class   -
    Description:    Tea Drop Object representing each drop of tea
    Class Vars:     position_rect   -   The bounding rect representing the drop png
                    image           -   The transformed image object from inputted image path
    """

    def __init__(self, pos_x, pos_y, image_path):
        self.position_rect = pygame.Rect(
            pos_x, pos_y, TEA_DROP_WIDTH, TEA_DROP_HEIGHT)
        self.image = pygame.transform.scale(pygame.image.load(
            image_path), (TEA_DROP_WIDTH, TEA_DROP_HEIGHT))


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
        elif cup.position_rect.contains(teaDrop.position_rect):
            cup.tea_level += 1

    return qualified
