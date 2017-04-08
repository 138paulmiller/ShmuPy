import graphics
import json
import os
import scene
from copy import deepcopy


class Node(graphics.sprite.Sprite):
    """
    Node
        The sprites that are loaded into a scene and continuously rendered
        until they are paused or deleted.
        Act as the fundamental drawing blocks for each individual sprite, and
        can be loaded from the node files in res/nodes/.
        Each file defines a node. These files use JSON
        syntax to set the nodes attributes.
    """
    def __init__(self, unique_id, parent=None):
        """
        :param unique_id:
            id of nodes sprite, changed to lowercase by default
        :param parent:
            parent of node to create
        """
        super(Node, self).__init__(unique_id.lower())
        self.bullet_system = None
        self.parent = parent
        self.children = {}
        self.is_duplicate = None
        self.collidable = False
        self.on_collision = None
        self.follow = False  # follow parent or not
        self.follow_dist = [0, 0]
        self.is_bullet = False

    def __deepcopy__(self, memo={}):
        sprite = super(Node, self).__deepcopy__(memo)
        node = Node(sprite.get_id())
        node.pos = sprite.pos
        node.size = sprite.size
        node.flip = sprite.flip
        node.velocity = sprite.velocity
        node.health = sprite.health
        node.damage = sprite.damage
        node.speed = sprite.speed
        node.on_update = sprite.on_update
        node.on_draw = sprite.on_draw
        for key in self.animations.iterkeys():
            node.animations[key] = deepcopy(sprite.animations[key])
        node.current_animation = sprite.current_animation  # id to current animation
        node.set_animation(sprite.current_animation)
        node.prev_animation = sprite.prev_animation  # id to prev animation
        node.is_bound = sprite.is_bound
        node.parent = self.parent
        for key in self.children.iterkeys():
            node.children[key] = self.children[key]
        node.is_duplicate = self.is_duplicate
        node.follow = self.follow
        node.follow_dist = self.follow_dist
        node.collidable = self.collidable
        node.on_collision = self.on_collision
        node.bullet_system = deepcopy(self.bullet_system)
        node.is_bullet = self.is_bullet
        memo[self] = node
        return node

    def set_is_duplicate(self, is_duplicate):
        self.is_duplicate = is_duplicate

    def set_on_collision(self, collision_callback):
        self.on_collision = collision_callback

    def set_collidable(self, collide):
        self.collidable = collide

    def is_collidable(self):
        return self.collidable

    def get_is_duplicate(self):
        return self.is_duplicate

    def add_child(self, node):
        """
        Adds the node as a child to self and self is then parent to child
        :param node:
            node to add to children
        """
        if node:
            if node.get_id() not in self.children:
                node.set_parent(self)
                self.children[node.get_id()] = node
            else:
                print "Node: ", node.get_id(), " already exists"

    def get_child(self, node_id):
        """
        Adds the node as a child to self and self is then parent to child
        :param node_id:
            id of node to return
        """
        node_id = node_id.lower()
        if node_id in self.children:
            return self.children[node_id]
        return None

    def get_children(self):
        """
        Get an array of children Nodes
        :return:
            Children nodes
        """
        return self.children.values()

    def get_parent(self):
        """
        :return:
            Nodes parent
        """
        return self.parent

    def set_parent(self, parent_node):
        self.parent = parent_node

    def set_follow(self, follow):
        self.follow = follow

    def get_follow(self):
        return self.follow

    def set_follow_dist(self, (dx, dy)):
        self.follow_dist[0] = dx
        self.follow_dist[1] = dy

    def shoot(self):
        if self.bullet_system:
            pos = (self.get_pos()[0]+self.get_size()[0]/2, self.get_pos()[1]+self.get_size()[1]/2)
            self.bullet_system.shoot(pos)
            for child in self.children.values():
                if not child.is_hidden():
                    child.shoot()

    def get_bullets(self):
        if self.bullet_system:
            return self.bullet_system.get_bullets()
        return []

    def update(self):
        super(Node, self).update()
        if self.bullet_system:
            self.bullet_system.update()
        for child in self.get_children():
            dx = 0
            dy = 0
            if child.get_follow():
                if child.get_pos()[0] - self.pos[0] < -child.follow_dist[0]:
                    dx = 1
                elif child.get_pos()[0] - self.pos[0] > child.follow_dist[0]:
                    dx = -1
                if child.get_pos()[1] - self.pos[1] < -child.follow_dist[1]:
                    dy = 1
                elif child.get_pos()[1] - self.pos[1] > child.follow_dist[1]:
                    dy = -1
                child.set_velocity((dx * child.get_speed()[0], dy * child.get_speed()[1]))
            child.update()

    def draw(self, window):
        super(Node, self).draw(window)
        if self.bullet_system:
            self.bullet_system.draw(window)
        for child in self.children.values():
                child.draw(window)


def is_collision(node, other):
    return is_collision_rect(node.get_rect(), other.get_rect())


