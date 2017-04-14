import sys
import pygame
import graphics


class Window(object):
    """
    Window:
        Acts as a display interface and display event handler.


    """
    def __init__(self, width=540, height=680):
        self.key_states = {}
        self.mouse_button_states = [0, 0, 0, 0, 0]
        self.width = width
        self.height = height
        self.display = graphics.get_display((width, height))
        self.quit = False
        self.mouse_pos = (0, 0)
        self.mouse_pos_prev = (0, 0)
        self.on_key_up = None
        self.on_key_down = None
        self.on_mouse_move = None
        self.on_mouse_button_down = None

    def is_key_down(self, key):
        try:
            key = ord(key)
        except:
            pass
        if key in self.key_states:
            return self.key_states[key]
        return False

    def is_mouse_button_down(self, button_id):
        if button_id < len(self.mouse_button_states):
            return self.mouse_button_states[button_id]

    def get_mouse_pos(self):
        return self.mouse_pos

    def get_mouse_dif(self):
        return (self.mouse_pos[0] - self.mouse_pos_prev[0],
                self.mouse_pos[1] - self.mouse_pos_prev[1])

    def set_on_key_up(self, callback_func):
        self.on_key_up = callback_func

    def set_on_key_down(self, callback_func):
        self.on_key_down = callback_func

    def set_on_mouse_move(self, callback_func):
        self.on_mouse_move = callback_func

    def set_mouse_button_down(self, callback_func):
        self.on_mouse_button_down = callback_func

    def clear(self, color):
        self.display.fill(color)

    def update(self):
        # poll events
        self.mouse_pos_prev = self.mouse_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.KEYDOWN:
                key = event.key
                self.key_states[key] = True
                if self.on_key_down:
                    self.on_key_down(key)
            elif event.type == pygame.KEYUP:
                key = event.key
                self.key_states[key] = False
                if self.on_key_up:
                    self.on_key_up(key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print event.button
                self.mouse_button_states[event.button - 1] = True
                if self.on_mouse_button_down:
                    self.on_mouse_button_down(event.button - 1)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_button_states[event.button-1] = False
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                if self.on_mouse_move:
                    self.on_mouse_move(self.mouse_pos)

        graphics.update()

    def is_quit(self):
        return self.quit

    def close(self):
        self.display = None
        pygame.quit()
        sys.exit(0)
