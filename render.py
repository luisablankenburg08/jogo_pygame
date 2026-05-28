import pygame
import assets
from utils import desenhar_barra_azul, desenhar_barra_amarela, desenhar_campo

pygame.init()

# =========================
# FUNÇÃO PRINCIPAL
# =========================
def desenhar():

    tela = assets.tela

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

        desenhar_campo(tela, assets.FONT, assets.CORES, "Nome:", assets.nome_rect, assets.player_name, assets.active_field == "nome")
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
        
        if "fase1_2" in assets.mode or "pergunta_fase1_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*2)
        
        if "fase1_3" in assets.mode or "pergunta_fase1_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*3)

        if "fase2_1" in assets.mode or "pergunta_fase2_1" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*4)

        if "fase2_2" in assets.mode or "pergunta_fase2_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*5)

        if "fase2_3" in assets.mode or "pergunta_fase2_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*6)
        
        if "fase3_1" in assets.mode or "pergunta_fase3_1" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*7)

        if "fase3_2" in assets.mode or "pergunta_fase3_2" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, ((assets.largura_tela)//9)*8)

        if "fase3_3" in assets.mode or "pergunta_fase3_3" in assets.mode:
            desenhar_barra_amarela(tela, assets.CORES, assets.largura_tela)

        if "fase" in assets.mode:
            pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_voltar_rect)
            tela.blit(assets.txt_voltar, assets.txt_voltar_rect)

        pygame.draw.rect(tela, assets.CORES["ciano"], assets.botao_avancar_rect)
        tela.blit(assets.txt_avancar, assets.txt_avancar_rect)

        tela.blit(assets.som, assets.som1_rect)
        tela.blit(assets.texto_som1_surface, assets.texto_som1_rect)
        tela.blit(assets.som, assets.som2_rect)
        tela.blit(assets.texto_som2_surface, assets.texto_som2_rect)

        if "pergunta_fase1" in assets.mode:
        
            tela.blit(assets.botao_rasp_amarelo_img, (assets.largura_tela*(23.3/100), assets.altura_tela*(41/100)))
            tela.blit(assets.botao_rasp_azul_img, (assets.largura_tela*(66/100), assets.altura_tela*(41/100)))

        elif "pergunta_fase2" in assets.mode:

            tela.blit(assets.botao_rasp_amarelo_img, (assets.largura_tela*(23.3/100), assets.altura_tela*(41/100)))
            tela.blit(assets.botao_rasp_azul_img, (assets.largura_tela*(66/100), assets.altura_tela*(41/100)))

        elif "pergunta_fase3" in assets.mode:
            tela.blit(assets.botao_rasp_amarelo_img, (assets.largura_tela*(23.3/100), assets.altura_tela*(41/100)))
            tela.blit(assets.botao_rasp_azul_img, (assets.largura_tela*(66/100), assets.altura_tela*(41/100)))
            

    # ================= RELATÓRIO =================
    elif assets.mode == "relatorio":

        tela.blit(assets.fundo_fases, (0, 0))

        tela.blit(assets.nuvem, (assets.largura_tela//2+250, assets.altura_tela//2-170))
        pygame.draw.rect(tela, assets.CORES["branco"], assets.botao_nuvem3_rect)
        tela.blit(assets.txt_nuvem3, assets.txt_nuvem3_rect)

        tela.blit(assets.bichinho2, (assets.largura_tela*(70/100), assets.altura_tela*(10/100)))
        tela.blit(assets.bandeira, (assets.largura_tela*(92/100), assets.altura_tela*(4/100)))

        tela.blit(assets.texto_relatorio_surf, assets.texto_relatorio_rect)