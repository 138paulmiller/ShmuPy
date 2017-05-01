import scene
import random

TOPDOWN = 'topdown'
SIDESCROLL = 'sidescroll'

class Level(object):
    def __init__(self):
        self.enemies = []  # enemy nodes
        self.boss = None  # boss node
        self.player = None  # player node
        self.scroll = None
        self.pause = False

    def set_player(self, player):
        self.player = player

    def get_player(self):
        return self.player

    def set_pause(self, pause):
        self.pause = pause

    def set_scroll(self, scroll):
        self.scroll =scroll

    def get_scroll(self):
        return self.scroll

    def set_boss(self, boss):
        self.boss = boss

    def add_enemy(self, enemy):
        self.enemies.append(enemy)

    def get_enemies(self):
        return self.enemies

    def draw(self, window):
        remove = []
        for e in self.enemies:
            if not self.pause:
                e.update()
                y = e.get_pos()[1]
                if y < window.height:
                    e.show()
                    if y + e.get_size()[1] > 0:
                        if self.player:
                            if e.is_alive() and abs(e.get_pos()[0]  - self.player.get_pos()[0]) < 12:
                                if random.randint(0, 3) == 0:
                                    e.shoot()
                            scene.node.handle_collision(self.player, e)
                else:
                    remove.append(e)
            else:
                e.show()
            e.draw(window)
        for r in remove:
            if r in self.enemies:
                self.enemies.remove(r)
        if self.player:
            if not self.pause:
                self.player.update()
            self.player.draw(window)

