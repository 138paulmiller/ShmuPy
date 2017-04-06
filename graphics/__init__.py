import image_loader
import pygame
import sprite
import animation
import window
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
font = pygame.font.SysFont('monospace bold', 42)
font_color = (250, 200, 3)
"""
Graphics Utility Functions
    Used by the other modules in package to simplify rendering
"""


def draw_font(display, text, font, color, pos):
    display.blit(font.render(text, 1, color), pos)


def get_display((width, height)):
    """
    return:
        instance of a pygame display
    """
    return pygame.display.set_mode((width, height))


def update():
    """
    updates the pygame display
    """
    pygame.display.flip()  # swap buffers


def render_rect(display, ((x, y), (w, h)), (r, g, b)):
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
    pygame.draw.rect(display, (r, g, b), ((x, y), (w, h)))


def render_img(display, image, ((x, y), (w, h))):
    """
    :param display:
        display to render image onto
    :param image:
        source image to render
    :param (x, y):
        position of image on display (0,0) is top-left corner
    :param (w, h):
       size on display (width, height)
    """
    display.blit(pygame.transform.scale(image, (w, h)), (x, y))


def flip_image(image, (x, y)):
    """
    :param image:
        source image to flip
    :param (x, y):
        booleans on whether or not to flip along its axis
    :return:
        flipped image
    """
    return pygame.transform.flip(image, x, y)

