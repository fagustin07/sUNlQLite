from enum import Enum


class EnumCommand(Enum):
    # commands
    SELECT = "SELECT"
    INSERT = "INSERT"

    # meta-commands
    EXIT = ".EXIT"
    METADATA = ".METADATA"
    EXCEPTION = "EXCEPTION"
