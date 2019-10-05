
def int_to_list_of_binary_digits(integer_input):
    retval = []

    while (integer_input > 0):
        retval.append(integer_input % 2)
        integer_input //= 2

    return retval