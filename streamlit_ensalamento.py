# app.py
import streamlit as st
import pandas as pd
import random
from unidecode import unidecode
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)
from reportlab.lib.units import cm
import io
import zipfile
from itertools import zip_longest

# =====================================================================
#           CONFIGURAÇÃO INICIAL DA PÁGINA
# =====================================================================
st.set_page_config(page_title="Gerador de Ensalamento", page_icon="🎓", layout="wide")


# =====================================================================
#           DADOS E LISTAS DE ALUNOS
# =====================================================================
@st.cache_data
def get_student_lists():
    return {
        "list_6ANO": [
            "ALICE SALVADOR",
            "ANA LAURA DE DEUS SIQUEIRA MEDEIROS",
            "ANA LUIZA SANTOS OLIVEIRA",
            "ARTHUR CARVALHO GONTIJO MOTA",
            "BERNARDO CÉSAR GONÇALVES E FERREIRA",
            "CÁSSIA MONTEIRO NETO",
            "CECÍLIA CARVALHO MAIA FONSECA",
            "CECÍLIA SILVA MATOS VIEIRA",
            "GABRIEL MORAIS FREITAS DE PAULA",
            "HEITOR AUGUSTO CAETANO ROMÃO",
            "ISAAC SILVA PORTO",
            "JOÃO EMILIO MACHADO DA CUNHA",
            "JOÃO VÍTOR COELHO MATOS",
            "JÚLIA MENDES NEULS",
            "LARISSA DIAS OLIVEIRA",
            "LORENZO DE SOUZA ASSIS",
            "LUCAS OLIVEIRA SILVA",
            "LUNA BARCELOS ABDALA",
            "MARIA EDUARDA LUIZ DE CARVALHO",
            "NÍCOLAS MATOS FALCÃO",
            "PEDRO CAIXETA FERREIRA",
            "PEDRO HENRIQUE BORGES CHAVES",
            "RAFAEL ALVES SANTOS",
            "SAMUEL OLIVEIRA SILVA",
            "SOPHIA RIBEIRO SILVA",
            "ALICE CHRISTINE CUNHA",
            "ALICIA JIAYIN LIU",
            "ANA LAURA QUEIROZ CASALI REIS",
            "ANTÔNIO TAVARES MARTINS",
            "BENÍCIO OLIVEIRA NAIMEG",
            "BERNARDO BARBOSA GONÇALVES",
            "BERNARDO DE CASTRO ÁVILA RESENDE",
            "DAVI OLIVIERI FERREIRA",
            "EDUARDO MARQUES DE OLIVEIRA ROSSI",
            "ENRICO DOMINGOS MOTA BONTEMPO MARTINS",
            "FERNANDA FERNANDES SOUSA",
            "FERNANDO FERREIRA DE QUEIROZ",
            "GABRIEL CAIXETA ALVES",
            "HELENA AVILA ESTANISLAU",
            "ISADORA BORGES FERNANDES RODRIGUES",
            "JÚLIA BORGES GATTÁS",
            "JÚLIA RODRIGUES ARAUJO",
            "LÍVIA FURTADO MARQUES",
            "LUIZA CARVALHO MENDES PIRES",
            "MARCELA RABELO AMORIM",
            "MARIA CLARA MACHADO",
            "MARIA LUIZA CANESCHI GOMES",
            "PEDRO MEDEIROS CAIXETA",
            "RAFAEL GONÇALVES NASCENTES DE OLIVEIRA",
            "VALENTINA PACHECO PARRILLO",
        ],
        "list_7ANO": [
            "ANDRÉ FRANCISCO FERNANDES COIMBRA",
            "ANNA LAURA FERREIRA SILVA LIMA",
            "ANTÔNIO CORRÊA DE OLIVEIRA NETO",
            "ARTHUR JUNIO MARTINS DE SOUSA",
            "BENICIO TEODORO REIS COSTA",
            "CECÍLIA ANDRADE PIAU RODRIGUES",
            "GABRIEL GARCIA DE MELLO",
            "ISABELA CHODRAUI PIVA",
            "JOAQUIM OTAVIO OLIVEIRA CARDOSO",
            "JULIA FERREIRA DE QUEIROZ",
            "MARCELO PEREIRA CAIXETA",
            "MARIA EDUARDA LUIZ MORO",
            "MARIA FERNANDA BARROS",
            "MARIANA CAIXETA CANEDO",
            "MELINA MOTA RAMOS",
            "MURILO SOARES E SILVA",
            "OTAVIO HENRIQUE DE FARIA FELIPE",
            "PEDRO CÉSAR ROSÁRIO DE SOUSA",
            "PEDRO HENRIQUE MAGALHÃES CALDEIRA",
            "PEDRO OSÓRIO RUELA VIEIRA",
            "PEDRO RIBEIRO CAIXETA DE SOUSA",
            "RAFAEL ARCANJO DE LIMA",
            "RAFAEL DAYRELL ROCHA TEIXEira",
            "RAÍSSA OLIVEIRA ATAÍDE",
            "SOFIA GONTIJO FARIA",
            "THEO LIMA GONTIJO",
            "THOMÁZ MAIA PELET CARVALHO",
            "VALENTINA ARVELOS ROCHA",
            "VALENTINA GONÇALVES MAGALHÃES RIBEIRO",
            "VITTORIA ÁVILA SANT´ ANA",
            "ALEXANDRE SOUSA DA CUNHA",
            "ALICE VIEIRA MELO",
            "ARTHUR GUIMARÃES GONTIJO",
            "BRUNNA ISABEL GOMES VIEIRA",
            "CECÍLIA ALVES NUNES",
            "DAVI HENRIQUE MOTA",
            "DAVID CAIXETA FONSECA",
            "EDUARDO ALVES DE ANDRADE",
            "JOÃO GABRIEL VERISSIMO SOARES",
            "JULIA AMORIM SILVA",
            "LUCAS SOARES SILVA",
            "LUIZA CONDE AUAD BRANDÃO",
            "MANUELA CORRÊA TROOST",
            "MARIA LAURA GOMES RODRIGUES",
            "RAFAEL OLIVEIRA GONÇALVES",
            "RAFAELA AMÂNCIO ALVES",
            "RENATO DIAS MARIANO",
            "SAMUEL RAMOS PENA FERREIRA SAIRRE",
            "SARAH CRISTINA ANDRADE",
            "SOPHIA EDUARDA ALVES VICTOR",
            "VALENTINA ARAUJO QUEIROZ",
            "VALENTINA DIAS TAVARES DO AMARAL",
            "VALENTINA OLIVEIRA ROCHA",
            "YNNARA MARIA PORTO BOMTEMPO",
        ],
        "list_8ANO": [
            "ARTHUR FERREIRA DE OLIVEIRA MELO",
            "CLARA ARAÚJO BORGES",
            "EDUARDA COELHO AMORIM",
            "GABRIEL FIDELIS MACIEL",
            "INÁCIO FERREIRA FLÔR",
            "LORENZO TELLES QUEIROZ",
            "LUCAS RODRIGUES COELHO",
            "LUCCA RIBEIRO ARAUJO REGO",
            "MANUELA DE DEUS SIQUEIRA MEDEIROS",
            "MANUELA LAVINE BRANT ABREU",
            "MARIA CECÍLIA ALVES ARAUJO",
            "MARIA CLARA OLIVEIRA CASTRO",
            "MATHEUS CAIXETA SILVA",
            "MATHEUS MOREIRA SILVA",
            "MIGUEL LORENZO FERREIRA",
            "PEDRO BIANCHINI REIS",
            "RAFAEL FIDELIS MACIEL",
            "SAULO DE CASTRO PERES FONSECA",
            "VALENTINA FIDELIS VIEIRA",
            "VINÍCIUS VASCONCELOS DOS REIS PEREIRA",
            "YURI ALVARENGA AZEVEDO",
            "ANNY GABRYELE ALVES FERNANDES",
            "CECÍLIA FERNANDES RABELO",
            "CECÍLIA GONTIJO SEIBT",
            "DAVI CÉSAR FERREIRA",
            "FILIPE MACEDO DE QUEIROZ FRANCO",
            "FILLIPE STEVÃO VALADÃO",
            "GABRIEL ALVES ROMÃO",
            "GIULIA SOUZA RODRIGUES",
            "HENRIQUE ASSIS SOARES",
            "HUGO BORGES MOREIRA",
            "ISADORA CUNHA COURY CAIXETA",
            "JORDANA IARA MARTINS SOARES",
            "LUCAS LOPES",
            "LUCAS MAIA CARVALHO MARTINS",
            "LUIS MIGUEL SILVA DE MELO",
            "LUIZ GUSTAVO SILVA",
            "MANUELA CARVALHO MENDES PIRES",
            "MARIA CLARA SILVA COELHO",
            "MIGUEL DA CRUZ PAULINO",
            "MIGUEL LARA LANZA STABILE",
            "MIGUEL REIS DIAS",
            "RAFAEL MARTINS TOLENTINO",
            "VITOR OLIVEIRA GONÇALVES",
            "YAN FERREIRA SOARES",
        ],
        "list_9ANO": [
            "AKEMI ALVARENGA MELO DE QUEIROZ",
            "ANA ALICE FERNANDES RIBEIRO",
            "ANA CLARA OLIVEIRA LOPES",
            "ANA CLARA PEREIRA SOUSA GONÇALVES",
            "ANALLU RAMOS PENA FERREIRA SAIRRE",
            "ARTUR DE OLIVEIRA PESSOA",
            "BIANCA MENDES NEULS",
            "EDMUNDO VAZ DE OLIVEIRA CAIXETA",
            "EMANUEL OLIVEIRA FONSECA",
            "FERNANDO PORTO CUNHA",
            "GABRIELA AMÂNCIO MACÊDO FRANÇA",
            "ÍSIS BEATRIZ DE CASTRO FARIA",
            "JÚLIA DEVOTI VILELA DE BRITO",
            "LAURA OLIVEIRA CHAVES",
            "LUCAS GABRIEL CAIXETA",
            "LUCAS MEDEIROS CAIXETA",
            "LUCAS YANMEI WEIDA",
            "LUÍSA DE PAULA LACERDA",
            "MARIA CLARA PEREIRA ARANTES",
            "MARIA CLARA RIBEIRO BORGES DE ALMEIDA",
            "MARIA EDUARDA ALVES DE QUEIROZ BICALHO",
            "MARIA FERNANDA PAES LACERDA",
            "MARIA PAULA MARTINS BORGES",
            "MARIANA ARAÚJO LANA",
            "NICOLAS FAGUNDES SOUZA",
            "NIKOLLY FERREIRA CAIXETA",
            "PEDRO AUGUSTO SOARES NOGUEIRA ARCANJO",
            "RAFAEL CARVALHO GONTIJO MOTA",
            "TOMAZ ROCHA PORTO",
            "VALENTINA STÉPHANY SANTANA ARAUJO",
            "VICTÓRIA MARTINS MELO FERREIRA",
            "VITOR BOLINA DUARTE",
            "ANA BEATRIZ PASSOS SCARDELATO",
            "ANA VICTORIA MARCONDES LEÃO",
            "ARTHUR MEIRELES BICALHO",
            "BERNARDO TELES GUEDES",
            "CAIO HENRIQUE SANTANA PEREIRA",
            "DANTE MACHADO PORTO QUEIROZ",
            "DAVI CALAZANS DE QUEIROZ FRANCO",
            "EDUARDO AZEVEDO BARBOSA",
            "GABRIELLA CORREA SILVA",
            "GUSTAVO BURGOS TEIXEIRA",
            "HEITOR MATOS FALCÃO",
            "JOÃO PEDRO DE DEUS SIQUEIRA MEDEIROS",
            "LETÍCIA ABREU TOLENTINO",
            "LUCAS CRISTIANO DE BRITO CAMBRAIA",
            "LUCAS SILVA FERREIRA",
            "LUÍZA FONSECA PÔRTO",
            "MANOEL ALFEU RAUSIS NASCIMENTO",
            "MARIA CLARA VERÍSSIMO SOARES",
            "MARIA EDUARDA SILVA SALES",
            "MARIA FERNANDA FERREIRA SILVA LIMA",
            "MARIA VITÓRIA RODRIGUES SOARES",
            "MIGUEL ANTÔNIO SILVERIO SILVA",
            "MIGUEL ARCANJO BORGES",
            "MIGUEL MIRANDA NORONHA",
            "NATHÁLIA EMILYN DA SILVA SOUSA",
            "NICOLAS LEAL GONÇALVES DIAS",
            "OLÍVIA JARDIM PFEILSTICKER SILVA",
            "PAOLA COSTA NAKAO",
            "PEDRO AUGUSTO XAVIER DE CARVALHO",
            "SOFIA VICTORIA SOUSA E SILVA",
            "VÍTOR ROCHA PEREIRA",
        ],
    }


