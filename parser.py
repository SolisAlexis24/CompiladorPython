import ply.yacc as yacc
import sys
from lexer import tokens, lexer



precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDE'),
    ('left', 'POTENCIA')
)

start = 'P'
symbolTable = {}


#  Regla para la produccion vacia epsilon
def p_empty(p):
    'empty :'
    pass

#  Simbolo inicial, contiene el prototipo inical del programa mas basico
def p_P_program(t):
    '''P : int main LlaveI C return ENTERO PyC LlaveD'''
    

# Regla para escoger que codigo quieres usar, D = declaracion aritmetica, B = Declaracion Booleana
#   R = Condicional if o ifelse y empty para no hacer nada
def p_C_code(t):
    '''C : D
         | empty'''

# Regla para declarar y/o asignar expresiones aritmeticas
def p_D_integer_dec(t):
    '''D : int ID PyC C
         | int ID ASIGNA E PyC C
         | ID ASIGNA E PyC C '''
    if len(t) == 5: #Para la primera regla, declaracion sin asignacion
        symbolTable[t[2]] = 0 #Se agrega a la tabla de simbolos

    elif len(t) == 7: #Para la regla dos, declaracion y asignacion
        symbolTable[t[2]] = t[4] #Se agrega a la tabla de simbolos

    elif len(t) == 6:
            symbolTable[t[1]] = t[3] #Se asigna el valor (ID = E)

# Regla para las expresiones aritmeticas mas y menos (mismo nivel de precedencia)
def p_E_arith(t):
    '''E : E MAS T
         | E MENOS T'''
    if t[2] == '+': t[0] = t[1]+t[3] 
    elif t[2] == '-': t[0] = t[1]-t[3]

#  Regla para pasar de E a T
def p_E_goT(t):
    'E : T'
    t[0] = t[1]

#  Regla para las expresiones aritmeticas por y entre (mismo nivel de precedencia)
def p_T_arith(t):
    '''T : T POR F
         | T DIVIDE F'''
    if t[2] == '*' : t[0] = t[1]*t[3]
    elif t[2] == '/' : t[0] = int(t[1]/t[3])

# Regla para pasar de T a F
def p_T_goF(t):
    'T : F'
    t[0] = t[1]

#  Regla para expresion aritmetica potencia
def p_F_arith(t):
    '''F : F POTENCIA H'''
    if t[2] == '**' : t[0] = pow(t[1], t[3])

# Regla para pasar de F a H
def p_F_goH(t):
    'F : H'
    t[0] = t[1]

#  Regla para regresar arriba con parentesis
def p_H_goback(t):
    'H : ParI E ParD'

#Regla para los identificadoes
def p_H_idname(t):
    'H : ID'
    try:
        t[0] = symbolTable[t[1]]
    except LookupError:
        print(f"Variable '{t[1]}' no definida antes.")
        t[0] = 0

#  Regla para los numeros
def p_H_integer(t):
    'H : ENTERO'
    t[0] = t[1]


#  Regla para los errores
def p_error(t):
    print(f"Error sintactico en '{t.value}'")


parser = yacc.yacc()

def parse_file(filename):
    with open(filename, 'r') as file:
        data = file.read()
    lexer.input(data)
    print("Lexical analysis success")
    parser.parse(data)

parse_file("scode.c")

print(symbolTable)