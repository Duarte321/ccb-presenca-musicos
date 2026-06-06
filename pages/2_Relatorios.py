import streamlit as st
import pandas as pd
import plotly.express as px
from utils.supabase_client import listar_servicos, listar_presenca, contar_por_funcao

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    .stApp { background-color: #f0f4f8; }
    .header-box {
        background: linear-gradient(135deg, #1a5276, #2980b9);
        border-radius: 16px; padding: 20px 24px;
        text-align: center; margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(26,82,118,0.18);
    }
    .header-box h2 { color: white; margin: 0; font-size: 1.5rem; }
    .metric-card {
        background: white; border-radius: 12px; padding: 16px;
        text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.06);
    }
    .metric-card .num { font-size: 2.2rem; font-weight: 700; color: #1a5276; }
    .metric-card .label { font-size: 0.85rem; color: #666; margin-top: 2px; }
    div.stButton > button {
        background: linear-gradient(135deg, #1a5276, #2980b9) !important;
        color: white !important; border: none !important;
        border-radius: 10px !important; padding: 12px 20px !important;
        font-size: 1rem !important; font-weight: 600 !important;
        width: 100% !important; box-shadow: 0 3px 12px rgba(26,82,118,0.2) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #154360, #1a6fa8) !important;
        transform: translateY(-1px) !important;
    }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

if st.button("← Voltar ao Início"):
    st.switch_page("app.py")

st.markdown("""
<div class="header-box">
    <h2>📊 Relatórios de Presença</h2>
</div>
""", unsafe_allow_html=True)

servicos = listar_servicos()
if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s for s in servicos}
escolha = st.selectbox("Selecione o serviço:", list(opcoes.keys()))
servico  = opcoes[escolha]
servico_id = servico['id']

contagem = contar_por_funcao(servico_id)
total    = sum(contagem.values())

st.markdown("")
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><div class="num">{contagem["Músico"]}</div><div class="label">🎵 Músicos</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><div class="num">{contagem["Organista"]}</div><div class="label">🎹 Organistas</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><div class="num">{contagem["Irmandade"]}</div><div class="label">🙏 Irmandade</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><div class="num">{total}</div><div class="label">👥 Total</div></div>', unsafe_allow_html=True)

st.markdown("")
presencas = listar_presenca(servico_id)

if presencas:
    df = pd.DataFrame(presencas)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Por Função")
        df_f = df['funcao'].value_counts().reset_index()
        df_f.columns = ['Função', 'Qtd']
        fig = px.bar(df_f, x='Função', y='Qtd', color='Função', text='Qtd',
                     color_discrete_map={'Músico':'#1a5276','Organista':'#2980b9','Irmandade':'#7fb3d3'})
        fig.update_layout(showlegend=False, plot_bgcolor='white', paper_bgcolor='white',
                          margin=dict(t=10,b=10,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🍧 Por Gênero")
        if 'genero' in df.columns and df['genero'].notna().any():
            df_g = df['genero'].value_counts().reset_index()
            df_g.columns = ['Gênero', 'Qtd']
            fig2 = px.pie(df_g, names='Gênero', values='Qtd',
                          color_discrete_sequence=['#1a5276','#85c1e9'])
            fig2.update_layout(paper_bgcolor='white', margin=dict(t=10,b=10,l=0,r=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Sem dados de gênero.")

    st.markdown("---")
    st.subheader("📄 Lista completa")
    df_show = df[['nome','funcao','genero','observacao','registrado_em']].copy()
    df_show.columns = ['Nome','Função','Gênero','Observação','Registrado em']
    st.dataframe(df_show, use_container_width=True, hide_index=True)

    csv = df_show.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv,
        file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ','_')}.csv",
        mime='text/csv',
        use_container_width=True
    )
else:
    st.info("🟡 Nenhuma presença registrada para este serviço.")
