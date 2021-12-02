import datetime

from src.domain.RentalValidator import RentalValidator
from src.repository.bookRepository import *
from src.repository.ClientRepository import *
from src.repository.RentalRepository import *
from src.services.rental_service import *
from src.services.book_service import *
from src.services.client_service import *


# todo everything needs to be an object

def test_book_repository():
    book_repository = BookRepository()
    assert len(book_repository) == 0
    carte = Book(1, 'titlu', 'autor')
    book_repository.save(carte)
    assert len(book_repository) == 1

    book_repository.remove(1)

    assert len(book_repository) == 0

    try:
        book_repository.remove(1)
        assert False
    except RepositoryException as re:
        pass

    book_repository.save(carte)

    try:
        book_repository.save(carte)
        assert False
    except RepositoryException as re:
        pass

    carte = Book(2, 'titlu', 'autor')
    book_repository.save(carte)
    assert len(book_repository) == 2

    book_repository.update(1, Book('2', 'new_title', 'new_author',))
    assert book_repository.get_book_by_id(1).title == 'new_title'
    assert book_repository.get_book_by_id(1).author == 'new_author'


def test_client_repository():
    client_repository = ClientRepository()
    assert len(client_repository) == 0
    client = Client(1, 'nume')
    client_repository.save(client)
    assert len(client_repository) == 1

    client_repository.remove(1)

    assert len(client_repository) == 0

    try:
        client_repository.remove(1)
        assert False
    except ClientRepositoryException as cre:
        pass

    client_repository.save(client)

    try:
        client_repository.save(client)
        assert False
    except ClientRepositoryException as cre:
        pass

    client = Client(2, 'nume2')
    client_repository.save(client)
    assert len(client_repository) == 2

    client_repository.update(1, Client(0, 'new_name'))
    assert client_repository.get_client_by_id(1).name == 'new_name'


def test_book_service():
    book_repository = BookRepository()
    book_validator = BookValidator()
    book_service = BookService(book_repository, book_validator)
    assert len(book_service.get_all()) == 0

    book_service.add_book(1, 'title', 'author')

    assert len(book_service.get_all()) == 1

    try:
        book_service.add_book(1, 'title', 'author')
        assert False
    except RepositoryException as re:
        pass

    try:
        book_service.add_book(2, '', '')
        assert False
    except BookValidationException as bve:
        pass

    book_service.change_status(1, True)

    assert book_service.get_book_by_id(1).status == True

    book_service.change_status(1, False)
    assert book_service.get_book_by_id(1).status == False

    try:
        book_service.change_status(500, False)
        assert False
    except RepositoryException as re:
        pass


def test_client_service():
    client_repository = ClientRepository()
    client_validator = ClientValidator()
    client_service = ClientService(client_repository, client_validator)
    assert len(client_service.get_all()) == 0

    client_service.add_client(1, 'nume')

    assert len(client_service.get_all()) == 1

    try:
        client_service.add_client(1, 'nume')
        assert False
    except ClientRepositoryException as re:
        pass

    try:
        client_service.add_client(2, '')
        assert False
    except ClientValidationException as cve:
        pass

    client_service.delete(1)

    assert len(client_service.get_all()) == 0

    client_service.add_random_clients(20)

    assert len(client_service.get_all()) == 20

    try:
        client_service.delete(54)
        assert False
    except ClientRepositoryException as cre:
        pass

    client_service.delete('11')
    client_service.delete('12')
    client_service.delete('13')
    assert len(client_service.get_all()) == 17

    client_service.update(5, 'new_name')
    assert client_service.get_client_by_id(5)


def test_rental_repository():
    rental_repository = RentalRepository()

    assert len(rental_repository.get_all()) == 0
    rental = Rental(2, 3, 4, rented_date=datetime.now().date(),
                    returned_date=datetime.now().date() + timedelta(days=random.randint(0, 7)))
    rental_repository.add_rent(rental)
    assert len(rental_repository.get_all()) == 1

    try:
        rental_repository.add_rent(rental)
        assert False
    except RentalRepositoryException as rre:
        pass

    rental_repository.remove_by_user_id(4)
    assert len(rental_repository.get_all()) == 0

    rental_repository.add_rent(rental)

    rental_repository.remove_by_book_id(4)
    assert len(rental_repository.get_all()) == 1

    rental_repository.remove_by_book_id(3)

    assert len(rental_repository.get_all()) == 0


def test_rental_service():
    books_repository = BookRepository()
    clients_repository = ClientRepository()
    rental_repository = RentalRepository()

    books_validator = BookValidator()
    client_validator = ClientValidator()
    rental_validator = RentalValidator()

    books_service = BookService(books_repository, books_validator)
    client_service = ClientService(clients_repository, client_validator)
    rental_service = RentalService(rental_repository, clients_repository, books_repository, rental_validator)

    assert len(rental_service.get_all()) == 0

    books_service.add_random_books(20)
    client_service.add_random_clients(20)
    rental_service.add_random_rental(10)

    assert len(rental_service.get_all()) == 10

    rental_service.remove_by_book_id(11)
    assert len(rental_service.get_all()) == 10

    rental_service.remove_by_book_id(6)

    assert len(rental_service.get_all()) == 9
    rental_service.remove_by_book_id(2)
    rental_service.remove_by_book_id(3)
    rental_service.remove_by_book_id(4)

    assert len(rental_service.get_all()) == 6

    try:

        rental_service.add_rental(2, 5, '4', rented_date=datetime.now().date(),
                                  returned_date=datetime.now().date() + timedelta(days=random.randint(0, 7)))
        assert False
    except BookAlreadyTakenException:
        pass



def run_all_tests():
    test_book_repository()
    test_client_repository()
    test_book_service()
    test_client_service()
    test_rental_repository()
    test_rental_service()
