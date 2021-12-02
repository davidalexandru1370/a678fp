from src.domain.command_pattern import *
import functools


class RedoService:
    def __init__(self, redo_repository, undo_repository):
        self.__data = redo_repository
        self.__undo_repository = undo_repository

    def add_in(self, function_redo, down_redo, parameters_redo, function_undo, down_undo
               , parameters_undo):
        redo_operation = undo(function_redo, *parameters_redo)
        undo_operation = undo(function_undo, *parameters_undo)
        self.__data.add_in(redo_operation, down_redo, undo_operation, down_undo)

    def pop_out(self):
        next = True
        operations = []
        while next == True:
            redo_operation, down_redo, undo_operation, down_undo = self.__data.pop_operation()
            next = down_redo
            if redo_operation.function is not None:
                execute = functools.partial(redo_operation.function, *redo_operation.parameters)
                execute()
            operations.append((redo_operation, down_redo, undo_operation, down_undo))
        for index in range(len(operations) - 1, -1, -1):
            self.__undo_repository.add_operation(operations[index][2], operations[index][3], operations[index][0],
                                                 operations[index][1])
        # return redo_operation, down_redo, undo_operation, down_undo

    def clear(self):
        self.__data.clear()
