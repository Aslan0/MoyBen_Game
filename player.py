"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame

import constants

from platforms import MovingPlatform
from spritesheet_functions import SpriteSheet

ACCELERATION_X_AIR = 2
ACCELERATION_X_GROUND = 15
WALK_SPEED_MAX_DEFAULT = 15

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """

    # -- Attributes
    # Set speed vector of player
    change_x = 0
    change_y = 0

    # This holds all the images for the animated walk left/right
    # of our player
    walking_frames_l = []
    walking_frames_r = []

    # What direction is the player facing?
    direction = "R"
    horizontal_movement_factor = 1
    direction_factor = 0
    walk_speed_max = WALK_SPEED_MAX_DEFAULT
    acceleration_x = 0

    # List of sprites we can bump against
    level = None
    jump_factor = 1.9

    is_screaming = False
    screaming_end_timestamp = 0

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the right facing images into a list
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)

        # Load all the right facing images, then flip them
        # to face left.
        image = sprite_sheet.get_image(0, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        image = pygame.transform.flip(image, True, False)
        self.walking_frames_l.append(image)

        # Set the image the player starts with
        self.image = self.walking_frames_r[0]

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

    def update(self):
        """ Move the player.
            handle collectible collection
        """
        # Gravity
        self.calc_grav()


        if self.has_footing():
            self.acceleration_x = ACCELERATION_X_GROUND
            if self.direction_factor == 0:
                self.change_x *= 0.3
                if abs(self.change_x) <= 0.1:
                    self.change_x = 0
        else:
            self.acceleration_x = ACCELERATION_X_AIR

        self.change_x = self.change_x + self.acceleration_x * self.direction_factor
        self.change_x = min(self.change_x, self.walk_speed_max)
        self.change_x = max(self.change_x, -self.walk_speed_max)




        # Dont walk out of the left side of the level
        if self.change_x < 0 and not self.rect.x - self.level.world_shift > self.rect.width / 2:
            self.change_x = 0

        # Dont walk out of the right side of the level
        if self.change_x > 0 and not self.rect.x - self.level.world_shift > self.level.level_limit:
            self.change_x = 0


        # p rint("player" + str(self.rect))
        # Move left/right
        self.rect.x += self.change_x * self.horizontal_movement_factor

        # print(self.level.world_shift)
        # dont allow the player to walk left
        if self.level.world_shift > 0:
            self.level.world_shift = -10


        pos = self.rect.x + self.level.world_shift

        # changes sprite animation direction
        if self.direction == "R":
            frame = (pos // 30) % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = (pos // 30) % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right




        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0

            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x

        collectible_hit_list = pygame.sprite.spritecollide(self, self.level.collectible_list, False)
        for collect in collectible_hit_list:
            # let the collectible disappear
            collect.rect.top = 5000
            MeowSound = pygame.mixer.Sound('nom.ogg')
            MeowSound.play()

        self.is_screaming = pygame.time.get_ticks() <= self.screaming_end_timestamp

        screaming_height_min = self.level.level_limit_y * 0.5
        if not self.is_screaming and self.change_y > 47 and (self.rect.y - self.level.world_shift_y < self.level.level_limit_y + self.rect.height - screaming_height_min):
            self.scream()

    def scream(self):
        sound = pygame.mixer.Sound('scream00.ogg')
        sound.play()
        self.screaming_end_timestamp = pygame.time.get_ticks() + 1000 * sound.get_length()
        self.is_screaming = True

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1 * self.level.gravity_factor
        else:
            self.change_y += .35 * self.level.gravity_factor


        # See if we are on the ground.
        if self.rect.y - self.level.world_shift_y >= self.level.level_limit_y + self.rect.height and self.change_y > 0:
            self.change_y = 0
            self.rect.y = self.level.level_limit_y + self.rect.height + self.level.world_shift_y

    def has_footing(self):

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 5
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 5

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.y - self.level.world_shift_y >= self.level.level_limit_y + self.rect.height:
            return True
        return False

    def jump(self):

        """ Called when user hits 'jump' button. """
        if self.has_footing():
            self.change_y = -10 * self.jump_factor

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """

        self.direction = "L"
        self.direction_factor = -1

    def go_right(self):
        """ Called when the user hits the right arrow. """

        self.direction = "R"
        self.direction_factor = 1


    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.direction_factor = 0
        self.acceleration_x = 0
