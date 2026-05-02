import marimo

__generated_with = "0.23.4"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell
def _(subprocess):
    #! ls /kaggle/input/sistema-de-informaes-hospitalares-sus
    subprocess.call(['ls', '/kaggle/input/sistema-de-informaes-hospitalares-sus'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Etapa 1: Coleta de dados
    """)
    return


@app.cell
def _():
    import pandas as pd
    import plotly.express as px
    # Configura a biblioteca pandas para exibir todos os itens da sequência do base de dados
    pd.options.display.max_seq_items = 113

    # Carrega a base de dados
    df = pd.read_csv('datasets/RD202401.csv', sep=';', low_memory=False)
    df_cnes = pd.read_csv('datasets/cnes_estabelecimentos.csv', sep=';', encoding='latin1', low_memory=False)
    df_municipios = pd.read_csv('../datasets/municipios.csv')
    df
    return df, df_cnes, df_municipios, pd, px


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Etapa 2: Limpeza e Preparação dos dados
    """)
    return


@app.cell
def _(df):
    # Mostra as colunas em sequência da base de dados
    df.columns
    return


@app.cell
def _(df):
    # Delimitar as colunas de interesse em recorte da base de dados
    df_1 = df[['UF_ZI', 'ANO_CMPT', 'MES_CMPT', 'ESPEC', 'N_AIH', 'IDENT', 'CEP', 'MUNIC_RES', 'NASC', 'SEXO', 'UTI_MES_TO', 'MARCA_UTI', 'UTI_INT_TO', 'DIAR_ACOM', 'QT_DIARIAS', 'PROC_SOLIC', 'PROC_REA', 'VAL_SH', 'VAL_SP', 'VAL_TOT', 'VAL_UTI', 'US_TOT', 'DT_INTER', 'DT_SAIDA', 'DIAG_PRINC', 'DIAG_SECUN', 'COBRANCA', 'NATUREZA', 'NAT_JUR', 'GESTAO', 'IND_VDRL', 'MUNIC_MOV', 'COD_IDADE', 'IDADE', 'DIAS_PERM', 'MORTE', 'NACIONAL', 'CAR_INT', 'HOMONIMO', 'NUM_FILHOS', 'INSTRU', 'CID_NOTIF', 'CONTRACEP1', 'CONTRACEP2', 'GESTRISCO', 'INSC_PN', 'SEQ_AIH5', 'CBOR', 'CNAER', 'VINCPREV', 'GESTOR_COD', 'GESTOR_TP', 'GESTOR_DT', 'CNES', 'INFEHOSP', 'CID_ASSO', 'CID_MORTE', 'COMPLEX', 'FINANC', 'FAEC_TP', 'REGCT', 'RACA_COR', 'ETNIA', 'VAL_SH_FED', 'VAL_SP_FED', 'VAL_SH_GES', 'VAL_SP_GES', 'VAL_UCI', 'MARCA_UCI']].copy()
    return (df_1,)


@app.cell
def _(df_1):
    # Gera um resumo das informações
    df_1.info()
    return


@app.cell
def _(df_1):
    # Transformar variável categórica
    df_1['DIAG_PRINC'] = df_1['DIAG_PRINC'].astype(str)
    df_1['CID_NOTIF'] = df_1['CID_NOTIF'].astype(str)
    return


@app.cell
def _(df_1):
    df_1['UF_ZI'] = df_1['UF_ZI'].astype(str)
    return


@app.cell
def _(df_1):
    # Verifica se há variáveis com valores nulos
    df_1.isnull().sum()
    return


@app.cell
def _(df_1):
    # Pré-processamento
    # Filtrar para a Bahia (código 29)
    df_1['UF_ZI'] = df_1['UF_ZI'].astype(str)
    df_bahia = df_1[df_1['UF_ZI'].str.startswith('29')].copy()
    return (df_bahia,)


@app.cell
def _(df_bahia, pd):
    # Converter data de internação para datetime (formato 'aaaammdd')
    df_bahia['DT_INTER'] = pd.to_datetime(df_bahia['DT_INTER'], format='%Y%m%d', errors='coerce')
    df_bahia['DT_SAIDA'] = pd.to_datetime(df_bahia['DT_SAIDA'], format='%Y%m%d', errors='coerce')
    df_bahia_1 = df_bahia.dropna(subset=['DT_INTER'])  # Remover datas inválidas se houver
    df_bahia_1 = df_bahia_1.dropna(subset=['DT_SAIDA'])
    return (df_bahia_1,)


@app.cell
def _(df_municipios):
    # Convertendo o código do município para string e pegando apenas os 6 primeiros caracteres
    # e filtrando para o estado da Bahia
    df_municipios['Codigo'] = df_municipios['Codigo'].astype(str).str[:6]
    df_municipios_1 = df_municipios[df_municipios['Codigo'].str.startswith('29')]
    df_municipios_1
    return (df_municipios_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Etapa 3: Análise Exploratória
    ## Pergunta 1: Quais cidades tem o maior numero de internações?
    """)
    return


@app.cell
def _(df_bahia_1, df_municipios_1, pd, px):
    # Contagem das 10 cidades com mais internações
    contagem_internacoes = df_bahia_1['MUNIC_MOV'].value_counts().nlargest(10).reset_index()
    contagem_internacoes['MUNIC_MOV'] = contagem_internacoes['MUNIC_MOV'].astype(str)
    contagem_internacoes.columns = ['MUNIC_MOV', 'INTER']
    top_municipios = pd.merge(contagem_internacoes, df_municipios_1, left_on='MUNIC_MOV', right_on='Codigo')
    # Merge com o dataframe de municípios
    top_municipios['Municipios'] = top_municipios['Nome'] + ' - ' + top_municipios['Uf']
    fig = px.bar(top_municipios, x='INTER', y='Municipios', orientation='h', color='Municipios', color_discrete_sequence=px.colors.sequential.Viridis, title='Top 10 Municípios com maior número de internações', labels={'INTER': 'Total de Internações', 'Municipios': 'Município de Estabelecimento'})
    fig.update_layout(showlegend=False, xaxis_title='Total de Internações', yaxis_title='Município de Estabelecimento', height=600)
    # Criando coluna com nome formatado
    # Gráfico interativo com Plotly
    # Ajustes visuais
    fig.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 2: Qual é a distribuição de internações por sexo dos pacientes na Bahia?
    """)
    return


@app.cell
def _(df_bahia_1, px):
    # Contar internações por sexo
    sexo_counts = df_bahia_1['SEXO'].value_counts().reset_index()
    sexo_counts.columns = ['SEXO', 'QTD_INTERNAÇÕES']
    df_bahia_1.loc[df_bahia_1['SEXO'] == 3, 'SEXO'] = 2
    # Mapeamento e limpeza: 1 = Masculino, 2 = Feminino
    sexo_counts['SEXO'] = sexo_counts['SEXO'].map({1: 'Masculino', 2: 'Feminino'})  # mantém sua lógica original
    fig_1 = px.bar(sexo_counts, x='SEXO', y='QTD_INTERNAÇÕES', text='QTD_INTERNAÇÕES', color='SEXO', color_discrete_sequence=px.colors.qualitative.Pastel, title='Distribuição de internações por sexo - Bahia', labels={'SEXO': 'Sexo do paciente', 'QTD_INTERNAÇÕES': 'Número de internações'})
    fig_1.update_traces(texttemplate='%{text}', textposition='outside')
    # Gráfico interativo
    fig_1.update_layout(showlegend=False, xaxis_title='Sexo do paciente', yaxis_title='Número de internações', height=400)
    # Ajustes visuais
    fig_1.show()  # paleta similar ao seaborn pastel
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 3: Qual é a faixa etária mais frequente entre os pacientes internados em hospitais baianos?
    """)
    return


@app.cell
def _(df_bahia_1, pd, px):
    # Criar faixas etárias
    bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 120]
    labels = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70–79', '80–89', '90–99', '100+']
    df_bahia_1['faixa_etaria'] = pd.cut(df_bahia_1['IDADE'], bins=bins, labels=labels, right=True)
    faixa_counts = df_bahia_1['faixa_etaria'].value_counts().sort_index().reset_index()
    # Contar internações por faixa etária
    faixa_counts.columns = ['Faixa Etária', 'Internações']
    fig_2 = px.bar(faixa_counts, x='Faixa Etária', y='Internações', text='Internações', color='Faixa Etária', color_discrete_sequence=px.colors.sequential.Tealgrn, title='Distribuição de internações por faixa etária - Bahia', labels={'Faixa Etária': 'Faixa Etária', 'Internações': 'Número de internações'})
    fig_2.update_traces(texttemplate='%{text}', textposition='outside')
    # Gráfico interativo
    fig_2.update_layout(showlegend=False, xaxis_title='Faixa Etária', yaxis_title='Número de internações', height=500, bargap=0.3)
    # Ajustes visuais
    fig_2.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 4: Qual é a idade média dos pacientes internados na Bahia por especialidade de leito (ESPEC)?
    """)
    return


