from nanoid import generate


def nano_id():
    alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return generate(alphabet, 10)


def nano_number_id():
    alphabet = '0123456789'
    return generate(alphabet, 6)
