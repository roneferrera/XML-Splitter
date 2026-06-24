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
  .tr-dot            { width:8px; height:8px; border-radius:50%; background:#FF8000; opacity:0.9; }
  .tr-dot.dim        { opacity:0.30; }
  .tr-dot.mid        { opacity:0.55; }
  .tr-brand          { display:flex; flex-direction:column; line-height:1.1; }
  .tr-brand-main     { font-size:1.3rem; font-weight:700; color:#F0F0F0; letter-spacing:-0.3px; }
  .tr-brand-sub      { font-size:0.72rem; font-weight:400; color:#FF8000; letter-spacing:2px; text-transform:uppercase; }

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

  /* ── Info / Success / Error boxes ── */
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

  /* ── Tabela de lotes ── */
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
  .batch-table tr:hover td { background: #242424; }
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
    background: #00AA4422;
    color: #4CAF50;
    border-color: #4CAF5055;
  }

  /* ── Inputs ── */
  .stFileUploader > div {
    background: #242424 !important;
    border: 1.5px dashed #444444 !important;
    border-radius: 10px !important;
  }
  .stFileUploader > div:hover { border-color: #FF8000 !important; }
  .stFileUploader label { color: #AAAAAA !important; font-size: 0.85rem !important; }

  div[data-testid="stFileUploaderDropzone"] { background: #242424 !important; }
  div[data-testid="stFileUploaderDropzone"] p { color: #888888 !important; }
  div[data-testid="stFileUploaderDropzone"] svg { fill: #FF8000 !important; }

  .stNumberInput > div > div > input {
    background: #242424 !important;
    border: 1.5px solid #444444 !important;
    border-radius: 8px !important;
    color: #F0F0F0 !important;
    font-size: 1rem !important;
    padding: 10px 14px !important;
  }
  .stNumberInput > div > div > input:focus {
    border-color: #FF8000 !important;
    box-shadow: 0 0 0 2px #FF800033 !important;
  }
  .stNumberInput label { color: #AAAAAA !important; font-size: 0.85rem !important; }

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
  .stProgress > div > div > div {
    background: linear-gradient(90deg, #FF8000, #FFB347) !important;
    border-radius: 4px !important;
  }
  .stProgress > div > div {
    background: #333333 !important;
    border-radius: 4px !important;
  }

  /* ── Métricas ── */
  div[data-testid="metric-container"] {
    background: #242424 !important;
    border: 1px solid #333333 !important;
    border-radius: 10px !important;
    padding: 16px 20px !important;
  }
  div[data-testid="metric-container"] label {
    color: #888888 !important;
    font-size: 0.75rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
  }
  div[data-testid="stMetricValue"] {
    color: #FF8000 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }

  /* ── Esconde elementos padrão ── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }

  hr { border-color: #333333 !important; margin: 24px 0 !important; }

  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #1A1A1A; }
  ::-webkit-scrollbar-thumb { background: #444444; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #FF8000; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  HEADER / LOGO
# ─────────────────────────────────────────────
st.markdown("""
<div class="tr-header">
  <div class="tr-logo-dots">
    <div class="tr-dot dim"></div><div class="tr-dot mid"></div><div class="tr-dot"></div><div class="tr-dot mid"></div>
    <div class="tr-dot mid"></div><div class="tr-dot"></div><div class="tr-dot"></div><div class="tr-dot"></div>
    <div class="tr-dot"></div><div class="tr-dot"></div><div class="tr-dot mid"></div><div class="tr-dot dim"></div>
    <div class="tr-dot mid"></div><div class="tr-dot"></div><div class="tr-dot dim"></div><div class="tr-dot mid"></div>
  </div>
  <div class="tr-brand">
    <span class="tr-brand-main">Domínio Sistemas</span>
    <span class="tr-brand-sub">Thomson Reuters</span>
  </div>
</div>
<div class="tr-divider"></div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  TÍTULO
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">Utilitário de Arquivos</div>', unsafe_allow_html=True)
st.markdown("## Divisor de XMLs em Lotes")
st.markdown(
    "<p style='color:#888888; font-size:0.9rem; margin-top:-10px; margin-bottom:24px;'>"
    "Faça o upload de um ZIP com seus XMLs, defina o limite por lote e baixe cada lote "
    "já compactado individualmente — pronto para importar direto no sistema."
    "</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  INFO BOX
# ─────────────────────────────────────────────
st.markdown("""
<div class="tr-info">
  <strong>📌 Como funciona</strong><br>
  • Envie um <strong>.zip</strong> contendo os XMLs (pode conter subpastas)<br>
  • Informe o limite máximo de XMLs por lote<br>
  • O sistema gera um ZIP mestre com os lotes já zipados individualmente:<br>
  &nbsp;&nbsp;&nbsp;
  <code style="color:#FF8000">lotes_xml.zip</code> →
  <code style="color:#FF8000">lote_001.zip</code>,
  <code style="color:#FF8000">lote_002.zip</code>,
  <code style="color:#FF8000">lote_003.zip</code>...<br>
  • Cada <code style="color:#FF8000">.zip</code> de lote é importado diretamente no Domínio<br>
  • Nenhum XML é duplicado ou perdido — divisão exata garantida
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  STEP 1 — UPLOAD
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">1 — Arquivo de entrada</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo ZIP com os XMLs",
    type=["zip"],
    help="Apenas arquivos .zip são aceitos. Os XMLs podem estar em subpastas dentro do ZIP.",
)

# ─────────────────────────────────────────────
#  STEP 2 — CONFIGURAÇÃO
# ─────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:20px">2 — Configuração dos lotes</div>', unsafe_allow_html=True)

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
    # Preview dinâmico — só calcula se já tiver arquivo
    if uploaded_file is not None:
        try:
            _buf = io.BytesIO(uploaded_file.getvalue())
            with zipfile.ZipFile(_buf, "r") as _z:
                _xmls = [n for n in _z.namelist() if n.lower().endswith(".xml") and not n.startswith("__MACOSX")]
            _total = len(_xmls)
            _lotes = math.ceil(_total / files_per_batch) if files_per_batch > 0 else 0
            st.metric("Lotes estimados", str(_lotes))
        except Exception:
            st.metric("Lotes estimados", "—")
    else:
        st.metric("Lotes estimados", "—")

# ─────────────────────────────────────────────
#  STEP 3 — PROCESSAR
# ─────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:20px">3 — Processar</div>', unsafe_allow_html=True)
process_btn = st.button("⚡  Gerar lotes zipados individualmente")

if process_btn:
    if uploaded_file is None:
        st.markdown(
            '<div class="tr-error">⚠️ Nenhum arquivo enviado. Faça o upload de um ZIP antes de processar.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    with st.spinner("Lendo os arquivos XML do ZIP..."):
        zip_bytes = uploaded_file.getvalue()
        zip_buffer = io.BytesIO(zip_bytes)

        try:
            with zipfile.ZipFile(zip_buffer, "r") as z:
                all_names = z.namelist()
        except zipfile.BadZipFile:
            st.markdown(
                '<div class="tr-error">⚠️ O arquivo enviado não é um ZIP válido ou está corrompido.</div>',
                unsafe_allow_html=True,
            )
            st.stop()

    # ── Filtra XMLs ──
    xml_files = sorted([
        n for n in all_names
        if n.lower().endswith(".xml") and not n.startswith("__MACOSX")
    ])
    total_files = len(xml_files)

    if total_files == 0:
        st.markdown(
            '<div class="tr-error">⚠️ Nenhum arquivo XML encontrado dentro do ZIP enviado.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    # ── Calcula grupos ──
    total_batches = math.ceil(total_files / files_per_batch)
    groups = [
        xml_files[i * files_per_batch : (i + 1) * files_per_batch]
        for i in range(total_batches)
    ]

    # ────────────────────────────────────────────────────────────
    #  MONTA O ZIP MESTRE  →  cada lote é um .zip dentro dele
    #
    #  Estrutura final:
    #    lotes_xml.zip
    #      ├── lote_001.zip   (contém os XMLs do lote 1)
    #      ├── lote_002.zip   (contém os XMLs do lote 2)
    #      └── lote_003.zip   (contém os XMLs do lote 3)
    # ────────────────────────────────────────────────────────────
    progress_bar = st.progress(0, text="Iniciando compactação dos lotes...")
    master_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "r") as src_zip:
        with zipfile.ZipFile(master_buffer, "w", zipfile.ZIP_DEFLATED) as master_zip:
            for idx, group in enumerate(groups, start=1):

                # Cria o ZIP do lote em memória
                batch_buffer = io.BytesIO()
                with zipfile.ZipFile(batch_buffer, "w", zipfile.ZIP_DEFLATED) as batch_zip:
                    for xml_path in group:
                        data = src_zip.read(xml_path)
                        # Mantém apenas o nome do arquivo, sem subpastas
                        arcname = os.path.basename(xml_path)
                        batch_zip.writestr(arcname, data)

                # Adiciona o ZIP do lote dentro do ZIP mestre
                batch_name = f"lote_{idx:03d}.zip"
                master_zip.writestr(batch_name, batch_buffer.getvalue())

                progress_bar.progress(
                    idx / total_batches,
                    text=f"Compactando lote {idx} de {total_batches} — {batch_name} ({len(group)} XMLs)",
                )

    progress_bar.progress(1.0, text="✅ Todos os lotes compactados!")
    master_buffer.seek(0)

    # ── Métricas ──
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de XMLs", f"{total_files:,}".replace(",", "."))
    with col2:
        st.metric("Lotes gerados", str(total_batches))
    with col3:
        st.metric("XMLs no último lote", str(len(groups[-1])))

    # ── Tabela de prévia dos lotes ──
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Prévia dos lotes gerados</div>', unsafe_allow_html=True)

    rows = ""
    for idx, group in enumerate(groups, start=1):
        is_last = idx == total_batches
        badge_class = "badge" if not is_last else "badge badge-ok"
        badge_label = f"{len(group)} XMLs"
        rows += f"""
        <tr>
          <td><code style="color:#FF8000">lote_{idx:03d}.zip</code></td>
          <td><span class="{badge_class}">{badge_label}</span></td>
          <td style="color:#555555">{
            "Lote completo" if not is_last else
            f"Último lote ({len(group)} de {files_per_batch})"
          }</td>
        </tr>
        """

    st.markdown(f"""
    <table class="batch-table">
      <thead>
        <tr>
          <th>Arquivo ZIP</th>
          <th>Quantidade</th>
          <th>Observação</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # ── Resumo ──
    st.markdown(f"""
    <div class="tr-success">
      <strong>✅ Processamento concluído com sucesso!</strong><br>
      • <strong>{total_files}</strong> XMLs distribuídos em <strong>{total_batches}</strong> lotes zipados<br>
      • Cada lote contém até <strong>{files_per_batch}</strong> arquivos XML já compactados<br>
      • Último lote: <strong>{len(groups[-1])}</strong> arquivo(s)<br>
      • Estrutura: <code style="color:#90EE90">lotes_xml.zip</code> →
        <code style="color:#90EE90">lote_001.zip</code>,
        <code style="color:#90EE90">lote_002.zip</code>...<br>
      • Nenhum XML duplicado ou perdido
    </div>
    """, unsafe_allow_html=True)

    # ── Download ──
    st.download_button(
        label=f"⬇️  Baixar lotes_xml.zip  ({total_batches} lotes zipados)",
        data=master_buffer,
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
  Domínio Sistemas · Thomson Reuters &nbsp;|&nbsp; Divisor de XML em Lotes &nbsp;|&nbsp;
  <span style="color:#FF800088;">Uso interno</span>
</div>
""", unsafe_allow_html=True)
