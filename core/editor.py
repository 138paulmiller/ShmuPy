import scene
import graphics

def run():
    main_window = graphics.window.Window(580, 720)

    def on_mouse_button_down(button):
        print "Button Down ", button
    main_window.set_mouse_button_down(on_mouse_button_down)

    while not main_window.is_quit():
        main_window.clear((0, 10, 30))
        main_window.update()
