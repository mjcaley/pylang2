from dataclasses import dataclass


class Error:
    def __init__(self, message: str, line: int, column: int):
        self.message = message
        self.line = line
        self.column = column


class Syntax(Error):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message, line, column)


class Redefinition(Syntax):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(f"Redefinition of {name}", line, column)
