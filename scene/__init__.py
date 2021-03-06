from scene import bullet_system
from scene import node
from scene import node_loader
from scene import level
from scene import level_loader


def on_player_collision(node, other):
    print("Player:", node.get_health())
    node.set_animation("damage")


def on_enemy_collision(node, other):
    node.set_animation("damage")
    if not node.alive:
        node.set_animation("death")


def on_helper_collision(helper, other):
    helper.set_animation("damage")
    if helper.get_health() < 0:
        helper.hide()
        helper.set_health(helper.start_health)

