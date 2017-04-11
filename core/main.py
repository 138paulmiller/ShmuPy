import sys

import core

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-e':
        core.editor.run()
    else:
        core.game.run()
