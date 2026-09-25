import urllib.request
import urllib.parse
import json
import time
import pygame

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


# === RESOLUÇÃO BASE ===
BASE_LARGURA = 1400
BASE_ALTURA = 800
info_tela = pygame.display.Info()
largura_tela = info_tela.current_w
altura_tela = info_tela.current_h
escala_x = largura_tela / BASE_LARGURA
escala_y = altura_tela / BASE_ALTURA

escala = min(escala_x, escala_y)

def s(valor):
    return int(valor * escala)

# === FONTES ===
FONT = pygame.font.SysFont("Arial", s(28))
fonte_menu = pygame.font.SysFont(None, s(48))
fonte_intro = pygame.font.SysFont(None, s(192))

# === GOOGLE SHEETS ===
# URL do Web App publicado no Google Apps Script.
URL_GOOGLE_SHEETS = "https://script.google.com/macros/s/AKfycbxozRAb5Yl3QdQuYlI-0f5O2vAPJ8ndvNHRGn9EZU78yNN0qebstECF9DBLZDQ-YIpGzA/exec"

# Deve ser igual ao API_TOKEN definido no Google Apps Script.
# Ele evita chamadas acidentais ao Web App.
API_TOKEN = "MUSICALIZANDO_2026"


def _requisicao_get(parametros, timeout=10):
    """Faz uma requisição GET ao Web App e devolve o JSON."""
    parametros = dict(parametros)
    parametros["token"] = API_TOKEN

    query = urllib.parse.urlencode(parametros)
    url = URL_GOOGLE_SHEETS + "?" + query

    with urllib.request.urlopen(url, timeout=timeout) as resposta:
        return json.loads(resposta.read().decode("utf-8"))

def gerar_id_participante():
    """
    Solicita um novo ID ao Google Sheets.

    Retorna:
        (id_participante, coluna)
    ou:
        (None, None) em caso de erro.
    """
    inicio = time.perf_counter()
    try:
        dados = _requisicao_get({"acao": "novo_id"})

        if dados.get("sucesso"):
            return dados["id"], dados["coluna"]

        print("Erro ao gerar ID:", dados.get("erro"))
        return None, None

    except Exception as e:
        print("Erro ao conectar ao Google Sheets:", e)
        return None, None
    finally:
        duracao_ms = round((time.perf_counter() - inicio) * 1000, 3)
        import assets
        assets.metricas_experimentais["geracao_id_ms"] = duracao_ms
        print(f"Tempo para gerar ID: {duracao_ms} ms")

