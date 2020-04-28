def month_num_to_str(x):
    convert = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }
    return convert[x]

def month_num_to_abr(x):
    convert = {
        1: 'Jan',
        2: 'Feb',
        3: 'Mar',
        4: 'Apr',
        5: 'May',
        6: 'Jun',
        7: 'Jul',
        8: 'Aug',
        9: 'Sep',
        10: 'Oct',
        11: 'Nov',
        12: 'Dec',
    }
    return convert[x]

def weekday_str_to_abr(x):
    convert = {
        'Sunday': 'Sun',
        'Monday': 'Mon',
        'Tuesday': 'Tue',
        'Wednesday': 'Wed',
        'Thursday': 'Thu',
        'Friday': 'Fri',
        'Saturday': 'Sat'
    }
    return convert[x]

def weekday_next(x):
    convert = {
        'Sunday': 'Monday',
        'Monday': 'Tuesday',
        'Tuesday': 'Wednesday',
        'Wednesday': 'Thursday',
        'Thursday': 'Friday',
        'Friday': 'Saturday',
        'Saturday': 'Sunday'
    }
    return convert[x]

def weekday_start(x):
    convert = {
        'Sunday': 0,
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6
    }
    return convert[x]

def phone_strip(x):
    string = str(x).replace('-','').replace('(','').replace(')','').replace('.','')
    convert = int(string)
    return convert

def phone_format(x):
    x = str(x)
    count=0
    for each in x:
        if count == 0:
            convert = '('
        elif count == 3:
            convert = convert + ')'
        elif count == 6:
            convert = convert + '-'
        convert = convert + x[count]
        count += 1
    return convert

def year_two_digits(x):
    x = str(x)
    convert = '\'' + x[-2] + x[-1]
    return convert

def avail_choices(x):
    data = {
        1:'All Day',
        2:'Need Off',
        3:'Late Start',
        4:'Early Out',
        5:'Custom'
    }
    return data[int(x)]
