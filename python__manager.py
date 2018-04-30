from python__maintainability import calculate_maintainability
from python__modularity import calculate_modularity


def section_header(section):
    print('=' * 50, end='\n\n')
    print('\x1B[42m', section.upper(), '\x1B[0m', end='\n\n')
    print('=' * 50, end='\n\n')


if __name__ == '__main__':
    # root = '/home/svanderwoude/UvA/Thesis/Projects/flask/'
    root = '/home/svanderwoude/UvA/Thesis/Projects/falcon/'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/bottle/'
    # root = '/home/svanderwoude/UvA/Thesis/Projects/cherrypy/'

    section_header('modularity')
    mavg, mmed, mmin, mmax = calculate_modularity(root, True)

    # section_header('maintainability')
    # testcoverage, volume = calculate_maintainability(root, True)