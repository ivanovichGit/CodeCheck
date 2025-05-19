import ply.yacc as yacc
from cc_lexer import my_lexer, tokens  # Asegúrate de importar los tokens desde tu lexer

# Precedencia (para operadores aritméticos)
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Reglas de la gramática
def p_program(p):
    'program : INT MAIN LBRACE statements RBRACE'
    pass

def p_statements_multiple(p):
    'statements : statements statement'
    pass

def p_statements_single(p):
    'statements : statement'
    pass

def p_statement_declaration(p):
    'statement : type var_list SEMICOLON'
    pass

def p_type(p):
    '''type : INT
            | FLOAT'''
    pass

def p_var_list_multiple(p):
    'var_list : var_list COMMA ID'
    pass

def p_var_list_single(p):
    'var_list : ID'
    pass

def p_statement_assignment(p):
    'statement : ID EQUALS expression SEMICOLON'
    pass

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    pass

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    pass

def p_expression_number(p):
    'expression : NUMBER'
    pass

def p_expression_id(p):
    'expression : ID'
    pass

def p_statement_printf(p):
    'statement : PRINTF LPAREN STRING COMMA AMPERSAND ID RPAREN SEMICOLON'
    pass

def p_statement_scanf(p):
    'statement : SCANF LPAREN STRING COMMA AMPERSAND ID RPAREN SEMICOLON'
    pass

def p_statement_if(p):
    'statement : IF LPAREN condition RPAREN LBRACE statements RBRACE'
    pass

def p_statement_if_else(p):
    'statement : IF LPAREN condition RPAREN LBRACE statements RBRACE ELSE LBRACE statements RBRACE'
    pass

def p_statement_while(p):
    'statement : WHILE LPAREN condition RPAREN LBRACE statements RBRACE'
    pass

def p_condition(p):
    'condition : expression relop expression'
    pass

def p_relop(p):
    '''relop : GT
             | LT
             | GE
             | LE
             | EQ
             | NE'''
    pass

# Manejo de errores
syntax_error = False

def p_error(p):
    global syntax_error
    syntax_error = True
    if p:
        print(f"Error de sintaxis en token '{p.value}' (línea {p.lineno})")
    else:
        print("Error de sintaxis al final del archivo")

# Construcción del parser
parser = yacc.yacc()
