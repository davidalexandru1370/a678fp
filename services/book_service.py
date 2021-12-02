import copy

from src.repository.bookRepository import *
from src.domain.book import *
from src.domain.BookValidator import *


class BookService:
    def __init__(self, repository, validator, undo_service, redo_service):
        self.__repository = repository
        self.__validator = validator
        self.__undo_service = undo_service
        self.__redo_service = redo_service

    def add_book(self, id, title, author):
        '''
        This function validates and add a book inside the repository
        :param id: integer number strictly positive and unique representing id of the book
        :param title: string representing the title of the book
        :param author: string representing the book author
        :return:
        '''
        book = Book(id, title, author)
        self.__validator.validate(book)
        self.__repository.save(book)
        # self.__undo_service.add_in(self.remove_by_id, False, book.id,)
        self.__redo_service.clear()
        self.__undo_service.add_in(self.__repository.remove, False, (book.id,), self.__repository.save, False,
                                   (Book(book.id, book.title, book.author),))


    def get_all(self):
        '''
        :return: all the values stored in the repository
        '''
        return self.__repository.get_all()

    def add_random_books(self, count):
        '''
        :param count: integer number strictly positive representing the no. of books to be added random
        :return:
        '''
        for index in range(0, count):
            self.add_book(str(index), 'title' + str(index), 'author' + str(index))

    def remove_by_id(self, id):
        '''
        This function remove a book by his id
        :param id: integer stricly positive reprensenting the id of the book to be deteled
        :return:
        '''
        old_book = self.get_book_by_id(id)
        self.__repository.remove(id)
        self.__redo_service.clear()
        self.__undo_service.add_in(self.__repository.save, False, (Book(old_book.id, old_book.title, old_book.author),),
                                   self.__repository.remove, False, (id,))
        # delete rental with this book

    def update(self, id, title, author):
        '''
        Update a book stored in the repository with new values
        :param id: id the book to be updated
        :param title: string representing the new title
        :param author: string representing the new author
        :return:
        '''
        book = Book(id, title, author)
        self.__validator.validate(book)
        old_book = self.get_book_by_id(id)
        old_book = Book(old_book.id, old_book.title, old_book.author)
        self.__repository.update(id, book)
        self.__redo_service.clear()
        self.__undo_service.add_in(self.__repository.update, False, (id, old_book), self.__repository.update, False, (id,
                                   Book(book.id, book.title, book.author)))

    def get_book_by_id(self, id):
        '''
        Return the book with id
        :param id: integer strictly positive representing the book id
        :return: the book with given id
        '''
        return self.__repository.get_book_by_id(id)

    def get_book_by_title(self, title):
        '''
        :param title: a string representing the book title
        :return: the book that contains the given title
        '''
        return self.__repository.get_book_by_title(title)

    def get_book_by_author(self, author):
        '''
        :param author:
        :return:
        '''
        return self.__repository.get_book_by_author(author)

    def change_status(self, id, new_value):
        '''
        Function that change the status of a book stored in repository
        :param id: the id of the book to be changed
        :param new_value: integer, 0 representing the book is taken, 1 representing the book is available to be rented
        :return:
        '''
        self.__repository.change_status(id, new_value)

    def get_most_rented_books(self):
        '''
        THis function returs the most rented books sorted by number of rents
        :return: a list with most rennted books in descending order
        '''
        return sorted(self.get_all(), key=lambda x: x.number_of_rents, reverse=True)
