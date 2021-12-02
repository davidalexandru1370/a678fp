class ClientRepositoryException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ClientRepository:
    def __init__(self):
        self.__data = dict()

    def save(self, client):
        '''
        This function save a new client inside the repository
        :param client: a class Client
        '''
        if client.id in self.__data:
            raise ClientRepositoryException("There exists an client with the same id=" + str(client.id))
        self.__data[client.id] = client

    def remove(self, id):
        '''
        This function remove a client stored in repository by his id
        :param id: the id of the client
        :return:
        '''
        if id in self.__data.keys():
            del self.__data[id]
        else:
            raise ClientRepositoryException("There is no such id=" + str(id))

    def get_all(self):
        '''
        :return:This function returns all the values stored in repository as a list
        '''
        return list(self.__data.values())

    def update(self, id, client):
        '''
        This function update a client by his id
        :param id: the id to be updated
        :param client: the new class client
        :return:
        '''
        if id not in self.__data.keys():
            raise ClientRepositoryException('There is no such id = ' + str(id))
        self.__data[id].name = client.name

    def get_client_by_id(self, id):
        '''
        This function returns the client by his id
        :param id: the id of the client
        :return: the client with that id
        '''
        if id not in self.__data.keys():
            raise ClientRepositoryException("There's no such id = " + str(id))

        return self.__data[id]

    def get_client_by_name(self, name):
        return list(filter(lambda x: name in x.name.lower(), self.__data.values()))

    def __len__(self):
        '''

        :return: the no. of elements in the repository
        '''
        return len(self.__data)