def salvar_dados(id_participante, usuario, idade, serie):
    """
    Salva os dados iniciais do participante somente no dados.json.

    A comunicação com o Google Sheets não acontece aqui para evitar
    que a conexão de rede deixe o jogo lento durante a execução.
    A sincronização completa ocorre uma única vez no final.
    """
    import assets

    dados_novos = {
        "id_participante": id_participante,
        "usuario": usuario,
        "idade": idade,
        "serie": serie,
        "fase1": [],
        "fase2": [],
        "fase3": [],
        "metricas_experimentais": {
            "troca_idioma_ms": list(assets.metricas_experimentais["troca_idioma_ms"]),
            "geracao_id_ms": assets.metricas_experimentais["geracao_id_ms"],
            "contabilizacao_respostas_ms": []
        }
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
        json.dump(
            dados_existentes,
            f,
            indent=4,
            ensure_ascii=False
        )

    return id_participante

# === REGISTRAR RESPOSTAS ===
respostas_fase1 = []
respostas_fase2 = []
respostas_fase3 = []

def _obter_jogador_atual():
    """Obtém o participante correspondente ao ID guardado em assets."""
    import assets

    try:
        with open("dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        id_atual = assets.id_participante

        if id_atual:
            for jogador in reversed(dados):
                if jogador.get("id_participante") == id_atual:
                    return jogador

        if dados:
            return dados[-1]

    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return None

def registrar_resposta(fase,pergunta,resposta,correta,tempo_resposta=None):
    """
    Salva a resposta somente no dados.json.

    Nenhuma requisição de rede é feita aqui. Isso evita travamentos
    durante as atividades caso o Google Sheets esteja lento ou
    temporariamente indisponível.
    """
    inicio_contabilizacao = time.perf_counter()
    try:
        import assets
        jogador = _obter_jogador_atual()

        if jogador is None:
            raise ValueError("Nenhum participante ativo encontrado.")

        registro = {
            "pergunta": pergunta,
            "resposta": resposta,
            "correta": correta,
            "tempo_resposta": tempo_resposta
        }

        jogador.setdefault(fase, []).append(registro)

        with open("dados.json", "r", encoding="utf-8") as f:
            dados = json.load(f)

        id_atual = jogador.get("id_participante")
        atualizado = False

        if id_atual:
            for indice in range(len(dados) - 1, -1, -1):
                if dados[indice].get("id_participante") == id_atual:
                    dados[indice] = jogador
                    atualizado = True
                    break

        if not atualizado:
            dados[-1] = jogador

        with open("dados.json", "w", encoding="utf-8") as f:
            json.dump(
                dados,
                f,
                indent=4,
                ensure_ascii=False
            )

        duracao_ms = round((time.perf_counter() - inicio_contabilizacao) * 1000, 3)
        metricas = jogador.setdefault("metricas_experimentais", {})
        metricas.setdefault("contabilizacao_respostas_ms", []).append(duracao_ms)
        for indice in range(len(dados) - 1, -1, -1):
            if dados[indice].get("id_participante") == id_atual:
                dados[indice] = jogador
                break
        with open("dados.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Tempo para contabilizar resposta: {duracao_ms} ms")

    except Exception as e:
        print("Erro ao registrar resposta:", e)

def sincronizar_participante():
    """
    Envia todos os dados do participante atual para o Google Sheets.

    Esta é a única sincronização feita durante a partida depois da
    geração do ID. As respostas já estão preservadas localmente no
    dados.json, então uma falha de rede não apaga os dados coletados.
    """
    jogador = _obter_jogador_atual()

    if jogador is None:
        return False

    dados_participante = {
        "id": jogador.get("id_participante"),
        "usuario": jogador.get("usuario", ""),
        "idade": jogador.get("idade", ""),
        "serie": jogador.get("serie", ""),
        "fase1": jogador.get("fase1", []),
        "fase2": jogador.get("fase2", []),
        "fase3": jogador.get("fase3", [])
    }

    try:
        dados_google = _requisicao_get({
            "acao": "sincronizar_participante",
            "dados": json.dumps(
                dados_participante,
                ensure_ascii=False,
                separators=(",", ":")
            )
        }, timeout=10)

        if dados_google.get("sucesso"):
            return True

        print(
            "Falha na sincronização final:",
            dados_google.get("erro")
        )
        return False

    except Exception as e:
        print("Falha na sincronização final:", e)
        return False

# === VERIFICAR RELÓGIO ===
def verificarRelogio(tempo=None):
    if tempo is None:
        return time.perf_counter()
    else:
        tempo_resposta_ms = (time.perf_counter() - tempo) * 1000
        return round(tempo_resposta_ms, 3)

# === CARREGAR DADOS ===
def carregar_dados():
    with open("dados.json", "r", encoding="utf-8") as f:
        return json.load(f)

# === CALCULAR RESULTADOS ===
def calcular_resultados(jogador):
    acertos = 0
    erros = 0

    resultados_por_fase = {}

    for fase in ["fase1", "fase2", "fase3"]:
        acertos_fase = 0
        erros_fase = 0

        for pergunta in jogador.get(fase, []):
            if pergunta["correta"]:
                acertos += 1
                acertos_fase += 1
            else:
                erros += 1
                erros_fase += 1

        resultados_por_fase[fase] = (acertos_fase, erros_fase)

    return acertos, erros, resultados_por_fase

def pegar_ultimo_jogador():
    dados = carregar_dados()
    return dados[-1]

# === BARRAS DE PROGRESSÃO ===
def desenhar_barra_azul(tela, CORES, largura_tela):
    pygame.draw.rect(tela, CORES["ciano"], (0, 0, largura_tela, 20))

def desenhar_barra_amarela(tela, CORES, tamanho):
    pygame.draw.rect(tela, CORES["amarelo"], (0, 0, tamanho, 20))

# === BOTÕES / CAMPOS ===
def criar_botao(texto, x, y, w=400, h=60, cor=CORES["ciano"], cor_texto=CORES["preto"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)

    linhas = texto.split("\n")

    altura_linha = fonte_menu.get_height()
    altura_total = len(linhas) * altura_linha

    texto_render = pygame.Surface((w, h), pygame.SRCALPHA)

    y_texto = (h - altura_total) // 2

    for linha in linhas:
        linha = linha.strip()

        txt = fonte_menu.render(linha, True, cor_texto)
        txt_rect = txt.get_rect(center=( w // 2, y_texto + altura_linha // 2))
        texto_render.blit( txt, txt_rect)
        y_texto += altura_linha

    texto_rect = texto_render.get_rect(center=rect.center)
    return rect, surf, texto_render, texto_rect

def desenhar_botao(tela, rect, texto, FONT, CORES, cor=None):
    if cor is None:
        cor = CORES["ciano"]

    pygame.draw.rect(tela, cor, rect)
    render = FONT.render(texto, True, CORES["preto"])
    tela.blit(render, render.get_rect(center=rect.center))

def desenhar_campo(tela, FONT, CORES, label, rect, valor, ativo=False):
    texto_label = FONT.render(label, True, CORES["preto"])
    tela.blit(texto_label, texto_label.get_rect(midbottom=(rect.centerx, rect.top - 8)))
    pygame.draw.rect(
        tela,
        CORES["amarelo"] if ativo else CORES["ciano"],
        rect
    )
    tela.blit(FONT.render(valor, True, CORES["preto"]), (rect.x + 5, rect.y + 10))

def criar_nuvem(texto, x, y, w=200, h=20, cor=CORES["branco"], cor_texto=CORES["preto"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)

    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)

    return rect, surf, texto_render, texto_rect

def quadro_explicativo(texto, x, y, w=650, h=60, cor=CORES["amarelo"], cor_texto=CORES["preto"]):
    rect = pygame.Rect(x, y, w, h)
    surf = pygame.Surface((w, h))
    surf.fill(cor)

    texto_render = fonte_menu.render(texto, True, cor_texto)
    texto_rect = texto_render.get_rect(center=rect.center)

    return rect, surf, texto_render, texto_rect

# === TROCAR MODO ===
def trocar_modo(novo_modo):
    import assets
    assets.mode = novo_modo

# === RELATÓRIO ===
relatorio_atual = None

def obter_ultimo_jogador():
    return pegar_ultimo_jogador()

def gerar_relatorio(jogador):

    total_acertos = 0
    total_erros = 0
    fases = {}

    for fase in ["fase1", "fase2", "fase3"]:

        acertos = 0
        erros = 0

        for resposta in jogador.get(fase, []):

            if resposta["correta"]:
                acertos += 1
            else:
                erros += 1

        fases[fase] = {
            "acertos": acertos,
            "erros": erros
        }

        total_acertos += acertos
        total_erros += erros

    return {
        "id_participante": jogador.get("id_participante"),
        "usuario": jogador["usuario"],
        "idade": jogador["idade"],
        "serie": jogador["serie"],
        "acertos": total_acertos,
        "erros": total_erros,
        "fases": fases
    }
