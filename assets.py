import pygame
from utils import criar_nuvem, quadro_explicativo, criar_botao
import sys
import time

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

idioma = "pt"
TEXTOS = {
    "pt": {
        "sair": "Sair", "ajuda": "Ajuda", "jogar": "Jogar",
        "comecar": "Começar", "voltar": "Voltar", "avancar": "Avançar",
        "usuario": "Usuário:", "idade": "Idade:", "serie": "Série:",
        "fase": "Fase", "som": "SOM", "musica": "MÚSICA",
        "iguais": "IGUAIS", "diferentes": "DIFERENTES",
        "guitarra": "GUITARRA", "piano": "PIANO", "bateria": "BATERIA",
        "saxofone": "SAXOFONE", "violino": "VIOLINO",
        "escute": "Escute com atenção!", "agudo": "Qual som é mais agudo?",
        "melodias": "São melodias iguais ou diferentes?",
        "instrumentos": "Quais instrumentos eram?", "tocando": "Tocando...",
        "carregando": "Carregando...", "relatorio": "Relatório Final",
        "acertos": "Total de acertos:", "erros": "Total de erros:",
        "acerto": "acertos", "erro": "erros",
        "bem_vindos": "Bem vindos ao jogo Musicalizando no Céu!",
        "hoje": "Hoje, você embarcará em uma aventura através de músicas e atividades.",
        "constituido": "O jogo constitui de 3 fases com atividades em que você deve prestar muita atenção.",
        "aproveite": "Espero que aproveite a experiência e se dedique ao máximo para chegar ao final.",
        "criador": "Criador: Luisa Narvaz Blankenburg",
        "projeto": "Projeto: Música, Jogo e Atenção: uma proposta educacional com Raspberry Pi.",
        "professor": "Professor orientador: André Luiz Silva de Moraes",
        "instituicao": "Instituição: Instituto Federal de Santa Catarina - Câmpus Garopaba",
        "preencha": "Preencha todos os campos.",
        "id_erro": "Não foi possível gerar o ID."
    },
    "es": {
        "sair": "Salir", "ajuda": "Ayuda", "jogar": "Jugar",
        "comecar": "Comenzar", "voltar": "Volver", "avancar": "Avanzar",
        "usuario": "Usuario:", "idade": "Edad:", "serie": "Curso:",
        "fase": "Fase", "som": "SONIDO", "musica": "MÚSICA",
        "iguais": "IGUALES", "diferentes": "DIFERENTES",
        "guitarra": "GUITARRA", "piano": "PIANO", "bateria": "BATERÍA",
        "saxofone": "SAXOFÓN", "violino": "VIOLÍN",
        "escute": "¡Escucha con atención!", "agudo": "¿Qué sonido es más agudo?",
        "melodias": "¿Las melodías son iguales o diferentes?",
        "instrumentos": "¿Qué instrumentos eran?", "tocando": "Reproduciendo...",
        "carregando": "Cargando...", "relatorio": "Informe final",
        "acertos": "Total de aciertos:", "erros": "Total de errores:",
        "acerto": "aciertos", "erro": "errores",
        "bem_vindos": "¡Bienvenidos al juego Musicalizando en el Cielo!",
        "hoje": "Hoy emprenderás una aventura a través de músicas y actividades.",
        "constituido": "El juego tiene 3 fases con actividades en las que debes prestar mucha atención.",
        "aproveite": "Espero que disfrutes la experiencia y te esfuerces al máximo para llegar al final.",
        "criador": "Creadora: Luisa Narvaz Blankenburg",
        "projeto": "Proyecto: Música, Juego y Atención: una propuesta educativa con Raspberry Pi.",
        "professor": "Profesor orientador: André Luiz Silva de Moraes",
        "instituicao": "Institución: Instituto Federal de Santa Catarina - Campus Garopaba",
        "preencha": "Completa todos los campos.",
        "id_erro": "No fue posible generar el ID."
    }
}

def t(chave):
    return TEXTOS[idioma][chave]

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
bandeira_brasil = pygame.transform.scale(pygame.image.load("images/bandeira-brasil.png"), (s(42), s(28)))
bandeira_espanha = pygame.transform.scale(pygame.image.load("images/bandeira-espanha.png"), (s(42), s(28)))
som = pygame.transform.scale(pygame.image.load("images/som.png"), (s(300), s(300)))

