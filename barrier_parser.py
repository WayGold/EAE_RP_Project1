#
#   barrier_parser.py
#   Description:        Txt parser functionalities that parse a txt file of barrier data into a dictionary
#   Author:             Wei Zeng
#   Date:               Aug.26th 2021
#

import os
import logging

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class BNode:
    """
    BNode Class:
    Description:    A Node class to store barrier data
    """
    def __init__(self, index, image_path, width, pos_x, tips_list):
        self.index = index
        self.image_path = image_path
        self.pos_x = pos_x
        self.tips_list = tips_list
        self.width = width

    def __str__(self):
        """
        Str casting overloading to print the Node data
        :return:    The Str to be casted to. Data in the node basically.
        """
        return str('BNode #: ' + str(self.index) + '\nImage Path: ' + str(self.image_path) + '\nX Position: ' +
                   str(self.pos_x) + '\nTips List: ' + str(self.tips_list))


def load_txt(file_path):
    """
    load_txt(file_path):
    :param file_path:       Load the barrier data txt file to a Node list
    :return:                The list containing all barrier nodes
    """
    file = open(file_path, 'r')
    lines = file.readlines()

    all_barrier_nodes = []

    for line in lines:
        # Get rid of endl char at end of line if exist and split into list by spaces
        data_list = line.rstrip('\n').split(' ')
        logging.info(data_list)
        tips_list = []

        # Extract tips data to list
        for i, data in enumerate(data_list):
            if i not in range(0, 4):
                tips_list.append(int(data))

        # Append Node to list
        all_barrier_nodes.append(BNode(int(data_list[0]), data_list[1], int(data_list[2]), int(data_list[3]), tips_list))

    # Call str overloading function
    for node in all_barrier_nodes:
        logging.info(str(node))

    return all_barrier_nodes
