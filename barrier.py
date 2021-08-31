from barrier_parser import BNode
import os
import pygame

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class Barrier:
    """
    Barrier Class:
    Description:    Class for our obsticle barriers
    """
    def __init__(self, bNode: BNode):
        self.image = pygame.image.load(ROOT_DIR + '\image\\' + bNode.image_path).convert_alpha()
        self.pos_x = bNode.pos_x
        self.tip_points = bNode.tips_list

    def get_global_position(self, map_pos_x):
        return self.pos_x + map_pos_x  
    