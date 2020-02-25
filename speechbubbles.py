"""
Module for managing platforms.
"""
import pygame

from spritesheet_functions import SpriteSheet

SPEECHBUBBLEWIDTH = 103
SPEECHBUBBLEHEEIGHT = 79
SPRITESHEETDATA = (54, 66, SPEECHBUBBLEWIDTH, SPEECHBUBBLEHEEIGHT)

SPRITESHEET = "characters_spritesheet.png"

class SpeechBubble(pygame.sprite.Sprite):
    """ Platform the user can jump on """
    level = None
    player = None
    character = None

    def __init__(self, texts):

        pygame.sprite.Sprite.__init__(self)
        self.texts = texts
        self.textcounter = 0
        self.last_changed = pygame.time.get_ticks()

        font_size = 22
        font_color = pygame.color.Color(0, 0, 0, 255)

        self.font = pygame.font.SysFont("Arial", font_size)
        self.textSurf = self.font.render("", 1, font_color)
        # self.image = pygame.Surface((width, height))

        # Grab the image for this character
        self.image = SpriteSheet(SPRITESHEET).get_image(SPRITESHEETDATA[0],
                                            SPRITESHEETDATA[1],
                                            SPRITESHEETDATA[2],
                                            SPRITESHEETDATA[3])

        self.rect = self.image.get_rect()

        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(self.textSurf, [SPEECHBUBBLEWIDTH / 2 - W / 2, SPEECHBUBBLEHEEIGHT / 2 - H / 2])

    def update(self):
        if (self.textcounter == 0 or pygame.time.get_ticks() - self.last_changed > 3000) and self.textcounter < len(self.texts):
            text = self.texts[self.textcounter]
            self.textcounter += 1
            self.last_changed = pygame.time.get_ticks()
            max_char = 1
            lines = text.split("\n")
            for line in lines:
                max_char = max(max_char, len(line))
            font_size = self.image.get_rect().width * 2.5 / max_char
            font_size = round(min(font_size, self.image.get_rect().height * 1.2 / (len(lines) + 1)))
            font_size = min(font_size, 60)

            font_color = pygame.color.Color(0, 0, 0, 255)

            self.image = SpriteSheet(SPRITESHEET).get_image(SPRITESHEETDATA[0],
                                                SPRITESHEETDATA[1],
                                                SPRITESHEETDATA[2],
                                                SPRITESHEETDATA[3])

            linecount = 0.5

            self.font = pygame.font.SysFont("Arial", int(font_size))

            for line in lines:
                self.textSurf = self.font.render(line, 1, font_color)
                W = self.textSurf.get_width()
                H = self.textSurf.get_height()
                if len(lines) > 1:
                    self.image.blit(self.textSurf, [SPEECHBUBBLEWIDTH / 2 - W / 2, linecount * (((SPEECHBUBBLEHEEIGHT * 0.92) / (len(lines) + 1)))])
                else:
                    self.image.blit(self.textSurf, [SPEECHBUBBLEWIDTH / 2 - W / 2, (SPEECHBUBBLEHEEIGHT * 0.5) - H / 2])
                linecount += 1
        elif self.textcounter >= len(self.texts) and pygame.time.get_ticks() - self.last_changed > 3000:
            # remove self after done
            self.character.is_talking = False
            self.remove(self.level.speechbubble_list)