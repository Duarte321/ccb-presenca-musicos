from supabase import create_client, Client
import streamlit as st


@st.cache_resource
def get_client() -> Client:
    """Retorna o cliente Supabase (singleton com cache)."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


# ── Serviços ──────────────────────────────────────────────────────────────────

def listar_servicos():
    supabase = get_client()
    response = (
        supabase.table("servicos")
        .select("*")
        .order("data", desc=True)
        .execute()
    )
    return response.data


def criar_servico(data: str, tipo: str, local: str = "", observacao: str = ""):
    supabase = get_client()
    response = (
        supabase.table("servicos")
        .insert({"data": data, "tipo": tipo, "local": local, "observacao": observacao})
        .execute()
    )
    return response.data


def deletar_servico(servico_id: str):
    supabase = get_client()
    supabase.table("servicos").delete().eq("id", servico_id).execute()


# ── Presença ──────────────────────────────────────────────────────────────────

def registrar_presenca(servico_id: str, nome: str, funcao: str, genero: str = None, observacao: str = ""):
    supabase = get_client()
    payload = {
        "servico_id": servico_id,
        "nome": nome,
        "funcao": funcao,
        "observacao": observacao,
    }
    if genero:
        payload["genero"] = genero
    response = supabase.table("presenca").insert(payload).execute()
    return response.data


def listar_presenca(servico_id: str):
    supabase = get_client()
    response = (
        supabase.table("presenca")
        .select("*")
        .eq("servico_id", servico_id)
        .order("registrado_em")
        .execute()
    )
    return response.data


def listar_presenca_todos():
    supabase = get_client()
    response = (
        supabase.table("presenca")
        .select("*, servicos(data, tipo, local)")
        .order("registrado_em", desc=True)
        .execute()
    )
    return response.data


def deletar_presenca(presenca_id: str):
    supabase = get_client()
    supabase.table("presenca").delete().eq("id", presenca_id).execute()


def contar_por_funcao(servico_id: str):
    registros = listar_presenca(servico_id)
    contagem = {"Músico": 0, "Organista": 0, "Irmandade": 0}
    for r in registros:
        funcao = r.get("funcao")
        if funcao in contagem:
            contagem[funcao] += 1
    return contagem
