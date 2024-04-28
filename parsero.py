import yacc as yacc
from lexer import tokens, lexer
import sys

precedence = (
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIG', 'MAYORIG'),
    ('left', 'MAS', 'MENOS', 'OR'),
    ('left', 'POR', 'DIVIDE', 'AND'),
    ('left', 'POTENCIA', 'NOT')
)

start = 'code'

# Regla para el codigo
def p_code(t):
    '''code : declaration
            | definition
            | ifCond
            | empty'''

# Regla para las declaraciones de enteros
def p_declaration(t):
    '''declaration : int ID asign PyC code
                   | bool ID asign PyC code'''

def p_asign(t):
    '''asign : empty
             | ASIGNA expression''' 

def p_definition(t):
    'definition : ID ASIGNA expression PyC code'

def p_expression(t):
    '''expression : numexp
                  | logicexp
                  | ID
                  | testexp
                  | ParI expression ParD
                  | ENTERO'''

# Regla para suma y resta
def p_numexp(t):
    '''numexp : expression MAS expression 
              | expression MENOS expression
              | expression POR expression 
              | expression DIVIDE expression
              | expression POTENCIA expression'''

def p_logicexp(t):
    '''logicexp : expression OR expression
                | expression AND expression
                | NOT expression
                | true
                | false'''

def p_ifCond(t):
    'ifCond : if ParI expression ParD LlaveI code LlaveD ifElse'

def p_ifElse(t):
    '''ifElse : else LlaveI code LlaveD code
              | code'''

def p_testexp(t):
    '''testexp : expression IGUAL expression
               | expression DIFERENTE expression
               | expression MENOR expression 
               | expression MAYOR expression
               | expression MENORIG expression
               | expression MAYORIG expression'''

#  Regla para los errores
def p_error(t):
    print(f"Error sintactico en '{t.value}'")
    exit

#  Regla para la produccion vacia epsilon
def p_empty(t):
    'empty :'
    pass

parser = yacc.yacc()

def main():
    code = input("Nombre del archivo a parsear: ")
    try :
        with open(code, 'r') as file:
            data = file.read()
            parser.parse(data, lexer)
    except FileNotFoundError:
        print("No se pudo encontrar el archivo referido")
        exit

if __name__ == "__main__":
    main()