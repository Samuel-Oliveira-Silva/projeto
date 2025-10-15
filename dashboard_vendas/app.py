import streamlit as st
import pandas as pd
import plotly.express as px
from database import conexao

st.set_page_config(page_title="Dashboard de Vendas e Lucro", layout="wide")
st.title("📈 Dashboard de Vendas e Lucro — Pluvius Tech (exemplo)")

# Inicializar banco (garante que exista)
conexao.inicializar_banco()

# Carregar dados
df = conexao.carregar_dados()

if df.empty:
    st.warning("Nenhuma venda encontrada no banco. Rode 'python popular_dados.py' para inserir dados de exemplo.")
    st.stop()

# Sidebar — filtros
st.sidebar.header("Filtros")
min_date = df['data_venda'].min().date()
max_date = df['data_venda'].max().date()
data_range = st.sidebar.date_input("Período", [min_date, max_date])

produtos = sorted(df['produto'].unique())
selecionados = st.sidebar.multiselect("Produtos", produtos, default=produtos)

# Aplicar filtros
start_date, end_date = data_range
mask = (df['data_venda'].dt.date >= start_date) & (df['data_venda'].dt.date <= end_date) & (df['produto'].isin(selecionados))
df_filtrado = df[mask].copy()

# KPIs
receita_total = df_filtrado['receita'].sum()
lucro_total = df_filtrado['lucro'].sum()
vendas_total = df_filtrado['quantidade'].sum()
ticket_medio = (receita_total / vendas_total) if vendas_total > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Receita Total", f"R$ {receita_total:,.2f}")
col2.metric("📦 Vendas Totais", f"{int(vendas_total)}")
col3.metric("📈 Lucro Total", f"R$ {lucro_total:,.2f}")
col4.metric("💳 Ticket Médio", f"R$ {ticket_medio:,.2f}")

st.markdown("---")

# Receita por produto (bar)
receita_prod = df_filtrado.groupby("produto", as_index=False)["receita"].sum().sort_values("receita", ascending=False)
fig1 = px.bar(receita_prod, x="produto", y="receita", title="Receita por Produto", labels={"receita":"Receita (R$)","produto":"Produto"})
st.plotly_chart(fig1, use_container_width=True)

# Lucro por produto (pie)
lucro_prod = df_filtrado.groupby("produto", as_index=False)["lucro"].sum().sort_values("lucro", ascending=False)
fig2 = px.pie(lucro_prod, names="produto", values="lucro", title="Participação do Lucro por Produto")
st.plotly_chart(fig2, use_container_width=True)

# Receita ao longo do tempo (time series)
time_df = df_filtrado.groupby("data_venda", as_index=False)["receita"].sum().sort_values("data_venda")
fig3 = px.line(time_df, x="data_venda", y="receita", title="Receita ao Longo do Tempo", markers=True, labels={"data_venda":"Data","receita":"Receita (R$)"})
st.plotly_chart(fig3, use_container_width=True)

# Tabela de vendas (últimas 50)
st.subheader("Últimas Vendas")
st.dataframe(df_filtrado.sort_values("data_venda", ascending=False).head(50).reset_index(drop=True))

st.markdown("#### Exportar")
col_x, col_y = st.columns([1,3])
with col_x:
    if st.button("Exportar CSV"):
        csv = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, file_name="vendas_filtradas.csv", mime="text/csv")
with col_y:
    st.write("Use os filtros para ajustar o conjunto de dados e clique em Exportar CSV.")
