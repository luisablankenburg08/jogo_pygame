import pygame
import sys
import json
import textwrap

pygame.init()

# === CORES ===
preto, cinza, branco = (0,0,0), (128,128,128), (255,255,255)
vermelho, verde, azul = (255,0,0), (0,255,0), (0,0,255)
amarelo, ciano, magenta = (255,255,0), (0,255,255), (255,0,255)

# === TELA ===
largura_tela, altura_tela = 1400,800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Musicalizando no Céu")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 28)
fonte_menu = pygame.font.SysFont(None, 48)
fonte_intro = pygame.font.SysFont(None, 72 )
inicio_modo = 0

# == BARRA PROGRESSÃO === 
tamanho = largura_tela/9
def desenhar_barra_azul():
    largura_barra = largura_tela
    altura_barra = 20
    x, y = 0, 0 
    pygame.draw.rect(tela, ciano, (x, y, largura_barra, altura_barra))

def desenhar_barra_amarela():
    largura_barra = tamanho
    altura_barra = 20
    x, y = 0, 0 
    pygame.draw.rect(tela, amarelo, (x, y, largura_barra, altura_barra))

# === FUNÇÕES AUXILIARES ===
def criar_botao(texto, x, y, w=300, h=40, cor=ciano, cor_texto=preto):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)
    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    return rect, surf, texto_render, texto_rect

def desenhar_campo(label, rect, valor, ativo=False):
    tela.blit(FONT.render(label, True, preto), (rect.x, rect.y - 30))
    pygame.draw.rect(tela, ciano if not ativo else amarelo, rect, 0)
    tela.blit(FONT.render(valor, True,preto), (rect.x+5, rect.y+5))

def salvar_dados(nome, escola, serie):
    dados_novos = {"nome": nome, "escola": escola, "serie": serie}

    try:
        with open("dados.json", "r", encoding="utf-8") as f:
            dados_existentes = json.load(f)
            if not isinstance(dados_existentes, list):
                dados_existentes = [dados_existentes]
    except (FileNotFoundError, json.JSONDecodeError):
        dados_existentes = []
    dados_existentes.append(dados_novos)
    with open("dados.json", "w", encoding="utf-8") as f:
        json.dump(dados_existentes, f, indent=4, ensure_ascii=False)

def criar_nuvem(texto, x, y, w=200, h=20, cor=branco, cor_texto=ciano):
    rect_nuvem = pygame.Rect(x, y, w, h)
    surf_nuvem = pygame.Surface((w, h))
    surf_nuvem.fill(cor)
    texto_nuvem_render = fonte_menu.render(texto, True, cor_texto)
    texto_nuvem_rect = texto_nuvem_render.get_rect(center=rect_nuvem.center)
    return rect_nuvem, surf_nuvem, texto_nuvem_render, texto_nuvem_rect


def quadro_explicativo(texto, x, y, w=300, h=40, cor=amarelo, cor_texto=preto, border_radius=20):
    rect_quadro = pygame.Rect(x, y, w, h)
    surf_quadro = pygame.Surface((w, h))
    surf_quadro.fill(cor)
    texto_render_quadro = fonte_menu.render(texto, True, cor_texto)
    texto_rect_quadro = texto_render_quadro.get_rect(center=rect_quadro.center)
    return rect_quadro, surf_quadro, texto_render_quadro, texto_rect_quadro

