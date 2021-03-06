import pygame, os
from graphics import sprite
from graphics import animation
from graphics import ui
from graphics import window
"""
Graphics
    Package to simplify rendering
    images to a window.
"""

"""
Non-Ascii input values.
These definitions can be used alongside the Window class.
    eg window.is_key_down(key) where key can equal any of the following definitions
    as well as all Ascii Literals('a','\r', etc)
"""
BUTTON_LEFT = 0
BUTTON_MIDDLE = 1
BUTTON_RIGHT = 2
SCROLL_UP = 4
SCROLL_DOWN = 5
KEY_DOWN = int(273)
KEY_UP = int(274)
KEY_RIGHT = int(275)
KEY_LEFT = int(276)


pygame.init()                   # Initialize pygame
clock = pygame.time.Clock()     # Clock object ised to stabalize framerate
prev_time = 0
images = {}                     # Images loaded from the image_loader

"""
Graphics Utility Functions
    Used by the other modules in package to simplify rendering
"""

def get_display(dimen):
    """
    return:
        instance of a pygame display
    """
    return pygame.display.set_mode(dimen)


def update():
    """
    updates the pygame display
    """
    pygame.display.flip()  # swap buffers


def render_font(display, text, font, color, pos):
    display.blit(font.render(text, 1, color), pos)


def render_rect(display, rect, color, offset):
    """
    :param display:
        display to render rect onto
    :param (x, y):
        position of rect on display (0,0) is top-left corner
    :param (w, h):
       size of rect on display (width, height)
   :param (r,g,b):
      color of rectangle
    """
    x,y = rect[0]
    w,h = rect[1]
    xoff, yoff = offset 
    r,g,b = color
    pygame.draw.rect(display, (r, g, b), ((x+xoff, y+yoff), (w, h)), 0)


def render_img(display, image, rect, offset):
    """
    :param display:
        display to render image onto
    :param image:
        source image to render
    :param (x, y):
        position of image on display (0,0) is top-left corner
    :param (w, h):
       size on display (width, height)
     :param (xoff, yoff):
        offset of translation of image on display (0,0) is top-left corner
    """
    x,y = rect[0]
    w,h = rect[1]
    xoff, yoff = offset 
    display.blit(pygame.transform.scale(image, (w, h)), (x+xoff, y+yoff))


def flip_image(image, pos):
    """
    :param image:
        source image to flip
    :param (x, y):
        booleans on whether or not to flip along its axis
    :return:
        flipped image
    """
    x,y = pos
    return pygame.transform.flip(image, x, y)





def load_image_file(img_file):
    return pygame.image.load(os.path.realpath(img_file)).convert_alpha()


def load_images(root_dir):
    images = {}
    if root_dir:
        for dir_name, subdir_list, file_list in os.walk(os.path.realpath(root_dir),topdown=False):  # do not travers . and ..
            for subdir in subdir_list:
                images.update(load_images(subdir))
            for file_name in file_list:
                images[file_name] = load_image_file('{}/{}'.format(dir_name, file_name))
    return images