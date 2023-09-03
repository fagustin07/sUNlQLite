from modules.commands.command_enum import EnumCommand
from modules.commands.exit import Exit
from modules.commands.insert import Insert
from modules.commands.invalid_command import InvalidCommand
from modules.commands.select import Select


class Compiler:

    @staticmethod
    def do(user_input):
        splitted_input = user_input.split()

        command_string = splitted_input[0].upper()

        if command_string == EnumCommand.SELECT.value:
            return Select()
        elif command_string == EnumCommand.INSERT.value:
            return Insert(0, "", "")
        elif command_string == EnumCommand.EXIT.value:
            return Exit()
        else:
            return InvalidCommand()
