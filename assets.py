import pygame
from utils import criar_nuvem, quadro_explicativo, criar_botao
import sys

pygame.init()

# === CORES ===
CORES = {
    "preto": (0, 0, 0),
    "cinza": (128, 128, 128),
    "branco": (255, 255, 255),
    "vermelho": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "amarelo": (255, 255, 0),
    "ciano": (0, 255, 255),
    "magenta": (255, 0, 255),
    "ciano_opaco": (0, 180, 180),
    "magenta_opaco": (180, 0, 180)
}

# RESOLUÇÃO BASE
BASE_LARGURA = 1400
BASE_ALTURA = 800

info_tela = pygame.display.Info()
MARGEM_HORIZONTAL = 40
MARGEM_VERTICAL = 100

largura_tela = info_tela.current_w - MARGEM_HORIZONTAL
altura_tela = info_tela.current_h - MARGEM_VERTICAL
tela = pygame.display.set_mode((largura_tela, altura_tela),pygame.RESIZABLE)
pygame.display.set_caption("Musicalizando no Céu")

# ESCALAS
escala_x = largura_tela / BASE_LARGURA
escala_y = altura_tela / BASE_ALTURA
escala = min(escala_x, escala_y)


def sx(valor):
    """Converte uma posição/tamanho horizontal da resolução base."""
    return int(valor * escala_x)


def sy(valor):
    """Converte uma posição/tamanho vertical da resolução base."""
    return int(valor * escala_y)


def s(valor):
    """Escala uniforme para tamanhos."""
    return int(valor * escala)


#=== FONTES ===
FONT = pygame.font.SysFont("Arial", s(28), bold=True)
fonte_menu = pygame.font.SysFont(None, s(48))
fonte_intro = pygame.font.SysFont(None, s(192))
fonte_pequena = pygame.font.SysFont("arial", s(22), bold=True)
fonte_relatorio_titulo = pygame.font.SysFont("Arial", s(50))
fonte_relatorio = pygame.font.SysFont("Arial", s(30))

