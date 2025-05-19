from graphviz import Digraph
import ply.lex as lex

def generate_lexer_automaton(output_filename="lexer_automaton_visual"):
    """
    Genera un diagrama de autómata finito para visualizar tu analizador léxico.
    """
    # Crear el diagrama
    dot = Digraph(comment='Autómata Finito del Analizador Léxico', format='png')
    dot.attr(rankdir='LR', size='11,8')
    
    # Crear estado inicial
    dot.attr('node', shape='circle')
    dot.node('start', shape='none', label='')
    dot.node('q0', label='q0')
    dot.edge('start', 'q0')
    
    # --- Identificadores y palabras reservadas ---
    dot.node('id', label='ID', shape='doublecircle')
    dot.edge('q0', 'id', label='[a-zA-Z_]')
    dot.edge('id', 'id', label='[a-zA-Z0-9_]')
    
    # Palabras reservadas (como una subgráfica para mostrar que se detectan después de ID)
    with dot.subgraph(name='cluster_reserved') as c:
        c.attr(label='Palabras Reservadas', style='dashed')
        c.node('int', label='INT', shape='doublecircle')
        c.node('float', label='FLOAT', shape='doublecircle')
        c.node('main', label='MAIN', shape='doublecircle')
        c.node('printf', label='PRINTF', shape='doublecircle')
        c.node('scanf', label='SCANF', shape='doublecircle')
        c.node('if', label='IF', shape='doublecircle')
        c.node('else', label='ELSE', shape='doublecircle')
        c.node('while', label='WHILE', shape='doublecircle')
    
    # Conectar ID con las palabras reservadas mediante una línea punteada
    dot.edge('id', 'int', label='lookup', style='dashed')
    
    # --- Números (enteros y flotantes) ---
    dot.node('num_start', label='digit', shape='circle')
    dot.edge('q0', 'num_start', label='[0-9]')
    
    dot.node('integer', label='INT', shape='doublecircle')
    dot.edge('num_start', 'integer', label='[0-9]*')
    
    dot.node('dot', label='.', shape='circle')
    dot.edge('integer', 'dot', label='.')
    
    dot.node('float', label='FLOAT', shape='doublecircle')
    dot.edge('dot', 'float', label='[0-9]+')
    
    # --- Operadores ---
    # = y ==
    dot.node('equals', label='EQUALS', shape='doublecircle')
    dot.edge('q0', 'equals', label='=')
    
    dot.node('eq', label='EQ', shape='doublecircle')
    dot.edge('equals', 'eq', label='=')
    
    # Otros operadores
    dot.node('plus', label='PLUS', shape='doublecircle')
    dot.edge('q0', 'plus', label='+')
    
    dot.node('minus', label='MINUS', shape='doublecircle')
    dot.edge('q0', 'minus', label='-')
    
    dot.node('times', label='TIMES', shape='doublecircle')
    dot.edge('q0', 'times', label='*')
    
    dot.node('divide', label='DIVIDE', shape='doublecircle')
    dot.edge('q0', 'divide', label='/')
    
    # --- Operadores relacionales ---
    # >
    dot.node('gt', label='GT', shape='doublecircle')
    dot.edge('q0', 'gt', label='>')
    
    # >=
    dot.node('ge', label='GE', shape='doublecircle')
    dot.edge('gt', 'ge', label='=')
    
    # <
    dot.node('lt', label='LT', shape='doublecircle')
    dot.edge('q0', 'lt', label='<')
    
    # <=
    dot.node('le', label='LE', shape='doublecircle')
    dot.edge('lt', 'le', label='=')
    
    # !=
    dot.node('not', label='!', shape='circle')
    dot.edge('q0', 'not', label='!')
    
    dot.node('ne', label='NE', shape='doublecircle')
    dot.edge('not', 'ne', label='=')
    
    # --- Delimitadores ---
    dot.node('lparen', label='LPAREN', shape='doublecircle')
    dot.edge('q0', 'lparen', label='(')
    
    dot.node('rparen', label='RPAREN', shape='doublecircle')
    dot.edge('q0', 'rparen', label=')')
    
    dot.node('lbrace', label='LBRACE', shape='doublecircle')
    dot.edge('q0', 'lbrace', label='{')
    
    dot.node('rbrace', label='RBRACE', shape='doublecircle')
    dot.edge('q0', 'rbrace', label='}')
    
    dot.node('semicolon', label='SEMICOLON', shape='doublecircle')
    dot.edge('q0', 'semicolon', label=';')
    
    dot.node('comma', label='COMMA', shape='doublecircle')
    dot.edge('q0', 'comma', label=',')
    
    dot.node('ampersand', label='AMPERSAND', shape='doublecircle')
    dot.edge('q0', 'ampersand', label='&')
    
    # --- Cadenas de texto ---
    dot.node('str_start', label='STRING_START', shape='circle')
    dot.edge('q0', 'str_start', label='"')
    
    dot.node('str_content', label='STRING_CONTENT', shape='circle')
    dot.edge('str_start', 'str_content', label='[^"\\\\]')
    dot.edge('str_content', 'str_content', label='[^"\\\\]')
    
    dot.node('str_escape', label='ESCAPE', shape='circle')
    dot.edge('str_content', 'str_escape', label='\\\\')
    dot.edge('str_escape', 'str_content', label='.')
    
    dot.node('string', label='STRING', shape='doublecircle')
    dot.edge('str_content', 'string', label='"')
    dot.edge('str_start', 'string', label='"')
    
    dot.node('comment_start', label='/', shape='circle')
    dot.edge('q0', 'comment_start', label='/')
    
    dot.node('comment', label='COMMENT', shape='circle')
    dot.edge('comment_start', 'comment', label='/')
    dot.edge('comment', 'comment', label='[^\\n]')
    
    try:
        dot.render(output_filename, view=False)
        print(f"Diagrama de autómata finito generado como {output_filename}.png")
        
        dot.format = 'svg'
        dot.render(output_filename + '_svg', view=False)
        print(f"Diagrama de autómata finito generado como {output_filename}_svg.svg")
        
        return True
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")
        return False

