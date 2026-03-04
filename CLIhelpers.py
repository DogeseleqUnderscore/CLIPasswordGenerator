CSI = "\033["
RESET = "\033[0m"

def print_error(msg):
    print(f"{CSI}1;31m[!!]{RESET} >> {msg}")

def print_warn(msg):
    print(f"{CSI}1;93m[!]{RESET} >> {msg}")

def print_success(msg):
    print(f"{CSI}1;92m[ :D ]{RESET} >> {msg}")

def print_info(msg, blinking=False):
    if blinking:
        print(f"{CSI}1;5m[#]{CSI}5m >> {msg}")
    else:
        print(f"{CSI}1m[#]{RESET} >> {msg}")