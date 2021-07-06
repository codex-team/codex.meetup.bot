from enum import Enum, auto


class State(Enum):
    START = auto()
    GET_SERVERS_LIST = auto()
    GET_SERVER = auto()
    DELETE_MY_SERVER = auto()
    GET_FULL_SERVERS_LIST = auto()
    DELETE_ALL_SERVERS = auto()
    CONFIRM_PARTICIPATION = auto()
    REJECT_PARTICIPATION = auto()

    def pattern(self):
        return '^' + str(self.name) + '$'
