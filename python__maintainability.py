import os

from numpy import average
from numpy.ma import median


def calculate_maintainability(root, log=True):
    _calls = {}
    _definitions = []
    _alllperc = []
    _errorcount = 0
    _pathcount = 0

    # Set up function definitions and funciton calls for each file
    for subdir, dirs, paths in os.walk(root):
        for path in paths:
            if not path.endswith('.py'):
                continue

            subdir = os.path.join(root, subdir)
            path = os.path.join(subdir, path)
            _pathcount += 1

            try:
                with open(path) as file:
                    pass
            except FileNotFoundError:
                _errorcount += 1
                _pathcount -= 1

            if log:
                print('FILE:', path)

    if log:
        print('-' * 50, end='\n\n')
        print('Tested %d files' % _pathcount)
        print('Failed %d files' % _errorcount)

    return 0


if __name__ == '__main__':
    calculate_maintainability('/home/svanderwoude/UvA/Thesis/repos/')