@app.cell
def _(df_bahia_1, pd, px):
    # Dicionário de mapeamento para ESPEC
    map_espec = {1: 'Cirúrgico', 2: 'Obstétricos', 3: 'Clínico', 4: 'Crônicos', 5: 'Psiquiatria', 6: 'Pneumologia Sanitária (Tisiologia)', 7: 'Pediátricos', 8: 'Reabilitação', 9: 'Leito Dia / Cirúrgicos', 10: 'Leito Dia / Aids', 11: 'Leito Dia / Fibrose Cística', 12: 'Leito Dia / Intercorrência Pós-Transplante', 13: 'Leito Dia / Geriatria', 14: 'Leito Dia / Saúde Mental', 51: 'UTI II Adulto COVID 19', 52: 'UTI II Pediátrica COVID 19', 64: 'Unidade Intermediária', 65: 'Unidade Intermediária Neonatal', 74: 'UTI I', 75: 'UTI Adulto II', 76: 'UTI Adulto III', 77: 'UTI Infantil I', 78: 'UTI Infantil II', 79: 'UTI Infantil III', 80: 'UTI Neonatal I', 81: 'UTI Neonatal II', 82: 'UTI Neonatal III', 83: 'UTI Queimados', 84: 'Acolhimento Noturno', 85: 'UTI Coronariana-UCO tipo II', 86: 'UTI Coronariana-UCO tipo III', 87: 'Saúde Mental (Clínico)', 88: 'Queimado Adulto (Clínico)', 89: 'Queimado Pediátrico (Clínico)', 90: 'Queimado Adulto (Cirúrgico)', 91: 'Queimado Pediátrico (Cirúrgico)', 92: 'UCI Neonatal Convencional', 93: 'UCI Neonatal Canguru', 94: 'UCI Pediátrico', 95: 'UCI Adulto', 96: 'Suporte Ventilatório Pulmonar COVID-19'}
    df_bahia_1['Especialidade_Desc'] = df_bahia_1['ESPEC'].map(map_espec)
    df_bahia_1['IDADE'] = pd.to_numeric(df_bahia_1['IDADE'], errors='coerce')
    idade_media = df_bahia_1.groupby('Especialidade_Desc')['IDADE'].mean().reset_index().sort_values(by='IDADE', ascending=False).head(15)
    fig_3 = px.bar(idade_media, x='IDADE', y='Especialidade_Desc', orientation='h', text='IDADE', color='IDADE', color_continuous_scale='Viridis', title='Idade média dos pacientes internados por especialidade de leito - Bahia (Top 15)', labels={'IDADE': 'Idade Média (anos)', 'Especialidade_Desc': 'Especialidade do Leito'})
    fig_3.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_3.update_layout(coloraxis_showscale=False, xaxis_title='Idade Média (anos)', yaxis_title='Especialidade do Leito', height=600, bargap=0.3)
    # Mapear as especialidades
    # Garantir que IDADE é numérica
    # Calcular idade média por especialidade
    # Gráfico interativo (barras horizontais)
    # Ajustes visuais
    fig_3.show()  # equivalente à paleta seaborn viridis  # oculta a barra de cores lateral
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 5: Qual é o percentual de óbitos entre as internações na Bahia?
    """)
    return


@app.cell
def _(df_bahia_1):
    total_internacoes = len(df_bahia_1)
    total_obitos = df_bahia_1[df_bahia_1['MORTE'] == 1].shape[0]
    percentual_obitos = total_obitos / total_internacoes * 100
    print(f'Total de internações na Bahia: {total_internacoes}')
    print(f'Total de óbitos na Bahia: {total_obitos}')
    print(f'Percentual de óbitos: {percentual_obitos:.2f}%')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 6: Qual é a proporção de gestantes de risco entre as internações obstétricas realizadas na Bahia?
    """)
    return


