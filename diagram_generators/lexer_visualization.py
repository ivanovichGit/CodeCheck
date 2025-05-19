import graphviz

def create_lexer_automaton():
    """
    Genera un diagrama de autómata finito a partir de las reglas léxicas definidas.
    """
    dot = graphviz.Digraph(comment='Autómata Finito para el Analizador Léxico')
    
    dot.attr(rankdir='LR', size='8,5')
    dot.attr('node', shape='circle')
    
    dot.node('start', shape='none', label='')
    dot.node('0', label='q0')
    dot.edge('start', '0')
        
    dot.node('1', label='ID', shape='doublecircle')
    dot.edge('0', '1', label='[a-zA-Z_]')
    dot.edge('1', '1', label='[a-zA-Z0-9_]')
    
    dot.node('2', label='INT', shape='doublecircle')
    dot.node('3', label='DOT', shape='circle')
    dot.node('4', label='FLOAT', shape='doublecircle')
    dot.edge('0', '2', label='[0-9]')
    dot.edge('2', '2', label='[0-9]')
    dot.edge('2', '3', label='.')
    dot.edge('3', '4', label='[0-9]')
    dot.edge('4', '4', label='[0-9]')
    
    dot.node('5', label='EQUALS', shape='doublecircle')
    dot.edge('0', '5', label='=')
    
    dot.node('6', label='EQ', shape='doublecircle')
    dot.edge('5', '6', label='=')
    
    dot.node('7', label='PLUS', shape='doublecircle')
    dot.edge('0', '7', label='+')
    
    dot.node('8', label='MINUS', shape='doublecircle')
    dot.edge('0', '8', label='-')
    
    dot.node('9', label='TIMES', shape='doublecircle')
    dot.edge('0', '9', label='*')
    
    dot.node('10', label='DIVIDE', shape='doublecircle')
    dot.edge('0', '10', label='/')
    
    dot.node('11', label='GT', shape='doublecircle')
    dot.node('12', label='GE', shape='doublecircle')
    dot.edge('0', '11', label='>')
    dot.edge('11', '12', label='=')
    
    dot.node('13', label='LT', shape='doublecircle')
    dot.node('14', label='LE', shape='doublecircle')
    dot.edge('0', '13', label='<')
    dot.edge('13', '14', label='=')
    
    dot.node('15', label='NOT', shape='circle')
    dot.node('16', label='NE', shape='doublecircle')
    dot.edge('0', '15', label='!')
    dot.edge('15', '16', label='=')
    
    dot.node('17', label='LPAREN', shape='doublecircle')
    dot.edge('0', '17', label='(')
    
    dot.node('18', label='RPAREN', shape='doublecircle')
    dot.edge('0', '18', label=')')
    
    dot.node('19', label='LBRACE', shape='doublecircle')
    dot.edge('0', '19', label='{')
    
    dot.node('20', label='RBRACE', shape='doublecircle')
    dot.edge('0', '20', label='}')
    
    dot.node('21', label='SEMICOLON', shape='doublecircle')
    dot.edge('0', '21', label=';')
    
    dot.node('22', label='COMMA', shape='doublecircle')
    dot.edge('0', '22', label=',')
    
    dot.node('23', label='AMPERSAND', shape='doublecircle')
    dot.edge('0', '23', label='&')
    
    dot.node('24', label='STRING_START', shape='circle')
    dot.node('25', label='STRING_CONTENT', shape='circle')
    dot.node('26', label='STRING_ESCAPE', shape='circle')
    dot.node('27', label='STRING', shape='doublecircle')
    
    dot.edge('0', '24', label='"')
    dot.edge('24', '25', label='[^"\\\\]')
    dot.edge('25', '25', label='[^"\\\\]')
    dot.edge('25', '26', label='\\\\')
    dot.edge('26', '25', label='any')
    dot.edge('25', '27', label='"')
    dot.edge('24', '27', label='"')
    
    dot.node('28', label='COMMENT_START', shape='circle')
    dot.node('29', label='COMMENT', shape='circle')
    
    dot.edge('0', '28', label='/')
    dot.edge('28', '29', label='/')
    dot.edge('29', '29', label='[^\\n]')
    
    return dot

def visualize_lexer():
    """
    Genera y guarda el diagrama del autómata finito para el analizador léxico.
    """
    dot = create_lexer_automaton()
    
    try:
        dot.render('lexer_automaton', format='png', cleanup=True)
        print("Diagrama del autómata finito generado como 'lexer_automaton.png'")
        
        dot.render('lexer_automaton', format='svg', cleanup=True)
        print("Diagrama del autómata finito generado como 'lexer_automaton.svg'")
        
        dot_source = dot.source
        with open('lexer_automaton.dot', 'w') as f:
            f.write(dot_source)
        print("Código DOT para el diagrama guardado como 'lexer_automaton.dot'")
        
        return dot
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")
        return None

if __name__ == "__main__":
    visualize_lexer()