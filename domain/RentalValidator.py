from datetime import datetime, timedelta


class RentalValidatorException(Exception):
    def __init__(self, message):
        super().__init__(message)


class RentalValidator:
    def validate(self, rental):
        if rental.rented_date < (datetime.now().date() - timedelta(days=1)):
            raise RentalValidatorException("Can not rent on that date!")
