import node
import bullet_system
import level



def on_player_collision(node, other):
    print"Player:", node.get_health()
    node.set_animation("acqua_damage")



def on_enemy_collision(node, other):
    print "Explosion"


def on_helper_collision(helper, other):
    helper.set_animation("pieret_damage")
    if helper.get_health() < 0:
        helper.hide()
        helper.set_health(helper.start_health)

