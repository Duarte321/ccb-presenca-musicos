import streamlit as st
from utils.supabase_client import listar_servicos, listar_presenca, deletar_presenca, deletar_servico

st.set_page_config(page_title="Gerenciar", page_icon="⚙️", layout="centered", initial_sidebar_state="collapsed")

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"]         { display: none !important; }
    [data-testid="stToolbar"]        { display: none !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    .stApp > header                  { display: none !important; }
    footer { visibility: hidden; } #MainMenu { visibility: hidden; }
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .main, .block-container {
        background: linear-gradient(135deg, #0f1923 0%, #1a2d45 50%, #0f1923 100%) !important;
    }
    .block-container { padding-top: 1.5rem !important; max-width: 860px !important; }

    .page-header {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px; padding: 20px 28px;
        text-align: center; margin-bottom: 24px; backdrop-filter: blur(10px);
    }
    .page-header h2 { color: #fff !important; margin: 0 0 4px; font-size: 1.5rem; font-weight: 800; }
    .page-header p  { color: rgba(255,255,255,0.4) !important; margin: 0; font-size: 0.85rem; }

    .section-title {
        color: rgba(255,255,255,0.85) !important; font-size: 0.8rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 24px 0 12px; padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* ── INPUTS CORRIGIDOS ── */
    .stSelectbox > div > div { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important; }
    .stSelectbox > div > div > div[data-baseweb="select"] > div { background: transparent !important; color: #f1f5f9 !important; }
    .stSelectbox span, .stSelectbox div { color: #f1f5f9 !important; }
    [data-baseweb="select"] * { color: #f1f5f9 !important; background: transparent !important; }
    [data-baseweb="popover"] [role="option"] { background: #1a2d45 !important; color: #f1f5f9 !important; }
    [data-baseweb="popover"] [role="option"]:hover { background: #2a3d55 !important; }
    .stTextInput input { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important; color: #f1f5f9 !important; caret-color: #60a5fa !important; }
    .stTextInput input::placeholder { color: rgba(255,255,255,0.3) !important; }
    .stTextInput input:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important; }
    label { color: rgba(255,255,255,0.75) !important; }
    p { color: rgba(255,255,255,0.75) !important; }

    .pres-item {
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 10px 16px; margin-bottom: 6px;
        display: flex; align-items: center; gap: 10px;
        color: rgba(255,255,255,0.75); font-size: 0.88rem;
    }
    .pres-badge { font-size: 0.7rem; font-weight: 700; padding: 3px 9px; border-radius: 20px; white-space: nowrap; }
    .badge-musico    { background: rgba(59,130,246,0.2);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
    .badge-organista { background: rgba(167,139,250,0.2); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.3); }
    .badge-irmandade { background: rgba(52,211,153,0.2);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.3); }

    /* Botão padrão azul */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 14px 20px !important;
        font-size: 0.93rem !important; font-weight: 700 !important;
        width: 100% !important; letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
        transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
    }
    div.stButton > button:hover {
        box-shadow: 0 8px 28px rgba(59,130,246,0.5) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    div.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

    /* Botão voltar */
    div.stButton:first-of-type > button {
        background: rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: none !important; font-size: 0.85rem !important;
        padding: 10px 18px !important; width: auto !important;
    }
    div.stButton:first-of-type > button:hover {
        background: rgba(255,255,255,0.12) !important;
        transform: translateY(-1px) !important; box-shadow: none !important;
    }

    /* Botão excluir serviço — vermelho */
    .btn-danger > div > button {
        background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 13px 20px !important;
        font-size: 0.9rem !important; font-weight: 700 !important;
        box-shadow: 0 4px 16px rgba(220,38,38,0.35) !important;
        transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
    }
    .btn-danger > div > button:hover {
        box-shadow: 0 8px 24px rgba(220,38,38,0.55) !important;
        transform: translateY(-2px) scale(1.02) !important;
    }
    .btn-danger > div > button:active { transform: translateY(0) scale(0.98) !important; }

    .danger-box {
        background: rgba(220,38,38,0.08); border: 1px solid rgba(220,38,38,0.25);
        border-radius: 14px; padding: 18px 20px; margin-top: 16px;
    }
    .danger-box .danger-title {
        color: #fca5a5 !important; font-size: 0.82rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 8px;
    }
    .danger-box .danger-desc {
        color: rgba(255,255,255,0.45) !important; font-size: 0.8rem; margin-bottom: 12px;
    }

    hr { border-color: rgba(255,255,255,0.08) !important; }
    .stAlert { border-radius: 12px !important; }
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

if st.button("← Voltar"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
    <h2>⚙️ Gerenciar Registros</h2>
    <p>Visualize, exclua registros de presença e serviços</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">Selecione o serviço</div>', unsafe_allow_html=True)
servicos = listar_servicos()
if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s for s in servicos}
escolha = st.selectbox("Serviço:", list(opcoes.keys()))
servico_selecionado = opcoes[escolha]
servico_id = servico_selecionado['id']

# ── Registros de presença ──────────────────────────────────────────────────
st.markdown('<div class="section-title">Registros do serviço</div>', unsafe_allow_html=True)
presencas = listar_presenca(servico_id)

if not presencas:
    st.info("Nenhuma presença registrada neste serviço.")
else:
    badge_map = {"Músico":"badge-musico","Organista":"badge-organista","Irmandade":"badge-irmandade"}
    for p in presencas:
        badge = badge_map.get(p['funcao'],"badge-irmandade")
        col1, col2 = st.columns([5,1])
        with col1:
            st.markdown(f"""
            <div class="pres-item">
                <span style="flex:1">👤 <strong style="color:#fff">{p['nome']}</strong></span>
                <span class="pres-badge {badge}">{p['funcao']}</span>
                <span style="color:rgba(255,255,255,0.35);font-size:0.78rem">{p.get('genero','')}</span>
            </div>""", unsafe_allow_html=True)
        with col2:
            if st.button("🗑️", key=f"del_{p['id']}", help=f"Excluir {p['nome']}"):
                deletar_presenca(p['id'])
                st.success(f"✅ {p['nome']} removido.")
                st.rerun()

# ── Zona de perigo: excluir serviço ──────────────────────────────────────────
st.markdown("""
<div class="danger-box">
    <div class="danger-title">⚠️ Zona de Perigo</div>
    <div class="danger-desc">Excluir o serviço apagará permanentemente o serviço e <strong style="color:#fca5a5">todas as presenças</strong> vinculadas a ele. Esta ação não pode ser desfeita.</div>
</div>
""", unsafe_allow_html=True)

if 'confirmar_exclusao' not in st.session_state:
    st.session_state.confirmar_exclusao = False

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

if not st.session_state.confirmar_exclusao:
    if st.button("🗑️ Excluir este serviço", key="btn_excluir_srv", use_container_width=True):
        st.session_state.confirmar_exclusao = True
        st.rerun()
else:
    st.warning(f"⚠️ Tem certeza que deseja excluir **{escolha}** e todas as suas presenças?")
    col_sim, col_nao = st.columns(2)
    with col_sim:
        if st.button("✅ Sim, excluir tudo", key="btn_confirmar_sim", use_container_width=True):
            deletar_servico(servico_id)
            st.session_state.confirmar_exclusao = False
            st.success("✅ Serviço excluído com sucesso!")
            st.rerun()
    with col_nao:
        if st.button("❌ Cancelar", key="btn_confirmar_nao", use_container_width=True):
            st.session_state.confirmar_exclusao = False
            st.rerun()
