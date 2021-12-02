class BookValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)


class BookValidator:
    def validate(self, book):
        if book.title is None or book.title == '':
            raise BookValidationException('The book has no title')
        if book.author is None or book.author == '':
            raise BookValidationException('The book has no author')
