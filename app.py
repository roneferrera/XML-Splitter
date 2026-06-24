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

  /* ── Labels ── */
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #FF8000;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  /* ── Boxes ── */
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

  /* ── File uploader ── */
  [data-testid="stFileUploaderDropzone"] {
    background-color: #242424 !important;
    border: 1.5px dashed #444444 !important;
    border-radius: 10px !important;
  }
  [data-testid="stFileUploaderDropzone"] p   { color: #888888 !important; }
  [data-testid="stFileUploaderDropzone"] svg { fill: #FF8000 !important; }

  /* ── Number input ── */
  [data-testid="stNumberInput"] input {
    background: #242424 !important;
    border: 1.5px solid #444444 !important;
    border-radius: 8px !important;
    color: #F0F0F0 !important;
    font-size: 1rem !important;
  }
  [data-testid="stNumberInput"] input:focus {
    border-color: #FF8000 !important;
    box-shadow: 0 0 0 2px #FF800033 !important;
  }

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
  [data-testid="metric-container"] label { color: #888888 !important; font-size: 0.75rem !important; }
  [data-testid="stMetricValue"]          { color: #FF8000 !important; font-size: 1.8rem !important; font-weight: 700 !important; }

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
#  FUNÇÕES AUXILIARES
# ─────────────────────────────────────────────
def ler_xmls_do_zip(file_bytes: bytes) -> list:
    """Lê o ZIP e retorna lista ordenada de caminhos XML encontrados."""
    buf = io.BytesIO(file_bytes)
    with zipfile.ZipFile(buf, "r") as z:
        names = z.namelist()
    return sorted([
        n for n in names
        if n.lower().endswith(".xml")
        and "__MACOSX" not in n
        and not os.path.basename(n).startswith(".")
    ])


def montar_lotes(file_bytes: bytes, xml_files: list, files_per_batch: int):
    """
    Cria o ZIP mestre em memória.
    Cada lote é um .zip individual dentro do ZIP mestre.

    Estrutura final:
      lotes_xml.zip
        ├── lote_001.zip  → xmls 1..N
        ├── lote_002.zip  → xmls N+1..2N
        └── lote_00X.zip  → restante
    """
    total_batches = math.ceil(len(xml_files) / files_per_batch)
    groups = [
        xml_files[i * files_per_batch: (i + 1) * files_per_batch]
        for i in range(total_batches)
    ]

    src_buf    = io.BytesIO(file_bytes)
    master_buf = io.BytesIO()

    with zipfile.ZipFile(src_buf, "r") as src_zip:
        with zipfile.ZipFile(master_buf, "w", zipfile.ZIP_DEFLATED) as master_zip:
            for idx, group in enumerate(groups, start=1):
                batch_buf = io.BytesIO()
                with zipfile.ZipFile(batch_buf, "w", zipfile.ZIP_DEFLATED) as batch_zip:
                    for xml_path in group:
                        data    = src_zip.read(xml_path)
                        arcname = os.path.basename(xml_path)
                        batch_zip.writestr(arcname, data)
                master_zip.writestr(f"lote_{idx:03d}.zip", batch_buf.getvalue())

    master_buf.seek(0)
    return master_buf, groups


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
    "Fa&ccedil;a o upload de um ZIP com seus XMLs, defina o limite por lote e baixe cada lote "
    "j&aacute; compactado individualmente &mdash; pronto para importar direto no sistema."
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
  &bull; Informe o limite m&aacute;ximo de XMLs por lote<br>
  &bull; O sistema gera um ZIP mestre com os lotes j&aacute; zipados individualmente:<br>
  &nbsp;&nbsp;&nbsp;
    <code style="color:#FF8000">lotes_xml.zip</code> &rarr;
    <code style="color:#FF8000">lote_001.zip</code>,
    <code style="color:#FF8000">lote_002.zip</code> ...<br>
  &bull; Cada <code style="color:#FF8000">.zip</code> de lote &eacute; importado diretamente no Dom&iacute;nio<br>
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
#  STEP 2 — CONFIGURAÇÃO
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:20px">2 &mdash; Configura&ccedil;&atilde;o dos lotes</div>',
    unsafe_allow_html=True,
)

col_a, col_b = st.columns([2, 1])

with col_a:
    files_per_batch = st.number_input(
        "Quantidade máxima de XMLs por lote",
        min_value=1,
        max_value=100_000,
        value=100,
        step=1,
        help="Cada lote ZIP terá no máximo esse número de arquivos XML.",
    )

with col_b:
    estimativa = "—"
    if uploaded_file is not None:
        try:
            _xmls = ler_xmls_do_zip(uploaded_file.getvalue())
            if _xmls and files_per_batch > 0:
                estimativa = str(math.ceil(len(_xmls) / files_per_batch))
        except Exception:
            estimativa = "erro"
    st.metric("Lotes estimados", estimativa)

# ─────────────────────────────────────────────
#  STEP 3 — PROCESSAR
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:20px">3 &mdash; Processar</div>',
    unsafe_allow_html=True,
)

process_btn = st.button("⚡  Gerar lotes zipados individualmente")

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

    # ── Valida ZIP e lê XMLs ──
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

    # ── Monta os lotes com progresso ──
    progress_bar = st.progress(0, text="Iniciando compacta&ccedil;&atilde;o dos lotes...")
    src_buf      = io.BytesIO(file_bytes)
    master_buf   = io.BytesIO()
    groups       = []

    with zipfile.ZipFile(src_buf, "r") as src_zip:
        with zipfile.ZipFile(master_buf, "w", zipfile.ZIP_DEFLATED) as master_zip:
            for idx in range(total_batches):
                start = idx * files_per_batch
                end   = start + files_per_batch
                group = xml_files[start:end]
                groups.append(group)

                batch_buf = io.BytesIO()
                with zipfile.ZipFile(batch_buf, "w", zipfile.ZIP_DEFLATED) as batch_zip:
                    for xml_path in group:
                        data    = src_zip.read(xml_path)
                        arcname = os.path.basename(xml_path)
                        batch_zip.writestr(arcname, data)

                lote_name = f"lote_{idx + 1:03d}.zip"
                master_zip.writestr(lote_name, batch_buf.getvalue())

                progress_bar.progress(
                    (idx + 1) / total_batches,
                    text=f"Compactando {lote_name} — {len(group)} XMLs "
                         f"({idx + 1}/{total_batches})",
                )

    progress_bar.progress(1.0, text="Todos os lotes compactados com sucesso!")
    master_buf.seek(0)

    # ── Métricas ──
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total de XMLs",      f"{total_files:,}".replace(",", "."))
    with c2:
        st.metric("Lotes gerados",       str(total_batches))
    with c3:
        st.metric("Último lote",         f"{len(groups[-1])} XMLs")

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
        obs         = (
            f"&Uacute;ltimo lote ({len(group)} de {files_per_batch})"
            if is_last else "Lote completo"
        )
        rows += f"""
        <tr>
          <td><code style="color:#FF8000">lote_{i:03d}.zip</code></td>
          <td><span class="{badge_class}">{len(group)} XMLs</span></td>
          <td style="color:#555555">{obs}</td>
        </tr>
        """

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
      &bull; <strong>{total_files}</strong> XMLs distribu&iacute;dos em
             <strong>{total_batches}</strong> lotes zipados<br>
      &bull; Cada lote cont&eacute;m at&eacute; <strong>{files_per_batch}</strong>
             arquivos XML j&aacute; compactados<br>
      &bull; &Uacute;ltimo lote: <strong>{len(groups[-1])}</strong> arquivo(s)<br>
      &bull; Estrutura:
        <code style="color:#90EE90">lotes_xml.zip</code> &rarr;
        <code style="color:#90EE90">lote_001.zip</code>,
        <code style="color:#90EE90">lote_002.zip</code> ...<br>
      &bull; Nenhum XML duplicado ou perdido
    </div>
    """, unsafe_allow_html=True)

    # ── Download ──
    st.download_button(
        label=f"⬇️  Baixar lotes_xml.zip  ({total_batches} lotes zipados)",
        data=master_buf,
        file_name="lotes_xml.zip",
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
