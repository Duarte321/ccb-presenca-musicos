import streamlit as st

st.set_page_config(
    page_title="CCB - Presença Músicos",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    /* Esconde sidebar e botão de toggle */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* Fundo geral */
    .stApp { background-color: #f0f4f8; }

    /* Cabeçalho */
    .header-box {
        background: linear-gradient(135deg, #1a5276, #2980b9);
        border-radius: 16px;
        padding: 32px 24px 24px 24px;
        text-align: center;
        margin-bottom: 32px;
        box-shadow: 0 4px 20px rgba(26,82,118,0.18);
    }
    .header-box h1 { color: white; font-size: 2rem; margin: 0 0 6px 0; }
    .header-box p  { color: rgba(255,255,255,0.85); margin: 0; font-size: 1rem; }

    /* Cards de navegação */
    .nav-card {
        background: white;
        border-radius: 14px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        transition: transform 0.15s, box-shadow 0.15s;
        cursor: pointer;
        border: 2px solid transparent;
        margin-bottom: 12px;
    }
    .nav-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(26,82,118,0.15);
        border-color: #2980b9;
    }
    .nav-card .icon { font-size: 2.5rem; margin-bottom: 10px; }
    .nav-card h3 { color: #1a5276; margin: 0 0 6px 0; font-size: 1.1rem; }
    .nav-card p  { color: #666; font-size: 0.85rem; margin: 0; }

    /* Botões principais */
    div.stButton > button {
        background: linear-gradient(135deg, #1a5276, #2980b9) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 20px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: 0 3px 12px rgba(26,82,118,0.2) !important;
        transition: all 0.2s !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #154360, #1a6fa8) !important;
        box-shadow: 0 6px 18px rgba(26,82,118,0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Botão voltar */
    div.stButton > button[kind="secondary"] {
        background: white !important;
        color: #1a5276 !important;
        border: 2px solid #1a5276 !important;
        box-shadow: none !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background: #eaf2fb !important;
        transform: translateY(-1px) !important;
    }

    /* Esconde footer */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Cabeçalho ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-box">
    <h1>🎵 CCB — Presença de Músicos</h1>
    <p>Congregação Cristã no Brasil · Controle de Presença</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Selecione uma opção:")
st.markdown("")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋\n\nRegistrar\n\nRegistre presenças de um serviço", use_container_width=True):
        st.switch_page("pages/1_Registrar.py")

with col2:
    if st.button("📊\n\nRelatórios\n\nGráficos e exportação CSV", use_container_width=True):
        st.switch_page("pages/2_Relatorios.py")

with col3:
    if st.button("⚙️\n\nGerenciar\n\nEditar e excluir registros", use_container_width=True):
        st.switch_page("pages/3_Gerenciar.py")

st.markdown("---")
st.caption("© 2026 · Sistema CCB · Desenvolvido com Streamlit + Supabase")
