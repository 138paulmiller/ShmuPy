import scene
import json
import os


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
                bound = e.get_pos()[1]
                if bound < window.height:
                    if bound + e.get_size()[1] > 0:
                        e.show()  # show enemy if in bounds
                        if self.player:
                            if e.is_alive() and abs(e.get_pos()[0] - self.player.get_pos()[0]) < 15:
                                e.shoot()
                            scene.node.handle_collision(self.player, e)
                else:
                    remove.append(e)
            e.draw(window)
        for r in remove:
            if r in self.enemies:
                self.enemies.remove(r)
        if self.player:
            if not self.pause:
                self.player.update()
            self.player.draw(window)


def load(level_file):
    l = None
    node_file = os.path.realpath('res/levels/{}.level'.format(level_file))
    # print "Loading:", node_file
    with open(node_file) as file:
        data = json.loads(file.read())
        l = Level()

        l.scroll = 'topdown'  # Default if scroll topdown set all enemies yvelocity to enemy speed
        if 'scroll' in data:
            l.scroll = data['scroll']
        if 'player' in data:
            player = scene.node_loader.load('players/{}.node'.format(data['player']))
            player.set_on_collision(scene.on_player_collision)
            pos = [500, 500]
            if 'startx' in data:
                pos[0] = data['startx']
            if 'starty' in data:
                pos[1] = data['starty']
            player.set_pos(pos)
            bullet = player.get_bullet_system().bullet()
            if l.scroll == 'sidescroll':
                bullet.set_velocity((bullet.get_speed()[0], 0))
            if l.scroll == 'topdown':
                bullet.set_velocity((0, -bullet.get_speed()[1]))
            for child in player.get_children():
                child.hide()
                child.kill()
                child.set_on_collision(scene.on_helper_collision)
                child.set_pos((player.get_pos()[0], player.get_pos()[1]))
                bullet = child.get_bullet_system().bullet()
                if l.scroll == 'sidescroll':
                    child.set_velocity((-child.get_speed()[0], 0))
                    bullet.set_velocity((bullet.get_speed()[0], 0))
                if l.scroll == 'topdown':
                    child.set_velocity((0, child.get_speed()[1]))
                    bullet.set_velocity((0, -bullet.get_speed()[1]))

            l.set_player(player)
        if 'enemies' in data:
            for enemy_data in data['enemies']:
                if 'id' in enemy_data:
                    enemy = scene.node_loader.load('enemies/{}.node'.format(enemy_data['id']))
                    enemy.set_on_collision(scene.on_enemy_collision)
                    enemy.birth()
                    enemy.hide()
                    pos = enemy.get_pos()
                    if 'x' in enemy_data:
                        pos[0] = enemy_data['x']
                    if 'y' in enemy_data:
                        pos[1] = enemy_data['y']
                    enemy.set_pos(pos)
                    vel = [0, 0]
                    bullet = enemy.get_bullet_system().bullet()
                    if l.scroll == 'sidescroll':
                        vel[0] = -enemy.get_speed()[0]
                        bullet.set_velocity((-bullet.get_speed()[0], 0))
                    elif l.scroll == 'topdown':
                        vel[1] = enemy.get_speed()[1]
                        bullet.set_velocity((0, bullet.get_speed()[1]))
                    enemy.set_velocity(vel)
                    l.add_enemy(enemy)
                else:
                    print level_file, ":Enemy ID Missing"
    return l

