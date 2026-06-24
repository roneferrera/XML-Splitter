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
#  Cores oficiais:
#    Laranja principal : #FF8000
#    Fundo escuro      : #1A1A1A
#    Card escuro       : #242424
#    Borda sutil       : #333333
#    Texto principal   : #F0F0F0
#    Texto secundário  : #AAAAAA
#    Cinza médio       : #555555
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Google Font ── */
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  /* ── Reset geral ── */
  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
  }

  /* ── Fundo da página ── */
  .stApp {
    background-color: #1A1A1A !important;
  }

  /* ── Bloco principal centralizado ── */
  .block-container {
    max-width: 680px !important;
    padding: 2.5rem 2rem 3rem 2rem !important;
  }

  /* ── Header / Logo ── */
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
  .tr-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #FF8000;
    opacity: 0.9;
  }
  .tr-dot.dim  { opacity: 0.35; }
  .tr-dot.mid  { opacity: 0.60; }

  .tr-brand {
    display: flex;
    flex-direction: column;
    line-height: 1.1;
  }
  .tr-brand-main {
    font-size: 1.3rem;
    font-weight: 700;
    color: #F0F0F0;
    letter-spacing: -0.3px;
  }
  .tr-brand-sub {
    font-size: 0.72rem;
    font-weight: 400;
    color: #FF8000;
    letter-spacing: 2px;
    text-transform: uppercase;
  }

  /* ── Divider laranja ── */
  .tr-divider {
    height: 2px;
    background: linear-gradient(90deg, #FF8000 0%, #FF800044 60%, transparent 100%);
    margin: 14px 0 28px 0;
    border-radius: 2px;
  }

  /* ── Títulos de seção ── */
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #FF8000;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }

  /* ── Cards ── */
  .tr-card {
    background: #242424;
    border: 1px solid #333333;
    border-radius: 10px;
    padding: 20px 22px;
    margin-bottom: 20px;
  }
  .tr-card-title {
    font-size: 0.82rem;
    font-weight: 600;
    color: #AAAAAA;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .tr-card-value {
    font-size: 2rem;
    font-weight: 700;
    color: #FF8000;
    line-height: 1.1;
  }
  .tr-card-desc {
    font-size: 0.8rem;
    color: #666666;
    margin-top: 2px;
  }

  /* ── Info box ── */
  .tr-info {
    background: #1E1E1E;
    border-left: 3px solid #FF8000;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin-bottom: 24px;
    font-size: 0.85rem;
    color: #AAAAAA;
    line-height: 1.7;
  }
  .tr-info strong { color: #F0F0F0; }

  /* ── Success box ── */
  .tr-success {
    background: #1A2A1A;
    border: 1px solid #2A5A2A;
    border-left: 3px solid #4CAF50;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 20px 0;
    font-size: 0.85rem;
    color: #90EE90;
    line-height: 1.8;
  }
  .tr-success strong { color: #AAFFAA; }

  /* ── Error box ── */
  .tr-error {
    background: #2A1A1A;
    border-left: 3px solid #FF4444;
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 12px 0;
    font-size: 0.85rem;
    color: #FF9999;
  }

  /* ── Inputs do Streamlit ── */
  .stFileUploader > div {
    background: #242424 !important;
    border: 1.5px dashed #444444 !important;
    border-radius: 10px !important;
    transition: border-color 0.2s;
  }
  .stFileUploader > div:hover {
    border-color: #FF8000 !important;
  }
  .stFileUploader label {
    color: #AAAAAA !important;
    font-size: 0.85rem !important;
  }

  div[data-testid="stFileUploaderDropzone"] {
    background: #242424 !important;
  }
  div[data-testid="stFileUploaderDropzone"] p {
    color: #888888 !important;
  }
  div[data-testid="stFileUploaderDropzone"] svg {
    fill: #FF8000 !important;
  }

  /* ── Number input ── */
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
  .stNumberInput label {
    color: #AAAAAA !important;
    font-size: 0.85rem !important;
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
    cursor: pointer !important;
    transition: all 0.2s !important;
    margin-top: 8px !important;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #FF9520 0%, #FF8000 100%) !important;
    box-shadow: 0 4px 20px #FF800055 !important;
    transform: translateY(-1px) !important;
  }
  .stButton > button:active {
    transform: translateY(0px) !important;
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
    cursor: pointer !important;
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

  /* ── Esconde elementos padrão do Streamlit ── */
  #MainMenu { visibility: hidden; }
  footer    { visibility: hidden; }
  header    { visibility: hidden; }

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
  div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #FF8000 !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
  }

  /* ── Separador ── */
  hr {
    border-color: #333333 !important;
    margin: 24px 0 !important;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #1A1A1A; }
  ::-webkit-scrollbar-thumb { background: #444444; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #FF8000; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  LOGO / HEADER
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
    "Faça o upload de um ZIP contendo seus arquivos XML e divida-os em lotes controlados, "
    "sem duplicação e sem perda de arquivos."
    "</p>",
    unsafe_allow_html=True,
)

# ─────────────────────────────────────────────
#  INFO BOX
# ─────────────────────────────────────────────
st.markdown("""
<div class="tr-info">
  <strong>📌 Como funciona</strong><br>
  • Envie um <strong>.zip</strong> contendo os XMLs (pode estar em subpastas)<br>
  • Informe o limite de arquivos por lote<br>
  • O sistema gera um novo ZIP com subpastas <code style="color:#FF8000">lote_001/</code>, <code style="color:#FF8000">lote_002/</code>...<br>
  • Nenhum XML é duplicado ou perdido — divisão exata garantida
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  UPLOAD
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">1 — Arquivo de entrada</div>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo ZIP com os XMLs",
    type=["zip"],
    help="Apenas arquivos .zip são aceitos. Os XMLs podem estar em subpastas dentro do ZIP.",
)

# ─────────────────────────────────────────────
#  QUANTIDADE POR LOTE
# ─────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:20px">2 — Configuração dos lotes</div>', unsafe_allow_html=True)
files_per_batch = st.number_input(
    "Quantidade de XMLs por lote",
    min_value=1,
    max_value=100000,
    value=100,
    step=1,
    help="Cada subpasta do ZIP final terá no máximo esse número de arquivos XML.",
)

# ─────────────────────────────────────────────
#  PROCESSAMENTO
# ─────────────────────────────────────────────
st.markdown('<div class="section-label" style="margin-top:20px">3 — Processar</div>', unsafe_allow_html=True)
process_btn = st.button("⚡  Processar e gerar ZIP de lotes")

if process_btn:
    if uploaded_file is None:
        st.markdown(
            '<div class="tr-error">⚠️ Nenhum arquivo enviado. Faça o upload de um ZIP antes de processar.</div>',
            unsafe_allow_html=True,
        )
    else:
        with st.spinner("Lendo e processando os arquivos XML..."):

            # ── Lê o ZIP em memória ──
            zip_bytes = uploaded_file.read()
            zip_buffer = io.BytesIO(zip_bytes)

            try:
                with zipfile.ZipFile(zip_buffer, "r") as z:
                    all_names = z.namelist()

                # ── Filtra apenas XMLs ──
                xml_files = sorted(
                    [n for n in all_names if n.lower().endswith(".xml") and not n.startswith("__MACOSX")]
                )
                total_files = len(xml_files)

                if total_files == 0:
                    st.markdown(
                        '<div class="tr-error">⚠️ Nenhum arquivo XML encontrado dentro do ZIP enviado.</div>',
                        unsafe_allow_html=True,
                    )
                    st.stop()

                # ── Calcula lotes ──
                total_batches = math.ceil(total_files / files_per_batch)
                groups = [
                    xml_files[i * files_per_batch : (i + 1) * files_per_batch]
                    for i in range(total_batches)
                ]

                # ── Monta ZIP de saída em memória ──
                output_buffer = io.BytesIO()
                progress_bar = st.progress(0, text="Montando lotes...")

                with zipfile.ZipFile(zip_buffer, "r") as src_zip:
                    with zipfile.ZipFile(output_buffer, "w", zipfile.ZIP_DEFLATED) as out_zip:
                        for idx, group in enumerate(groups, start=1):
                            folder_name = f"lote_{idx:03d}"
                            for xml_path in group:
                                data = src_zip.read(xml_path)
                                arcname = f"{folder_name}/{os.path.basename(xml_path)}"
                                out_zip.writestr(arcname, data)
                            progress_bar.progress(
                                idx / total_batches,
                                text=f"Montando lote {idx} de {total_batches}...",
                            )

                progress_bar.progress(1.0, text="Concluído!")
                output_buffer.seek(0)

                # ── Métricas de resultado ──
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de XMLs", f"{total_files:,}".replace(",", "."))
                with col2:
                    st.metric("Lotes gerados", str(total_batches))
                with col3:
                    last_batch = len(groups[-1]) if groups else 0
                    st.metric("XMLs no último lote", str(last_batch))

                # ── Detalhes ──
                st.markdown(f"""
                <div class="tr-success">
                  <strong>✅ Processamento concluído com sucesso!</strong><br>
                  • <strong>{total_files}</strong> XMLs encontrados e distribuídos<br>
                  • <strong>{total_batches}</strong> lotes criados com até <strong>{files_per_batch}</strong> arquivos cada<br>
                  • Último lote: <strong>{last_batch}</strong> arquivo(s)<br>
                  • Nenhum XML duplicado ou perdido
                </div>
                """, unsafe_allow_html=True)

                # ── Botão de download ──
                st.download_button(
                    label=f"⬇️  Baixar ZIP com {total_batches} lote(s)",
                    data=output_buffer,
                    file_name=f"lotes_xml_{total_batches}pastas.zip",
                    mime="application/zip",
                )

            except zipfile.BadZipFile:
                st.markdown(
                    '<div class="tr-error">⚠️ O arquivo enviado não é um ZIP válido ou está corrompido.</div>',
                    unsafe_allow_html=True,
                )

# ─────────────────────────────────────────────
#  RODAPÉ
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#444444; font-size:0.75rem; border-top:1px solid #2A2A2A; padding-top:16px;">
  Domínio Sistemas · Thomson Reuters &nbsp;|&nbsp; Divisor de XML em Lotes &nbsp;|&nbsp;
  <span style="color:#FF800088;">Uso interno</span>
</div>
""", unsafe_allow_html=True)