@app.cell
def _(df_bahia_1):
    # 1. Filtrar as internações obstétricas (ESPEC == 2 - Obstétricos) na Bahia
    # O valor '2' é obtido do mapeamento para ESPEC na Pergunta 4, onde 2 = 'Obstétricos'
    df_obstetricas_bahia = df_bahia_1[df_bahia_1['ESPEC'] == 2].copy()
    total_obstetricas = len(df_obstetricas_bahia)
    # 2. Contar o total de internações obstétricas
    total_gestrisco = df_obstetricas_bahia[df_obstetricas_bahia['GESTRISCO'] == 1].shape[0]
    if total_obstetricas > 0:
    # 3. Contar as gestantes de risco (GESTRISCO == 1) entre as obstétricas
    # O campo 'GESTRISCO' (Gestante de Risco) é um indicador com 1 (Sim) ou 0 (Não/Ausente).
    # A coluna GESTRISCO no df_bahia é do tipo int64.
        proporcao_gestrisco = total_gestrisco / total_obstetricas * 100
    else:
    # 4. Calcular o percentual
        proporcao_gestrisco = 0
    print(f'Total de internações obstétricas na Bahia: {total_obstetricas}')
    print(f'Total de internações obstétricas de Gestantes de Risco (GESTRISCO=1): {total_gestrisco}')
    # 5. Imprimir o resultado
    print(f'Proporção de Gestantes de Risco entre internações obstétricas: {proporcao_gestrisco:.2f}%')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 7: Qual é a distribuição de pacientes por raça/cor nos hospitais da Bahia?
    """)
    return


@app.cell
def _(df_bahia_1, px):
    map_raca_cor = {1: 'Branca', 2: 'Preta', 3: 'Parda', 4: 'Amarela', 5: 'Indígena', 99: 'Sem informação'}
    raca_counts = df_bahia_1['RACA_COR'].value_counts().reset_index()
    raca_counts.columns = ['RACA_COR_COD', 'Total_Internacoes']
    # Dicionário de mapeamento para Raça/Cor
    raca_counts['Raça/Cor'] = raca_counts['RACA_COR_COD'].map(map_raca_cor)
    total_internacoes_bahia = raca_counts['Total_Internacoes'].sum()
    raca_counts['Percentual'] = raca_counts['Total_Internacoes'] / total_internacoes_bahia * 100
    raca_counts = raca_counts.sort_values(by='Total_Internacoes', ascending=False)
    fig_4 = px.bar(raca_counts, x='Percentual', y='Raça/Cor', orientation='h', text=raca_counts['Percentual'].map(lambda x: f'{x:.1f}%'), color='Raça/Cor', color_discrete_sequence=px.colors.qualitative.Set2, title='Distribuição de Internações por Raça/Cor - Bahia', labels={'Percentual': 'Percentual de Internações (%)', 'Raça/Cor': 'Raça/Cor'})
    fig_4.update_traces(textposition='outside', hovertemplate='<b>%{y}</b><br>%{x:.2f}% das internações')
    fig_4.update_layout(showlegend=False, xaxis_title='Percentual de Internações (%)', yaxis_title='Raça/Cor', height=500, bargap=0.3)
    # 1. Contar a frequência de cada código de Raça/Cor
    # 2. Adicionar a descrição da Raça/Cor
    # 3. Calcular o percentual de cada categoria
    # 4. Ordenar por frequência
    # 5. Gráfico interativo com Plotly
    # Ajustes visuais
    fig_4.show()  # mesma paleta do seaborn 'Set2'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 8: Qual é o tempo médio de permanência por faixa etária no estado da Bahia?
    """)
    return


