import scene
import graphics
import json
import os

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
            node = scene.node.Node(data['id'].lower())
        else:
            print node.get_id(), ":Missing ID!!!"
        if 'width' in data and 'height' in data:
            node.set_size((data['width'], data['height']))
        else:
            print node.get_id(), ":Missing size(x and y)!!!"
        if 'x' in data and 'y' in data:
            node.set_pos((data['x'], data['y']))
        if 'xspeed' in data:
            node.speed[0] = data['xspeed']
        if 'yspeed' in data:
            node.speed[1] = data['yspeed']
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
                        bs = '/'
                        if os.name == 'nt':
                            bs = '\\'
                        path = node_file[0:node_file.rfind(bs)]
                        parent_dir = ''
                        if path.rfind(bs) >= 0:
                            parent_dir = path[path.rfind(bs):]
                        child = load('{}/{}.node'.format(parent_dir, child_data['file_id'].lower()))
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
