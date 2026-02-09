import re
from typing import NamedTuple, List
import statscrypt.core.exceptions as exceptions

class Token(NamedTuple):
    type: str
    value: str

class Tokenizer:
    TOKEN_SPEC = [
        ('COMMAND',  r'\b(use|summarize|list|describe|gen|drop|keep|regress|graph)\b'),
        ('IF',       r'\bif\b'),
        ('STRING',   r'"(?:\\.|[^"\\])*"'),
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('OP',       r'[+\-*/^==<>!]+'),
        ('VAR',      r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.'),
    ]

    def tokenize(self, code: str) -> List[Token]:
        tokens = []
        regex = '|'.join('(?P<%s>%s)' % pair for pair in self.TOKEN_SPEC)
        for mo in re.finditer(regex, code):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise exceptions.SyntaxError(f'Unexpected character: {value}')
            tokens.append(Token(kind, value))
        return tokens
