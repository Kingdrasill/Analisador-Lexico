import re
from tabulate import tabulate

# Expressões regulares para dígitos e letras
D = '[0-9]'
L = '[a-zA-Z_]'

class AFD:
    def __init__(self):
        # Definição dos estados inicial e atual, e estados finais com tipos e retornos associados
        self.inicial = 'q0'
        self.atual = 'q0'
        self.final = {
            'q2': {'tipo': 'ID', 'retorno': -1},         # Identificador
            'q4': {'tipo': 'NUM_INT', 'retorno': -1},    # Número inteiro
            'q7': {'tipo': 'NUM_DEC', 'retorno': -1},    # Número decimal
            'q9': {'tipo': 'TEXTO', 'retorno': 0},       # Texto entre aspas
            'q12': {'tipo': 'COMENT', 'retorno': -1},    # Comentário
            'q13': {'tipo': '/', 'retorno': -1},         # Divisão ou início de comentário
            'q14': {'tipo': '+', 'retorno': 0},          # Soma
            'q15': {'tipo': '-', 'retorno': 0},          # Subtração
            'q16': {'tipo': '*', 'retorno': 0},          # Multiplicação
            'q17': {'tipo': '%', 'retorno': 0},          # Módulo
            'q19': {'tipo': '==', 'retorno': 0},         # Igualdade
            'q20': {'tipo': '=', 'retorno': -1},         # Atribuição ou comparação
            'q22': {'tipo': '!=', 'retorno': 0},         # Diferente
            'q23': {'tipo': '!', 'retorno': -1},         # Negação
            'q25': {'tipo': '>=', 'retorno': 0},         # Maior ou igual
            'q26': {'tipo': '>', 'retorno': -1},         # Maior
            'q28': {'tipo': '<=', 'retorno': 0},         # Menor ou igual
            'q29': {'tipo': '<', 'retorno': -1},         # Menor
            'q31': {'tipo': '||', 'retorno': 0},         # OU lógico
            'q33': {'tipo': '&&', 'retorno': 0},         # E lógico
            'q34': {'tipo': ',', 'retorno': 0},          # Vírgula
            'q35': {'tipo': ';', 'retorno': 0},          # Ponto e vírgula
            'q36': {'tipo': '(', 'retorno': 0},          # Parêntese esquerdo
            'q37': {'tipo': ')', 'retorno': 0},          # Parêntese direito
            'q38': {'tipo': '[', 'retorno': 0},          # Colchete esquerdo
            'q39': {'tipo': ']', 'retorno': 0},          # Colchete direito
            'q40': {'tipo': '{', 'retorno': 0},          # Chave esquerda
            'q41': {'tipo': '}', 'retorno': 0},          # Chave direita
            'q42': {'tipo': 'ERRO', 'retorno': 0},       # Estado de erro
            'q43': {'tipo': 'SPACE', 'retorno': 0},      # Espaço em branco
            'q44': {'tipo': 'BREAKLINE', 'retorno': 0},  # Quebra de linha
            'q45': {'tipo': '.', 'retorno': 0}           # Ponto
        }
        # Transições de estado para cada estado atual
        self.transicao = {
            'q0': [
                [L, 'q1'], [D, 'q3'], ['"', 'q8'], ['/', 'q10'], ['[+]', 'q14'],
                ['-', 'q15'], ['[*]', 'q16'], ['%', 'q17'], ['=', 'q18'], ['!', 'q21'],
                ['>', 'q24'], ['<', 'q27'], ['\\|', 'q30'], ['&', 'q32'], [',', 'q34'],
                [';', 'q35'], ['\\(', 'q36'], ['\\)', 'q37'], ['\\[', 'q38'], [']', 'q39'],
                ['{', 'q40'], ['}', 'q41'], [' ', 'q43'], ['\n', 'q44'], ['[.]', 'q45']
            ], 
            'q1': [[f'{D}|{L}', 'q1'], [f'(?!{D}|{L}).|\n', 'q2']],            # Transições para identificadores
            'q3': [[D, 'q3'], [f'(?!{D}|{L}|[.]).|\n', 'q4'], ['[.]', 'q5']],  # Transições para números inteiros
            'q5': [[D, 'q6']],                                                 # Transições para números decimais
            'q6': [[D, 'q6'], [f'(?!{D}|{L}).|\n', 'q7']],                     # Transições para números decimais
            'q8': [['(?!"|\n).', 'q8'], ['"', 'q9'], ['\n', 'q42']],           # Transições para texto entre aspas
            'q10': [['/', 'q11'], ['(?!/).|\n', 'q13']],                       # Transições para divisão ou início de comentário
            'q11': [['(?!\n).', 'q11'], ['\n', 'q12']],                        # Transições para comentário
            'q18': [['=', 'q19'], ['(?!=).|\n', 'q20']],                       # Transições para atribuição ou comparação
            'q21': [['=', 'q22'], ['(?!=).|\n', 'q23']],                       # Transições para negação ou diferença
            'q24': [['=', 'q25'], ['(?!=).|\n', 'q26']],                       # Transições para maior ou maior ou igual
            'q27': [['=', 'q28'], ['(?!=).|\n', 'q29']],                       # Transições para menor ou menor ou igual
            'q30': [['[|]', 'q31']],                                           # Transições para operador lógico OR
            'q32': [['&', 'q33']]                                              # Transições para operador lógico AND
        }
    
    # Método para testar cada caracter e transitar para o próximo estado
    def testaCaracter(self, caracter):
        trns = self.transicao[self.atual]  # Transições possíveis do estado atual
        
        for i in trns:
            if re.fullmatch(i[0], caracter) != None:  # Verifica se o caractere corresponde à transição
                self.atual = i[1]  # Atualiza o estado atual
                if self.atual in self.final:  # Se o estado atual for final
                    temp = self.final[self.atual]  # Obtém as informações associadas ao estado final
                    self.atual = self.inicial  # Reinicia o estado atual
                    return (temp['tipo'], temp['retorno'])  # Retorna o tipo e o retorno do token
                else:
                    return ('', 0)  # Caso contrário, retorna uma tupla vazia
        else:
            return ('erro', 0)  # Se não houver transição correspondente, retorna um erro

