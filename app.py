# app.py (versão com dados mock)
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import time
from datetime import datetime

# ------------------------------
# Configuração da página
# ------------------------------
st.set_page_config(
    page_title="Shein Sales Dashboard - Demo",
    page_icon="🛍️",
    layout="wide"
)

# ------------------------------
# CSS melhorado
# ------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        color: #EE4D2D;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f9fafb;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #EE4D2D;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: 0.3s;
        text-align: center;
    }
    .metric-card:hover {
        transform: scale(1.02);
    }
    .stButton button {
        background-color: #EE4D2D;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Configuração da API
# ------------------------------
API_URL = "http://api:8000"  # URL do container da API

# ------------------------------
# DADOS MOCK (funciona sem API)
# ------------------------------
def carregar_dados_mock():
    """Retorna dados de exemplo quando a API não está disponível"""
    produtos_mock = [
        {"id": 1, "nome": "Vestido Floral", "categoria": "Vestidos", "marca": "Shein", "preco": 79.90, "estoque": 50, "vendas": 15},
        {"id": 2, "nome": "Blusa Masculina", "categoria": "Blusas", "marca": "Shein", "preco": 49.90, "estoque": 30, "vendas": 10},
        {"id": 3, "nome": "Calça Jeans", "categoria": "Calças", "marca": "Shein", "preco": 99.90, "estoque": 20, "vendas": 8},
        {"id": 4, "nome": "Saia Plissada", "categoria": "Saias", "marca": "Shein", "preco": 59.90, "estoque": 40, "vendas": 12},
        {"id": 5, "nome": "Camiseta Básica", "categoria": "Camisetas", "marca": "Shein", "preco": 29.90, "estoque": 100, "vendas": 25}
    ]
    
    analise_categorias_mock = {
        "Vestidos": 15,
        "Blusas": 10,
        "Calças": 8,
        "Saias": 12,
        "Camisetas": 25
    }
    
    analise_marcas_mock = {
        "Shein": 70
    }
    
    return produtos_mock, analise_categorias_mock, analise_marcas_mock

# ------------------------------
# Funções para buscar dados (com fallback para mock)
# ------------------------------
@st.cache_data(ttl=30)
def carregar_produtos():
    try:
        response = requests.get(f"{API_URL}/produtos/", timeout=5)
        if response.status_code == 200:
            st.sidebar.success("✅ Conectado à API")
            return response.json()
        else:
            st.sidebar.warning("⚠️ API retornou erro, usando dados demo")
            produtos_mock, _, _ = carregar_dados_mock()
            return produtos_mock
    except requests.exceptions.RequestException:
        st.sidebar.warning("🔌 API offline, usando dados demo")
        produtos_mock, _, _ = carregar_dados_mock()
        return produtos_mock

@st.cache_data(ttl=30)
def carregar_analise_categorias():
    try:
        response = requests.get(f"{API_URL}/categorias/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            _, categorias_mock, _ = carregar_dados_mock()
            return categorias_mock
    except requests.exceptions.RequestException:
        _, categorias_mock, _ = carregar_dados_mock()
        return categorias_mock

@st.cache_data(ttl=30)
def carregar_analise_marcas():
    try:
        response = requests.get(f"{API_URL}/marcas/", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            _, _, marcas_mock = carregar_dados_mock()
            return marcas_mock
    except requests.exceptions.RequestException:
        _, _, marcas_mock = carregar_dados_mock()
        return marcas_mock

# ------------------------------
# Barra lateral com filtros e ações
# ------------------------------
with st.sidebar:
    st.markdown("## 🛍️ Shein Dashboard")
    st.markdown("**Dados em tempo real da API**")
    st.markdown("---")
    
    # Exibir status da API
    st.markdown("**Status da Conexão:**")
    
    # Botão para atualizar dados
    if st.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    st.markdown("**Adicionar Novo Produto**")
    
    # Formulário para adicionar produto (só funciona com API)
    with st.form("novo_produto"):
        nome = st.text_input("Nome do Produto", value="Vestido Floral")
        categoria = st.text_input("Categoria", value="Vestidos")
        marca = st.text_input("Marca", value="Shein")
        preco = st.number_input("Preço", min_value=0.0, value=79.90, format="%.2f")
        estoque = st.number_input("Estoque", min_value=0, value=50)
        vendas = st.number_input("Vendas", min_value=0, value=15)
        
        submitted = st.form_submit_button("Adicionar Produto")
        if submitted:
            novo_produto = {
                "nome": nome,
                "categoria": categoria,
                "marca": marca,
                "preco": preco,
                "estoque": estoque,
                "vendas": vendas
            }
            try:
                response = requests.post(f"{API_URL}/produtos/", json=novo_produto, timeout=5)
                if response.status_code == 200:
                    st.success("✅ Produto adicionado com sucesso!")
                    st.cache_data.clear()
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Erro ao adicionar produto (API offline)")
            except requests.exceptions.RequestException:
                st.error("❌ API offline - não foi possível adicionar produto")

# ------------------------------
# Carregar dados da API (com fallback para mock)
# ------------------------------
produtos = carregar_produtos()
analise_categorias = carregar_analise_categorias()
analise_marcas = carregar_analise_marcas()

# Converter para DataFrame
df_produtos = pd.DataFrame(produtos)

# ------------------------------
# Cabeçalho com indicador de atualização
# ------------------------------
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown("<div class='main-header'>Dashboard de Vendas - Shein</div>", unsafe_allow_html=True)
with col_head2:
    st.markdown(f"<div style='text-align: right; color: #666;'>Última atualização:<br>{datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)

# ------------------------------
# Métricas principais
# ------------------------------
if not df_produtos.empty:
    vendas_totais = df_produtos['vendas'].sum()
    total_produtos = len(df_produtos)
    ticket_medio = df_produtos['preco'].mean()
    estoque_total = df_produtos['estoque'].sum()
else:
    vendas_totais = 0
    total_produtos = 0
    ticket_medio = 0
    estoque_total = 0

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Vendas Totais</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>{vendas_totais:,}</div>
        <div style='font-size: 0.8rem; color: #666;'>Unidades vendidas</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Total de Produtos</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>{total_produtos}</div>
        <div style='font-size: 0.8rem; color: #666;'>Produtos cadastrados</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Ticket Médio</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>R$ {ticket_medio:,.2f}</div>
        <div style='font-size: 0.8rem; color: #666;'>Preço médio</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div>Estoque Total</div>
        <div style='font-size: 1.5rem; font-weight: bold;'>{estoque_total:,}</div>
        <div style='font-size: 0.8rem; color: #666;'>Unidades em estoque</div>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------
# Gráficos
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    if analise_categorias:
        fig_categorias = go.Figure()
        fig_categorias.add_trace(go.Bar(
            x=list(analise_categorias.keys()),
            y=list(analise_categorias.values()),
            name='Vendas por Categoria',
            marker_color='#EE4D2D'
        ))
        fig_categorias.update_layout(
            title='Vendas por Categoria',
            xaxis_title='Categoria',
            yaxis_title='Total de Vendas',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_categorias, use_container_width=True)

with col2:
    if analise_marcas:
        fig_marcas = go.Figure()
        fig_marcas.add_trace(go.Bar(
            x=list(analise_marcas.keys()),
            y=list(analise_marcas.values()),
            name='Vendas por Marca',
            marker_color='#FF6B6B'
        ))
        fig_marcas.update_layout(
            title='Vendas por Marca',
            xaxis_title='Marca',
            yaxis_title='Total de Vendas',
            height=400,
            template='plotly_white'
        )
        st.plotly_chart(fig_marcas, use_container_width=True)

# ------------------------------
# Tabela de produtos
# ------------------------------
st.markdown("### 📦 Produtos Cadastrados")
if not df_produtos.empty:
    # Formatar a tabela
    df_display = df_produtos.copy()
    df_display['preco'] = df_display['preco'].apply(lambda x: f"R$ {x:,.2f}")
    
    st.dataframe(df_display, use_container_width=True)
    
    # Estatísticas rápidas
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.metric("Produto mais vendido", df_produtos.loc[df_produtos['vendas'].idxmax(), 'nome'] if not df_produtos.empty else "-")
    with col_stat2:
        st.metric("Categoria com mais vendas", max(analise_categorias, key=analise_categorias.get) if analise_categorias else "-")
    with col_stat3:
        st.metric("Marca líder", max(analise_marcas, key=analise_marcas.get) if analise_marcas else "-")
else:
    st.info("📝 Nenhum produto carregado")

# ------------------------------
# Status do sistema
# ------------------------------
st.markdown("---")
st.markdown("### 🔍 Status do Sistema")

col_status1, col_status2, col_status3 = st.columns(3)

with col_status1:
    try:
        response = requests.get(f"{API_URL}/produtos/", timeout=5)
        if response.status_code == 200:
            st.success("✅ API Online")
        else:
            st.warning("⚠️ API com problemas")
    except:
        st.error("❌ API Offline")

with col_status2:
    if produtos:
        st.success(f"✅ {len(produtos)} produtos carregados")
    else:
        st.warning("⚠️ Nenhum produto carregado")

with col_status3:
    st.info(f"🕒 Última atualização: {datetime.now().strftime('%H:%M:%S')}")