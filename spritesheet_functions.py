"""
This module is used to pull individual sprites from sprite sheets.
"""
import pygame

import constants

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()


    def get_image(self, x, y, width, height, colorkey=constants.BLACK, padding_x=0, padding_y=0):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pygame.Surface([width + 2 * padding_x, height + 2 * padding_y], 0).convert()

        # Assuming black works as the transparent color
        image.set_colorkey(colorkey)

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (padding_x, padding_y), (x, y, width, height))


        # Return the image
        return image
