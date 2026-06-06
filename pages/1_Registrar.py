import streamlit as st
from datetime import date
from utils.supabase_client import (
    listar_servicos, criar_servico, registrar_presenca,
    listar_presenca, contar_por_funcao
)

st.set_page_config(page_title="Registrar Presença", page_icon="📋", layout="centered")
st.title("📋 Registrar Presença")

# ── Selecionar ou criar serviço ────────────────────────────────────────────────
st.subheader("1. Selecione ou crie um serviço")

servicos = listar_servicos()
opcoes = {f"{s['data']} - {s['tipo']} ({s.get('local', '') or 'Sem local'})": s['id'] for s in servicos}

aba = st.radio("Serviço:", ["Selecionar existente", "Criar novo serviço"], horizontal=True)

servico_id = None

if aba == "Selecionar existente":
    if opcoes:
        escolha = st.selectbox("Escolha o serviço:", list(opcoes.keys()))
        servico_id = opcoes[escolha]
    else:
        st.warning("Nenhum serviço cadastrado. Crie um novo abaixo.")
else:
    with st.form("form_servico"):
        col1, col2 = st.columns(2)
        with col1:
            data_srv = st.date_input("Data do serviço:", value=date.today())
        with col2:
            tipo_srv = st.selectbox("Tipo:", [
                "Culto de Semana",
                "Culto de Sábado",
                "Culto de Domingo",
                "Reunião de Oração",
                "Reunião de Jovens",
                "Outro"
            ])
        local_srv = st.text_input("Local (opcional):")
        obs_srv = st.text_input("Observação (opcional):")
        salvar = st.form_submit_button("✅ Criar Serviço", use_container_width=True)
        if salvar:
            resultado = criar_servico(str(data_srv), tipo_srv, local_srv, obs_srv)
            if resultado:
                servico_id = resultado[0]['id']
                st.success(f"Serviço criado com sucesso! ID: {servico_id}")
                st.rerun()

st.markdown("---")

# ── Registrar presença ─────────────────────────────────────────────────────────
if servico_id:
    st.subheader("2. Registrar presença")

    contagem = contar_por_funcao(servico_id)
    c1, c2, c3 = st.columns(3)
    c1.metric("🎵 Músicos", contagem['Músico'])
    c2.metric("🎹 Organistas", contagem['Organista'])
    c3.metric("🙏 Irmandade", contagem['Irmandade'])

    st.markdown("")

    with st.form("form_presenca", clear_on_submit=True):
        nome = st.text_input("Nome completo:", placeholder="Ex: João da Silva")
        col1, col2 = st.columns(2)
        with col1:
            funcao = st.selectbox("Função:", ["Músico", "Organista", "Irmandade"])
        with col2:
            genero = st.selectbox("Gênero:", ["Irmão", "Irmã"])
        obs = st.text_input("Observação (opcional):")
        registrar = st.form_submit_button("➕ Registrar Presença", use_container_width=True)

        if registrar:
            if nome.strip() == "":
                st.error("Por favor, informe o nome.")
            else:
                registrar_presenca(servico_id, nome.strip(), funcao, genero, obs)
                st.success(f"✅ {nome} registrado como {funcao}!")
                st.rerun()

    st.markdown("---")
    st.subheader("📄 Presenças registradas neste serviço")
    presencas = listar_presenca(servico_id)
    if presencas:
        for p in presencas:
            st.write(f"• **{p['nome']}** — {p['funcao']} ({p.get('genero', '—')})")
    else:
        st.info("Nenhuma presença registrada ainda.")
else:
    st.info("Selecione ou crie um serviço para começar a registrar presenças.")
