
import graphics
import scene
import random
from copy import deepcopy


def run():
    """ShmuPy
      Python based Shoot Em Up Game Engine
      Copyright Paul Miller 2017"""
    # creates a window instance
    main_window = graphics.window.Window(580, 720)
    running = True
    # load all images from img
    graphics.images = graphics.image_loader.load_images("res/img/")
    root = scene.node.load("player.node")
    root.set_pos((main_window.width / 2, main_window.height / 2))

    for child in root.get_children():
        child.hide()
        child.kill()
        child.set_pos((root.get_pos()[0], root.get_pos()[1]))

    def on_enemy_collision(node, other):
            print "Explosion"

    enemies = []
    enemy = scene.node.load("enemy_skull.node")
    for i in range(500):
        enemies.append(deepcopy(enemy))
        enemies[-1].set_pos((random.randint(0, main_window.width), -100*random.randint(1,500)))
        enemies[-1].hide()
        enemies[-1].set_on_collision(on_enemy_collision)

    def on_player_collision(node, other):
        if node == root:
            print"Player:", node.get_health()
            node.set_animation("Player_Damage")
            if not node.is_alive():
                print "Game Over"
                run()

    def on_player_draw(window):
        """
        Called everytime player nodes draw is called
        :param window:
            Window the player in drawn on
        """
        # only move withing window bounds if bound
        dx, dy = root.get_velocity()
        if window.is_key_down('\r'):
            root.shoot()
        if window.is_key_down('a'):
            dx = -1
        if window.is_key_down('d'):
            dx = 1
        if window.is_key_down('w'):
            dy = -1
        if window.is_key_down('s'):
            dy = +1
        if root.get_is_bound():
            if root.get_pos()[0]+dx < 0 or root.get_pos()[0]+root.get_size()[0]+dx > window.width:
                dx = 0
            if root.get_pos()[1]+dy < 0 or root.get_pos()[1]+root.get_size()[1]+dy > window.height:
                dy = 0
        root.set_velocity((dx * root.get_speed()[0], dy * root.get_speed()[1]))

    def on_player_update():
        """
        Called everytime player nodes update is called
        """
        if root.get_velocity()[0] != 0:
            root.set_velocity((0, root.get_velocity()[1]))
        if root.get_velocity()[1] != 0:
            root.set_velocity((0, 0))

    root.set_on_collision(on_player_collision)
    root.set_on_draw(on_player_draw)
    root.set_on_update(on_player_update)




    def on_key_down(key):
        if key == ord('e'):
            for helper in root.get_children():
                if helper.is_hidden():
                    helper.show()
                    helper.birth()
                    break  # only add one helper at a time


    def on_key_up(key):
        pass

    main_window.set_on_key_down(on_key_down)
    main_window.set_on_key_up(on_key_up)
    while not main_window.is_quit():
        timedelta = graphics.clock.tick(60)

        main_window.clear((0, 10, 30))
        if main_window.is_key_down('q'):
            root.set_animation("Player_Damage")
        if main_window.is_key_down('z'):
            root.set_size((root.get_size()[0]+1, root.get_size()[1]+1))
        if main_window.is_key_down('x'):
            root.set_size((root.get_size()[0] - 1, root.get_size()[1] - 1))
        remove = []
        for e in enemies:
            if e.is_alive():
                e.draw(main_window)
                y = e.get_pos()[1]
                if y < main_window.height:
                    if y > 0:
                        e.show()
                        if abs(e.get_pos()[0]-root.get_pos()[0]) < 15:
                            e.shoot()
                        handle_collision(root, e)
                        handle_collision(e, root)
                    e.update()
                else:
                    remove.append(e)

        for e in remove:
            if e in enemies:
                enemies.remove(e)
        if root.is_alive():
            root.draw(main_window)
            root.update()  # update inputs
            main_window.update()
        else:
            run()
    main_window.close()


def handle_collision(node, other):
    if node.is_alive() and other.is_alive():
        if node.is_collidable() and other.is_collidable():
            # if collision between node and other
            if scene.node.is_collision(node, other):
                # take damage to both nodes
                node.health -= other.damage
                print node.get_id(), ":", node.get_health(), " hit ", other.get_id(), ":",other.get_health()
                # kill is no health
                if node.health <= 0:
                    node.kill()
                # if node has a callback call it
                if node.on_collision:
                    node.on_collision(node, other)
            # handle collision between other and node.bullets
            dead_bullets = []
            for bullet in node.get_bullets():
                if scene.node.is_collision(bullet, other):
                    # take damage to both nodes
                    other.health -= bullet.damage
                    bullet.health -= other.damage
                    if other.on_collision:
                        other.on_collision(other, bullet)
                    print bullet.get_id(), ":", bullet.get_health(), " hit ", other.get_id(), ":", other.get_health()
                    # kill is no health
                    if other.health <= 0:
                        other.kill()
                    if bullet.health <= 0:
                        bullet.kill()
                if not bullet.is_alive():
                    dead_bullets.append(bullet)
            for bullet in dead_bullets:
                node.get_bullets().remove(bullet)
            dead_bullets_other = []
            # handle collision between node and other.children
            for child_other in other.get_children():
                handle_collision(child_other, node)
                if not child_other.is_alive():
                    child_other.hide()
            # handle collision between node and other.bullets

    for child in node.get_children():
        handle_collision(child, other)

if __name__ == '__main__':
    run()
