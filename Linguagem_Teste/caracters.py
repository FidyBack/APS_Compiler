private_filters = [' ', '\n', '\t']
private_words = ['escreva', 'leia', 'retorne', 'se', 'senao', 'enquanto', 'variavel', 'funcao']
private_types = ['vazia', 'inteiro', 'palavra']

private_operators = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    '(': 'LPAR',
    ')': 'RPAR',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ';': 'SEMICOLON',
    '=': 'EQUAL',
    '==': 'ISEQUAL',
    '>': 'GREATER',
    '<': 'LESS',
    '!': 'NOT',
    '&&': 'AND',
    '||': 'OR',
    '.': 'DOT',
    ',': 'COMMA',
    ':': 'COLON',
    '->': 'ARROW'
}