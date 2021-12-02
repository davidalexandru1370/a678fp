from datetime import datetime, timedelta
import random

import src.domain.book
from src.domain.book import *
from src.domain.rental import *
import src.domain.client
import src.domain.client


class RentalService:
    def __init__(self, repository, client_repository, book_repository, validator, undo_service, redo_service):
        self.__repository = repository
        self.__client_repository = client_repository
        self.__book_repository = book_repository
        self.__validator = validator
        self.__undo_service = undo_service
        self.__redo_service = redo_service

    def add_rental(self, rental_id, client_id, book_id, rented_date, returned_date):
        '''
        This function add a new rental
        :param rental_id: integer stricly positive reprensenting the rental id
        :param client_id: integer strictly positive representing the client id
        :param book_id: integer strictly positive reprenseting the book id
        :param rented_date: the date of today
        :param returned_date: datetime.date representing the returning date
        :return:
        '''
        rental = Rental(rental_id, book_id, client_id, rented_date, returned_date)
        self.__validator.validate(rental)
        if self.__book_repository.get_book_by_id(book_id).status == 0:
            raise src.domain.book.BookAlreadyTakenException('Book already taken')
        elif self.__client_repository.get_client_by_id(client_id):
            self.__redo_service.clear()
            self.__book_repository.change_status(book_id, 0)
            self.__repository.add_rent(rental)
            self.__undo_service.add_in(self.__book_repository.change_status, False, (str(book_id), 1),
                                       self.__book_repository.change_status, False, (str(book_id), 0))
            book = self.__book_repository.get_book_by_id(book_id)
            self.__undo_service.add_in(self.__repository.remove_by_book_id, True, (str(book_id),),
                                       self.__repository.add_rent, True,
                                       (Rental(rental.rental_id, rental.book_id, rental.client_id, rental.rented_date,
                                               rental.returned_date),))

    def add_random_rental(self, count):
        '''
        This function add random rentals into the repository
        :param count: integer strictly positive reprensenting the no. of random rentals
        :return:
        '''
        for index in range(0, 10):
            book_id = str(index)
            client_id = str(random.randint(0, 19))
            rented_date = datetime.now().date()
            returned_date = datetime.now().date() + timedelta(days=random.randint(0, 7))
            self.add_rental(str(index), client_id, book_id, rented_date, returned_date)

    def get_all(self):
        '''
        :return: the values stored in the repository
        '''
        return self.__repository.get_all()

    def remove_by_user_id(self, id):
        '''
        This function remove all the rents made by an user id
        :param id: the id of the user to be deleted
        :return:
        '''

        deleted = self.__repository.remove_by_user_id(id)
        # for item in deleted:
        client = self.__client_repository.get_client_by_id(id)
        client = src.domain.client.Client(client.id, client.name)
        self.__client_repository.remove(id)
        self.__redo_service.clear()
        if len(deleted) > 0:
            for index in range(0, len(deleted)):
                self.__book_repository.change_status(deleted[index].book_id, 1)
                self.__undo_service.add_in(self.__book_repository.change_status,
                                           False if index == 0 else True, (deleted[index].book_id, 0),
                                           self.__book_repository.change_status,
                                           False if index == 0 else True, (deleted[index].book_id, 1))

                self.__undo_service.add_in(None, True, (), self.__repository.remove_by_user_id, True, (str(id),))
                self.__undo_service.add_in(self.__repository.add_rent, True,
                                           (deleted[index],), self.__client_repository.remove, True, (str(id),))

        # print('len deleted = ',len(deleted))
        self.__undo_service.add_in(self.__client_repository.save, False if len(deleted) == 0 else True, (client,),
                                   self.__client_repository.remove, False if len(deleted) == 0 else True, (id,))

    def remove_by_book_id(self, id):
        '''
        This function remove the rents by id book and also the book
        :param id: the id of the book to be deleted
        :return:
        '''
        deleted = self.__book_repository.get_book_by_id(id)
        deleted = Book(str(deleted.id), deleted.title, deleted.author)
        self.__book_repository.remove(id)
        deleted_rentals = self.__repository.remove_by_book_id(id)
        if len(deleted_rentals) > 0:
            self.__redo_service.clear()
            for deleted_rental in deleted_rentals:
                self.__undo_service.add_in(self.__repository.add_rent, False,
                                           (deleted_rental,), self.__book_repository.remove, False, (str(id),))
                self.__undo_service.add_in(self.__book_repository.save, True, (deleted,),
                                           self.__repository.remove_by_book_id, True, (str(id),))
            # print('len deleted = ',len(deleted))

    def get_most_active_clients(self):
        '''
        This function get most active clients
        :return: a list with most active clients in sorted in descending order
        '''
        most_active_users = set()
        for client in self.__repository.get_all():
            occurences = list(filter(lambda x: x.client_id == client.client_id, self.__repository.get_all()))
            total_days = sum((x.returned_date - x.rented_date).days for x in occurences)
            most_active_users.add((client.client_id, total_days))

        return sorted(most_active_users, key=lambda x: x[1], reverse=True)

    def get_most_rented_author(self):
        '''
        This function get the most rented author
        :return: a list with most rented author sorted in descending order by the number of rents
        '''
        most_rented_author = dict()
        for book in self.__repository.get_all():
            author = self.__book_repository.get_book_by_id(book.book_id).author
            if author not in most_rented_author.keys():
                most_rented_author[author] = 1
            else:
                most_rented_author[author] = most_rented_author[author] + 1

        return sorted(most_rented_author.items(), key=lambda x: x[1], reverse=True)
