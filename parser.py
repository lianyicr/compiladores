import ply.yacc as yacc
from lexer import tokens, lexer
from ast_nodes import *

def get_column(lexpos):
    """Calcula la columna exacta a partir del lexpos global del archivo."""
    last_cr = lexer.lexdata.rfind('\n', 0, lexpos)
    if last_cr < 0:
        last_cr = -1
    return lexpos - last_cr

precedence = (
    ('left', 'UNION', 'INTERSECCION', 'DIFERENCIA'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'EQ', 'NE'),
    ('left', 'EN')
)

def p_program(p):
    '''
    program : statement_list
    '''
    # La línea/columna recae en la primera instrucción
    p[0] = Program(p[1], lineno=p.lineno(1), column=get_column(p.lexpos(1)))

def p_statement_list_many(p):
    '''
    statement_list : statement_list statement
    '''
    p[0] = p[1] + [p[2]]

def p_statement_list_one(p):
    '''
    statement_list : statement
    '''
    p[0] = [p[1]]

def p_statement(p):
    '''
    statement : declaration
              | assignment
              | print_stmt
              | if_stmt
    '''
    # Se propaga el nodo tal cual (ya viene con su lineno y column)
    p[0] = p[1]

def p_declaration(p):
    '''
    declaration : CONJUNTO ID ASSIGN set_literal SEMICOLON
    '''
    p[0] = Declaration(
        p[2],
        p[4],
        lineno=p.lineno(1), # Toma la línea de "conjunto"
        column=get_column(p.lexpos(1))
    )

def p_assignment(p):
    '''
    assignment : ID ASSIGN expression SEMICOLON
    '''
    p[0] = Assignment(
        p[1],
        p[3],
        lineno=p.lineno(1), # Toma la línea del ID
        column=get_column(p.lexpos(1))
    )

def p_print(p):
    '''
    print_stmt : IMPRIMIR expression SEMICOLON
    '''
    p[0] = Print(
        p[2],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_if(p):
    '''
    if_stmt : IF LPAREN expression RPAREN block
    '''
    p[0] = If(
        p[3],
        p[5].statements,
        [],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_if_else(p):
    '''
    if_stmt : IF LPAREN expression RPAREN block ELSE block
    '''
    p[0] = If(
        p[3],
        p[5].statements,
        p[7].statements,
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_block(p):
    '''
    block : LBRACE statement_list RBRACE
    '''
    p[0] = Block(
        p[2],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_set_literal(p):
    '''
    set_literal : LBRACE element_list RBRACE
    '''
    p[0] = SetLiteral(
        p[2],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_element_list_many(p):
    '''
    element_list : element_list COMMA expression
    '''
    p[0] = p[1] + [p[3]]

def p_element_list_one(p):
    '''
    element_list : expression
    '''
    p[0] = [p[1]]

def p_expression_identifier(p):
    '''
    expression : ID
    '''
    p[0] = Identifier(
        p[1],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_expression_number(p):
    '''
    expression : NUMBER
    '''
    p[0] = Number(
        p[1],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_expression_string(p):
    '''
    expression : STRING
    '''
    p[0] = String(
        p[1],
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_expression_true(p):
    '''
    expression : TRUE
    '''
    p[0] = Boolean(
        True,
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_expression_false(p):
    '''
    expression : FALSE
    '''
    p[0] = Boolean(
        False,
        lineno=p.lineno(1),
        column=get_column(p.lexpos(1))
    )

def p_union(p):
    '''
    expression : expression UNION expression
    '''
    p[0] = SetOperation(
        "union",
        p[1],
        p[3],
        lineno=p.lineno(2), # Toma la línea del operador UNION
        column=get_column(p.lexpos(2))
    )

def p_intersection(p):
    '''
    expression : expression INTERSECCION expression
    '''
    p[0] = SetOperation(
        "interseccion",
        p[1],
        p[3],
        lineno=p.lineno(2),
        column=get_column(p.lexpos(2))
    )

def p_difference(p):
    '''
    expression : expression DIFERENCIA expression
    '''
    p[0] = SetOperation(
        "diferencia",
        p[1],
        p[3],
        lineno=p.lineno(2),
        column=get_column(p.lexpos(2))
    )

def p_membership(p):
    '''
    expression : expression EN expression
    '''
    p[0] = Membership(
        p[1],
        p[3],
        lineno=p.lineno(2),
        column=get_column(p.lexpos(2))
    )

def p_relational(p):
    '''
    expression : expression LT expression
               | expression LE expression
               | expression GT expression
               | expression GE expression
               | expression EQ expression
               | expression NE expression
    '''
    p[0] = Comparison(
        p[2],
        p[1],
        p[3],
        lineno=p.lineno(2),
        column=get_column(p.lexpos(2))
    )

def p_arithmetic(p):
    '''
    expression : expression PLUS expression
               | expression MINUS expression
               | expression TIMES expression
               | expression DIVIDE expression
    '''
    p[0] = Arithmetic(
        p[2],
        p[1],
        p[3],
        lineno=p.lineno(2),
        column=get_column(p.lexpos(2))
    )

def p_group(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_statement_error(p):
    '''
    statement : error SEMICOLON
    '''
    print("Recuperando después de un error sintáctico.")
    p[0] = None

def p_error(p):
    if p is None:
        print("Error sintáctico: fin inesperado del archivo.")
        return
    
    col = get_column(p.lexpos)
    print(
        f"Error sintáctico [línea {p.lineno}, columna {col}]: "
        f"token inesperado '{p.value}'"
    )
    parser.errok()

parser = yacc.yacc()

if __name__ == "main":
    with open("examples/valido.set") as f:
        source = f.read()
    
    lexer.input(source) # Esto asegura que lexdata esté disponible
    ast = parser.parse(source, lexer=lexer)
    print(ast)