import random
import string


def rand_number_n_digits(num_digits: int):
    return random.randrange(10**(num_digits - 1), (10**num_digits) - 1)


def get_random_string(min_length: int = 5, max_length: int = 10):
    length = random.randrange(min_length, max_length)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))