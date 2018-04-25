from python__modularity import calculate_modularity


if __name__ == '__main__':
    root = '/home/svanderwoude/UvA/Thesis/repos/'
    mavg, mmed, mmin, mmax = calculate_modularity(root, True)

    print(mavg)