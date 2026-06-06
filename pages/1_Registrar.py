import streamlit as st
from datetime import date
from utils.supabase_client import (
    listar_servicos, criar_servico, registrar_presenca,
    listar_presenca, contar_por_funcao
)

st.set_page_config(page_title="Registrar Presença", page_icon="📋", layout="centered", initial_sidebar_state="collapsed")

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

# ── Botão Voltar ────────────────────────────────────────────────────────────────
if st.button("← Voltar ao Início"):
    st.switch_page("app.py")

st.markdown("""
<div class="header-box">
    <h2>📋 Registrar Presença</h2>
</div>
""", unsafe_allow_html=True)

# ── Selecionar ou criar serviço ────────────────────────────────────────────────
st.subheader("1️⃣ Selecione ou crie um serviço")

servicos = listar_servicos()
opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local', '') or 'Sem local'}": s['id'] for s in servicos}

aba = st.radio("", ["Selecionar existente", "Criar novo serviço"], horizontal=True)

servico_id = None

if aba == "Selecionar existente":
    if opcoes:
        escolha = st.selectbox("Serviço:", list(opcoes.keys()))
        servico_id = opcoes[escolha]
    else:
        st.warning("⚠️ Nenhum serviço cadastrado. Crie um novo abaixo.")
else:
    with st.form("form_servico"):
        col1, col2 = st.columns(2)
        with col1:
            data_srv = st.date_input("Data:", value=date.today())
        with col2:
            tipo_srv = st.selectbox("Tipo:", [
                "Culto de Semana", "Culto de Sábado",
                "Culto de Domingo", "Reunião de Oração",
                "Reunião de Jovens", "Outro"
            ])
        local_srv = st.text_input("Local:")
        obs_srv   = st.text_input("Observação:")
        if st.form_submit_button("✅ Criar Serviço", use_container_width=True):
            resultado = criar_servico(str(data_srv), tipo_srv, local_srv, obs_srv)
            if resultado:
                st.success("Serviço criado com sucesso!")
                st.rerun()

st.markdown("---")

# ── Registrar presença ─────────────────────────────────────────────────────────
if servico_id:
    st.subheader("2️⃣ Contagem atual")
    contagem = contar_por_funcao(servico_id)
    total    = sum(contagem.values())

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><div class="num">{contagem["Músico"]}</div><div class="label">🎵 Músicos</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="num">{contagem["Organista"]}</div><div class="label">🎹 Organistas</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="num">{contagem["Irmandade"]}</div><div class="label">🙏 Irmandade</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><div class="num">{total}</div><div class="label">👥 Total</div></div>', unsafe_allow_html=True)

    st.markdown("")
    st.subheader("3️⃣ Adicionar presença")

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

    st.markdown("---")
    st.subheader("📄 Lista de presenças")
    presencas = listar_presenca(servico_id)
    if presencas:
        for p in presencas:
            st.markdown(f"• **{p['nome']}** — {p['funcao']} · {p.get('genero', '—')}")
    else:
        st.info("🟡 Nenhuma presença registrada ainda neste serviço.")
else:
    st.info("⬅️ Selecione ou crie um serviço acima para começar.")
