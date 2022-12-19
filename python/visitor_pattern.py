# The Visitor pattern allows adding new behaviors to existing class hierarchy
# without altering any existing code.
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generic, TypeVar

T = TypeVar("T")


class Expr(ABC):
    """
    The Expr interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abstractmethod
    def accept(self, visitor: Visitor[T]) -> T:
        pass


class Token(Enum):
    PLUS = 1
    MINUS = 2


class Binary(Expr):
    """
    Each Concrete Expr must implement the `accept` method in such a way
    that it calls the visitor's method corresponding to the expr's class.
    """

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_binary(self)


class Literal(Expr):

    def __init__(self, value: int | float | str | None):
        self.value = value

    def accept(self, visitor: Visitor[T]) -> T:
        return visitor.visit_literal(self)


class Visitor(ABC, Generic[T]):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """

    @abstractmethod
    def visit_binary(self, element: Binary) -> T:
        pass

    @abstractmethod
    def visit_literal(self, element: Literal) -> T:
        pass


"""
Concrete Visitors implement several versions of the same algorithm, which can
work with all concrete component classes.

You can experience the biggest benefit of the Visitor pattern when using it with
a complex object structure, such as a Composite tree. In this case, it might be
helpful to store some intermediate state of the algorithm while executing
visitor's methods over various objects of the structure.
"""


class ExprPrinter(Visitor[str]):

    def print_expr(self, expr: Expr) -> str:
        return expr.accept(self)

    def visit_binary(self, element: Binary) -> str:
        return '({} {} {})'.format(element.operator,
                                   self.print_expr(element.left),
                                   self.print_expr(element.right))

    def visit_literal(self, element: Literal) -> str:
        return str(element.value)


if __name__ == "__main__":
    expr = Binary(Literal(3), Token.PLUS, Literal(5))
    printer = ExprPrinter()
    expr_str = printer.print_expr(expr)
    print(expr_str)
