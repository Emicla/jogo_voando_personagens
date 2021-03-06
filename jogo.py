import pygame, random, os

os.system("cls")

from Funcoes.funcoes_gerais import armazenar, verificaInf

nomeJogador = verificaInf("Informe seu nome:")

while True:
    email = verificaInf("Informe seu email: ")
    if "@" not in email or ".com" not in email:
        print("Escreva corretamente seu email")

    elif email.index(".com") !=len(email)-4 or email.index("@") == 1:
        print("Email inválido")

    else:
        break

armazenar(nomeJogador, "Registro de acessos.txt")
armazenar(email, "Registro de acessos.txt")

from Funcoes.funcoes_telas import escreveTela, telaMenu, telaLoja, telaComoJogar, morreu

pygame.init()

largura_tela = 1200
altura_tela = 600
tamanho = (largura_tela, altura_tela)

pygame_display = pygame.display
pygame_display.set_caption("Voando com personagens")

gameDisplay = pygame.display.set_mode(tamanho)
incone = pygame.image.load("Imagens/controle.ico")
pygame_display.set_icon(incone)

clock = pygame.time.Clock()

corLetra = (255, 255, 255)

pontos = 0

personagem = "insectoide"

def jogo(nomePersonagem):
    fundo = pygame.image.load("Imagens/Cenarios/%s cidade.jpg"%nomePersonagem)

    jogador = pygame.image.load("Imagens/Personagens/"+ nomePersonagem + ".png")
    jogadorPosX = 400
    jogadorPosY = 400
    movimentoXPersonagem = 0
    movimentoYPersonagem = 0
    velocidade = 5
    jogadorLargura =  100
    jogadorAltura = 136

    missil = pygame.image.load("Imagens/Laiser.png")
    missilPosX = 0
    missilPosY = 0
    movimentoXMissil = -5
    missilLargura = 150
    missilAltura = 40

    robo = pygame.image.load("Imagens/robo vilgax.png")
    roboAltura = 217
    roboLargura = 198
    roboPosX = 20
    roboPosY = 100
    movimentoXRobo = 5

    missilLiberado = False
    velocidadeIncrementoRobo = 1
    velocidadeIncrementoMissil = -8
    pontosJogo = 0

    pygame.mixer.music.load("Sons/" + nomePersonagem + ".mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    virou = False

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if virou == True:
                        jogador = pygame.transform.flip(jogador, True, False)
                        virou = False
                    movimentoXPersonagem = - velocidade
                    velocidadeIncrementoMissil = -8

                elif event.key == pygame.K_RIGHT:
                    if virou == False:
                        jogador = pygame.transform.flip(jogador, True, False)
                        virou = True
                    movimentoXPersonagem = velocidade
                    velocidadeIncrementoMissil = 8
                
                elif event.key == pygame.K_UP:
                    movimentoYPersonagem = -velocidade

                elif event.key == pygame.K_DOWN:
                    movimentoYPersonagem = velocidade
                
                elif event.key == pygame.K_a and missilLiberado == False:
                    missilLiberado = True
                    missilPosX = jogadorPosX
                    missilPosY = jogadorPosY
                    movimentoXMissil = velocidadeIncrementoMissil

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    movimentoXPersonagem = 0
                    movimentoYPersonagem = 0

        jogadorPosX += movimentoXPersonagem
        jogadorPosY += movimentoYPersonagem

        # Colisão com bordas da tela
        if jogadorPosX < 0:
            jogadorPosX = 0

        elif jogadorPosX >= largura_tela - jogadorLargura:
            jogadorPosX = largura_tela - jogadorLargura

        if jogadorPosY < 0:
            jogadorPosY = 0

        elif jogadorPosY >= altura_tela - jogadorAltura:
            jogadorPosY = altura_tela - jogadorAltura
        
        # Colisão com missil
        pixelsXjogador = list(range(jogadorPosX, jogadorPosX + jogadorLargura + 1))
        pixelsYjogador = list(range(jogadorPosY, jogadorPosY + jogadorAltura + 1))

        pixelsXRobo = list(range(roboPosX, roboPosX + roboLargura + 1))
        pixelsYRobo = list(range(roboPosY, roboPosY + roboAltura + 1))

        pixelsXMissel = list(range(missilPosX, missilPosX + missilLargura + 1))
        pixelsYMissel = list(range(missilPosY, missilPosY + missilAltura + 1))

        if len(list(set(pixelsYRobo) & set(pixelsYjogador))) > 60 and len(list(set(pixelsXRobo) & set(pixelsXjogador))) > 65:
                return ["Morreu", pontosJogo]
        
        if roboPosX > largura_tela or roboPosX < 0 - roboLargura:
            movimentoXRobo = -movimentoXRobo
            roboPosY = random.randrange(0, altura_tela - roboAltura)
            robo = pygame.transform.flip(robo, True, False)
        
        elif missilLiberado == True:
            if len(list(set(pixelsXRobo) & set(pixelsXMissel))) > 25 and len(list(set(pixelsYRobo) & set(pixelsYMissel))) > 25:
                missilLiberado = False
                missilPosX = 0
                missilPosY = 0
                pontosJogo = pontosJogo + 1
                roboPosY = random.randrange(0, altura_tela - roboAltura)
                numeroAleatorio = random.randrange(1, 3)
                movimentoXRobo = movimentoXRobo + velocidadeIncrementoRobo

                if numeroAleatorio == 1:
                    roboPosX = 0 - roboLargura
                    if movimentoXRobo < 0:
                        movimentoXRobo = -(movimentoXRobo - velocidadeIncrementoRobo)
                    else:
                        movimentoXRobo = movimentoXRobo + velocidadeIncrementoRobo
                else:
                    roboPosX = largura_tela
                    if movimentoXRobo > 0:
                        movimentoXRobo = -(movimentoXRobo + velocidadeIncrementoRobo)
                    else:
                        movimentoXRobo = movimentoXRobo - velocidadeIncrementoRobo

        roboPosX = roboPosX + movimentoXRobo

        # Desenhando na tela as imagens
        gameDisplay.blit(fundo, (0, 0))
        gameDisplay.blit(robo, (roboPosX, roboPosY))
        gameDisplay.blit(jogador, (jogadorPosX, jogadorPosY))

        # Escrevendo na tela
        gameDisplay.blit(escreveTela("Pontos: %d"%pontosJogo, corLetra, 20), (20, 20))

        if missilLiberado == True and missilPosX > 0 and missilPosX + missilLargura < largura_tela:
            gameDisplay.blit(missil, (missilPosX, missilPosY))
            
            missilPosX += movimentoXMissil
        else:
            missilLiberado = False

        pygame_display.update()
        clock.tick(60)

telaAtual = "Menu"

while True:
    if telaAtual == "Menu":
        telaAtual = telaMenu(pontos)

    elif telaAtual == "Jogo":
        lista = jogo(personagem)
        telaAtual = lista[0]
        pontos += lista[1]
    
    elif telaAtual == "Loja":
        lista = telaLoja(pontos)
        telaAtual = lista[0]
        personagem = lista[1]
    
    elif telaAtual == "Como jogar":
        telaAtual = telaComoJogar()

    elif telaAtual == "Morreu":
        telaAtual = morreu(pontos)