#=== IMAGENS ===
background = pygame.transform.scale(pygame.image.load("images/fundo_menu.png"),(largura_tela, altura_tela))
quadro_menu = pygame.transform.scale(pygame.image.load("images/quadro_menu.png"),(sx(BASE_LARGURA // 3), sy(BASE_ALTURA // 2 + 50)))
background_fase0 = pygame.transform.scale(pygame.image.load("images/fundo.png"),(largura_tela, altura_tela))
quadro_fase0 = pygame.transform.scale(pygame.image.load("images/quadro_fase0.png"), (sx(BASE_LARGURA // 3), sy(BASE_ALTURA // 2 + 50)))
fundo_fases = pygame.transform.scale(pygame.image.load("images/fundo_fases.png"), (largura_tela, altura_tela))
nuvem = pygame.transform.scale(pygame.image.load("images/nuvem.png"), (s(300), s(110)))
cadeado = pygame.transform.scale(pygame.image.load("images/cadeado.png"),(s(50), s(75)))
cadeadoaberto = pygame.transform.scale(pygame.image.load("images/cadeadoaberto.png"), (s(50), s(75)))
bichinho1 = pygame.transform.scale(pygame.image.load("images/bichinho1.png"), (s(200), s(180)))
bichinho2 = pygame.transform.scale(pygame.image.load("images/bichinho2.png"), (s(200), s(180)))
bandeira = pygame.transform.scale(pygame.image.load("images/bandeira.png"), (s(120), s(110)))
som = pygame.transform.scale(pygame.image.load("images/som.png"), (s(300), s(300)))

#=== BOTÕES DO MENU ===
botao_sair_rect, surf_sair, txt_sair, txt_sair_rect = criar_botao("Sair", sx(700-185), sy(400 + 150), s(400), s(60))
botao_ajuda_rect, surf_ajuda, txt_ajuda, txt_ajuda_rect = criar_botao("Ajuda", sx(700-185), sy(400 + 50), s(400), s(60))
botao_jogar_rect, surf_jogar, txt_jogar, txt_jogar_rect = criar_botao("Jogar", sx(700-185), sy(400 - 50), s(400), s(60))

# === BOTÕES DOS MENUS DAS FASES === 
largura_botao_nuvem = s(200)
espaco_nuvens = s(200)
inicio_nuvens = (largura_tela - (largura_botao_nuvem * 3 + espaco_nuvens * 2)) // 2

botao_fase1_rect, surf_fase1, txt_fase1, txt_fase1_rect = criar_nuvem("Fase 1", inicio_nuvens, sy(BASE_ALTURA // 2 - 10), s(200), s(20))
botao_nuvem2_rect, surf_nuvem2, txt_nuvem2, txt_nuvem2_rect = criar_nuvem("Fase 2", inicio_nuvens + largura_botao_nuvem + espaco_nuvens, sy(BASE_ALTURA // 2 - 10), s(200), s(20))
botao_nuvem3_rect, surf_nuvem3, txt_nuvem3, txt_nuvem3_rect = criar_nuvem( "Fase 3", inicio_nuvens + (largura_botao_nuvem + espaco_nuvens) * 2, sy(BASE_ALTURA // 2 - 10), s(200), s(20))

# === BOTÕES DE CONTROLE ===
botao_comecar_rect, surf_comecar, txt_comecar, txt_comecar_rect = criar_botao("Começar", sx(BASE_LARGURA - 300), sy(BASE_ALTURA - 150), s(240), s(56))
botao_voltar_rect, surf_voltar, txt_voltar, txt_voltar_rect = criar_botao("Voltar", sx(BASE_LARGURA // 15), sy(BASE_ALTURA // 17), s(240), s(56))
botao_avancar_rect, surf_avancar, txt_avancar, txt_avancar_rect = criar_botao("Avançar",  sx(BASE_LARGURA // 2 - 120), sy(BASE_ALTURA//2 + 300), s(240), s(56))

# === ÁREAS DE SOM === 
espaco_botoes_som = s(200)
largura_total_sons = som.get_width() * 2 + espaco_botoes_som
inicio_sons = (largura_tela - largura_total_sons) // 2

som1_rect = som.get_rect(topleft=(inicio_sons, sy(300)))
som2_rect = som.get_rect(topleft=(inicio_sons + som.get_width() + espaco_botoes_som, sy(300)))
som3_rect = som.get_rect(topleft=(sx(BASE_LARGURA // 2 - 150), sy(300)))

# === BOTÕES DE RESPOSTA ===
borda_botao1_resposta_rect = pygame.Rect(som1_rect.x - s(5), sy(295), s(310), s(310))
borda_botao2_resposta_rect = pygame.Rect(som2_rect.x - s(5), sy(295), s(310), s(310))

botao1_resposta1_rect, surf_botao1_resposta1, txt_botao1_resposta1, txt_botao1_resposta1_rect = criar_botao("SOM 1", som1_rect.x, sy(300), s(300), s(300))
botao2_resposta1_rect, surf_botao2_resposta1, txt_botao2_resposta1, txt_botao2_resposta1_rect = criar_botao("SOM 2", som2_rect.x, sy(300), s(300), s(300))
botao1_resposta3_rect, surf_botao1_resposta3, txt_botao1_resposta3, txt_botao1_resposta3_rect = criar_botao("IGUAIS", som1_rect.x, sy(300), s(300), s(300))
botao2_resposta3_rect, surf_botao2_resposta3, txt_botao2_resposta3, txt_botao2_resposta3_rect = criar_botao("DIFERENTES", som2_rect.x, sy(300), s(300), s(300))
botao1_resposta2_rect, surf_botao1_resposta2, txt_botao1_resposta2, txt_botao1_resposta2_rect = criar_botao("GUITARRA\n\nPIANO\n\nBATERIA", som1_rect.x, sy(300), s(300), s(300))
botao2_resposta2_rect, surf_botao2_resposta2, txt_botao2_resposta2, txt_botao2_resposta2_rect = criar_botao("PIANO\n\nSAXOFONE\n\nVIOLINO", som2_rect.x, sy(300), s(300), s(300))

# === QUADROS EXPLICATIVOS === 
quadro_explicativo1_rect, surf_quadro_explicativo1, txt_quadro_explicativo1, txt_quadro_explicativo1_rect = quadro_explicativo(
    "Escute com atenção!",
    sx(BASE_LARGURA // 2 - 300),
    sy(BASE_ALTURA // 6),
    s(600),
    s(60)
)

quadro_explicativo2_rect, surf_quadro_explicativo2, txt_quadro_explicativo2, txt_quadro_explicativo2_rect = quadro_explicativo(
    "Qual som é mais agudo?",
    sx(BASE_LARGURA // 2 - 300),
    sy(BASE_ALTURA // 6),
    s(600),
    s(60)
)

quadro_explicativo3_rect, surf_quadro_explicativo3, txt_quadro_explicativo3, txt_quadro_explicativo3_rect = quadro_explicativo(
    "São melodias iguais ou diferentes?",
    sx(BASE_LARGURA // 2 - 300),
    sy(BASE_ALTURA // 6),
    s(600),
    s(60)
)

quadro_explicativo4_rect, surf_quadro_explicativo4, txt_quadro_explicativo4, txt_quadro_explicativo4_rect = quadro_explicativo(
    "Quais instrumentos eram?",
    sx(BASE_LARGURA // 2 - 300),
    sy(BASE_ALTURA // 6),
    s(600),
    s(60)
)


# === CAMPOS DE TEXTO === 
usuario = pygame.Rect(sx(BASE_LARGURA // 2 - 200),sy(BASE_ALTURA // 2 - 40),s(400),s(50))
idade_rect = pygame.Rect(sx(BASE_LARGURA // 2 - 200),sy(BASE_ALTURA // 2 + 60),s(400),s(50))
serie_rect = pygame.Rect(sx(BASE_LARGURA // 2 - 200), sy(BASE_ALTURA // 2 + 150), s(400), s(50))
opcoes_serie = ["1º ano","2º ano","3º ano", "4º ano"]

# == ESTADOS === 
dropdown_aberto = False
active_field = None
player_name = ""
player_age = ""
player_serie = ""
id_participante = None
coluna_participante = None
mode = "menu"
error_msg = ""
resposta_selecionada = None

# === TEXTOS ===

texto_som1_surface = FONT.render("SOM 1", True, CORES["preto"])
texto_som1_rect = texto_som1_surface.get_rect(center=(sx(inicio_sons+25), sy(340)))
texto_som2_surface = FONT.render("SOM 2", True, CORES["preto"])
texto_som2_rect = texto_som2_surface.get_rect(center=(sx(inicio_sons + espaco_botoes_som+230), sy(340)))
texto_som3_surface = FONT.render("MÚSICA", True, CORES["preto"])
texto_som3_rect = texto_som3_surface.get_rect(center=(sx(BASE_LARGURA // 2-10), sy(340)))

texto_intro1_surf = fonte_intro.render("FASE 1", True, CORES["preto"])
texto_intro1_rect = texto_intro1_surf.get_rect( center=(sx(BASE_LARGURA // 2), sy(BASE_ALTURA // 2)))
texto_intro2_surf = fonte_intro.render("FASE 2",True, CORES["preto"])
texto_intro2_rect = texto_intro2_surf.get_rect(center=(sx(BASE_LARGURA // 2), sy(BASE_ALTURA // 2)))
texto_intro3_surf = fonte_intro.render("FASE 3", True, CORES["preto"])
texto_intro3_rect = texto_intro3_surf.get_rect(center=(sx(BASE_LARGURA // 2), sy(BASE_ALTURA // 2)))

texto_relatorio_surf = fonte_relatorio_titulo.render("Relatório Final",True,CORES["preto"])
texto_relatorio_rect = texto_relatorio_surf.get_rect(center=(largura_tela // 2, sy(100)))

# === SONS ===
click_sound = pygame.mixer.Sound("sons/botao1.mp3")

background_sound = pygame.mixer.Sound("sons/background-sound.mp3")
background_sound.set_volume(0.3) 

som_nuvem = pygame.mixer.Sound("sons/som_nuvem.mp3")
som_agudo1_fase1 = pygame.mixer.Sound("sons/agudo1.mp3")
som_grave1_fase1 = pygame.mixer.Sound("sons/grave1.mp3")

som_agudo2_fase1 = pygame.mixer.Sound("sons/agudo2.mp3")
som_grave2_fase1 = pygame.mixer.Sound("sons/grave2.mp3")

som_agudo3_fase1 = pygame.mixer.Sound("sons/agudo3.mp3")
som_grave3_fase1 = pygame.mixer.Sound("sons/grave3.mp3")

musica_fase2_1 = pygame.mixer.Sound("sons/musica1.mp3")
musica_fase2_2 = pygame.mixer.Sound("sons/musica2.mp3")
musica_fase2_3 = pygame.mixer.Sound("sons/musica3.mp3")

melodia1_fase3 = pygame.mixer.Sound("sons/melodia1.mp3")
melodia2_fase3 = pygame.mixer.Sound("sons/melodia2.mp3")
melodia3_fase3 = pygame.mixer.Sound("sons/melodia3.mp3")
melodia4_fase3 = pygame.mixer.Sound("sons/melodia4.mp3")
melodia5_fase3 = pygame.mixer.Sound("sons/melodia5e6.mp3")
melodia6_fase3 = pygame.mixer.Sound("sons/melodia5e6.mp3")

level_complete = pygame.mixer.Sound("sons/level_complete.mp3")

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
    "\n"
    "\n"
    "Criador: Luisa Narvaz Blankenburg\n"
    "Projeto: Música, Jogo e Atenção: uma proposta educacional com Raspberry Pi.\n"
    "Professor orientador: André Luiz Silva de Moraes\n"
    "Instituição: Instituto Federal de Santa Catarina - Câmpus Garopaba")

linhas_texto_ajuda = texto_ajuda.split('\n')
superficies_texto_ajuda = [FONT.render(linha, True, CORES["azul"]) for linha in linhas_texto_ajuda]
velocidade_rolagem_ajuda = 1.2
posicao_y = altura_tela

# ==== SELEÇÃO DE BOTÕES ====
resposta_selecionada = None