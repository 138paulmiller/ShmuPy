import editor
import graphics


def run(level_file=None):

    main_window = graphics.window.Window(580, 720)
    graphics.images = graphics.image_loader.load_images("res/img/")

    main_editor = editor.Editor()

    main_window.set_on_key_down(main_editor.on_key_down)
    main_window.set_mouse_button_down(main_editor.on_mouse_button_down)

    while not main_window.is_quit():
        timedelta = graphics.clock.tick(60)
        main_window.clear((0, 10, 30))

        if main_window.is_key_down(graphics.KEY_LEFT) or \
            main_window.is_key_down('a'):
            main_editor.offset[0] -= 1

        if main_window.is_key_down(graphics.KEY_RIGHT)or \
            main_window.is_key_down('d'):
            main_editor.offset[0] += 1

        if main_window.is_key_down(graphics.KEY_UP)or \
            main_window.is_key_down('w'):
            main_editor.offset[1] -= 1

        if main_window.is_key_down(graphics.KEY_DOWN)or \
            main_window.is_key_down('s'):
            main_editor.offset[1] += 1
        main_editor.draw(main_window)
        main_window.update()
