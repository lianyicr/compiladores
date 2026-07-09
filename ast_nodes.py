from dataclasses import dataclass
from typing import List

########################################################
# NODO BASE
########################################################
class Node:
    pass

########################################################
# PROGRAMA
########################################################
@dataclass
class Program(Node):
    statements: List
    lineno: int = 0
    column: int = 0

########################################################
# DECLARACIÓN
########################################################
@dataclass
class Declaration(Node):
    name: str
    value: Node
    lineno: int = 0
    column: int = 0

########################################################
# ASIGNACIÓN
########################################################
@dataclass
class Assignment(Node):
    name: str
    value: Node
    lineno: int = 0
    column: int = 0

########################################################
# IMPRIMIR
########################################################
@dataclass
class Print(Node):
    expression: Node
    lineno: int = 0
    column: int = 0

########################################################
# IF
########################################################
@dataclass
class If(Node):
    condition: Node
    then_branch: List
    else_branch: List
    lineno: int = 0
    column: int = 0

########################################################
# IDENTIFICADOR
########################################################
@dataclass
class Identifier(Node):
    name: str
    lineno: int = 0
    column: int = 0

########################################################
# LITERALES
########################################################
@dataclass
class Number(Node):
    value: int | float
    lineno: int = 0
    column: int = 0

@dataclass
class String(Node):
    value: str
    lineno: int = 0
    column: int = 0

@dataclass
class Boolean(Node):
    value: bool
    lineno: int = 0
    column: int = 0

########################################################
# CONJUNTO
########################################################
@dataclass
class SetLiteral(Node):
    elements: List
    lineno: int = 0
    column: int = 0

########################################################
# OPERACIÓN BINARIA
########################################################
@dataclass
class BinaryOperation(Node):
    operator: str
    left: Node
    right: Node
    lineno: int = 0
    column: int = 0

########################################################
# OPERACIÓN UNARIA
########################################################
@dataclass
class UnaryOperation(Node):
    operator: str
    operand: Node
    lineno: int = 0
    column: int = 0

########################################################
# OPERADOR EN
########################################################
@dataclass
class Membership(Node):
    element: Node
    collection: Node
    lineno: int = 0
    column: int = 0

@dataclass
class Block(Node):
    statements: list
    lineno: int = 0
    column: int = 0

@dataclass
class Type(Node):
    name: str
    lineno: int = 0
    column: int = 0

@dataclass
class SetType(Node):
    element_type: str
    lineno: int = 0
    column: int = 0

@dataclass
class Comparison(Node):
    operator: str
    left: Node
    right: Node
    lineno: int = 0
    column: int = 0

@dataclass
class Arithmetic(Node):
    operator: str
    left: Node
    right: Node
    lineno: int = 0
    column: int = 0

@dataclass
class SetOperation(Node):
    operator: str
    left: Node
    right: Node
    lineno: int = 0
    column: int = 0