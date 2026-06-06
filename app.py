import streamlit as st

st.set_page_config(
    page_title="CCB - Presença Músicos",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }

    /* Remove TUDO branco do Streamlit */
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"]         { background: transparent !important; display: none !important; }
    [data-testid="stToolbar"]        { display: none !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    .stApp > header                  { display: none !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    section[data-testid="stMain"] > div:first-child { padding-top: 0 !important; }

    /* Fundo escuro em TODA a app, incluindo a área do header */
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .main, .block-container {
        background: linear-gradient(135deg, #0f1923 0%, #1a2d45 50%, #0f1923 100%) !important;
    }
    .block-container { padding-top: 2rem !important; max-width: 860px !important; }

    /* HERO */
    .hero { text-align: center; padding: 48px 24px 36px; margin-bottom: 8px; }
    .hero-logo {
        width: 72px; height: 72px;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6);
        border-radius: 20px;
        display: flex; align-items: center; justify-content: center;
        font-size: 2.2rem; margin: 0 auto 20px;
        box-shadow: 0 8px 32px rgba(59,130,246,0.4);
    }
    .hero h1 { color: #ffffff; font-size: 2.2rem; font-weight: 800; margin: 0 0 8px 0; letter-spacing: -0.5px; }
    .hero p  { color: rgba(255,255,255,0.45); font-size: 0.95rem; margin: 0; }

    /* NAV CARDS */
    .nav-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px; padding: 28px 20px 24px;
        text-align: center; backdrop-filter: blur(10px);
        transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
        margin-bottom: 8px;
    }
    .nav-card:hover {
        background: rgba(255,255,255,0.10);
        border-color: rgba(59,130,246,0.5);
        transform: translateY(-4px);
        box-shadow: 0 16px 40px rgba(0,0,0,0.3), 0 0 0 1px rgba(59,130,246,0.3);
    }
    .nav-card .icon { font-size: 2.4rem; margin-bottom: 12px; display: block; }
    .nav-card h3    { color: #fff; font-size: 1rem; font-weight: 700; margin: 0 0 6px; }
    .nav-card p     { color: rgba(255,255,255,0.45); font-size: 0.78rem; margin: 0; line-height: 1.4; }
    .nav-card .badge {
        display: inline-block; margin-top: 12px;
        background: rgba(59,130,246,0.2); color: #93c5fd;
        font-size: 0.7rem; font-weight: 600;
        padding: 3px 10px; border-radius: 20px;
        border: 1px solid rgba(59,130,246,0.3);
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
        color: white !important; border: none !important;
        border-radius: 14px !important; padding: 16px 20px !important;
        font-size: 0.95rem !important; font-weight: 700 !important;
        width: 100% !important; letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(59,130,246,0.35) !important;
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        box-shadow: 0 8px 30px rgba(59,130,246,0.5) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    div.stButton > button:active { transform: translateY(0) scale(0.99) !important; }

    /* FOOTER */
    .footer-bar {
        text-align: center; padding: 24px 0 8px;
        color: rgba(255,255,255,0.2); font-size: 0.75rem;
        border-top: 1px solid rgba(255,255,255,0.06); margin-top: 16px;
    }
    .footer-bar span { color: rgba(255,255,255,0.35); }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-logo">🎵</div>
    <h1>CCB Presença</h1>
    <p>Congregação Cristã no Brasil &nbsp;·&nbsp; Controle de Presença</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="nav-card">
        <span class="icon">📋</span>
        <h3>Registrar</h3>
        <p>Registre presenças de um serviço</p>
        <span class="badge">Novo registro</span>
    </div>""", unsafe_allow_html=True)
    if st.button("Acessar →", key="btn_reg", use_container_width=True):
        st.switch_page("pages/1_Registrar.py")

with col2:
    st.markdown("""
    <div class="nav-card">
        <span class="icon">📊</span>
        <h3>Relatórios</h3>
        <p>Gráficos, exportação CSV e PDF</p>
        <span class="badge">Exportar dados</span>
    </div>""", unsafe_allow_html=True)
    if st.button("Acessar →", key="btn_rel", use_container_width=True):
        st.switch_page("pages/2_Relatorios.py")

with col3:
    st.markdown("""
    <div class="nav-card">
        <span class="icon">⚙️</span>
        <h3>Gerenciar</h3>
        <p>Editar e excluir registros</p>
        <span class="badge">Administrar</span>
    </div>""", unsafe_allow_html=True)
    if st.button("Acessar →", key="btn_ger", use_container_width=True):
        st.switch_page("pages/3_Gerenciar.py")

st.markdown("""
<div class="footer-bar">
    © 2026 &nbsp;·&nbsp; <span>Sistema CCB</span> &nbsp;·&nbsp; Desenvolvido com Streamlit + Supabase
</div>
""", unsafe_allow_html=True)
