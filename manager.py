import os
import time
from os import mkdir, getcwd, system, path
import ctypes
from time import sleep
from json import load, dump
from sys import platform
from pick import pick
from prettify_print import message_error, message_success, message_magenta, message_warning
import getpass


class Manager:
    def __init__(self):
        self.check_platform()
        self.HOME_PATH = getcwd()
        self.CONFIG: dict = self.init_config()
        self.login, self.password = self.account_register()
        self.current_room = self.select_room()
        self.run()

    def run(self):
        if self.CONFIG:

            self.return_to_menu(tick_to=3)

    @staticmethod
    def account_register():
        print(message_warning(f'\tВведите ваш логин:'))
        login = input('> ').strip().lower()

        print(message_warning(f'\tВведите ваш пароль:'))
        password = getpass.getpass('> ').strip()

        return login, password

    @staticmethod
    def select_room():
        print(message_warning(f'\tВведите номер аудитории: '))
        print(message_magenta(f'\tExample: u518-520'))
        return input('Room: ').lower()

    def init_config(self) -> dict:
        """
        Initializing the config
        """
        if path.exists(f'{self.HOME_PATH}\\CONFIG.json'):
            print(message_success("[Конфиг есть... Происходит загрузка конфига]"))
            with open("CONFIG.json", "r", encoding="utf-8") as file:
                return load(file)
        else:
            print(message_error("[Конфиг не найден... Происходит создание стандартного конфига]"))
            try:
                with open("CONFIG.json", "w+") as file:
                    default_config = {
                        "psexec": "",
                        "commands": {
                            "Change_Room": "Change_Room",
                            "Add_Command": "Add_Command",
                        },
                        "examples": {
                            "test_command_name": "Silent install python",
                            "test_command_arg": "\\\\server\\folder\\path\\python3.10.exe /S"
                        }
                    }
                    dump(default_config, file)
                print(message_success("[Конфиг создан успешно...]"))
                return default_config
            except Exception as e:
                print(message_error("[Ошибка создания файла конфига]"))
                print(message_error(e))
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
        title = f'Ваш логин: [{self.login}] \n' \
                f'Выбранная комната: [{self.current_room}] \n\n' \
                f'Choose command:'

        commands = self.CONFIG["commands"]
        if commands:
            options = [command for command in commands]
            option, index = pick(options, title, indicator=">")
            match option:
                case "Add_Command":
                    self.add_command()
                case "Change_Room":
                    self.current_room = self.select_room()
                    self.show_menu()
                case "Remove_Command":
                    pass
                case default:
                    self.run_command(option)
        else:
            print(message_error("[На данный момент нет зарегистрированных команд...]"))
            self.add_command()

    def return_to_menu(self, tick_to=15):
        for tick in range(tick_to, 0, -1):
            print(message_warning(f'До возврата в главное меню осталось... {tick}'), end="\r", flush=True)
            sleep(1)
        self.show_menu()

    def run_command(self, command_name):
        with open(f'{self.HOME_PATH}\\{command_name}\\{command_name}.txt', 'r') as file:
            command = file.readline()
        print(f'{command}')
        self.return_to_menu()

    def add_command(self):
        """
        Manager for adding commands
        """
        print(message_success("\tДля добавления команды напишите в следующем формате:"))
        print(message_magenta('\t\t[Command name] >> "command"'))
        print('\tExample: \n',
              message_magenta(f'\t\t{self.CONFIG["examples"]["test_command_name"]} >> '),
              message_magenta(f'"{self.CONFIG["examples"]["test_command_arg"]}"\n'))

        new_command: list = [elem.strip(" ") for elem in input().split(">>")]

        if self.check_format_new_command(new_command):
            if self.create_command_folder(command_name=new_command[0]):
                if self.create_command_file(command_data=new_command):
                    if self.add_command_to_config(command_name=new_command[0]):
                        print(message_success("[Команда успешно добавлена в список команд...OK]"))
        self.return_to_menu(tick_to=3)

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
            print(message_error("[Неверный формат добавления команды]"))

    @staticmethod
    def create_command_folder(command_name: str):
        """
        Creating a folder corresponding
        to the command
        """
        command_name = command_name.replace(" ", "_")
        try:
            mkdir(command_name)
            print(message_success("[Папка успешно создана...OK]"))
            return True
        except Exception as e:
            print(message_error("[Ошибка создания папки]"))
            print(message_error(f'{e}'))
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
            print(message_success("[Файл команды успешно создан...OK]"))
            return True
        except Exception as e:
            print(message_error("[Ошибка создания файла команды]"))
            print(message_error(f'{e}'))
            return False

    def add_command_to_config(self, command_name):
        command = command_name.replace(" ", "_")
        self.CONFIG['commands'][f'{command}'] = f'{self.HOME_PATH}\\{command}\\{command}.txt'
        try:
            with open(f'{self.HOME_PATH}\\CONFIG.json', "w") as outfile:
                dump(self.CONFIG, outfile)
            return True
        except Exception as e:
            print(message_error("[Ошибка записи команды в конфиг файл]"))
            print(message_error(f'{e}'))
            return False


if __name__ == '__main__':
    worker = Manager()
