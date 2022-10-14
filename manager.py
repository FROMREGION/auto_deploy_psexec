import os
from json import load
from pick import pick
# title = 'Please choose your favorite programming language: '
# options = ['Java', 'JavaScript', 'Python', 'PHP', 'C++', 'Erlang', 'Haskell']
# option, index = pick(options, title, indicator="->")
# print(option)


class Manager:
    def __init__(self):
        self.CONFIG = self.init_config()
        self.run()

    def run(self):
        self.check_commands()

    @staticmethod
    def init_config():
        with open("CONFIG.json", "r", encoding="utf-8") as file:
            return load(file)

    def check_commands(self):
        commands = self.CONFIG["commands"]
        if commands:
            for number, command_name in commands:
                print(number, command_name)
        else:
            print("На данный момент нет зарегистрированных команд...")
            self.add_command()

    def add_command(self):
        print("Для добавления команды напишите в следующем формате:")
        print("[Command name]-[command]")


if __name__ == '__main__':
    worker = Manager()
