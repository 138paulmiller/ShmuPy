
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
    # load all images from img
    # load all images used
    graphics.images = graphics.image_loader.load_images("res/img/")
    # load root (player)
    level = scene.level.load('level0')

    # window keyboard callbacks
    def on_key_down(key):
        if key == ord('e'): ## DEBUGGING
            for helper in level.player.get_children():
                if helper.is_hidden():
                    helper.show()
                    helper.birth()
                    break  # only add one helper at a time

    def on_key_up(key):
        pass
    # set window callback
    main_window.set_on_key_down(on_key_down)
    main_window.set_on_key_up(on_key_up)

    while not main_window.is_quit():
        timedelta = graphics.clock.tick(60)
        main_window.clear((0, 10, 30))
        ## Debug zoom
        if main_window.is_key_down('z'):
            level.player.set_size((level.player.get_size()[0]+1, level.player.get_size()[1]+1))
        if main_window.is_key_down('x'):
            level.player.set_size((level.player.get_size()[0] - 1, level.player.get_size()[1] - 1))

        # get players dx dy and set based on keys down
        dx, dy = 0, 0
        if main_window.is_key_down('\r'):
            level.player.shoot()
        if main_window.is_key_down('a'):
            dx = -1
        if main_window.is_key_down('d'):
            dx = 1
        if main_window.is_key_down('w'):
            dy = -1
        if main_window.is_key_down('s'):
            dy = +1
        if level.player.get_is_bound():
            if level.player.get_pos()[0] + dx < 0 or level.player.get_pos()[0] + level.player.get_size()[0] + dx > main_window.width:
                dx = 0
            if level.player.get_pos()[1] + dy < 0 or level.player.get_pos()[1] + level.player.get_size()[1] + dy > main_window.height:
                dy = 0
        # appliy velocity
        level.player.set_velocity((dx * level.player.get_speed()[0], dy * level.player.get_speed()[1]))
        level.draw(main_window)
        # draw ui stuff
        graphics.draw_font(main_window.display, 'Health:{:3}'.format(level.player.get_health()),
                           graphics.font, graphics.font_color, (0, 0))
        i = 0
        for child in level.player.get_children():
            if child.is_alive() and not child.is_hidden():
                graphics.draw_font(main_window.display, 'Health:{:3}'.format(child.get_health()),
                                   graphics.font_small, graphics.font_color, (0, 24*i+32))
                i+=1


        if level.player.is_alive():
            # update velocity
            if level.player.get_velocity()[0] != 0:
                level.player.set_velocity((0, level.player.get_velocity()[1]))
            if level.player.get_velocity()[1] != 0:
                level.player.set_velocity((level.player.get_velocity()[0], 0))
            # update window
            main_window.update()
        else:
            run()
    main_window.close()





if __name__ == '__main__':
    run()
