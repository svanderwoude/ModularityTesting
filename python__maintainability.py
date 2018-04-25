# import coverage
import os
# import radon
import re
import signal
import subprocess

from numpy import average
from numpy.ma import median


def calculate_testcoverage(path):
    # cov = coverage.Coverage()
    # cov.start()

    # pro = subprocess.Popen(
    #     self.testargs,
    #     stdout=subprocess.PIPE,
    #     preexec_fn=os.setsid,
    #     close_fds=True)
    # os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

    # cov.stop()
    # cov.save()
    # return 'testing...'
    return 0


def calculate_volume(path):
    result = subprocess.Popen(
        ['sloccount', path],
        stdout=subprocess.PIPE)

    for line in result.stdout:
        if line.startswith('python'.encode()):
            line = str(line)
            line = re.sub('[ \t\n]+', ' ', line)
            line_count = int(line.split(' ')[1])
            return line_count


def calculate_maintainability(root, log=True):
    _calls = {}
    _definitions = []
    _allperc_testcoverage = []
    _all_volume = []
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
                testcoverage = calculate_testcoverage(path)
                volume = calculate_volume(path)
            except FileNotFoundError:
                _errorcount += 1
                _pathcount -= 1

            _allperc_testcoverage.append(testcoverage)
            _all_volume.append(volume)

            if log:
                print('FILE:', path)
                print('Test coverage:', testcoverage * 100)
                print('Volume:', volume, end='\n\n')

    if log:
        print('-' * 50, end='\n\n')
        print('Tested %d files' % _pathcount)
        print('Failed %d files' % _errorcount)
        print('Overall test coverage (avg):', average(_allperc_testcoverage) * 100)
        print('Overall test coverage (med):', median(_allperc_testcoverage) * 100)
        print('Overall test coverage (min):', min(_allperc_testcoverage) * 100)
        print('Overall test coverage (max):', max(_allperc_testcoverage) * 100)
        print('Overall volume (avg):', average(_all_volume))
        print('Overall volume (med):', median(_all_volume))
        print('Overall volume (min):', min(_all_volume))
        print('Overall volume (max):', max(_all_volume), end='\n\n')

    return ((average(_allperc_testcoverage), median(_allperc_testcoverage),
             min(_allperc_testcoverage), max(_allperc_testcoverage)),
            (average(_all_volume), median(_all_volume), min(_all_volume),
             max(_all_volume)))


if __name__ == '__main__':
    calculate_maintainability('/home/svanderwoude/UvA/Thesis/repos/')
