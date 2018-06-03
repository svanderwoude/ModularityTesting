import ast
import os

from python__maintainability import calculate_maintainability
from python__modularity import calculate_modularity
from python__modularity_index_validation import calculate_modularity as validate_modularity


def section_header(section):
    print('=' * 50, end='\n\n')
    print('\x1B[42m', section.upper(), '\x1B[0m', end='\n\n')
    print('=' * 50, end='\n\n')


def setup_files(root):
    count = 0
    errors = 0
    files = []
    zero_liners = 0

    for subdir, dirs, paths in os.walk(root):
        subfiles = []
        subdir = os.path.join(root, subdir)

        for path in paths:
            if not path.endswith('.py') or 'test' in path:
                continue

            path = os.path.join(subdir, path)
            count += 1

            try:
                with open(path) as file:
                    data = file.read()
                    ast.parse(data)
                    
                    if len(data):
                        subfiles.append(path)
                    else:
                        zero_liners += 1
            except:
                errors += 1

        if len(subfiles):
            files.append(subfiles)

    return (files, errors / count)


if __name__ == '__main__':
    roots = [
        # '/home/svanderwoude/UvA/Thesis/Projects/flask',
        # '/home/svanderwoude/UvA/Thesis/Projects/falcon',
        # '/home/svanderwoude/UvA/Thesis/Projects/bottle',
        # '/home/svanderwoude/UvA/Thesis/Projects/cherrypy',
        # '/home/svanderwoude/UvA/Thesis/Projects/klein',
        # '/home/svanderwoude/UvA/Thesis/Projects/aiohttp',
        # '/home/svanderwoude/UvA/Thesis/Projects/tornado',
        # '/home/svanderwoude/UvA/Thesis/Projects/webpy',
        # '/home/svanderwoude/UvA/Thesis/Projects/pyramid',

        # '/home/svanderwoude/UvA/Thesis/Projects/crankycoin',
        # '/home/svanderwoude/UvA/Thesis/Projects/mmgen',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/Piper',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/dashman',
        # '/home/svanderwoude/UvA/Thesis/Projects/bcwallet',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/encompass',
        # '/home/svanderwoude/UvA/Thesis/Projects/django-cc',
        # '/home/svanderwoude/UvA/Thesis/Projects/pywallet',
        # '/home/svanderwoude/UvA/Thesis/Projects/DarkWallet',
        # '/home/svanderwoude/UvA/Thesis/Projects/python-trezor',

        # '/home/svanderwoude/UvA/Thesis/Projects/screenly-ose',
        # '/home/svanderwoude/UvA/Thesis/Projects/iot-python',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/GrovePi',
        # '/home/svanderwoude/UvA/Thesis/Projects/iotedgedev',
        # '/home/svanderwoude/UvA/Thesis/Projects/aws-iot-device-sdk-python',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/azure-iot-sdk-python',
        # '/home/svanderwoude/UvA/Thesis/Projects/PiClock',
        # '/home/svanderwoude/UvA/Thesis/Projects/python-gpiozero',
        # '/home/svanderwoude/UvA/Thesis/Projects/goSecure',
        # '/home/svanderwoude/UvA/Thesis/Projects/audio-reactive-led-strip',
        # '/home/svanderwoude/UvA/Thesis/Projects/picamera',

        # '/home/svanderwoude/UvA/Thesis/Projects/cola',
        # '/home/svanderwoude/UvA/Thesis/Projects/demiurge',
        # '/home/svanderwoude/UvA/Thesis/Projects/feedparser',
        # '/home/svanderwoude/UvA/Thesis/Projects/grab',
        # '/home/svanderwoude/UvA/Thesis/Projects/MechanicalSoup',
        # #  # '/home/svanderwoude/UvA/Thesis/Projects/portia',
        # '/home/svanderwoude/UvA/Thesis/Projects/pyspider',
        # '/home/svanderwoude/UvA/Thesis/Projects/robobrowser',
        # '/home/svanderwoude/UvA/Thesis/Projects/scrapy',

        # '/home/svanderwoude/UvA/Thesis/Projects/gain',
        # '/home/svanderwoude/UvA/Thesis/Projects/xcrawler',
        # '/home/svanderwoude/UvA/Thesis/Projects/crawlerino',
        # '/home/svanderwoude/UvA/Thesis/Projects/Zeek',
        '/home/svanderwoude/UvA/Thesis/Projects/creepy',
        '/home/svanderwoude/UvA/Thesis/Projects/pholcidae',
        '/home/svanderwoude/UvA/Thesis/Projects/crawler4py',
        '/home/svanderwoude/UvA/Thesis/Projects/crawler-1',
    ]


    section_header('modularity')
    print('name,', 'Own Method,', 'MI,')
    discard_threshold = 0.30
    threshold = 0.575

    for root in roots:
        files, fault_perc = setup_files(root)

        if fault_perc > discard_threshold:
            print('%s, %s, %s,' % (root.split('/')[-1], 'DISCARDED', 'DISCARDED'))
            continue

        mavg = calculate_modularity(files, False)

        print(root.split('/')[-1], mavg, (mavg * 10) / 2)

        # mval = validate_modularity(files, False)

        # print('%s, %s, %s,' % (root.split('/')[-1], mval >= threshold, mavg >= threshold))


    section_header('maintainability')
    print('name', 'volume', 'unit_size', 'complexity', end='\n\n')
 
    for root in roots:
        files, zero_liners = setup_files(root)
        testcoverage, volume, complexity = calculate_maintainability(files, False)

        print(root.split('/')[-1], end=' ')

        # Volume
        print(root.split('/')[-1], volume[0], end=' ')

        if volume[0] <= 66000:
            print(5, end=' ')
        elif volume[0] > 66000 and volume[0] <= 246000:
            print(4, end=' ')
        elif volume[0] > 246000 and volume[0] <= 665000:
            print(3, end=' ')
        elif volume[0] > 665000 and volume[0] <= 1310000:
            print(2, end=' ')
        else:
            print(1, end=' ')

        # Unit size (using SIG Building Maintainable Software page 45). Look at adjusting percentages below 5 stars.
        small = [v for v in volume[5] if v <= 15]
        medium = [v for v in volume[5] if v > 15]
        large = [v for v in volume[5] if v > 30]
        very_large = [v for v in volume[5] if v > 60]
        total = len(volume[5])

        small_perc = (len(small) / total) * 100
        medium_perc = (len(medium) / total) * 100
        large_perc = (len(large) / total) * 100
        very_large_perc = (len(very_large) / total) * 100
        
        if small_perc >= 57.3 and medium_perc <= 43.7 and large_perc <= 22.3 and very_large_perc <= 6.9:
            print(5, end=' ')
        elif small_perc >= 50 and medium_perc <= 50 and large_perc <= 25 and very_large_perc <= 10:
            print(4, end=' ')
        elif small_perc >= 45 and medium_perc <= 55 and large_perc <= 30 and very_large_perc <= 12.5:
            print(3, end=' ')
        elif small_perc >= 40 and medium_perc <= 60 and large_perc <= 35 and very_large_perc <= 15:
            print(2, end=' ')
        else:
            print(1, end=' ')


        # Complexity
        moderate = [c for c in complexity if c > 10 and c <= 20]
        high = [c for c in complexity if c > 20 and c <= 50]
        very_high = [c for c in complexity if c > 50]
        total = len(complexity)
        
        try:
            moderate_perc = (len(moderate) / total) * 100
            high_perc = (len(high) / total) * 100
            very_high_perc = (len(very_high) / total) * 100

            if moderate_perc <= 25 and high_perc == 0 and very_high_perc == 0:
                print(5, end=' ')
            elif moderate_perc <= 30 and high_perc <= 5 and very_high_perc == 0:
                print(4, end=' ')
            elif moderate_perc <= 40 and high_perc <= 10 and very_high_perc == 0:
                print(3, end=' ')
            elif moderate_perc <= 50 and high_perc <= 15 and very_high_perc <= 5:
                print(2, end=' ')
            else:
                print(1, end=' ')
        except ZeroDivisionError:
            print('N/A')

        print('')
