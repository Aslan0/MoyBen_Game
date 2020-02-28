import pygame

import constants
import platforms
import characters
import speechbubbles
import collectibles
import random
import time

def add_platforms_to_list_repeated_horizontally(list_to_add_to, sprite_sheet_data_quadruple, pos_x_start, pos_y_start,
                                                times, additional_offset_x=0, additional_offset_y=0):
    offset_x = sprite_sheet_data_quadruple[2] + additional_offset_x
    offset_y = additional_offset_y

    for i in range(0, times):
        list_to_add_to.append([sprite_sheet_data_quadruple, pos_x_start + i * offset_x, pos_y_start + i * offset_y])

class Level():
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game. """
    platform_list = None
    enemy_list = None
    collectible_list = None

    musicfile = "silence.ogg"

    # Background image
    background = None

    # How far this world has been scrolled left/right
    world_shift = 0
    world_shift_y = 0
    level_limit = -1000

    level_limit_y = 420
    gravity_factor = 3
    background_final = None

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.collectible_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.character_list = pygame.sprite.Group()
        self.speechbubble_list = pygame.sprite.Group()

        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.collectible_list.update()
        self.enemy_list.update()
        self.character_list.update()
        self.speechbubble_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)

        # allows to load two backgrounds, making the heads in the main menu wobble
        try:
            if ( (time.time() % 1) > 0.5 ):
                self.background_final = self.background2
            else:
                self.background_final = self.background
        except:
            pass

        # in case you want to switch resolutions to anything that isnt 800x600 - this is the first of many codechanges necessary
        #if not constants.Devmode:
        #    self.background_final = pygame.transform.scale(self.background_final, (constants.SCREEN_WIDTH_new, constants.SCREEN_HEIGHT_new))

        if self.background_final:
            screen.blit(self.background_final, (self.world_shift // 3, self.world_shift_y))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.collectible_list.draw(screen)
        self.enemy_list.draw(screen)
        self.character_list.draw(screen)
        self.speechbubble_list.draw(screen)

    def play_background_music(self):
        if (self.musicfile):
            pygame.mixer.music.stop()
            # print("musicfile:" + self.musicfile)
            pygame.mixer.music.load(self.musicfile)
            pygame.mixer.music.play(-1, 0)

    def shift_world_x(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for character in self.character_list:
            character.rect.x += shift_x

        for speechbubble in self.speechbubble_list:
            speechbubble.rect.x += shift_x

        for collectible in self.collectible_list:
            collectible.rect.x += shift_x

    def shift_world_y(self, shift_y):

        shift = shift_y

        # if camera is moving down
        if (shift_y < 0):
            shift_highest_allowed_down = self.world_shift_y # dont go below floor with camera!
            shift = max(shift_highest_allowed_down, shift_y)
        elif shift_y > 0:
            shift_highest_allowed_up = self.level_limit_y - self.world_shift_y#  dont go above ceiling
            shift = min(shift_highest_allowed_up, shift_y)



        # Keep track of the shift amount
        self.world_shift_y += shift

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.y += shift

        for enemy in self.enemy_list:
            enemy.rect.y += shift


        for character in self.character_list:
            character.rect.y += shift

        for speechbubble in self.speechbubble_list:
            speechbubble.rect.y += shift
        
        for collectible in self.collectible_list:
            collectible.rect.x += shift

        return shift

class Level_00(Level):
    """ Definition for Main Screen """

    def __init__(self, player):
        """ Create level 0. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.musicfile = 'I Can Go The Distance - Hercules Lyrics-2aqpF-MwyUs.ogg'
        self.background = pygame.image.load("background_00a.png").convert()
        self.background.set_colorkey(constants.BLUE)

        self.background2 = pygame.image.load("background_00b.png").convert()
        self.background2.set_colorkey(constants.BLUE)

        # self.gravity_factor = 2
        self.level_limit = -3000


        #SchiffImg = pygame.image.load('Schiff1.png')
        #if loopRound % (2*AnzahlFrames) > (AnzahlFrames - 1):
         #   SchiffImg = pygame.image.load('Schiff2.png')




# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)
        self.musicfile = "Billie Eilish - Bad Guy (Cover by UMC)_-EjMtDFRl-Ws.ogg"
        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -2500


        # Array with type of platform, and x, y location of the platform.
        level_platforms = [ [platforms.GRASS_LEFT, 500, 500],
                  [platforms.GRASS_MIDDLE, 570, 500],
                  [platforms.GRASS_RIGHT, 640, 500],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]

        # manual placements for collectibles
        level_collectibles = [ [collectibles.SUSHI, 300, 300],
                               [collectibles.SUSHI, 400, 300],
                               [collectibles.SUSHI, 500, 300],
                               [collectibles.SUSHI, 600, 300],
                               [collectibles.SUSHI, 700, 300],
                               ]

        # random mass placement for collectibles
        for i in range(10):
            level_collectibles.append([collectibles.SUSHI, random.randint(200, -self.level_limit), random.randint(0, 400)])

        # Go through the array above and add platforms
        for platform in level_platforms:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        for collectible in level_collectibles:
            block = collectibles.Collectible(collectible[0])
            block.rect.x = collectible[1]
            block.rect.y = collectible[2]
            block.player = self.player
            self.collectible_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1400
        block.rect.y = 280
        block.boundary_left = 1400
        block.boundary_right = 1600
        block.change_x = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        # Add a custom moving collectible
        #block = collectibles.MovingCollectible(collectibles.SUSHI)
        #block.rect.x = 500
        #block.rect.y = 300
        #block.boundary_top = 220
        #block.boundary_bottom = 200
        #block.change_y = 1
        #block.player = self.player
        #block.level = self
        #self.collectible_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -4000

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT, 500, 550],
                  [platforms.STONE_PLATFORM_MIDDLE, 570, 550],
                  [platforms.STONE_PLATFORM_RIGHT, 640, 550],
                  [platforms.GRASS_LEFT, 800, 400],
                  [platforms.GRASS_MIDDLE, 870, 400],
                  [platforms.GRASS_RIGHT, 940, 400],
                  [platforms.GRASS_LEFT, 1000, 500],
                  [platforms.GRASS_MIDDLE, 1070, 500],
                  [platforms.GRASS_RIGHT, 1140, 500],
                  [platforms.STONE_PLATFORM_LEFT, 1120, 280],
                  [platforms.STONE_PLATFORM_MIDDLE, 1190, 280],
                  [platforms.STONE_PLATFORM_RIGHT, 1260, 280],
                  ]


        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)

        # Add a custom moving platform
        block = platforms.MovingPlatform(platforms.STONE_PLATFORM_MIDDLE)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -1
        block.player = self.player
        block.level = self
        self.platform_list.add(block)


class Level_03(Level):
    """ Definition for level 3, aka the excel level"""

    def __init__(self, player):
        """ Create level 3. """

        # Call the parent constructor
        Level.__init__(self, player)

        # self.gravity_factor = 1

        self.background = pygame.image.load("background_03.png").convert()
        # self.background.set_colorkey(constants.WHITE)
        self.level_limit = -9000
        self.level_limit_y = 1690
        self.world_shift_y = -1200
        self.musicfile = "Jaws Theme Song-A9QTSyLwd4w.ogg"

        # Array with type of platform, and x, y location of the platform.
        level = [ [platforms.STONE_PLATFORM_LEFT_SMALL, 0, self.level_limit_y + self.world_shift_y + 50],
                  [platforms.STONE_PLATFORM_LEFT_SMALL, 11000, self.level_limit_y + self.world_shift_y + 60],
                  ]
        add_platforms_to_list_repeated_horizontally(level, platforms.STONE_PLATFORM_MIDDLE_SMALL, -1000,
                                                    self.level_limit_y + self.world_shift_y + 50,
                                                    200)

        stair_platform = platforms.STONE_PLATFORM_MIDDLE
        add_platforms_to_list_repeated_horizontally(level, stair_platform, 5000,
                                                    self.level_limit_y + self.world_shift_y - 50,
                                                    10, -stair_platform[2] -140, -140)

        level2 = [[platforms.STONE_PLATFORM_MIDDLE, x, self.level_limit_y + self.world_shift_y + -1350] for x in range(0, 3640, 50)]


        for lvl in level2:
            level.append(lvl)

        level.append([platforms.BOULDER, 50, self.level_limit_y + self.world_shift_y + -1550])

        # Go through the array above and add platforms
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            block.player = self.player
            self.platform_list.add(block)


        # Add a lissi
        lissi = characters.TaklingCharacter(characters.LISSI, ["das ist\n doch \nalbern"], [])
        lissi.rect.x = 500
        lissi.rect.y = self.level_limit_y + self.world_shift_y + 55 - lissi.rect.height
        # block.boundary_top = 100
        # block.boundary_bottom = 550
        # block.change_y = -1
        lissi.player = self.player
        lissi.level = self
        self.character_list.add(lissi)


        # Add a li-ming
        li_ming = characters.TaklingCharacter(characters.LI_MING, [" Aaaargh! ", "DAS \nwillst Du\n machen?", "Why? \nEcht jetzt?!", "Na gut \nich mach mit."], optional_soundfiles=["li_blergh.ogg"])
        li_ming.rect.x = 1000
        li_ming.rect.y = self.level_limit_y + self.world_shift_y + 55 - li_ming.rect.height
        # block.boundary_top = 100
        # block.boundary_bottom = 550
        # block.change_y = -1
        li_ming.player = self.player
        li_ming.level = self
        self.character_list.add(li_ming)

        level_collectibles = [[collectibles.FISTBUMP, 50, self.level_limit_y + self.world_shift_y + -1550],
                              [collectibles.SUSHI, 50, self.level_limit_y + self.world_shift_y + -1650]]

        for collectible in level_collectibles:
            block = collectibles.Collectible(collectible[0])
            if collectible[0] == collectibles.FISTBUMP:
                block.sound = 'woop_woop.ogg'
            block.rect.x = collectible[1]
            block.rect.y = collectible[2]
            block.player = self.player
            self.collectible_list.add(block)

