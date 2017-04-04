from copy import deepcopy
import os
import json
import scene
import graphics


class BulletSystem(object):
    def __init__(self, source_bullet, rate, max=10):
        self.max = max
        self.rate = rate
        self.bullets = []
        self.source_bullet = source_bullet
        self.count = 0

    def get_bullets(self):
        return self.bullets

    def shoot(self, pos):
        self.count += self.rate
        if self.count > 1:
            if len(self.bullets) < self.max:
                self.bullets.append(deepcopy(self.source_bullet))
                self.bullets[-1].set_pos((pos[0] - self.source_bullet.get_size()[0] / 2,
                                          pos[1] - self.source_bullet.get_size()[1] / 2))
                self.count = 0

    def draw(self, window):
        remove = []
        for b in self.bullets:
            if (b.get_pos()[1] > 0) and (b.get_pos()[1] < window.height):
                b.draw(window)
            else:
                remove.append(b)
        for r in remove:
            self.bullets.remove(r)

    def update(self):
        # updates
        for b in self.bullets:
            b.update()


def load(bullet_file):
    bullet_system = BulletSystem(None, 0)
    bullet_file = os.path.realpath('res/nodes/{}'.format(bullet_file))
    #print "Loading:", bullet_file
    with open(bullet_file) as file:
        data = json.loads(file.read())
        if 'id' in data:
            bullet = scene.node.Node(data['id'].lower())
            if 'width' in data and 'height' in data:
                bullet.set_size((data['width'], data['height']))
                if 'speed' in data:
                    speed = data['speed']
                    bullet.set_speed((0,speed))
                    bullet.set_velocity((0,speed))
                    # parse animations
                    if 'animation' in data:
                        for anim_data in data['animation']:
                            imgs = []
                            seq = []
                            speed = 1
                            for img_file in anim_data['images']:
                                seq.append(len(imgs))
                                imgs.append(graphics.images[img_file])
                            loop = anim_data['loop'].lower() in ('true', '1', 'yes')
                            if 'speed' in anim_data:
                                speed = anim_data['speed']
                            if 'id' in anim_data:
                                anim_id = anim_data['id']
                                bullet.add_animation(anim_id, graphics.animation.Animation(imgs, seq, speed, loop))
                            else:
                                bullet.get_id(), ":Child Missing Id!!!"
                        if 'default' in data:
                            bullet.set_animation(data['default'].lower())
                        else:
                            print bullet.get_id(), ":Missing Default Animation!!!"
                if 'bound' in data:
                    bullet.set_is_bound(data['bound'].lower() in ('true', '1', 'yes'))
                if 'health' in data:
                    bullet.set_health(data['health'])
                if 'damage' in data:
                    bullet.set_damage(data['damage'])
                bullet_system.source_bullet = bullet
                if 'rate' in data:
                    bullet_system.rate = data['rate']
                if 'max' in data:
                    bullet_system.max = data['max']
            else:
                print bullet.get_id(), ":Missing size(x and y)!!!"
        else:
            print ":Missing ID!!!"

    return bullet_system