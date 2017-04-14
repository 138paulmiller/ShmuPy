import level
import scene
import json
import os


def load(level_file):
    l = None
    node_file = os.path.realpath('res/levels/{}.level'.format(level_file))
    # print "Loading:", node_file
    with open(node_file) as file:
        data = json.loads(file.read())
        l = level.Level()
        if 'scroll' in data:
            l.scroll = data['scroll'].lower()
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
            if l.scroll == level.SIDESCROLL:
                bullet.set_velocity((bullet.get_speed()[0], 0))
                l.set_scroll(level.SIDESCROLL)
            if l.scroll == level.TOPDOWN:
                l.set_scroll(level.TOPDOWN)
                bullet.set_velocity((0, -bullet.get_speed()[1]))
            for child in player.get_children():
                child.hide()
                child.kill()
                child.set_on_collision(scene.on_helper_collision)
                child.set_pos((player.get_pos()[0], player.get_pos()[1]))
                bullet = child.get_bullet_system().bullet()
                if l.scroll == level.SIDESCROLL:
                    child.set_velocity((-child.get_speed()[0], 0))
                    bullet.set_velocity((bullet.get_speed()[0], 0))
                if l.scroll == level.TOPDOWN:
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
                    if l.scroll == level.SIDESCROLL:
                        vel[0] = -enemy.get_speed()[0]
                        bullet.set_velocity((-bullet.get_speed()[0], 0))
                    elif l.scroll == level.TOPDOWN:
                        vel[1] = enemy.get_speed()[1]
                        bullet.set_velocity((0, bullet.get_speed()[1]))
                    print "VELOCITY", l.scroll
                    enemy.set_velocity(vel)
                    l.add_enemy(enemy)
                else:
                    print level_file, ":Enemy ID Missing"
    return l

