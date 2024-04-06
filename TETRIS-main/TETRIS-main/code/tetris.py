from tkinter import *
import random
import sqlite3


def randomPeca():
    return random.randint(1, 7)


coneccao = sqlite3.connect('pontuacoes.db')
c = coneccao.cursor()

def criarTabela():
    c.execute("CREATE TABLE IF NOT EXISTS dados (nome text, pontos integer)")
    #Cria um banco de dados pra armazenar as iniciais e a pontuação do jogador, caso ele não exista.

criarTabela()

def entrarDados(a,b):
    c.execute("INSERT INTO dados (nome, pontos) VALUES (?,?)", (a,b))
    coneccao.commit()
    #Faz as iniciais e a pontuação do jogador entrar no banco de dados.

def imprimirMelhores(a):
    cont = 0

    janela = Tk()

    Label(janela, text='SUA PONTUAÇÃO:').pack()
    Label(janela, text=a).pack()
    Label(janela, text='10 MELHORES PONTUAÇÕES:').pack()

    for row in c.execute('SELECT * FROM dados ORDER BY pontos DESC'):
        cont += 1

        colocacao = str(row)
        colocacao = colocacao.replace("('", "").replace("',", "").replace(")", "")

        if cont != 10:
            Label(janela, text=str(cont) + 'º | ' + str(colocacao)).pack()
        else:
            Label(janela, text=str(cont) + 'º| ' + str(colocacao)).pack()

        if cont == 10:
            break

    Button(janela, text='SAIR', command=quit).pack()

    janela.mainloop()

    #Imprime as 10 melhores pontuações do jogo.


# Dimensoes
lado = 30
quadrado_Largura = 10
quadrado_altura = 20
largura = lado * quadrado_Largura
altura = lado * quadrado_altura


class Peca:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        if tipo == 1:
            self.grade = [[0, 0, 1], [0, 1, 1], [0, 0, 1]]
            self.tamanho = 3
        elif tipo == 2:
            self.grade = [[0, 1, 0], [0, 1, 1], [0, 0, 1]]
            self.tamanho = 3
        elif tipo == 3:
            self.grade = [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]]
            self.tamanho = 4
        elif tipo == 4:
            self.grade = [[0, 0, 1], [0, 0, 1], [0, 1, 1]]
            self.tamanho = 3
        elif tipo == 5:
            self.grade = [[1, 1, 1], [1, 0, 0], [0, 0, 0]]
            self.tamanho = 3
        elif tipo == 6:
            self.grade = [[0, 0, 0], [0, 1, 1], [1, 1, 0]]
            self.tamanho = 3
        elif tipo == 7:
            self.grade = [[1, 1], [1, 1]]
            self.tamanho = 2

    def vira(self, tela):

        Girar_peca = [[0 for i in range(self.tamanho)] for j in range(self.tamanho)]

        for linha in range(self.tamanho):
            for coluna in range(self.tamanho):  # ver se pode virar a peça.

                if self.grade[linha][coluna] * (self.x + 1 + coluna) > quadrado_Largura - 1 and self.x >= 8 and 4 > self.tamanho > 2:
                    for x in range(self.tamanho):
                        for z in range(self.tamanho):
                            if tela.grade[self.y + linha - x][self.x + coluna - z] != 0:
                                return 0
                    while self.x == 8 and self.grade[linha][coluna] * (self.x - 1 + coluna) != 1:
                        self.esquerda(tela)


                elif self.grade[linha][coluna] * (self.x + 3 + coluna) > quadrado_Largura - 1 and self.tamanho > 3 and self.x > 6:
                    for x in range(self.tamanho):
                        for z in range(self.tamanho):
                            if tela.grade[self.y + linha+x][self.x + coluna - z] != 0:
                                return 0
                    while 8 >= self.x > 6:
                        self.esquerda(tela)

                if self.grade[linha][coluna] * (self.x - 1 + coluna) < 0 and (Girar_peca[linha][0] == 0 and self.x < 0):
                    for x in range(self.tamanho):
                        for z in range(self.tamanho):
                            if tela.grade[self.y + linha + x][self.x + coluna + z] != 0:
                                return 0
                    while self.x < 0:
                        self.direita(tela)

                elif self.grade[linha][coluna] * (self.x - 3 + coluna) < 0 and (Girar_peca[linha][0] == 0 and self.x < 0) and self.tamanho>3:
                    for x in range(self.tamanho):
                        for z in range(self.tamanho):
                            if tela.grade[self.y + linha + x][self.x + coluna + z] != 0:
                                return 0

                    while self.x < 0:
                        self.direita(tela)
                if Girar_peca[linha][coluna] == 1 and tela.grade[self.y + linha][self.x + coluna] != 0:
                    return 0

        for lin in range(self.tamanho):
            for col in range(self.tamanho):  # faz uma matriz pra girar a peça.

                Girar_peca[self.tamanho - 1 - col][lin] = self.grade[lin][col]

                if self.grade[lin][col] == 0 and (tela.grade[self.y + lin][self.x + col] != 0 or self.grade[lin][col] * (self.y + 1 + lin) >= quadrado_altura):
                    return 0

        for i in range(self.tamanho):
            for j in range(self.tamanho):  # TRANSFORMAR A PELA VIRADA NO TABULEIRO
                self.grade[i][j] = Girar_peca[i][j]
        return 1

    def desce(self, tela):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grade[i][j] * (self.y + 1 + i) >= quadrado_altura:
                    return 0  # se chegar no limite da matriz parar.
                if self.grade[i][j] == 1 and tela.grade[self.y + i + 1][
                    self.x + j] != 0:  # se tiver algo em baixo ele para.
                    return 0
        self.y += 1  # Indicando que a peça pode descer.
        return 1

    def direita(self, tela):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grade[i][j] * (self.x + 1 + j) > quadrado_Largura - 1:
                    return 0  # se chegar no limite da matriz parar.
                if self.grade[i][j] == 1 and tela.grade[self.y + i][
                    self.x + j + 1] != 0:  # se tiver algo em baixo ele para.
                    return 0
        self.x += 1  # Indicando que a peça pode ir na direita.
        return 1

    def esquerda(self, tela):
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                if self.grade[i][j] * (self.x - 1 + j) < 0:
                    return 0  # se chegar no limite da matriz parar.
                if self.grade[i][j] == 1 and tela.grade[self.y + i][
                    self.x + j - 1] != 0:  # se tiver algo em baixo ele para.
                    return 0
        self.x -= 1  # Indicando que a peça pode ir na esquerda.
        return 1


