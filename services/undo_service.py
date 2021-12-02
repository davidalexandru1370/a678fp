from src.domain.command_pattern import *
import functools
from src.services.book_service import *
from src.domain.command_pattern import *
from src.services.rental_service import *
from src.services.client_service import *
import unittest


class UndoService:
    def __init__(self, undo_repository, redo_repository):
        self.__data = undo_repository
        self.__redo_repository = redo_repository

    def add_in(self, function_undo, down_undo: bool, parameters_undo: tuple, function_redo, down_redo: bool,
               parameters_redo: tuple):
        undo_operation = undo(function_undo, *parameters_undo)
        redo_operation = undo(function_redo, *parameters_redo)
        self.__data.add_operation(undo_operation, down_undo, redo_operation, down_redo)

    def pop_out(self):
        next = True
        operations = []
        while next == True:
            operation, down_undo, redo, down_redo = self.__data.pop_operation()
            next = down_undo
            if operation.function is not None:
                execute = functools.partial(operation.function, *operation.parameters)
                execute()
            operations.append((operation, down_undo, redo, down_redo))

        for index in range(len(operations) - 1, -1, -1):
            self.__redo_repository.add_in(operations[index][2], operations[index][3], operations[index][0],
                                          operations[index][1])