# Os valores estão como (filas, lugares_por_fila)
filas_lugares = {
    "Sala 32 - 7º JM": (5, 6),  # 5 filas de 6 lugares = 30 vagas
    "Sala 33 - 9º JMB": (5, 6),  # 5 filas de 6 lugares = 30 vagas
    "Sala 20 - 9º MC": (5, 6),  # 5 filas de 6 lugares = 30 vagas
    "Sala 31 - 7º MB": (9, 3),  # 3 filas de 9 lugares = 27 vagas  troquei aqiu
    "Sala 04 - 8º JM": (5, 5),  # 5 filas de 5 lugares = 25 vagas
    "Sala 36 - 6º MB": (8, 3),  # 3 filas de 8 lugares = 24 vagas troquei aqui
    "Sala 38 - 6º JM": (8, 3),  # 3 filas de 8 lugares = 24 vagas troquei aqui
    "Sala 05 - 8º MB": (4, 6),  # 4 filas de 6 lugares = 24 vagas
}


# =====================================================================
#           FUNÇÕES DE LÓGICA
# =====================================================================


def remover_acentos(lista):
    return [unidecode(nome) for nome in lista]


def intercalar_listas(*listas):
    resultado = []
    indices = [0] * len(listas)
    while any(index < len(lista) for index, lista in zip(indices, listas)):
        for i, lista in enumerate(listas):
            if indices[i] < len(lista):
                resultado.append(lista[indices[i]])
                indices[i] += 1
    return resultado


