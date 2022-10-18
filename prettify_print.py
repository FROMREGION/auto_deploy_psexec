from colorama import Fore, Back, Style


def message_success(text):
    return f'{Fore.GREEN}{text}{Style.RESET_ALL}'


def message_error(text):
    return f'{Fore.RED}{text}{Style.RESET_ALL}'


def message_warning(text):
    return f'{Fore.YELLOW}{text}{Style.RESET_ALL}'


def message_magenta(text):
    return f'{Fore.MAGENTA}{text}{Style.RESET_ALL}'
