import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from datetime import datetime
from utils.supabase_client import listar_servicos, listar_presenca, contar_por_funcao

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="centered", initial_sidebar_state="collapsed")

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
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px; padding: 20px 28px;
        text-align: center; margin-bottom: 24px; backdrop-filter: blur(10px);
    }
    .page-header h2 { color: #fff; margin: 0 0 4px; font-size: 1.5rem; font-weight: 800; }
    .page-header p  { color: rgba(255,255,255,0.4); margin: 0; font-size: 0.85rem; }

    .metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 16px 0; }
    .metric-card {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 18px 12px; text-align: center;
    }
    .metric-card .num { font-size: 2rem; font-weight: 800; line-height: 1; }
    .metric-card .lbl { font-size: 0.75rem; color: rgba(255,255,255,0.45); margin-top: 5px; }
    .metric-card.blue  .num { color: #60a5fa; }
    .metric-card.purple .num { color: #a78bfa; }
    .metric-card.green  .num { color: #34d399; }
    .metric-card.gold   .num { color: #fbbf24; }

    .section-title {
        color: rgba(255,255,255,0.85); font-size: 0.8rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 24px 0 12px; padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .stSelectbox > div > div { background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.12) !important; border-radius: 10px !important; color: #fff !important; }
    label { color: rgba(255,255,255,0.7) !important; }

    /* Export buttons row */
    .export-row { display: flex; gap: 12px; margin-top: 8px; }

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
        box-shadow: 0 8px 28px rgba(59,130,246,0.5) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    div.stButton:first-child > button {
        background: rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: none !important; font-size: 0.85rem !important;
        padding: 10px 16px !important; width: auto !important;
    }
    div.stButton:first-child > button:hover {
        background: rgba(255,255,255,0.12) !important;
        transform: translateY(-1px) !important; box-shadow: none !important;
    }
    .stDownloadButton > button {
        background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 13px 20px !important;
        font-size: 0.9rem !important; font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(5,150,105,0.3) !important;
        transition: all 0.25s cubic-bezier(0.34,1.56,0.64,1) !important;
    }
    .stDownloadButton > button:hover {
        box-shadow: 0 8px 24px rgba(5,150,105,0.5) !important;
        transform: translateY(-2px) scale(1.01) !important;
    }
    hr { border-color: rgba(255,255,255,0.08) !important; }
    .stAlert { border-radius: 12px !important; }
    /* Tabela */
    .stDataFrame { border-radius: 12px !important; overflow: hidden; }
</style>
"""
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

if st.button("← Voltar"):
    st.switch_page("app.py")

st.markdown("""
<div class="page-header">
    <h2>📊 Relatórios</h2>
    <p>Visualize dados e exporte relatórios do serviço</p>
</div>
""", unsafe_allow_html=True)

# ── Selecionar serviço ────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Selecione o serviço</div>', unsafe_allow_html=True)
servicos = listar_servicos()
if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s for s in servicos}
escolha = st.selectbox("Serviço:", list(opcoes.keys()))
servico = opcoes[escolha]
servico_id = servico['id']

# ── Métricas ──────────────────────────────────────────────────────────────────
contagem = contar_por_funcao(servico_id)
total    = sum(contagem.values())
presencas = listar_presenca(servico_id)

st.markdown('<div class="section-title">Contagem</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card blue"><div class="num">{contagem['Músico']}</div><div class="lbl">🎵 Músicos</div></div>
    <div class="metric-card purple"><div class="num">{contagem['Organista']}</div><div class="lbl">🎹 Organistas</div></div>
    <div class="metric-card green"><div class="num">{contagem['Irmandade']}</div><div class="lbl">🙏 Irmandade</div></div>
    <div class="metric-card gold"><div class="num">{total}</div><div class="lbl">👥 Total</div></div>
</div>
""", unsafe_allow_html=True)

# ── Gráfico ───────────────────────────────────────────────────────────────────
if total > 0:
    st.markdown('<div class="section-title">Gráfico de distribuição</div>', unsafe_allow_html=True)
    df_chart = pd.DataFrame([
        {"Função": k, "Quantidade": v} for k, v in contagem.items() if v > 0
    ])
    fig = px.bar(
        df_chart, x="Função", y="Quantidade",
        color="Função",
        color_discrete_map={"Músico": "#60a5fa", "Organista": "#a78bfa", "Irmandade": "#34d399"},
        text="Quantidade"
    )
    fig.update_traces(textfont_size=16, textfont_color="white", marker_line_width=0)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.03)",
        font_color="rgba(255,255,255,0.7)",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)", zeroline=False),
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
    )
    st.plotly_chart(fig, use_container_width=True)

# ── Lista ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Lista completa</div>', unsafe_allow_html=True)
if presencas:
    df = pd.DataFrame(presencas)
    df_show = df[["nome", "funcao", "genero"]].rename(
        columns={"nome": "Nome", "funcao": "Função", "genero": "Gênero"}
    )
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma presença registrada neste serviço.")
    st.stop()

# ── Exportações ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Exportar</div>', unsafe_allow_html=True)

col_csv, col_pdf = st.columns(2)

# CSV
with col_csv:
    csv_bytes = df_show.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv_bytes,
        file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ','_')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# PDF
with col_pdf:
    musicos_list  = [p for p in presencas if p['funcao'] == 'Músico']
    organistas_list = [p for p in presencas if p['funcao'] == 'Organista']
    irmandade_list  = [p for p in presencas if p['funcao'] == 'Irmandade']

    def make_rows(items, badge_color, badge_bg):
        if not items:
            return '<tr><td colspan="3" style="text-align:center;color:#94a3b8;padding:12px;font-style:italic">Nenhum registrado</td></tr>'
        rows = ""
        for i, p in enumerate(items):
            bg = "#f8fafc" if i % 2 == 0 else "#ffffff"
            rows += f"""
            <tr style="background:{bg}">
                <td style="padding:10px 14px;border-bottom:1px solid #e2e8f0;color:#1e293b;font-weight:500">{p['nome']}</td>
                <td style="padding:10px 14px;border-bottom:1px solid #e2e8f0;text-align:center">
                    <span style="background:{badge_bg};color:{badge_color};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700">{p['funcao']}</span>
                </td>
                <td style="padding:10px 14px;border-bottom:1px solid #e2e8f0;color:#64748b;text-align:center">{p.get('genero','—')}</td>
            </tr>"""
        return rows

    gerado_em = datetime.now().strftime("%d/%m/%Y às %H:%M")
    local_txt  = servico.get('local') or '—'
    obs_txt    = servico.get('obs') or ''

    html_pdf = f"""
    <!DOCTYPE html><html lang="pt-BR"><head>
    <meta charset="UTF-8">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
      * {{ box-sizing:border-box; margin:0; padding:0; font-family:'Inter',sans-serif; }}
      body {{ background:#ffffff; color:#1e293b; padding:0; }}

      /* CAPA / HEADER */
      .cover {{
        background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 60%, #7c3aed 100%);
        padding: 52px 48px 44px;
        color: white;
        position: relative;
        overflow: hidden;
      }}
      .cover::before {{
        content: '';
        position: absolute; top: -60px; right: -60px;
        width: 260px; height: 260px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
      }}
      .cover::after {{
        content: '';
        position: absolute; bottom: -80px; left: 30px;
        width: 200px; height: 200px;
        background: rgba(255,255,255,0.04);
        border-radius: 50%;
      }}
      .cover-logo {{
        width: 56px; height: 56px;
        background: rgba(255,255,255,0.15);
        border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
        font-size: 28px; margin-bottom: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
      }}
      .cover h1 {{ font-size: 28px; font-weight: 800; letter-spacing: -0.5px; margin-bottom: 6px; }}
      .cover .subtitle {{ font-size: 13px; opacity: 0.65; margin-bottom: 28px; }}
      .cover-meta {{
        display: flex; gap: 24px; flex-wrap: wrap;
        background: rgba(0,0,0,0.15); border-radius: 14px;
        padding: 16px 20px; margin-top: 4px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.1);
      }}
      .cover-meta-item {{ }}
      .cover-meta-item .meta-label {{ font-size: 10px; opacity: 0.55; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 3px; }}
      .cover-meta-item .meta-val   {{ font-size: 14px; font-weight: 700; }}

      /* MÉTRICAS */
      .metrics {{
        display: grid; grid-template-columns: repeat(4,1fr);
        gap: 0; border-bottom: 1px solid #e2e8f0;
      }}
      .metric-box {{
        padding: 24px 20px; text-align: center;
        border-right: 1px solid #e2e8f0;
      }}
      .metric-box:last-child {{ border-right: none; }}
      .metric-box .m-num {{ font-size: 36px; font-weight: 800; line-height: 1; }}
      .metric-box .m-lbl {{ font-size: 11px; color: #94a3b8; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; }}
      .metric-box.blue   .m-num {{ color: #2563eb; }}
      .metric-box.purple .m-num {{ color: #7c3aed; }}
      .metric-box.green  .m-num {{ color: #059669; }}
      .metric-box.slate  .m-num {{ color: #334155; }}

      /* CONTENT */
      .content {{ padding: 32px 48px; }}
      .section-hdr {{
        display: flex; align-items: center; gap: 10px;
        margin: 28px 0 14px; padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
      }}
      .section-hdr .dot {{
        width: 10px; height: 10px; border-radius: 50%;
      }}
      .section-hdr h3 {{ font-size: 14px; font-weight: 700; color: #1e293b; text-transform: uppercase; letter-spacing: 0.8px; }}
      .section-hdr .count {{
        margin-left: auto;
        font-size: 12px; font-weight: 700;
        padding: 3px 10px; border-radius: 20px;
      }}

      table {{ width: 100%; border-collapse: collapse; }}
      thead th {{
        padding: 10px 14px; text-align: left;
        font-size: 11px; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.8px;
        color: #64748b; background: #f8fafc;
        border-bottom: 2px solid #e2e8f0;
      }}
      thead th:nth-child(2), thead th:nth-child(3) {{ text-align: center; }}

      /* FOOTER */
      .pdf-footer {{
        margin: 40px 0 0;
        padding: 0 48px 40px;
      }}
      .pdf-footer-inner {{
        background: linear-gradient(135deg, #f8fafc, #eff6ff);
        border: 1px solid #dbeafe;
        border-radius: 16px;
        padding: 24px 28px;
        display: flex; align-items: center; gap: 20px;
      }}
      .pdf-footer-logo {{
        width: 48px; height: 48px;
        background: linear-gradient(135deg, #2563eb, #7c3aed);
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 22px; flex-shrink: 0;
      }}
      .pdf-footer-text h4 {{ font-size: 14px; font-weight: 700; color: #1e3a5f; margin-bottom: 3px; }}
      .pdf-footer-text p  {{ font-size: 11px; color: #64748b; }}
      .pdf-footer-stamp {{
        margin-left: auto; text-align: right;
        font-size: 10px; color: #94a3b8;
      }}
      .pdf-footer-stamp strong {{ display: block; font-size: 11px; color: #475569; }}
    </style>
    </head><body>

    <!-- CAPA -->
    <div class="cover">
      <div class="cover-logo">🎵</div>
      <h1>Relatório de Presença</h1>
      <div class="subtitle">Congregação Cristã no Brasil</div>
      <div class="cover-meta">
        <div class="cover-meta-item">
          <div class="meta-label">Data do Serviço</div>
          <div class="meta-val">{servico['data']}</div>
        </div>
        <div class="cover-meta-item">
          <div class="meta-label">Tipo</div>
          <div class="meta-val">{servico['tipo']}</div>
        </div>
        <div class="cover-meta-item">
          <div class="meta-label">Local</div>
          <div class="meta-val">{local_txt}</div>
        </div>
        <div class="cover-meta-item">
          <div class="meta-label">Total Presentes</div>
          <div class="meta-val">{total} pessoas</div>
        </div>
      </div>
    </div>

    <!-- MÉTRICAS -->
    <div class="metrics">
      <div class="metric-box blue"><div class="m-num">{contagem['Músico']}</div><div class="m-lbl">🎵 Músicos</div></div>
      <div class="metric-box purple"><div class="m-num">{contagem['Organista']}</div><div class="m-lbl">🎹 Organistas</div></div>
      <div class="metric-box green"><div class="m-num">{contagem['Irmandade']}</div><div class="m-lbl">🙏 Irmandade</div></div>
      <div class="metric-box slate"><div class="m-num">{total}</div><div class="m-lbl">👥 Total</div></div>
    </div>

    <!-- LISTAS -->
    <div class="content">

      <!-- Músicos -->
      <div class="section-hdr">
        <div class="dot" style="background:#2563eb"></div>
        <h3>Músicos</h3>
        <span class="count" style="background:#dbeafe;color:#1d4ed8">{contagem['Músico']}</span>
      </div>
      <table>
        <thead><tr><th>Nome</th><th>Função</th><th>Gênero</th></tr></thead>
        <tbody>{make_rows(musicos_list,'#1d4ed8','#dbeafe')}</tbody>
      </table>

      <!-- Organistas -->
      <div class="section-hdr">
        <div class="dot" style="background:#7c3aed"></div>
        <h3>Organistas</h3>
        <span class="count" style="background:#ede9fe;color:#5b21b6">{contagem['Organista']}</span>
      </div>
      <table>
        <thead><tr><th>Nome</th><th>Função</th><th>Gênero</th></tr></thead>
        <tbody>{make_rows(organistas_list,'#5b21b6','#ede9fe')}</tbody>
      </table>

      <!-- Irmandade -->
      <div class="section-hdr">
        <div class="dot" style="background:#059669"></div>
        <h3>Irmandade</h3>
        <span class="count" style="background:#d1fae5;color:#065f46">{contagem['Irmandade']}</span>
      </div>
      <table>
        <thead><tr><th>Nome</th><th>Função</th><th>Gênero</th></tr></thead>
        <tbody>{make_rows(irmandade_list,'#065f46','#d1fae5')}</tbody>
      </table>

    </div>

    <!-- FOOTER PREMIUM -->
    <div class="pdf-footer">
      <div class="pdf-footer-inner">
        <div class="pdf-footer-logo">✝️</div>
        <div class="pdf-footer-text">
          <h4>Congregação Cristã no Brasil</h4>
          <p>Relatório gerado automaticamente pelo Sistema de Presença CCB</p>
        </div>
        <div class="pdf-footer-stamp">
          <strong>Gerado em</strong>
          {gerado_em}
        </div>
      </div>
    </div>

    </body></html>
    """

    pdf_b64 = base64.b64encode(html_pdf.encode("utf-8")).decode()
    nome_pdf = f"presenca_{servico['data']}_{servico['tipo'].replace(' ','_')}.html"

    st.download_button(
        label="📄 Exportar PDF",
        data=html_pdf.encode("utf-8"),
        file_name=nome_pdf,
        mime="text/html",
        use_container_width=True,
        help="Abre no navegador → use Ctrl+P / Imprimir → Salvar como PDF"
    )

st.markdown('<div style="color:rgba(255,255,255,0.25);font-size:0.72rem;text-align:center;margin-top:20px">💡 Para o PDF: abra o arquivo no navegador e use Ctrl+P → Salvar como PDF</div>', unsafe_allow_html=True)
