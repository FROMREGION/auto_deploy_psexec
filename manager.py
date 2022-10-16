from os import mkdir, getcwd
import ctypes
from json import load
from sys import platform
from anytree import Node, RenderTree
from pickpack import pickpack
from colorama import Fore, Back, Style


class Manager:
    def __init__(self):
        self.CONFIG: dict = self.init_config()
        self.HOME_PATH = getcwd()
        self.check_platform()
        self.run()

    def run(self):
        self.check_commands()

    @staticmethod
    def init_config() -> dict:
        with open("CONFIG.json", "r", encoding="utf-8") as file:
            return load(file)

    @staticmethod
    def check_platform():
        if platform == "win32":
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def check_commands(self):
        commands = self.CONFIG["commands"]
        if commands:
            for number, command_name in commands:
                print(number, command_name)
        else:
            print(f"{Fore.RED}[На данный момент нет зарегистрированных команд...]{Style.RESET_ALL}")
            self.add_command()

    def add_command(self):
        print(f"\t{Fore.GREEN}Для добавления команды напишите в следующем формате:{Style.RESET_ALL}")
        print(f'\t\t{Fore.MAGENTA} [Command name] >> "command" {Style.RESET_ALL}')
        print('\tExample: \n',
              f'\t\t{Fore.MAGENTA} {self.CONFIG["examples"]["test_command_name"]} >> '
              f'"{self.CONFIG["examples"]["test_command_arg"]}" {Style.RESET_ALL}\n')
        new_command: list = [elem.strip(" ") for elem in input().split(">>")]
        if self.check_format_new_command(new_command):
            if self.create_command_folder(command_name=new_command[0]):
                print(f'{Fore.GREEN}[Папка успешно создана...OK]{Style.RESET_ALL}')

                if self.create_command_file(command_data=new_command):
                    print(f'{Fore.GREEN}[Файл команды успешно создан...OK]{Style.RESET_ALL}')

    @staticmethod
    def check_format_new_command(command_data: list):
        def check_blacklist_chars(text: str):
            blacklist_chars = ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']
            for char in blacklist_chars:
                if char in text:
                    return False
            return True

        if len(command_data) == 2:
            command_name, command_body = command_data[0], list(command_data[1])
            if check_blacklist_chars(command_name):
                if command_body[0] == '\"' and command_body[-1] == '\"':
                    return True
        else:
            print(f'{Fore.RED}[Неверный формат добавления команды]{Style.RESET_ALL}')

    @staticmethod
    def create_command_folder(command_name: str):
        command_name = command_name.replace(" ", "_")
        try:
            mkdir(command_name)
            return True
        except Exception as e:
            print(f'{Fore.RED}Ошибка создания папки')
            print(f'{e}\n{Style.RESET_ALL}')
            return False

    def create_command_file(self, command_data: list):
        try:
            with open(f'{self.HOME_PATH}\\{command_data[0].replace(" ", "_")}\\{command_data[0].replace(" ", "_")}.txt',
                      'w+') as file:
                file.write(f'{command_data[1]}')
            return True
        except Exception as e:
            print(f'{Fore.RED}Ошибка создания файла команды')
            print(f'{e}\n{Style.RESET_ALL}')
            return False


if __name__ == '__main__':
    worker = Manager()
