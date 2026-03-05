from CLIhelpers import *
import subprocess
import argparse
import secrets

VERSION = "1.0"
NAME = f"{CSI}1;33mPython{RESET} {CSI}1mPassword Generator v{VERSION}{RESET}\n"

AUTO_COPY = True # Should the generated password be automatically copied to clipboard? (Requires pyperclip library)
ASK_FOR_INSTALL = True # Should the user be asked to install pyperclip if it's not found? (Only if AUTO_COPY is True)
DEF_PASS_LEN = 32 # Default password length, can be changed using --length argument.
DEF_PASS_CHARS = 'lowercase,uppercase,numbers' # Default allowed chars, can be changed using --allowed-chars argument. (uppercase,lowercase,numbers,special,all)

def copy_to_clipboard(passwd):
    import pyperclip
    pyperclip.copy(passwd)
    print_success("Copied to clipboard!")

def try_to_copy_to_clipboard(pw):
    try:
        copy_to_clipboard(pw)
    except ModuleNotFoundError:
        print("\n")
        print_error(
            f"Cannot copy password to clipboard,\n{CSI}1mpyperclip{RESET} library is missing.\n\nInstall it using {CSI}1mpip install pyperclip{RESET}")
        if AUTO_COPY and ASK_FOR_INSTALL:
            nput = input("Do you want to install it now? (y/n)\n")
            print("\n")
            if nput.lower() == "y":
                result = subprocess.run(['pip', 'install', 'pyperclip'], check=True, text=True)
                print("\n")
                try:
                    copy_to_clipboard(pw)
                except Exception as e:
                    print_error(f"Failed to install pyperclip!")
                    print(result.stdout)
                    exit(1)
            elif nput.lower() == "n":
                print_info("Ok :(")
                exit(1)
            else:
                print_warn("Invalid input.")
                exit(1)


def generate_password(length, allowed_chars):
    char_sets = {
        'uppercase': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'lowercase': 'abcdefghijklmnopqrstuvwxyz',
        'numbers': '0123456789',
        'special': '!@#$%^&*()-_=+[]{}|;:,.<>?'
    }

    chars = ''
    for char_type in allowed_chars:
        if char_type in char_sets:
            chars += char_sets[char_type]

    if not chars:
        print_error("No valid character types selected. Please choose from uppercase, lowercase, numbers, special.")
        exit(1)

    password = ''.join(secrets.choice(chars) for _ in range(length))
    return password


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=NAME)
    ap.add_argument('--length', help='Length of the generated password.', type=int, default=DEF_PASS_LEN)
    ap.add_argument('--allowed-chars', help='Comma separated types of chars that will be used in the generated password: uppercase,lowercase,numbers,special', default=DEF_PASS_CHARS)

    args = ap.parse_args()

    pass_length = None
    pass_chars = None

    print_info("Generating password...")

    if args.length is not None:
        pass_length = args.length

    if args.allowed_chars is not None:
        pass_chars = args.allowed_chars.split(',')
        for char in pass_chars:
            if char == 'all':
                pass_chars = ['uppercase', 'lowercase', 'numbers', 'special']
            elif char not in ['uppercase', 'lowercase', 'numbers', 'special']:
                print_error(f"Invalid character type: {char}!")
                exit(1)

    try:
        password = generate_password(pass_length, pass_chars)
        print_success("Generated Password!")
        print(f"{CSI}1m+{"-" * (pass_length + 6)}+")
        print(f"|   {password}   |")
        print(f"+{"-" * (pass_length + 6)}+{RESET}")

        if AUTO_COPY:
            try_to_copy_to_clipboard(password)
        else:
            _input = input("Copy password to clipboard? (y/n)\n")
            if _input.lower() == "y":
                try_to_copy_to_clipboard(password)

    except Exception as e:
        print_error(f"Failed to generate password: {e}")