@app.cell
def _(df_bahia_1, pd, px):
    # Mapeamento e cálculo da faixa etária
    bins_1 = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 120]
    labels_1 = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70–79', '80–89', '90–99', '100+']
    df_bahia_1['IDADE_INT'] = df_bahia_1['IDADE'].fillna(0).astype(int)
    # Preenche NaNs e cria coluna de faixa etária
    df_bahia_1['faixa_etaria'] = pd.cut(df_bahia_1['IDADE_INT'], bins=bins_1, labels=labels_1, right=True, ordered=False)
    df_bahia_1.dropna(subset=['DIAS_PERM', 'faixa_etaria'], inplace=True)
    tempo_medio_permanencia = df_bahia_1.groupby('faixa_etaria', observed=True)['DIAS_PERM'].mean().reset_index().sort_values(by='DIAS_PERM', ascending=False)
    # Tratar NaNs na coluna DIAS_PERM e faixa_etaria
    tempo_medio_permanencia.columns = ['Faixa_Etaria', 'Tempo_Medio_Permanencia_(dias)']
    fig_5 = px.bar(tempo_medio_permanencia, x='Tempo_Medio_Permanencia_(dias)', y='Faixa_Etaria', orientation='h', text=tempo_medio_permanencia['Tempo_Medio_Permanencia_(dias)'].map(lambda x: f'{x:.1f}'), color='Tempo_Medio_Permanencia_(dias)', color_continuous_scale='Magma', title='Tempo médio de permanência por faixa etária - Bahia', labels={'Tempo_Medio_Permanencia_(dias)': 'Tempo médio de permanência (dias)', 'Faixa_Etaria': 'Faixa Etária'})
    # Calcular tempo médio de permanência (DIAS_PERM) por faixa etária
    fig_5.update_traces(textposition='outside', hovertemplate='<b>%{y}</b><br>Tempo médio: %{x:.1f} dias')
    fig_5.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Tempo médio de permanência (dias)', yaxis_title='Faixa Etária', height=600, bargap=0.3)
    # Gráfico interativo
    # Ajustes visuais
    fig_5.show()  # equivalente ao seaborn 'magma'  # remove a barra de cor lateral
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 9: Há diferenças no tempo de permanência entre homens e mulheres internados na Bahia?
    """)
    return


@app.cell
def _(df_bahia_1, px):
    # Remover NaNs nas colunas essenciais
    df_bahia_1.dropna(subset=['DIAS_PERM', 'SEXO'], inplace=True)
    map_sexo = {1: 'Masculino', 2: 'Feminino'}
    # Mapeamento para rótulos
    tempo_medio_sexo = df_bahia_1.groupby('SEXO')['DIAS_PERM'].mean().reset_index().sort_values(by='DIAS_PERM', ascending=False)
    tempo_medio_sexo.columns = ['SEXO_COD', 'Tempo_Medio_Permanencia_(dias)']
    # Calcular o tempo médio de permanência por sexo
    tempo_medio_sexo['Sexo'] = tempo_medio_sexo['SEXO_COD'].map(map_sexo)
    fig_6 = px.bar(tempo_medio_sexo, x='Sexo', y='Tempo_Medio_Permanencia_(dias)', text=tempo_medio_sexo['Tempo_Medio_Permanencia_(dias)'].map(lambda x: f'{x:.2f}'), color='Sexo', color_discrete_sequence=px.colors.qualitative.Set1, title='Tempo médio de permanência por sexo - Bahia', labels={'Sexo': 'Sexo', 'Tempo_Medio_Permanencia_(dias)': 'Tempo médio de permanência (dias)'})
    fig_6.update_traces(textposition='outside', hovertemplate='<b>%{x}</b><br>Tempo médio: %{y:.2f} dias')
    fig_6.update_layout(showlegend=False, xaxis_title='Sexo', yaxis_title='Tempo médio de permanência (dias)', height=450, bargap=0.3)
    # Gráfico interativo
    # Ajustes visuais
    fig_6.show()  # equivalente à paleta Seaborn 'Set1'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 10: Qual é a proporção de internações com infecção hospitalar nos hospitais baianos?
    """)
    return


