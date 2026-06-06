import streamlit as st
import pandas as pd
import plotly.express as px
from utils.supabase_client import listar_servicos, listar_presenca, contar_por_funcao

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
st.title("📊 Relatórios de Presença")

servicos = listar_servicos()

if not servicos:
    st.info("Nenhum serviço cadastrado ainda. Acesse a página Registrar para começar.")
    st.stop()

# ── Filtros ───────────────────────────────────────────────────────────────────
st.subheader("🔍 Filtrar por serviço")
opcoes = {
    f"{s['data']} — {s['tipo']} {('| ' + s['local']) if s.get('local') else ''}": s
    for s in servicos
}
escolha = st.selectbox("Serviço:", list(opcoes.keys()))
servico = opcoes[escolha]

registros = listar_presenca(servico["id"])

if not registros:
    st.warning("Nenhuma presença registrada neste serviço.")
    st.stop()

df = pd.DataFrame(registros)
df["registrado_em"] = pd.to_datetime(df["registrado_em"])

# ── Métricas ──────────────────────────────────────────────────────────────────
st.divider()
contagem = contar_por_funcao(servico["id"])
total = sum(contagem.values())

col1, col2, col3, col4 = st.columns(4)
col1.metric("🎵 Músicos", contagem["Músico"])
col2.metric("🎹 Organistas", contagem["Organista"])
col3.metric("🙏 Irmandade", contagem["Irmandade"])
col4.metric("👥 Total Geral", total)

# ── Gráficos ──────────────────────────────────────────────────────────────────
st.divider()
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.subheader("Contagem por Função")
    df_contagem = pd.DataFrame(
        [{"Função": k, "Quantidade": v} for k, v in contagem.items()]
    )
    fig_bar = px.bar(
        df_contagem,
        x="Função",
        y="Quantidade",
        color="Função",
        color_discrete_map={
            "Músico": "#01696f",
            "Organista": "#437a22",
            "Irmandade": "#006494",
        },
        text="Quantidade",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)

with col_g2:
    st.subheader("Proporção")
    fig_pie = px.pie(
        df_contagem,
        names="Função",
        values="Quantidade",
        color="Função",
        color_discrete_map={
            "Músico": "#01696f",
            "Organista": "#437a22",
            "Irmandade": "#006494",
        },
    )
    fig_pie.update_layout(showlegend=True)
    st.plotly_chart(fig_pie, use_container_width=True)

# ── Tabela completa ───────────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Lista completa de presentes")

cols_exibir = [c for c in ["nome", "funcao", "genero", "observacao", "registrado_em"] if c in df.columns]
df_exib = df[cols_exibir].copy()
df_exib["registrado_em"] = df_exib["registrado_em"].dt.strftime("%d/%m/%Y %H:%M")
df_exib.columns = ["Nome", "Função", "Gênero", "Observação", "Registrado em"][:len(cols_exibir)]

st.dataframe(df_exib, use_container_width=True, hide_index=True)

# ── Exportar CSV ──────────────────────────────────────────────────────────────
csv = df_exib.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Exportar CSV",
    data=csv,
    file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ', '_')}.csv",
    mime="text/csv",
    use_container_width=True,
)
