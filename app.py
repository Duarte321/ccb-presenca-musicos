import streamlit as st

st.set_page_config(
    page_title="CCB - Presença Músicos",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🎵 CCB - Presença de Músicos")
st.markdown("""
Bem-vindo ao sistema de controle de presença da **Congregação Cristã no Brasil**.

Utilize o menu lateral para navegar entre as seções:

| Seção | Descrição |
|-------|-----------|
| 📋 **Registrar** | Registrar presença em um serviço |
| 📊 **Relatórios** | Visualizar contagens e gráficos |
| ⚙️ **Gerenciar** | Editar ou excluir registros |
""")

st.info("👈 Selecione uma página no menu lateral para começar.")

st.markdown("---")
st.caption("Sistema desenvolvido para a CCB · Powered by Streamlit + Supabase")
