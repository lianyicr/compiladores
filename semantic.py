from ast_nodes import *
from symbol_table import Scope

class SemanticError(Exception):
    """Excepción personalizada para errores semánticos limpios."""
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.scope = self.global_scope

    def error(self, node, message):
        """Genera un error semántico con formato posicional exacto."""
        raise SemanticError(
            f"Error semántico [línea {node.lineno}, columna {node.column}]: {message}"
        )

    def visit(self, node):
        if node is None:
            return
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No existe visit_{node.__class__.__name__}")

    def visit_Program(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_Declaration(self, node):
        value_type = self.visit(node.value)
        
        # Chequeo 1: Variable redeclarada en el mismo ámbito
        if node.name in self.scope.symbols:
            self.error(node, f"Variable '{node.name}' redeclarada en el mismo ámbito.")
        
        self.scope.declare(node.name, value_type)
        self.scope.assign(node.name)

    def visit_Assignment(self, node):
        symbol = self.scope.lookup(node.name)
        
        # Chequeo 2: Variable usada sin declarar
        if symbol is None:
            self.error(node, f"Variable '{node.name}' usada sin declarar.")
        
        value_type = self.visit(node.value)
        
        # Chequeo 3: Tipos incompatibles en operaciones/asignaciones
        if symbol.type != value_type:
            self.error(node, f"Tipos incompatibles: no se puede asignar '{value_type}' a '{symbol.type}'.")
        
        symbol.initialized = True

    def visit_Identifier(self, node):
        symbol = self.scope.lookup(node.name)
        
        if symbol is None:
            self.error(node, f"Variable '{node.name}' usada sin declarar.")
        
        # Chequeo 4: Uso de variable antes de asignación
        if not symbol.initialized:
            self.error(node, f"Variable '{node.name}' usada antes de asignación.")
        
        return symbol.type

    def visit_Number(self, node):
        return "int"

    def visit_String(self, node):
        return "string"

    def visit_Boolean(self, node):
        return "booleano"

    def visit_SetLiteral(self, node):
        if len(node.elements) == 0:
            return "conjunto de any"
        
        first_type = self.visit(node.elements[0])
        for element in node.elements[1:]:
            t = self.visit(element)
            # Regla del dominio: Homogeneidad
            if t != first_type:
                self.error(node, f"los conjuntos deben ser homogéneos. Se encontró '{first_type}' y '{t}'.")
        
        return f"conjunto de {first_type}"

    def visit_Print(self, node):
        self.visit(node.expression)

    def visit_SetOperation(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if not left.startswith("conjunto") or not right.startswith("conjunto"):
            self.error(node, f"La operación '{node.operator}' requiere conjuntos.")

        # Regla del dominio: Compatibilidad de tipos
        if left != right:
            op_verb = "unir" if node.operator == "union" else "operar"
            self.error(
                node, 
                f"no se pueden {op_verb} conjuntos de tipos distintos: '{left}' y '{right}'"
            )
        
        return left

    def visit_Membership(self, node):
        elem = self.visit(node.element)
        collection = self.visit(node.collection)

        if not collection.startswith("conjunto de "):
            self.error(node, f"El operador 'en' requiere un conjunto. Se encontró '{collection}'.")
            
        expected = collection.replace("conjunto de ", "")
        
        # Regla del dominio: x debe ser del mismo tipo que los elementos de A
        if elem != expected:
            self.error(node, f"el elemento buscado ('{elem}') debe ser del mismo tipo que los elementos del '{collection}'.")
        
        return "booleano"

    def visit_Arithmetic(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left != "int" or right != "int":
            self.error(node, f"Operación aritmética solo permitida entre enteros. Se encontró '{left}' y '{right}'.")
        return "int"

    def visit_Comparison(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left != right:
            self.error(node, f"Comparación entre tipos distintos: '{left}' y '{right}'.")
        return "booleano"

    def visit_If(self, node):
        condition = self.visit(node.condition)
        if condition != "booleano":
            self.error(node, f"La condición de un if debe ser booleana. Se encontró '{condition}'.")
        
        # Manejo de ámbitos para el bloque THEN
        old_scope = self.scope
        self.scope = Scope(old_scope)
        for stmt in node.then_branch:
            self.visit(stmt)
        self.scope = old_scope
        
        # Manejo de ámbitos para el bloque ELSE
        if node.else_branch:
            self.scope = Scope(old_scope)
            for stmt in node.else_branch:
                self.visit(stmt)
            self.scope = old_scope

    def visit_Block(self, node):
        old_scope = self.scope
        self.scope = Scope(old_scope)
        for stmt in node.statements:
            self.visit(stmt)
        self.scope = old_scope