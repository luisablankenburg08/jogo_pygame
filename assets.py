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
    "magenta": (255, 0, 255)
}

# === TELA ===
largura_tela, altura_tela = 1400, 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Musicalizando no Céu")

# === FONTES ===
FONT = pygame.font.SysFont("Arial", 28)
fonte_menu = pygame.font.SysFont(None, 48)
fonte_intro = pygame.font.SysFont(None, 96)

# === IMAGENS ===
background = pygame.transform.scale(pygame.image.load("images/fundo_menu.png"), (largura_tela, altura_tela))
quadro_menu = pygame.transform.scale(pygame.image.load("images/quadro_menu.png"), (largura_tela//3, altura_tela//2 + 50))

background_fase0 = pygame.transform.scale(pygame.image.load("images/fundo.png"), (largura_tela, altura_tela))
quadro_fase0 = pygame.transform.scale(pygame.image.load("images/quadro_fase0.png"), (largura_tela//3, altura_tela//2 + 50))

fundo_fases = pygame.transform.scale(pygame.image.load("images/fundo_fases.png"), (largura_tela, altura_tela))

nuvem = pygame.transform.scale(pygame.image.load("images/nuvem.png"), (300, 110))
cadeado = pygame.transform.scale(pygame.image.load("images/cadeado.png"), (50, 75))
cadeadoaberto = pygame.transform.scale(pygame.image.load("images/cadeadoaberto.png"), (50, 75))

bichinho1 = pygame.transform.scale(pygame.image.load("images/bichinho1.png"), (200, 180))
bichinho2 = pygame.transform.scale(pygame.image.load("images/bichinho2.png"), (200, 180))

bandeira = pygame.transform.scale(pygame.image.load("images/bandeira.png"), (120, 110))

som = pygame.transform.scale(pygame.image.load("images/som.png"), (300, 300))

botao_rasp_amarelo_img = pygame.transform.scale(pygame.image.load("images/botao_rasp_amarelo.png"), (200, 200))
botao_rasp_azul_img = pygame.transform.scale(pygame.image.load("images/botao_rasp_azul.png"), (200, 200))

# === BOTÕES MENU ===
botao_sair_rect, surf_sair, txt_sair, txt_sair_rect = criar_botao("Sair", largura_tela//2-150, altura_tela//2+150)
botao_ajuda_rect, surf_ajuda, txt_ajuda, txt_ajuda_rect = criar_botao("Ajuda", largura_tela//2-150, altura_tela//2+50)
botao_jogar_rect, surf_jogar, txt_jogar, txt_jogar_rect = criar_botao("Jogar", largura_tela//2-150, altura_tela//2-50)

# === BOTÕES FASES ===
botao_fase1_rect, surf_fase1, txt_fase1, txt_fase1_rect = criar_nuvem("Fase 1", largura_tela//4, altura_tela//2+100)
botao_nuvem2_rect, surf_nuvem2, txt_nuvem2, txt_nuvem2_rect = criar_nuvem("Fase 2", largura_tela//2, altura_tela//2)
botao_nuvem3_rect, surf_nuvem3, txt_nuvem3, txt_nuvem3_rect = criar_nuvem("Fase 3", largura_tela-400, altura_tela//2-120)

botao_comecar_rect, surf_comecar, txt_comecar, txt_comecar_rect = criar_botao("Começar", largura_tela-300, altura_tela-150, 240, 56)
botao_voltar_rect, surf_voltar, txt_voltar, txt_voltar_rect = criar_botao("Voltar", largura_tela//15, altura_tela//17, 240, 56)
botao_avancar_rect, surf_avancar, txt_avancar, txt_avancar_rect = criar_botao("Avançar", largura_tela//2-120, altura_tela-100, 240, 56)

# === ÁREAS DE SOM ===
som1_rect = som.get_rect(topleft=(300, 300))
som2_rect = som.get_rect(topleft=(900, 300))
som3_rect = som.get_rect(topleft=(largura_tela//2-150, 300))

# === BOTÕES RASPBERRY ===
rasp_amarelo_rect = botao_rasp_amarelo_img.get_rect(topleft=(350, 400))
rasp_azul_rect = botao_rasp_azul_img.get_rect(topleft=(950, 400))

# === BOTÕES FASE 2 ===
botao_piano = pygame.Rect(120, 350, 220, 80)
botao_flauta = pygame.Rect(420, 350, 220, 80)
botao_violao = pygame.Rect(720, 350, 220, 80)
botao_tambor = pygame.Rect(1020, 350, 220, 80)
botao_xilofone = pygame.Rect(570, 500, 220, 80)

# === BOTÕES FASE 3 ===
botao_iguais = pygame.Rect(300, 400, 300, 120)
botao_diferentes = pygame.Rect(800, 400, 300, 120)

# === CAMPOS DE TEXTO ===
nome_rect = pygame.Rect(largura_tela//2-150, altura_tela//2-50, 300, 40)
escola_rect = pygame.Rect(largura_tela//2-150, altura_tela//2+50, 300, 40)
serie_rect = pygame.Rect(largura_tela//2-150, altura_tela//2+150, 300, 40)

opcoes_serie = ["1º ano", "2º ano", "3º ano", "4º ano"]

# === ESTADOS ===
dropdown_aberto = False
active_field = None

player_name = ""
player_school = ""
player_serie = ""

mode = "menu"
error_msg = ""

# === TEXTOS ===
texto_som1_surface = FONT.render("SOM 1", True, CORES["preto"])
texto_som1_rect = texto_som1_surface.get_rect(center=(450, 350))

texto_som2_surface = FONT.render("SOM 2", True, CORES["preto"])
texto_som2_rect = texto_som2_surface.get_rect(center=(1050, 350))

texto_som3_surface = FONT.render("MÚSICA", True, CORES["preto"])
texto_som3_rect = texto_som3_surface.get_rect(center=(largura_tela//2, 350))

texto_intro1_surf = fonte_intro.render("FASE 1", True, CORES["azul"])
texto_intro1_rect = texto_intro1_surf.get_rect(center=(largura_tela//2, altura_tela//2))

texto_intro2_surf = fonte_intro.render("FASE 2", True, CORES["azul"])
texto_intro2_rect = texto_intro2_surf.get_rect(center=(largura_tela//2, altura_tela//2))

texto_intro3_surf = fonte_intro.render("FASE 3", True, CORES["azul"])
texto_intro3_rect = texto_intro3_surf.get_rect(center=(largura_tela//2, altura_tela//2))

# === SONS ===
click_sound = pygame.mixer.Sound("sons/botao1.mp3")
som_start = pygame.mixer.Sound("sons/botao2.mp3")

som_agudo1_fase1 = pygame.mixer.Sound("sons/agudo1.mp3")
som_grave1_fase1 = pygame.mixer.Sound("sons/grave1.mp3")

musica_fase2_1 = pygame.mixer.Sound("sons/agudo1.mp3")
musica_fase2_2 = pygame.mixer.Sound("sons/agudo1.mp3")
musica_fase2_3 = pygame.mixer.Sound("sons/agudo1.mp3")

melodia_fase3_1 = pygame.mixer.Sound("sons/agudo1.mp3")
melodia_fase3_2 = pygame.mixer.Sound("sons/agudo1.mp3")
melodia_fase3_3 = pygame.mixer.Sound("sons/agudo1.mp3")