def turma_do_aluno(aluno, listas_com_turmas):
    for lista, turma in listas_com_turmas:
        if aluno in lista:
            return turma
    return ""


def distribuir_alunos_sem_mesma_turma_ao_lado_ou_acima(
    alunos, filas, lugares_por_fila, listas_com_turmas
):
    random.shuffle(alunos)
    sala = [[""] * lugares_por_fila for _ in range(filas)]
    alunos_a_posicionar = list(alunos)
    for row in range(filas):
        for col in range(lugares_por_fila):
            if not alunos_a_posicionar:
                break

            turma_esquerda = ""
            if col > 0:
                turma_esquerda = turma_do_aluno(sala[row][col - 1], listas_com_turmas)

            turma_acima = ""
            if row > 0:
                turma_acima = turma_do_aluno(sala[row - 1][col], listas_com_turmas)

            indices_candidatos = list(range(len(alunos_a_posicionar)))
            random.shuffle(indices_candidatos)
            escolhido_idx = None
            for idx in indices_candidatos:
                turma_candidato = turma_do_aluno(
                    alunos_a_posicionar[idx], listas_com_turmas
                )
                if turma_candidato != turma_esquerda and turma_candidato != turma_acima:
                    escolhido_idx = idx
                    break
            if escolhido_idx is None and alunos_a_posicionar:
                escolhido_idx = 0
            if escolhido_idx is not None:
                sala[row][col] = alunos_a_posicionar.pop(escolhido_idx)
    return sala


