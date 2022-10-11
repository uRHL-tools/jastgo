import sys
from src import aux
from src import stego

# This is the main program
# It maps the configuration from ./db/secrets.yml into an object
# This (global) object is accessible from any other function

# Optimize memory usage using a char to indicate the exit option umber. Char -> 1B, int -> 4B
__MENU_EXIT = '9'
__menu_options = ['Encode a message', 'Obtain message from an encoded file']

def print_usage():
    print(f'Usage: python3 jastgo.py [encode <msg_to_encode>] [decode <path_to_encoded_file>] [help]')


def print_help():
    # Here I should print whatever help message I consider necessary
    print(f'HELP')
    print_usage()


def print_header():
    print(f'+---------------------------------------+')
    print(f'|\tJASTGO: Java Stego Tool\t\t|')
    print(f'+---------------------------------------+\n')


def print_menu():

    print_header()
    for index, opt in enumerate(__menu_options):
        print(f'{index + 1}.  {opt}')
    print(f'\n{__MENU_EXIT}.  Exit')
    print(f'------------------------------\n')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        # TODO: show app menu
        nx = '-1'
        while nx != __MENU_EXIT:
            print_menu()
            nx = input(f'Select an option to continue:\t')
            if nx == '1':
                # Encode
                msg = input("Type your secret message:\t")
                stego.encode(msg)
                exit(0)
            elif nx == '2':
                # Decode
                encoded_file = input(f'Path to file containing the message:\t')
                stego.decode(encoded_file)
                exit(0)
            elif nx == __MENU_EXIT:
                print(f'Exiting...')
            else:
                print(f'Option not recognised')
        exit(0)
    elif sys.argv[1] == 'encode':
        if len(sys.argv) > 2:
            msg = sys.argv[-1]
        else:
            msg = input("Type your secret message:\t")
        stego.encode(msg)
        exit(0)
    elif sys.argv[1] == 'decode':
        if len(sys.argv) > 2:
            encoded_file = sys.argv[-1]
        else:
            encoded_file = input(f'Path to file containing the message:\t')
        print(f'The secret message is:\n')
        print((stego.decode(encoded_file)))
        exit(0)
    elif sys.argv[1] == 'help':
        print_help()
        exit(0)
    else:
        print(f'Bad usage')
        print_usage()
        exit(1)
