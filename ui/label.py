import graphics

class Label(object):
    def __init__(self, text, (x,y),(w,h), font_size, border, font_color=(230, 100, 1), rect_color=(1, 100, 20)):
        self.text = text
        self.font = font = graphics.pygame.font.SysFont('monospace bold', font_size)
        self.border = border
        self.pos = [x, y]
        self.size = [w, h]
        self.font_color = font_color
        self.rect_color = rect_color

    def draw(self, window):
        graphics.render_rect(window.display, (self.pos, self.size), self.rect_color, (0, 0))
        graphics.render_font(window.display, self.text, self.font, self.font_color,
                           (self.pos[0]+self.border, self.pos[1]+self.border))
