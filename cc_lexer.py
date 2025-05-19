import ply.lex as lex

# Lista de nombres de tokens
tokens = [
    'INT',
    'FLOAT',
    'MAIN',
    'ID',
    'NUMBER',
    'EQUALS',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'SEMICOLON',
    'COMMA',
    'AMPERSAND',
    'PRINTF',
    'SCANF',
    'STRING',
    'GT', 'LT', 'GE', 'LE', 'EQ', 'NE',
    'IF',      # <-- Agrega esto
    'ELSE',    # <-- Agrega esto
    'WHILE',   # <-- Agrega esto
]

# Palabras reservadas (las identificamos en una función especial)
reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'main': 'MAIN',
    'printf': 'PRINTF',
    'scanf': 'SCANF',
    'if': 'IF',         # <-- Agrega esto
    'else': 'ELSE',     # <-- Agrega esto
    'while': 'WHILE',   # <-- Agrega esto
}

# Expresiones regulares simples para los tokens
t_EQUALS     = r'='
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_COMMA      = r','
t_AMPERSAND  = r'&'
t_GT         = r'>'
t_LT         = r'<'
t_GE         = r'>='
t_LE         = r'<='
t_EQ         = r'=='
t_NE         = r'!='

# Números (enteros o flotantes)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Cadenas (para printf/scanf)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Verifica si es palabra reservada
    return t

# Ignorar espacios y tabs
t_ignore = ' \t'

# Ignorar comentarios tipo C
def t_COMMENT(t):
    r'\/\/.*'
    pass

# Saltos de línea (para contar líneas)
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    # Solo marcar que hubo un error, sin detalles
    t.lexer.invalid = True
    t.lexer.skip(1)

# Construcción del lexer
my_lexer = lex.lex()