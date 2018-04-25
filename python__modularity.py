import ast
import os

from numpy import average
from numpy.ma import median


def calls(abstree):
    return [node.func.id for node in ast.walk(abstree)
            if type(node) is ast.Call and type(node.func) is ast.Name]


def create_or_update(_calls, call, path):
    call += '_' + path

    if call in _calls:
        _calls[call] += 1
    else:
        _calls.update({call: 1})


def definitions(abstree):
    return [node.name for node in ast.walk(abstree) if type(node) is ast.FunctionDef]


def intersection(lst1, lst2):
    return [value for value in lst1 if value in lst2]


def calculate_modularity(root, log=True):
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
                    data = file.read()

                    try:
                        abstree = ast.parse(data)
                    except SyntaxError:
                        _errorcount += 1
                        _pathcount -= 1
                        continue

                    for call in calls(abstree):
                        # Exclude defaults (only print for now)
                        if call != 'print':
                            create_or_update(_calls, call, path)
                    
                    for definition in definitions(abstree):
                        _definitions.append(definition + '_' + path)
            except FileNotFoundError:
                _errorcount += 1
                _pathcount -= 1

    
    # Calculate modularity for each file
    for subdir, dirs, paths in os.walk(root):
        for path in paths:
            if not path.endswith('.py'):
                continue

            subdir = os.path.join(root, subdir)
            path = os.path.join(subdir, path)
            fcalls = [c for c in _calls if c.endswith(path)]
            fdefs = [d for d in _definitions if d.endswith(path)]

            local = intersection(fcalls, fdefs)
            all_count = 0
            local_count = 0

            # Get local function call count
            for call in local:
                local_count += _calls[call]
                all_count += _calls[call]
                fcalls.remove(call)

            # Get all leftover function calls
            for call in fcalls:
                all_count += _calls[call]

            # Modularity percentage
            perc = 1

            if all_count > 0:
                perc = local_count / all_count

            _alllperc.append(perc)

            if log:
                print('FILE:', path)
                print('Local call count:', local_count)
                print('Total call count:', all_count)
                print('Modularity percentage:', perc * 100, end='\n\n')

    if log:
        print('-' * 50, end='\n\n')
        print('Tested %d files' % _pathcount)
        print('Failed %d files' % _errorcount)
        print('Overall modularity (avg):', average(_alllperc) * 100)
        print('Overall modularity (med):', median(_alllperc) * 100)
        print('Overall modularity (min):', min(_alllperc) * 100)
        print('Overall modularity (max):', max(_alllperc) * 100)

    return average(_alllperc), median(_alllperc), min(_alllperc), max(_alllperc)


if __name__ == '__main__':
    calculate_modularity('/home/svanderwoude/UvA/Thesis/repos/')
