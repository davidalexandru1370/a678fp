import datetime
import random
from src.domain.rental import *


class RentalRepositoryException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RentalRepository:
    def __init__(self):
        # self.__data = dict(list())
        self.__data = list()

    def add_rent(self, rental):
        '''
        This function add a new rent into the repository
        :param rental: rent class with associated values
        :return:
        '''

        # self.__data[rental.rental_id].append(rental)
        for item in self.__data:
            if item.rental_id == rental.rental_id:
                raise RentalRepositoryException(
                    'An rent with this id = ' + str(rental.rental_id) + ' is already in the list')
        self.__data.append(rental)

    def get_all(self):
        '''

        :return: the elements inside the repository as a list
        '''
        return self.__data

    def remove_by_user_id(self, id):
        '''
        This function removes the rents by the user id
        :param id: id of the user to be deleted
        :return: a new list with deleted items in order to delete their associated data further
        '''
        # trebe sa returnez ce am sters sa stiu  ce carti sa le trec pe liber

        filtered = list(filter(lambda item: item.client_id == id, self.__data))
        new_list = list(filter(lambda item: item.client_id != id, self.__data))
        self.__data = new_list[:]
        return filtered

    def remove_by_book_id(self, id):
        '''
        Remove a rent by book id
        :param id: the id of the book to be removed
        :return: nothing
        '''
        filtered = list(filter(lambda item: item.book_id != id, self.__data))
        deleted = list(filter(lambda item: item.book_id == id, self.__data))
        self.__data = filtered[:]
        return deleted