#=== BOTÕES DO MENU ===
largura_botoes_menu = s(400)
x_botoes_menu = (largura_tela - largura_botoes_menu) // 2
botao_sair_rect, surf_sair, txt_sair, txt_sair_rect = criar_botao("Sair", x_botoes_menu, sy(400 + 150), largura_botoes_menu, s(60))
botao_ajuda_rect, surf_ajuda, txt_ajuda, txt_ajuda_rect = criar_botao("Ajuda", x_botoes_menu, sy(400 + 50), largura_botoes_menu, s(60))
botao_jogar_rect, surf_jogar, txt_jogar, txt_jogar_rect = criar_botao("Jogar", x_botoes_menu, sy(400 - 50), largura_botoes_menu, s(60))

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
som3_rect = som.get_rect(midtop=(largura_tela // 2, sy(300)))

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
altura_quadros = s(60)
largura_quadro_padrao = s(600)
largura_quadro_fase3 = s(800)
x_quadro_padrao = largura_tela // 2 - largura_quadro_padrao // 2
x_quadro_fase3 = largura_tela // 2 - largura_quadro_fase3 // 2

quadro_explicativo1_rect, surf_quadro_explicativo1, txt_quadro_explicativo1, txt_quadro_explicativo1_rect = quadro_explicativo(
    "Escute com atenção!",
    x_quadro_padrao,
    sy(BASE_ALTURA // 6),
    largura_quadro_padrao,
    altura_quadros
)

quadro_explicativo2_rect, surf_quadro_explicativo2, txt_quadro_explicativo2, txt_quadro_explicativo2_rect = quadro_explicativo(
    "Qual som é mais agudo?",
    x_quadro_padrao,
    sy(BASE_ALTURA // 6),
    largura_quadro_padrao,
    altura_quadros
)

quadro_explicativo3_rect, surf_quadro_explicativo3, txt_quadro_explicativo3, txt_quadro_explicativo3_rect = quadro_explicativo(
    "São melodias iguais ou diferentes?",
    x_quadro_fase3,
    sy(BASE_ALTURA // 6),
    largura_quadro_fase3,
    altura_quadros
)

quadro_explicativo4_rect, surf_quadro_explicativo4, txt_quadro_explicativo4, txt_quadro_explicativo4_rect = quadro_explicativo(
    "Quais instrumentos eram?",
    x_quadro_padrao,
    sy(BASE_ALTURA // 6),
    largura_quadro_padrao,
    altura_quadros
)


# === CAMPOS DE TEXTO === 
largura_campos = s(400)
x_campos = (largura_tela - largura_campos) // 2
usuario = pygame.Rect(x_campos, sy(BASE_ALTURA // 2 - 40), largura_campos, s(50))
idade_rect = pygame.Rect(x_campos, sy(BASE_ALTURA // 2 + 60), largura_campos, s(50))
serie_rect = pygame.Rect(x_campos, sy(BASE_ALTURA // 2 + 150), largura_campos, s(50))
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

# === MÉTRICAS EXPERIMENTAIS ===
metricas_experimentais = {
    "troca_idioma_ms": [],
    "geracao_id_ms": None,
    "contabilizacao_respostas_ms": []
}

# === TEXTOS ===

texto_som1_surface = FONT.render("SOM 1", True, CORES["preto"])
texto_som1_rect = texto_som1_surface.get_rect(center=(som1_rect.centerx, som1_rect.top + s(40)))
texto_som2_surface = FONT.render("SOM 2", True, CORES["preto"])
texto_som2_rect = texto_som2_surface.get_rect(center=(som2_rect.centerx, som2_rect.top + s(40)))
texto_som3_surface = FONT.render("MÚSICA", True, CORES["preto"])
texto_som3_rect = texto_som3_surface.get_rect(center=(som3_rect.centerx, som3_rect.top + s(40)))

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

# === IDIOMA ===
largura_bandeira = s(42)
altura_bandeira = s(28)
espaco_bandeiras = s(8)
brasil_rect = pygame.Rect(
    largura_tela - largura_bandeira - s(24), s(18),
    largura_bandeira, altura_bandeira
)
espanha_rect = pygame.Rect(
    brasil_rect.x - largura_bandeira - espaco_bandeiras, s(18),
    largura_bandeira, altura_bandeira
)

def definir_idioma(novo_idioma):
    global idioma, superficies_texto_ajuda
    global surf_sair, txt_sair, txt_sair_rect
    global surf_ajuda, txt_ajuda, txt_ajuda_rect
    global surf_jogar, txt_jogar, txt_jogar_rect
    global surf_fase1, txt_fase1, txt_fase1_rect
    global surf_nuvem2, txt_nuvem2, txt_nuvem2_rect
    global surf_nuvem3, txt_nuvem3, txt_nuvem3_rect
    global surf_comecar, txt_comecar, txt_comecar_rect
    global surf_voltar, txt_voltar, txt_voltar_rect
    global surf_avancar, txt_avancar, txt_avancar_rect
    global txt_botao1_resposta1, txt_botao1_resposta1_rect
    global txt_botao2_resposta1, txt_botao2_resposta1_rect
    global txt_botao1_resposta2, txt_botao1_resposta2_rect
    global txt_botao2_resposta2, txt_botao2_resposta2_rect
    global txt_botao1_resposta3, txt_botao1_resposta3_rect
    global txt_botao2_resposta3, txt_botao2_resposta3_rect
    global txt_quadro_explicativo1, txt_quadro_explicativo1_rect
    global txt_quadro_explicativo2, txt_quadro_explicativo2_rect
    global txt_quadro_explicativo3, txt_quadro_explicativo3_rect
    global txt_quadro_explicativo4, txt_quadro_explicativo4_rect
    global texto_som1_surface, texto_som2_surface, texto_som3_surface
    global texto_som1_rect, texto_som2_rect, texto_som3_rect
    global texto_intro1_surf, texto_intro2_surf, texto_intro3_surf
    global texto_relatorio_surf, texto_relatorio_rect

    idioma = novo_idioma if novo_idioma in TEXTOS else "pt"

    botao_sair_rect, surf_sair, txt_sair, txt_sair_rect = criar_botao(t("sair"), x_botoes_menu, sy(550), largura_botoes_menu, s(60))
    botao_ajuda_rect, surf_ajuda, txt_ajuda, txt_ajuda_rect = criar_botao(t("ajuda"), x_botoes_menu, sy(450), largura_botoes_menu, s(60))
    botao_jogar_rect, surf_jogar, txt_jogar, txt_jogar_rect = criar_botao(t("jogar"), x_botoes_menu, sy(350), largura_botoes_menu, s(60))

    botao_fase1_rect, surf_fase1, txt_fase1, txt_fase1_rect = criar_nuvem(f"{t('fase')} 1", inicio_nuvens, sy(BASE_ALTURA // 2 - 10), s(200), s(20))
    botao_nuvem2_rect, surf_nuvem2, txt_nuvem2, txt_nuvem2_rect = criar_nuvem(f"{t('fase')} 2", inicio_nuvens + largura_botao_nuvem + espaco_nuvens, sy(BASE_ALTURA // 2 - 10), s(200), s(20))
    botao_nuvem3_rect, surf_nuvem3, txt_nuvem3, txt_nuvem3_rect = criar_nuvem(f"{t('fase')} 3", inicio_nuvens + (largura_botao_nuvem + espaco_nuvens) * 2, sy(BASE_ALTURA // 2 - 10), s(200), s(20))

    botao_comecar_rect, surf_comecar, txt_comecar, txt_comecar_rect = criar_botao(t("comecar"), sx(BASE_LARGURA - 300), sy(BASE_ALTURA - 150), s(240), s(56))
    botao_voltar_rect, surf_voltar, txt_voltar, txt_voltar_rect = criar_botao(t("voltar"), sx(BASE_LARGURA // 15), sy(BASE_ALTURA // 17), s(240), s(56))
    botao_avancar_rect, surf_avancar, txt_avancar, txt_avancar_rect = criar_botao(t("avancar"), sx(BASE_LARGURA // 2 - 120), sy(BASE_ALTURA // 2 + 300), s(240), s(56))

    textos_resposta = [
        (f"{t('som')} 1", botao1_resposta1_rect), (f"{t('som')} 2", botao2_resposta1_rect),
        (f"{t('guitarra')}\n\n{t('piano')}\n\n{t('bateria')}", botao1_resposta2_rect),
        (f"{t('piano')}\n\n{t('saxofone')}\n\n{t('violino')}", botao2_resposta2_rect),
        (t("iguais"), botao1_resposta3_rect), (t("diferentes"), botao2_resposta3_rect)
    ]
    nomes_resposta = ["txt_botao1_resposta1", "txt_botao2_resposta1", "txt_botao1_resposta2", "txt_botao2_resposta2", "txt_botao1_resposta3", "txt_botao2_resposta3"]
    for nome, (texto, rect) in zip(nomes_resposta, textos_resposta):
        superficie = criar_botao(texto, rect.x, rect.y, rect.width, rect.height)[2:]
        globals()[nome], globals()[f"{nome}_rect"] = superficie

    quadros = [
        ("escute", quadro_explicativo1_rect), ("agudo", quadro_explicativo2_rect),
        ("melodias", quadro_explicativo3_rect), ("instrumentos", quadro_explicativo4_rect)
    ]
    for indice, (chave, rect) in enumerate(quadros, 1):
        superficie = fonte_menu.render(t(chave), True, CORES["preto"])
        globals()[f"txt_quadro_explicativo{indice}"] = superficie
        globals()[f"txt_quadro_explicativo{indice}_rect"] = superficie.get_rect(center=rect.center)

    texto_som1_surface = FONT.render(f"{t('som')} 1", True, CORES["preto"])
    texto_som1_rect = texto_som1_surface.get_rect(center=(som1_rect.centerx, som1_rect.top + s(40)))
    texto_som2_surface = FONT.render(f"{t('som')} 2", True, CORES["preto"])
    texto_som2_rect = texto_som2_surface.get_rect(center=(som2_rect.centerx, som2_rect.top + s(40)))
    texto_som3_surface = FONT.render(t("musica"), True, CORES["preto"])
    texto_som3_rect = texto_som3_surface.get_rect(center=(som3_rect.centerx, som3_rect.top + s(40)))
    texto_intro1_surf = fonte_intro.render(f"{t('fase')} 1", True, CORES["preto"])
    texto_intro2_surf = fonte_intro.render(f"{t('fase')} 2", True, CORES["preto"])
    texto_intro3_surf = fonte_intro.render(f"{t('fase')} 3", True, CORES["preto"])
    for indice, superficie in enumerate((texto_intro1_surf, texto_intro2_surf, texto_intro3_surf), 1):
        globals()[f"texto_intro{indice}_rect"] = superficie.get_rect(center=(sx(BASE_LARGURA // 2), sy(BASE_ALTURA // 2)))
    texto_relatorio_surf = fonte_relatorio_titulo.render(t("relatorio"), True, CORES["preto"])
    texto_relatorio_rect = texto_relatorio_surf.get_rect(center=(largura_tela // 2, sy(100)))

    linhas_ajuda = [t("bem_vindos"), "", t("hoje"), "", t("constituido"), "", t("aproveite"), "", "", "", t("criador"), t("projeto"), t("professor"), t("instituicao")]
    superficies_texto_ajuda = [FONT.render(linha, True, CORES["azul"]) for linha in linhas_ajuda]

def desenhar_bandeiras(tela):
    tela.blit(bandeira_espanha, espanha_rect)
    tela.blit(bandeira_brasil, brasil_rect)
    pygame.draw.rect(tela, CORES["preto"], espanha_rect, 1)
    pygame.draw.rect(tela, CORES["preto"], brasil_rect, 1)

def definir_idioma_e_atualizar(novo_idioma):
    inicio = time.perf_counter()
    definir_idioma(novo_idioma)
    duracao_ms = round((time.perf_counter() - inicio) * 1000, 3)
    metricas_experimentais["troca_idioma_ms"].append(duracao_ms)
    print(f"Tempo de troca de idioma: {duracao_ms} ms")

def idioma_esta_em(escolha):
    return idioma == escolha

def texto_campo(chave):
    return t(chave)

def texto_erro(chave):
    return t(chave)

def texto_tocando():
    return t("tocando")

# ==== SELEÇÃO DE BOTÕES ====
resposta_selecionada = None

definir_idioma("pt")