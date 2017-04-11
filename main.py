import sys
import game
import editor

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-e':
        editor.run()
    else:
        game.run()
