from copy import copy
from copy import deepcopy
import src.repository.bookRepository
import src.repository.ClientRepository
import src.domain.BookValidator
import src.domain.book
import src.domain.ClientValidator
import src.repository.RentalRepository
from src.repository.undoRepository import UndoException
from src.repository.RedoRepository import RedoRepositoryException
from datetime import datetime, timedelta


class ui:
    def __init__(self, book_service, client_service, rental_service, undo_service, redo_service, gui):
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service
        self.__undo_service = undo_service
        self.__redo_service = redo_service
        self.__gui = gui
        self.__commands = {'1': self.ui_add_book, '2': self.ui_remove_book_by_id, '3': self.ui_update_book_by_id,
                           '4': self.display_books, '5': self.ui_add_client, '6': self.ui_remove_client_by_id,
                           '7': self.ui_update_client_by_id, '8': self.display_clients, '9': self.ui_rent_book,
                           '10': self.ui_return_book, '11': self.display_all_rents, '12': self.ui_get_book_by_title,
                           '13': self.ui_get_book_by_author, '14': self.ui_get_client_by_name,
                           '15': self.ui_get_most_rented_books, '16': self.ui_get_most_active_clients,
                           '17': self.ui_get_most_rented_author, '18': self.ui_undo, '19': self.ui_redo,
                           '20': self.open_gui}

    def print_menu(self):
        '''
        This function prints all the menu options
        '''
        print('Press 1 to add a new book')
        print('Press 2 to remove a book by id')
        print('Press 3 to update a book by id')
        print('Press 4 to list all books')
        print('Press 5 to add a new client')
        print('Press 6 to remove a client by id')
        print('Press 7 to update a client by id')
        print('Press 8 to list all clients')
        print('Press 9 to rent a book')
        print('Press 10 to return a book')
        print('Press 11 to show the rented list')
        print('Press 12 to get book by title')
        print('Press 13 to get book by author')
        print('Press 14 to get client by name')
        print('Press 15 to get most rented books')
        print('Press 16 to get most active clients')
        print('Press 17 to get most rented author')
        print('Press 18 to undo the last operation')
        print('Press 19 to redo the last operation')
        print('Press 20 to start the graphical interface')

    def split_statement(self, statement):
        '''
        This function split the statements by comma
        :param statement: string representing the input statement
        :return: a list of each word
        '''
        words = statement.split(',')
        return words

    def remove_multiple_spaces(self, statement):
        words = statement.split()
        statement = ' '.join(words)
        return statement

    def ui_add_book(self):
        '''
        This function add book in the repository from the keyboard
        '''
        print("add,id,title,author")
        statement = input('command=')
        words = self.split_statement(statement)
        # words = self.remove_multiple_spaces(words)
        if len(words) == 4 and words[0] == 'add':
            try:
                words[1] = self.remove_multiple_spaces(words[1])
                # words[3] = ' '.join(words[3].split())
                # words[2] = ' '.join(words[2].split())
                words[3] = self.remove_multiple_spaces(words[3])
                words[2] = self.remove_multiple_spaces(words[2])
                self.__book_service.add_book(words[1], words[2], words[3])
            except src.repository.bookRepository.RepositoryException as re:
                print(str(re))

    def ui_remove_book_by_id(self):
        '''
        This function remove a book by an input statement id
        :return:
        '''
        statement = input('Id of the book to delete =')
        try:
            # deleted = self.__book_service.get_book_by_id(statement)
            self.__rental_service.remove_by_book_id(statement)
            # todo de adaugat undo si la rental
            # if len(deleted_rental) > 0:
            #     self.__undo_service.add_in(self.__rental_service.add_rental, False, deleted_rental[0].rental_id,
            #                                deleted_rental[0].client_id, str(deleted_rental[0].book_id),
            #                                deleted_rental[0].rented_date, deleted_rental[0].returned_date)
            #     self.__undo_service.add_in(self.__book_service.add_book, True, str(deleted.id), deleted.title,
            #                                deleted.author)
        except src.repository.bookRepository.RepositoryException as re:
            print(str(re))
        except src.repository.RentalRepository.RentalRepositoryException as rre:
            pass

    def ui_update_book_by_id(self):
        statement = input('ID of the book to be updated=')
        title = input('new title=')
        author = input('new author=')
        try:
            # old = self.__book_service.get_book_by_id(statement)
            # old_title = old.title
            # old_author = old.author
            self.__book_service.update(statement, title, author)
            # self.__undo_service.add_in(self.__book_service.update, old.id, old_title, old_author)
            # because python side effect
        except src.repository.bookRepository.RepositoryException as re:
            print(re)

    def display_books(self, book_list=None):
        '''
        Prints all the books in the repository
        :return:
        '''
        # for key in self.__service.get_all()):
        #     print('Id=' + str(self.__books[key].isbn) + ' title is =' + str(
        #         self.__books[key].title) + ' and author is = ' + str(self.__books[key].author))
        if book_list is None:
            book_list = self.__book_service.get_all()

        for book in book_list:
            print('Id is = ' + str(book.id) + ' Title is =' + str(book.title) + ' author is =' + str(
                book.author) + ' available for rent = ' + str(
                'True' if book.status == 1 else 'False') + ' and number of rents = ' + str(book.number_of_rents))

    def ui_get_book_by_title(self):
        title = input('title=')
        title = self.remove_multiple_spaces(title)
        self.display_books(self.__book_service.get_book_by_title(title.lower()))

    def ui_get_book_by_author(self):
        author = input('author=')
        author = self.remove_multiple_spaces(author)
        self.display_books(self.__book_service.get_book_by_author(author.lower()))

    def ui_add_client(self):
        print('add,id,name')
        statement = input('command=')
        words = self.split_statement(statement)
        if len(words) == 3 and words[0] == 'add':
            try:
                # words[2] = ' '.join(words[2].split())
                for index in range(0, len(words)):
                    words[index] = self.remove_multiple_spaces(words[index])
                self.__client_service.add_client(words[1], words[2])
            except src.repository.ClientRepository.ClientRepositoryException as cre:
                print(str(cre))

    def ui_remove_client_by_id(self):
        statement = input('Id of the user to be deleted=')
        try:
            # todo pus client_Service.delete in rental_service
            self.__rental_service.remove_by_user_id(statement)
        except src.repository.ClientRepository.ClientRepositoryException as cre:
            print(str(cre))

    def ui_update_client_by_id(self):
        new_id = input('id of the user to be updated =')
        new_name = input('new name =')
        try:
            self.__client_service.update(new_id, new_name)
        except src.repository.ClientRepository.ClientRepositoryException as cle:
            print(str(cle))
        except src.domain.ClientValidator.ClientValidationException as cve:
            print(str(cve))

    def display_clients(self, client_list=None):

        if client_list is None:
            client_list = self.__client_service.get_all()

        for client in client_list:
            print('Client with id= ', str(client.id), ' and name = ', client.name)

    def ui_get_most_active_clients(self):
        # self.display_clients()
        for client in self.__rental_service.get_most_active_clients():
            print('Client with id = ' + str(client[0]) + ' has ' + str(client[1]) + ' book rental days!')

    def ui_get_most_rented_author(self):
        for author in self.__rental_service.get_most_rented_author():
            print('Author = ' + str(author[0]) + ' has ' + str(author[1]) + ' rented books ')

    def ui_get_client_by_name(self):
        statement = input('name=')
        statement = self.remove_multiple_spaces(statement)
        self.display_clients(self.__client_service.get_client_by_name(statement.lower()))

    def ui_rent_book(self):
        rental_id = input('rental id=')
        user_id = input('user id=')
        book_id = input('book id=')
        try:
            self.__rental_service.add_rental(rental_id, user_id, book_id, datetime.now().date(),
                                             datetime.now().date() + timedelta(days=2))
        except src.domain.book.BookAlreadyTakenException as bat:
            print(str(bat))
        except KeyError as ke:

            print("The client or the book does not exist!")
        except src.repository.RentalRepository.RentalRepositoryException as rre:
            print(str(rre))

    def ui_return_book(self):
        book_id = input('book id =')
        try:
            self.__rental_service.remove_by_book_id(book_id)
            # self.__book_service.remove_by_id(book_id)
            self.__book_service.change_status(book_id, 1)

        except src.repository.bookRepository.RepositoryException as re:
            pass

    def display_all_rents(self):
        for rent in self.__rental_service.get_all():
            print('User with id = ' + rent.client_id + ' rented book with id = ' + rent.book_id + ' in date = ' + str(
                rent.rented_date) + ' expiration date =' + str(rent.returned_date))

    def ui_get_most_rented_books(self):
        self.display_books(self.__book_service.get_most_rented_books())

    def ui_undo(self):
        try:
            self.__undo_service.pop_out()
        except UndoException as ue:
            print(ue)

    def ui_redo(self):
        try:
            self.__redo_service.pop_out()
        except RedoRepositoryException as rre:
            print(rre)

    def open_gui(self):
        self.__gui.start()

    def start(self):

        while True:
            self.print_menu()
            _command = input('your choose=').lower()
            if _command not in self.__commands:
                print("invalid menu!")
                continue
            try:
                self.__commands[_command]()
            except KeyError as ke:
                print('error = ' + str(ke))
