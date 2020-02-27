"""
Module for managing platforms.
"""
import pygame
import constants
import speechbubbles
import events
import random
from spritesheet_functions import SpriteSheet

# These constants define our character types:
#   Name of file
#   X location of sprite
#   Y location of sprite
#   Width of sprite
#   Height of sprite


LISSI = (0, 0, 44, 88)
LI_MING = (0, 95, 54, 100)

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
                                            120)
        self.default_image = self.image.copy()

        # self.image.set_colorkey(constants.WHITE)
        self.current_animation = ""
        self.current_animation_framecount = 0
        self.current_animation_should_loop = False
        self.rect = self.image.get_rect()
        self.animations = dict()
        self.last_animation_frame_change_time = pygame.time.get_ticks()

    def add_animation(self, name, sprite_sheet_data_list, sprite_sheet_name="characters_spritesheet.png"):
        self.animations[name] = []
        sprite_sheet = SpriteSheet(sprite_sheet_name)
        for sprite_sheet_data in sprite_sheet_data_list:
            image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],
                                            constants.BLACK,
                                            120)
            self.animations[name].append(image)

    def play_animation(self, name, loop=False):
        if name in self.animations:
            self.current_animation_framecount = 0
            self.current_animation_should_loop = loop
            self.current_animation = name

    def stop_animation(self):
        self.current_animation = ""
        self.image = self.default_image

    def update(self):
        now = pygame.time.get_ticks()
        if self.current_animation and now - self.last_animation_frame_change_time > 200:
            if (self.current_animation_framecount >= len(self.animations) and self.current_animation_should_loop):
                self.current_animation_framecount = self.current_animation_framecount % len(self.animations)

            if self.current_animation_framecount < len(self.animations):
                self.image = self.animations[self.current_animation_framecount]

                self.last_animation_frame_change_time = now
            else:
                self.stop_animation()

class TaklingCharacter(Character, events.EventListener):

    def __init__(self, sprite_sheet_data, texts, optional_soundfiles=[]):
        """ Character constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        Character.__init__(self, sprite_sheet_data)
        self.texts = texts

        self.rect = self.image.get_rect()



        self.left_range_since_last_speechbubble_ended = True
        self.is_talking = False
        self.sounds = []
        for soundname in optional_soundfiles:
            self.sounds.append(pygame.mixer.Sound(soundname))
        self.in_meow_range_state_previous = False

    def notify(self, event):
        print ("notified of meow")
        if event.type == events.EVENT_SOUNDEND_MEOW:
            if len(self.sounds) > 0:
                self.sounds[random.randint(0, len(self.sounds) - 1)].play()
            else:
                self.speechbubble([" meow! "])
                print("meow back!")

    def speechbubble(self, texts):
        if not self.is_talking:
            self.is_talking = True
            self.left_range_since_last_speechbubble_ended = False
            bubble = speechbubbles.SpeechBubble(texts)
            bubble.player = self.player
            bubble.level = self.level
            bubble.character = self
            bubble.rect.x = self.rect.centerx
            bubble.rect.y = self.rect.y - self.rect.height
            self.level.speechbubble_list.add(bubble)

    def update(self):
        # Check and see if we are near the player
        Character.update(self)
        hit = pygame.sprite.collide_rect(self, self.player)

        meow_listener_rect = self.rect.copy() # need to update it, since rect constantly moves but this pro
        meow_listener_rect.inflate_ip(500, 200)

        in_meow_range = hit or meow_listener_rect.colliderect(self.player.rect)


        if hit and not self.is_talking and self.left_range_since_last_speechbubble_ended:
            self.speechbubble(self.texts)
        elif not hit and not self.is_talking:
            self.left_range_since_last_speechbubble_ended = True


        # Only react once when the meow range state changes
        if self.in_meow_range_state_previous != in_meow_range:
            if in_meow_range and not self.in_meow_range_state_previous:
                events.global_eventmanager.register(events.EVENT_SOUNDEND_MEOW, self)  # start listening to meows
            elif not in_meow_range and self.in_meow_range_state_previous:
                events.global_eventmanager.unregister(events.EVENT_SOUNDEND_MEOW, self)  # stop listening to meows
        self.in_meow_range_state_previous = in_meow_range