def mermaid_af_diagram():
    """
    Genera un diagrama Mermaid para visualizar el autómata finito del analizador léxico.
    Esto puede ser útil si no tienes Graphviz instalado.
    """
    mermaid_code = """
stateDiagram-v2
    [*] --> q0
    
    %% Identificadores y palabras reservadas
    q0 --> ID: [a-zA-Z_]
    ID --> ID: [a-zA-Z0-9_]
    
    state "Palabras Reservadas" as Reserved {
        ID --> INT: lookup(int)
        ID --> FLOAT: lookup(float)
        ID --> MAIN: lookup(main)
        ID --> PRINTF: lookup(printf)
        ID --> SCANF: lookup(scanf)
        ID --> IF: lookup(if)
        ID --> ELSE: lookup(else)
        ID --> WHILE: lookup(while)
    }
    
    %% Números
    q0 --> Digit: [0-9]
    Digit --> INT: [0-9]*
    INT --> DOT: .
    DOT --> FLOAT: [0-9]+
    
    %% Operadores
    q0 --> EQUALS: =
    EQUALS --> EQ: =
    q0 --> PLUS: +
    q0 --> MINUS: -
    q0 --> TIMES: *
    q0 --> DIV: /
    
    %% Operadores relacionales
    q0 --> GT: >
    GT --> GE: =
    q0 --> LT: <
    LT --> LE: =
    q0 --> NOT: !
    NOT --> NE: =
    
    %% Delimitadores
    q0 --> LPAREN: (
    q0 --> RPAREN: )
    q0 --> LBRACE: {
    q0 --> RBRACE: }
    q0 --> SEMICOLON: ;
    q0 --> COMMA: ,
    q0 --> AMPERSAND: &
    
    %% Cadenas
    q0 --> S1: "
    S1 --> S2: [^"\\]
    S2 --> S2: [^"\\]
    S2 --> S3: \\
    S3 --> S2: .
    S2 --> STRING: "
    S1 --> STRING: "
    
    %% Comentarios
    DIV --> COMMENT: /
    COMMENT --> COMMENT: [^\\n]
    """
    
    return mermaid_code

if __name__ == "__main__":
    generate_lexer_automaton()
    
    print("\nCódigo Mermaid para diagrama de AF:")
    print(mermaid_af_diagram())
