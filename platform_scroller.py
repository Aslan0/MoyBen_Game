"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Main module for platform scroller example.

From:
http://programarcadegames.com/python_examples/en/sprite_sheets/

Explanation video: http://youtu.be/czBDKWJqOao

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/

Game art from Kenney.nl:
http://opengameart.org/content/platformer-art-deluxe

"""

import pygame

import constants
import levels
import events
import speechbubbles
from player import Player





def main():
    """ Main Program """

    pygame.init()


    # Set the height and width of the screen
    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("MoyBen the Wedding")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append(levels.Level_00(player))
    level_list.append(levels.Level_01(player))
    level_list.append(levels.Level_02(player))
    level_list.append(levels.Level_03(player))

    # Set the current level
    current_level_no = 3
    current_level = level_list[current_level_no]
    current_level.play_background_music()

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 640
    player.rect.y = constants.SCREEN_HEIGHT - player.rect.height + -2000
    active_sprite_list.add(player)

    #Loop until the user clicks the close button.
    done = False
    meowcounter = 0
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    speechbubbles.preload_font()

    meowsounds = [pygame.mixer.Sound("meow00.ogg"), pygame.mixer.Sound("meow01.ogg")]

    pygame.mixer.set_reserved(1)
    meow_channel = pygame.mixer.Channel(0)  # reserved
    meow_channel.set_endevent(events.EVENT_SOUNDEND_MEOW)

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something


            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_ESCAPE:
                    done = True  # Flag that we are done so we exit this loop
                if event.key == pygame.K_SPACE:
                    #  MEOW
                    meowcounter += 1
                    meowcounter = meowcounter % len(meowsounds)
                    if pygame.mixer.get_init():
                        sound = meowsounds[meowcounter]
                        meow_channel.play(sound)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.stop()
                if event.key == pygame.K_RIGHT:
                    player.stop()


            events.global_eventmanager.notify(event)



        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()
        #print player.rect.x, player.rect.y

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.x >= 500:
            diff = player.rect.x - 500
            player.rect.x = 500
            current_level.shift_world_x(-diff)

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.x <= 120 and player.rect.x - current_level.world_shift > 120:
            diff = 120 - player.rect.x
            player.rect.x = 120
            current_level.shift_world_x(diff)

        # Move camera down, if not on the floor yet
        if player.rect.y > 500 and player.rect.y - current_level.world_shift_y < current_level.level_limit_y + player.rect.height:
            diff = player.rect.y - 500
            player.rect.y = 500
            current_level.shift_world_y(-diff)

        # Move camera up
        if player.rect.y <= 120 and player.rect.y - current_level.world_shift_y > 120:
            diff = 120 - player.rect.y
            player.rect.y = 120
            current_level.shift_world_y(diff)

        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            player.rect.x = 120
            if current_level_no < len(level_list)-1:
                current_level_no += 1
                current_level = level_list[current_level_no]
                current_level.play_background_music()
                player.level = current_level

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)

        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(30)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

if __name__ == "__main__":
    main()
