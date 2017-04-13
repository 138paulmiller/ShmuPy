import ui


class Menu(object):

    def __init__(self, font_color, rect_color, highlight_color, (w, h), font_size=1, border=5):
        self.labels = {}
        self.font_color = font_color
        self.highlight_color = highlight_color
        self.size = [w, h]
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

    def set_pos(self, (x, y)):
        self.pos[0] = x
        self.pos[1]= y

    def click(self):
        if self.selected and self.selected.on_click:
            self.selected.on_click(self.selected)

    def add_label(self, id, text, click_callback=None):
        offset_y = len(self.labels)*self.size[1]
        label = ui.label.Label(text,
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