def adicionar_turma(aluno, listas_com_turmas):
    if not aluno or not aluno.strip():
        return ""
    for lista, turma in listas_com_turmas:
        if aluno in lista:
            return f"{aluno} ({turma})"
    return aluno


# CORREÇÃO: Garante que as linhas são "Fila X" e as colunas são "Carteira X"
def sala_para_dataframe(sala, listas_com_turmas):
    sala_com_turma = []
    for fila in sala:
        fila_com_turma = [adicionar_turma(aluno, listas_com_turmas) for aluno in fila]
        sala_com_turma.append(fila_com_turma)

    if not sala_com_turma:
        return pd.DataFrame()

    # Cria o DataFrame diretamente. As linhas de 'sala_com_turma' já são as filas da sala.
    df = pd.DataFrame(sala_com_turma)

    # Atribui os nomes aos eixos conforme a visualização desejada:
    # Linhas (index): Fila 1, Fila 2... (correspondendo às fileiras da sala)
    # Colunas: Carteira 1, Carteira 2... (correspondendo aos lugares em cada fila)
    df.columns = [f"Fila {i+1}" for i in range(df.shape[1])]

    return df


# =====================================================================
#           FUNÇÕES DE GERAÇÃO DE ARQUIVOS
# =====================================================================
def gerar_mapa_salas_pdf(df_salas, data_ensalamento, data_aplicacao, disciplinas):
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,  # CORREÇÃO: Alterado de landscape(A4) para A4 (retrato)
        topMargin=1 * cm,
        bottomMargin=1 * cm,
        leftMargin=1 * cm,
        rightMargin=1 * cm,
    )

    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle(
        name="Normal_Small", parent=styles["Normal"], fontSize=14, autoLeading='max'
    )
    style_title = styles["Title"]

    elements = []

    salas_items = list(df_salas.items())
    for i, (nome_sala, df_sala) in enumerate(salas_items):
        # O DataFrame df_sala já vem de sala_para_dataframe na orientação correta
        # (Filas como linhas, Carteiras como colunas). Não é necessária transposição aqui.
        df_para_pdf = df_sala.copy()
        posicao = 1
        dados_tabela = []

        # Cabeçalho da tabela com os nomes das carteiras (colunas do DataFrame)
        # As colunas já são "Carteira 1", "Carteira 2", etc.
        header = [
            Paragraph(f"<b>{col}</b>", style_normal) for col in df_para_pdf.columns
        ]
        dados_tabela.append(header)

        # Corpo da tabela: itera pelas linhas do DataFrame, que são as Filas da sala.
        for index, row in df_para_pdf.iterrows():
            linha_formatada = []
            for item in row:
                if pd.notna(item) and str(item).strip():
                    texto_celula = f"<b>({posicao:02})</b> {item.replace(' (', '<br/>(')}"
                    linha_formatada.append(Paragraph(texto_celula, style_normal))
                    posicao += 1
                else:
                    linha_formatada.append("")
            dados_tabela.append(linha_formatada)

        elements.append(Paragraph(f"Mapeamento da Turma - {nome_sala}", style_title))
        elements.append(Spacer(1, 0.2 * cm))
        elements.append(
            Paragraph(
                f"Ensalamento: {data_ensalamento} | Data da Aplicação: {data_aplicacao} | Disciplinas: {', '.join(disciplinas)}",
                styles["Normal"],
            )
        )
        elements.append(Spacer(1, 0.5 * cm))
        elements.append(
            Paragraph(
                "MESA DO(A) PROFESSOR(A)",
                ParagraphStyle(name="mesa", fontName="Helvetica-Bold", fontSize=14),
            )
        )
        elements.append(Spacer(1, 0.2 * cm))

        tabela = Table(dados_tabela, repeatRows=1)

        style_tabela = TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
        tabela.setStyle(style_tabela)

        elements.append(tabela)

        # Adiciona PageBreak se não for a última sala
        if i < len(salas_items) - 1:
            elements.append(PageBreak())

    doc.build(elements)

    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()


