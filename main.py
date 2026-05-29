import pygame
import sys

import assets
from render import desenhar
from utils import *

pygame.init()

clock = pygame.time.Clock()
inicio_modo = 0
musica_relatorio = 0
rodando = True

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
                    trocar_modo("ajuda")
                elif assets.botao_jogar_rect.collidepoint(event.pos):
                    trocar_modo("fase0")

            # ===== AJUDA =====
            elif assets.mode == "ajuda":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")

            # ===== FASE 0 =====
            elif assets.mode == "fase0":

                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")

                elif assets.nome_rect.collidepoint(event.pos):
                    assets.active_field = "nome"

                elif assets.escola_rect.collidepoint(event.pos):
                    assets.active_field = "escola"

                elif assets.serie_rect.collidepoint(event.pos):
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
                            assets.dropdown_aberto = False

                elif assets.botao_comecar_rect.collidepoint(event.pos):
                    if (
                        assets.player_name.strip()
                        and assets.player_school.strip()
                        and assets.player_serie.strip()
                    ):
                        salvar_dados(
                            assets.player_name,
                            assets.player_school,
                            assets.player_serie
                        )
                        trocar_modo("menu_fase1")
                    else:
                        assets.error_msg = "Preencha todos os campos."

            # ===== MENU FASE 1 =====
            elif assets.mode == "menu_fase1":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")

                elif assets.botao_fase1_rect.collidepoint(event.pos):
                    trocar_modo("introducao_fase1")
                    inicio_modo = pygame.time.get_ticks()

            # ================= FASE 1 =================

            elif assets.mode == "fase1_1":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_1")

                elif assets.som1_rect.collidepoint(event.pos):
                    assets.som_grave1_fase1.stop()
                    assets.som_agudo1_fase1.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    assets.som_agudo1_fase1.stop()
                    assets.som_grave1_fase1.play()

            elif assets.mode == "pergunta_fase1_1":
                if pygame.Rect(350,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("amarelo")

                elif pygame.Rect(950,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase1) == {"azul"}
                    registrar_resposta("fase1","fase1_1",respostas_fase1,correta)
                    respostas_fase1.clear()
                    trocar_modo("fase1_2")

            elif assets.mode == "fase1_2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu_fase1")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_2")

                elif assets.som1_rect.collidepoint(event.pos):
                    assets.som_grave1_fase1.stop()
                    assets.som_agudo1_fase1.play()

                elif assets.som2_rect.collidepoint(event.pos):
                    assets.som_agudo1_fase1.stop()
                    assets.som_grave1_fase1.play()

            elif assets.mode == "pergunta_fase1_2":
                if pygame.Rect(350,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("amarelo")

                elif pygame.Rect(950,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase1) == {"amarelo"}
                    registrar_resposta("fase1","fase1_2",respostas_fase1,correta)
                    respostas_fase1.clear()
                    trocar_modo("fase1_3")

            elif assets.mode == "fase1_3":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase1_3")

            elif assets.mode == "pergunta_fase1_3":
                if pygame.Rect(350,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("amarelo")

                elif pygame.Rect(950,400,200,200).collidepoint(event.pos):
                    respostas_fase1.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase1) == {"amarelo"}
                    registrar_resposta("fase1","fase1_3",respostas_fase1,correta)
                    respostas_fase1.clear()
                    trocar_modo("menu_fase2")

            # ================= FASE 2 =================

            elif assets.mode == "menu_fase2":
                if assets.botao_voltar_rect.collidepoint(event.pos):
                    trocar_modo("menu")

                elif assets.botao_nuvem2_rect.collidepoint(event.pos):
                    trocar_modo("introducao_fase2")
                    inicio_modo = pygame.time.get_ticks()

            elif assets.mode == "fase2_1":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_1")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.musica_fase2_1.play()

            elif assets.mode == "pergunta_fase2_1":

                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase2.append("amarelo")

                elif assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase2.append("azul")
     
                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase2) == {"amarelo"}
                    registrar_resposta("fase2","fase2_1",respostas_fase2,correta)
                    respostas_fase2.clear()
                    trocar_modo("fase2_2")

            elif assets.mode == "fase2_2":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_2")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.musica_fase2_2.play()

            elif assets.mode == "pergunta_fase2_2":
                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase2.append("amarelo")

                if assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase2.append("azul")
             
                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase2) == {"azul"}
                    registrar_resposta("fase2","fase2_2",respostas_fase2,correta)
                    respostas_fase2.clear()
                    trocar_modo("fase2_3")


            elif assets.mode == "fase2_3":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase2_3")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.musica_fase2_3.play()

            elif assets.mode == "pergunta_fase2_3":
                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase2.append("amarelo")

                if assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase2.append("azul")
        
                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase2) == {"azul"}
                    registrar_resposta("fase2","fase2_3",respostas_fase2,correta)
                    respostas_fase2.clear()
                    trocar_modo("menu_fase3")

            # ================= FASE 3 =================

            elif assets.mode == "menu_fase3":
                if assets.botao_nuvem3_rect.collidepoint(event.pos):
                    trocar_modo("introducao_fase3")
                    inicio_modo = pygame.time.get_ticks()

            elif assets.mode == "fase3_1":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_1")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.melodia_fase3_1.play()

            elif assets.mode == "pergunta_fase3_1":
                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase3.append("amarelo")

                if assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase3.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase3) == {"azul"}
                    registrar_resposta("fase3","fase3_1",respostas_fase3,correta)
                    respostas_fase3.clear()
                    trocar_modo("fase3_2")

            elif assets.mode == "fase3_2":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_2")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.melodia_fase3_2.play()

            elif assets.mode == "pergunta_fase3_2":
                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase3.append("amarelo")

                if assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase3.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase3) == {"azul"}
                    registrar_resposta("fase3","fase3_2",respostas_fase3,correta)
                    respostas_fase3.clear()
                    trocar_modo("fase3_3")

            elif assets.mode == "fase3_3":
                if assets.botao_avancar_rect.collidepoint(event.pos):
                    trocar_modo("pergunta_fase3_3")

                elif assets.som3_rect.collidepoint(event.pos):
                    assets.melodia_fase3_3.play()

            elif assets.mode == "pergunta_fase3_3":

                if assets.rasp_amarelo_rect.collidepoint(event.pos):
                    respostas_fase3.append("amarelo")

                if assets.rasp_azul_rect.collidepoint(event.pos):
                    respostas_fase3.append("azul")

                elif assets.botao_avancar_rect.collidepoint(event.pos):
                    correta = set(respostas_fase3) == {"amarelo"}
                    registrar_resposta("fase3","fase3_3",respostas_fase3,correta)
                    respostas_fase3.clear()
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
                if assets.active_field == "nome":
                    if event.key == pygame.K_BACKSPACE:
                        assets.player_name = assets.player_name[:-1]
                    else:
                        assets.player_name += event.unicode

                elif assets.active_field == "escola":
                    if event.key == pygame.K_BACKSPACE:
                        assets.player_school = assets.player_school[:-1]
                    else:
                        assets.player_school += event.unicode

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

        jogador = pegar_ultimo_jogador()
        acertos, erros, por_fase = calcular_resultados(jogador)

        y = 100

    desenhar()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()