@app.cell
def _(df_bahia_1, px):
    # --- Limpeza e mapeamento ---
    map_cid_capitulo = {'A': 'I. Algumas doenças infecciosas e parasitárias', 'B': 'I. Algumas doenças infecciosas e parasitárias', 'C': 'II. Neoplasias (tumores)', 'D': 'III. Doenças sangue órgãos hemat e transt imunitár', 'E': 'IV. Doenças endócrinas nutricionais e metabólicas', 'F': 'V. Transtornos mentais e comportamentais', 'G': 'VI. Doenças do sistema nervoso', 'H': 'VII/VIII. Doenças do olho/ouvido e anexos', 'I': 'IX. Doenças do aparelho circulatório', 'J': 'X. Doenças do aparelho respiratório', 'K': 'XI. Doenças do aparelho digestivo', 'L': 'XII. Doenças da pele e do tecido subcutâneo', 'M': 'XIII. Doenças sist osteomuscular e tec conjuntivo', 'N': 'XIV. Doenças do aparelho geniturinário', 'O': 'XV. Gravidez parto e puerpério', 'P': 'XVI. Algumas afec originadas no período perinatal', 'Q': 'XVII. Malf cong deformid e anomalias cromossômicas', 'R': 'XVIII. Sint sinais e achad anorm ex clín e laborat', 'S': 'XIX. Lesões enven e alg out conseq causas externas', 'T': 'XIX. Lesões enven e alg out conseq causas externas', 'V': 'XX. Causas externas de morbidade e mortalidade', 'W': 'XX. Causas externas de morbidade e mortalidade', 'X': 'XX. Causas externas de morbidade e mortalidade', 'Y': 'XX. Causas externas de morbidade e mortalidade', 'Z': 'XXI. Contatos com serviços de saúde', 'U': 'XXII. Códigos para propósitos especiais'}
    df_bahia_2 = df_bahia_1.dropna(subset=['DIAG_PRINC'])
    df_bahia_2 = df_bahia_2[df_bahia_2['DIAG_PRINC'].str.len() >= 1].copy()
    df_bahia_2['CAPITULO_CID'] = df_bahia_2['DIAG_PRINC'].str[0].str.upper()
    df_bahia_2['DESCRICAO_CAPITULO'] = df_bahia_2['CAPITULO_CID'].map(map_cid_capitulo)
    frequencia_capitulos = df_bahia_2['DESCRICAO_CAPITULO'].value_counts().reset_index()
    frequencia_capitulos.columns = ['Capitulo_CID', 'Frequencia']
    frequencia_capitulos['Percentual'] = frequencia_capitulos['Frequencia'] / frequencia_capitulos['Frequencia'].sum() * 100
    frequencia_capitulos = frequencia_capitulos.sort_values(by='Frequencia', ascending=False)
    fig_7 = px.bar(frequencia_capitulos, x='Percentual', y='Capitulo_CID', orientation='h', color='Capitulo_CID', color_discrete_sequence=px.colors.sequential.Sunset, text=frequencia_capitulos['Percentual'].map(lambda x: f'{x:.1f}%'), title='Distribuição das Internações por Capítulo da CID-10 - Bahia', labels={'Percentual': 'Percentual de Internações (%)', 'Capitulo_CID': 'Capítulo da CID-10'})
    fig_7.update_traces(textposition='outside', hovertemplate='<b>%{y}</b><br>Frequência: %{customdata[0]}<br>Percentual: %{x:.1f}%', customdata=frequencia_capitulos[['Frequencia']])
    fig_7.update_layout(showlegend=False, xaxis_title='Percentual de Internações (%)', yaxis_title='Capítulo da CID-10', height=700, margin=dict(l=20, r=20, t=60, b=40))
    # Garantir colunas válidas
    # Extrair letra inicial (capítulo)
    # Contagem e percentual
    # Ordenar por frequência
    # --- Gráfico interativo ---
    # Ajustes de layout
    fig_7.show()  # cores suaves e legíveis
    return (df_bahia_2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 11: Quais hospitais da Bahia registraram o maior número de internações?
    """)
    return


@app.cell
def _(df_bahia_2, df_cnes, px):
    # Manter apenas as colunas relevantes
    df_cnes_1 = df_cnes[['CO_CNES', 'NO_FANTASIA']].copy()
    df_cnes_1['CO_CNES'] = df_cnes_1['CO_CNES'].astype(str).str.strip()
    df_cnes_1['NO_FANTASIA'] = df_cnes_1['NO_FANTASIA'].astype(str).str.strip()
    df_bahia_3 = df_bahia_2.dropna(subset=['CNES']).copy()
    # === 2️⃣ Preparar o DataFrame de internações ===
    df_bahia_3['CNES'] = df_bahia_3['CNES'].astype(str).str.strip()
    for col in ['CO_CNES', 'NO_FANTASIA']:
        if col in df_bahia_3.columns:
    # 🔒 Remover colunas duplicadas se existirem
            df_bahia_3.drop(columns=col, inplace=True)
    df_bahia_3 = df_bahia_3.merge(df_cnes_1[['CO_CNES', 'NO_FANTASIA']], left_on='CNES', right_on='CO_CNES', how='left')
    frequencia_hospitais = df_bahia_3.groupby(['CNES', 'NO_FANTASIA']).size().reset_index(name='Total_Internacoes').sort_values(by='Total_Internacoes', ascending=False)
    top_10_hospitais = frequencia_hospitais.head(10)
    # === 3️⃣ Fazer o merge de forma segura ===
    print('Top 10 Hospitais da Bahia por Número de Internações:')
    print(top_10_hospitais[['NO_FANTASIA', 'Total_Internacoes']].to_markdown(index=False))
    fig_8 = px.bar(top_10_hospitais, x='Total_Internacoes', y='NO_FANTASIA', orientation='h', color='Total_Internacoes', color_continuous_scale='Blues', text='Total_Internacoes', title='Top 10 Hospitais por Número de Internações - Bahia', labels={'Total_Internacoes': 'Total de Internações', 'NO_FANTASIA': 'Hospital (Nome Fantasia)'})
    fig_8.update_traces(textposition='outside', hovertemplate='<b>Hospital:</b> %{y}<br><b>Internações:</b> %{x}<extra></extra>')
    fig_8.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Total de Internações', yaxis_title='Hospital', height=600, margin=dict(l=150, r=20, t=60, b=40))
    # === 4️⃣ Contagem de internações por hospital ===
    # Selecionar top 10
    # === 5️⃣ Exibir tabela ===
    # === 6️⃣ Gráfico interativo ===
    # === 7️⃣ Ajustes visuais ===
    fig_8.show()
    return df_bahia_3, df_cnes_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 12: Qual é o tempo médio de permanência por hospital baiano?
    """)
    return


