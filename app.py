import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página e tema
st.set_page_config(
    page_title="Dashboard SIH/SUS - Bahia",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="metric-container"] {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. Funções de Carregamento e Pré-processamento (Otimizadas com Cache) ---

@st.cache_data
def carregar_dados():
    """Carrega e pré-processa todos os dados."""
    try:
        df = pd.read_csv('datasets/RD202401.csv', sep=';', low_memory=False)
        
        colunas_interesse = [
            'UF_ZI', 'ESPEC', 'MUNIC_RES', 'SEXO', 'DIAR_ACOM', 'QT_DIARIAS', 
            'VAL_TOT', 'DT_INTER', 'DT_SAIDA', 'DIAG_PRINC', 'GESTRISCO',
            'COD_IDADE', 'IDADE', 'DIAS_PERM', 'MORTE', 'RACA_COR', 'CNES',
            'COMPLEX', 'MARCA_UTI', 'MUNIC_MOV', 'VAL_UTI'
        ]
        df = df[colunas_interesse].copy()

        df['UF_ZI'] = df['UF_ZI'].astype(str)
        df_bahia = df[df['UF_ZI'].str.startswith('29')].copy()

        # Conversões
        df_bahia['DIAG_PRINC'] = df_bahia['DIAG_PRINC'].astype(str)
        df_bahia['CNES'] = df_bahia['CNES'].astype(str).str.strip()
        df_bahia['MORTE'] = pd.to_numeric(df_bahia['MORTE'], errors='coerce')
        df_bahia['IDADE'] = pd.to_numeric(df_bahia['IDADE'], errors='coerce')
        df_bahia['DIAS_PERM'] = pd.to_numeric(df_bahia['DIAS_PERM'], errors='coerce')
        df_bahia['VAL_TOT'] = pd.to_numeric(df_bahia['VAL_TOT'], errors='coerce')
        df_bahia['ESPEC'] = pd.to_numeric(df_bahia['ESPEC'], errors='coerce')
        df_bahia['MARCA_UTI'] = pd.to_numeric(df_bahia['MARCA_UTI'], errors='coerce')
        df_bahia['GESTRISCO'] = pd.to_numeric(df_bahia['GESTRISCO'], errors='coerce')
        df_bahia['MUNIC_MOV'] = df_bahia['MUNIC_MOV'].astype(str).str.strip()

        # Faixa Etária
        bins = [0, 9, 19, 29, 39, 49, 59, 69, 79, 89, 99, 120]
        labels = ['0–9', '10–19', '20–29', '30–39', '40–49', '50–59', '60–69', '70–79', '80–89', '90–99', '100+']
        df_bahia['faixa_etaria'] = pd.cut(df_bahia['IDADE'].fillna(-1).astype(int), bins=bins, labels=labels, right=True, ordered=False)
        
        # Status de Óbito
        df_bahia['Status_Obito'] = df_bahia['MORTE'].map({0: 'Sem Óbito', 1: 'Com Óbito'})

        # Municípios
        df_municipios = pd.read_csv('datasets/municipios.csv')
        df_municipios['codigo_ibge'] = df_municipios['codigo_ibge'].astype(str).str[:6]
        df_municipios = df_municipios[df_municipios['codigo_ibge'].str.startswith('29')]
        
        return df_bahia, df_municipios

    except FileNotFoundError as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return pd.DataFrame(), pd.DataFrame()

df_bahia, df_municipios = carregar_dados()

if df_bahia.empty:
    st.stop()

# --- 2. Funções de Gráficos (Plotly) ---

def plot_top_municipios(df_bahia, df_municipios):
    df_temp = df_bahia.dropna(subset=['MUNIC_MOV']).copy()
    contagem_internacoes = df_temp['MUNIC_MOV'].value_counts().nlargest(10).reset_index()
    contagem_internacoes.columns = ['MUNIC_MOV', 'INTER']
    
    top_municipios = pd.merge(contagem_internacoes, df_municipios, left_on='MUNIC_MOV', right_on='codigo_ibge', how='left')
    top_municipios['Municipios'] = top_municipios['nome'].fillna('Desconhecido') + ' - BA'
    
    fig = px.bar(
        top_municipios, 
        x='INTER', 
        y='Municipios', 
        orientation='h',
        title='Top 10 Municípios (Local de Internação)',
        labels={'INTER': 'Internações', 'Municipios': ''},
        color='INTER',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, height=400)
    return fig

def plot_distribuicao_idade(df_bahia):
    faixa_counts = df_bahia['faixa_etaria'].value_counts().sort_index().reset_index()
    faixa_counts.columns = ['Faixa Etária', 'Internações']
    
    fig = px.bar(
        faixa_counts, 
        x='Faixa Etária', 
        y='Internações',
        title='Distribuição por Faixa Etária',
        labels={'Internações': 'Nº de Internações', 'Faixa Etária': ''},
        color='Internações',
        color_continuous_scale='Tealgrn'
    )
    fig.update_layout(coloraxis_showscale=False, height=400)
    return fig

def plot_distribuicao_cid10(df_bahia):
    map_cid_capitulo = {
        'A': 'I. Infecciosas', 'B': 'I. Infecciosas', 'C': 'II. Neoplasias', 'D': 'III. Sangue',
        'E': 'IV. Endócrinas', 'F': 'V. Transtornos mentais', 'G': 'VI. Sistema nervoso',
        'H': 'VII/VIII. Olho/Ouvido', 'I': 'IX. Circulatório', 'J': 'X. Respiratório',
        'K': 'XI. Digestivo', 'L': 'XII. Pele', 'M': 'XIII. Osteomusculares',
        'N': 'XIV. Geniturinário', 'O': 'XV. Gravidez parto puerpério',
        'P': 'XVI. Perinatais', 'Q': 'XVII. Malformações', 'R': 'XVIII. Sintomas anormais',
        'S': 'XIX. Lesões/envenenamentos', 'T': 'XIX. Lesões/envenenamentos',
        'V': 'XX. Causas externas', 'W': 'XX. Causas externas', 'X': 'XX. Causas externas', 
        'Y': 'XX. Causas externas', 'Z': 'XXI. Contatos com serviços', 'U': 'XXII. Especiais'
    }

    df_temp = df_bahia.dropna(subset=['DIAG_PRINC']).copy()
    df_temp = df_temp[df_temp['DIAG_PRINC'].str.len() >= 1].copy()
    df_temp['CAPITULO_CID'] = df_temp['DIAG_PRINC'].str[0].str.upper()
    df_temp['DESCRICAO_CAPITULO'] = df_temp['CAPITULO_CID'].map(map_cid_capitulo).fillna('Outros')

    frequencia = df_temp['DESCRICAO_CAPITULO'].value_counts().reset_index()
    frequencia.columns = ['Capitulo_CID', 'Frequencia']
    
    fig = px.bar(
        frequencia.head(12), 
        x='Frequencia', 
        y='Capitulo_CID',
        orientation='h',
        title='Top 12 Causas (Capítulo CID-10)',
        labels={'Frequencia': 'Internações', 'Capitulo_CID': ''},
        color='Frequencia',
        color_continuous_scale='Sunset'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, coloraxis_showscale=False, height=500)
    return fig

# --- 3. Layout do Dashboard ---

st.title("🏥 SIH/SUS Bahia - Dashboard Executivo")
st.markdown("Visão geral das Autorizações de Internação Hospitalar (AIH).")

# Métricas
total_internacoes = len(df_bahia)
total_obitos = df_bahia[df_bahia['MORTE'] == 1].shape[0]
percentual_obitos = (total_obitos / total_internacoes) * 100 if total_internacoes > 0 else 0
valor_total = df_bahia['VAL_TOT'].sum()
custo_medio = df_bahia['VAL_TOT'].mean()

col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Total Internações", f"{total_internacoes:,.0f}".replace(',', '.'))
with col2: st.metric("Taxa Mortalidade", f"{percentual_obitos:.2f}%", f"{total_obitos:,.0f} Óbitos")
with col3: st.metric("Custo Total", f"R$ {valor_total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
with col4: st.metric("Custo Médio AIH", f"R$ {custo_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

st.divider()

# Gráficos Principais
col_graf1, col_graf2 = st.columns(2)
with col_graf1:
    st.plotly_chart(plot_distribuicao_cid10(df_bahia), width='stretch')
with col_graf2:
    st.plotly_chart(plot_top_municipios(df_bahia, df_municipios), width='stretch')

st.plotly_chart(plot_distribuicao_idade(df_bahia), width='stretch')

# Expanders de Dados Detalhados
with st.expander("📊 Ver Dados Detalhados por Hospital e Gestão"):
    col_tab1, col_tab2 = st.columns(2)
    
    with col_tab1:
        st.subheader("Top Hospitais (CNES) por Volume")
        df_hosp = df_bahia['CNES'].value_counts().reset_index().head(10)
        df_hosp.columns = ['CNES', 'Internações']
        st.dataframe(df_hosp, width='stretch', hide_index=True)
        
    with col_tab2:
        df_obst = df_bahia[df_bahia['ESPEC'] == 2]
        risco = len(df_obst[df_obst['GESTRISCO'] == 1])
        st.subheader("Obstetrícia e Risco")
        st.metric("Total Obstétricas", f"{len(df_obst):,.0f}".replace(',', '.'))
        st.metric("Gestantes de Risco", f"{risco:,.0f} ({risco/len(df_obst)*100 if len(df_obst) else 0:.1f}%)")
