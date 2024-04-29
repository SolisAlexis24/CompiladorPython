import yacc as yacc
from lexer import tokens, lexer

precedence = (
    ('nonassoc', 'MENOR', 'MAYOR', 'MENORIG', 'MAYORIG'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDE'),
    ('right', 'POTENCIA')
)
start = 'P'
symbolTable = {}
pasada = 1


#  Regla para la produccion vacia epsilon
def p_empty(t):
    'empty :'
    pass

#  Simbolo inicial, contiene el prototipo inical del programa mas basico
def p_P_program(t):
    '''P : int main LlaveI code return ENTERO PyC LlaveD'''
    

# Regla para escoger que codigo quieres usar, D = declaracion aritmetica, B = Declaracion Booleana
#   R = Condicional if o ifelse y empty para no hacer nada
def p_C_code(t):
    '''code : declaration
            | definition
            | ifCond
            | empty'''

# Regla para declarar y/o asignar expresiones aritmeticas
def p_declaration(t):
    '''declaration : int ID asign PyC code
                   | bool ID asign PyC code'''
    symbolTable[t[2]] = None

def p_definition(t):
    'definition : identifier ASIGNA expression PyC code'

def p_asign(t):
    '''asign : empty
             | ASIGNA expression'''

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
def p_T_arith(t):
    '''T : T POR F
         | T DIVIDE F
         | F'''

#  Regla para expresion aritmetica potencia
def p_F_arith(t):
    '''F : H POTENCIA F
         | H'''

#  Regla para regresar arriba con parentesis
def p_H(t):
    '''H : ParI expression ParD
         | identifier
         | ENTERO'''

#Regla para los identificadoes
def p_identifier(t):
    'identifier : ID'
    if pasada == 2:
        try:
            symbolTable[t[1]]
        except LookupError:
            print(f"Variable '{t[1]}' no definida antes.")
    else:
        pass

def p_ifCond(t):
    'ifCond : if ParI expression ParD LlaveI code LlaveD ifElse'

def p_ifElse(t):
    '''ifElse : else LlaveI code LlaveD code
              | code'''

#  Regla para los errores
def p_error(t):
    if pasada == 2:
        if(t):
            print(f"Error sintactico en '{t.value}' .")
            parser.errok()
        else:
            print("Error sintatcico en el archivo de entrada.")
    else:
        pass


parser = yacc.yacc()

def parse_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
        parser.parse(data, lexer)

parse_file("scode.c")

print(symbolTable)