class UndoException(Exception):
    def __init__(self, message):
        super().__init__(message)


class UndoRepository:
    def __init__(self):
        # eventually set
        self.__data = list()

    def add_operation(self, undo, down_undo, redo, down_redo):
        self.__data.append((undo, down_undo, redo, down_redo))

    def pop_operation(self):
        if len(self.__data) <= 0:
            raise UndoException('Cannot undo further!')
        else:
            out = self.__data.pop()
            return out[0], out[1], out[2], out[3]