def gerar_listas_chamada_zip(
    salas_cruas, listas_com_turmas, data_ensalamento, data_aplicacao, disciplinas
):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for nome_sala, sala_matriz in salas_cruas.items():
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                pdf_buffer,
                pagesize=A4,
                topMargin=1 * cm,
                rightMargin=1 * cm,
                leftMargin=1 * cm,
                bottomMargin=1 * cm,
            )
            styles = getSampleStyleSheet()
            estilo_negrito = ParagraphStyle(
                name="Bold", fontName="Helvetica-Bold", fontSize=10
            )
            elements = [
                Paragraph("Colégio Nossa Senhora das Graças - CNSG", styles["Title"]),
                Paragraph(f"Lista de Chamada - {nome_sala}", styles["h2"]),
                Paragraph(f"Data da aplicação: {data_aplicacao}", styles["Normal"]),
                Paragraph(
                    f"Ensalamento realizado em: {data_ensalamento}", styles["Normal"]
                ),
                Paragraph(f"Disciplinas: {', '.join(disciplinas)}", styles["Normal"]), # LINHA CORRIGIDA AQUI
                Paragraph(
                    "Assinatura do(a) aplicador(a): ________________________",
                    styles["Normal"],
                ),
            ]
            header = [
                Paragraph("Nº", estilo_negrito),
                Paragraph("Nome", estilo_negrito),
                Paragraph("Assinatura", estilo_negrito),
            ]
            alunos_ordenados = sorted(
                [
                    adicionar_turma(aluno, listas_com_turmas)
                    for fila in sala_matriz
                    for aluno in fila
                    if aluno and aluno.strip()
                ]
            )
            data_table = [header] + [
                [Paragraph(str(i)), Paragraph(aluno), ""]
                for i, aluno in enumerate(alunos_ordenados, 1)
            ]

            if len(data_table) > 1:
                tabela_alunos = Table(data_table, colWidths=[1 * cm, 12 * cm, 5 * cm])
                tabela_alunos.setStyle(
                    TableStyle(
                        [
                            ("GRID", (0, 0), (-1, -1), 1, colors.black),
                            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                            ("FONTSIZE", (0, 0), (-1, -1), 14),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                        ]
                    )
                )
                elements.append(tabela_alunos)

            doc.build(elements)
            zip_file.writestr(
                f"Lista_Chamada_{nome_sala.replace(' ', '_')}.pdf",
                pdf_buffer.getvalue(),
            )
    return zip_buffer.getvalue()


