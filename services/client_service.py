from src.domain.ClientValidator import *
from src.domain.client import *


class ClientService:
    def __init__(self, repository, validator, undo_service, redo_service):
        self.__repository = repository
        self.__validator = validator
        self.__undo_service = undo_service
        self.__redo_service = redo_service

    def add_client(self, id, name):
        '''
        This function validdate and add a new client into the repository
        :param id: integer strictly positive and unique representing the id of client to be added
        :param name: string representing the name of the user
        :return:
        '''
        client = Client(id, name)
        self.__validator.validate(client)
        self.__repository.save(client)
        self.__redo_service.clear()
        self.__undo_service.add_in(self.__repository.remove, False, (id,), self.__repository.save, False,
                                   (Client(id, name),))

    def delete(self, id):
        '''
        This function delete a user by his id
        :param id: the id of user to be deleted
        :return:
        '''
        # delete the user
        # delete the rental with user
        self.__repository.remove(id)

    def add_random_clients(self, count):
        '''
        this function add random clients into the repository
        :param count: integer stricly positive representing the number of random clients to be added
        :return:
        '''
        for index in range(0, count):
            self.add_client(str(index), 'client' + str(index))

    def get_all(self):
        '''
        :return: all the clients stored in repository
        '''
        return self.__repository.get_all()

    def update(self, id, name):
        '''
        this function update a client stored in the repository
        :param id: the id of client to be updated
        :param name: string representing the new name of the client
        :return:
        '''
        id = str(id)
        client = Client(id, name)
        old_client = self.get_client_by_id(id)
        old_client = Client(id, old_client.name)
        self.__validator.validate(client)
        self.__repository.update(id, client)
        self.__redo_service.clear()
        self.__undo_service.add_in(self.__repository.update, False, (old_client,), self.__repository.update, False,
                                   (Client(id, name),))
        # self.__undo_service.add_in(self.__repository.update, False, id, old_client)

    def get_client_by_id(self, id):
        '''
        :param id: the id of the client
        :return: the associated client with that id
        '''
        return self.__repository.get_client_by_id(str(id))

    def get_client_by_name(self, name):
        '''
        This function returns all clients that contains a given name
        :param name: a string representing the name
        :return: list with all clients that contains a given name
        '''
        return self.__repository.get_client_by_name(name)


