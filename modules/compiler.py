from modules.commands.blank import Blank
from modules.commands.command_enum import EnumCommand
from modules.commands.command_validator import CommandValidator
from modules.commands.exit import Exit
from modules.commands.insert import Insert
from modules.commands.invalid_command import InvalidCommand
from modules.commands.metadata import Metadata
from modules.commands.select import Select


class Compiler:

    def __init__(self):
        self.command_validator = CommandValidator()

    def do(self, user_input):
        split_input = user_input.split()

        command_string = self.command_validator.command_string(split_input)

        if command_string == EnumCommand.SELECT.value:
            if self.command_validator.do_for_select(split_input):
                return InvalidCommand()
            return Select()
        elif command_string == EnumCommand.INSERT.value:
            if self.command_validator.do_for_insert(split_input):
                return InvalidCommand()
            pk = self.command_validator.get_id(split_input)
            username = self.command_validator.get_username(split_input)
            email = self.command_validator.get_email(split_input)
            return Insert(pk, username, email)
        elif command_string == EnumCommand.EXIT.value:
            if self.command_validator.do_for_exit(split_input):
                return InvalidCommand()
            return Exit()
        elif command_string == EnumCommand.METADATA.value:
            return Metadata()
        elif command_string == EnumCommand.BLANK.value:
            return Blank()
        else:
            return InvalidCommand()
