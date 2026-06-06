import streamlit as st
from utils.supabase_client import listar_servicos, listar_presenca, deletar_presenca, deletar_servico

st.set_page_config(page_title="Gerenciar", page_icon="⚙️", layout="centered", initial_sidebar_state="collapsed")

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
    .item-row {
        background: white; border-radius: 10px; padding: 12px 16px;
        margin-bottom: 8px; box-shadow: 0 1px 6px rgba(0,0,0,0.05);
        display: flex; align-items: center; justify-content: space-between;
    }
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
    <h2>⚙️ Gerenciar Registros</h2>
</div>
""", unsafe_allow_html=True)

servicos = listar_servicos()
if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

# ── Excluir presença individual ────────────────────────────────────────────────
st.subheader("🗑️ Excluir presença")
opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s['id'] for s in servicos}
escolha   = st.selectbox("Serviço:", list(opcoes.keys()), key="sel_ger")
servico_id = opcoes[escolha]

presencas = listar_presenca(servico_id)
if presencas:
    for p in presencas:
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(f"👤 **{p['nome']}** — {p['funcao']} · {p.get('genero','—')}")
        with col2:
            if st.button("🗑️", key=f"del_{p['id']}", help="Excluir"):
                deletar_presenca(p['id'])
                st.success(f"{p['nome']} removido!")
                st.rerun()
else:
    st.info("🟡 Nenhuma presença neste serviço.")

st.markdown("---")

# ── Excluir serviço inteiro ────────────────────────────────────────────────────
st.subheader("⚠️ Excluir serviço completo")
st.warning("⚠️ Isso remove o serviço **e todas** as presenças vinculadas!")

opcoes2    = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s['id'] for s in servicos}
escolha2   = st.selectbox("Serviço para excluir:", list(opcoes2.keys()), key="sel_del_srv")
servico_id2 = opcoes2[escolha2]

confirmar = st.checkbox("✅ Confirmo que desejo excluir este serviço e todas as presenças.")
if st.button("🗑️ Excluir Serviço Permanentemente", use_container_width=True):
    if confirmar:
        deletar_servico(servico_id2)
        st.success("Serviço excluído com sucesso!")
        st.rerun()
    else:
        st.error("Marque a caixa de confirmação primeiro.")
