import pygame
import json

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

# === FONTES ===
FONT = pygame.font.SysFont("Arial", 28)
fonte_menu = pygame.font.SysFont(None, 48)
fonte_intro = pygame.font.SysFont(None, 96)

# === SALVAR DADOS ===
def salvar_dados(nome, escola, serie):
    dados_novos = {
        "nome": nome,
        "escola": escola,
        "serie": serie,
        "fase1": [],
        "fase2": [],
        "fase3": []
    }

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


# === REGISTRAR RESPOSTAS ===
respostas_fase1 = []
respostas_fase2 = []
respostas_fase3 = ""

def registrar_resposta(fase, pergunta, resposta, correta):
    try:
        with open("dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        jogador = dados[-1]

        jogador[fase].append({
            "pergunta": pergunta,
            "resposta": resposta,
            "correta": correta
        })

        with open("dados.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)

    except:
        print("Erro ao registrar resposta")


# === BARRAS DE PROGRESSÃO ===
def desenhar_barra_azul(tela, CORES, largura_tela):
    pygame.draw.rect(tela, CORES["ciano"], (0, 0, largura_tela, 20))


def desenhar_barra_amarela(tela, CORES, tamanho):
    pygame.draw.rect(tela, CORES["amarelo"], (0, 0, tamanho, 20))


# === BOTÕES / CAMPOS ===
def criar_botao(texto, x, y, w=300, h=40, cor=CORES["ciano"], cor_texto=CORES["preto"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)
    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)
    return rect, surf, texto_render, texto_rect


def desenhar_botao(tela, rect, texto, FONT, CORES, cor=None):
    if cor is None:
        cor = CORES["ciano"]

    pygame.draw.rect(tela, cor, rect)
    render = FONT.render(texto, True, CORES["preto"])
    tela.blit(render, render.get_rect(center=rect.center))


def desenhar_campo(tela, FONT, CORES, label, rect, valor, ativo=False):
    tela.blit(FONT.render(label, True, CORES["preto"]), (rect.x, rect.y - 30))
    pygame.draw.rect(
        tela,
        CORES["amarelo"] if ativo else CORES["ciano"],
        rect
    )
    tela.blit(FONT.render(valor, True, CORES["preto"]), (rect.x + 5, rect.y + 5))


def criar_nuvem(texto, x, y, w=200, h=20, cor=CORES["branco"], cor_texto=CORES["ciano"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)

    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)

    return rect, surf, texto_render, texto_rect


def quadro_explicativo(texto, x, y, w=300, h=40, cor=CORES["amarelo"], cor_texto=CORES["preto"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)

    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)

    return rect, surf, texto_render, texto_rect


# === TROCAR MODO ===
def trocar_modo(novo_modo, som=True):
    import assets

    if som and hasattr(assets, "click_sound"):
        assets.click_sound.play()

    assets.mode = novo_modo