import os
import time
from os import mkdir, getcwd, system, path
import ctypes
from time import sleep
from json import load, dump
from sys import platform
from pick import pick
from colorama import Fore, Back, Style


class Manager:
    def __init__(self):
        self.CONFIG: dict = self.init_config()
        self.HOME_PATH = getcwd()
        self.check_platform()
        self.run()

    def run(self):
        self.show_menu()

    def init_config(self) -> dict:
        """
        Initializing the config
        """
        # FIXME Переписать функцию
        if self.check_config():
            with open("CONFIG.json", "r", encoding="utf-8") as file:
                return load(file)
        else:
            with open("CONFIG.json", "w+") as file:
                default_config = {
                    "psexec": "path\\to\\psexec",
                    "commands": {
                        "Add_Command": "Add_Command",
                    },
                    "examples": {
                        "test_command_name": "Silent install python",
                        "test_command_arg": "\\\\server/folder/path/python3.10.exe /S"
                    }
                }
                dump(default_config, file)

    def check_config(self):
        # FIXME Существует или нет
        if os.path.exists(f'{self.HOME_PATH}\\CONFIG.json'):
            print(f'[Конфиг найден...]')
            return True
        else:
            print(f'[Конфиг не найден... Происходит создание стандартного конфига]')
            return False

    @staticmethod
    def check_platform():
        """
        Checking the platform, if windows
        then enable colors in the console
        """
        if platform == "win32":
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    def show_menu(self):
        system("cls")
        title = 'Choose command:'
        commands = self.CONFIG["commands"]
        if commands:
            options = [command for command in commands]
            option, index = pick(options, title, indicator=">")
            match option:
                case "Add_Command":
                    self.add_command()
                case "Remove_Command":
                    pass
                case default:
                    self.run_command(option)
        else:
            print(f"{Fore.RED}[На данный момент нет зарегистрированных команд...]{Style.RESET_ALL}")
            self.add_command()

    def wait_before_menu(self):
        for tick in range(15, 0, -1):
            print(f'[До возврата в главное меню осталось... {tick}]', end="\r", flush=True)
            sleep(1)
        self.show_menu()

    def run_command(self, command_name):
        with open(f'{self.HOME_PATH}\\{command_name}\\{command_name}.txt', 'r') as file:
            command = file.readline()
        print(f'{command}')
        self.wait_before_menu()

    def add_command(self):
        """
        Manager for adding commands
        """
        print(f"\t{Fore.GREEN}Для добавления команды напишите в следующем формате:{Style.RESET_ALL}")
        print(f'\t\t{Fore.MAGENTA} [Command name] >> "command" {Style.RESET_ALL}')
        print('\tExample: \n',
              f'\t\t{Fore.MAGENTA} {self.CONFIG["examples"]["test_command_name"]} >> '
              f'"{self.CONFIG["examples"]["test_command_arg"]}" {Style.RESET_ALL}\n')

        new_command: list = [elem.strip(" ") for elem in input().split(">>")]

        if self.check_format_new_command(new_command):
            if self.create_command_folder(command_name=new_command[0]):
                if self.create_command_file(command_data=new_command):
                    if self.add_command_to_config(command_name=new_command[0]):
                        print(f'{Fore.GREEN}[Команда успешно добавлена в список команд...OK]{Style.RESET_ALL}')
        self.wait_before_menu()

    @staticmethod
    def check_format_new_command(command_data: list):
        """
        Checking the entered command for format compliance
        so that there are no errors during the addition
        process and in subsequent executions
        """
        def check_blacklist_chars(text: str):
            """
            Checking the entered command name for the content
            of forbidden characters when creating a folder
            """
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
        """
        Creating a folder corresponding
        to the command
        """
        command_name = command_name.replace(" ", "_")
        try:
            mkdir(command_name)
            print(f'{Fore.GREEN}[Папка успешно создана...OK]{Style.RESET_ALL}')
            return True
        except Exception as e:
            print(f'{Fore.RED}Ошибка создания папки')
            print(f'{e}\n{Style.RESET_ALL}')
            return False

    def create_command_file(self, command_data: list):
        """
        Creating a file containing
        the command text
        """
        try:
            with open(f'{self.HOME_PATH}\\{command_data[0].replace(" ", "_")}\\{command_data[0].replace(" ", "_")}.txt',
                      'w+') as file:
                file.write(f'{command_data[1]}')
            print(f'{Fore.GREEN}[Файл команды успешно создан...OK]{Style.RESET_ALL}')
            return True
        except Exception as e:
            print(f'{Fore.RED}Ошибка создания файла команды')
            print(f'{e}\n{Style.RESET_ALL}')
            return False

    def add_command_to_config(self, command_name):
        command = command_name.replace(" ", "_")
        self.CONFIG['commands'][f'{command}'] = f'{self.HOME_PATH}\\{command}\\{command}.txt'
        try:
            with open(f'{self.HOME_PATH}\\CONFIG.json', "w") as outfile:
                dump(self.CONFIG, outfile)
            return True
        except Exception as e:
            print(f'{Fore.RED}Ошибка записи команды в конфиг файл')
            print(f'{e}\n{Style.RESET_ALL}')
            return False


if __name__ == '__main__':
    worker = Manager()
