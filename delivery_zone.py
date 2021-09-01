from barrier_parser import BNode
import os
import random
import pygame
import logging
from container import *
from map import *

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class DeliveryZone:
    def __init__(self, bNode: BNode):
        self.image = self.image = pygame.image.load(ROOT_DIR + '\image\\' + bNode.image_path).convert_alpha()
        self.pos_x = bNode.pos_x
        self.width = bNode.width
        self.tip_points = bNode.tips_list
        self.tea_level = 0
        self.is_full = False
        self.tea_requirement = random.randint(10, 15)

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
        if container_top_pos_y <= self.tip_points[0] or container_bottom_pos_y >= self.tip_points[1]:
            logging.info('Inside delivery zone')
            if container.tea_level > self.tea_requirement - self.tea_level:
                self.tea_level = self.tea_requirement
                self.is_full = True
                container.tea_level -= self.tea_requirement - self.tea_level
            else:
                self.tea_level += container.tea_level
                container.tea_level = 0
            
            return True
        else:
            return False
    