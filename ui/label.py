import graphics


class Label(object):
    def __init__(self, text, (x, y), (w, h), font_size, border, font_color=(230, 100, 1), rect_color=(1, 100, 20)):
        self.text = text
        self.font = graphics.pygame.font.SysFont('monospace bold', font_size)
        self.border = border
        self.pos = [x, y]
        self.size = [w, h]
        self.font_color = font_color
        self.rect_color = rect_color
        self.on_click = None

    def draw(self, window):
        graphics.render_rect(window.display, (self.pos, self.size), self.rect_color, (0, 0))
        graphics.render_font(window.display, self.text, self.font, self.font_color,
                            (self.pos[0]+self.border, self.pos[1]+self.border))

    def is_point_in(self, (x, y)):
        if x > self.pos[0] and (x < self.pos[0] + self.size[0]):
            if y > self.pos[1] and (y < self.pos[1] + self.size[1]):
                return True
        return False

    def set_on_click(self, on_click_callback):
        self.on_click = on_click_callback

