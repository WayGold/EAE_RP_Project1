from barrier_parser import BNode
import os
import logging
import pygame
from container import *
from map import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Barrier:
    """
    Barrier Class:
    Description:    Class for our obsticle barriers
    """
    def __init__(self, bNode: BNode):
        self.image = pygame.image.load(ROOT_DIR + '\image\\' + bNode.image_path).convert_alpha()
        self.pos_x = bNode.pos_x
        self.width = bNode.width
        self.tip_points = bNode.tips_list
        

    def get_global_position(self, map_pos_x):
        return self.pos_x + map_pos_x  

    def detect_collision(self, container: Container, map: Map):
        # if container is no where near the barrier horizontally, there is no collision so return true immediately to
        # save power
        if container.position_rect.x + container.position_rect.width < self.get_global_position(map.starting_dx) or container.position_rect.x > self.get_global_position(map.starting_dx) + self.width:
            return False

        # get container top and bottom y coordinates
        container_top_pos_y = container.position_rect.y
        container_bottom_pos_y = container.position_rect.y + container.position_rect.height

        if len(self.tip_points) == 2:
            if container_top_pos_y <= self.tip_points[0] or container_bottom_pos_y >= self.tip_points[1]:
                logging.info('barrier hit')
                container.can_receive_damage = False
                return True
        # else condition is == 4
        else:
            if (container_top_pos_y > self.tip_points[0] and container_bottom_pos_y < self.tip_points[1]) or (
                    container_top_pos_y > self.tip_points[2] and container_bottom_pos_y < self.tip_points[3]):
                return False
            else:
                logging.info('barrier hit')
                container.can_receive_damage = False
                return True
    
    