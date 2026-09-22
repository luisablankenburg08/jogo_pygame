import pygame
import sys
import time
import assets
from render import desenhar
from utils import *

pygame.init()

clock = pygame.time.Clock()
inicio_modo = 0
musica_relatorio = 0
rodando = True
inicio_tempo_resposta = None

#== MENSAGEM CARREGANDO ===
def mostrar_carregando():
    tela = assets.tela
    tela.blit(assets.fundo_fases, (0, 0))
    texto = assets.fonte_intro.render("Carregando...",True,assets.CORES["preto"])
    texto_rect = texto.get_rect(center=( assets.largura_tela // 2, assets.altura_tela // 2))
    tela.blit(texto, texto_rect)
    pygame.display.flip()
    
while rodando:
    for event in pygame.event.get():

        # ================= SAIR =================
        if event.type == pygame.QUIT:
            rodando = False

        # ================= CLIQUE =================
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # ===== MENU =====
            if assets.mode == "menu":
                if assets.botao_sair_rect.collidepoint(event.pos):
                    rodando = False
                elif assets.botao_ajuda_rect.collidepoint(event.pos):
                    assets.click_sound.play()
                    trocar_modo("ajuda")
                elif assets.botao_jogar_rect.collidepoint(event.pos):
                    assets.click_sound.play()
                    trocar_modo("fase0")

            # ===== AJUDA =====
            elif assets.mode == "ajuda":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    assets.click_sound.play()
                    trocar_modo("menu")

            # ===== FASE 0 =====
            elif assets.mode == "fase0":

                if assets.botao_voltar_rect.collidepoint(event.pos):
                    assets.click_sound.play()
                    trocar_modo("menu")

                elif assets.usuario.collidepoint(event.pos):
                    assets.active_field = "usuario"

                elif assets.idade_rect.collidepoint(event.pos):
                    assets.active_field = "idade"

                elif assets.serie_rect.collidepoint(event.pos):
                    assets.active_field = None
                    assets.dropdown_aberto = not assets.dropdown_aberto

                elif assets.dropdown_aberto:
                    for i, opcao in enumerate(assets.opcoes_serie):
                        opt_rect = pygame.Rect(
                            assets.serie_rect.x,
                            assets.serie_rect.y + (i+1)*40,
                            assets.serie_rect.width,
                            40
                        )
                        if opt_rect.collidepoint(event.pos):
                            assets.player_serie = opcao
                            assets.active_field = None
                            assets.dropdown_aberto = False

                elif assets.botao_comecar_rect.collidepoint(event.pos):
                    if (
                        assets.player_name.strip()
                        and assets.player_age.strip()
                        and assets.player_serie.strip()
                    ):
                        mostrar_carregando()
                        id_participante, coluna_participante = gerar_id_participante()

                        if id_participante is not None:
                            assets.id_participante = id_participante
                            assets.coluna_participante = coluna_participante

                            salvar_dados(
                                id_participante,
                                assets.player_name,
                                assets.player_age,
                                assets.player_serie
                            )

                            assets.error_msg = ""
                            assets.click_sound.play()
                            trocar_modo("menu_fase1")

                        else:
                            assets.error_msg = ("Não foi possível gerar o ID.")

                    else:
                        assets.error_msg = "Preencha todos os campos."

            # ===== MENU FASE 1 =====
            elif assets.mode == "menu_fase1":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    assets.click_sound.play()
                    trocar_modo("menu")

                elif assets.botao_fase1_rect.collidepoint(event.pos):
                    assets.som_nuvem.play()
                    trocar_modo("introducao_fase1")
                    inicio_modo = pygame.time.get_ticks()

            # ================= FASE 1 =================

            elif assets.mode == "fase1_1":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_1")
                    assets.som_grave1_fase1.stop()
                    assets.som_agudo1_fase1.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_grave1_fase1.stop()
                    assets.som_agudo1_fase1.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_agudo1_fase1.stop()
                    assets.som_grave1_fase1.play()

            elif assets.mode == "pergunta_fase1_1":
                if assets.botao1_resposta1_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "som1"

                elif assets.botao2_resposta1_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "som2"

                elif assets.botao_avancar_rect.collidepoint(event.pos):

                     if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "som1"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase1", "fase1_1", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase1_2")

            elif assets.mode == "fase1_2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_2")
                    assets.som_grave2_fase1.stop()
                    assets.som_agudo2_fase1.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_grave2_fase1.stop()
                    assets.som_agudo2_fase1.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_agudo2_fase1.stop()
                    assets.som_grave2_fase1.play()

            elif assets.mode == "pergunta_fase1_2":
                if assets.botao1_resposta1_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "som1"

                elif assets.botao2_resposta1_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "som2"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "som1"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase1", "fase1_2", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase1_3")

            elif assets.mode == "fase1_3":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_3")
                    assets.som_grave3_fase1.stop()
                    assets.som_agudo3_fase1.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_grave3_fase1.stop()
                    assets.som_agudo3_fase1.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.som_agudo3_fase1.stop()
                    assets.som_grave3_fase1.play()

            elif assets.mode == "pergunta_fase1_3":
                if assets.botao1_resposta1_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "som1"

                elif assets.botao2_resposta1_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "som2"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "som1"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase1", "fase1_3", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("menu_fase2")

            # ================= FASE 2 =================

            elif assets.mode == "menu_fase2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")

                elif assets.botao_nuvem2_rect.collidepoint(event.pos):
                    assets.som_nuvem.play()
                    trocar_modo("introducao_fase2")
                    inicio_modo = pygame.time.get_ticks()

            elif assets.mode == "fase2_1":

                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_1")
                    assets.musica_fase2_1.stop()

                elif assets.som3_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.musica_fase2_1.play()

            elif assets.mode == "pergunta_fase2_1":

                if assets.botao1_resposta2_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "guitarra"

                elif assets.botao2_resposta2_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "saxofone"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "guitarra"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase2", "fase2_1", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase2_2")

            elif assets.mode == "fase2_2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_2")
                    assets.musica_fase2_2.stop()

                elif assets.som3_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.musica_fase2_2.play()

            elif assets.mode == "pergunta_fase2_2":
                if assets.botao1_resposta2_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "guitarra"

                elif assets.botao2_resposta2_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "saxofone"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "guitarra"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase2", "fase2_2", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase2_3")

            elif assets.mode == "fase2_3":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_3")
                    assets.musica_fase2_3.stop()

                elif assets.som3_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.musica_fase2_3.play()

            elif assets.mode == "pergunta_fase2_3":
                if assets.botao1_resposta2_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "guitarra"

                elif assets.botao2_resposta2_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "saxofone"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "saxofone"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase2", "fase2_3", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("menu_fase3")

            # ================= FASE 3 =================

            elif assets.mode == "menu_fase3":
                if assets.botao_nuvem3_rect.collidepoint(event.pos):
                    assets.som_nuvem.play()
                    trocar_modo("introducao_fase3")
                    inicio_modo = pygame.time.get_ticks()

            elif assets.mode == "fase3_1":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase2")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_1")
                    assets.melodia1_fase3.stop()
                    assets.melodia2_fase3.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia1_fase3.play()
                    assets.melodia2_fase3.stop()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia1_fase3.stop()
                    assets.melodia2_fase3.play()

            elif assets.mode == "pergunta_fase3_1":
                if assets.botao1_resposta3_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "iguais"

                elif assets.botao2_resposta3_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "diferentes"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "diferentes"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase3", "fase3_1", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase3_2")


            elif assets.mode == "fase3_2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase2")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_2")
                    assets.melodia3_fase3.stop()
                    assets.melodia4_fase3.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia3_fase3.play()
                    assets.melodia4_fase3.stop()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia3_fase3.stop()
                    assets.melodia4_fase3.play()

            elif assets.mode == "pergunta_fase3_2":
                if assets.botao1_resposta3_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "iguais"

                elif assets.botao2_resposta3_rect.collidepoint(event.pos):
                     assets.resposta_selecionada = "diferentes"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "diferentes"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase3", "fase3_2", assets.resposta_selecionada, correta, tempo_resposta)
                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        trocar_modo("fase3_3")

            elif assets.mode == "fase3_3":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase2")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_3")
                    assets.melodia5_fase3.stop()
                    assets.melodia6_fase3.stop()

                elif assets.som1_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia6_fase3.stop()
                    assets.melodia5_fase3.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    if inicio_tempo_resposta is None:
                        inicio_tempo_resposta = verificarRelogio(inicio_tempo_resposta)
                    assets.melodia5_fase3.stop()
                    assets.melodia6_fase3.play()

            elif assets.mode == "pergunta_fase3_3":

                if assets.botao1_resposta3_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "iguais"

                elif assets.botao2_resposta3_rect.collidepoint(event.pos):
                    assets.resposta_selecionada = "diferentes"

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    
                    if assets.resposta_selecionada is not None:
                        correta = assets.resposta_selecionada == "iguais"
                        tempo_resposta = verificarRelogio(inicio_tempo_resposta)

                        registrar_resposta("fase3","fase3_3",assets.resposta_selecionada,correta,tempo_resposta)

                        inicio_tempo_resposta = None
                        assets.resposta_selecionada = None
                        mostrar_carregando()
                        sincronizar_participante()
                        trocar_modo("relatorio")

            # ================= RELATÓRIO =================
            elif assets.mode == "relatorio":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")


        # ================= TECLADO =================
        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                trocar_modo("menu")

            elif assets.mode == "fase0":

                # ================= NOME =================
                if assets.active_field == "usuario":

                    if event.key == pygame.K_BACKSPACE:
                        assets.player_name = assets.player_name[:-1]

                    else:
                        # Adiciona qualquer caractere digitado no nome
                        if event.unicode:
                            assets.player_name += event.unicode

                # ================= IDADE =================
                elif assets.active_field == "idade":

                    if event.key == pygame.K_BACKSPACE:
                        assets.player_age = assets.player_age[:-1]

                    else:
                        # Aceita somente números e no máximo 2 dígitos
                        if event.unicode.isdigit() and len(assets.player_age) < 2:
                            assets.player_age += event.unicode

    # ================= INTRO TEMPO =================
    if assets.mode == "introducao_fase1":
        if pygame.time.get_ticks() - inicio_modo > 1000:
            trocar_modo("fase1_1")

    elif assets.mode == "introducao_fase2":
        if pygame.time.get_ticks() - inicio_modo > 1000:
            trocar_modo("fase2_1")

    elif assets.mode == "introducao_fase3":
        if pygame.time.get_ticks() - inicio_modo > 1000:
            trocar_modo("fase3_1")


    # ================= RELATÓRIO =================
    if assets.mode == "relatorio":
        while musica_relatorio == 0:
            assets.level_complete.play()
            musica_relatorio += 1

    desenhar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()