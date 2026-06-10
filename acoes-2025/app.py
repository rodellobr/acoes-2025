import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

ACOES = {
    "Petrobras (PETR4)": "PETR4.SA",
    "Itaú (ITUB4)": "ITUB4.SA",
    "Vale (VALE3)": "VALE3.SA",
}

CORES = {
    "Petrobras (PETR4)": "#009B3A",
    "Itaú (ITUB4)": "#003087",
    "Vale (VALE3)": "#005B8E",
}

st.set_page_config(page_title="Ações BR 2025", page_icon="📈", layout="wide")
st.title("📈 Dashboard de Ações Brasileiras — 2025")
st.caption("Petrobras (PETR4) · Itaú (ITUB4) · Vale (VALE3)")

with st.sidebar:
    st.header("Filtros")
    data_inicio = st.date_input("Data inicial", value=pd.Timestamp("2025-01-02"))
    data_fim = st.date_input("Data final", value=pd.Timestamp("2025-12-31"))
    mostrar_tabela = st.checkbox("Mostrar tabela de dados brutos", value=False)

@st.cache_data(ttl=3600)
def carregar_dados(inicio, fim):
    frames = {}
    for nome, ticker in ACOES.items():
        df = yf.download(ticker, start=inicio, end=fim, progress=False, auto_adjust=True)
        if not df.empty:
            frames[nome] = df["Close"].squeeze()
    return pd.DataFrame(frames).dropna()

with st.spinner("Buscando cotações..."):
    df = carregar_dados(str(data_inicio), str(data_fim))

if df.empty:
    st.error("Não foi possível carregar os dados. Verifique sua conexão e o intervalo de datas.")
    st.stop()

# Métricas no topo
st.subheader("Resumo do período")
cols = st.columns(len(ACOES))
for i, nome in enumerate(ACOES):
    if nome in df.columns:
        preco_inicial = df[nome].iloc[0]
        preco_final = df[nome].iloc[-1]
        retorno = (preco_final / preco_inicial - 1) * 100
        maximo = df[nome].max()
        minimo = df[nome].min()
        retornos_diarios = df[nome].pct_change().dropna()
        volatilidade = retornos_diarios.std() * 100
        cols[i].metric(
            label=nome,
            value=f"R$ {preco_final:.2f}",
            delta=f"{retorno:+.2f}% no período",
        )
        cols[i].caption(f"Máx: R$ {maximo:.2f} · Mín: R$ {minimo:.2f} · Volatilidade: {volatilidade:.2f}%/dia")

st.divider()

aba1, aba2, aba3, aba4 = st.tabs([
    "💰 Preço de Fechamento",
    "📊 Performance Acumulada (%)",
    "📉 Retorno Diário (%)",
    "📦 Volume Negociado",
])

with aba1:
    fig = go.Figure()
    for nome in ACOES:
        if nome in df.columns:
            fig.add_trace(go.Scatter(
                x=df.index, y=df[nome],
                name=nome, line=dict(color=CORES[nome], width=2),
            ))
    fig.update_layout(
        title="Preço de Fechamento Ajustado (R$)",
        xaxis_title="Data", yaxis_title="Preço (R$)",
        hovermode="x unified", height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

with aba2:
    perf = (df / df.iloc[0] - 1) * 100
    fig = go.Figure()
    for nome in ACOES:
        if nome in perf.columns:
            fig.add_trace(go.Scatter(
                x=perf.index, y=perf[nome],
                name=nome, line=dict(color=CORES[nome], width=2),
            ))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    fig.update_layout(
        title="Performance Acumulada (base = primeiro dia do período)",
        xaxis_title="Data", yaxis_title="Variação (%)",
        hovermode="x unified", height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

with aba3:
    retornos = df.pct_change().dropna() * 100
    fig = go.Figure()
    for nome in ACOES:
        if nome in retornos.columns:
            fig.add_trace(go.Bar(
                x=retornos.index, y=retornos[nome],
                name=nome, marker_color=CORES[nome], opacity=0.7,
            ))
    fig.update_layout(
        title="Retorno Diário (%)",
        xaxis_title="Data", yaxis_title="Variação (%)",
        barmode="group", hovermode="x unified", height=500,
    )
    st.plotly_chart(fig, use_container_width=True)

with aba4:
    volumes = {}
    for nome, ticker in ACOES.items():
        raw = yf.download(ticker, start=str(data_inicio), end=str(data_fim), progress=False, auto_adjust=True)
        if not raw.empty and "Volume" in raw.columns:
            volumes[nome] = raw["Volume"].squeeze()
    df_vol = pd.DataFrame(volumes).dropna()

    if not df_vol.empty:
        fig = go.Figure()
        for nome in ACOES:
            if nome in df_vol.columns:
                fig.add_trace(go.Bar(
                    x=df_vol.index, y=df_vol[nome],
                    name=nome, marker_color=CORES[nome], opacity=0.7,
                ))
        fig.update_layout(
            title="Volume Negociado Diário",
            xaxis_title="Data", yaxis_title="Volume",
            barmode="group", hovermode="x unified", height=500,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Dados de volume não disponíveis para o período selecionado.")

if mostrar_tabela:
    st.subheader("Dados brutos — Preço de Fechamento (R$)")
    st.dataframe(df.style.format("R$ {:.2f}"), use_container_width=True)
