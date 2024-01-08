from colorama import Style


def print_with_color(message, color):
    print(color + message + "\n" + Style.RESET_ALL)