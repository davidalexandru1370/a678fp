class RedoRepositoryException(Exception):
    def __init__(self, message):
        super().__init__(message)

class RedoRepository:
    def __init__(self):
        self.__data = list()

    def clear(self):
        self.__data.clear()

    def add_in(self, redo, down_redo, undo, down_undo):
        self.__data.append((redo, down_redo, undo, down_undo))

    def pop_operation(self):
        if len(self.__data) == 0:
            raise RedoRepositoryException('There s no more to redo!')
        else:
            # operation, down_redo, undo, down_undo = self.__data.pop()
            out = self.__data.pop()
            return out[0], out[1], out[2], out[3]
