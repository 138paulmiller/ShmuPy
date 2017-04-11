from copy import deepcopy
import scene
import graphics
import ui
import os
    # TODO add node img for starting pos
    # TODO ui for selecting player, helper and enemy nodes by listing files
    # TODO export and import for level, also new level

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
        self.cursor_node = None

    def draw(self, window):
        if self.cursor_node:
            self.cursor_node.set_pos(window.get_mouse_pos())
            self.cursor_node.draw(window)
        for e in self.level.get_enemies():
           e.set_translate(self.offset)
        self.level.draw(window)

    def on_mouse_button_down(self, button):
        if button == graphics.BUTTON_LEFT and self.setting == ENEMY:
            node = deepcopy(self.cursor_node)
            node.move_by((-self.offset[0], -self.offset[1]))
            self.level.add_enemy(node)

        print "Button Down ", button

    def on_key_down(self, key):
        if key == ord(' '):
            print "Toggle Pause"
            self.level.set_pause(not self.level.pause)
        elif key == ord('e'):
            self.setting = ENEMY
            self.cursor_node = scene.node.load('skull.node')
        print "Key Down ", key, " Setting - ", self.setting


def run(level_file=None):

    main_window = graphics.window.Window(580, 720)
    graphics.images = graphics.image_loader.load_images("res/img/")

    nodes = []
    bullets = []
    for dir_name, subdir_list, file_list in os.walk(os.path.realpath("res/nodes/"),
                                                            topdown=False):  # do not travers . and ..
        for file_name in file_list:
            nodes.append(file_name)
    for dir_name, subdir_list, file_list in os.walk(os.path.realpath("res/bullets/"),
                                                            topdown=False):  # do not travers . and ..
        for file_name in file_list:
            bullets.append(file_name)
    print "\nNodes ", nodes
    print "\nBullets", bullets
    border = 5
    font_size = 24
    label = ui.label.Label("Label", (10, 10),
                           (font_size*5, font_size+border),
                           font_size, border)
    editor = Editor()

    main_window.set_on_key_down(editor.on_key_down)
    main_window.set_mouse_button_down(editor.on_mouse_button_down)

    while not main_window.is_quit():
        timedelta = graphics.clock.tick(60)
        main_window.clear((0, 10, 30))

        if main_window.is_key_down(graphics.KEY_LEFT) or \
            main_window.is_key_down('a'):
            editor.offset[0] -= 1

        if main_window.is_key_down(graphics.KEY_RIGHT)or \
            main_window.is_key_down('d'):
            editor.offset[0] += 1

        if main_window.is_key_down(graphics.KEY_UP)or \
            main_window.is_key_down('w'):
            editor.offset[1] -= 1

        if main_window.is_key_down(graphics.KEY_DOWN)or \
            main_window.is_key_down('s'):
            editor.offset[1] += 1
        editor.draw(main_window)
        label.draw(main_window)
        main_window.update()


