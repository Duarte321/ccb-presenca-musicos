import streamlit as st
import pandas as pd
from datetime import date
from utils.supabase_client import (
    listar_servicos,
    criar_servico,
    registrar_presenca,
    listar_presenca,
    contar_por_funcao,
)

st.set_page_config(page_title="Registrar Presença", page_icon="📋", layout="centered")
st.title("📋 Registrar Presença")

TIPOS_SERVICO = [
    "Culto de Semana",
    "Culto de Sábado",
    "Reunião de Oração",
    "Culto de Domingo",
    "Reunião de Jovens",
    "Outro",
]

# ── Seleção / Criação de Serviço ──────────────────────────────────────────────
st.subheader("1️⃣ Selecione ou crie um serviço")

aba_sel, aba_novo = st.tabs(["Selecionar existente", "Criar novo serviço"])

servico_selecionado = None

with aba_sel:
    servicos = listar_servicos()
    if servicos:
        opcoes = {
            f"{s['data']} — {s['tipo']} {('| ' + s['local']) if s.get('local') else ''}": s
            for s in servicos
        }
        escolha = st.selectbox("Serviço:", list(opcoes.keys()))
        servico_selecionado = opcoes[escolha]
    else:
        st.info("Nenhum serviço cadastrado. Crie um na aba ao lado.")

with aba_novo:
    with st.form("form_novo_servico"):
        col1, col2 = st.columns(2)
        nova_data = col1.date_input("Data:", value=date.today())
        novo_tipo = col2.selectbox("Tipo:", TIPOS_SERVICO)
        novo_local = st.text_input("Local (opcional):")
        nova_obs = st.text_input("Observação (opcional):")
        if st.form_submit_button("✅ Criar serviço", use_container_width=True):
            resultado = criar_servico(
                str(nova_data), novo_tipo, novo_local, nova_obs
            )
            if resultado:
                st.success(f"Serviço '{novo_tipo}' criado para {nova_data}!")
                st.rerun()
            else:
                st.error("Erro ao criar serviço. Verifique as configurações do Supabase.")

st.divider()

# ── Registro de Presença ──────────────────────────────────────────────────────
if servico_selecionado:
    st.subheader("2️⃣ Registrar presença")

    with st.form("form_presenca", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        nome = col1.text_input("Nome do irmão/irmã:", placeholder="Ex: João da Silva")
        funcao = col2.selectbox("Função:", ["Músico", "Organista", "Irmandade"])
        col3, col4 = st.columns([1, 2])
        genero = col3.selectbox("Gênero (opcional):", ["", "Irmão", "Irmã"])
        obs = col4.text_input("Obs. (opcional):")

        submitted = st.form_submit_button("➕ Registrar", use_container_width=True, type="primary")
        if submitted:
            if not nome.strip():
                st.warning("Por favor, informe o nome.")
            else:
                registrar_presenca(
                    servico_selecionado["id"],
                    nome.strip(),
                    funcao,
                    genero if genero else None,
                    obs,
                )
                st.success(f"✅ {nome} registrado como **{funcao}**!")
                st.rerun()

    # ── Contadores ────────────────────────────────────────────────────────────
    st.divider()
    st.subheader("3️⃣ Contagem atual")
    contagem = contar_por_funcao(servico_selecionado["id"])
    total = sum(contagem.values())

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎵 Músicos", contagem["Músico"])
    col2.metric("🎹 Organistas", contagem["Organista"])
    col3.metric("🙏 Irmandade", contagem["Irmandade"])
    col4.metric("👥 Total", total)

    # ── Lista de presentes ────────────────────────────────────────────────────
    st.subheader("📋 Lista de presentes")
    registros = listar_presenca(servico_selecionado["id"])
    if registros:
        df = pd.DataFrame(registros)[["nome", "funcao", "genero", "registrado_em"]]
        df["registrado_em"] = pd.to_datetime(df["registrado_em"]).dt.strftime("%H:%M")
        df.columns = ["Nome", "Função", "Gênero", "Hora"]
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhuma presença registrada ainda neste serviço.")
else:
    st.info("Selecione ou crie um serviço para iniciar o registro.")
