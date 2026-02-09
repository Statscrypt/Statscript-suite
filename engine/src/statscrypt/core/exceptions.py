"""
Custom exception classes for the statscrypt engine, including Stata-style error codes.
"""


class StatscryptError(Exception):
    """Base class for all statscrypt-specific errors."""

    def __init__(self, message, code=0):
        super().__init__(message)
        self.code = code
        self.stata_message = f"r({self.code}); {message}"

    def __str__(self):
        return self.stata_message


class SyntaxError(StatscryptError):
    """Raised when a command has incorrect syntax."""

    def __init__(self, message="syntax error", code=198):
        super().__init__(message, code)


class DataError(StatscryptError):
    """Raised when there is an issue with data operations."""

    def __init__(self, message="data not loaded or invalid data operation", code=4):
        super().__init__(message, code)


class CommandError(StatscryptError):
    """Raised when a command fails to execute or is not implemented."""

    def __init__(self, message="command not found or not implemented", code=199):
        super().__init__(message, code)


class VariableError(StatscryptError):
    """Raised when there is an issue with variables (e.g., not found, already exists)."""

    def __init__(self, message="variable not found or already exists", code=101):
        super().__init__(message, code)


class FileError(StatscryptError):
    """Raised when there is an issue with file operations."""

    def __init__(self, message="file not found or inaccessible", code=601):
        super().__init__(message, code)
