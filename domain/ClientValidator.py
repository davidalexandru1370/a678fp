class ClientValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class ClientValidator:

    def validate(self, client):
        if client.name is None or len(client.name) == 0 or client.name == '':
            raise ClientValidationException("The client has no name!")
