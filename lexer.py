import ply.lex as lex

##############################
# PALABRAS RESERVADAS
##############################

reserved = {
    "conjunto": "CONJUNTO",
    "de": "DE",

    "union": "UNION",
    "interseccion": "INTERSECCION",
    "diferencia": "DIFERENCIA",
    "en": "EN",
    "imprimir": "IMPRIMIR",

    "if": "IF",
    "else": "ELSE",

    "true": "TRUE",
    "false": "FALSE",

    "int": "INT",
    "string": "STRING_TYPE",
    "booleano": "BOOLEANO"
}

##############################
# TOKENS
##############################

tokens = [

    # Identificadores
    "ID",

    # Literales
    "NUMBER",
    "STRING",

    # Operadores

    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",

    "ASSIGN",

    "LT",
    "GT",
    "LE",
    "GE",
    "EQ",
    "NE",

    # Delimitadores

    "LPAREN",
    "RPAREN",

    "LBRACE",
    "RBRACE",

    "COMMA",
    "SEMICOLON"

] + list(reserved.values())

##############################
# EXPRESIONES REGULARES
##############################

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

t_ASSIGN = r'='

t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_LBRACE = r'\{'
t_RBRACE = r'\}'

t_COMMA = r','
t_SEMICOLON = r';'

##############################
# IGNORAR ESPACIOS
##############################

t_ignore = " \t"

##############################
# COMENTARIOS
##############################

def t_COMMENT(t):
    r'//.*'
    pass

def t_BLOCKCOMMENT(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')

##############################
# CADENAS
##############################

def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = bytes(
        t.value[1:-1],
        "utf-8"
    ).decode("unicode_escape")
    return t

##############################
# NÚMEROS
##############################

def t_NUMBER(t):
    r'-?\d+(\.\d+)?'

    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)

    return t

##############################
# IDENTIFICADORES
##############################

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    t.type = reserved.get(
        t.value,
        "ID"
    )

    return t

##############################
# NUEVA LÍNEA
##############################

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

##############################
# COLUMNA
##############################

def find_column(input, token):

    last_cr = input.rfind('\n',0,token.lexpos)

    if last_cr < 0:
        last_cr = -1

    return token.lexpos-last_cr

##############################
# ERRORES LÉXICOS
##############################

def t_error(t):

    column = find_column(
        t.lexer.lexdata,
        t
    )

    print(
        f"Error léxico "
        f"[línea {t.lineno}, columna {column}]: "
        f"carácter inesperado '{t.value[0]}'"
    )

    t.lexer.skip(1)

##############################
# CONSTRUCCIÓN
##############################

lexer = lex.lex()

##############################
# PRUEBA
##############################

if __name__ == "__main__":

    data = '''
    conjunto A = {1,2,3};

    conjunto B = {4,5};

    imprimir A union B;

    '''

    lexer.input(data)

    while True:

        tok = lexer.token()

        if not tok:
            break

        print(tok)