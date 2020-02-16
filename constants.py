"""
Global constants
"""

# Colors
BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)

# Screen dimensions
SCREEN_WIDTH_dev  = 800
SCREEN_HEIGHT_dev = 600

#import gtk

#width = gtk.gdk.screen_width()
#height = gtk.gdk.screen_height()

# SCREEN_WIDTH  = width
# SCREEN_HEIGHT = height


SCREEN_WIDTH_new  = 1920
SCREEN_HEIGHT_new = 1080

Devmode = True

if Devmode:
    SCREEN_WIDTH  = SCREEN_WIDTH_dev
    SCREEN_HEIGHT = SCREEN_HEIGHT_dev
else:
    SCREEN_WIDTH  = SCREEN_WIDTH_new
    SCREEN_HEIGHT = SCREEN_HEIGHT_new