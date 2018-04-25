import ast


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


if __name__ == '__main__':
    _calls = {}
    _definitions = []
    _alllperc = []

    paths = ['testmodule.py', 'testscript.py', 'moduletest.py']

    # Set up function definitions and funciton calls for each file
    for path in paths:
        with open(path) as file:
            data = file.read()
            abstree = ast.parse(data)

            for call in calls(abstree):
                # Exclude defaults (only print for now)
                if call != 'print':
                    create_or_update(_calls, call, path)
            
            for definition in definitions(abstree):
                _definitions.append(definition + '_' + path)

    
    # Calculate modularity for each file
    for path in paths:
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

        print('Local call count:', local_count)
        print('Total call count:', all_count)
        print('Modularity percentage:', perc * 100, end='\n\n')

    print('-' * 50, end='\n\n')
    print('Overall modularity (avg):', (sum(_alllperc) / len(paths)) * 100)
    print('Overall modularity (min):', min(_alllperc) * 100)
    print('Overall modularity (max):', max(_alllperc) * 100)
