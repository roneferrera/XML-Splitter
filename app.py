import streamlit as st
import zipfile
import math
import os
import io

# ─────────────────────────────────────────────
#  CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Domínio Sistemas | Divisor de XML",
    page_icon="📂",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  TEMA ESCURO – THOMSON REUTERS / DOMÍNIO
# ─────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
  }
  .stApp {
    background-color: #1A1A1A !important;
  }
  .block-container {
    max-width: 700px !important;
    padding: 2.5rem 2rem 3rem 2rem !important;
  }

  /* ── Header ── */
  .tr-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 6px;
  }
  .tr-logo-dots {
    display: grid;
    grid-template-columns: repeat(4, 8px);
    grid-template-rows: repeat(4, 8px);
    gap: 3px;
  }
  .tr-dot     { width:8px; height:8px; border-radius:50%; background:#FF8000; opacity:0.9; }
  .tr-dot.dim { opacity:0.30; }
  .tr-dot.mid { opacity:0.55; }
  .tr-brand      { display:flex; flex-direction:column; line-height:1.1; }
  .tr-brand-main { font-size:1.3rem; font-weight:700; color:#F0F0F0; letter-spacing:-0.3px; }
  .tr-brand-sub  { font-size:0.72rem; font-weight:400; color:#FF8000; letter-spacing:2px; text-transform:uppercase; }

  .tr-divider {
    height: 2px;
    background: linear-gradient(90deg, #FF8000 0%, #FF800044 60%, transparent 100%);
    margin: 14px 0 28px 0;
    border-radius: 2px;
  }

  /* ── Labels de seção ── */
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #FF8000;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  /* ── Info / Success / Error ── */
  .tr-info {
    background: #1E1E1E;
    border-left: 3px solid #FF8000;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 24px;
    font-size: 0.85rem;
    color: #AAAAAA;
    line-height: 1.8;
  }
  .tr-info strong { color: #F0F0F0; }

  .tr-success {
    background: #1A2A1A;
    border: 1px solid #2A5A2A;
    border-left: 3px solid #4CAF50;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 20px 0;
    font-size: 0.85rem;
    color: #90EE90;
    line-height: 1.9;
  }
  .tr-success strong { color: #AAFFAA; }

  .tr-error {
    background: #2A1A1A;
    border-left: 3px solid #FF4444;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.85rem;
    color: #FF9999;
  }

  /* ── Cards de seleção de lote ── */
  .lote-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 8px;
  }
  .lote-card {
    background: #242424;
    border: 2px solid #333333;
    border-radius: 12px;
    padding: 20px 14px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    user-select: none;
  }
  .lote-card:hover {
    border-color: #FF8000;
    background: #2A2A2A;
    transform: translateY(-2px);
    box-shadow: 0 6px 20px #FF800033;
  }
  .lote-card.selected {
    border-color: #FF8000 !important;
    background: #2A1F10 !important;
    box-shadow: 0 0 0 3px #FF800033, 0 6px 20px #FF800033 !important;
  }
  .lote-card .lote-num {
    font-size: 1.7rem;
    font-weight: 700;
    color: #FF8000;
    line-height: 1;
    margin-bottom: 4px;
  }
  .lote-card .lote-label {
    font-size: 0.7rem;
    color: #666666;
    text-transform: uppercase;
    letter-spacing: 1.2px;
  }
  .lote-card .lote-desc {
    font-size: 0.75rem;
    color: #555555;
    margin-top: 6px;
  }
  .lote-card.selected .lote-label { color: #FF8000AA; }
  .lote-card.selected .lote-desc  { color: #FF800077; }

  /* ── Preview badge ── */
  .preview-bar {
    background: #1E1E1E;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 12px;
    font-size: 0.83rem;
    color: #888888;
  }
  .preview-bar .pv-val {
    color: #FF8000;
    font-weight: 700;
    font-size: 1rem;
  }
  .preview-bar .pv-sep {
    color: #333333;
    margin: 0 4px;
  }

  /* ── Tabela ── */
  .batch-table {
    width: 100%;
    border-collapse: collapse;
    margin: 16px 0 24px 0;
    font-size: 0.82rem;
  }
  .batch-table th {
    background: #2A2A2A;
    color: #FF8000;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid #3A3A3A;
  }
  .batch-table td {
    padding: 9px 14px;
    color: #CCCCCC;
    border-bottom: 1px solid #2A2A2A;
  }
  .batch-table tr:last-child td { border-bottom: none; }
  .batch-table tr:hover td      { background: #242424; }

  .badge {
    display: inline-block;
    background: #FF800022;
    color: #FF8000;
    border: 1px solid #FF800055;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .badge-ok {
    background: #00AA4422 !important;
    color: #4CAF50 !important;
    border-color: #4CAF5055 !important;
  }

  /* ── Radio buttons ocultos (usamos cards customizados) ── */
  div[data-testid="stRadio"] > label          { display: none !important; }
  div[data-testid="stRadio"] > div            { gap: 0 !important; }
  div[data-testid="stRadio"] > div > label    {
    background: #242424 !important;
    border: 2px solid #333333 !important;
    border-radius: 12px !important;
    padding: 18px 14px !important;
    flex: 1 !important;
    text-align: center !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
  }
  div[data-testid="stRadio"] > div > label:hover {
    border-color: #FF8000 !important;
    background: #2A2A2A !important;
  }
  div[data-testid="stRadio"] > div > label[data-selected="true"] {
    border-color: #FF8000 !important;
    background: #2A1F10 !important;
  }
  div[data-testid="stRadio"] > div > label > div > p {
    color: #F0F0F0 !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
  }
  div[data-testid="stRadio"] > div > label > div:first-child {
    display: none !important;
  }

  /* ── File uploader ── */
  [data-testid="stFileUploaderDropzone"] {
    background-color: #242424 !important;
    border: 1.5px dashed #444444 !important;
    border-radius: 10px !important;
  }
  [data-testid="stFileUploaderDropzone"] p   { color: #888888 !important; }
  [data-testid="stFileUploaderDropzone"] svg { fill: #FF8000 !important; }

  /* ── Botão principal ── */
  .stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #FF8000 0%, #E06000 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.3px !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #FF9520 0%, #FF8000 100%) !important;
    box-shadow: 0 4px 20px #FF800055 !important;
    transform: translateY(-1px) !important;
  }

  /* ── Botão de download ── */
  .stDownloadButton > button {
    width: 100% !important;
    background: #242424 !important;
    color: #FF8000 !important;
    border: 1.5px solid #FF8000 !important;
    border-radius: 8px !important;
    padding: 13px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
  }
  .stDownloadButton > button:hover {
    background: #FF800015 !important;
    box-shadow: 0 4px 20px #FF800033 !important;
  }

  /* ── Progress bar ── */
  [data-testid="stProgressBar"] > div {
    background: #333333 !important;
    border-radius: 4px !important;
  }
  [data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #FF8000, #FFB347) !important;
    border-radius: 4px !important;
  }

  /* ── Métricas ── */
  [data-testid="metric-container"] {
    background: #242424 !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
  }
  [data-testid="metric-container"] label {
    color: #888888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
  }
  [data-testid="stMetricValue"] {
    color: #FF8000 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }

  /* ── Esconde padrão Streamlit ── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }

  hr { border-color: #333333 !important; margin: 24px 0 !important; }

  ::-webkit-scrollbar       { width: 6px; }
  ::-webkit-scrollbar-track { background: #1A1A1A; }
  ::-webkit-scrollbar-thumb { background: #444444; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #FF8000; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  OPÇÕES DE LOTE
# ─────────────────────────────────────────────
OPCOES_LOTE = {
    "1.000 XMLs":  1_000,
    "5.000 XMLs":  5_000,
    "10.000 XMLs": 10_000,
}
DESCRICOES_LOTE = {
    "1.000 XMLs":  "Ideal para testes e volumes pequenos",
    "5.000 XMLs":  "Recomendado para uso padrão",
    "10.000 XMLs": "Para volumes grandes e importações em massa",
}


# ─────────────────────────────────────────────
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def ler_xmls_do_zip(file_bytes: bytes) -> list:
    buf = io.BytesIO(file_bytes)
    with zipfile.ZipFile(buf, "r") as z:
        names = z.namelist()
    return sorted([
        n for n in names
        if n.lower().endswith(".xml")
        and "__MACOSX" not in n
        and not os.path.basename(n).startswith(".")
    ])


# ─────────────────────────────────────────────
#  HEADER / LOGO
# ─────────────────────────────────────────────
st.markdown("""
<div class="tr-header">
  <div class="tr-logo-dots">
    <div class="tr-dot dim"></div><div class="tr-dot mid"></div>
    <div class="tr-dot"></div>    <div class="tr-dot mid"></div>
    <div class="tr-dot mid"></div><div class="tr-dot"></div>
    <div class="tr-dot"></div>    <div class="tr-dot"></div>
    <div class="tr-dot"></div>    <div class="tr-dot"></div>
    <div class="tr-dot mid"></div><div class="tr-dot dim"></div>
    <div class="tr-dot mid"></div><div class="tr-dot"></div>
    <div class="tr-dot dim"></div><div class="tr-dot mid"></div>
  </div>
  <div class="tr-brand">
    <span class="tr-brand-main">Dom&iacute;nio Sistemas</span>
    <span class="tr-brand-sub">Thomson Reuters</span>
  </div>
</div>
<div class="tr-divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TÍTULO
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Utilit&aacute;rio de Arquivos</div>', unsafe_allow_html=True)
st.markdown("## Divisor de XMLs em Lotes")
st.markdown(
    "<p style='color:#888888; font-size:0.9rem; margin-top:-10px; margin-bottom:24px;'>"
    "Fa&ccedil;a o upload de um ZIP com seus XMLs, escolha o tamanho do lote e baixe "
    "cada lote j&aacute; compactado individualmente &mdash; pronto para importar no sistema."
    "</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  INFO BOX
# ─────────────────────────────────────────────
st.markdown("""
<div class="tr-info">
  <strong>&#128204; Como funciona</strong><br>
  &bull; Envie um <strong>.zip</strong> contendo os XMLs (pode conter subpastas)<br>
  &bull; Escolha o tamanho do lote: <strong>1.000</strong>, <strong>5.000</strong> ou <strong>10.000</strong> XMLs<br>
  &bull; O sistema gera um ZIP mestre com os lotes j&aacute; zipados individualmente:<br>
  &nbsp;&nbsp;&nbsp;
    <code style="color:#FF8000">lotes_xml.zip</code> &rarr;
    <code style="color:#FF8000">lote_001.zip</code>,
    <code style="color:#FF8000">lote_002.zip</code> ...<br>
  &bull; Cada <code style="color:#FF8000">.zip</code> &eacute; importado diretamente no Dom&iacute;nio<br>
  &bull; Nenhum XML duplicado ou perdido &mdash; divis&atilde;o exata garantida
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  STEP 1 — UPLOAD
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label">1 &mdash; Arquivo de entrada</div>',
    unsafe_allow_html=True,
)
uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo ZIP com os XMLs",
    type=["zip"],
    help="Apenas arquivos .zip são aceitos. Os XMLs podem estar em subpastas.",
)

# ─────────────────────────────────────────────
#  STEP 2 — SELEÇÃO DO LOTE (cards visuais)
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:24px">2 &mdash; Tamanho do lote</div>',
    unsafe_allow_html=True,
)

# Calcula preview se já tiver arquivo
total_xmls_preview = 0
if uploaded_file is not None:
    try:
        total_xmls_preview = len(ler_xmls_do_zip(uploaded_file.getvalue()))
    except Exception:
        total_xmls_preview = 0

# Cards HTML para exibição visual
cards_html = '<div class="lote-grid">'
for label, valor in OPCOES_LOTE.items():
    lotes_est = math.ceil(total_xmls_preview / valor) if total_xmls_preview > 0 else "—"
    est_txt   = f"{lotes_est} lotes" if total_xmls_preview > 0 else "aguardando arquivo"
    cards_html += f"""
    <div class="lote-card" id="card_{valor}">
      <div class="lote-num">{label.replace(' XMLs','')}</div>
      <div class="lote-label">XMLs por lote</div>
      <div class="lote-desc">{DESCRICOES_LOTE[label]}</div>
      <div class="lote-desc" style="margin-top:8px; color:#FF800077">&#128200; {est_txt}</div>
    </div>
    """
cards_html += "</div>"
st.markdown(cards_html, unsafe_allow_html=True)

# Radio funcional (oculto via CSS, mas necessário para capturar valor)
opcao_selecionada = st.radio(
    "Tamanho do lote",
    options=list(OPCOES_LOTE.keys()),
    index=1,                   # padrão: 5.000
    horizontal=True,
    label_visibility="collapsed",
)

files_per_batch = OPCOES_LOTE[opcao_selecionada]

# Preview dinâmico após seleção
if total_xmls_preview > 0:
    lotes_calc   = math.ceil(total_xmls_preview / files_per_batch)
    ultimo_lote  = total_xmls_preview - (lotes_calc - 1) * files_per_batch
    st.markdown(f"""
    <div class="preview-bar">
      &#128202;&nbsp;
      <span><span class="pv-val">{total_xmls_preview:,}".replace(",",".")}</span> XMLs encontrados</span>
      <span class="pv-sep">&nbsp;&#9656;&nbsp;</span>
      <span><span class="pv-val">{lotes_calc}</span> lotes de <span class="pv-val">{files_per_batch:,}".replace(",",".")</span></span>
      <span class="pv-sep">&nbsp;&#9656;&nbsp;</span>
      <span>&#250;ltimo lote: <span class="pv-val">{ultimo_lote}</span> XMLs</span>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  STEP 3 — PROCESSAR
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:24px">3 &mdash; Processar</div>',
    unsafe_allow_html=True,
)

process_btn = st.button(
    f"⚡  Gerar lotes de {opcao_selecionada} zipados individualmente"
)

if process_btn:

    # ── Valida upload ──
    if uploaded_file is None:
        st.markdown(
            '<div class="tr-error">&#9888; Nenhum arquivo enviado. '
            'Fa&ccedil;a o upload de um ZIP antes de processar.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    file_bytes = uploaded_file.getvalue()

    # ── Lê e valida XMLs ──
    try:
        xml_files = ler_xmls_do_zip(file_bytes)
    except zipfile.BadZipFile:
        st.markdown(
            '<div class="tr-error">&#9888; O arquivo enviado n&atilde;o &eacute; '
            'um ZIP v&aacute;lido ou est&aacute; corrompido.</div>',
            unsafe_allow_html=True,
        )
        st.stop()
    except Exception as e:
        st.markdown(
            f'<div class="tr-error">&#9888; Erro ao ler o arquivo: {e}</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    if not xml_files:
        st.markdown(
            '<div class="tr-error">&#9888; Nenhum arquivo XML encontrado '
            'dentro do ZIP enviado.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    total_files   = len(xml_files)
    total_batches = math.ceil(total_files / files_per_batch)
    groups        = [
        xml_files[i * files_per_batch: (i + 1) * files_per_batch]
        for i in range(total_batches)
    ]

    # ── Gera lotes com progresso ──
    progress_bar = st.progress(0, text="Iniciando compacta&ccedil;&atilde;o...")
    src_buf      = io.BytesIO(file_bytes)
    master_buf   = io.BytesIO()

    with zipfile.ZipFile(src_buf, "r") as src_zip:
        with zipfile.ZipFile(master_buf, "w", zipfile.ZIP_DEFLATED) as master_zip:
            for idx, group in enumerate(groups, start=1):
                batch_buf = io.BytesIO()
                with zipfile.ZipFile(batch_buf, "w", zipfile.ZIP_DEFLATED) as batch_zip:
                    for xml_path in group:
                        data    = src_zip.read(xml_path)
                        arcname = os.path.basename(xml_path)
                        batch_zip.writestr(arcname, data)

                lote_name = f"lote_{idx:03d}.zip"
                master_zip.writestr(lote_name, batch_buf.getvalue())

                progress_bar.progress(
                    idx / total_batches,
                    text=f"Compactando {lote_name} — {len(group)} XMLs ({idx}/{total_batches})",
                )

    progress_bar.progress(1.0, text="Todos os lotes compactados com sucesso!")
    master_buf.seek(0)

    # ── Métricas ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total de XMLs",     f"{total_files:,}".replace(",", "."))
    with c2:
        st.metric("Lotes gerados",      str(total_batches))
    with c3:
        st.metric("Último lote",        f"{len(groups[-1])} XMLs")

    # ── Tabela prévia ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="section-label">Pr&eacute;via dos lotes gerados</div>',
        unsafe_allow_html=True,
    )

    rows = ""
    for i, group in enumerate(groups, start=1):
        is_last     = i == total_batches
        badge_class = "badge badge-ok" if is_last else "badge"
        obs = (
            f"&Uacute;ltimo lote ({len(group)} de {files_per_batch:,})".replace(",", ".")
            if is_last else "Lote completo"
        )
        rows += f"""
        <tr>
          <td><code style="color:#FF8000">lote_{i:03d}.zip</code></td>
          <td><span class="{badge_class}">{len(group):,} XMLs</span></td>
          <td style="color:#555555">{obs}</td>
        </tr>
        """.replace(",", ".")

    st.markdown(f"""
    <table class="batch-table">
      <thead>
        <tr>
          <th>Arquivo ZIP</th>
          <th>Quantidade</th>
          <th>Observa&ccedil;&atilde;o</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── Resumo ──
    st.markdown(f"""
    <div class="tr-success">
      <strong>&#10003; Processamento conclu&iacute;do com sucesso!</strong><br>
      &bull; <strong>{total_files:,}</strong> XMLs distribu&iacute;dos em
             <strong>{total_batches}</strong> lotes zipados<br>
      &bull; Cada lote cont&eacute;m at&eacute;
             <strong>{files_per_batch:,}</strong> arquivos XML j&aacute; compactados<br>
      &bull; &Uacute;ltimo lote: <strong>{len(groups[-1]):,}</strong> arquivo(s)<br>
      &bull; Estrutura:
        <code style="color:#90EE90">lotes_xml.zip</code> &rarr;
        <code style="color:#90EE90">lote_001.zip</code>,
        <code style="color:#90EE90">lote_002.zip</code> ...<br>
      &bull; Nenhum XML duplicado ou perdido
    </div>
    """.replace(",", "."), unsafe_allow_html=True)

    # ── Download ──
    st.download_button(
        label=f"⬇️  Baixar lotes_xml.zip  ({total_batches} lotes de {opcao_selecionada})",
        data=master_buf,
        file_name=f"lotes_xml_{opcao_selecionada.replace('.','').replace(' ','_')}.zip",
        mime="application/zip",
    )

# ─────────────────────────────────────────────
#  RODAPÉ
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#444444; font-size:0.75rem;
            border-top:1px solid #2A2A2A; padding-top:16px;">
  Dom&iacute;nio Sistemas &middot; Thomson Reuters &nbsp;|&nbsp;
  Divisor de XML em Lotes &nbsp;|&nbsp;
  <span style="color:#FF800088;">Uso interno</span>
</div>
""", unsafe_allow_html=True)
