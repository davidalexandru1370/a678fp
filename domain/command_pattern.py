from typing import Callable
import functools

class undo:
    def __init__(self, function, *function_parameters):
        self.__function = function
        self.__function_parameters = function_parameters


    @property
    def function(self):
        return self.__function
    

    @property
    def parameters(self):
        return self.__function_parameters