# Função para retornar o subtipo do identificador
def subtiposId(token, word):
    tipos = ['int', 'float', 'char', 'boolean', 'void', 'if', 'else', 'for', 'while', 'scanf', 'println', 'main', 'return']

    if word in tipos:  # Verifica se o identificador é uma palavra-chave
        return (word.upper(), '')  # Retorna o token
    else:
        return ('ID', word)  # Caso contrário, retorna o tipo como ID e o próprio identificador

# Classe para armazenar os identificadores encontrados
class Simbolos:
    def __init__(self):
        self.ids = []

    def __str__(self):
        return tabulate({'ID': self.ids}, headers=['INDEX', 'ID'], tablefmt="outline", showindex='always')

    # Método para inserir um identificador na lista de identificadores
    def inserirID(self, token):
        self.ids.append(token[1])  # Adiciona o identificador à lista
        return ('ID', self.ids.index(token[1]))  # Retorna o tipo e o índice do identificador na lista

    # Método para encontrar um identificador na lista de identificadores
    def findID(self, token):
        if token[1] in self.ids:  # Verifica se o identificador já está na lista
            return ('ID', self.ids.index(token[1]))  # Retorna o tipo e o índice do identificador na lista
        else:
            return self.inserirID(token)  # Caso contrário, insere o identificador na lista e retorna suas informações

# Classe para armazenar os tokens encontrados
class Tokens:
    def __init__(self):
        self.tokens = []
    
    def __str__(self):
        return tabulate(self.tokens, headers=['Token', 'Value'], tablefmt="outline")

    # Método para inserir um token na lista de tokens
    def inserirToken(self, token):
        self.tokens.append(token)  # Adiciona o token à lista