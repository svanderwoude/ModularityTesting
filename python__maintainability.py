import coverage
import os
from radon.visitors import ComplexityVisitor
import re
import signal
import subprocess

from numpy import average
from numpy.ma import median


# https://www.sig.eu/wp-content/uploads/2016/10/APracticalModelForMeasuringMaintainability.pdf


def calculate_complexity(path):
    try:
        with open(path) as file:
            data = file.read()

            v = ComplexityVisitor.from_code(data)
            return v.complexity
    except SyntaxError:
        return -1


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
    return 0


def calculate_maintainability(files, log=True):
    _calls = {}
    _definitions = []
    _allperc_testcoverage = []
    _all_volume = []
    _all_complexity = []

    # Set up function definitions and funciton calls for each file
    for subdir in files:
        for path in subdir:
            testcoverage = calculate_testcoverage(path)
            volume = calculate_volume(path)
            complexity = calculate_complexity(path)

            _allperc_testcoverage.append(testcoverage)
            _all_volume.append(volume)

            if complexity >= 0:
                _all_complexity.append(complexity)

            if log:
                print('FILE:', path)
                print('Complexity:', complexity)
                print('Test coverage:', testcoverage * 100)
                print('Volume:', volume, end='\n\n')

    if log:
        print('-' * 50, end='\n\n')
        print('Overall test coverage (avg):', average(_allperc_testcoverage) * 100)
        print('Overall test coverage (med):', median(_allperc_testcoverage) * 100)
        print('Overall test coverage (min):', min(_allperc_testcoverage) * 100)
        print('Overall test coverage (max):', max(_allperc_testcoverage) * 100)
        print('Overall volume (avg):', average(_all_volume))
        print('Overall volume (med):', median(_all_volume))
        print('Overall volume (min):', min(_all_volume))
        print('Overall volume (max):', max(_all_volume))
        print('Overall volume (sum):', sum(_all_volume), end='\n\n')

    return ((average(_allperc_testcoverage), median(_allperc_testcoverage),
             min(_allperc_testcoverage), max(_allperc_testcoverage)),
            (sum(_all_volume), average(_all_volume), median(_all_volume),
             min(_all_volume), max(_all_volume), _all_volume),
            _all_complexity)


if __name__ == '__main__':
    calculate_maintainability('/home/svanderwoude/UvA/Thesis/Projects/flask/')
