WIDTH, HEIGHT = 1600, 900
BACKGROUND_WIDTH = 4000
BACKGROUND_SPEED = 2
import pygame

class Map:
    """
    Map Class     -
    Description:        Map Obj Class for background image and obsticle hosting
    Class Vars:         starting_dx         -   The maps left most x coordinate for sliding purposes
                        image               -   The transformed image object from inputted image path
    """

    def __init__(self, background_image_path, barriers, delivery_zones):
        self.image = pygame.transform.scale(pygame.image.load(background_image_path),
                                            (BACKGROUND_WIDTH, HEIGHT)).convert_alpha()
        self.starting_dx = 0
        self.barriers = barriers
        self.delivery_zones = delivery_zones

    def slideMap(self):
        """
        tea_drop_position_update    -   Function to update the left most x coordinate of the map
                                        object to give thge illusion of sliding and also
                                        (resets to 0 to make it loop) 
        :return:                    -   void
        """
        if self.starting_dx + BACKGROUND_WIDTH == WIDTH:
            self.starting_dx = 0
        self.starting_dx -= BACKGROUND_SPEED

    def are_delivery_zones_full(self):
        for zone in self.delivery_zones:
            if not zone.is_full:
                return False

        return True

                
