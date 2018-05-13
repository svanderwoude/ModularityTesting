import ast
import math
import os

from numpy import average

from python__libraryfunctions import res
from python__maintainability import calculate_complexity, calculate_volume


def calculate_modularity(files, log=True):
    mqs = []

    for subdir in files:
        for path in subdir:
            with open(path) as file:
                try:
                    data = file.read()
                    tree = ast.parse(data, 'eval')
                except SyntaxError:
                    continue

                # Functions: the number of functions in module
                functions = sum(isinstance(exp, ast.FunctionDef) for exp in tree.body)

                fq = 0.172 * functions + 0.171 if functions <= 5 else pow(functions - 4.83, -2.739)


            # Size Metrics: NLOC, Lines and Statements. NLOC will also represent others.
            ncloc = calculate_volume(path)

            locq = (0.0125 * ncloc) + 0.375 if ncloc <= 50 else pow(ncloc - 50, -2.046)

            # Cohesion: LCOM4 (improved version of LCOM1).
            lcom4 = 1

            # Module quality
            mq = ((locq + fq) / (2 * lcom4)) + 0.25

            # print(locq, fq, mq)
            mqs.append(mq)

    if len(mqs):
        if log:
            print('AVERAGE:', average(mqs), '\n')
        return average(mqs)

    return 1
    
