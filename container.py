import pygame

CONTAINER_WIDTH, CONTAINER_HEIGHT = 180, 180


class Container:
    """
    Container Class     -
    Description:        Container Obj Class for Teapot and Teacup
    Class Vars:         position_rect       -   The bounding rect representing the container png
                        image               -   The transformed image object from inputted image path
                        tea_drop_position   -   The tea drop pouring start point
                        tea_level            -   The level(amount) of tea currently being held in the container
    """

    # 143 106

    def __init__(self, pos_x, pos_y, image_path, tea_level, h, w):
        self.position_rect = pygame.Rect(
            pos_x, pos_y, h, w)
        self.image = pygame.image.load(
            image_path)
        self.tea_drop_position = (
            self.position_rect.x, self.position_rect.y + CONTAINER_HEIGHT / 2)
        self.tea_level = tea_level
        self.can_receive_damage = True

    def tea_drop_position_update(self):
        """
        tea_drop_position_update    -   Arbitrary Function to update the tea drop pouring start point according to the
                                        (updated) position of the container
        :return:                    -   void
        """
        self.tea_drop_position = (
            self.position_rect.x + self.position_rect.width - 3, self.position_rect.y + 18)