def is_collision_rect(node_rect, other_rect):
    collide = False
    if (node_rect[0][0] < other_rect[0][0] + other_rect[1][0]) and (
                    node_rect[0][0] + node_rect[1][0] > other_rect[0][0]):
        if (node_rect[0][1] < other_rect[0][1] + other_rect[1][1]) and (
                        node_rect[0][1] + node_rect[1][1] > other_rect[0][1]):
            collide = True
    return collide


def load(node_file):
    """
    Creates a new Node instance along with its children with the defined attributes
    parsed as JSON from node_file.
    The Id's of the children should match the name of the node file. (child_id.node)
     This allows for all the children to be loaded into the parent node.
    :param node_file:
        JSON Node file in /res/nodes/ directory.
    :return:
        Created Node with the node_file attributes.
    """
    node_file = os.path.realpath('res/nodes/{}'.format(node_file))
    #print "Loading:", node_file
    node = None
    with open(node_file) as file:
        data = json.loads(file.read())
        if 'id' in data:
            node = Node(data['id'].lower())
        else:
            print node.get_id(), ":Missing ID!!!"
        if 'width' in data and 'height' in data:
            node.set_size((data['width'], data['height']))
        else:
            print node.get_id(), ":Missing size(x and y)!!!"
        if 'x' in data and 'y' in data:
            node.set_pos((data['x'], data['y']))
        if 'xspeed' in data and 'yspeed' in data:
            node.set_speed((data['xspeed'], data['yspeed']))
        if 'xflip' in data and 'yflip' in data:
            node.set_flip((data['xflip'], data['yflip']))
        if 'xvelocity' in data and 'yvelocity' in data:
            node.set_velocity((data['xvelocity'], data['yvelocity']))
        if 'bullet_system' in data:
            node.bullet_system = scene.bullet_system.load('{}.bullet'.format(data['bullet_system']))
        if 'bound' in data:
            node.set_is_bound(data['bound'].lower() in ('true', '1', 'yes'))
        if 'health' in data:
            node.set_health(data['health'])
            node.set_start_health(node.get_health())

        if 'damage' in data:
            node.set_damage(data['damage'])
        if 'collide' in data:
            node.set_collidable(data['collide'].lower() in ('true', '1', 'yes'))
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
                    node.add_animation(anim_id, graphics.animation.Animation(imgs, seq, speed, loop))
                else:
                    node.get_id(), ":Child Missing Id!!!"
            if 'default' in data:
                node.set_animation(data['default'].lower())
            else:
                print node.get_id(), ":Missing Default Animation!!!"

        else:
            print node.get_id(),":Missing Animation!!!"
        if 'children' in data:
            for child_data in data['children']:
                if 'id' in child_data:
                    child_id = child_data['id']
                    if 'file_id' in child_data:
                        child = load('{}.node'.format(child_data['file_id'].lower()))
                        child.set_id(child_id)
                        node.add_child(child)
                        if 'follow' in child_data:
                            follow = child_data['follow'].lower() in ('true', '1', 'yes')
                            child.set_follow(follow)
                            follow_dist = [0, 0]
                            if 'follow_dist' in child_data:
                                follow_dist = child_data['follow_dist']
                            child.set_follow_dist((follow_dist[0], follow_dist[1]))
                else:
                    print node.get_id(), ":Child Missing Id!!!"

    return node


def handle_collision(node, other):
    # handles node collisions by applying damage to node and or other
    # and making callback on collision between two nodes

    if node.is_alive() and other.is_alive():
        if node.is_collidable() and not node.is_hidden() and other.is_collidable() and not other.is_hidden():
            # if collision between node and other
            if scene.node.is_collision(node, other):
                print node.get_id(),":",other.get_health(), "--", other.get_id(),":", other.get_health()
                # take damage to both nodes
                node.health -= other.damage
                other.health -= node.damage
                # kill is no health
                if node.health <= 0:
                    node.kill()
                if other.health <= 0:
                    other.kill()
                # if node has a callback call it
                if node.on_collision:
                    node.on_collision(node, other)
                if other.on_collision:
                    other.on_collision(other, node)
    # handle collision between other and node.bullets
    dead_bullets = []
    for bullet in node.get_bullets():
        if not other.is_bullet:
            handle_collision(bullet, other)
        if not bullet.is_alive():
            dead_bullets.append(bullet)
    for bullet in dead_bullets:
        node.get_bullets().remove(bullet)
    dead_bullets_other = []
    # handle collision between node and other.bullets
    for other_bullet in other.get_bullets():
        if not node.is_bullet:
            handle_collision(other_bullet, node)
        if not other_bullet.is_alive():
            dead_bullets_other.append(other_bullet)
    for other_bullet in dead_bullets_other:
        other.get_bullets().remove(other_bullet)
    # handle collision between node and other.children
    for child_other in other.get_children():
        handle_collision(node, child_other)
    for child in node.get_children():
        handle_collision(child, other)