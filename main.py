import src.tests.teste
from src.domain.RentalValidator import RentalValidator
from src.repository.bookRepository import *
from src.repository.ClientRepository import *
from src.repository.RentalRepository import *
from src.repository.undoRepository import *
from src.repository.RedoRepository import *
from src.services.book_service import *
from src.services.client_service import *
from src.services.rental_service import *
from src.services.undo_service import *
from src.services.redo_service import *
from src.domain.BookValidator import *
from src.domain.ClientValidator import *
from src.domain.command_pattern import *

from src.ui.console import *
from tkinter import *
from src.ui.gui import *
from src.tests.teste import *


# todo de trecut din ui redo/undo in service undo/redo x
# todo testat undo/redo pe mai multe functionalitati
# todo return a book de trecut cartea pe liber
def main():
    books_repository = BookRepository()
    clients_repository = ClientRepository()
    rental_repository = RentalRepository()
    undo_repository = UndoRepository()
    redo_repository = RedoRepository()

    books_validator = BookValidator()
    client_validator = ClientValidator()
    rental_validator = RentalValidator()

    undo_service = UndoService(undo_repository, redo_repository)
    redo_service = RedoService(redo_repository, undo_repository)
    books_service = BookService(books_repository, books_validator, undo_service, redo_service)
    client_service = ClientService(clients_repository, client_validator, undo_service, redo_service)
    rental_service = RentalService(rental_repository, clients_repository, books_repository, rental_validator,
                                   undo_service, redo_service)

    books_service.add_random_books(20)
    client_service.add_random_clients(20)
    rental_service.add_random_rental(20)

    # src.tests.tests.run_all_tests()

    graphic = gui(books_service, client_service, rental_service, undo_service, redo_service)
    console = ui(books_service, client_service, rental_service, undo_service, redo_service, graphic)

    console.start()


main()
