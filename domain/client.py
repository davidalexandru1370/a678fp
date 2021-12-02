class Client:
    def __init__(self, client_id, name):
        self.__client_id = client_id
        self.__name = name

    @property
    def id(self):
        return self.__client_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
