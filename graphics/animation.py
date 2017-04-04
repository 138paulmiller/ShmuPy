import graphics
import pdb


class Animation(object):
    def __init__(self, images=[], sequence=[], speed=0, loop=True):
        self.images = images
        self.sequence = sequence
        self.speed = speed
        self.loop = loop
        self.pause = True
        self.done = True
        self.current_i = 0
        self.step = 0

    def __deepcopy__(self, memodict={}):
        animation = Animation()
        animation.images = []
        for img in self.images:
            animation.images.append(img.copy())
        animation.speed = self.speed
        animation.sequence = self.sequence
        animation.loop = self.loop
        return animation

    def start(self):
        self.pause = False
        self.done = False

    def stop(self):
        self.pause = True
        self.done = True
        self.current_i = 0
        self.step = 0

    def is_done(self):
        return self.done

    def set_loop(self, loop):
        self.loop = loop

    def get_loop(self):
        return self.loop

    def update(self):
        if not self.pause:
            self.step += self.speed
            if self.step > 1:
                self.step = 0
                self.current_i += 1
                if self.loop:
                    self.current_i %= len(self.sequence)
                elif self.current_i >= len(self.sequence):
                    self.done = True
                    self.current_i = 0

    def draw(self, display, (pos, size), flip=(0, 0)):
        img_i = self.sequence[self.current_i]
        if img_i < len(self.images):
            img = graphics.flip_image(self.images[img_i], flip)
            graphics.render_img(display, img, (pos, size))

