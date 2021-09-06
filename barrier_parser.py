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
    :return:                The list containing all barrier nodes and all delivery zone nodes
    """
    file = open(file_path, 'r')
    lines = file.readlines()

    all_barrier_nodes = []
    all_delivery_nodes = []
    working_list = []

    for line in lines:
        # Get rid of end line char at end of line if exist and split into list by spaces
        data_list = line.rstrip('\n').split(' ')
        logging.info(data_list)
        tips_list = []

        if len(data_list) == 1 and data_list[0] == '-':
            # Save Barrier Nodes and Reset Working List
            all_barrier_nodes = working_list
            working_list = []
            logging.info('Reading Delivery Zone Data...')
        else:
            # Extract tips data to list
            for i, data in enumerate(data_list):
                if i not in range(0, 4):
                    tips_list.append(int(data))

            # Append Node to list
            working_list.append(BNode(int(data_list[0]), data_list[1], int(data_list[2]), int(data_list[3]), tips_list))

    # Save Delivery Nodes
    all_delivery_nodes = working_list

    # Call str overloading function
    logging.info('All Barriers: ')
    for node in all_barrier_nodes:
        logging.info(str(node))

    logging.info('All Delivery Zones: ')
    for node in all_delivery_nodes:
        logging.info(str(node))

    return [all_barrier_nodes, all_delivery_nodes]


def test():
    load_txt('/Users/wzeng/EAE_Rapid/EAE_RP_Project1/barrier_data.txt')


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    test()
