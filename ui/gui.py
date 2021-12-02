import datetime
import tkinter.ttk
from tkinter import *
from functools import partial

import src.repository.bookRepository
from src.domain.book import *
import src.domain.BookValidator
from src.domain.rental import *
from src.domain.client import *
from src.repository.bookRepository import *
import tkinter as tk
from tkinter import ttk
import src.repository.ClientRepository
from src.repository.ClientRepository import ClientRepositoryException
import src.domain.ClientValidator
import src.repository.RentalRepository
import src.domain.RentalValidator
import src.domain.book
from src.domain.ClientValidator import ClientValidationException
from src.domain.BookValidator import BookValidationException
from datetime import datetime, timedelta


class gui:
    def __init__(self, book_service, client_service, rental_service, undo_service, redo_service):
        self.__book_service = book_service
        self.__client_service = client_service
        self.__rental_service = rental_service
        self.__undo_service = undo_service
        self.__redo_service = redo_service
        self.__root = Tk()
        self.__treeview = None
        self.__add_widgets = []
        self.__add_labels = []
        self.__message_label = Label()
        self.__listbox_name_label = Label()
        self.__previous_items = []

    def gui_add_new_book(self):

        self.delete_add_text_boxes()

        id_textbox = Text(self.__root, bg='grey', height=1, width=27)
        id_textbox.place(x=300, y=20)
        id_label = Label(self.__root, text='Id:')
        id_label.place(x=265, y=20)

        title_textbox = Text(self.__root, bg='grey', height=1, width=27)
        title_textbox.place(x=300, y=70)
        title_label = Label(self.__root, text='Title:')
        title_label.place(x=265, y=70)

        author_textbox = Text(self.__root, bg='grey', height=1, width=27)
        author_textbox.place(x=300, y=120)
        author_label = Label(self.__root, text='author')
        author_label.place(x=255, y=120)

        self.__add_widgets.append(Book)
        self.__add_widgets.append(id_textbox)
        self.__add_widgets.append(title_textbox)
        self.__add_widgets.append(author_textbox)

        self.__add_labels.append(id_label)
        self.__add_labels.append(author_label)
        self.__add_labels.append(title_label)

    def gui_add_new_client(self):
        self.delete_add_text_boxes()

        id_textbox = Text(self.__root, bg='grey', height=1, width=27)
        id_textbox.place(x=300, y=20)
        id_label = Label(self.__root, text='Id:')
        id_label.place(x=250, y=20)

        name_textbox = Text(self.__root, bg='grey', height=1, width=27)
        name_textbox.place(x=300, y=70)
        name_label = Label(self.__root, text='name:')
        name_label.place(x=250, y=70)

        self.__add_widgets.append(Client)
        self.__add_widgets.append(id_textbox)
        self.__add_widgets.append(name_textbox)
        self.__add_labels.append(id_label)

        self.__add_labels.append(id_label)
        self.__add_labels.append(name_label)

    def gui_add_new_rental(self):
        self.delete_add_text_boxes()

        id_textbox = Text(self.__root, bg='grey', height=1, width=27)
        id_textbox.place(x=300, y=20)
        id_label = Label(self.__root, text='Id:')
        id_label.place(x=250, y=20)

        user_id_textbox = Text(self.__root, bg='grey', height=1, width=27)
        user_id_textbox.place(x=300, y=70)
        user_id_label = Label(self.__root, text='user id:')
        user_id_label.place(x=250, y=70)

        book_id_textbox = Text(self.__root, bg='grey', height=1, width=27)
        book_id_textbox.place(x=300, y=120)
        book_id_label = Label(self.__root, text='book id:')
        book_id_label.place(x=250, y=120)

        self.__add_widgets.append(Rental)
        self.__add_widgets.append(id_textbox)
        self.__add_widgets.append(user_id_textbox)
        self.__add_widgets.append(book_id_textbox)

        self.__add_labels.append(id_label)
        self.__add_labels.append(user_id_label)
        self.__add_labels.append(book_id_label)

    def gui_execute_command(self):
        if len(self.__add_widgets) == 0:
            return
        if self.__message_label is not None:
            self.__message_label.destroy()
        label = None
        if self.__add_widgets[0] == Book:
            try:
                self.__book_service.add_book(str(self.__add_widgets[1].get(1.0, "end-1c")),
                                             self.__add_widgets[2].get(1.0, 'end-1c'),
                                             self.__add_widgets[3].get(1.0, 'end-1c'))
            except src.repository.bookRepository.RepositoryException as re:
                label = Label(self.__root, text=str(re), fg='red')
            except src.domain.BookValidator.BookValidationException as vde:
                label = Label(self.__root, text=str(vde), fg='red')
            finally:
                if label is None:
                    label = Label(self.__root, text='Added succesfully', fg='green')
                self.__message_label = label
                self.__message_label.place(x=400, y=160)

        elif self.__add_widgets[0] == Client:
            try:
                self.__client_service.add_client(str(self.__add_widgets[1].get(1.0, 'end-1c')),
                                                 self.__add_widgets[2].get(1.0, 'end-1c'))
            except src.domain.ClientValidator.ClientValidationException as cve:
                label = Label(self.__root, text=str(cve), fg='red')
            except src.repository.ClientRepository.ClientRepositoryException as cre:
                label = Label(self.__root, text=str(cre), fg='red')
            finally:
                if label is None:
                    label = Label(self.__root, text='Client added succesfully!', fg='green')
                self.__message_label = label
                self.__message_label.place(x=300, y=160)

        elif self.__add_widgets[0] == Rental:
            try:
                self.__rental_service.add_rental(str(self.__add_widgets[1].get(1.0, 'end-1c')),
                                                 str(self.__add_widgets[2].get(1.0, 'end-1c')),
                                                 str(self.__add_widgets[3].get(1.0, 'end-1c')), datetime.now().date(),
                                                 datetime.now().date() + timedelta(days=2))
            except src.domain.book.BookAlreadyTakenException as bate:
                label = Label(self.__root, text=str(bate), fg='red')
            except RepositoryException as re:
                label = Label(self.__root, text=re, fg='red')
            except src.repository.RentalRepository.RentalRepositoryException as rre:
                label = Label(self.__root, text=str(rre), fg='red')
            finally:
                if label is None:
                    label = Label(self.__root, text='Rental added succesfully!', fg='green')
                self.__message_label = label
                self.__message_label.place(x=250, y=170)

    def gui_show_books(self):
        columns = ('id', 'title', 'author')
        self.generate_list_view(list((book.id, book.title, book.author) for book in self.__book_service.get_all()),
                                columns, 'books')

    def gui_show_clients(self):
        columns = ('id', 'name')
        self.generate_list_view(list((client.id, client.name) for client in self.__client_service.get_all()), columns,
                                'clients')

    def gui_show_rentals(self):
        columns = ('rental id', 'client id', 'book id')
        self.generate_list_view(list(
            (rental.rental_id, rental.client_id, rental.book_id, rental.rented_date, rental.returned_date) for rental in
            self.__rental_service.get_all()), columns, 'rentals')

    def gui_get_most_rented_books(self):
        columns = ('id', 'title', 'author', 'rents')
        data = list(
            (book.id, book.title, book.author, book.number_of_rents) for book in
            self.__book_service.get_most_rented_books())
        self.generate_list_view(data, columns, "most rented books")

    def gui_get_most_active_clients(self):
        columns = ('Client Id', 'Rented days')
        self.generate_list_view(self.__rental_service.get_most_active_clients(), columns, 'Most active clients')

    def generate_list_view(self, data, columns, message):

        if self.__treeview is not None:
            self.__treeview.destroy()
        treeview = tkinter.ttk.Treeview(self.__root, column=columns, show='headings', height=5)
        for item in columns:
            treeview.column(item, anchor=CENTER, width=80, stretch=YES)
            treeview.heading(item, text=item)
        listbox_name_label = Label(self.__root, text=message)
        for element in data:
            treeview.insert('', tk.END, values=element)
        if self.__listbox_name_label is not None:
            self.__listbox_name_label.destroy()
        self.__listbox_name_label = listbox_name_label
        self.__listbox_name_label.place(x=220, y=280)
        treeview.place(x=200, y=300)
        self.__treeview = treeview

    def gui_search_for_book(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Book)
        search_text = Text(self.__root, bg='grey', height=1, width=27)
        search_text.place(x=300, y=20)
        self.__previous_items.append(search_text)

        listbox = Listbox(self.__root, width=20, height=10, selectmode=SINGLE)
        listbox.insert(1, 'id')
        listbox.insert(2, 'title')
        listbox.insert(3, 'author')
        listbox.place(x=300, y=50)
        self.__previous_items.append(listbox)

    def gui_search(self):
        index = self.__previous_items[2].curselection()
        if len(index) == 0:
            return
        if self.__message_label is not None:
            self.__message_label.destroy()
        if self.__previous_items[0] == Book:

            try:
                columns = ('id', 'title', 'author')
                book = Book
                if index[0] == 0:
                    book = self.__book_service.get_book_by_id(str(self.__previous_items[1].get(1.0, 'end-1c')))
                elif index[0] == 1:
                    book = self.__book_service.get_book_by_title(str(self.__previous_items[1].get(1.0, 'end-1c')))
                elif index[0] == 2:
                    book = self.__book_service.get_book_by_author(str(self.__previous_items[1].get(1.0, 'end-1c')))
                if type(book) == list:
                    self.generate_list_view(list((bk.id, bk.author, bk.title) for bk in book), columns, 'searched book')
                else:
                    self.generate_list_view(((book.id, book.author, book.title),), columns, 'searched book')
            except BookRepository as bk:
                print(bk)
        elif self.__previous_items[0] == Client:
            try:
                columns = ('id', 'name')
                client = Client
                if index[0] == 0:
                    client = self.__client_service.get_client_by_id(str(self.__previous_items[1].get(1.0, 'end-1c')))
                if index[0] == 1:
                    client = self.__client_service.get_client_by_name(str(self.__previous_items[1].get(1.0, 'end-1c')))
                if type(client) == list:
                    self.generate_list_view(list((cl.id, cl.name) for cl in client), columns,
                                            'searched client')
                else:
                    self.generate_list_view(((client.id, client.name),), columns, 'searched client')
            except ClientRepositoryException as cle:
                print(cle)

    def gui_search_for_client(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Client)
        search_text = Text(self.__root, bg='grey', height=1, width=27)
        search_text.place(x=300, y=20)
        self.__previous_items.append(search_text)

        listbox = Listbox(self.__root, width=20, height=10, selectmode=SINGLE)
        listbox.insert(1, 'id')
        listbox.insert(2, 'name')
        listbox.place(x=300, y=50)
        self.__previous_items.append(listbox)

    def gui_delete_book(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Book)
        delete_text = Text(self.__root, bg='grey', height=1, width=27)
        delete_text.place(x=300, y=20)
        self.__previous_items.append(delete_text)

    def delete(self):
        message = None
        if self.__message_label is not None:
            self.__message_label.destroy()
        if len(self.__previous_items) == 0:
            return
        try:
            if self.__previous_items[0] == Book:
                self.__rental_service.remove_by_book_id(str(self.__previous_items[1].get(1.0, 'end-1c')))
            elif self.__previous_items[0] == Client:
                self.__rental_service.remove_by_user_id(str(self.__previous_items[1].get(1.0, 'end-1c')))
            self.__message_label = Label(self.__root, fg='green', text='Deleted succesfully!')
        except RepositoryException as bk:
            message = bk
        except ClientRepositoryException as cre:
            message = cre

        if message is None:
            self.__message_label = Label(self.__root, fg='red', text=message)

        self.__message_label.place(x=300, y=50)

    def gui_delete_client(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Client)
        delete_text = Text(self.__root, bg='grey', height=1, width=27)
        delete_text.place(x=300, y=20)
        self.__previous_items.append(delete_text)

    def update(self):
        message = None
        if self.__message_label is not None:
            self.__message_label.destroy()
        if len(self.__previous_items) == 0:
            return
        try:
            if self.__previous_items[0] == Book:
                aidi = str(self.__previous_items[1].get(1.0, 'end-1c'))
                new_title = self.__previous_items[2].get(1.0, 'end-1c')
                new_author = self.__previous_items[3].get(1.0, 'end-1c')
                self.__book_service.update(aidi, new_title, new_author)
            if self.__previous_items[0] == Client:
                aidi = str(self.__previous_items[1].get(1.0, 'end-1c'))
                new_name = self.__previous_items[2].get(1.0, 'end-1c')
                self.__client_service.update(aidi, new_name)
            self.__message_label = Label(self.__root, fg='green', text='Updated Succesfully')
        except RepositoryException as re:
            message = str(re)
        except BookValidationException as bve:
            message = str(bve)
        except ClientRepositoryException as cre:
            message = str(cre)
        except ClientValidationException as cve:
            message = str(cve)

        if message is not None:
            self.__message_label = Label(self.__root, fg='red', text=message)
        self.__message_label.place(x=300, y=150)

    def gui_update_book(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Book)

        id_to_update_text = Text(self.__root, bg='grey', height=1, width=27)
        id_to_update_text.place(x=300, y=20)
        self.__previous_items.append(id_to_update_text)

        new_title_text = Text(self.__root, bg='grey', height=1, width=27)
        new_title_text.place(x=300, y=70)
        self.__previous_items.append(new_title_text)

        new_author_text = Text(self.__root, bg='grey', height=1, width=27)
        new_author_text.place(x=300, y=120)
        self.__previous_items.append(new_author_text)

        id_label = Label(self.__root, text='Id')
        id_label.place(x=250, y=20)
        self.__previous_items.append(id_label)

        title_label = Label(self.__root, text='new title')
        title_label.place(x=200, y=70)
        self.__previous_items.append(title_label)

        author_label = Label(self.__root, text='new author')
        author_label.place(x=200, y=120)
        self.__previous_items.append(author_label)

    def gui_update_client(self):
        self.delete_add_text_boxes()
        self.__previous_items.append(Client)

        id_to_update_text = Text(self.__root, bg='grey', height=1, width=27)
        id_to_update_text.place(x=300, y=20)
        self.__previous_items.append(id_to_update_text)

        new_name_text = Text(self.__root, bg='grey', height=1, width=27)
        new_name_text.place(x=300, y=70)
        self.__previous_items.append(new_name_text)

        id_label = Label(self.__root, text='Id')
        id_label.place(x=250, y=20)
        self.__previous_items.append(id_label)

        name_label = Label(self.__root, text='new name')
        name_label.place(x=200, y=70)
        self.__previous_items.append(name_label)

    def generate_buttons(self):
        add_book_button = Button(self.__root, text='Add a new book', command=self.gui_add_new_book)
        add_book_button.place(x=50, y=20)

        add_client_button = Button(self.__root, text='Add new client', command=self.gui_add_new_client)
        add_client_button.place(x=50, y=70)

        add_rental_button = Button(self.__root, text="Add new rental", command=self.gui_add_new_rental)
        add_rental_button.place(x=50, y=120)

        show_books_button = Button(self.__root, text='Show books', command=self.gui_show_books)
        show_books_button.place(x=210, y=250)

        show_clients_button = Button(self.__root, text='Show clients', command=self.gui_show_clients)
        show_clients_button.place(x=290, y=250)

        show_rentals_button = Button(self.__root, text='Show rentals', command=self.gui_show_rentals)
        show_rentals_button.place(x=380, y=250)

        most_rented_books_button = Button(self.__root, text='Show most rented books',
                                          command=self.gui_get_most_rented_books)
        most_rented_books_button.place(x=480, y=250)

        most_active_clients_button = Button(self.__root, text='Show most active clients',
                                            command=self.gui_get_most_active_clients)
        most_active_clients_button.place(x=650, y=250)

        add_button = Button(self.__root, text='add', command=self.gui_execute_command)
        add_button.place(x=580, y=20)

        search_button = Button(self.__root, text='search', command=self.gui_search)
        search_button.place(x=580, y=50)

        delete_button = Button(self.__root, text='delete', command=self.delete)
        delete_button.place(x=580, y=80)

        update_button = Button(self.__root, text='update', command=self.update)
        update_button.place(x=580, y=110)

        search_for_book_button = Button(self.__root, text='search for a book', command=self.gui_search_for_book)
        search_for_book_button.place(x=50, y=170)

        search_for_client_button = Button(self.__root, text='search for a client', command=self.gui_search_for_client)
        search_for_client_button.place(x=50, y=220)

        delete_book_button = Button(self.__root, text='delete book by id', command=self.gui_delete_book)
        delete_book_button.place(x=50, y=270)

        delete_client_button = Button(self.__root, text='delete by client id', command=self.gui_delete_client)
        delete_client_button.place(x=50, y=320)

        update_book_button = Button(self.__root, text='update book', command=self.gui_update_book)
        update_book_button.place(x=50, y=370)

        update_client_button = Button(self.__root, text='update client', command=self.gui_update_client)
        update_client_button.place(x=50, y=420)

    def delete_add_text_boxes(self):
        if self.__message_label is not None:
            self.__message_label.destroy()
            self.__message_label = None

        for index in range(1, len(self.__previous_items)):
            self.__previous_items[index].destroy()

        self.__previous_items.clear()

        for index in range(1, len(self.__add_widgets)):
            self.__add_widgets[index].destroy()

        for index in range(0, len(self.__add_labels)):
            self.__add_labels[index].destroy()

        self.__add_widgets.clear()
        self.__add_labels.clear()

    def start(self):
        self.__root.title = 'Library FP'
        self.__root.geometry("960x480")

        self.generate_buttons()

        self.__root.mainloop()
