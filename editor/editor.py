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
        self.level = scene.level_loader.load('level0')
        self.level.set_pause(True)
        self.cursor_node = None
        self.players = load_file_names('res/nodes/players')

        self.enemies = load_file_names('res/nodes/enemies')
        self.bullets = load_file_names('res/bullets')
        print "\nPlayers : ", self.players

        print "\nEnemies : ", self.enemies
        print "\nBullets : ", self.bullets
        border = 5
        font_size = 24
        font_color = (200, 150, 250)
        rect_color = (200, 20, 0)
        highlight_color = (170, 0, 240)

        self.menu = ui.menu.Menu(font_color,
                                 rect_color,
                                 highlight_color,
                                  (font_size * 5, font_size + border),
                                  font_size,
                                  border)

        self.menu.add_label('Player', 'Add Player', self.on_menu_label_click)
        self.menu.add_label('Enemy', 'Add Enemy', self.on_menu_label_click)
        self.menu.add_label('Import', 'Import Level')
        self.menu.add_label('Export', 'Export Level')

        self.menu.open()

        self.player_menu = ui.menu.Menu(font_color,
                                       rect_color,
                                       highlight_color,
                                      (font_size * 5, font_size + border),
                                      font_size,
                                      border)
        i = 0
        for n in self.players:
            self.player_menu.add_label('Player_{}'.format(i), n, self.on_player_menu_label_click)
            i += 1
        self.enemy_menu = ui.menu.Menu(font_color,
                                        rect_color,
                                        highlight_color,
                                        (font_size * 5, font_size + border),
                                        font_size,
                                        border)
        i = 0
        for n in self.enemies:
            self.enemy_menu.add_label('Enemy_{}'.format(i), n, self.on_enemy_menu_label_click)
            i += 1

    def draw(self, window):
        for e in self.level.get_enemies():
           e.set_translate(self.offset)
        if self.level.get_player():
            self.level.get_player().set_translate(self.offset)
        self.level.draw(window)
        self.menu.draw(window)
        self.player_menu.draw(window)
        self.enemy_menu.draw(window)
        if self.cursor_node:
            self.cursor_node.set_pos(window.get_mouse_pos())
            self.cursor_node.draw(window)

    def on_menu_label_click(self, label):
        self.enemy_menu.hide()
        self.player_menu.hide()
        print "click"
        if label.text == 'Add Player':
            self.setting = PLAYER
            self.player_menu.pos[0] = self.menu.pos[0] + self.menu.size[0]
            self.player_menu.pos[1] = label.pos[1]
            self.player_menu.open()
            #self.menu.toggle_sticky()

        elif label.text == 'Add Enemy':
            self.setting = ENEMY
            self.enemy_menu.pos[0] = self.menu.pos[0] + self.menu.size[0]
            self.enemy_menu.pos[1] = label.pos[1]
            self.enemy_menu.open()
            # self.menu.toggle_sticky()

    def on_player_menu_label_click(self, label):
        if self.setting == PLAYER:
            node_parent_dir = 'players/'
            self.cursor_node = scene.node_loader.load(node_parent_dir + label.text)
            self.player_menu.hide()
            for c in self.cursor_node.get_children():
                c.hide()

    def on_enemy_menu_label_click(self, label):
        if self.setting == ENEMY:
            node_parent_dir = 'enemies/'
            self.cursor_node = scene.node_loader.load(node_parent_dir + label.text)
            self.enemy_menu.hide()
            for c in self.cursor_node.get_children():
                c.hide()

    def on_mouse_button_down(self, button):
        if button == graphics.BUTTON_LEFT:
            # select from main menu
            if self.menu.selected:
                self.menu.click()
                # selected from player menu
            elif self.player_menu.selected:
                self.player_menu.click()
            # selected from enemy menu
            elif self.enemy_menu.selected:
                self.enemy_menu.click()
            elif self.cursor_node:
                self.enemy_menu.hide()
                self.player_menu.hide()
                node = deepcopy(self.cursor_node)
                node.move_by((-self.offset[0], -self.offset[1]))
                if self.setting == ENEMY:
                    self.level.add_enemy(node)
                elif self.setting == PLAYER:
                    self.level.set_player(node)


            # is clicked outside menu but cursor node is valid


        print "Button Down ", button

    def on_key_down(self, key):
        if key == ord(' '):
            print "Toggle Pause"
            self.level.set_pause(not self.level.pause)
        elif key == ord('e'):
            self.setting = ENEMY
        print "Key Down ", key, " Setting - ", self.setting


def load_file_names(dir_path):
    file_names = []
    for dir_name, subdir_list, file_list in os.walk(os.path.realpath(dir_path),topdown=False):  # do not travers . and ..
        for file_name in file_list:
            file_names.append(file_name)
    return file_names




