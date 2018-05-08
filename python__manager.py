from python__maintainability import calculate_maintainability
from python__modularity import calculate_modularity


def section_header(section):
    print('=' * 50, end='\n\n')
    print('\x1B[42m', section.upper(), '\x1B[0m', end='\n\n')
    print('=' * 50, end='\n\n')


if __name__ == '__main__':
    root = '/home/svanderwoude/UvA/Thesis/Projects/flask'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/falcon'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/bottle'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/cherrypy'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/klein'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/aiohttp'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/tornado'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/webpy'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/pyramid'

    # root = '/home/svanderwoude/UvA/Thesis/Projects/crankycoin'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/mmgen'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/Piper'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/dashman'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/bcwallet'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/encompass'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/django-cc'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/pywallet'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/DarkWallet'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/python-trezor'

    section_header('modularity')
    mavg, mmed, mmin, mmax = calculate_modularity(root, True)

    # section_header('maintainability')
    # testcoverage, volume = calculate_maintainability(root, True)