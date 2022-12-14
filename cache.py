import random
writeMiss = 0
writeHit = 0
readMiss = 0
readHit = 0
tamanhoBloco = 2
tamanhoCache = 16
tamanhoRam = 1000
cpu = 3


class LinhaCache:
    # o parametro tamanho é referente ao tamanho dos blocos da ram
    def __init__(self):
        self.elemento = [None]*tamanhoBloco
        self.indice = [-1]*tamanhoBloco
        self.modificado = [0]*tamanhoBloco
        self.ocupada = 0
        self.marcador = ''

# Novo valor caso o valor acessado deva ser modificado


def geraValor():
    valor = random.randint(100, 1100)
    return valor


# verifica a primeira linha de cache vazia do processador escolhido
def verificaCache(caches, processador):
    for i in range(0, tamanhoCache):
        if(caches[processador][i].ocupada == 0):

            return i

    return -1


# busca o valor na cache do processador selecionado, caso encontrado retorna a posicao na cache do valor
def percorreCache(caches, indice, processador):

    for i in range(0, tamanhoCache):
        for j in range(0, tamanhoBloco):
            if (caches[processador][i].indice[j] == indice) and (caches[processador][i].marcador != 'i'):

                return i, j

    return -1, -1


# função que varre as caches procurando o marcados do elemento em questão


def percorreCaches(caches, indice, processador, operacao):
    retorno = 0
    for i in range(0, cpu):
        # Caso seja o processador diferente do indice em questao deve percorrer a cache do processador
        if(i != processador):
            for j in range(0, tamanhoCache):
                for k in range(0, tamanhoBloco):
                    if(caches[i][j].indice[k] == indice):
                        if(operacao == 0) and (caches[i][j].marcador == 'e' or caches[i][j].marcador == 'c' or caches[i][j].marcador == 'm') and (i != processador):
                            if(caches[i][j].marcador == 'm'):
                                retorno = -1
                            else:
                                caches[i][j].marcador = 'c'
                                retorno = 1
                        else:
                            caches[i][j].marcador = 'i'
    return retorno


def removeFIFO(caches, processador):
    caches[processador][0].ocupada = 0
    caches[processador][0].marcador = ''
    for i in range(0, tamanhoBloco):
        caches[processador][0].indice[i] = -1
        caches[processador][0].elemento[i] = None
        caches[processador][0].modificado[i] = 0

    return 0


def writeBack(caches, indiceCache, processador):
    for i in range(0, tamanhoBloco):
        if(caches[processador][indiceCache].modificado[i] == 1):
            ram[caches[processador][indiceCache].indice[i]
                ] = caches[processador][indiceCache].elemento[i]


