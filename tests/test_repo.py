import unittest
from src.repository.bookRepository import *
from src.domain.book import *
from src.repository.ClientRepository import *
from src.domain.client import *
from src.repository.RentalRepository import *
from datetime import datetime, timedelta
from src.domain.BookValidator import *
from src.domain.ClientValidator import *
from src.domain.RentalValidator import *
from src.services.book_service import *
from src.services.redo_service import *
from src.services.undo_service import *
from src.services.redo_service import *
from src.repository.undoRepository import *
from src.repository.RedoRepository import *


class BookRepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        '''
        runs before every test method
        :return:
        '''
        pass

    def tearDown(self) -> None:
        '''
        runs after every test method
        :return:
        '''
        pass

    def test_book_repository(self):
        book_repository = BookRepository()
        self.assertEqual(len(book_repository), 0)
        carte = Book(1, 'titlu', 'autor')
        book_repository.save(carte)
        self.assertEqual(len(book_repository), 1)

        book_repository.remove(1)

        self.assertEqual(len(book_repository), 0)

        self.assertRaises(RepositoryException, book_repository.remove, 1)

        book_repository.save(carte)

        with self.assertRaises(RepositoryException):
            book_repository.save(carte)

        carte = Book(2, 'titlu', 'autor')
        book_repository.save(carte)
        self.assertEqual(len(book_repository), 2)
        book_repository.update(1, Book('2', 'new_title', 'new_author', ))

        self.assertEqual(book_repository.get_book_by_id(1).title, 'new_title')
        self.assertEqual(book_repository.get_book_by_id(1).author, 'new_author')


class ClientRepositoryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__client_repository = ClientRepository()

    def test_client_repository(self):
        self.assertEqual(len(self.__client_repository), 0)
        client = Client(1, 'nume')
        self.__client_repository.save(client)
        self.assertEqual(len(self.__client_repository), 1)
        self.__client_repository.remove(1)

        self.assertEqual(len(self.__client_repository), 0)

        with self.assertRaises(ClientRepositoryException):
            self.__client_repository.remove(1)
        self.__client_repository.save(client)

        with self.assertRaises(ClientRepositoryException):
            self.__client_repository.save(client)

        client = Client(2, 'nume2')
        self.__client_repository.save(client)
        self.assertEqual(len(self.__client_repository), 2)
        self.__client_repository.update(1, Client(0, 'new_name'))
        self.assertEqual(self.__client_repository.get_client_by_id(1).name, 'new_name')


class RentalRepositoryTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__rental_repository = RentalRepository()

    def test_rental_repository(self):
        self.assertEqual(len(self.__rental_repository.get_all()), 0)
        rental = Rental(2, 3, 4, rented_date=datetime.now().date(),
                        returned_date=datetime.now().date() + timedelta(days=random.randint(0, 7)))
        self.__rental_repository.add_rent(rental)
        self.assertEqual(len(self.__rental_repository.get_all()), 1)

        with self.assertRaises(RentalRepositoryException):
            self.__rental_repository.add_rent(rental)

        self.__rental_repository.remove_by_user_id(4)
        self.assertEqual(len(self.__rental_repository.get_all()), 0)
        self.__rental_repository.add_rent(rental)

        self.__rental_repository.remove_by_book_id(4)
        self.assertEqual(len(self.__rental_repository.get_all()), 1)

        self.__rental_repository.remove_by_book_id(3)
        self.assertEqual(len(self.__rental_repository.get_all()), 0)


class BookServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__book_repository = BookRepository()
        self.__book_validator = BookValidator()
        self.__undo_repository = UndoRepository()
        self.__redo_repository = RedoRepository()
        self.__undo_service = UndoService(self.__undo_repository, self.__redo_repository)
        self.__redo_service = RedoService(self.__redo_repository, self.__undo_repository)
        self.__book_service = BookService(self.__book_repository, self.__book_validator, self.__undo_service,
                                          self.__redo_service)

    def test_book_service(self):
        self.assertEqual(len(self.__book_service.get_all()), 0)
        self.__book_service.add_book(1, 'title', 'author')

        self.assertEqual(len(self.__book_service.get_all()), 1)

        with self.assertRaises(RepositoryException):
            self.__book_service.add_book(1, 'title', 'author')

        with self.assertRaises(BookValidationException):
            self.__book_service.add_book(2, '', '')

        self.__book_service.change_status(1, True)

        self.assertEqual(self.__book_service.get_book_by_id(1).status, True)
        self.__book_service.change_status(1, False)

        self.assertEqual(self.__book_service.get_book_by_id(1).status, False)

        with self.assertRaises(RepositoryException):
            self.__book_service.change_status(500, False)

        self.assertEqual(self.__book_service.get_most_rented_books()[0].number_of_rents,1)




class ClientServiceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.__client_repository = ClientRepository()
        self.__client_validator = ClientValidator()
        self.__undo_repository = UndoRepository()
        self.__redo_repository = RedoRepository()
        self.__undo_service = UndoService(self.__undo_repository, self.__redo_repository)
        self.__redo_service = RedoService(self.__redo_repository, self.__undo_repository)
        self.__client_service = ClientService(self.__client_repository, self.__client_validator, self.__undo_service,
                                              self.__redo_service)

    def test_client_service(self):
        self.assertEqual(len(self.__client_service.get_all()), 0)
        self.__client_service.add_client(1, 'nume')

        self.assertEqual(len(self.__client_service.get_all()), 1)

        with self.assertRaises(ClientRepositoryException):
            self.__client_service.add_client(1, 'nume')

        with self.assertRaises(ClientValidationException):
            self.__client_service.add_client(2, '')

        self.__client_service.delete(1)

        self.assertEqual(len(self.__client_service.get_all()), 0)

        self.__client_service.add_random_clients(20)

        self.assertEqual(len(self.__client_service.get_all()), 20)

        with self.assertRaises(ClientRepositoryException):
            self.__client_service.delete(54)

        self.__client_service.delete('11')
        self.__client_service.delete('12')
        self.__client_service.delete('13')

        self.assertEqual(len(self.__client_service.get_all()), 17)

        self.__client_service.update(5, 'new_name')
        self.assertEqual(self.__client_service.get_client_by_id(5).name, 'new_name')


class RentalServiceTest(unittest.TestCase):

    def setUp(self) -> None:
        self.__books_repository = BookRepository()
        self.__clients_repository = ClientRepository()
        self.__rental_repository = RentalRepository()
        self.__undo_repository = UndoRepository()
        self.__redo_repository = RedoRepository()

        self.__books_validator = BookValidator()
        self.__client_validator = ClientValidator()
        self.__rental_validator = RentalValidator()

        self.__undo_service = UndoService(self.__undo_repository, self.__redo_repository)
        self.__redo_service = RedoService(self.__redo_repository, self.__undo_repository)
        self.__books_service = BookService(self.__books_repository, self.__books_validator, self.__undo_service,
                                           self.__redo_service)
        self.__client_service = ClientService(self.__clients_repository, self.__client_validator, self.__undo_service,
                                              self.__redo_service)
        self.__rental_service = RentalService(self.__rental_repository, self.__clients_repository,
                                              self.__books_repository, self.__rental_validator,
                                              self.__undo_service, self.__redo_service)

    def test_rental_service(self):
        self.assertEqual(len(self.__rental_service.get_all()), 0)
        self.__books_service.add_random_books(20)
        self.__client_service.add_random_clients(20)
        self.__rental_service.add_random_rental(10)

        self.assertEqual(len(self.__rental_service.get_all()), 10)

        self.__rental_service.remove_by_book_id('11')
        self.assertEqual(len(self.__rental_service.get_all()), 10)
        self.assertEqual(len(self.__rental_service.get_all()), 10)
        self.__rental_service.remove_by_book_id('6')
        self.assertEqual(len(self.__rental_service.get_all()), 9)
        self.__rental_service.remove_by_book_id('2')
        self.__rental_service.remove_by_book_id('3')
        self.__rental_service.remove_by_book_id('4')

        self.assertEqual(len(self.__rental_service.get_all()), 6)

        with self.assertRaises(BookAlreadyTakenException):
            self.__rental_service.add_rental(2, 5, '4', rented_date=datetime.now().date(),
                                             returned_date=datetime.now().date() + timedelta(days=random.randint(0, 7)))

        self.assertEqual(self.__rental_service.get_most_rented_author()[0][0], 'author0')
        self.assertEqual(self.__rental_service.get_most_rented_author()[1][0], 'author1')
        self.assertEqual(self.__rental_service.get_most_rented_author()[2][0], 'author5')
