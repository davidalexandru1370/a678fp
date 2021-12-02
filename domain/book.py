class BookAlreadyTakenException(Exception):
    def __init__(self, message):
        super().__init__(message)


class Book:
    def __init__(self, book_id, title, author):
        self.__book_id = book_id
        self.__book_title = title
        self.__book_author = author
        self.__status = 1
        self.__number_of_rents = 0

    @property
    def id(self):
        return self.__book_id

    @property
    def title(self):
        return self.__book_title

    @title.setter
    def title(self, value):
        self.__book_title = value

    @property
    def author(self):
        return self.__book_author

    @author.setter
    def author(self, value):
        self.__book_author = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        self.__status = value

    @property
    def number_of_rents(self):
        return self.__number_of_rents

    @number_of_rents.setter
    def number_of_rents(self, value):
        self.__number_of_rents = value
