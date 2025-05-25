def format_number(number):
    num_str = str(abs(number))
    result = ''
    for i, digit in enumerate(reversed(num_str)):
        if i > 0 and i % 3 == 0:
            result = ',' + result
        result = digit + result
    
    if number < 0:
        result = '-' + result
    return result

import sys
print(format_number(int(sys.argv[1])))