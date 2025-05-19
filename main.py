from cc_lexer import my_lexer
from cc_parser import parser, syntax_error
import cc_parser

if __name__ == "__main__":
    cc_code = '''
    int main {
        int x, y;
        y = 5;
        x = 3 + y;
        
        printf("%d", &x);
        
        scanf("%d", &y);
        
        if (x > 0) {
            x = x - 1;
        } else {
            x = x + 1;
        }

        while (x > 0) {
            x = x - 1;
        }
    }
    '''
    # Análisis léxico
    my_lexer.input(cc_code)
    my_lexer.invalid = False
    for _ in my_lexer:
        pass

    if getattr(my_lexer, 'invalid', False):
        print("El código NO es válido (error léxico)")
    else:
        parser.parse(cc_code)
        if cc_parser.syntax_error:
            print("El código NO es válido (error sintáctico)")
        else:
            print("El código es válido")
