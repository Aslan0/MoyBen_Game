"""
Module for managing platforms.
"""
import pygame

from spritesheet_functions import SpriteSheet

SPEECHBUBBLEWIDTH = 103
SPEECHBUBBLEHEEIGHT = 79
SPRITESHEETDATA = (54, 66, SPEECHBUBBLEWIDTH, SPEECHBUBBLEHEEIGHT)

SPRITESHEET = "characters_spritesheet.png"

def preload_font():
    # subsequent calls will not lagg, even if we directly throw away the result
    font = pygame.font.SysFont("Arial", 70)


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


        # Grab the image for this character

        self.speechbubble_image = SpriteSheet(SPRITESHEET).get_image(SPRITESHEETDATA[0],
                                            SPRITESHEETDATA[1],
                                            SPRITESHEETDATA[2],
                                            SPRITESHEETDATA[3])
        self.image = self.speechbubble_image.copy()


        self.rect = self.image.get_rect()


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


            self.image = self.speechbubble_image.copy()


            SpriteSheet(SPRITESHEET).get_image(SPRITESHEETDATA[0],
                                                SPRITESHEETDATA[1],
                                                SPRITESHEETDATA[2],
                                                SPRITESHEETDATA[3])

            linecount = 0.5

            self.font = pygame.font.SysFont("Arial", int(font_size))  # laggy - consider preloading

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

