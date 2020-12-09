class Error(Exception):
    def __init__(self, message: str, line: int, column: int):
        self.line = line
        self.column = column
        super().__init__(message)


class Syntax(Error):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(message, line, column)


class Redefinition(Syntax):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(f"Redefinition of {name}", line, column)


class Undefined(Syntax):
    def __init__(self, name: str, line: int, column: int):
        super().__init__(f"{name} undefined ", line, column)


class ExpectedOperand(Syntax):
    def __init__(self, line: int, column: int):
        super().__init__("Unary instruction expects an operand", line, column)


class UnexpectedOperand(Syntax):
    def __init__(self, line: int, column: int):
        super().__init__("Nullary instruction doesn't expect operand", line, column)
