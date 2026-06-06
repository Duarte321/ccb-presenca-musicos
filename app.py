import streamlit as st

st.set_page_config(
    page_title="CCB - Presença",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("🎵 CCB — Sistema de Presença")
st.markdown(
    """
    Bem-vindo ao sistema de registro de presença da **Congregação Cristã no Brasil**.

    Use o menu lateral para navegar entre as telas:

    | Página | Função |
    |---|---|
    | 📋 **Registrar** | Registrar presença em um serviço |
    | 📊 **Relatórios** | Ver contagens e gráficos por serviço |
    | ⚙️ **Gerenciar** | Editar ou excluir registros |

    ---
    > Desenvolvido para uso interno da CCB.
    """
)

st.info("👈 Selecione uma página no menu lateral para começar.", icon="ℹ️")