def gerar_relatorio_pdf(df_salas, data_ensalamento, data_aplicacao, disciplinas):
    relatorio = []
    total_por_turma = {"6º Ano": 0, "7º Ano": 0, "8º Ano": 0, "9º Ano": 0}
    total_geral_alunos = 0
    for nome_sala, df in df_salas.items():
        cont_6ano = df.stack().astype(str).str.contains(r"\(6º Ano\)", regex=True).sum()
        cont_7ano = df.stack().astype(str).str.contains(r"\(7º Ano\)", regex=True).sum()
        cont_8ano = df.stack().astype(str).str.contains(r"\(8º Ano\)", regex=True).sum()
        cont_9ano = df.stack().astype(str).str.contains(r"\(9º Ano\)", regex=True).sum()
        sala_total = cont_6ano + cont_7ano + cont_8ano + cont_9ano
        relatorio.append(
            [nome_sala, sala_total, cont_6ano, cont_7ano, cont_8ano, cont_9ano]
        )
        total_por_turma["6º Ano"] += cont_6ano
        total_por_turma["7º Ano"] += cont_7ano
        total_por_turma["8º Ano"] += cont_8ano
        total_por_turma["9º Ano"] += cont_9ano
        total_geral_alunos += sala_total

    resumo_global = [
        "TOTAL GERAL",
        total_geral_alunos,
        total_por_turma["6º Ano"],
        total_por_turma["7º Ano"],
        total_por_turma["8º Ano"],
        total_por_turma["9º Ano"],
    ]

    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4))
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Relatório de Ensalamento", styles["Title"]))
    elements.append(
        Paragraph(f"Data do Ensalamento: {data_ensalamento}", styles["Normal"])
    )
    elements.append(
        Paragraph(f"Data da Aplicação: {data_aplicacao}", styles["Normal"])
    )
    elements.append(
        Paragraph(f"Disciplinas: {', '.join(disciplinas)}", styles["Normal"])
    )
    elements.append(Paragraph("Resumo por sala:", styles["h2"]))
    dados_tabela = [
        [
            "Sala",
            "Total Alunos",
            "Alunos 6º Ano",
            "Alunos 7º Ano",
            "Alunos 8º Ano",
            "Alunos 9º Ano",
        ]
    ] + relatorio + [resumo_global]
    tabela = Table(dados_tabela)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
                ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ]
        )
    )
    elements.append(tabela)
    doc.build(elements)
    return pdf_buffer.getvalue()


