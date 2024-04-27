import yacc as yacc
from lexer import tokens, lexer
import sys

precedence = (
    ('left', 'MAS', 'MENOS', 'OR'),
    ('left', 'POR', 'DIVIDE', 'AND'),
    ('left', 'POTENCIA', 'NOT')
)

start = 'code'
symbolTable = {}



# Regla para el codigo
def p_code(t):
    '''code : declarationI
            | declarationII
            | empty'''

# Regla para las declaraciones de enteros
def p_declarationI(t):
    '''declarationI : int ID PyC code
                    | int ID ASIGNA expression PyC code
                    | ID ASIGNA expression PyC code'''
    
    if len(t) == 5: #Para la primera regla, declaracion sin asignacion
        if t[2] in symbolTable:
            print(f"La variable '{t[2]}' ya ha sido declarada antes, no puede ser declarada de nuevo.")
        else:
            symbolTable[t[2]] = 0 #Se agrega a la tabla de simbolos
            print(f"Se declara '{t[2]}'")

    elif len(t) == 7: #Para la regla dos, declaracion y asignacion
        if t[2] in symbolTable:
            print(f"La variable '{t[2]}' ya ha sido declarada antes, no puede ser declarada e inicializada de nuevo.")
        else:
            symbolTable[t[2]] = t[4] #Se agrega a la tabla de simbolos
            print(f"Se declara '{t[2]}' y se le asigna un valor")

    elif len(t) == 6:
        if t[1] in symbolTable:
            symbolTable[t[1]] = t[3] #Se asigna el valor (ID = E)
            print(f"Se le asigna un valor a '{t[1]}'")
        else:
            print(f"La variable '{t[1]}' no sido declarada antes, no se le puede asignar un valor.")

# Regla para suma y resta
def p_expression(t):
    '''expression : expression MAS T 
                  | expression MENOS T'''
    if t[2] == '+': t[0] = t[1]+t[3] 
    elif t[2] == '-': t[0] = t[1]-t[3]

# Regla para pasar de expression a T
def p_expression_T(t):
    'expression : T'
    t[0] = t[1]

def p_T(t):
    '''T : T POR F
         | T DIVIDE F'''
    if t[2] == '*' : t[0] = t[1]*t[3]
    elif t[2] == '/' : t[0] = int(t[1]/t[3])

def p_T_F(t):
    'T : F'
    t[0] = t[1]

#  Regla para expresion aritmetica potencia
def p_F(t):
    '''F : F POTENCIA H'''
    if t[2] == '**' : t[0] = pow(t[1], t[3])  

# Regla para pasar de F a H
def p_F_H(t):
    'F : H'
    t[0] = t[1]

#  Regla para parentesis arriba con parentesis
def p_H_expression(t):
    'H : ParI expression ParD'
    t[0] = t[2]

#Regla para los identificadoes
def p_H_ID(t):
    'H : ID'
    try:
        t[0] = symbolTable[t[1]]
    except LookupError:
        print(f"Variable '{t[1]}' no definida antes.")
        t[0] = 0

#  Regla para los numeros
def p_H_ENTERO(t):
    'H : ENTERO'
    t[0] = t[1]


def p_declarationII(t):
    '''declarationII : bool ID PyC code
                    | bool ID ASIGNA expressionbool PyC code
                    | ID ASIGNA expressionbool PyC code'''
    
    if len(t) == 5: #Para la primera regla, declaracion sin asignacion
        if t[2] in symbolTable:
            print(f"La variable '{t[2]}' ya ha sido declarada antes, no puede ser declarada de nuevo.")
        else:
            symbolTable[t[2]] = True #Se agrega a la tabla de simbolos
            print(f"Se declara '{t[2]}'")

    elif len(t) == 7: #Para la regla dos, declaracion y asignacion
        if t[2] in symbolTable:
            print(f"La variable '{t[2]}' ya ha sido declarada antes, no puede ser declarada e inicializada de nuevo.")
        else:
            symbolTable[t[2]] = t[4] #Se agrega a la tabla de simbolos
            print(f"Se declara '{t[2]}' y se le asigna un valor")

    elif len(t) == 6:
        if t[1] in symbolTable:
            symbolTable[t[1]] = t[3] #Se asigna el valor (ID = E)
            print(f"Se le asigna un valor a '{t[1]}'")
        else:
            print(f"La variable '{t[1]}' no sido declarada antes, no se le puede asignar un valor.")   

def p_expressionbool(t):
    'expressionbool : expressionbool OR boolT'
    t[0] = (t[1] or t[3])

def p_expressionbool_boolT(t):
    'expressionbool : boolT'
    t[0] = t[1]

def p_boolT(t):
    'boolT : boolT AND boolF'
    t[0] = (t[1] and t[3])

def p_boolT_boolF(t):
    'boolT : boolF'
    t[0] = t[1]

def p_boolF(t):
    'boolF : NOT boolF'
    t[0] = not(t[1])

def p_boolF_W(t):
    'boolF : W'
    t[0] = t[1]

def p_W_True(t):
    'W : true'
    t[0] = True

def p_W_False(t):
    'W : false'
    t[0] = False

def p_W_Par(t):
    'W : ParI expressionbool ParD'

#Regla para los identificadoes
def p_W_ID(t):
    'W : ID'
    try:
        t[0] = symbolTable[t[1]]
    except LookupError:
        print(f"Variable '{t[1]}' no definida antes.")
        t[0] = 0

#  Regla para los errores
def p_error(t):
    print(f"Error sintactico en '{t.value}'")

#  Regla para la produccion vacia epsilon
def p_empty(p):
    'empty :'
    pass

parser = yacc.yacc()

'''
operations = [
    "int a;",
    "a = 10*5;",
    "int b = 5+3;",
    "int c = b+a;",
    "int d = c/2;",
    "bool x = true;",
    "bool y = false;",
    "bool z;",
    "z = x|y;"
]

for i in operations:
    parser.parse(i, lexer)
'''

def main():
    code_lines = []  # Lista para almacenar el código introducido por el usuario   
    print("Ingresa tu código linea a linea (presiona Ctrl + D para terminar):")
    
    # Bucle para leer la entrada del usuario línea por línea
    while True:
        try:
            # Lee una línea de entrada
            line = input(">>> ")
            
            # Agrega la línea a la lista
            code_lines.append(line)
        
        except EOFError:
            # Si se produce un EOF (End of File, por ejemplo, Ctrl + D en Unix), termina el bucle
            break

    # Procesa el código
    for line in code_lines:
        parser.parse(line, lexer)  # Parsea cada línea utilizando tu módulo yacc
        
    # Haz algo con la lista de código, como imprimirlo
    print("El código introducido es:")
    for line in code_lines:
        print(line)

    print("Tabla de simbolos: ")
    print(symbolTable)

if __name__ == "__main__":
    main()
