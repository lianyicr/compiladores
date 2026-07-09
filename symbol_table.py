from dataclasses import dataclass


@dataclass
class Symbol:

    name: str
    type: str
    initialized: bool = False


class Scope:

    def __init__(self, parent=None):

        self.parent = parent
        self.symbols = {}

    ##########################################

    def declare(self, name, type_name):

        if name in self.symbols:
            raise Exception(
                f"Variable '{name}' redeclarada en el mismo ámbito."
            )

        self.symbols[name] = Symbol(
            name,
            type_name,
            False
        )

    ##########################################

    def assign(self, name):

        symbol = self.lookup(name)

        if symbol is None:
            raise Exception(
                f"Variable '{name}' no declarada."
            )

        symbol.initialized = True

    ##########################################

    def lookup(self, name):

        scope = self

        while scope:

            if name in scope.symbols:
                return scope.symbols[name]

            scope = scope.parent

        return None