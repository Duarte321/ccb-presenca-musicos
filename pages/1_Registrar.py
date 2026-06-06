import streamlit as st
from datetime import date
from utils.supabase_client import (
    listar_servicos, criar_servico, registrar_presenca,
    listar_presenca, contar_por_funcao
)

st.set_page_config(page_title="Registrar Presença", page_icon="📋", layout="centered", initial_sidebar_state="collapsed")

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    footer { visibility: hidden; } #MainMenu { visibility: hidden; }
    .stApp { background: linear-gradient(135deg, #0f1923 0%, #1a2d45 50%, #0f1923 100%) !important; }
    .block-container { padding-top: 1.5rem !important; }

    .page-header {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px; padding: 20px 28px;
        text-align: center; margin-bottom: 24px;
        backdrop-filter: blur(10px);
    }
    .page-header h2 { color: #fff; margin: 0 0 4px; font-size: 1.5rem; font-weight: 800; }
    .page-header p  { color: rgba(255,255,255,0.4); margin: 0; font-size: 0.85rem; }

    /* Métrica premium */
    .metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 16px 0; }
    .metric-card {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 18px 12px;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .metric-card .num { font-size: 2rem; font-weight: 800; color: #fff; line-height: 1; }
    .metric-card .lbl { font-size: 0.75rem; color: rgba(255,255,255,0.45); margin-top: 5px; }
    .metric-card.blue  .num { color: #60a5fa; }
    .metric-card.purple .num { color: #a78bfa; }
    .metric-card.green  .num { color: #34d399; }
    .metric-card.gold   .num { color: #fbbf24; }

    /* Presença list */
    .pres-item {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px; padding: 10px 16px;
        margin-bottom: 6px;
        display: flex; align-items: center; gap: 10px;
        color: rgba(255,255,255,0.75); font-size: 0.88rem;
    }
    .pres-badge {
        font-size: 0.7rem; font-weight: 700; padding: 3px 9px;
        border-radius: 20px; white-space: nowrap;
    }
    .badge-musico   { background: rgba(59,130,246,0.2);  color: #93c5fd; border: 1px solid rgba(59,130,246,0.3); }
    .badge-organista{ background: rgba(167,139,250,0.2); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.3); }
    .badge-irmandade{ background: rgba(52,211,153,0.2);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.3); }

    /* Inputs e forms */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }
    .stTextInput label, .stSelectbox label,
    .stDateInput label, .stRadio label p,
    .stTextInput > label, label { color: rgba(255,255,255,0.7) !important; }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 14px 20px !important;
        font-size: 0.93rem !important; font-weight: 700 !important;
        width: 100% !important; letter-spacing: 0.3px !important;
        box-shadow: 0 4px 20px rgba(59,130,246,0.3) !important;
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
        box-shadow: 0 8px 28px rgba(59,130,246,0.5) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    /* Botão voltar */
    div.stButton:first-child > button {
        background: rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: none !important;
        font-size: 0.85rem !important;
        padding: 10px 16px !important;
        width: auto !important;
    }
    div.stButton:first-child > button:hover {
        background: rgba(255,255,255,0.12) !important;
        transform: translateY(-1px) !important;
        box-shadow: none !important;
    }

    .section-title {
        color: rgba(255,255,255,0.85); font-size: 0.8rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 24px 0 12px; padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .stAlert { border-radius: 12px !important; }
    hr { border-color: rgba(255,255,255,0.08) !important; }
    .stRadio > div { flex-direction: row; gap: 12px; }
    .stRadio > div > label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important; padding: 8px 16px !important;
        color: rgba(255,255,255,0.7) !important;
    }
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

if st.button("← Voltar"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
    <h2>📋 Registrar Presença</h2>
    <p>Selecione o serviço e adicione os presentes</p>
</div>
""", unsafe_allow_html=True)

# ── Serviço ──────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">① Selecione ou crie um serviço</div>', unsafe_allow_html=True)

servicos = listar_servicos()
opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s['id'] for s in servicos}

aba = st.radio("", ["Selecionar existente", "Criar novo serviço"], horizontal=True)

servico_id = None

if aba == "Selecionar existente":
    if opcoes:
        escolha = st.selectbox("Serviço:", list(opcoes.keys()))
        servico_id = opcoes[escolha]
    else:
        st.warning("Nenhum serviço cadastrado. Crie um novo.")
else:
    TIPOS_PADRAO = [
        "Culto de Semana", "Culto de Sábado",
        "Culto de Domingo", "Reunião de Oração",
        "Reunião de Jovens", "Outro"
    ]
    with st.form("form_servico"):
        col1, col2 = st.columns(2)
        with col1:
            data_srv = st.date_input("Data:", value=date.today())
        with col2:
            tipo_opcao = st.selectbox("Tipo (base):", TIPOS_PADRAO)

        # Campo editável para personalizar o tipo
        tipo_srv = st.text_input(
            "Editar tipo (opcional):",
            value=tipo_opcao,
            placeholder="Ex: Culto Especial de Natal",
            help="Você pode personalizar o nome do tipo livremente."
        )
        col3, col4 = st.columns(2)
        with col3:
            local_srv = st.text_input("Local:")
        with col4:
            obs_srv = st.text_input("Observação:")

        if st.form_submit_button("✅ Criar Serviço", use_container_width=True):
            tipo_final = tipo_srv.strip() if tipo_srv.strip() else tipo_opcao
            resultado = criar_servico(str(data_srv), tipo_final, local_srv, obs_srv)
            if resultado:
                st.success("Serviço criado com sucesso!")
                st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# ── Contagem e registros ──────────────────────────────────────────────────────
if servico_id:
    contagem = contar_por_funcao(servico_id)
    total    = sum(contagem.values())

    st.markdown('<div class="section-title">② Contagem atual</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card blue"><div class="num">{contagem['Músico']}</div><div class="lbl">🎵 Músicos</div></div>
        <div class="metric-card purple"><div class="num">{contagem['Organista']}</div><div class="lbl">🎹 Organistas</div></div>
        <div class="metric-card green"><div class="num">{contagem['Irmandade']}</div><div class="lbl">🙏 Irmandade</div></div>
        <div class="metric-card gold"><div class="num">{total}</div><div class="lbl">👥 Total</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">③ Adicionar presença</div>', unsafe_allow_html=True)
    with st.form("form_presenca", clear_on_submit=True):
        nome = st.text_input("Nome completo:", placeholder="Ex: João da Silva")
        col1, col2 = st.columns(2)
        with col1:
            funcao = st.selectbox("Função:", ["Músico", "Organista", "Irmandade"])
        with col2:
            genero = st.selectbox("Gênero:", ["Irmão", "Irmã"])
        obs = st.text_input("Observação (opcional):")
        if st.form_submit_button("➕ Registrar Presença", use_container_width=True):
            if not nome.strip():
                st.error("Informe o nome.")
            else:
                registrar_presenca(servico_id, nome.strip(), funcao, genero, obs)
                st.success(f"✅ {nome} registrado como {funcao}!")
                st.rerun()

    st.markdown('<div class="section-title">④ Lista de presenças</div>', unsafe_allow_html=True)
    presencas = listar_presenca(servico_id)
    if presencas:
        badge_map = {"Músico": "badge-musico", "Organista": "badge-organista", "Irmandade": "badge-irmandade"}
        for p in presencas:
            badge = badge_map.get(p['funcao'], "badge-irmandade")
            st.markdown(f"""
            <div class="pres-item">
                <span style="flex:1">👤 <strong style="color:#fff">{p['nome']}</strong></span>
                <span class="pres-badge {badge}">{p['funcao']}</span>
                <span style="color:rgba(255,255,255,0.35);font-size:0.78rem">{p.get('genero','')}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Nenhuma presença registrada ainda neste serviço.")
else:
    st.info("⬅️ Selecione ou crie um serviço acima para começar.")
