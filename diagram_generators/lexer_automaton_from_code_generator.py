import graphviz
import re

def extract_token_rules(lexer_code):
    """
    Extrae las reglas de tokens desde el código léxico
    """
    tokens = []
    simple_tokens = {}
    regex_tokens = {}
    
    # Buscar lista de tokens
    token_list_match = re.search(r'tokens\s*=\s*\[(.*?)\]', lexer_code, re.DOTALL)
    if token_list_match:
        token_list = token_list_match.group(1)
        tokens = [t.strip().strip("'").strip('"') for t in token_list.split(',') if t.strip()]
    
    # Buscar expresiones regulares simples (t_TOKEN = r'...')
    simple_token_matches = re.finditer(r't_([A-Z_]+)\s*=\s*r[\'"](.+?)[\'"]', lexer_code)
    for match in simple_token_matches:
        token_name = match.group(1)
        regex = match.group(2)
        simple_tokens[token_name] = regex
    
    # Buscar funciones de token (def t_TOKEN...)
    regex_token_matches = re.finditer(r'def\s+t_([A-Za-z_]+)\s*\(.*?\):\s*r[\'"](.+?)[\'"]', lexer_code, re.DOTALL)
    for match in regex_token_matches:
        token_name = match.group(1)
        regex = match.group(2)
        regex_tokens[token_name] = regex
    
    # Buscar palabras reservadas
    reserved_match = re.search(r'reserved\s*=\s*{(.*?)}', lexer_code, re.DOTALL)
    reserved = {}
    if reserved_match:
        reserved_items = reserved_match.group(1).split(',')
        for item in reserved_items:
            if ':' in item:
                key, value = item.split(':', 1)
                key = key.strip().strip("'").strip('"')
                value = value.strip().strip("'").strip('"')
                reserved[key] = value
    
    return tokens, simple_tokens, regex_tokens, reserved

def create_lexer_automaton_from_code(lexer_code):
    """
    Genera un diagrama del autómata finito basado en el código del analizador léxico
    """
    tokens, simple_tokens, regex_tokens, reserved = extract_token_rules(lexer_code)
    
    # Crear un nuevo grafo
    dot = graphviz.Digraph(comment='Autómata Finito para el Analizador Léxico (Extraído del Código)')
    
    # Configurar el formato y estilo
    dot.attr(rankdir='LR', size='10,7')
    dot.attr('node', shape='circle')
    
    # Estado inicial
    dot.node('start', shape='none', label='')
    dot.node('q0', label='q0', shape='circle')
    dot.edge('start', 'q0')
    
    # Contador para los estados
    state_counter = 1
    
    # Procesar tokens simples
    for token_name, regex in simple_tokens.items():
        state_name = f'q{state_counter}'
        state_counter += 1
        
        dot.node(state_name, label=token_name, shape='doublecircle')
        
        # Simplificar la expresión regular para la etiqueta
        label = regex.replace('\\', '\\\\')
        
        dot.edge('q0', state_name, label=label)
    
    # Procesar tokens con regex complejas
    for token_name, regex in regex_tokens.items():
        if token_name == 'error' or token_name == 'newline' or token_name == 'COMMENT':
            continue  # Saltamos estos casos especiales
            
        state_name = f'q{state_counter}'
        state_counter += 1
        
        dot.node(state_name, label=token_name, shape='doublecircle')
        
        # Simplificar la expresión regular para la etiqueta
        label = regex.replace('\\', '\\\\')
        if len(label) > 30:  # Si es muy larga, acortarla
            label = label[:20] + '...'
            
        dot.edge('q0', state_name, label=label)
    
    # Agregar palabras reservadas
    if reserved:
        reserved_state = f'q{state_counter}'
        state_counter += 1
        dot.node(reserved_state, label='Reserved\nWords', shape='doublecircle')
        
        # Conectar con una línea punteada para representar verificación después de ID
        id_state = next((f'q{i}' for i in range(1, state_counter) if dot.body and f'label=ID' in ''.join(dot.body)), None)
        if id_state:
            dot.edge(id_state, reserved_state, label='lookup', style='dashed')
    
    return dot

# Generar y guardar el diagrama basado en el código léxico proporcionado
def generate_automaton_from_code(lexer_code):
    dot = create_lexer_automaton_from_code(lexer_code)
    
    # Renderizar el gráfico (requiere que Graphviz esté instalado)
    try:
        dot.render('lexer_automaton_from_code', format='png', cleanup=True)
        print("Diagrama basado en el código generado como 'lexer_automaton_from_code.png'")
        
        dot.render('lexer_automaton_from_code', format='svg', cleanup=True)
        print("Diagrama basado en el código generado como 'lexer_automaton_from_code.svg'")
        
        # Para ver el código DOT que genera el diagrama
        dot_source = dot.source
        with open('lexer_automaton_from_code.dot', 'w') as f:
            f.write(dot_source)
        print("Código DOT para el diagrama guardado como 'lexer_automaton_from_code.dot'")
        
        return dot
    except Exception as e:
        print(f"Error al generar el diagrama: {e}")
        return None

# Script principal
if __name__ == "__main__":
    # Aquí puedes cargar el código del léxico desde un archivo
    with open('cc_lexer.py', 'r') as file:
        lexer_code = file.read()
    
    # O usar directamente el código que proporcionaste
    # lexer_code = """import ply.lex as lex... (tu código aquí)"""
    
    generate_automaton_from_code(lexer_code)
