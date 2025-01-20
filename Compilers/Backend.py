#DEFINING THE DATA STRUCTURE FOR TREE

from dataclasses import dataclass

from dataclasses import dataclass
from collections.abc import Iterator
from more_itertools import peekable

class Token:
    pass

@dataclass
class NumberToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i >= len(s):
            return

        if s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isdigit():
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        else:
            match t := s[i]:
                case '+' | '*' | '-' | '/' :
                    i = i + 1
                    yield OperatorToken(t)




class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class Number(AST):
    val: str



def parse(s: str) -> AST:
    t = peekable(lex(s))
    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_atom()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_atom())
                case OperatorToken('/'):
                    next(t)
                    ast = BinOp("/", ast, parse_atom())
                case _:
                    return ast

    def parse_atom():
        match t.peek(None):
            case NumberToken(v):
                next(t)
                return Number(v)

    return parse_add()


#evaluating the tree
def e(tree: AST) -> int:
    match tree:
        case Number(v): return int(v)
        case BinOp("+", l, r): return e(l) + e(r)
        case BinOp("*", l, r): return e(l) * e(r)
        case BinOp("-", l, r): return e(l) - e(r)
        case BinOp("/", l, r): return e(l) / e(r)


expr_t1 = parse("2*3-5")
print(e(expr_t1))