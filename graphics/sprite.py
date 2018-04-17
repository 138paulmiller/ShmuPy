from copy import deepcopy


class Sprite(object):
    def __init__(self, unique_id):
        self.unique_id = unique_id
        self.pos = [0, 0]
        self.size = [0, 0]
        self.flip = [0, 0]
        self.velocity = [0, 0]
        self.health = 100
        self.start_health = 100
        self.damage =  100
        self.speed = [0, 0]
        self.animations = {}
        self.current_animation = None # id to current animation
        self.prev_animation = None    # id to prev animation
        self.is_bound = False
        self.on_update = None
        self.on_draw = None
        self.hidden = False
        self.alive = True
        self.translate = [0,0]


    def __deepcopy__(self, memo={}):
        sprite = Sprite(self.unique_id)
        sprite.pos = deepcopy(self.pos)
        sprite.size = deepcopy(self.size)
        sprite.flip = deepcopy(self.flip)
        sprite.start_health = self.start_health
        sprite.velocity = deepcopy(self.velocity)
        sprite.health = self.health
        sprite.damage =  self.damage
        sprite.speed = deepcopy(self.speed)
        sprite.on_update = self.on_update
        sprite.on_draw = self.on_draw
        for key in self.animations.keys():
            sprite.animations[key] = deepcopy(self.animations[key])
        sprite.current_animation = self.current_animation # id to current animation
        sprite.set_animation(sprite.current_animation)
        sprite.prev_animation = self.prev_animation # id to prev animation
        sprite.is_bound = self.is_bound
        sprite.alive = self.alive
        sprite.translate = deepcopy(self.translate)
        memo[self] = sprite
        return sprite

    def get_health(self):
        return self.health

    def set_health(self, health):
        self.health = health

    def set_start_health(self, health):
        self.start_health = health

    def kill(self):
        self.alive = False

    def birth(self):
        self.alive = True

    def is_alive(self):
        return self.alive

    def get_damage(self):
        return self.damage

    def set_damage(self, damage):
        self.damage = damage

    def get_is_bound(self):
        return self.is_bound

    def set_is_bound(self, is_bound):
        self.is_bound = is_bound

    def update(self):
        if self.on_update:
            self.on_update()
        self.move_by(self.velocity)
        if self.current_animation:
            if self.animations[self.current_animation].is_done():
                if self.current_animation != 'death' and self.prev_animation:
                    self.set_animation(self.prev_animation)
            else:
                self.animations[self.current_animation].update()

    def draw(self, window):
        if self.on_draw:
            self.on_draw(window)
        if self.current_animation and not self.hidden and self.alive:
            self.animations[self.current_animation].draw(window.display, (self.pos, self.size), self.flip, self.translate)

    def add_animation(self, unique_id, animation):
        unique_id = unique_id.lower()
        self.animations[unique_id] = animation

    def get_animation(self, unique_id):
        unique_id = unique_id.lower()
        if unique_id in self.animations:
            return self.animations[unique_id]

    def set_animation(self, unique_id):
        unique_id = unique_id.lower()
        if unique_id in self.animations:
            # stop old animation and assign to prev
            if self.current_animation and self.current_animation != unique_id:
                self.animations[self.current_animation].stop()
                self.prev_animation = self.current_animation
            self.current_animation = unique_id
            animation = self.animations[self.current_animation]
            animation.start()  # start new

    def move_by(self, pos):
        x,y = pos
        self.pos[0] += x
        self.pos[1] += y

    def accelerate_by(self, pos):
        x,y = pos
        
        if abs(self.velocity[0]+x):
            self.velocity[0] += x
        if abs(self.velocity[1]+y):
            self.velocity[1] += y

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, pos):
        x,y = pos
        
        self.velocity[0] = x
        self.velocity[1] = y

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        x,y = pos
        
        self.pos[0] = x
        self.pos[1] = y

    def set_translate(self, pos):
        x,y = pos
        
        self.translate[0] = x
        self.translate[1] = y

    def get_size(self):
        return self.size

    def set_size(self, size):
        w,h = size
        
        if w > 0 and h > 0:
            self.size[0] = w
            self.size[1] = h

    def get_id(self):
        return self.unique_id

    def set_id(self, unique_id):
        self.unique_id = unique_id

    def get_speed(self):
        return self.speed

    def set_speed(self, speed):
        self.speed[0] = speed[0]
        self.speed[1] = speed[1]

    def get_speed(self):
        return self.speed

    def set_flip(self, flip):
        self.flip[0] = flip[0]
        self.flip[1] = flip[1]

    def get_flip(self):
        return self.flip

    def set_rect(self, rect):
        self.pos = rect[0]
        self.size = rect[1]

    def get_rect(self):
        return self.pos, self.size

    def get_id(self):
        return self.unique_id

    def set_on_update(self, callback_func):
        self.on_update = callback_func

    def set_on_draw(self, callback_func):
        self.on_draw = callback_func

    def is_hidden(self):
        return self.hidden

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def is_within(self, rect):
        x,y,w,h = rect
        pos = self.get_pos()
        size = self.get_size()
        if pos[0]+size[0] > x and pos[0] < x + w:
            if pos[1] + size[1] > y and pos[1] < y + h:
                return True