# =====================================================================
#           PÁGINA DE LOGIN
# =====================================================================
def show_login_page():
    """Exibe a página de login otimizada e centralizada."""

    # CSS customizado para layout compacto e centralizado
    st.markdown(
        """
    <style>
        /* Oculta sidebar */
        section[data-testid="stSidebar"] { display: none !important; }
        header, div[data-testid="stToolbar"] { display: none !important; }

        /* Remove padding padrão do container principal */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
            max-width: 1000px !important;
        }
        
        /* Centraliza o conteúdo verticalmente */
        .main .block-container {
            display: flex !important;
            flex-direction: column;
            justify-content: center;
            min-height: 80vh;
        }
        
        /* Estiliza o título */
        .login-title {
            text-align: center;
            color: #1f77b4;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Compacta os inputs */
        .stTextInput > div > div > input {
            padding: 0.5rem 0.75rem !important;
            height: 2.5rem !important;
            font-size: 0.9rem !important;
        }
        
        /* Estiliza o botão */
        .stButton > button {
            background: linear-gradient(90deg, #1f77b4, #ff7f0e);
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: 600;
            padding: 0.6rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #0d5f8a, #cc5f0b);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Reduz espaçamento entre elementos */
        .element-container {
            margin-bottom: 0.5rem !important;
        }
        
        /* Estiliza mensagens de erro */
        .stAlert {
            padding: 0.5rem 1rem !important;
            margin: 0.5rem 0 !important;
        }
        
        /* Compacta o formulário */
        .stForm {
            border: 1px solid #e0e0e0;
            border-radius: 12px;
            padding: 1.5rem;
            background: #fafafa;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        /* Centraliza caption */
        .caption-text {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            margin-top: 1rem;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    def password_entered():
        user = st.session_state.get("username", "").lower()
        pwd  = st.session_state.get("password", "")
        if user == "cnsg" and pwd == "123456":
            st.session_state["password_correct"] = True
            st.session_state.pop("username", None)
            st.session_state.pop("password", None)
        else:
            st.session_state["password_correct"] = False

    # Layout centralizado: colunas [1,3,1]
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        # Título
        st.markdown(
            '<h1 class="login-title">CNSG - Ensalamento</h1>',
            unsafe_allow_html=True,
        )

        # Formulário compacto
        with st.form("login_form", clear_on_submit=True):
            st.text_input(
                "👤 Usuário",
                key="username",
                placeholder="Digite seu usuário",
                help="Use: cnsg",
            )
            st.text_input(
                "🔒 Senha",
                type="password",
                key="password",
                placeholder="Digite sua senha",
                help="Use: 123456",
            )
            submitted = st.form_submit_button("🚀 Entrar", use_container_width=True)
            if submitted:
                password_entered()
                st.rerun()

        # Mensagem de erro
        if st.session_state.get("password_correct") is False:
            st.error("⚠️ Credenciais inválidas. Tente novamente.")

        # Rodapé compacto
        st.markdown(
            '<p class="caption-text">Desenvolvido por Flávio Carvalho - Analista de Dados</p>',
            unsafe_allow_html=True,
        )
















# =====================================================================
#           PÁGINA PRINCIPAL
# =====================================================================
def show_main_page():
    st.markdown(
        """
        <style>
            /* Garante que a sidebar esteja visível na página principal */
            div[data-testid="stSidebar"] {
                display: block;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("🎓 CNSG - Ensalamento de Alunos")
    st.write(
        "Prezado Paulo, esta aplicação gera a distribuição de alunos em salas, evitando que estudantes da mesma turma sentem-se próximos, e cria os documentos necessários para a aplicação de provas."
    )

    with st.sidebar:
        st.image(
            "https://placehold.co/250x100/1f77b4/ffffff?text=CNSG&font=roboto",
            use_container_width=True,
        )
        st.header("Parâmetros do Ensalamento")

        data_aplicacao_widget = st.date_input("Data da Aplicação:", datetime.now())

        disciplinas_opts = [
            "Geografia",
            "Matemática",
            "Literatura",
            "Sociologia",
            "Biologia",
            "Português",
            "Arte",
            "Filosofia",
            "Oficina de Texto",
            "Química",
            "História",
            "Ciências",
            "Inglês",
            "Física",
            "Redação",
        ]
        disciplinas_selecionadas = st.multiselect(
            "Selecione as Disciplinas:",
            options=disciplinas_opts,
            default=disciplinas_opts[0],
        )

        st.markdown("---")

        if st.button("🚀 Gerar Ensalamento", type="primary", use_container_width=True):
            with st.spinner("Gerando ensalamento..."):
                student_lists_raw = get_student_lists()
                student_lists = {
                    k: remover_acentos(v) for k, v in student_lists_raw.items()
                }
                for slist in student_lists.values():
                    random.shuffle(slist)

                alunos_intercalados = intercalar_listas(
                    student_lists["list_6ANO"],
                    student_lists["list_7ANO"],
                    student_lists["list_8ANO"],
                    student_lists["list_9ANO"],
                )

                listas_com_turmas = [
                    (student_lists["list_6ANO"], "6º Ano"),
                    (student_lists["list_7ANO"], "7º Ano"),
                    (student_lists["list_8ANO"], "8º Ano"),
                    (student_lists["list_9ANO"], "9º Ano"),
                ]

                salas_cruas = {}
                alunos_restantes = list(alunos_intercalados)
                for nome_sala, (filas, lugares) in filas_lugares.items():
                    capacidade = filas * lugares
                    alunos_nesta_sala = alunos_restantes[:capacidade]
                    alunos_restantes = alunos_restantes[capacidade:]
                    salas_cruas[
                        nome_sala
                    ] = distribuir_alunos_sem_mesma_turma_ao_lado_ou_acima(
                        alunos_nesta_sala, filas, lugares, listas_com_turmas
                    )

                df_salas = {
                    nome_sala: sala_para_dataframe(sala_matriz, listas_com_turmas)
                    for nome_sala, sala_matriz in salas_cruas.items()
                }

                st.session_state.update(
                    {
                        "ensalamento_gerado": True,
                        "df_salas": df_salas,
                        "salas_cruas": salas_cruas,
                        "listas_com_turmas": listas_com_turmas,
                        "data_aplicacao": data_aplicacao_widget.strftime("%d/%m/%Y"),
                        "disciplinas": disciplinas_selecionadas,
                    }
                )
                st.success("Ensalamento gerado com sucesso!")

        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state["password_correct"] = False
            st.session_state.pop("ensalamento_gerado", None)
            st.rerun()

    if st.session_state.get("ensalamento_gerado", False):
        st.header("Resultados do Ensalamento")
        st.info("Utilize os botões abaixo para baixar os documentos gerados.")

        df_salas = st.session_state.df_salas
        salas_cruas = st.session_state.salas_cruas
        listas_com_turmas = st.session_state.listas_com_turmas
        data_aplicacao = st.session_state.data_aplicacao
        disciplinas = st.session_state.disciplinas
        data_ensalamento = datetime.now().strftime("%d/%m/%Y")

        st.subheader("⬇️ Downloads")
        col1, col2, col3 = st.columns(3)

        with col1:
            pdf_mapa_bytes = gerar_mapa_salas_pdf(
                df_salas, data_ensalamento, data_aplicacao, disciplinas
            )
            if pdf_mapa_bytes:
                st.download_button(
                    "📄 Baixar Mapa das Salas (PDF)",
                    pdf_mapa_bytes,
                    "ensalamento_mapa_salas.pdf",
                    "application/pdf",
                    use_container_width=True,
                )

        with col2:
            zip_chamada_bytes = gerar_listas_chamada_zip(
                salas_cruas,
                listas_com_turmas,
                data_ensalamento,
                data_aplicacao,
                disciplinas,
            )
            st.download_button(
                "📋 Baixar Listas de Chamada (ZIP)",
                zip_chamada_bytes,
                "listas_de_chamada.zip",
                "application/zip",
                use_container_width=True,
            )

        with col3:
            pdf_relatorio_bytes = gerar_relatorio_pdf(
                df_salas, data_ensalamento, data_aplicacao, disciplinas
            )
            st.download_button(
                "📊 Baixar Relatório Geral (PDF)",
                pdf_relatorio_bytes,
                "relatorio_geral_ensalamento.pdf",
                "application/pdf",
                use_container_width=True,
            )

        st.markdown("---")

        st.subheader("Visualização do Ensalamento por Sala")
        for nome_sala, df_sala in df_salas.items():
            with st.expander(f"Visualizar {nome_sala}"):
                st.dataframe(df_sala)
    else:
        st.info(
            "Preencha os parâmetros na barra lateral e clique em 'Gerar Ensalamento' para começar."
        )


# =====================================================================
#           EXECUÇÃO PRINCIPAL
# =====================================================================

if not st.session_state.get("password_correct", False):
    show_login_page()
else:
    show_main_page()