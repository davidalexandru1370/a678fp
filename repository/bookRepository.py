import string


class RepositoryException(Exception):
    def __init__(self, message):
        # self.__message = 'There exists an item with the same id = ' + str(id) + ' in the repository!'
        self.__message = message
        super().__init__(self.__message)


class BookRepository():
    def __init__(self):
        self.__data = dict()

    def save(self, book):
        '''
        This function save a book in the repository
        :param book: an class element
        :return: nothing
        '''
        if book.id in self.__data:
            raise RepositoryException("There exists an book with the same id = " + str(book.id))
        self.__data[book.id] = book

    def get_all(self):
        '''

        :return: all the values inside the repository as a list
        '''
        return list(self.__data.values())
        # return list(bk[0] for bk in self.__data.values())

    def remove(self, isbn):
        '''
        This function remove a book from repository by id
        :param isbn:  the id of the book to be removed
        :return: nothing
        '''
        if isbn not in self.__data.keys():
            raise RepositoryException('The id=' + str(isbn) + ' does not exist in the repository!')
        del self.__data[isbn]

    def update(self, id, book):
        '''
        This function update a book by its id
        :param id: the id of the book to be updated
        :param book: the new book with new values
        :return: nothing
        '''
        if id not in self.__data.keys():
            raise RepositoryException("The id=" + str(id) + "cannot be updated!")
        else:
            self.__data[id].title = book.title
            self.__data[id].author = book.author

    def __len__(self):
        '''
        :return: the no. of elements inside the repository
        '''
        return len(self.__data)

    def get_book_by_id(self, id):
        '''
        :param id: integer strictly positive representing the id of the book
        :return: the book with that id
        '''
        if id not in self.__data.keys():
            raise RepositoryException('The id = ' + str(id) + ' is not in the repository!')
        else:
            return self.__data[id]

    def get_book_by_title(self, title):
        return list(filter(lambda x: title in x.title.lower(), self.__data.values()))

    def get_book_by_author(self, author):
        return list(filter(lambda x: author in x.author.lower(), self.__data.values()))

    def change_status(self, id, new_status):
        '''
        This function change the status of the book
        :param id: the id of the book to be changed
        :param new_status: 0 representing the book is already rented, 1 represeting is free
        :return:
        '''
        if id not in self.__data.keys():
            raise RepositoryException('The id = ' + str(id) + ' is not found!')
        elif new_status == False:
            self.__data[id].number_of_rents = self.__data[id].number_of_rents + 1

        self.__data[id].status = new_status
