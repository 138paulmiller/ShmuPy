import graphics 

class Label(object):
    def __init__(self, text, pos, size, font_size, border, font_color=(230, 100, 1), rect_color=(1, 100, 20)):
        self.text = text
        self.font = graphics.pygame.font.SysFont('monospace bold', font_size)
        self.border = border
        self.pos = [pos[0], pos[1]]
        self.size = [size[0], size[1]]
        self.font_color = font_color
        self.rect_color = rect_color
        self.on_click = None

    def draw(self, window):
        graphics.render_rect(window.display, (self.pos, self.size), self.rect_color, (0, 0))
        graphics.render_font(window.display, self.text, self.font, self.font_color,
                            (self.pos[0]+self.border, self.pos[1]+self.border))

    def is_point_in(self, pos):
        x,y = pos
        if x > self.pos[0] and (x < self.pos[0] + self.size[0]):
            if y > self.pos[1] and (y < self.pos[1] + self.size[1]):
                return True
        return False

    def set_on_click(self, on_click_callback):
        self.on_click = on_click_callback


class Menu(object):

    def __init__(self, font_color, rect_color, highlight_color, size, font_size=1, border=5):
        
        self.labels = {}

        self.font_color = font_color
        self.highlight_color = highlight_color
        self.size = [size[0], size[1]]
        self.rect_color = rect_color
        self.pos = [0, 0]
        self.is_hidden = True
        self.border = border
        self.font_size = font_size
        self.selected = None
        self.sticky = False   # highlight selected

    def open(self):
        self.is_hidden = False

    def hide(self):
        self.is_hidden = True

    def toggle_sticky(self):
        self.sticky = not self.sticky

    def is_open(self):
        return self.is_hidden

    def set_pos(self, pos):
        self.pos[0] = pos[0]
        self.pos[1]= pos[1]

    def click(self):
        if self.selected and self.selected.on_click:
            self.selected.on_click(self.selected)

    def add_label(self, id, text, click_callback=None):
        offset_y = len(self.labels)*self.size[1]
        label = Label(text,
                              (self.pos[0], self.pos[1]+offset_y),
                              self.size,
                              self.font_size,
                              self.border,
                              self.font_color,
                              self.rect_color)
        label.set_on_click(click_callback)
        self.labels[id] = label

    def get_label(self, id):
        if id in self.labels:
            return self.labels[id]
        return None

    def draw(self, window):
        self.selected = None
        if not self.is_hidden:
            i = 0
            for label in self.labels.values():
                label.pos = (self.pos[0], self.pos[1]+i * self.size[1])
                i+=1
                if label.is_point_in(window.get_mouse_pos()):
                    self.selected = label
                else:
                    label.rect_color = self.rect_color
                label.draw(window)
            if not self.sticky and self.selected:
                self.selected.rect_color = self.highlight_color
                self.selected.draw(window)

