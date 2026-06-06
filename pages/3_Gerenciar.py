import streamlit as st
import pandas as pd
from utils.supabase_client import (
    listar_servicos,
    deletar_servico,
    listar_presenca,
    deletar_presenca,
)

st.set_page_config(page_title="Gerenciar", page_icon="⚙️", layout="wide")
st.title("⚙️ Gerenciar Registros")

aba_presenca, aba_servicos = st.tabs(["Excluir Presenças", "Excluir Serviços"])

# ── Aba: Excluir Presenças ────────────────────────────────────────────────────
with aba_presenca:
    st.subheader("Remover presença incorreta")
    servicos = listar_servicos()
    if not servicos:
        st.info("Nenhum serviço encontrado.")
    else:
        opcoes = {
            f"{s['data']} — {s['tipo']}": s for s in servicos
        }
        escolha = st.selectbox("Selecione o serviço:", list(opcoes.keys()), key="sel_ger")
        servico = opcoes[escolha]

        registros = listar_presenca(servico["id"])
        if not registros:
            st.info("Nenhuma presença registrada neste serviço.")
        else:
            df = pd.DataFrame(registros)
            df["registrado_em"] = pd.to_datetime(df["registrado_em"]).dt.strftime("%H:%M")

            st.write(f"**{len(df)} presença(s) registrada(s):**")
            for _, row in df.iterrows():
                col1, col2, col3 = st.columns([3, 2, 1])
                col1.write(f"**{row['nome']}**")
                col2.write(f"{row['funcao']} {('— ' + row['genero']) if row.get('genero') else ''}")
                if col3.button("🗑️ Excluir", key=f"del_{row['id']}"):
                    deletar_presenca(row["id"])
                    st.success(f"'{row['nome']}' removido!")
                    st.rerun()

# ── Aba: Excluir Serviços ─────────────────────────────────────────────────────
with aba_servicos:
    st.subheader("Remover serviço")
    st.warning("⚠️ Excluir um serviço remove também **todas as presenças** vinculadas a ele.", icon="⚠️")
    servicos = listar_servicos()
    if not servicos:
        st.info("Nenhum serviço encontrado.")
    else:
        for s in servicos:
            registros = listar_presenca(s["id"])
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.write(f"**{s['data']}** — {s['tipo']}")
            col2.write(f"{len(registros)} presença(s) | {s.get('local', '')}")
            if col3.button("🗑️ Excluir", key=f"delserv_{s['id']}"):
                deletar_servico(s["id"])
                st.success("Serviço excluído com sucesso!")
                st.rerun()
