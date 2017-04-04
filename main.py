
import graphics
import scene
import random
from copy import deepcopy


def run():
    """ShmuPy
      Python based Shoot Em Up Game Engine
      Copyright Paul Miller 2017"""
    # creates a window instance
    main_window = graphics.window.Window(580, 640)
    running = True
    # load all images from img
    graphics.images = graphics.image_loader.load_images("res/img/")
    world = []  # all nodes
    root = scene.node.load("player.node")
    root.set_pos((main_window.width / 2, main_window.height / 2))
    world.append(root)
    for child in root.get_children():
        child.hide()
        world.append(child)
        child.set_pos((root.get_pos()[0], root.get_pos()[1]))

    enemies = []
    for i in range(100):
        enemies.append(scene.node.load("enemy_skull.node"))
        enemies[-1].set_pos((random.randint(0, main_window.width), -100*random.randint(1,100)))
        enemies[-1].hide()
        world.append(enemies[-1])

    def on_player_draw(window):
        """
        Called everytime player nodes draw is called
        :param window:
            Window the player in drawn on
        """
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
        root.set_velocity((dx*root.get_speed()[0], dy*root.get_speed()[1]))



    def on_player_update():
        """
        Called everytime player nodes update is called
        """
        if root.get_velocity()[0] != 0:
            root.set_velocity((0, root.get_velocity()[1]))
        if root.get_velocity()[1] != 0:
            root.set_velocity((0, 0))



    root.set_on_draw(on_player_draw)
    root.set_on_update(on_player_update)




    def on_key_down(key):
        if key == ord('e'):
            for helper in root.get_children():
                if helper.is_hidden():
                    helper.show()
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
                y = e.get_pos()[1]+e.get_size()[1]
                if y < main_window.height:
                    if y > 0 :
                        e.show()
                        if abs(e.get_pos()[0]+ e.get_size()[0]/2-root.get_pos()[0]+root.get_size()[0]/2) < 15:
                            e.shoot()
                        if e.attack(root):
                            root.set_animation("Player_Damage")
                            if root.get_health() <= 0:
                                print "Game Over"
                                run()

                    e.update()
                else:
                    remove.append(e)
            else:
                remove.append(e)

            if root.attack(e):
                if e.get_health() <= 0:
                    e.kill()
        for e in remove:
            if e in enemies:
                enemies.remove(e)
        root.draw(main_window)
        root.update()  # update inputs
        main_window.update()
    main_window.close()


if __name__ == '__main__':
    run()
