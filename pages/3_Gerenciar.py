import streamlit as st
from utils.supabase_client import (
    listar_servicos, listar_presenca, deletar_presenca, deletar_servico
)

st.set_page_config(page_title="Gerenciar", page_icon="⚙️", layout="centered")
st.title("⚙️ Gerenciar Registros")

servicos = listar_servicos()

if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

# ── Excluir presença individual ────────────────────────────────────────────────
st.subheader("🗑️ Excluir presença")

opcoes = {f"{s['data']} - {s['tipo']} ({s.get('local', '') or 'Sem local'})": s['id'] for s in servicos}
escolha = st.selectbox("Selecione o serviço:", list(opcoes.keys()), key="sel_gerenciar")
servico_id = opcoes[escolha]

presencas = listar_presenca(servico_id)

if presencas:
    for p in presencas:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{p['nome']}** — {p['funcao']} ({p.get('genero', '—')})")
        with col2:
            if st.button("🗑️", key=f"del_{p['id']}", help="Excluir este registro"):
                deletar_presenca(p['id'])
                st.success(f"{p['nome']} removido!")
                st.rerun()
else:
    st.info("Nenhuma presença registrada neste serviço.")

st.markdown("---")

# ── Excluir serviço inteiro ────────────────────────────────────────────────────
st.subheader("⚠️ Excluir serviço inteiro")
st.warning("Atenção: excluir um serviço remove **todas** as presenças vinculadas a ele!")

opcoes2 = {f"{s['data']} - {s['tipo']} ({s.get('local', '') or 'Sem local'})": s['id'] for s in servicos}
escolha2 = st.selectbox("Selecione o serviço para excluir:", list(opcoes2.keys()), key="sel_del_srv")
servico_del_id = opcoes2[escolha2]

confirmar = st.checkbox("Confirmo que desejo excluir este serviço e todas as presenças vinculadas.")
if st.button("🗑️ Excluir Serviço", type="primary", use_container_width=True):
    if confirmar:
        deletar_servico(servico_del_id)
        st.success("Serviço excluído com sucesso!")
        st.rerun()
    else:
        st.error("Marque a caixa de confirmação antes de excluir.")
