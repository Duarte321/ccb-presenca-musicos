import streamlit as st
import pandas as pd
import plotly.express as px
from utils.supabase_client import listar_servicos, listar_presenca, contar_por_funcao

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="wide")
st.title("📊 Relatórios de Presença")

servicos = listar_servicos()

if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

# ── Filtros ────────────────────────────────────────────────────────────────────
st.subheader("Filtrar por serviço")
opcoes = {f"{s['data']} - {s['tipo']} ({s.get('local', '') or 'Sem local'})": s for s in servicos}
escolha = st.selectbox("Serviço:", list(opcoes.keys()))
servico = opcoes[escolha]
servico_id = servico['id']

# ── Contadores ─────────────────────────────────────────────────────────────────
contagem = contar_por_funcao(servico_id)
total = sum(contagem.values())

c1, c2, c3, c4 = st.columns(4)
c1.metric("🎵 Músicos", contagem['Músico'])
c2.metric("🎹 Organistas", contagem['Organista'])
c3.metric("🙏 Irmandade", contagem['Irmandade'])
c4.metric("👥 Total", total)

st.markdown("---")

# ── Gráficos ───────────────────────────────────────────────────────────────────
presencas = listar_presenca(servico_id)

if presencas:
    df = pd.DataFrame(presencas)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Contagem por Função")
        df_funcao = df['funcao'].value_counts().reset_index()
        df_funcao.columns = ['Função', 'Quantidade']
        fig_bar = px.bar(
            df_funcao, x='Função', y='Quantidade',
            color='Função',
            color_discrete_map={'Músico': '#1f77b4', 'Organista': '#ff7f0e', 'Irmandade': '#2ca02c'},
            text='Quantidade'
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Distribuição por Gênero")
        if 'genero' in df.columns and df['genero'].notna().any():
            df_genero = df['genero'].value_counts().reset_index()
            df_genero.columns = ['Gênero', 'Quantidade']
            fig_pizza = px.pie(
                df_genero, names='Gênero', values='Quantidade',
                color_discrete_sequence=['#4C72B0', '#DD8452']
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        else:
            st.info("Sem dados de gênero para exibir.")

    st.markdown("---")
    st.subheader("📄 Lista completa de presenças")
    df_exibir = df[['nome', 'funcao', 'genero', 'observacao', 'registrado_em']].copy()
    df_exibir.columns = ['Nome', 'Função', 'Gênero', 'Observação', 'Registrado em']
    st.dataframe(df_exibir, use_container_width=True, hide_index=True)

    # ── Exportar CSV ───────────────────────────────────────────────────────────
    csv = df_exibir.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv,
        file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ', '_')}.csv",
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("Nenhuma presença registrada para este serviço.")
