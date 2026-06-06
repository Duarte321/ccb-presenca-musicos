import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from io import BytesIO
from utils.supabase_client import listar_servicos, listar_presenca, contar_por_funcao

st.set_page_config(page_title="Relatórios", page_icon="📊", layout="centered", initial_sidebar_state="collapsed")

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif !important; }
    [data-testid="stSidebar"]        { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    [data-testid="stHeader"]         { display: none !important; }
    [data-testid="stToolbar"]        { display: none !important; }
    [data-testid="stDecoration"]     { display: none !important; }
    .stApp > header                  { display: none !important; }
    footer { visibility: hidden; } #MainMenu { visibility: hidden; }
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMain"], .main, .block-container {
        background: linear-gradient(135deg, #0f1923 0%, #1a2d45 50%, #0f1923 100%) !important;
    }
    .block-container { padding-top: 1.5rem !important; max-width: 860px !important; }

    .page-header {
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px; padding: 20px 28px;
        text-align: center; margin-bottom: 24px; backdrop-filter: blur(10px);
    }
    .page-header h2 { color: #fff !important; margin: 0 0 4px; font-size: 1.5rem; font-weight: 800; }
    .page-header p  { color: rgba(255,255,255,0.4) !important; margin: 0; font-size: 0.85rem; }

    .metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 12px; margin: 16px 0; }
    .metric-card {
        background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px; padding: 18px 12px; text-align: center;
    }
    .metric-card .num { font-size: 2rem; font-weight: 800; line-height: 1; }
    .metric-card .lbl { font-size: 0.75rem; color: rgba(255,255,255,0.45) !important; margin-top: 5px; }
    .metric-card.blue   .num { color: #60a5fa !important; }
    .metric-card.purple .num { color: #a78bfa !important; }
    .metric-card.green  .num { color: #34d399 !important; }
    .metric-card.gold   .num { color: #fbbf24 !important; }

    .section-title {
        color: rgba(255,255,255,0.85) !important; font-size: 0.8rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 1.5px;
        margin: 24px 0 12px; padding-bottom: 8px;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* ── INPUTS CORRIGIDOS ── */
    .stSelectbox > div > div { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important; }
    .stSelectbox > div > div > div[data-baseweb="select"] > div { background: transparent !important; color: #f1f5f9 !important; }
    .stSelectbox span, .stSelectbox div { color: #f1f5f9 !important; }
    [data-baseweb="select"] * { color: #f1f5f9 !important; background: transparent !important; }
    [data-baseweb="popover"] [role="option"] { background: #1a2d45 !important; color: #f1f5f9 !important; }
    [data-baseweb="popover"] [role="option"]:hover { background: #2a3d55 !important; }
    .stTextInput input { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important; color: #f1f5f9 !important; caret-color: #60a5fa !important; }
    .stTextInput input::placeholder { color: rgba(255,255,255,0.3) !important; }
    .stTextInput input:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important; }
    .stDateInput input { background: rgba(255,255,255,0.08) !important; border: 1px solid rgba(255,255,255,0.18) !important; border-radius: 10px !important; color: #f1f5f9 !important; }
    label { color: rgba(255,255,255,0.75) !important; }
    p { color: rgba(255,255,255,0.75) !important; }

    /* ── BOTÃO VOLTAR ── */
    div.stButton:first-of-type > button {
        background: rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.8) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        box-shadow: none !important; font-size: 0.85rem !important;
        padding: 10px 18px !important; width: auto !important;
        border-radius: 12px !important;
    }
    div.stButton:first-of-type > button:hover {
        background: rgba(255,255,255,0.12) !important;
        transform: translateY(-1px) !important;
    }

    /* ── BOTÃO CSV (verde) ── */
    .stDownloadButton:nth-of-type(1) > button,
    .csv-btn > div > div > button,
    [data-testid="stDownloadButton"]:first-of-type button {
        background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 14px 20px !important;
        font-size: 0.93rem !important; font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(5,150,105,0.35) !important;
        transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
        letter-spacing: 0.3px !important;
    }
    .stDownloadButton:nth-of-type(1) > button:hover { box-shadow: 0 8px 28px rgba(5,150,105,0.55) !important; transform: translateY(-3px) scale(1.02) !important; }
    .stDownloadButton:nth-of-type(1) > button:active { transform: translateY(0) scale(0.98) !important; box-shadow: 0 2px 10px rgba(5,150,105,0.3) !important; }

    /* ── BOTÃO PDF (vermelho/âmbar) ── */
    .stDownloadButton button {
        background: linear-gradient(135deg, #dc2626 0%, #ea580c 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 14px 20px !important;
        font-size: 0.93rem !important; font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 20px rgba(220,38,38,0.35) !important;
        transition: all 0.22s cubic-bezier(0.34,1.56,0.64,1) !important;
        letter-spacing: 0.3px !important;
    }
    .stDownloadButton button:hover { box-shadow: 0 8px 28px rgba(220,38,38,0.55) !important; transform: translateY(-3px) scale(1.02) !important; }
    .stDownloadButton button:active { transform: translateY(0) scale(0.98) !important; box-shadow: 0 2px 10px rgba(220,38,38,0.3) !important; }

    hr { border-color: rgba(255,255,255,0.08) !important; }
    .stAlert { border-radius: 12px !important; }
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

st.markdown('<div class="section-title">Selecione o serviço</div>', unsafe_allow_html=True)
servicos = listar_servicos()
if not servicos:
    st.warning("Nenhum serviço cadastrado ainda.")
    st.stop()

opcoes = {f"{s['data']} — {s['tipo']} | {s.get('local','') or 'Sem local'}": s for s in servicos}
escolha = st.selectbox("Serviço:", list(opcoes.keys()))
servico = opcoes[escolha]
servico_id = servico['id']

contagem  = contar_por_funcao(servico_id)
total     = sum(contagem.values())
presencas = listar_presenca(servico_id)

st.markdown('<div class="section-title">Contagem</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card blue">  <div class="num">{contagem['Músico']}</div>   <div class="lbl">🎵 Músicos</div></div>
    <div class="metric-card purple"><div class="num">{contagem['Organista']}</div> <div class="lbl">🎹 Organistas</div></div>
    <div class="metric-card green"> <div class="num">{contagem['Irmandade']}</div><div class="lbl">🙏 Irmandade</div></div>
    <div class="metric-card gold">  <div class="num">{total}</div>               <div class="lbl">👥 Total</div></div>
</div>""", unsafe_allow_html=True)

if total > 0:
    st.markdown('<div class="section-title">Gráfico de distribuição</div>', unsafe_allow_html=True)
    df_chart = pd.DataFrame([{"Função": k, "Quantidade": v} for k, v in contagem.items() if v > 0])
    fig = px.pie(
        df_chart, names="Função", values="Quantidade",
        color="Função",
        color_discrete_map={"Músico": "#60a5fa", "Organista": "#a78bfa", "Irmandade": "#34d399"},
        hole=0.45,
    )
    fig.update_traces(
        textposition="outside",
        textinfo="label+percent+value",
        textfont=dict(size=14, color="rgba(255,255,255,0.85)"),
        marker=dict(line=dict(color="rgba(0,0,0,0.3)", width=2)),
        pull=[0.04] * len(df_chart),
        hovertemplate="<b>%{label}</b><br>Quantidade: %{value}<br>%{percent}<extra></extra>"
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="rgba(255,255,255,0.7)",
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5,
            font=dict(color="rgba(255,255,255,0.75)", size=13),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(l=20, r=20, t=20, b=20),
        height=340,
        annotations=[dict(
            text=f"<b>{total}</b><br><span style='font-size:10px'>Total</span>",
            x=0.5, y=0.5, font_size=20, font_color="white", showarrow=False
        )]
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="section-title">Lista completa</div>', unsafe_allow_html=True)
if presencas:
    df = pd.DataFrame(presencas)
    df_show = df[["nome","funcao","genero"]].rename(columns={"nome":"Nome","funcao":"Função","genero":"Gênero"})
    st.dataframe(df_show, use_container_width=True, hide_index=True)
else:
    st.info("Nenhuma presença registrada neste serviço.")
    st.stop()

st.markdown('<div class="section-title">Exportar</div>', unsafe_allow_html=True)
col_csv, col_pdf = st.columns(2)

with col_csv:
    csv_bytes = df_show.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="⬇️ Exportar CSV",
        data=csv_bytes,
        file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ','_')}.csv",
        mime="text/csv",
        use_container_width=True
    )

with col_pdf:
    musicos_list    = [p for p in presencas if p['funcao'] == 'Músico']
    organistas_list = [p for p in presencas if p['funcao'] == 'Organista']
    irmandade_list  = [p for p in presencas if p['funcao'] == 'Irmandade']
    gerado_em = datetime.now().strftime("%d/%m/%Y às %H:%M")
    local_txt = servico.get('local') or '—'

    try:
        from fpdf import FPDF
        import unicodedata

        def limpar(texto):
            if not texto:
                return ''
            return unicodedata.normalize('NFKD', str(texto)).encode('latin-1', 'ignore').decode('latin-1')

        class PDF(FPDF):
            def header(self):
                self.set_fill_color(30, 58, 95)
                self.rect(0, 0, 210, 42, 'F')
                self.set_fill_color(37, 99, 235)
                self.rect(0, 0, 140, 42, 'F')
                self.set_font('Arial', 'B', 18)
                self.set_text_color(255, 255, 255)
                self.set_xy(14, 8)
                self.cell(0, 10, limpar('Relatório de Presença'), ln=True)
                self.set_font('Arial', '', 10)
                self.set_text_color(180, 200, 255)
                self.set_x(14)
                self.cell(0, 6, limpar('Congregação Cristã no Brasil'), ln=True)
                self.set_text_color(255, 255, 255)
                self.set_font('Arial', '', 9)
                self.set_x(14)
                self.cell(0, 6, limpar(f'Data: {servico["data"]}   |   Tipo: {servico["tipo"]}   |   Local: {local_txt}   |   Total: {total} pessoas'), ln=True)
                self.ln(6)

            def footer(self):
                self.set_y(-18)
                self.set_fill_color(240, 245, 255)
                self.rect(0, self.get_y(), 210, 20, 'F')
                self.set_font('Arial', '', 8)
                self.set_text_color(100, 116, 139)
                self.cell(0, 6, limpar(f'Congregação Cristã no Brasil  |  Sistema de Presença CCB  |  Gerado em: {gerado_em}'), align='C', ln=True)
                self.set_text_color(148, 163, 184)
                self.cell(0, 4, limpar(f'Página {self.page_no()}'), align='C')

        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=22)
        pdf.add_page()

        # ── Bloco métricas ──
        pdf.set_y(48)
        boxes = [
            (contagem['Músico'],    'Músicos',    (96, 165, 250),  (219, 234, 254)),
            (contagem['Organista'], 'Organistas', (167, 139, 250), (237, 233, 254)),
            (contagem['Irmandade'], 'Irmandade',  (52, 211, 153),  (209, 250, 229)),
            (total,                 'Total',      (51, 65, 85),    (248, 250, 252)),
        ]
        box_w = 44
        start_x = 14
        for i, (num, lbl, cor_num, cor_bg) in enumerate(boxes):
            x = start_x + i * (box_w + 4)
            pdf.set_fill_color(*cor_bg)
            pdf.set_draw_color(220, 220, 230)
            pdf.rect(x, pdf.get_y(), box_w, 22, 'FD')
            pdf.set_font('Arial', 'B', 20)
            pdf.set_text_color(*cor_num)
            pdf.set_xy(x, pdf.get_y() + 2)
            pdf.cell(box_w, 10, str(num), align='C', ln=False)
            pdf.set_font('Arial', '', 8)
            pdf.set_text_color(100, 116, 139)
            pdf.set_xy(x, pdf.get_y() + 10)
            pdf.cell(box_w, 8, limpar(lbl), align='C', ln=False)
        pdf.ln(30)

        def draw_section(titulo, itens, cor_dot, cor_badge_bg, cor_badge_txt):
            pdf.set_font('Arial', 'B', 10)
            pdf.set_text_color(*cor_dot)
            pdf.set_fill_color(*cor_dot)
            pdf.circle(pdf.get_x(), pdf.get_y() + 2.5, 2.5, 'F')
            pdf.set_x(pdf.get_x() + 6)
            pdf.set_text_color(30, 41, 59)
            pdf.cell(0, 8, limpar(titulo.upper()), ln=True)

            pdf.set_draw_color(226, 232, 240)
            pdf.line(14, pdf.get_y(), 196, pdf.get_y())
            pdf.ln(2)

            if not itens:
                pdf.set_font('Arial', 'I', 9)
                pdf.set_text_color(148, 163, 184)
                pdf.cell(0, 8, limpar('Nenhum registrado'), ln=True)
                pdf.ln(3)
                return

            # Cabeçalho tabela
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(226, 232, 240)
            pdf.set_font('Arial', 'B', 8)
            pdf.set_text_color(100, 116, 139)
            pdf.cell(100, 8, 'NOME', border='B', fill=True)
            pdf.cell(40,  8, 'FUNÇÃO', border='B', fill=True, align='C')
            pdf.cell(40,  8, 'GÊNERO', border='B', fill=True, align='C', ln=True)

            for idx, p in enumerate(itens):
                bg = (248, 250, 252) if idx % 2 == 0 else (255, 255, 255)
                pdf.set_fill_color(*bg)
                pdf.set_text_color(30, 41, 59)
                pdf.set_font('Arial', 'B', 9)
                pdf.cell(100, 8, limpar(p['nome']), border='B', fill=True)

                # Badge função
                pdf.set_fill_color(*cor_badge_bg)
                pdf.set_text_color(*cor_badge_txt)
                pdf.set_font('Arial', 'B', 8)
                cx = pdf.get_x()
                cy = pdf.get_y()
                pdf.set_xy(cx + 5, cy + 1)
                pdf.cell(30, 6, limpar(p['funcao']), align='C', fill=True, border=0)
                pdf.set_xy(cx + 40, cy)

                pdf.set_fill_color(*bg)
                pdf.set_text_color(100, 116, 139)
                pdf.set_font('Arial', '', 8)
                pdf.cell(40, 8, limpar(p.get('genero') or '—'), border='B', fill=True, align='C', ln=True)

            pdf.ln(6)

        draw_section('Músicos',    musicos_list,    (37, 99, 235),  (219, 234, 254), (29, 78, 216))
        draw_section('Organistas', organistas_list, (124, 58, 237), (237, 233, 254), (91, 33, 182))
        draw_section('Irmandade',  irmandade_list,  (5, 150, 105),  (209, 250, 229), (6, 95, 70))

        pdf_bytes = bytes(pdf.output())
        st.download_button(
            label="📄 Exportar PDF",
            data=pdf_bytes,
            file_name=f"presenca_{servico['data']}_{servico['tipo'].replace(' ','_')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except ImportError:
        st.error("❌ Instale fpdf2: adicione 'fpdf2' ao requirements.txt")
