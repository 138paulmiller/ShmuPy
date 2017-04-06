import node

class Level(object):
    def __init__(self):
        self.enemies = []
        self.boss = None
        self.player = None

    def set_player(self, node):
        self.player= node

    def set_boss(self, node):
        self.boss= node

    def add_enemy(self, node):
        self.enemies.append(node)

    def draw(self, window):
        remove = []
        for e in self.enemies:
            if e.is_alive():
                bound = e.get_pos()[1]
                e.draw(window)
                if bound < window.height:
                    if bound + e.get_size()[1] > 0:
                        e.show()
                        if abs(e.get_pos()[0] - self.player.get_pos()[0]) < 15:
                            e.shoot()
                        node.handle_collision(self.player, e)
                else:
                    remove.append(e)
                e.update()
        for r in remove:
            if r in self.enemies:
                self.enemies.remove(r)
        self.player.draw(window)
        self.player.update()
