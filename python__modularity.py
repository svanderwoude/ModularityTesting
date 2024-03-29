import ast
import os

from numpy import average
from numpy.ma import median

from python__libraryfunctions import res


builtin_functions = [
    'abs', 'dict', 'help', 'min', 'setattr',
    'all', 'dir', 'hex', 'next', 'slice',
    'any', 'divmod', 'id', 'object', 'sorted',
    'ascii', 'enumerate', 'input', 'oct', 'staticmethod',
    'bin', 'eval', 'int', 'open', 'str',
    'bool', 'exec', 'isinstance', 'ord', 'sum',
    'bytearray', 'filter', 'issubclass', 'pow', 'super',
    'bytes', 'float', 'iter', 'print', 'tuple',
    'callable', 'format', 'len', 'property', 'type',
    'chr', 'frozenset', 'list', 'range', 'vars',
    'classmethod', 'getattr', 'locals', 'repr', 'zip',
    'compile', 'globals', 'map', 'reversed', '__import__',
    'complex', 'hasattr', 'max', 'round',
    'delattr', 'hash', 'memoryview', 'set',
    'int', 'float', 'bool', 'str', 'self', 'exit',
] + res


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


def calculate_modularity(files, log=True):
    _calls = {}
    _definitions = []
    _alllperc = []
    _errorcount = 0

    # Set up function definitions and funciton calls for each file
    for subdir in files:
        for path in subdir:
            with open(path) as file:
                data = file.read()

                try:
                    abstree = ast.parse(data)
                except SyntaxError:
                    _errorcount += 1

                    continue

                for call in calls(abstree):
                    # Exclude built-in functions
                    if(not call in builtin_functions and
                       not call.endswith('Error')):
                        create_or_update(_calls, call, path)
                
                for definition in definitions(abstree):
                    _definitions.append(definition + '_' + path)

    
    # Calculate modularity for each file
    for subdir in files:
        for path in subdir:
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
        print('Overall modularity (avg):', average(_alllperc) * 100)
        print('Overall modularity (med):', median(_alllperc) * 100)
        print('Overall modularity (min):', min(_alllperc) * 100)
        print('Overall modularity (max):', max(_alllperc) * 100, end='\n\n')

    return average(_alllperc)


if __name__ == '__main__':
    calculate_modularity('/home/svanderwoude/UvA/Thesis/Projects/gain/')