@app.cell
def _(df_bahia_3, df_cnes_1, px):
    # Manter apenas as colunas necessárias
    df_cnes_2 = df_cnes_1[['CO_CNES', 'NO_FANTASIA']].copy()
    df_cnes_2['CO_CNES'] = df_cnes_2['CO_CNES'].astype(str).str.strip()
    df_cnes_2['NO_FANTASIA'] = df_cnes_2['NO_FANTASIA'].astype(str).str.strip()
    df_bahia_4 = df_bahia_3.dropna(subset=['CNES', 'DIAS_PERM']).copy()
    # === 2️⃣ Preparar o DataFrame de internações ===
    df_bahia_4['CNES'] = df_bahia_4['CNES'].astype(str).str.strip()
    for col_1 in ['CO_CNES', 'NO_FANTASIA']:
        if col_1 in df_bahia_4.columns:
    # Garantir que não há colunas conflitantes antes do merge
            df_bahia_4.drop(columns=col_1, inplace=True)
    df_bahia_4 = df_bahia_4.merge(df_cnes_2[['CO_CNES', 'NO_FANTASIA']], left_on='CNES', right_on='CO_CNES', how='left')
    faltando_nome = df_bahia_4['NO_FANTASIA'].isna().sum()
    print(f'Hospitais sem nome encontrado no CNES: {faltando_nome}')
    # === 3️⃣ Fazer o merge com CNES ===
    tempo_medio_hospitais = df_bahia_4.groupby(['CNES', 'NO_FANTASIA'], dropna=False)['DIAS_PERM'].mean().reset_index().sort_values(by='DIAS_PERM', ascending=False)
    tempo_medio_hospitais.columns = ['CNES', 'NO_FANTASIA', 'Tempo_Medio_Permanencia_(dias)']
    tempo_medio_hospitais['NO_FANTASIA'] = tempo_medio_hospitais['NO_FANTASIA'].fillna(tempo_medio_hospitais['CNES'])
    top_10_tempo_medio = tempo_medio_hospitais.head(10)
    print('\nTop 10 Hospitais da Bahia por Tempo Médio de Permanência:')
    print(top_10_tempo_medio[['NO_FANTASIA', 'Tempo_Medio_Permanencia_(dias)']].to_markdown(index=False, floatfmt='.2f'))
    fig_9 = px.bar(top_10_tempo_medio, x='Tempo_Medio_Permanencia_(dias)', y='NO_FANTASIA', orientation='h', color='Tempo_Medio_Permanencia_(dias)', color_continuous_scale='Reds', text=top_10_tempo_medio['Tempo_Medio_Permanencia_(dias)'].map(lambda x: f'{x:.1f}'), title='Top 10 Hospitais por Tempo Médio de Permanência - Bahia', labels={'Tempo_Medio_Permanencia_(dias)': 'Tempo Médio de Permanência (dias)', 'NO_FANTASIA': 'Hospital (Nome Fantasia)'})
    # 🚨 Verificação: mostrar se há hospitais sem nome encontrado
    fig_9.update_traces(textposition='outside', hovertemplate='<b>Hospital:</b> %{y}<br><b>Tempo Médio:</b> %{x:.2f} dias<extra></extra>')
    fig_9.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Tempo Médio de Permanência (dias)', yaxis_title='Hospital', height=600, margin=dict(l=150, r=20, t=60, b=40))
    # === 4️⃣ Calcular tempo médio de permanência por hospital ===
    # Substituir nomes ausentes pelo próprio código CNES
    # Selecionar top 10
    # === 5️⃣ Exibir tabela no console ===
    # === 6️⃣ Gráfico interativo ===
    # === 7️⃣ Layout ===
    fig_9.show()
    return df_bahia_4, df_cnes_2


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 13: Quais hospitais da Bahia têm maior taxa de mortalidade hospitalar?
    """)
    return


@app.cell
def _(df_bahia_4, df_cnes_2, pd, px):
    df_cnes_3 = df_cnes_2[['CO_CNES', 'NO_FANTASIA']].copy()
    df_cnes_3['CO_CNES'] = df_cnes_3['CO_CNES'].astype(str).str.strip()
    df_cnes_3['NO_FANTASIA'] = df_cnes_3['NO_FANTASIA'].astype(str).str.strip()
    df_bahia_5 = df_bahia_4.copy()
    # === 2️⃣ Limpeza do DataFrame da Bahia ===
    df_bahia_5['CNES'] = df_bahia_5['CNES'].astype(str).str.strip()
    df_bahia_5['MORTE'] = pd.to_numeric(df_bahia_5['MORTE'], errors='coerce')
    for col_2 in ['CO_CNES', 'NO_FANTASIA']:
        if col_2 in df_bahia_5.columns:
    # Remover colunas conflitantes, se existirem
            df_bahia_5.drop(columns=col_2, inplace=True)
    df_bahia_5 = df_bahia_5.merge(df_cnes_3[['CO_CNES', 'NO_FANTASIA']], left_on='CNES', right_on='CO_CNES', how='left')
    print(f"Hospitais sem nome encontrado: {df_bahia_5['NO_FANTASIA'].isna().sum()}")
    mortalidade_hosp = df_bahia_5.groupby(['CNES', 'NO_FANTASIA'], dropna=False).agg(Total_Internacoes=('MORTE', 'size'), Total_Obitos=('MORTE', lambda x: (x == 1).sum())).reset_index()
    # === 3️⃣ Merge com CNES ===
    mortalidade_hosp['NO_FANTASIA'] = mortalidade_hosp['NO_FANTASIA'].fillna(mortalidade_hosp['CNES'])
    MIN_INTERNACOES = 50
    mortalidade_hosp = mortalidade_hosp[mortalidade_hosp['Total_Internacoes'] >= MIN_INTERNACOES].copy()
    mortalidade_hosp['Taxa_Mortalidade_(%)'] = mortalidade_hosp['Total_Obitos'] / mortalidade_hosp['Total_Internacoes'] * 100
    top_10_mortalidade = mortalidade_hosp.sort_values(by='Taxa_Mortalidade_(%)', ascending=False).head(10)
    print('\nTop 10 Hospitais da Bahia com maior taxa de mortalidade:')
    print(top_10_mortalidade[['NO_FANTASIA', 'Total_Internacoes', 'Total_Obitos', 'Taxa_Mortalidade_(%)']].to_markdown(index=False, floatfmt='.2f'))
    # Verificar se o merge trouxe nomes
    fig_10 = px.bar(top_10_mortalidade, x='Taxa_Mortalidade_(%)', y='NO_FANTASIA', orientation='h', color='Taxa_Mortalidade_(%)', color_continuous_scale='Inferno', text=top_10_mortalidade['Taxa_Mortalidade_(%)'].map(lambda x: f'{x:.1f}%'), title='Top 10 Hospitais por Taxa de Mortalidade Hospitalar - Bahia', labels={'Taxa_Mortalidade_(%)': 'Taxa de Mortalidade (%)', 'NO_FANTASIA': 'Hospital (Nome Fantasia)'})
    fig_10.update_traces(textposition='outside', hovertemplate='<b>Hospital:</b> %{y}<br><b>Taxa Mortalidade:</b> %{x:.2f}%<extra></extra>')
    # === 4️⃣ Calcular mortalidade hospitalar ===
    fig_10.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Taxa de Mortalidade (%)', yaxis_title='Hospital', height=600, margin=dict(l=150, r=20, t=60, b=40))
    # Preencher nomes faltantes com o código CNES
    # Aplicar filtro mínimo de internações
    # Calcular taxa
    # Selecionar top 10
    # === 5️⃣ Exibir tabela ===
    # === 6️⃣ Gráfico interativo ===
    # === 7️⃣ Layout ===
    fig_10.show()
    return df_bahia_5, df_cnes_3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 14: Qual é o valor médio total (VAL_TOT) das AIHs por hospital no estado da Bahia?
    """)
    return


