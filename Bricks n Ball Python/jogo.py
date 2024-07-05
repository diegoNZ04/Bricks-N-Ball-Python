import pygame


# inicializar
pygame.init()

tamanho_tela = (800, 800)
tela = pygame.display.set_mode(tamanho_tela)  # criar a tela
pygame.display.set_caption('Brick N Ball Python')  # título do jogo


tamanho_bola = 15
bola = pygame.Rect(100, 500, tamanho_bola, tamanho_bola)  # definir a bola
tamanho_jogador = 100
# definir a retângulo do jogador
jogador = pygame.Rect(0, 750, tamanho_jogador, 15)

qtde_blocos_linha = 8
qtde_linhas_blocos = 5
qntde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos  # definir blocos


def criar_blocos(qnte_blocos_linha, qntde_linhas_blocos):
    altura_tela = tamanho_tela[1]
    largura_tela = tamanho_tela[0]
    distancia_entre_blocos = 5
    largura_bloco = largura_tela / 8 - distancia_entre_blocos
    altura_bloco = 15
    distancia_entre_linhas = altura_bloco + 10

    blocos = []
    # criar blocos
    for j in range(qntde_linhas_blocos):
        for i in range(qnte_blocos_linha):
            # criar bloco
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos),
                                j * distancia_entre_linhas, largura_bloco, altura_bloco)
            # adicionar bloco na lista de blocos
            blocos.append(bloco)

    return blocos


# cores seguem o padrão rgb
cores = {
    'branca': (255, 255, 255),
    'preta': (0, 0, 0),
    'amarela': (255, 255, 0),
    'azul': (0, 0, 255),
    'verde': (0, 255, 0)
}

fim_jogo = False
pontuacao = 0
# definir como lista para ser alterada posteriormente, eixo (x, y)
movimento_bola = [1, -1]

# criar as regras do jogo


def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:  # pressionar teclar
        if evento.key == pygame.K_RIGHT:
            # delimitar barreira de tela a direita
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x = jogador.x + 3
        if evento.key == pygame.K_LEFT:  # delimitar barreira de tela a esquerda
            if jogador.x > 0:
                jogador.x = jogador.x - 3


def movimentar_bola(bola):
    movimento = movimento_bola  # transformar variavel em espoco local
    bola.x += movimento[0]
    bola.y += movimento[1]
    # inversão de eixos
    if bola.x <= 0:
        movimento[0] = - movimento[0]
    if bola.y <= 0:
        movimento[1] = - movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = - movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento = None
    # definir colisões
    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = - movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = - movimento[1]

    return movimento


def atualizar_pontuacao(pontuacao):
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f'Pontuação: {pontuacao}', 1, cores['amarela'])
    tela.blit(texto, (0, 780))
    if pontuacao >= qntde_total_blocos:
        return True
    else:
        return False


# desenhar os elementos na tela
def desenhar_inicio_jogo():
    tela.fill(cores['preta'])  # tela
    pygame.draw.rect(tela, cores['azul'], jogador)  # barra do jogador
    pygame.draw.rect(tela, cores['branca'], bola)  # bola


def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores['verde'], bloco)  # bloco


blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos)

# criar um loop infinito
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao(qntde_total_blocos - len(blocos))
    for evento in pygame.event.get():  # armazenar interações do usuário
        if evento.type == pygame.QUIT:  # se usuário fechar o jogo
            fim_jogo = True  # encerrar jogo
    movimentar_jogador(evento)

    movimento_bola = movimentar_bola(bola)
    if not movimento_bola:
        fim_jogo = True

    pygame.time.wait(1)  # atualizar a cada 1 milisegundo os comandos do jogo
    pygame.display.flip()  # atualiza a tela do jogo

pygame.quit()
