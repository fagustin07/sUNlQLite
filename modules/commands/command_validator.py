import sys


class CommandValidator:

    @staticmethod
    def command_string(split_entry):
        return split_entry[0].upper()

    def do_for_select(self, split_entry):
        return self.__is_invalid_select_command(split_entry)

    def do_for_insert(self, split_entry):
        return self.__is_invalid_insert_command(split_entry)

    def do_for_exit(self, split_entry):
        return self.__is_invalid_exit(split_entry)

    @staticmethod
    def get_id(split_entry):
        return int(split_entry[1])

    @staticmethod
    def get_email(split_entry):
        return split_entry[3]

    @staticmethod
    def get_username(split_entry):
        return split_entry[2]

    # PRIVATE
    @staticmethod
    def __is_invalid_insert_command(split_entry):
        # todo: refactor: renames
        return (len(split_entry) != 4 or
                not split_entry[1].isdigit() or
                # todo: refactor: extract a encoder
                len(split_entry[2].encode('ascii')) > 32 or
                len(split_entry[3].encode('ascii')) > 255)

    @staticmethod
    def __is_invalid_select_command(split_entry):
        return len(split_entry) > 1

    def __is_invalid_exit(self, split_entry):
        return self.__has_more_than_one_word(split_entry)

    @staticmethod
    def __has_more_than_one_word(split_entry):
        return len(split_entry) > 1
