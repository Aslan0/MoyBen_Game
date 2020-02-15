import pygame

import constants
import platforms
import collectibles
import random

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
    level_limit = -1000

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.collectible_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.collectible_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        screen.fill(constants.BLUE)
        screen.blit(self.background, (self.world_shift // 3, 0))

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.collectible_list.draw(screen)
        self.enemy_list.draw(screen)

    def play_background_music(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(self.musicfile)
        pygame.mixer.music.play(-1, 0)

    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything: """

        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x

        for collectible in self.collectible_list:
            collectible.rect.x += shift_x

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

        level_collectibles = [ [collectibles.SUSHI, 300, 300],
                               [collectibles.SUSHI, 400, 300],
                               [collectibles.SUSHI, 500, 300],
                               [collectibles.SUSHI, 600, 300],
                               [collectibles.SUSHI, 700, 300],
                               ]

        for i in range(100):
            level_collectibles.append([collectibles.SUSHI, random.randint(200, -self.level_limit ), random.randint(0, 400)])

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
        block = collectibles.MovingCollectible(collectibles.SUSHI)
        block.rect.x = 500
        block.rect.y = 300
        block.boundary_top = 220
        block.boundary_bottom = 200
        block.change_y = 1
        block.player = self.player
        block.level = self
        self.collectible_list.add(block)


# Create platforms for the level
class Level_02(Level):
    """ Definition for level 2. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        self.background = pygame.image.load("background_02.png").convert()
        self.background.set_colorkey(constants.WHITE)
        self.level_limit = -1000

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