@app.cell
def _(df_bahia_5, df_cnes_3, px):
    df_cnes_4 = df_cnes_3[['CO_CNES', 'NO_FANTASIA']].copy()
    df_cnes_4['CO_CNES'] = df_cnes_4['CO_CNES'].astype(str).str.strip()
    df_cnes_4['NO_FANTASIA'] = df_cnes_4['NO_FANTASIA'].astype(str).str.strip()
    df_bahia_6 = df_bahia_5.copy()
    # === 2️⃣ Limpar o DataFrame da Bahia ===
    df_bahia_6['CNES'] = df_bahia_6['CNES'].astype(str).str.strip()
    for col_3 in ['CO_CNES', 'NO_FANTASIA']:
        if col_3 in df_bahia_6.columns:
    # Remover colunas duplicadas antes do merge
            df_bahia_6.drop(columns=col_3, inplace=True)
    df_bahia_6 = df_bahia_6.merge(df_cnes_4[['CO_CNES', 'NO_FANTASIA']], left_on='CNES', right_on='CO_CNES', how='left')
    print(f"Hospitais com nome ausente após merge: {df_bahia_6['NO_FANTASIA'].isna().sum()}")
    valor_medio_hosp = df_bahia_6.groupby(['CNES', 'NO_FANTASIA'], dropna=False)['VAL_TOT'].mean().reset_index().sort_values(by='VAL_TOT', ascending=False)
    # === 3️⃣ Merge com CNES (traz nome do hospital) ===
    valor_medio_hosp['NO_FANTASIA'] = valor_medio_hosp['NO_FANTASIA'].fillna(valor_medio_hosp['CNES'])
    top_10_valor_medio = valor_medio_hosp.head(10)
    print('\nTop 10 Hospitais da Bahia por Valor Médio Total da AIH:')
    print(top_10_valor_medio.to_markdown(index=False, floatfmt='.2f'))
    fig_11 = px.bar(top_10_valor_medio, x='VAL_TOT', y='NO_FANTASIA', orientation='h', color='VAL_TOT', color_continuous_scale='Greens', text=top_10_valor_medio['VAL_TOT'].map(lambda x: f'R$ {x:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.')), title='Top 10 Hospitais por Valor Médio Total da AIH - Bahia', labels={'VAL_TOT': 'Valor Médio Total da AIH (R$)', 'NO_FANTASIA': 'Hospital (Nome Fantasia)'})
    fig_11.update_traces(textposition='outside', hovertemplate='<b>Hospital:</b> %{y}<br><b>Valor Médio AIH:</b> R$ %{x:,.2f}<extra></extra>')
    fig_11.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Valor Médio Total da AIH (R$)', yaxis_title='Hospital', height=600, margin=dict(l=150, r=20, t=60, b=40))
    # Conferir se o merge deu certo
    # === 4️⃣ Calcular valor médio total da AIH ===
    # Selecionar top 10
    # === 5️⃣ Exibir tabela no console ===
    # === 6️⃣ Gráfico interativo ===
    # === 7️⃣ Ajustes visuais ===
    fig_11.show()
    return df_bahia_6, df_cnes_4


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 15: Quais hospitais baianos têm maior proporção de internações em UTI?
    """)
    return


@app.cell
def _(df_bahia_6, df_cnes_4, px):
    df_cnes_5 = df_cnes_4[['CO_CNES', 'NO_FANTASIA']].copy()
    df_cnes_5['CO_CNES'] = df_cnes_5['CO_CNES'].astype(str).str.strip()
    df_cnes_5['NO_FANTASIA'] = df_cnes_5['NO_FANTASIA'].astype(str).str.strip()
    df_bahia_6['CNES'] = df_bahia_6['CNES'].astype(str).str.strip()
    # === 2️⃣ Garantir que CNES está limpo no df_bahia ===
    for col_4 in ['CO_CNES', 'NO_FANTASIA']:
        if col_4 in df_bahia_6.columns:
    # Remover possíveis colunas duplicadas
            df_bahia_6.drop(columns=col_4, inplace=True)
    df_bahia_7 = df_bahia_6.merge(df_cnes_5[['CO_CNES', 'NO_FANTASIA']], left_on='CNES', right_on='CO_CNES', how='left')
    proporcao_uti_hosp = df_bahia_7.groupby(['CNES', 'NO_FANTASIA']).agg(Total_Internacoes=('MARCA_UTI', 'size'), Total_UTI=('MARCA_UTI', lambda x: (x > 0).sum())).reset_index()
    MIN_INTERNACOES_1 = 50
    # === 3️⃣ Merge com CNES para trazer o nome do hospital ===
    proporcao_uti_hosp = proporcao_uti_hosp[proporcao_uti_hosp['Total_Internacoes'] >= MIN_INTERNACOES_1].copy()
    proporcao_uti_hosp['Proporcao_UTI_(%)'] = proporcao_uti_hosp['Total_UTI'] / proporcao_uti_hosp['Total_Internacoes'] * 100
    top_10_uti = proporcao_uti_hosp.sort_values(by='Proporcao_UTI_(%)', ascending=False).head(10)
    print('\nTop 10 Hospitais da Bahia por Proporção de Internações em UTI:')
    print(top_10_uti[['NO_FANTASIA', 'Total_Internacoes', 'Total_UTI', 'Proporcao_UTI_(%)']].to_markdown(index=False, floatfmt='.2f'))
    fig_12 = px.bar(top_10_uti, x='Proporcao_UTI_(%)', y='NO_FANTASIA', orientation='h', color='Proporcao_UTI_(%)', color_continuous_scale='Purples', text=top_10_uti['Proporcao_UTI_(%)'].map(lambda x: f'{x:.1f}%'), title='Top 10 Hospitais por Proporção de Internações em UTI - Bahia', labels={'Proporcao_UTI_(%)': 'Proporção de Internações em UTI (%)', 'NO_FANTASIA': 'Hospital (Nome Fantasia)'})
    fig_12.update_traces(textposition='outside', hovertemplate='<b>Hospital:</b> %{y}<br><b>Proporção em UTI:</b> %{x:.1f}%<extra></extra>')
    # === 4️⃣ Calcular total de internações e proporção em UTI ===
    fig_12.update_layout(coloraxis_showscale=False, showlegend=False, xaxis_title='Proporção de Internações em UTI (%)', yaxis_title='Hospital', height=600, margin=dict(l=150, r=20, t=60, b=40))
    # Definir limite mínimo de internações
    # Calcular a proporção (%)
    # Selecionar top 10 hospitais
    # === 5️⃣ Exibir tabela no console ===
    # === 6️⃣ Gráfico interativo (Plotly) ===
    # === 7️⃣ Ajustes de layout ===
    fig_12.show()
    return (df_bahia_7,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 16: Qual é o valor total gasto com internações hospitalares na Bahia?
    """)
    return