class Tela:
    def __init__(self):
        self.grade = [[0 for i in range(quadrado_Largura)] for j in range(quadrado_altura)]  # tamanho do tabuleiro.

    def elimina(self):
        eliminaLinha = []
        for lin in range(quadrado_altura - 1, 0, -1):
            for col in range(quadrado_Largura):
                if self.grade[lin][col] == 0:
                    break
                if col == quadrado_Largura - 1:
                    eliminaLinha.append(lin)
        return eliminaLinha

    def desceLinhas(self, eliminaLinha):

        for i in eliminaLinha:
            for lin in range(i, 0, -1):
                for col in range(quadrado_Largura):
                    self.grade[lin][col] = self.grade[lin - 1][col]

            for j in range(len(eliminaLinha)):
                eliminaLinha[j] += 1

            for col in range(quadrado_Largura):
                self.grade[0][col] = 0

    def addPecas(self, p):
        for i in range(p.tamanho):
            for j in range(p.tamanho):
                if p.grade[i][j] != 0:
                    self.grade[i + p.y][j + p.x] = p.grade[i][j]


class game:
    def __init__(self):
        self.window = Tk()
        self.canvas = Canvas(self.window, width=largura, height=altura, bg='black')
        self.canvas.pack()
        self.p = Peca(3, 1, randomPeca())  # posição inicial da peça...
        self.nump = 0
        self.t = Tela()

        self.window.bind('<Right>', self.moveDireita)  # ir na direita.
        self.window.bind('<Left>', self.moveEsquerda)
        self.window.bind('<Up>', self.gira)
        self.window.bind('<Down>', self.desce)

    def gira(self, event):
        self.p.vira(self.t)

    def moveEsquerda(self, event):
        self.p.esquerda(self.t)

    def moveDireita(self, event):
        self.p.direita(self.t)

    def desce(self, event):
        self.p.desce(self.t)

    def desenha(self):
        for i in range(self.p.tamanho):  # LINHA, Y é a linha. #### desenha a peça.
            for j in range(self.p.tamanho):  # COLUNA, x é a coluna.
                if self.p.grade[j][i] != 0:
                    self.canvas.create_polygon(
                        [(self.p.x + i) * lado, (self.p.y + j) * lado, (self.p.x + i) * lado + lado,
                         (self.p.y + j) * lado, (self.p.x + i) * lado + lado, (self.p.y + j) * lado + lado,
                         (self.p.x + i) * lado, (self.p.y + j) * lado + lado], fill='gray', outline='white')
            

        for lin in range(quadrado_altura):  ## cria a peça no fim do tabuleiro.
            for col in range(quadrado_Largura):
                if self.t.grade[lin][col] != 0:
                    self.canvas.create_polygon(
                        [col * lado, lin * lado, col * lado + lado, lin * lado, col * lado + lado, lin * lado + lado,
                         col * lado, lin * lado + lado], fill='red', outline='white')

    def run(self):

        tempo = 0
        pontuacao = 0
        pontuacao_anterior = 0   #Serve para a comparação entre as pontuações atual e anterior para saber quando aumentar a velocidade.
        velocidade = 20          #Velocidade inicial.
        aumentar_velocidade = 6  #Aumemento da velocidade.
        pontprovel = 5000        #Pontuação para a próxima velocidade.

        while True:
            self.canvas.delete('all')  # deletar o espaço que passou...

            if tempo == velocidade:
                FimGrade = self.p.desce(self.t)
                tempo = 0

                if FimGrade == 0:
                    self.t.addPecas(self.p)
                    LinElimina = self.t.elimina()

                    if len(LinElimina) > 0:
                        self.t.desceLinhas(LinElimina)
                        pontuacao += len(LinElimina) * 1000
                        print(pontuacao)

                        if pontuacao >= pontuacao_anterior + pontprovel and velocidade > aumentar_velocidade:
                            velocidade -= aumentar_velocidade
                            pontuacao_anterior = pontuacao
                            aumentar_velocidade -= 1


                    self.p = Peca(3, 1, randomPeca())

                    for lin in range(self.p.tamanho):
                        for col in range(self.p.tamanho):
                            if self.p.grade[lin][col] == 1 and self.t.grade[self.p.y + lin][self.p.x + col] != 0:
                                print('FIM DE JOGO.')
                                iniciais = input('Digite suas iniciais: ')
                                iniciais = iniciais.upper()
                                suapont = str(iniciais) + ' ' + str(pontuacao)
                                entrarDados(iniciais, pontuacao)
                                imprimirMelhores(suapont)
                                quit()


            else:
                tempo += 1

            self.desenha()
            self.canvas.after(30)
            self.window.update_idletasks()
            self.window.update()


g = game()
g.run()