def fifo(acessos, caches, i):
    novoValor = geraValor()
    disponivel = verificaCache(caches, acessos[i][1])
    indiceCache = disponivel
    buscaValor, indiceBloco = percorreCache(
        caches, acessos[i][0], acessos[i][1])
    # resto da divisão do indice do acesso pelo tamanho do bloco
    mod = acessos[i][0] % tamanhoBloco
    # variavel que vai delimitar o for para preencher o bloco da cache
    len1 = (acessos[i][0] + tamanhoBloco) - mod
    if(buscaValor > -1):  # o elemento está na cache do processador selecionado
        if(acessos[i][2] == 1):  # caso o valor acessado deva ser modificado
            caches[acessos[i][1]][buscaValor].elemento[indiceBloco] = novoValor
            caches[acessos[i][1]][buscaValor].modificado[indiceBloco] = 1
            caches[acessos[i][i]][buscaValor].marcador = 'm'
            percorreCaches(caches, acessos[i][0], acessos[i][1], acessos[i][2])
            global writeHit
            writeHit += 1

            print('indice ' + str(acessos[i][0]) +
                  ' buscado se encontra na cache' + ' do processador ' + str(acessos[i][1]))
            print('O indice foi modificado')
            print('*****************************************')

        else:
            global readHit
            readHit += 1

            print('indice ' + str(acessos[i][0]) +
                  ' buscado se encontra na cache' + ' do processador ' + str(acessos[i][1]))
            print('*****************************************')

    else:  # o elemento n está na cache do processador selecionado

        print('indice ' + str(acessos[i][0]) +
              ' buscado nao se encontra na cache' + ' do processador ' + str(acessos[i][1]))
        print('*****************************************')

        if(disponivel > -1):

            if(acessos[i][2] == 1):
                global writeMiss
                writeMiss += 1

            else:
                global readMiss
                readMiss += 1

        else:
            indiceCache = removeFIFO(caches, i)
            writeBack(caches, indiceCache, i)

        k = 0

        caches[acessos[i][1]][indiceCache].ocupada = 1
        for j in range(acessos[i][0] - mod, len1):
            caches[acessos[i][1]][indiceCache].indice[k] = j
            if(acessos[i][2] == 1 and acessos[i][0] == j):
                caches[acessos[i][1]][indiceCache].elemento[k] = novoValor
                caches[acessos[i][1]][indiceCache].modificado[k] = 1
                caches[acessos[i][1]][indiceCache].marcador = 'm'
                percorreCaches(
                    caches, acessos[i][0], acessos[i][1], acessos[i][2])

            else:
                caches[acessos[i][1]][indiceCache].elemento[k] = ram[j]
                if(acessos[i][2] != 1):
                    caches[acessos[i][1]][indiceCache].marcador = 'e'

                    # varre a cache verificando se ele já está marcado como exclusivo em outro elementos e marca como compartilhado
                    retorno = percorreCaches(
                        caches, acessos[i][0], acessos[i][1], acessos[i][2])
                    if(retorno == 1):  # caso ele exista marca como compartilhado
                        caches[acessos[i][1]][indiceCache].marcador = 'c'
                    elif(retorno == -1):  # caso ele exista em outra cache e tenha sido modificada
                        caches[acessos[i][i]][indiceCache].marcador = 'i'
            k += 1


def adicionaRam(ram):
    for i in range(0, tamanhoRam):
        ram[i] = random.randint(100, 1100)


# primeiro teste está sendo feito com 6 acessos
# parametro acessos - index:0 - indece de acesso na ram, 1 - processador  escolhido, 2 - se vai ser modificado ou n(0 ou 1) tudo isso referente a ram
# acessos = [[-1]*3]*6 nessa sintaxe ocorre um problema, os valores se repetem, os ultimos valores se repetem para todos os indices
acessos = [[-1] * 3 for i in range(0, 6)]
acessos[0][0] = 5
acessos[0][1] = 0
acessos[0][2] = 1
acessos[1][0] = 5
acessos[1][1] = 1
acessos[1][2] = 0
acessos[2][0] = 2
acessos[2][1] = 0
acessos[2][2] = 1
acessos[3][0] = 1
acessos[3][1] = 0
acessos[3][2] = 0
acessos[4][0] = 9
acessos[4][1] = 0
acessos[4][2] = 0
acessos[5][0] = 5
acessos[5][1] = 0
acessos[5][2] = 0


ram = [None]*tamanhoRam
# caches = [[LinhaCache()] * tamanhoCache for i in range(0, cpu)] nessa sintaxe estava ocorrendo um problema
caches = []
for i in range(0, cpu):
    cache = []
    for j in range(0, tamanhoCache):
        linha = LinhaCache()
        cache.append(linha)
    caches.append(cache)
adicionaRam(ram)


for i in range(0, 6):
    fifo(acessos, caches, i)
for i in range(0, cpu):
    print('Cache' + str(i) + ' ')
    for j in range(0, tamanhoCache):
        print('Linha da cache:  ' + str(j))
        print('Ocupada: ' + str(caches[i][j].ocupada))
        print('Marcador: ' + str(caches[i][j].marcador))
        print('**-**-**-**-**-**-**-**-**-')
