"""
Module for managing platforms.
"""
import pygame
import constants
import speechbubbles
from spritesheet_functions import SpriteSheet

# These constants define our character types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite


LISSI = (0, 0, 44, 88)

class Character(pygame.sprite.Sprite):
    """ Platform the user can jump on """
    level = None
    player = None

    def __init__(self, sprite_sheet_data):
        """ Character constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("characters_spritesheet.png")
        # Grab the image for this character
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],
                                            constants.BLACK,
                                            20)

        # self.image.set_colorkey(constants.WHITE)

        self.rect = self.image.get_rect()

class TaklingCharacter(Character):

    def __init__(self, sprite_sheet_data, texts, optional_soundfile=""):
        """ Character constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        Character.__init__(self, sprite_sheet_data)
        self.texts = texts

        self.rect = self.image.get_rect()

        self.left_range_since_last_speechbubble_ended = True
        self.is_talking = False
        self.optional_soundfile = optional_soundfile


    def update(self):

        # Check and see if we are near the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit and not self.is_talking and self.left_range_since_last_speechbubble_ended:
            self.is_talking = True
            self.left_range_since_last_speechbubble_ended = False
            bubble = speechbubbles.SpeechBubble(self.texts)
            bubble.player = self.player
            bubble.level = self.level
            bubble.character = self
            bubble.rect.x = self.rect.centerx
            bubble.rect.y = self.rect.y - self.rect.height
            self.level.speechbubble_list.add(bubble)
        elif not hit and not self.is_talking:
            self.left_range_since_last_speechbubble_ended = True
