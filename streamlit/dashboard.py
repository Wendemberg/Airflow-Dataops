"""
Streamlit Dashboard - Varejo Inteligente
Lê dados já agregados do Gold e apenas visualiza
Sem processamento adicional - dados prontos para análise
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from minio import Minio
import io
from env_config import get_minio_config

st.set_page_config(
    page_title="Varejo Inteligente - Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
    <style>
    .title-main { color: #0066cc; font-size: 2.5em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Carregamento seguro de configurações (sem valores padrão para credenciais)
minio_cfg = get_minio_config()
MINIO_CONFIG = {
    'endpoint': minio_cfg['endpoint'],
    'access_key': minio_cfg['access_key'],
    'secret_key': minio_cfg['secret_key'],
    'secure': False
}

@st.cache_data(ttl=60)
def get_analytics():
    """Lê gold_analytics_*.parquet"""
    try:
        client = Minio(**MINIO_CONFIG)
        objects = list(client.list_objects('gold', recursive=True))
        files = [o for o in objects if 'gold_analytics' in o.object_name and '.parquet' in o.object_name]

        if not files:
            return None, "Nenhum arquivo encontrado"

        latest = max(files, key=lambda x: x.last_modified)
        response = client.get_object('gold', latest.object_name)
        df = pd.read_parquet(io.BytesIO(response.read()))

        return df, latest.object_name
    except Exception as e:
        return None, str(e)

@st.cache_data(ttl=60)
def get_dimension(dim_name):
    """Lê gold_dim_*.parquet"""
    try:
        client = Minio(**MINIO_CONFIG)
        objects = list(client.list_objects('gold', recursive=True))
        files = [o for o in objects if f'gold_dim_{dim_name}' in o.object_name and '.parquet' in o.object_name]

        if not files:
            return None

        latest = max(files, key=lambda x: x.last_modified)
        response = client.get_object('gold', latest.object_name)
        return pd.read_parquet(io.BytesIO(response.read()))
    except Exception:
        return None

# ============================================
# HEADER
# ============================================
st.markdown('<div class="title-main">🛒 VAREJO INTELIGENTE</div>', unsafe_allow_html=True)
st.markdown("Análise de Vendas em Tempo Real")
st.markdown("---")

gold_df, gold_info = get_analytics()

if gold_df is None:
    st.error(f"❌ {gold_info}")
    st.stop()

st.caption(f"📄 Arquivo: {gold_info}")

# ============================================
# KPIs PRINCIPAIS
# ============================================
st.subheader("📊 Principais Indicadores")

# Função para formatar valores grandes
def format_currency(value):
    """Formata valores grandes em notação compacta"""
    if value >= 1_000_000:
        return f"R$ {value / 1_000_000:.1f}M"
    elif value >= 1_000:
        return f"R$ {value / 1_000:.0f}K"
    else:
        return f"R$ {value:.2f}"

col1, col2, col3, col4, col5 = st.columns(5)

total_vendas = gold_df['receita'].sum() if 'receita' in gold_df.columns else gold_df['valor'].sum()
qtd_total = gold_df['quantidade'].sum() if 'quantidade' in gold_df.columns else 0
num_clientes = gold_df['cliente'].nunique()
num_produtos = gold_df['produto'].nunique()
ticket_medio = total_vendas / len(gold_df) if len(gold_df) > 0 else 0

with col1:
    st.metric("💰 Total Vendas", format_currency(total_vendas))
with col2:
    st.metric("📦 Quantidade", f"{qtd_total:,.0f}")
with col3:
    st.metric("👥 Clientes", f"{num_clientes:,}")
with col4:
    st.metric("🏷️ Produtos", f"{num_produtos:,}")
with col5:
    st.metric("💳 Ticket Médio", format_currency(ticket_medio))

st.markdown("---")

# ============================================
# ANÁLISES POR ABAS
# ============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Vendas",
    "👥 Clientes",
    "🏷️ Produtos",
    "🏙️ Geográfico",
    "💳 Pagamento",
    "📊 Dados Brutos"
])

# TAB 1: VENDAS
with tab1:
    st.subheader("📈 Análise de Vendas")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Distribuição por Canal")
        df_canal = get_dimension('canal')
        if df_canal is not None and len(df_canal) > 0:
            fig = px.pie(df_canal, values='valor_total', names='canal', title="Vendas por Canal")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de canal")

    with col2:
        st.markdown("#### Status dos Pedidos")
        df_status = get_dimension('status')
        if df_status is not None and len(df_status) > 0:
            fig = px.bar(df_status, x='status', y='qtd_transacoes', title="Pedidos por Status")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de status")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Maiores Vendas")
        top10 = gold_df.nlargest(10, 'valor')[['cliente', 'produto', 'valor', 'data']]
        st.dataframe(top10, use_container_width=True)

    with col2:
        st.markdown("#### Distribuição de Valores")
        if len(gold_df) > 0:
            fig = px.histogram(gold_df, x='valor', nbins=50, title="Histograma de Valores")
            st.plotly_chart(fig, use_container_width=True)

# TAB 2: CLIENTES
with tab2:
    st.subheader("👥 Análise de Clientes")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top 10 Clientes (Valor)")
        df_cliente = get_dimension('cliente')
        if df_cliente is not None and len(df_cliente) > 0:
            df_top = df_cliente.head(10)
            fig = px.bar(df_top.sort_values('valor_total'), y='cliente', x='valor_total', orientation='h', title="Top Clientes por Valor")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top 10 Clientes (Quantidade)")
        if df_cliente is not None and len(df_cliente) > 0:
            df_top = df_cliente.head(10)
            fig = px.bar(df_top.sort_values('quantidade_vendida'), y='cliente', x='quantidade_vendida', orientation='h', title="Top Clientes por Qtd")
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Clientes por Avaliação")
        if 'avaliacao' in gold_df.columns:
            aval_data = gold_df['avaliacao'].value_counts().sort_index()
            if len(aval_data) > 0:
                fig = px.bar(x=aval_data.index, y=aval_data.values, title="Distribuição de Avaliações")
                st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Análise de Sentimento")
        if 'sentimento' in gold_df.columns:
            sent_data = gold_df['sentimento'].value_counts()
            if len(sent_data) > 0:
                fig = px.pie(values=sent_data.values, names=sent_data.index, title="Sentimento dos Clientes")
                st.plotly_chart(fig, use_container_width=True)

# TAB 3: PRODUTOS
with tab3:
    st.subheader("🏷️ Análise de Produtos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Top Produtos (Quantidade)")
        df_produto = get_dimension('produto')
        if df_produto is not None and len(df_produto) > 0:
            df_top = df_produto.head(10)
            fig = px.bar(df_top.sort_values('quantidade_vendida'), y='produto', x='quantidade_vendida', orientation='h', title="Top Produtos")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Top Produtos (Receita)")
        if df_produto is not None and len(df_produto) > 0:
            df_top = df_produto.head(10)
            fig = px.bar(df_top.sort_values('valor_total'), y='produto', x='valor_total', orientation='h', title="Receita por Produto")
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Produtos Mais Vendidos")
        if df_produto is not None:
            st.dataframe(df_produto[['produto', 'quantidade_vendida', 'valor_total']].head(15), use_container_width=True)

    with col2:
        st.markdown("#### Correlação: Quantidade vs Valor")
        if len(gold_df) > 0:
            fig = px.scatter(gold_df, x='quantidade', y='valor', title="Quantidade x Valor", opacity=0.6)
            st.plotly_chart(fig, use_container_width=True)

# TAB 4: GEOGRÁFICO
with tab4:
    st.subheader("🏙️ Análise Geográfica")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Vendas por Cidade")
        df_cidade = get_dimension('cidade')
        if df_cidade is not None and len(df_cidade) > 0:
            df_top = df_cidade.head(15)
            fig = px.bar(df_top.sort_values('valor_total'), y='cidade', x='valor_total', orientation='h', title="Top 15 Cidades por Vendas")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Quantidade por Cidade")
        if df_cidade is not None and len(df_cidade) > 0:
            df_top = df_cidade.head(15)
            fig = px.bar(df_top.sort_values('quantidade_vendida'), y='cidade', x='quantidade_vendida', orientation='h', title="Top 15 Cidades por Qtd")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Distribuição de Cidades")
    if df_cidade is not None and len(df_cidade) > 0:
        fig = px.pie(df_cidade, values='valor_total', names='cidade', title="Proporção por Cidade")
        st.plotly_chart(fig, use_container_width=True)

# TAB 5: PAGAMENTO
with tab5:
    st.subheader("💳 Análise de Pagamento")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Formas de Pagamento")
        df_pagto = get_dimension('pagamento')
        if df_pagto is not None and len(df_pagto) > 0:
            fig = px.pie(df_pagto, values='qtd_transacoes', names='forma_pagamento', title="Distribuição de Formas")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Valor Médio por Forma")
        if df_pagto is not None and len(df_pagto) > 0:
            fig = px.bar(df_pagto.sort_values('valor_medio'), y='forma_pagamento', x='valor_medio', orientation='h', title="Valor Médio por Forma")
            st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Receita Total por Forma")
        if df_pagto is not None and len(df_pagto) > 0:
            fig = px.bar(df_pagto.sort_values('valor_total'), y='forma_pagamento', x='valor_total', orientation='h', title="Receita por Forma")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Quantidade de Transações")
        if df_pagto is not None and len(df_pagto) > 0:
            fig = px.bar(df_pagto, x='forma_pagamento', y='qtd_transacoes', title="Transações por Forma")
            st.plotly_chart(fig, use_container_width=True)

# TAB 6: DADOS BRUTOS
with tab6:
    st.subheader("📊 Dados Brutos")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total de Registros", len(gold_df))
    with col2:
        st.metric("📋 Total de Colunas", len(gold_df.columns))
    with col3:
        st.metric("💾 Tamanho (MB)", f"{gold_df.memory_usage(deep=True).sum() / 1024 / 1024:.2f}")

    st.markdown("#### Colunas Disponíveis")
    st.write(list(gold_df.columns))

    st.markdown("#### Tabela Completa")
    st.dataframe(gold_df, use_container_width=True, height=500)

    st.markdown("#### Estatísticas Descritivas")
    st.dataframe(gold_df.describe(), use_container_width=True)

    csv = gold_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar como CSV",
        data=csv,
        file_name=f"varejo_inteligente_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

# ============================================
# FOOTER
# ============================================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    if st.button("🔄 Atualizar Dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.caption(f"Última atualização: {datetime.now().strftime('%H:%M:%S')} | {gold_info}")
