def get_numbers(line):
    numbers = line.split(':')[1]
    winning_numbers = numbers.split('|')[0].strip().split(' ')
    my_numbers = numbers.split('|')[1].strip().split(' ')
    return [x for x in my_numbers if x != ''], [x for x in winning_numbers if x != '']