# === IMAGENS ===
background = pygame.transform.scale(pygame.image.load("fundo_menu.png"), (largura_tela, altura_tela))
quadro_menu = pygame.transform.scale(pygame.image.load("quadro_menu.png"), (largura_tela//3, altura_tela//2 + 50))
background_fase0 = pygame.transform.scale(pygame.image.load("fundo.png"), (largura_tela, altura_tela))
quadro_fase0 = pygame.transform.scale(pygame.image.load("quadro_fase0.png"), (largura_tela//3, altura_tela//2 + 50))
fundo_fases = pygame.transform.scale(pygame.image.load("fundo_fases.png"), (largura_tela, altura_tela))
nuvem = pygame.transform.scale(pygame.image.load("nuvem.png"), (300,110))
cadeado = pygame.transform.scale(pygame.image.load("cadeado.png"), (50,75))
bichinho1 = pygame.transform.scale(pygame.image.load("bichinho1.png"), (200,180))
bichinho2 = pygame.transform.scale(pygame.image.load("bichinho2.png"), (200,180))
cadeadoaberto = pygame.transform.scale(pygame.image.load("cadeadoaberto.png"), (50,75))
bandeira = pygame.transform.scale(pygame.image.load("bandeira.png"), (120,110))
som = pygame.transform.scale(pygame.image.load("som.png"), (300,300))
botao_rasp_amarelo = pygame.transform.scale(pygame.image.load("botao_rasp_amarelo.png"), (200,200))
botao_rasp_azul = pygame.transform.scale(pygame.image.load("botao_rasp_azul.png"), (200,200))

# === BOTÕES ===
botao_sair_rect, surf_sair, txt_sair, txt_sair_rect = criar_botao("Sair", largura_tela//2-150, altura_tela//2+150)
botao_ajuda_rect, surf_ajuda, txt_ajuda, txt_ajuda_rect = criar_botao("Ajuda", largura_tela//2-150, altura_tela//2+50)
botao_jogar_rect, surf_jogar, txt_jogar, txt_jogar_rect = criar_botao("Jogar", largura_tela//2-150, altura_tela//2-50)

botao_fase1_rect, surf_fase1, txt_fase1, txt_fase1_rect = criar_nuvem("Fase 1",  largura_tela//4, altura_tela//2+100, 200, 20)
botao_nuvem2_rect, surf_nuvem2, txt_nuvem2, txt_nuvem2_rect = criar_nuvem("Fase 2",  largura_tela//2, altura_tela//2, 200, 20)
botao_nuvem3_rect, surf_nuvem3, txt_nuvem3, txt_nuvem3_rect = criar_nuvem("Fase 3",  largura_tela-400, altura_tela//2-120, 200, 20)

botao_comecar_rect, surf_comecar, txt_comecar, txt_comecar_rect = criar_botao("Começar", largura_tela-300, altura_tela-150, 240, 56)
botao_voltar_rect, surf_voltar, txt_voltar, txt_voltar_rect = criar_botao("Voltar",(largura_tela//15), (altura_tela//17), 240, 56)
botao_avancar_rect, surf_avancar, txt_avancar, txt_avancar_rect = criar_botao("Avançar", largura_tela//2-120, altura_tela-100, 240, 56)

som1_rect = som.get_rect(topleft=(300, 300))
som2_rect = som.get_rect(topleft=(900, 300))
som3_rect = som.get_rect(topleft=(largura_tela//2-150, 300))

rasp_amarelo_rect = botao_rasp_amarelo.get_rect(topleft=(350,400))
rasp_azul_rect = botao_rasp_azul.get_rect(topleft=(950,400))

# === QUADROS EXPLICATIVOS ===
quadro_explicativo1_rect, surf_quadro1, txt_quadro1, txt_quadro1_rect = quadro_explicativo("Escute os sons, um de cada vez.", largura_tela//2-300, 100, 600,100)

quadro_explicativo_p1_rect, surf_quadro_p1, txt_quadro_p1, txt_quadro_p1_rect = quadro_explicativo("Qual som que você ouviu é mais agudo?", largura_tela//2-350, 100, 700,100)

quadro_explicativo2_rect, surf_quadro2, txt_quadro2, txt_quadro2_rect = quadro_explicativo("Escute a música", largura_tela//2-200, 100, 400,100)

quadro_explicativo_p2_rect, surf_quadro_p2, txt_quadro_p2, txt_quadro_p2_rect = quadro_explicativo("Clique nos botões correspondetes aos instrumentos que você escutou ", largura_tela//2-600, 100, 1200,100)

quadro_explicativo3_rect, surf_quadro3, txt_quadro3, txt_quadro3_rect = quadro_explicativo("Escute as melodias", largura_tela//2-300, 100, 400,100)

quadro_explicativo_p3_rect, surf_quadro_p3, txt_quadro_p3, txt_quadro_p3_rect = quadro_explicativo("Clique no botão que corresponde a melodia que você acabou de escutar", largura_tela//2-600, 100, 1200,100)

# === TEXTOS ===
texto_aqui_surface = FONT.render("Você está aqui!", True, preto)
texto_aqui_rect = texto_aqui_surface.get_rect()
texto_aqui_rect.center = ((largura_tela-1200, altura_tela-100))

texto_som1_surface = FONT.render("SOM 1", True, preto)
texto_som1_rect = texto_som1_surface.get_rect()
texto_som1_rect.center = ((450, 350))

texto_som2_surface = FONT.render("SOM 2", True, preto)
texto_som2_rect = texto_som2_surface.get_rect()
texto_som2_rect.center = ((1050, 350))

texto_som3_surface = FONT.render("MÚSICA 1", True, preto)
texto_som3_rect = texto_som2_surface.get_rect()
texto_som3_rect.center = ((largura_tela//2-20, 350))

"""texto_intro1 = "FASE 1"
linhas_texto_intro1 = texto_intro1.split('\n')
superficies_texto_intro1 = [fonte_intro.render(linha, True, preto) for linha in linhas_texto_intro1]
velocidade_rolagem_intro1 = 0.09
posicao_x = largura_tela """

# === AJUDA ===
texto_ajuda = (
    "Bem vindos ao jogo Musicalizando no Céu! \n"
    "\n"
    "Hoje, você embarcará em uma aventura através de músicas e atividades. \n "
    "\n"
    "O jogo constitui de 3 fases com atividades em que você deve prestar muita atenção. \n "
    "\n"
    "Espero que aproveite a experiência e se dedique ao máximo para chegar ao final. \n " 
    "\n"
    "Este é o Projeto Integrador da aluna Luisa Narvaz Blankenbug, \n estudante do 2º ano do ensino médio do Instituto Federal de Santa Catarina de Garopaba/SC. \n"
    "\n"
    "Trata-se de uma proposta de melhoria do desempenho infantil nas escolas, \n aprimorando o foco e atenção de crianças em atividades que precisam ser realizadas. \n "
    "\n"
    "\n"
    "Criador: Luisa Narvaz Blankenburg\n"
    "Projeto: Música, Jogo e Atenção: uma proposta educacional com Raspberry Pi.\n"
    "Professor orientador: André Luiz Silva de Moraes\n"
    "Instituição: Instituto Federal de Santa Catarina - Câmpus Garopaba")

linhas_texto_ajuda = texto_ajuda.split('\n')
superficies_texto_ajuda = [FONT.render(linha, True, preto) for linha in linhas_texto_ajuda]
velocidade_rolagem_ajuda = 1.2
posicao_y = altura_tela

# === CAMPOS DE TEXTO FASE 0 ===
nome_rect   = pygame.Rect(largura_tela//2-150, altura_tela//2-50, 300, 40)
escola_rect = pygame.Rect(largura_tela//2-150, altura_tela//2+50, 300, 40)
serie_rect  = pygame.Rect(largura_tela//2-150, altura_tela//2+150, 300, 40)

# SÉRIE - CAIXA DE SELEÇÃO
opcoes_serie = ["1º ano", "2º ano", "3º ano", "4º ano"]
dropdown_aberto = False
opcao_hover = -1

player_name, player_school, player_serie = "", "", ""
active_field, error_msg, mode = None, "", "menu"

# === SONS ===
click_sound = pygame.mixer.Sound("botao1.mp3")
som_start = pygame.mixer.Sound("botao2.mp3")
som_agudo1_fase1 = pygame.mixer.Sound("agudo1.mp3")
som_grave1_fase1 = pygame.mixer.Sound("grave1.mp3")


# === LOOP PRINCIPAL ===
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if mode == "menu":
                if botao_sair_rect.collidepoint(event.pos): rodando = False
                elif botao_ajuda_rect.collidepoint(event.pos): click_sound.play(); mode = "ajuda"
                elif botao_jogar_rect.collidepoint(event.pos): click_sound.play(); mode = "fase0"

            elif mode == "ajuda":
                if botao_voltar_rect.collidepoint(event.pos): click_sound.play(); mode = "menu"
                
            elif mode == "fase0":
                if botao_voltar_rect.collidepoint(event.pos): click_sound.play(); mode = "menu"
                elif nome_rect.collidepoint(event.pos): active_field = "nome"
                elif escola_rect.collidepoint(event.pos): active_field = "escola"
                elif serie_rect.collidepoint(event.pos):
                    dropdown_aberto = not dropdown_aberto
                elif dropdown_aberto:
                    for i, opcao in enumerate(opcoes_serie):
                        opt_rect = pygame.Rect(serie_rect.x, serie_rect.y + (i+1)*40, serie_rect.width, 40)
                        if opt_rect.collidepoint(event.pos):
                            player_serie = opcao
                            dropdown_aberto = False
                            break
                elif botao_comecar_rect.collidepoint(event.pos):
                    click_sound.play()
                    if player_name.strip() and player_school.strip() and player_serie.strip():
                        salvar_dados(player_name, player_school, player_serie)
                        mode, error_msg = "menu_fase1", ""
                    else:
                        error_msg = "Preencha todos os campos."
                else: active_field = None
                
            elif mode == "menu_fase1":
                if botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu"
                elif botao_fase1_rect.collidepoint(event.pos):
                    som_start.play()
                    mode = "introducao_fase1"
                    inicio_modo = pygame.time.get_ticks()
                 
            elif mode == "introducao_fase1":
                tempo_decorrido = pygame.time.get_ticks() - inicio_modo  # em milissegundos
                if tempo_decorrido > 2000: 
                    mode = "fase1_1"
                    inicio_modo = pygame.time.get_ticks()  # reinicia o contador se quiser usar de novo

            # === FASE 1 ===
            elif mode == "fase1_1":

                if botao_voltar_rect.collidepoint(event.pos):
                    if som_agudo1_fase1.get_num_channels() > 0 or som_grave1_fase1.get_num_channels() > 0:  
                        som_agudo1_fase1.stop()
                        som_grave1_fase1.stop(); click_sound.play(); mode = "menu_fase1_1"
                    else:
                        click_sound.play(); mode = "menu_fase1"

                elif botao_avancar_rect.collidepoint(event.pos):
                    if som_agudo1_fase1.get_num_channels() > 0 or som_grave1_fase1.get_num_channels() > 0:  
                        som_agudo1_fase1.stop()
                        som_grave1_fase1.stop(); click_sound.play(); mode = "pergunta_fase1_1"
                    else:
                        click_sound.play(); mode = "pergunta_fase1_1"

                elif som1_rect.collidepoint(event.pos):
                    if som_grave1_fase1.get_num_channels() > 0:  
                        som_grave1_fase1.stop()
                    som_agudo1_fase1.play()

                elif som2_rect.collidepoint(event.pos):
                    if som_agudo1_fase1.get_num_channels() > 0:  
                        som_agudo1_fase1.stop()
                    som_grave1_fase1.play()
            
            elif mode == "pergunta_fase1_1":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase1_2"

            elif mode == "fase1_2":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase1_2"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase1"
             
            elif mode == "pergunta_fase1_2":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase1_3"

            elif mode == "fase1_3":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase1_3"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase1"

            elif mode == "pergunta_fase1_3":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase2"
            #=== FIM DA FASE 1 ===
            
            elif mode == "menu_fase2":
                if botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu"
                elif botao_nuvem2_rect.collidepoint(event.pos):click_sound.play(); mode = "introducao_fase2"
                elif botao_fase1_rect.collidepoint(event.pos):click_sound.play(); mode = "introducao_fase1"

            elif mode == "introducao_fase2":
                tempo_decorrido = pygame.time.get_ticks() - inicio_modo  # em milissegundos
                if tempo_decorrido > 2000: 
                    mode = "fase2_1"
                    inicio_modo = pygame.time.get_ticks()  # reinicia o contador se quiser usar de novo

            # === FASE 2 ===
            elif mode == "fase2_1":
                if botao_voltar_rect.collidepoint(event.pos): click_sound.play(); mode = "menu_fase2"
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase2_1"

            elif mode == "pergunta_fase2_1":
                 if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase2_2"

            elif mode == "fase2_2":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase2_2"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase2"
             
            elif mode == "pergunta_fase2_2":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase2_3"

            elif mode == "fase2_3":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase2_3"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase2"

            elif mode == "pergunta_fase2_3":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase3" 
            #=== FIM DA FASE 2 ===

            elif mode == "menu_fase3":
                if botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu"
                elif botao_nuvem3_rect.collidepoint(event.pos):click_sound.play(); mode = "introducao_fase3"
                elif botao_nuvem2_rect.collidepoint(event.pos):click_sound.play(); mode = "introducao_fase2"
                elif botao_fase1_rect.collidepoint(event.pos):click_sound.play(); mode = "introducao_fase1"

            elif mode == "introducao_fase3":
                tempo_decorrido = pygame.time.get_ticks() - inicio_modo  # em milissegundos
                if tempo_decorrido > 2000: 
                    mode = "fase3_1"
                    inicio_modo = pygame.time.get_ticks()  # reinicia o contador se quiser usar de novo

            # === FASE 3 ===
            elif mode == "fase3_1":
                if botao_voltar_rect.collidepoint(event.pos): click_sound.play(); mode = "menu_fase3"
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase3_1"

            elif mode == "pergunta_fase3_1":
                 if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase3_2"

            elif mode == "fase3_2":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase3_2"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase3"
             
            elif mode == "pergunta_fase3_2":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "fase3_3"

            elif mode == "fase3_3":
                if botao_avancar_rect.collidepoint(event.pos): click_sound.play(); mode = "pergunta_fase3_3"
                elif botao_voltar_rect.collidepoint(event.pos):click_sound.play(); mode = "menu_fase3"

            elif mode == "pergunta_fase3_3":
                if botao_avancar_rect.collidepoint(event.pos):click_sound.play(); mode = "parabens" 
            #=== FIM DA FASE 3 ===

            #elif mode == "parabens":
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: mode = "menu"
            elif mode == "fase0":
                if active_field == "nome":
                    if event.key == pygame.K_BACKSPACE: player_name = player_name[:-1]
                    elif event.key != pygame.K_RETURN and len(player_name)<32: player_name += event.unicode
                elif active_field == "escola":
                    if event.key == pygame.K_BACKSPACE: player_school = player_school[:-1]
                    elif event.key != pygame.K_RETURN and len(player_school)<32: player_school += event.unicode

    # === DESENHOS ===

    # === MENU ===
    if mode == "menu":
        tela.blit(background, (0, 0))
        tela.blit(quadro_menu, ((largura_tela - quadro_menu.get_width())//2, (altura_tela - quadro_menu.get_height())//2))
        for surf, rect, txt, txt_rect in [(surf_sair, botao_sair_rect, txt_sair, txt_sair_rect),
                                        (surf_ajuda, botao_ajuda_rect, txt_ajuda, txt_ajuda_rect),
                                        (surf_jogar, botao_jogar_rect, txt_jogar, txt_jogar_rect)]:
            tela.blit(surf, rect.topleft)
            tela.blit(txt, txt_rect)

    # === AJUDA ===
    elif mode == "ajuda":

        tela.blit(fundo_fases, (0, 0))
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)
        
        posicao_atual_ajuda = posicao_y 
        for superficie in superficies_texto_ajuda:
            rect_texto_ajuda = superficie.get_rect(center=(largura_tela//2, posicao_atual_ajuda))
            tela.blit(superficie, rect_texto_ajuda)
            posicao_atual_ajuda += 40

        posicao_y -= velocidade_rolagem_ajuda
        if posicao_atual_ajuda < 0:
            posicao_y = altura_tela

    # === FASE 0 ===
    elif mode == "fase0":
        tela.blit(background_fase0, (0, 0))
        tela.blit(quadro_fase0, ((largura_tela - quadro_menu.get_width())//2, (altura_tela - quadro_menu.get_height())//2))

        desenhar_campo("Nome:", nome_rect, player_name, active_field=="nome")
        desenhar_campo("Escola:", escola_rect, player_school, active_field=="escola")
        desenhar_campo("Série:", serie_rect, player_serie, False)

        # Dropdown se aberto
        if dropdown_aberto:
            for i, opcao in enumerate(opcoes_serie):
                opt_rect = pygame.Rect(serie_rect.x, serie_rect.y + (i+1)*40, serie_rect.width, 40)
                pygame.draw.rect(tela, amarelo, opt_rect)
                tela.blit(FONT.render(opcao, True, preto), (opt_rect.x+5, opt_rect.y+5))

        pygame.draw.rect(tela, ciano, botao_comecar_rect)
        tela.blit(txt_comecar, txt_comecar_rect)

        if error_msg: tela.blit(FONT.render(error_msg, True, vermelho), (nome_rect.x, botao_comecar_rect.y+60))

        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

    # === MENU FASES - 1 ===
    elif mode == "menu_fase1":
        tela.blit(fundo_fases, (0,0))

        tela.blit(nuvem, (largura_tela//4-50, altura_tela//2+50))
        pygame.draw.rect(tela, branco, botao_fase1_rect)
        tela.blit(txt_fase1, txt_fase1_rect)
            
        tela.blit(nuvem, (largura_tela//2-50, altura_tela//2-50))
        pygame.draw.rect(tela, branco, botao_nuvem2_rect)
        tela.blit(txt_nuvem2, txt_nuvem2_rect)
        tela.blit(cadeado, (largura_tela//2-50, altura_tela//2-50))

        tela.blit(nuvem, (largura_tela//2+250, altura_tela//2-170))
        pygame.draw.rect(tela, branco, botao_nuvem3_rect)
        tela.blit(txt_nuvem3, txt_nuvem3_rect)
        tela.blit(cadeado, (largura_tela//2+250, altura_tela//2-170))    

        tela.blit(bichinho1, ((largura_tela//15), altura_tela//2+100))
        tela.blit(texto_aqui_surface, texto_aqui_rect)

        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        tela.blit(bandeira, (largura_tela-110,0))

    # === INTRODUÇÃO FASE 1 ===
    elif mode == "introducao_fase1":
        tela.blit(background_fase0, (0, 0))
         # posicao_atual_intro1 = posicao_x 
          #for superficie in superficies_texto_intro1:
           #   rect_texto_intro1 = superficie.get_rect(center=(altura_tela//2, posicao_atual_intro1))
            #  tela.blit(superficie, rect_texto_intro1)
            #  posicao_atual_intro1 += 20

         # posicao_x -= velocidade_rolagem_intro1
         # if posicao_atual_intro1 < 0:
           #   posicao_x = largura_tela

    # === FASE 1_1 ===
    elif mode == "fase1_1":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-300 + 5, 100 + 5, 600 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro1, txt_quadro1_rect)

        #botões de som
        tela.blit(som, som1_rect)
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(som, som2_rect)
        tela.blit(texto_som2_surface, texto_som2_rect)


    # === PERGUNTA FASE 1_1 ===
    elif mode == "pergunta_fase1_1":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-350 + 5, 100 + 5, 700 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p1, txt_quadro_p1_rect)

        #botões raspberry de opção
        tela.blit(botao_rasp_amarelo, (350,400))
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(botao_rasp_azul, (950,400))
        tela.blit(texto_som2_surface, texto_som2_rect)

 # === FASE 1_2 ===
    elif mode == "fase1_2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*2
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-300 + 5, 100 + 5, 600 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro1, txt_quadro1_rect)
        
        #botões de som
        tela.blit(som, som1_rect)
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(som, som2_rect)
        tela.blit(texto_som2_surface, texto_som2_rect)

    # === PERGUNTA FASE 1_2 ===
    elif mode == "pergunta_fase1_2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*2
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-350 + 5, 100 + 5, 700 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p1, txt_quadro_p1_rect)

        #botões raspberry de opção
        tela.blit(botao_rasp_amarelo, (350,400))
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(botao_rasp_azul, (950,400))
        tela.blit(texto_som2_surface, texto_som2_rect)


 # === FASE 1_3 ===
    elif mode == "fase1_3":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*3
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-300 + 5, 100 + 5, 600 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro1, txt_quadro1_rect)

        #botões de som
        tela.blit(som, som1_rect)
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(som, som2_rect)
        tela.blit(texto_som2_surface, texto_som2_rect)

    # === PERGUNTA FASE 1_3 ===
    elif mode == "pergunta_fase1_3":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*3
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p1_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-350 + 5, 100 + 5, 700 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p1, txt_quadro_p1_rect)

        #botões raspberry de opção
        tela.blit(botao_rasp_amarelo, (350,400))
        tela.blit(texto_som1_surface, texto_som1_rect)

        tela.blit(botao_rasp_azul, (950,400))
        tela.blit(texto_som2_surface, texto_som2_rect)

    # === MENU FASES - 2 ===
    elif mode == "menu_fase2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #nuvem fase 1
        tela.blit(nuvem, (largura_tela//4-50, altura_tela//2+50))
        pygame.draw.rect(tela, branco, botao_fase1_rect)
        tela.blit(txt_fase1, txt_fase1_rect)

        #nuvem fase 2 
        tela.blit(nuvem, (largura_tela//2-50, altura_tela//2-50))
        pygame.draw.rect(tela, branco, botao_nuvem2_rect)
        tela.blit(txt_nuvem2, txt_nuvem2_rect)
        tela.blit(cadeadoaberto, (largura_tela//2-50, altura_tela//2-70))

        #nuvem fase 3 
        tela.blit(nuvem, (largura_tela//2+250, altura_tela//2-170))
        pygame.draw.rect(tela, branco, botao_nuvem3_rect)
        tela.blit(txt_nuvem3, txt_nuvem3_rect)

        #cadeado fase 3
        tela.blit(cadeado, (largura_tela//2+250, altura_tela//2-170)) 
   
        #bichinho na nuvem 2
        tela.blit(bichinho2, (largura_tela//4-20, altura_tela//2-(90)))

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #bandeira de chegada
        tela.blit(bandeira, (largura_tela-110,0))

    # === INTRODUÇÃO FASE 2 ===
    elif mode == "introducao_fase2":
        tela.blit(background_fase0, (0, 0))

    # === FASE 2_1 ===
    elif mode == "fase2_1":
        #fundo
        tela.blit(fundo_fases, (0,0))
        
        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*4
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro2, txt_quadro2_rect)

        #botão de som
        tela.blit(som, som3_rect)
        tela.blit(texto_som3_surface, texto_som3_rect)

    # === PERGUNTA FASE 2_1 ===
    elif mode == "pergunta_fase2_1":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*4
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p2, txt_quadro_p2_rect)

        #botões raspberry de opção

    # === FASE 2_2 ===
    elif mode == "fase2_2":
        #fundo
        tela.blit(fundo_fases, (0,0))
        
        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*5
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro2, txt_quadro2_rect)

        #botão de som
        tela.blit(som, som3_rect)
        tela.blit(texto_som3_surface, texto_som3_rect)

    # === PERGUNTA FASE 2_2 ===
    elif mode == "pergunta_fase2_2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*5
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p2, txt_quadro_p2_rect)

        #botões raspberry de opção

    # === FASE 2_3 ===
    elif mode == "fase2_3":
        #fundo
        tela.blit(fundo_fases, (0,0))
        
        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*6
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro2, txt_quadro2_rect)

        #botão de som
        tela.blit(som, som3_rect)
        tela.blit(texto_som3_surface, texto_som3_rect)

    # === PERGUNTA FASE 2_3 ===
    elif mode == "pergunta_fase2_3":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*6
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p2_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p2, txt_quadro_p2_rect)

        #botões raspberry de opção

    # === MENU FASES - 3 ===
    elif mode == "menu_fase3":
        tela.blit(fundo_fases, (0,0))

        tela.blit(nuvem, (largura_tela//4-50, altura_tela//2+50))
        pygame.draw.rect(tela, branco, botao_fase1_rect)
        tela.blit(txt_fase1, txt_fase1_rect)
            
        tela.blit(nuvem, (largura_tela//2-50, altura_tela//2-50))
        pygame.draw.rect(tela, branco, botao_nuvem2_rect)
        tela.blit(txt_nuvem2, txt_nuvem2_rect)

        tela.blit(nuvem, (largura_tela//2+250, altura_tela//2-170))
        pygame.draw.rect(tela, branco, botao_nuvem3_rect)
        tela.blit(txt_nuvem3, txt_nuvem3_rect)
        tela.blit(cadeadoaberto, (950, 200))   

        tela.blit(bichinho2, (700, 200))

        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        tela.blit(bandeira, (largura_tela-110,0))

    # === INTRODUÇÃO FASE 3 ===
    elif mode == "introducao_fase3":
        tela.blit(background_fase0, (0, 0))

    # === FASE 3_1 ===
    elif mode == "fase3_1":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*7
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro3, txt_quadro3_rect)

    # === PERGUNTA FASE 3_1 ===
    elif mode == "pergunta_fase3_1":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*7
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p3, txt_quadro_p3_rect)

        #botões raspberry de opção

    # === FASE 3_2 ===
    elif mode == "fase3_2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*8
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro3, txt_quadro3_rect)

    # === PERGUNTA FASE 3_2 ===
    elif mode == "pergunta_fase3_2":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        desenhar_barra_azul()
        tamanho = (largura_tela/9)*8
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p3, txt_quadro_p3_rect)

        #botões raspberry de opção


    # === FASE 3_3 ===
    elif mode == "fase3_3":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        tamanho = (largura_tela)
        desenhar_barra_amarela()

        #botão voltar
        pygame.draw.rect(tela, ciano, botao_voltar_rect)
        tela.blit(txt_voltar, txt_voltar_rect)

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-200 + 5, 100 + 5, 400 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro3, txt_quadro3_rect)


    # === PERGUNTA FASE 2_3 ===
    elif mode == "pergunta_fase3_3":
        #fundo
        tela.blit(fundo_fases, (0,0))

        #barra de progresão
        tamanho = (largura_tela)
        desenhar_barra_amarela()

        #botão avançar
        pygame.draw.rect(tela, ciano, botao_avancar_rect)
        tela.blit(txt_avancar, txt_avancar_rect)

        #quadro explicativo
        pygame.draw.rect(tela, preto, quadro_explicativo_p3_rect)
        pygame.draw.rect(tela, amarelo, (largura_tela//2-600 + 5, 100 + 5, 1200 - 2 * 5, 100 - 2 * 5))
        tela.blit(txt_quadro_p3, txt_quadro_p3_rect)

        #botões raspberry de opção

    # === RELATORIO ===
    #elif mode == "relatorio"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
