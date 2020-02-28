"""
Module for managing platforms.
"""
import pygame

from spritesheet_functions import SpriteSheet
import constants

# These constants define our platform types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite

SUSHI            = (360, 0, 70, 70)
FISTBUMP         = (430, 800,  717-430, 933-800)

class Collectible(pygame.sprite.Sprite):
    """ Collectible the user can collect on """

    def __init__(self, sprite_sheet_data):
        """ Collectible constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3])

        self.rect = self.image.get_rect()
        self.sound = 'nom.ogg'


class MovingCollectible(Collectible):
    """ This is a fancier Collectible that can actually move. """
    change_x = 0
    change_y = 0

    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0

    level = None
    player = None

    def disappear(self):
        image = pygame.Surface([1, 1]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        #image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey(constants.WHITE)
        return image

    def update(self):
        """ Move the Collectible.
        """

        # Move left/right
        # self.rect.x += self.change_x

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        #if hit:
            # We did hit the player. Make Collectible disappear and play sound

            #self.image = self.disappear()

        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1

        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
