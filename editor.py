from copy import deepcopy
import scene
import graphics
import os

ENEMY = 0
PLAYER = 1  # enemy
HELPER = 2
TILE = 3  # background sprites
class Editor(object):
    def __init__(self):
        self.setting = None
        self.offset = [0, 0]     # control with arrow keys
        self.level = scene.level.Level()
        self.level.set_pause(True)
        self.node = None

    def draw(self, window):
        if self.node:
            self.node.set_pos(window.get_mouse_pos())
            self.node.draw(window)
        self.level.draw(window)

    def on_mouse_button_down(self, button):
        if button == graphics.BUTTON_LEFT and self.setting == ENEMY:
            self.level.add_enemy(deepcopy(self.node))

        print "Button Down ", button

    def on_key_down(self, key):
        if key == ord('e'):
            self.setting = ENEMY
            self.node = scene.node.load('skull.node')
        print "Key Down ", key, " Setting - ", self.setting


def run(level_file=None):
    main_window = graphics.window.Window(580, 720)
    graphics.images = graphics.image_loader.load_images("res/img/")
    editor = Editor()


    main_window.set_on_key_down(editor.on_key_down)
    main_window.set_mouse_button_down(editor.on_mouse_button_down)

    while not main_window.is_quit():
        main_window.clear((0, 10, 30))
        editor.draw(main_window)
        main_window.update()
ENEMY = 0
PLAYER = 1  # enemy
HELPER = 2
TILE = 3  # background sprites

