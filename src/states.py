from enum import Enum, auto


class State(Enum):
    START = auto()
    GET_SERVERS_LIST = auto()
    GET_SERVER = auto()
    GET_FULL_SERVERS_LIST = auto()
    DELETE_ALL_SERVERS = auto()

    def pattern(self):
        return '^' + str(self.name) + '$'
