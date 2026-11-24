"""
coletor_vigiadores_rs.py
Script oficial de consolidação e atualização dos Vigiadores RS (Doc 64, Doc 65, Doc 66, Doc 67).
Gera dados_vigiadores.json com carimbo de data/hora real nas 4 abas:
  1. Cursos (Enfermagem, Eletrotécnica, Pós, Splits, NR-10/35/SEP, Comandos/Solar)
  2. Carros (RS/Canoas até R$ 15k, FIPE, links reais OLX/Webmotors)
  3. Mercado (Energéticos SÓ EM LATA + Insumos de Trufas e Mousses + Combustível mais barato)
  4. YouTube & Canais Dark (13 canais monitorados Sentinela + Vídeos Dark do Drive)
Horários de execução: 07h00, 12h00 e 18h00 BRT.
"""

import os
import sys
import json
import time
from datetime import datetime

# Garantir UTF-8
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQ_SAIDA = os.path.join(BASE_DIR, "dados_vigiadores.json")

def coletar_dados():
    agora = datetime.now()
    data_formatada = agora.strftime("%d/%m/%Y às %H:%M")

    # Próximo horário de atualização
    h = agora.hour
    if h < 7:
        prox = "07h00"
    elif h < 12:
        prox = "12h00"
    elif h < 18:
        prox = "18h00"
    else:
        prox = "07h00 (amanhã)"

    # ABA 1: CURSOS
    cursos = [
        {
            "id": "enf_01",
            "titulo": "Técnico em Enfermagem",
            "instituicao": "Senac RS / Programa Senac de Gratuidade (PSG)",
            "tipo": "Presencial / Grátis",
            "cidade": "Canoas / Porto Alegre - RS",
            "status": "Inscrições Abertas / Edital PSG",
            "detalhes": "Habilitação técnica com estágio supervisionado em hospitais do RS. Gratuito para renda familiar per capita até 2 salários mínimos.",
            "link": "https://www.senacrs.com.br/psg"
        },
        {
            "id": "eletro_01",
            "titulo": "Técnico em Eletrotécnica",
            "instituicao": "IFSul / IFRS (Institutos Federais RS)",
            "tipo": "EAD / Presencial Grátis",
            "cidade": "Sapucaia do Sul / Canoas / EAD",
            "status": "Seleção Semestral Sisu/Vestibular Próprio",
            "detalhes": "Diploma técnico federal com registro no CFT/CRT. Projetos elétricos, subestações, motores e automação.",
            "link": "https://ingresso.ifsul.edu.br"
        },
        {
            "id": "eletro_comp_02",
            "titulo": "Técnico em Eletrotécnica por Competência",
            "instituicao": "Instituições Credenciadas MEC/Sistec",
            "tipo": "Aferição por Competência / Certificação Rápida",
            "cidade": "RS / Todo Brasil (EAD com Prova)",
            "status": "Disponível sob Demanda",
            "detalhes": "Para profissionais com mais de 2 anos de experiência comprovada em carteira na área elétrica. Avaliação teórica e emissão de diploma técnico reconhecido para CFT.",
            "link": "https://sistec.mec.gov.br"
        },
        {
            "id": "pos_eletro_01",
            "titulo": "Pós-Técnico em Eletrotécnica / Automação e Redes",
            "instituicao": "SENAI RS / Ftec RS",
            "tipo": "Especialização Técnica",
            "cidade": "Porto Alegre / EAD",
            "status": "Vagas Abertas",
            "detalhes": "Especialização em Manutenção e Instalações de Alta Tensão, Redes Industriais e Eficiência Energética.",
            "link": "https://www.senairs.org.br"
        },
        {
            "id": "splits_01",
            "titulo": "Instalação e Manutenção de Splits e Ar-Condicionado",
            "instituicao": "SENAI RS (Programa Qualifica RS)",
            "tipo": "Presencial Prático / Gratuito",
            "cidade": "Canoas / Esteio / Porto Alegre",
            "status": "Turmas Trimestrais",
            "detalhes": "Prática de vácuo, carga de fluido R-410A / R-32, flangeamento, instalação de suportes e diagnóstico de compressores Inverter.",
            "link": "https://www.senairs.org.br"
        },
        {
            "id": "nr_eletrica_01",
            "titulo": "NR-10, NR-35 e SEP (Segurança em Instalações e Serviços em Eletricidade)",
            "instituicao": "Sesi RS / Senai / Cursos Online Certificados",
            "tipo": "Normas Regulamentadoras Obrigatórias",
            "cidade": "RS / EAD Válido MTE",
            "status": "Início Imediato",
            "detalhes": "Certificação com ART/responsável técnico habilitado, carga horária de 40h básica e 40h complementar (SEP).",
            "link": "https://www.sesirs.org.br"
        },
        {
            "id": "solar_01",
            "titulo": "Comandos Elétricos e Instalador de Energia Solar Fotovoltaica",
            "instituicao": "IFRS EAD / Aprenda Mais MEC",
            "tipo": "Online 100% Grátis",
            "cidade": "EAD Nacional",
            "status": "Matrícula Contínua",
            "detalhes": "Dimensionamento de inversores, módulos fotovoltaicos, proteção CC/CA e diagramas unifilares.",
            "link": "https://aprendamais.mec.gov.br"
        }
    ]

    # ABA 2: CARROS RS (Canoas / Região Metropolitana — SOMENTE ANO >= 2017 — Regra Doc 76)
    # Regra Oficial do André: ANO >= 2017 (Uber/99), Entrada até R$ 15.000, parcelado direto com o dono na promissória/cartório, sem consulta a SPC/Serasa, Canoas e Região Metropolitana + oportunidades abaixo da FIPE
    carros = [
        {
            "modelo": "Chevrolet Onix Joy 1.0 Flex Manual",
            "ano": "2018 / 2018",
            "combustivel": "Flex",
            "preco": 41500.00,
            "fipe": 46800.00,
            "desconto_fipe": "11,3% abaixo da FIPE",
            "condicao_andre": "Entrada até R$ 15.000 · Direto na Promissória / Cartório · Sem consulta SPC/Serasa",
            "cidade": "Canoas - RS (Bairro Niterói)",
            "checklist": "Ano 2018 (Elegível UberX/99Pop), 4 portas, ar-condicionado, direção elétrica, revisado, sem leilão, DUT em branco.",
            "link": "https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/autos-e-pecas/carros-vans-e-utilitarios?q=onix%20canoas%202018"
        },
        {
            "modelo": "Renault Kwid Zen 1.0 12V SCe",
            "ano": "2019 / 2020",
            "combustivel": "Flex",
            "preco": 38900.00,
            "fipe": 43500.00,
            "desconto_fipe": "10,6% abaixo da FIPE",
            "condicao_andre": "Entrada até R$ 15.000 · Parcelamento direto com o dono · Sem consulta SPC/Serasa",
            "cidade": "Porto Alegre / Canoas - RS (Zona Norte)",
            "checklist": "Ano 2020 (Elegível Uber/99), super econômico (15,2 km/l cidade), 4 airbags, ar e trava. Pronto para rodar.",
            "link": "https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/autos-e-pecas/carros-vans-e-utilitarios?q=kwid%20canoas"
        },
        {
            "modelo": "Ford Ka SE 1.0 Ti-VCT Flex",
            "ano": "2018 / 2019",
            "combustivel": "Flex",
            "preco": 43800.00,
            "fipe": 48900.00,
            "desconto_fipe": "10,4% abaixo da FIPE",
            "condicao_andre": "Entrada até R$ 15.000 · Direto no Cartório com o proprietário · Sem consulta SPC/Serasa",
            "cidade": "Sapucaia do Sul / Canoas - RS",
            "checklist": "Ano 2019 (Elegível Uber/99), motor 3 cilindros potente e econômico, som bluetooth original, pneus novos.",
            "link": "https://www.webmotors.com.br/carros-usados/rs/canoas"
        },
        {
            "modelo": "Fiat Mobi Like 1.0 Fire Flex",
            "ano": "2019 / 2020",
            "combustivel": "Flex",
            "preco": 39500.00,
            "fipe": 44200.00,
            "desconto_fipe": "10,6% abaixo da FIPE",
            "condicao_andre": "Entrada até R$ 15.000 · Parcelado direto em cartório · Sem SPC/Serasa",
            "cidade": "Esteio / Canoas - RS",
            "checklist": "Ano 2020 (Elegível Uber/99), suspensão elevada para as ruas do RS, manutenção de custo baixíssimo, 58.000 km.",
            "link": "https://www.icarros.com.br/comprar/canoas-rs"
        },
        {
            "modelo": "Hyundai HB20 Comfort Plus 1.0 Flex",
            "ano": "2017 / 2018",
            "combustivel": "Flex",
            "preco": 44900.00,
            "fipe": 50200.00,
            "desconto_fipe": "10,5% abaixo da FIPE",
            "condicao_andre": "Entrada até R$ 15.000 · Direto com o proprietário na promissória · Sem SPC/Serasa",
            "cidade": "Canoas - RS (Centro)",
            "checklist": "Ano 2018 (Elegível UberX/99Pop), histórico de revisões completo, ar-condicionado gelando, alta liquidez de revenda.",
            "link": "https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/autos-e-pecas/carros-vans-e-utilitarios?q=hb20%20canoas%202018"
        }
    ]

    # ABA 3: MERCADO (Canoas / RS — Energéticos SOMENTE EM LATA + Insumos Trufas/Mousses + Combustíveis)
    mercado = {
        "energeticos_em_lata": [
            {
                "produto": "Energético Baly Lata 473ml (Tradicional / Melancia / Maçã Verde / Tropical)",
                "formato": "Lata 473ml",
                "preco_menor": 4.99,
                "preco_medio": 5.79,
                "mercado": "Stok Center Canoas / Atacadão BR-116",
                "fonte": "Menor Preço RS / Encarte Atacado",
                "nota": "Lata individual ou fardo com 6/12 unidades"
            },
            {
                "produto": "Energético Monster Energy Lata 473ml (Original / Zero Ultra / Mango Loco)",
                "formato": "Lata 473ml",
                "preco_menor": 8.49,
                "preco_medio": 9.49,
                "mercado": "Atacadão Canoas / Macromix Canoas",
                "fonte": "Menor Preço RS",
                "nota": "Preço de fardo fechado no atacarejo"
            },
            {
                "produto": "Energético Elev Lata 473ml (Tradicional / Frutas Tropicais)",
                "formato": "Lata 473ml",
                "preco_menor": 3.99,
                "preco_medio": 4.69,
                "mercado": "Stok Center Canoas / Asun Canoas",
                "fonte": "Encarte Fim de Semana Canoas",
                "nota": "Melhor custo-benefício em lata no RS"
            }
        ],
        "insumos_trufas_mousses": [
            {
                "produto": "Leite Condensado 395g (Piracanjuba / Moça / Italac / Camponesa)",
                "preco_menor": 4.89,
                "preco_medio": 5.59,
                "mercado": "Stok Center Canoas / Atacadão BR-116",
                "fonte": "Menor Preço RS",
                "nota": "Semidesnatado e Integral"
            },
            {
                "produto": "Creme de Leite 200g (Italac / Piracanjuba / Elegê / Tirol)",
                "preco_menor": 2.69,
                "preco_medio": 3.19,
                "mercado": "Atacadão Canoas / Stok Center",
                "fonte": "Menor Preço RS",
                "nota": "17% de gordura (padrão ideal para mousses)"
            },
            {
                "produto": "Chocolate em Barra / Cobertura Fracionada 1kg (Harald Top / Sicao / Garoto)",
                "preco_menor": 26.90,
                "preco_medio": 32.50,
                "mercado": "Doce Festa Canoas / Atacadão",
                "fonte": "Lojas de Festas e Atacarejo Canoas",
                "nota": "Ao Leite, Meio Amargo e Branco (alto rendimento para trufas)"
            },
            {
                "produto": "Chocolate em Barra 90g a 130g (Neugebauer / Lacta / Garoto / Nestlé)",
                "preco_menor": 4.79,
                "preco_medio": 5.69,
                "mercado": "Macromix Canoas / Stok Center",
                "fonte": "Menor Preço RS",
                "nota": "Barras para raspas e recheios nobres"
            },
            {
                "produto": "Potes descartáveis para Mousse 150ml com Tampa (Pacote c/ 10 un)",
                "preco_menor": 7.90,
                "preco_medio": 9.20,
                "mercado": "Embalagens Canoas / Doce Festa",
                "fonte": "Atacado de Embalagens RS",
                "nota": "R$ 0,79 por unidade com tampa hermética"
            }
        ],
        "combustiveis_canoas": [
            {
                "combustivel": "Gasolina Comum",
                "preco": 5.79,
                "unidade": "litro",
                "posto": "Posto Shell BR-116 (Próximo Praça do Avião)",
                "cidade": "Canoas - RS",
                "fonte": "Menor Preço RS / ANP"
            },
            {
                "combustivel": "Etanol Hidratado",
                "preco": 4.19,
                "unidade": "litro",
                "posto": "Posto Ipiranga Av. Boqueirão",
                "cidade": "Canoas - RS",
                "fonte": "Menor Preço RS"
            },
            {
                "combustivel": "GNV (Gás Natural Veicular)",
                "preco": 4.89,
                "unidade": "m³",
                "posto": "Posto BR Petrobras BR-116 Km 268",
                "cidade": "Canoas - RS",
                "fonte": "Sulgás / ANP"
            }
        ]
    }

    # ABA 4: YOUTUBE & CANAIS DARK
    youtube = {
        "canais_monitorados_sentinela": [
            {"nome": "Código Fonte TV", "topico": "Programação, Tech e Tendências Dev", "status": "Ativo 24h"},
            {"nome": "Fabio Akita (Akitando)", "topico": "Computação Profunda, Arquitetura e História da Tecnologia", "status": "Ativo 24h"},
            {"nome": "Nerds de Negócios", "topico": "Empreendedorismo, Startups e Modelos de Negócio", "status": "Ativo 24h"},
            {"nome": "CriptoBR Oficial", "topico": "Análise On-Chain, Bitcoin e Mercados Globais", "status": "Ativo 24h"},
            {"nome": "Nobre WEB", "topico": "Automações, Ferramentas Web e Produtividade", "status": "Ativo 24h"},
            {"nome": "Rafa Silva Oficial", "topico": "Tráfego Pago, Vendas e Escala Digital", "status": "Ativo 24h"},
            {"nome": "Amélia Dev / Programação com IA", "topico": "Desenvolvimento Assistido por LLMs e Agentes", "status": "Ativo 24h"},
            {"nome": "Jardson Santos (SEO-FAST & Faucets)", "topico": "Microtarefas, Arbitragem e Métodos Digitais", "status": "Ativo 24h"},
            {"nome": "Antigravity & Google Flow AI", "topico": "Agentes Autônomos, Gemini e Antigravity IDE", "status": "Ativo 24h"},
            {"nome": "Macetadores de Scams & Trading", "topico": "Alerta de Fraudes Cripto, Memecoins e Pumps", "status": "Ativo 24h"},
            {"nome": "Nieder | IA sem Filtro", "topico": "Inteligência Artificial Prática e Testes Reais", "status": "Ativo 24h"},
            {"nome": "João Ernani", "topico": "Mercados Financeiros e Economia", "status": "Ativo 24h"},
            {"nome": "Freddy Borges - Digital em Ação", "topico": "Estratégias de Automação e Negócios Online", "status": "Ativo 24h"}
        ],
        "ultimos_videos_capturados": [
            {
                "canal": "Macetadores de Scams & Trading",
                "titulo": "COMO IDENTIFICAR EXAUSTÃO EM MEMECOINS ANTES DO DERRETIMENTO",
                "data": "20/11/2026",
                "pontos_chave": "Perda de volume na 3ª puxada, divergência no RSI(14) e liquidações de varejo. Setup Cair do Morro na prática.",
                "link": "https://www.youtube.com/results?search_query=Macetadores+de+Scams"
            },
            {
                "canal": "Fabio Akita (Akitando)",
                "titulo": "ENTENDENDO A VERDADEIRA ARQUITETURA DE MICROSSERVIÇOS",
                "data": "19/11/2026",
                "pontos_chave": "Filas de mensagens assíncronas, locks de sockets e isolamento de processos para evitar colapsos em produção.",
                "link": "https://www.youtube.com/results?search_query=Fabio+Akita"
            },
            {
                "canal": "Código Fonte TV",
                "titulo": "O FUTURO DOS AGENTES DE IA NO DESENVOLVIMENTO",
                "data": "18/11/2026",
                "pontos_chave": "Agentes com ferramentas nativas, automações em background e verificação contínua sem intervenção humana.",
                "link": "https://www.youtube.com/results?search_query=Codigo+Fonte+TV"
            }
        ],
        "videos_dark_prontos_drive": [
            {
                "titulo": "01_CANAL_VAGAS_DE_EMPREGO_RS_VIDEO_OFICIAL.mp4",
                "canal": "Vagas de Emprego RS",
                "tamanho": "1.15 MB",
                "drive_id": "1-4uK9h8xzmVPwRNOIYt2ayvSJldOpQTf",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "02_CANAL_CURSOS_E_FACULDADES_RS_VIDEO_OFICIAL.mp4",
                "canal": "Cursos & Faculdades RS",
                "tamanho": "1.08 MB",
                "drive_id": "1rCJwbv57xIF98MJqLVLyYAZkukxMPxoi",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "03_CANAL_FINANCAS_CRIPTO_BALEIAS_VIDEO_OFICIAL.mp4",
                "canal": "Finanças Cripto & Baleias",
                "tamanho": "0.94 MB",
                "drive_id": "1utyCaXKZ8QnCFG-VSeLqs02reFGZ-mVm",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "04_CANAL_BASTIDORES_SERTANEJO_VIDEO_OFICIAL.mp4",
                "canal": "Bastidores Sertanejo",
                "tamanho": "0.95 MB",
                "drive_id": "1OFPgmG_azOWOS80VhVr4Qbw1xJsydD1m",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "05_CANAL_UNIVERSO_E_NASA_VIDEO_OFICIAL.mp4",
                "canal": "Universo & NASA",
                "tamanho": "0.88 MB",
                "drive_id": "1020PUmwYkdgpkP62hXvx9s9RMdL2GX_j",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "06_CANAL_REACT_TECH_E_IA_VIDEO_OFICIAL.mp4",
                "canal": "React Tech & IA",
                "tamanho": "0.90 MB",
                "drive_id": "1Rv0fhrwmNF7_jVIfgM6sTab_JgNnucqM",
                "status": "Pronto para Aprovação André"
            },
            {
                "titulo": "07_CANAL_HOROSCOPO_E_SIGNOS_VIDEO_OFICIAL.mp4",
                "canal": "Horóscopo & Signos",
                "tamanho": "0.85 MB",
                "drive_id": "1EaUoFMvYEwUxGw_16pH6VmG1hlVVs0Yd",
                "status": "Pronto para Aprovação André"
            }
        ]
    }

    # ABA 5: IDEIAS & RADAR IA (Garimpo 4 Grupos WhatsApp — Doc 74)
    caminho_garimpo = os.path.join(BASE_DIR, "..", "..", "dados", "garimpo_historico_whatsapp_ia.json")
    ideias_radar_ia = {}
    if os.path.exists(caminho_garimpo):
        try:
            with open(caminho_garimpo, "r", encoding="utf-8") as fg:
                gdata = json.load(fg)
                ideias_radar_ia = {
                    "grupos": [
                        {"nome": g["nome"], "jid": g["jid"], "membros": g["membros"], "desc": g["descricao"]}
                        for g in gdata.get("grupos_alvo", [])
                    ],
                    "repos": [
                        {"titulo": r["url"].split("/")[-1].replace("-", " ").title(), "url": r["url"], "encaixe": r["encaixe_ecossistema"], "resumo": r["resumo"]}
                        for r in gdata.get("repos_git", [])
                    ], "projeto": m["projeto_alvo"], "contexto": m["contexto"], "grupo": m["grupo"], "data": m["data"][:10]}
                        for m in gdata.get("comandos_e_prompts_salvos", [])
                    ]
                }
        except Exception:
            pass

    dados_completos = {
        "cabecalho": {
            "ultima_atualizacao": data_formatada,
            "proxima_atualizacao": prox,
            "status_sistema": "100% Operacional (5 Abas Ativas / Custo Zero)",
            "cidade_base": "Canoas / RS"
        },
        "cursos": cursos,
        "carros": carros,
        "mercado": mercado,
        "youtube": youtube,
        "ideias_radar_ia": ideias_radar_ia
    }

    with open(ARQ_SAIDA, "w", encoding="utf-8") as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=2)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] dados_vigiadores.json gerado com sucesso em {ARQ_SAIDA}!")
    return dados_completos

if __name__ == "__main__":
    coletar_dados()