@app.cell
def _(df_bahia_7):
    # Calcular o valor total gasto
    valor_total_gasto = df_bahia_7['VAL_TOT'].sum()
    print(f'O Valor Total Gasto (VAL_TOT) com internações hospitalares na Bahia é:')
    print(f'R$ {valor_total_gasto:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 17: Qual é o custo médio por internação em hospitais da Bahia?
    """)
    return


@app.cell
def _(df_bahia_7):
    # Calcular o Custo Médio por Internação
    custo_medio_internacao = df_bahia_7['VAL_TOT'].mean()
    print(f'O Custo Médio por internação em hospitais da Bahia é:')
    print(f'R$ {custo_medio_internacao:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 18: Qual é o valor médio das internações com óbito versus sem óbito no estado da Bahia?
    """)
    return


@app.cell
def _(df_bahia_7, px):
    map_obito = {0: 'Sem Óbito', 1: 'Com Óbito'}
    df_bahia_7['Status_Obito'] = df_bahia_7['MORTE'].map(map_obito)
    valor_medio_obito = df_bahia_7.groupby('Status_Obito')['VAL_TOT'].mean().reset_index().sort_values(by='VAL_TOT', ascending=False)
    # === 1️⃣ Mapeamento do status de óbito ===
    valor_medio_obito.columns = ['Status', 'Valor_Medio_Internacao']
    valor_medio_obito['Valor_Medio_R$'] = valor_medio_obito['Valor_Medio_Internacao'].apply(lambda x: f'R$ {x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    print('Valor Médio das Internações (R$) com e sem Óbito na Bahia:')
    # === 2️⃣ Calcular o valor médio total (VAL_TOT) por status ===
    print(valor_medio_obito[['Status', 'Valor_Medio_R$']].to_markdown(index=False))
    fig_13 = px.bar(valor_medio_obito, x='Status', y='Valor_Medio_Internacao', color='Status', text=valor_medio_obito['Valor_Medio_Internacao'].map(lambda x: f'R$ {x:,.0f}'.replace(',', 'X').replace('.', ',').replace('X', '.')), color_discrete_map={'Sem Óbito': '#4c72b0', 'Com Óbito': '#c44e52'}, title='Valor Médio das Internações: Óbito vs. Não Óbito - Bahia', labels={'Status': 'Resultado da Internação', 'Valor_Medio_Internacao': 'Valor Médio da AIH (R$)'})
    fig_13.update_traces(textposition='outside', hovertemplate='<b>%{x}</b><br>Valor Médio: R$ %{y:,.2f}<extra></extra>')
    fig_13.update_layout(showlegend=False, xaxis_title='Resultado da Internação', yaxis_title='Valor Médio da AIH (R$)', height=500, margin=dict(l=40, r=20, t=60, b=40))
    # === 3️⃣ Formatar valores para exibição textual ===
    # === 4️⃣ Exibir tabela no console ===
    # === 5️⃣ Gráfico interativo (Plotly) ===
    # === 6️⃣ Ajustes de layout e hover ===
    fig_13.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pergunta 19: Como evoluem os custos médios mensais das internações na Bahia?
    """)
    return


@app.cell
def _(df_bahia_7, pd):
    df_bahia_7['VAL_TOT'] = pd.to_numeric(df_bahia_7['VAL_TOT'], errors='coerce')
    df_bahia_7['COMPLEX'] = pd.to_numeric(df_bahia_7['COMPLEX'], errors='coerce')
    df_bahia_7.dropna(subset=['VAL_TOT', 'COMPLEX'], inplace=True)
    # Remover NaNs
    df_alta_complexidade = df_bahia_7[df_bahia_7['COMPLEX'] == 3].copy()
    valor_total_alta_complexidade = df_alta_complexidade['VAL_TOT'].sum()
    # Filtrar internações de ALTA COMPLEXIDADE
    print(f'O Valor Total Gasto com internações de Alta Complexidade na Bahia é:')
    # 2. Calcular o Valor Total Gasto (soma de VAL_TOT)
    print(f'R$ {valor_total_alta_complexidade:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'))
    return


if __name__ == "__main__":
    app.run()
