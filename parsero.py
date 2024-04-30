import yacc as yacc
from lexer import tokens, lexer

pasada = 1
symbolTable = {}
errores = 0

precedence = (
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIG', 'MAYORIG'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDE'),
    ('right', 'POTENCIA')
)

start = 'program'


def p_program(t):
    '''program : main LlaveI code LlaveD'''

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
    symbolTable[t[2]] = None

def p_asign(t):
    '''asign : empty
             | ASIGNA expression'''


def p_definition(t):
    'definition : identifier ASIGNA expression PyC code'


def p_expression(t):
    '''expression : expression OR A
                  | A'''

def p_A(t):
    '''A : A AND B
         | B'''

def p_B(t):
    '''B : NOT B
         | C
         | true
         | false'''
    
def p_C(t):
    '''C : C IGUAL D
         | C DIFERENTE D
         | D'''

def p_D(t):
    '''D : D MENOR expression1 
         | D MAYOR expression1
         | D MENORIG expression1
         | D MAYORIG expression1
         | expression1'''

# Regla para las expresiones aritmeticas mas y menos (mismo nivel de precedencia)
def p_expression1(t):
    '''expression1 : expression1 MAS T
                   | expression1 MENOS T
                   | T'''

#  Regla para las expresiones aritmeticas por y entre (mismo nivel de precedencia)
def p_T(t):
    '''T : T POR F
         | T DIVIDE F
         | F'''

#  Regla para expresion aritmetica potencia
def p_F(t):
    '''F : H POTENCIA F
         | H'''

#  Regla para regresar arriba con parentesis
def p_H(t):
    '''H : ParI expression ParD
         | identifier
         | ENTERO'''

def p_identifier(t):
    'identifier : ID'
    global errores
    if pasada == 2:
        try:
            symbolTable[t[1]]
        except LookupError:
            print(f"Variable '{t[1]}' not defined yet.")
            errores = errores + 1
    else:
        pass

def p_ifCond(t):
    'ifCond : if ParI expression ParD LlaveI code LlaveD ifElse'

def p_ifElse(t):
    '''ifElse : else LlaveI code LlaveD code
              | code'''

#  Regla para los errores
def p_error(t):
    global errores
    if pasada == 2:
        if(t):
            print(f"Error sintactico en '{t.value}' .")
            parser.errok()
            errores = errores + 1
        else:
            print("Error sintatcico en el archivo de entrada.")
    else:
        pass

#  Regla para la produccion vacia epsilon
def p_empty(t):
    'empty :'


parser = yacc.yacc()



def main():
    code = input("Nombre del archivo a parsear: ")
    global pasada
    global errores
    try :
        with open(code, 'r') as file:
            data = file.read()
            parser.parse(data, lexer)
            pasada = pasada + 1
            parser.parse(data, lexer)
            if errores == 0:
                print("Parsing success!!!")
            else:
                print("Parsing errors, can't parse the program")
    except FileNotFoundError:
        print("No se pudo encontrar el archivo referido")
        exit

if __name__ == "__main__":
    main()