import analisador as ans  # Importa o módulo 'analisador' como 'ans'

# Função para testar uma linha do código fonte
def testaLinha(afd, simbolos, tokens, linha, line):
    count = -1  # Inicializa um contador para os caracteres na linha
    word = ''  # Inicializa uma string vazia para armazenar os caracteres
    resposta = True  # Inicializa a variável de resposta como True

    while count < len(line)-1:  # Loop enquanto o contador for menor que o comprimento da linha
        count += 1  # Incrementa o contador
        caracter = line[count]  # Obtém o caracter na posição do contador

        retorno = afd.testaCaracter(caracter)  # Chama o método testaCaracter do autômato finito determinístico (AFD) para testar o caracter
        count += retorno[1]  # Incrementa o contador com o retorno do método testaCaracter

        # Verifica se ocorreu um erro léxico ou um erro
        if retorno[0] == 'erro' or retorno[0] == 'ERRO':
            tokens.inserirToken(('ERRO', 'Tem um erro lexico na linha {}'.format(linha)))  # Insere um token de erro na lista de tokens
            resposta = False  # Define a resposta como False
            break  # Sai do loop

        else: 
            word += caracter  # Adiciona o caracter à palavra em construção

            if retorno[0] == 'SPACE' or retorno[0] == 'BREAKLINE':  # Se o retorno for um espaço em branco ou quebra de linha
                word = ''  # Reinicia a palavra

            if retorno[0] != '' and retorno[0] != 'SPACE' and retorno[0] != 'BREAKLINE':  # Se o retorno não for vazio, espaço ou quebra de linha
                if retorno[1] == -1:  # Se o retorno for -1, remove o último caracter da palavra
                    word = word[:-1]

                if retorno[0] == 'ID':  # Se o retorno for um identificador
                    resp = ans.subtiposId(retorno[0], word)  # Obtém o subtipo do identificador

                    if resp[0] == 'ID':  # Se o subtipo for ID
                        resp = simbolos.findID(resp)  # Verifica se o identificador já existe na tabela de símbolos
                
                elif retorno[0] == '>' or retorno[0] == '>=' or retorno[0] == '<' or retorno[0] == '<=' or retorno[0] == '!=' or retorno[0] == '==':
                    resp = ('COMP', retorno[0])  # Se o retorno for um operador de comparação, define o token como 'COMP'

                else:
                    resp = (retorno[0], word)  # Caso contrário, define o tipo como o próprio retorno e a palavra

                if resp[0] == 'COMENT':  # Se o tipo for um comentário
                    word = ''  # Reinicia a palavra
                    continue  # Pula para a próxima iteração do loop
                
                tokens.inserirToken(resp)  # Insere o token na lista de tokens
                word = ''  # Reinicia a palavra
    return resposta  # Retorna a resposta

# Inicializa o AFD, a tabela de símbolos e a lista de tokens
afd = ans.AFD() 
simbolos = ans.Simbolos()
tokens = ans.Tokens()

# Abre o arquivo de código fonte
filename = input("Nome do arquivo do codigo: ")
file = open(filename, 'r')
lines = file.readlines()
linha = 0

# Loop para testar cada linha do código fonte
for line in lines:
    linha += 1  # Incrementa o contador de linhas
    resp = testaLinha(afd, simbolos, tokens, linha, line)  # Chama a função para testar a linha
    if resp == False:  # Se houver um erro léxico
        break  # Sai do loop

# Imprime a lista de tokens e a tabela de símbolos
print('Lista de Tokes')
print(tokens)
print('Tabela de Simbolos')
print(simbolos)