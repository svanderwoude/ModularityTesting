import os

from python__maintainability import calculate_maintainability
from python__modularity import calculate_modularity


def section_header(section):
    print('=' * 50, end='\n\n')
    print('\x1B[42m', section.upper(), '\x1B[0m', end='\n\n')
    print('=' * 50, end='\n\n')


def setup_files(root):
    files = []
    zero_liners = 0

    for subdir, dirs, paths in os.walk(root):
        subfiles = []
        subdir = os.path.join(root, subdir)

        for path in paths:
            if not path.endswith('.py') or 'test' in path:
                continue

            path = os.path.join(subdir, path)

            try:
                with open(path) as file:
                    data = file.read()
                    
                    if len(data):
                        subfiles.append(path)
                    else:
                        zero_liners += 1
            except:
                pass

        if len(subfiles):
            files.append(subfiles)

    return (files, zero_liners)


if __name__ == '__main__':
    roots = [
        '/home/svanderwoude/UvA/Thesis/Projects/flask',
        '/home/svanderwoude/UvA/Thesis/Projects/falcon',
        '/home/svanderwoude/UvA/Thesis/Projects/bottle',
        '/home/svanderwoude/UvA/Thesis/Projects/cherrypy',
        '/home/svanderwoude/UvA/Thesis/Projects/klein',
        '/home/svanderwoude/UvA/Thesis/Projects/aiohttp',
        '/home/svanderwoude/UvA/Thesis/Projects/tornado',
        '/home/svanderwoude/UvA/Thesis/Projects/webpy',
        '/home/svanderwoude/UvA/Thesis/Projects/pyramid',

        '/home/svanderwoude/UvA/Thesis/Projects/crankycoin',
        '/home/svanderwoude/UvA/Thesis/Projects/mmgen',
        '/home/svanderwoude/UvA/Thesis/Projects/Piper',
        '/home/svanderwoude/UvA/Thesis/Projects/dashman',
        '/home/svanderwoude/UvA/Thesis/Projects/bcwallet',
        '/home/svanderwoude/UvA/Thesis/Projects/encompass',
        '/home/svanderwoude/UvA/Thesis/Projects/django-cc',
        '/home/svanderwoude/UvA/Thesis/Projects/pywallet',
        '/home/svanderwoude/UvA/Thesis/Projects/DarkWallet',
        '/home/svanderwoude/UvA/Thesis/Projects/python-trezor',
    ]

    section_header('modularity')

    # for root in roots:
    #     files, zero_liners = setup_files(root)
    #     mavg, mmed, mmin, mmax = calculate_modularity(files, False)

    #     print(root.split('/')[-1], mavg, mavg >= 0.575)


    section_header('maintainability')
    print('name', 'volume', 'small', 'medium', 'large', 'lowest', 'low', 'medium', 'high', end='\n\n')

    for root in roots:
        files, zero_liners = setup_files(root)
        testcoverage, volume, complexity = calculate_maintainability(files, False)

        print(root.split('/')[-1], volume[0], end=' ')

        small = [v for v in volume[5] if v <= 15]
        medium = [v for v in volume[5] if v > 15 and v <= 30]
        large = [v for v in volume[5] if v > 30]

        print(len(small) / len(volume[5]),
              len(medium) / len(volume[5]),
              len(large)/ len(volume[5]), end=' ')

        lowest = [c for c in complexity if c <= 10]
        low = [c for c in complexity if c > 10 and c <= 20]
        medium = [c for c in complexity if c > 21 and c <= 50]
        high = [c for c in complexity if c > 50]

        if len(complexity):
            print(len(lowest) / len(complexity),
                  len(low) / len(complexity),
                  len(medium) / len(complexity),
                  len(high) / len(complexity))
