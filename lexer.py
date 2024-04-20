import ply.lex as lex
import sys
global code
code = ""

#Reserved words
reserved = {
    'if' : 'if',
    'else' : 'else',
    'return': 'return',
    'True': 'true',
    'False' : 'false',
    'int' : 'int',
    'bool':'bool'
}
#List of token names
tokens = ['ENTERO','ID','MAS','MENOS','DIVIDE','POTENCIA','POR',
    'AND','OR','NOT','MENOR','MAYOR','MENORIG','MAYORIG',
    'IGUAL','DIFERENTE','ASIGNA', 'PyC', 'ParI', 'ParD',
    'LlaveI', 'LlaveD'] + list(reserved.values())

def codeGetter():
    """This function read the content of a file and store the content onto the "code" variable"""
    global code
    if(len(sys.argv)!= 2):
        sys.exit()
    else:
        file_name = sys.argv[1]
        with open(file_name) as file:
            for line in file.readlines():
                code = code + line #Open the file and line by line, it reads the content and concatenate each line onto the string "code"

def Lexer():
    #Tokens
    t_MENORIG = r'<='
    t_MAYORIG = r'>='
    t_IGUAL = r'=='
    t_DIFERENTE = r'!='
    t_POTENCIA = r'\*\*'
    t_MAS = r'\+'
    t_MENOS = r'-'
    t_DIVIDE = r'/'
    t_POR = r'\*'
    t_AND = r'\^'
    t_OR = r'\|'
    t_NOT = r'\~'
    t_MENOR = r'<'
    t_MAYOR = r'>'
    t_ASIGNA = r'='
    t_PyC = r';'
    t_ParI = r'\('
    t_ParD = r'\)'
    t_LlaveI = r'\{'
    t_LlaveD = r'\}'

    #Ignored tokens
    t_ignore_comment = r'@.*'
    t_ignore_tab = r'\t'
    t_ignore_space = r'\s'

    #New line
    def t_newline(t):
        r'\n+'
        t.lineno += len(t.value)
    #Caracter desconocido
    def t_error(t):
        print("Unknown char: ''%s'" %t.value[0])

    def t_ENTERO(t):
        r'\d+'
        try:
            t.value = int(t.value)
        except ValueError:
            print("Integer too large %s" %t.value)
            t.value = 0
        return t
    #Definicion de la estructura de los ID
    def t_ID(t):
        r'[a-z_][a-z_0_9]*'
        t.type = reserved.get(t.value, 'ID')
        return t

    return lex.lex()

Lexer()
codeGetter()
lex.runmain(data = code)
