import pygame
import assets
from utils import desenhar_barra_azul, desenhar_barra_amarela, desenhar_campo, gerar_relatorio, obter_ultimo_jogador

pygame.init()

# =========================
# FUNÇÃO PRINCIPAL
# =========================

def desenhar():
    tela = assets.tela
    cor_botao1 = assets.CORES["magenta"]
    cor_botao2 = assets.CORES["ciano"]

    if assets.resposta_selecionada == "som1" or assets.resposta_selecionada == "guitarra" or assets.resposta_selecionada == "iguais":
        cor_botao1 = assets.CORES["magenta_opaco"]

    if assets.resposta_selecionada == "som2" or assets.resposta_selecionada == "violão" or assets.resposta_selecionada == "diferentes":
        cor_botao2 = assets.CORES["ciano_opaco"]

    # ================= MENU =================
    if assets.mode == "menu":
        tela.blit(assets.background, (0, 0))
        tela.blit(
            assets.quadro_menu,
            ((assets.largura_tela - assets.quadro_menu.get_width()) // 2,
             (assets.altura_tela - assets.quadro_menu.get_height()) // 2)
        )

        for surf, rect, txt, txt_rect in [
            (assets.surf_sair, assets.botao_sair_rect, assets.txt_sair, assets.txt_sair_rect),
            (assets.surf_ajuda, assets.botao_ajuda_rect, assets.txt_ajuda, assets.txt_ajuda_rect),
            (assets.surf_jogar, assets.botao_jogar_rect, assets.txt_jogar, assets.txt_jogar_rect),
        ]:
            tela.blit(surf, rect.topleft)
            tela.blit(txt, txt_rect)

    # ================= AJUDA =================
    elif assets.mode == "ajuda":
        tela.blit(assets.fundo_fases, (0, 0))

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
        tela.blit(assets.txt_voltar, assets.txt_voltar_rect)

        pos_y = assets.posicao_y

        for superficie in assets.superficies_texto_ajuda:
            rect = superficie.get_rect(center=(assets.largura_tela // 2, pos_y))
            tela.blit(superficie, rect)
            pos_y += 40

        assets.posicao_y -= assets.velocidade_rolagem_ajuda
        if pos_y < 0:
            assets.posicao_y = assets.altura_tela

    # ================= FASE 0 =================
    elif assets.mode == "fase0":
        tela.blit(assets.background_fase0, (0, 0))
        tela.blit(
            assets.quadro_fase0,
            ((assets.largura_tela - assets.quadro_fase0.get_width()) // 2,
             (assets.altura_tela - assets.quadro_fase0.get_height()) // 2)
        )

        desenhar_campo(tela, assets.FONT, assets.CORES, "Usuário:", assets.usuario, assets.player_name, assets.active_field == "usuario")
        desenhar_campo(tela, assets.FONT, assets.CORES, "Escola:", assets.escola_rect, assets.player_school, assets.active_field == "escola")
        desenhar_campo(tela, assets.FONT, assets.CORES, "Série:", assets.serie_rect, assets.player_serie)

        if assets.dropdown_aberto:
            for i, opcao in enumerate(assets.opcoes_serie):
                rect = pygame.Rect(
                    assets.serie_rect.x,
                    assets.serie_rect.y + (i+1)*40,
                    assets.serie_rect.width,
                    40
                )
                pygame.draw.rect(tela, assets.CORES["amarelo"], rect)
                tela.blit(assets.FONT.render(opcao, True, assets.CORES["preto"]), (rect.x+5, rect.y+5))

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_comecar_rect)
        tela.blit(assets.txt_comecar, assets.txt_comecar_rect)

        if assets.error_msg:
            tela.blit( assets.FONT.render(assets.error_msg, True, assets.CORES["vermelho"]), (assets.largura_tela*37/100, assets.altura_tela*33/100) )

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
        tela.blit(assets.txt_voltar, assets.txt_voltar_rect)

    # ================= MENUS DE FASE =================
    elif assets.mode in ["menu_fase1", "menu_fase2", "menu_fase3"]:
        tela.blit(assets.fundo_fases, (0, 0))

        tela.blit(assets.nuvem, (assets.largura_tela//4-50, assets.altura_tela//2+50))
        tela.blit(assets.nuvem, (assets.largura_tela//2-50, assets.altura_tela//2-50))
        tela.blit(assets.nuvem, (assets.largura_tela//2+250, assets.altura_tela//2-170))

        pygame.draw.rect(tela, assets.CORES["branco"], assets.botao_fase1_rect)
        pygame.draw.rect(tela, assets.CORES["branco"], assets.botao_nuvem2_rect)
        pygame.draw.rect(tela, assets.CORES["branco"], assets.botao_nuvem3_rect)

        tela.blit(assets.txt_fase1, assets.txt_fase1_rect)
        tela.blit(assets.txt_nuvem2, assets.txt_nuvem2_rect)
        tela.blit(assets.txt_nuvem3, assets.txt_nuvem3_rect)
        tela.blit(assets.bandeira, (assets.largura_tela*(92/100), assets.altura_tela*(4/100)))

        if assets.mode == "menu_fase1":
            tela.blit(assets.cadeado, (assets.largura_tela//2-50, assets.altura_tela//2-50))
            tela.blit(assets.cadeado, (assets.largura_tela//2+250, assets.altura_tela//2-170))
            tela.blit(assets.bichinho1, (assets.largura_tela*(4/100), assets.altura_tela*(60/100)))

        elif assets.mode == "menu_fase2":
            tela.blit(assets.cadeadoaberto, (assets.largura_tela//2-50, assets.altura_tela//2-70))
            tela.blit(assets.cadeado, (assets.largura_tela//2+250, assets.altura_tela//2-170))
            tela.blit(assets.bichinho1, (assets.largura_tela*(23/100), assets.altura_tela*(37/100)))

        elif assets.mode == "menu_fase3":
            tela.blit(assets.cadeadoaberto, (950, 200))
            tela.blit(assets.bichinho1, (assets.largura_tela*(48/100), assets.altura_tela*(25/100)))

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
        tela.blit(assets.txt_voltar, assets.txt_voltar_rect)

    # ================= INTRODUÇÕES =================
    elif assets.mode == "introducao_fase1":
        tela.blit(assets.fundo_fases, (0, 0))
        tela.blit(assets.texto_intro1_surf, assets.texto_intro1_rect)

    elif assets.mode == "introducao_fase2":
        tela.blit(assets.fundo_fases, (0, 0))
        tela.blit(assets.texto_intro2_surf, assets.texto_intro2_rect)

    elif assets.mode == "introducao_fase3":
        tela.blit(assets.fundo_fases, (0, 0))
        tela.blit(assets.texto_intro3_surf, assets.texto_intro3_rect)

    # ================= FASES =================
    elif "fase" in assets.mode or "pergunta" in assets.mode:

        tela.blit(assets.fundo_fases, (0, 0))

        desenhar_barra_azul(tela, assets.CORES, assets.largura_tela)

        if "fase1_1" in assets.mode or "pergunta_fase1_1" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, (assets.largura_tela)//9)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase1_2" in assets.mode or "pergunta_fase1_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*2)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase1_3" in assets.mode or "pergunta_fase1_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*3)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase2_1" in assets.mode or "pergunta_fase2_1" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*4)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase2_2" in assets.mode or "pergunta_fase2_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*5)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase2_3" in assets.mode or "pergunta_fase2_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*6)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)
        
        if "fase3_1" in assets.mode or "pergunta_fase3_1" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*7)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase3_2" in assets.mode or "pergunta_fase3_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*8)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase3_3" in assets.mode or "pergunta_fase3_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, assets.largura_tela)
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo1_rect)
            tela.blit(assets.txt_quadro_explicativo1, assets.txt_quadro_explicativo1_rect)

        if "fase" in assets.mode:
            pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
            tela.blit(assets.txt_voltar, assets.txt_voltar_rect)

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_avancar_rect)
        tela.blit(assets.txt_avancar, assets.txt_avancar_rect)

        if assets.som_agudo1_fase1.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        elif assets.som_agudo2_fase1.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        elif assets.som_agudo3_fase1.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        elif assets.melodia1_fase3.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        elif assets.melodia3_fase3.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        elif assets.melodia5_fase3.get_num_channels() > 0:
            texto_tocando = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
            texto_tocando_rect = texto_tocando.get_rect(center=(assets.som1_rect.centerx, assets.som1_rect.top - 20))
            tela.blit(texto_tocando, texto_tocando_rect)

        # ================= BOTÕES DE SOM =================

        if assets.mode in (
            "fase2_1",
            "fase2_2",
            "fase2_3"
        ):
            if (
                assets.musica_fase2_1.get_num_channels() > 0 or
                assets.musica_fase2_2.get_num_channels() > 0 or
                assets.musica_fase2_3.get_num_channels() > 0
            ):
                texto = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
                texto_rect = texto.get_rect(center=(assets.som3_rect.centerx, assets.som3_rect.top - 20))
                tela.blit(texto, texto_rect)

            tela.blit(assets.som, assets.som3_rect)
            tela.blit(assets.texto_som3_surface, assets.texto_som3_rect)

        else:

            # ---------- SOM 1 ----------

            if (
                assets.som_agudo1_fase1.get_num_channels() > 0 or
                assets.som_agudo2_fase1.get_num_channels() > 0 or
                assets.som_agudo3_fase1.get_num_channels() > 0 or
                assets.melodia1_fase3.get_num_channels() > 0 or
                assets.melodia3_fase3.get_num_channels() > 0 or
                assets.melodia5_fase3.get_num_channels() > 0
            ):
                texto = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
                texto_rect = texto.get_rect(center=(assets.som1_rect.centerx,assets.som1_rect.top - 20))
                tela.blit(texto, texto_rect)

            tela.blit(assets.som, assets.som1_rect)
            tela.blit(assets.texto_som1_surface, assets.texto_som1_rect)

            # ---------- SOM 2 ----------

            if (
                assets.som_grave1_fase1.get_num_channels() > 0 or
                assets.som_grave2_fase1.get_num_channels() > 0 or
                assets.som_grave3_fase1.get_num_channels() > 0 or
                assets.melodia2_fase3.get_num_channels() > 0 or
                assets.melodia4_fase3.get_num_channels() > 0 or
                assets.melodia6_fase3.get_num_channels() > 0
            ):
                texto = assets.fonte_pequena.render("Tocando...", True, assets.CORES["preto"])
                texto_rect = texto.get_rect(center=(assets.som2_rect.centerx, assets.som2_rect.top - 20))
                tela.blit(texto, texto_rect)

            tela.blit(assets.som, assets.som2_rect)
            tela.blit(assets.texto_som2_surface, assets.texto_som2_rect)

        if "pergunta_fase1" in assets.mode:
        
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo2_rect)
            tela.blit(assets.txt_quadro_explicativo2, assets.txt_quadro_explicativo2_rect)

            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao1_resposta_rect ,border_radius=10)
            pygame.draw.rect(tela, cor_botao1, assets.botao1_resposta1_rect)
            tela.blit(assets.txt_botao1_resposta1, assets.txt_botao1_resposta1_rect)

            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao2_resposta_rect,border_radius=10)
            pygame.draw.rect(tela, cor_botao2, assets.botao2_resposta1_rect)
            tela.blit(assets.txt_botao2_resposta1, assets.txt_botao2_resposta1_rect)

        elif "pergunta_fase2" in assets.mode:
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo2_rect)
            tela.blit(assets.txt_quadro_explicativo4, assets.txt_quadro_explicativo4_rect)


            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao1_resposta_rect ,border_radius=10)
            pygame.draw.rect(tela, cor_botao1, assets.botao1_resposta2_rect)
            tela.blit(assets.txt_botao1_resposta2, assets.txt_botao1_resposta2_rect)


            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao2_resposta_rect,border_radius=10)
            pygame.draw.rect(tela, cor_botao2, assets.botao2_resposta2_rect)
            tela.blit(assets.txt_botao2_resposta2, assets.txt_botao2_resposta2_rect)

        elif "pergunta_fase3" in assets.mode:
            pygame.draw.rect(tela, assets.CORES["amarelo"], assets.quadro_explicativo3_rect)
            tela.blit(assets.txt_quadro_explicativo3, assets.txt_quadro_explicativo3_rect)

            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao1_resposta_rect,border_radius=10)
            pygame.draw.rect(tela, cor_botao1, assets.botao1_resposta3_rect)
            tela.blit(assets.txt_botao1_resposta3, assets.txt_botao1_resposta3_rect)

            pygame.draw.rect(tela, assets.CORES["preto"], assets.borda_botao2_resposta_rect,border_radius=10)
            pygame.draw.rect(tela, cor_botao2, assets.botao2_resposta3_rect)
            tela.blit(assets.txt_botao2_resposta3, assets.txt_botao2_resposta3_rect)

            

    # ================= RELATÓRIO =================
    elif assets.mode == "relatorio":
        tela.blit(assets.fundo_fases, (0, 0))

        relatorio = gerar_relatorio(
            obter_ultimo_jogador()
        )

        tela.blit(
            assets.texto_relatorio_surf,
            assets.texto_relatorio_rect
        )

        y = 220

        linhas = [
            f"Usuário: {relatorio['usuario']}",
            f"Escola: {relatorio['escola']}",
            f"Série: {relatorio['serie']}",
            "",
            f"Total de acertos: {relatorio['acertos']}",
            f"Total de erros: {relatorio['erros']}",
            "",
            f"Fase 1: {relatorio['fases']['fase1']['acertos']} acertos | {relatorio['fases']['fase1']['erros']} erros",
            f"Fase 2: {relatorio['fases']['fase2']['acertos']} acertos | {relatorio['fases']['fase2']['erros']} erros",
            f"Fase 3: {relatorio['fases']['fase3']['acertos']} acertos | {relatorio['fases']['fase3']['erros']} erros",
        ]

        for linha in linhas:
            texto = assets.fonte_relatorio.render(
                linha,
                True,
                assets.CORES["preto"]
            )

            tela.blit(texto, (100, y))
            y += 40

        tela.blit(assets.nuvem, (assets.largura_tela//2+250, assets.altura_tela//2-170))
        pygame.draw.rect(tela, assets.CORES["branco"], assets.botao_nuvem3_rect)
        tela.blit(assets.txt_nuvem3, assets.txt_nuvem3_rect)

        tela.blit(assets.bichinho2, (assets.largura_tela*(70/100), assets.altura_tela*(10/100)))
        tela.blit(assets.bandeira, (assets.largura_tela*(92/100), assets.altura_tela*(4/100)))

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
        tela.blit(assets.txt_voltar, assets.txt_voltar_rect)
