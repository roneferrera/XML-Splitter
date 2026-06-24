import streamlit as st
import zipfile
import math
import os
import io

st.set_page_config(
    page_title="Domínio Sistemas | Divisor de XML",
    page_icon="📂",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', sans-serif !important;
  }
  .stApp { background-color: #1A1A1A !important; }
  .block-container {
    max-width: 700px !important;
    padding: 2.5rem 2rem 3rem 2rem !important;
  }

  .tr-header { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
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
  .tr-brand-sub  { font-size:0.72rem; color:#FF8000; letter-spacing:2px; text-transform:uppercase; }

  .tr-divider {
    height: 2px;
    background: linear-gradient(90deg, #FF8000 0%, #FF800044 60%, transparent 100%);
    margin: 14px 0 28px 0;
    border-radius: 2px;
  }
  .section-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: #FF8000;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 10px;
  }
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

  .preview-bar {
    background: #1E1E1E;
    border: 1px solid #2A2A2A;
    border-radius: 8px;
    padding: 12px 16px;
    margin-top: 8px;
    margin-bottom: 8px;
    font-size: 0.83rem;
    color: #888888;
  }
  .pv-val { color: #FF8000; font-weight: 700; font-size: 1rem; }

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

  /* ── Card de lote via container nativo ── */
  div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #242424 !important;
    border: 2px solid #333333 !important;
    border-radius: 12px !important;
    padding: 4px !important;
    transition: all 0.2s !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #FF8000 !important;
    box-shadow: 0 4px 20px #FF800033 !important;
  }

  /* ── Botões dos cards ── */
  .stButton > button {
    width: 100% !important;
    background: transparent !important;
    color: #555555 !important;
    border: 1px solid #333333 !important;
    border-radius: 8px !important;
    padding: 8px !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
    margin-top: 4px !important;
  }
  .stButton > button:hover {
    background: #FF800015 !important;
    color: #FF8000 !important;
    border-color: #FF8000 !important;
    box-shadow: none !important;
    transform: none !important;
  }

  /* ── Botão processar ── */
  .btn-processar > div > .stButton > button {
    background: linear-gradient(135deg, #FF8000 0%, #E06000 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 20px !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    margin-top: 8px !important;
  }
  .btn-processar > div > .stButton > button:hover {
    background: linear-gradient(135deg, #FF9520 0%, #FF8000 100%) !important;
    box-shadow: 0 4px 20px #FF800055 !important;
    transform: translateY(-1px) !important;
  }

  /* ── Botão download ── */
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

  /* ── File uploader ── */
  [data-testid="stFileUploaderDropzone"] {
    background-color: #242424 !important;
    border: 1.5px dashed #444444 !important;
    border-radius: 10px !important;
  }
  [data-testid="stFileUploaderDropzone"] p   { color: #888888 !important; }
  [data-testid="stFileUploaderDropzone"] svg { fill: #FF8000 !important; }

  /* ── Texto geral ── */
  p, span, div { color: inherit; }

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
#  CONSTANTES
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
#  FUNÇÕES
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


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


# ─────────────────────────────────────────────
#  HEADER
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
    <span class="tr-brand-main">Domínio Sistemas</span>
    <span class="tr-brand-sub">Thomson Reuters</span>
  </div>
</div>
<div class="tr-divider"></div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Utilitário de Arquivos</div>', unsafe_allow_html=True)
st.markdown("## Divisor de XMLs em Lotes")
st.markdown(
    "<p style='color:#888888; font-size:0.9rem; margin-top:-10px; margin-bottom:24px;'>"
    "Faça o upload de um ZIP com seus XMLs, escolha o tamanho do lote e baixe "
    "cada lote já compactado individualmente — pronto para importar no sistema."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="tr-info">
  <strong>📌 Como funciona</strong><br>
  &bull; Envie um <strong>.zip</strong> contendo os XMLs (pode conter subpastas)<br>
  &bull; Escolha o tamanho do lote: <strong>1.000</strong>, <strong>5.000</strong> ou <strong>10.000</strong> XMLs<br>
  &bull; O sistema gera um ZIP mestre com os lotes já zipados individualmente<br>
  &bull; Cada lote é importado diretamente no Domínio<br>
  &bull; Nenhum XML duplicado ou perdido — divisão exata garantida
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STEP 1 — UPLOAD
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">1 — Arquivo de entrada</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo ZIP com os XMLs",
    type=["zip"],
    help="Apenas arquivos .zip são aceitos.",
)

# ─────────────────────────────────────────────
#  STEP 2 — SELEÇÃO DO LOTE (cards nativos)
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:24px">2 — Tamanho do lote</div>',
    unsafe_allow_html=True,
)

# Preview de XMLs
total_xmls_preview = 0
if uploaded_file is not None:
    try:
        total_xmls_preview = len(ler_xmls_do_zip(uploaded_file.getvalue()))
    except Exception:
        total_xmls_preview = 0

# Estado de seleção
if "lote_selecionado" not in st.session_state:
    st.session_state.lote_selecionado = "5.000 XMLs"

opcoes_list  = list(OPCOES_LOTE.keys())
valores_list = list(OPCOES_LOTE.values())

col1, col2, col3 = st.columns(3)

for col, label, valor in zip([col1, col2, col3], opcoes_list, valores_list):
    with col:
        with st.container(border=True):
            ativo = label == st.session_state.lote_selecionado

            # Número grande
            st.markdown(
                f"<div style='text-align:center; font-size:1.8rem; font-weight:700;"
                f"color:{'#FF8000' if ativo else '#555555'}; line-height:1; margin-bottom:2px;'>"
                f"{label.replace(' XMLs','')}</div>",
                unsafe_allow_html=True,
            )

            # Label
            st.markdown(
                "<div style='text-align:center; font-size:0.68rem; color:#666666;"
                "text-transform:uppercase; letter-spacing:1.2px;'>XMLs por lote</div>",
                unsafe_allow_html=True,
            )

            # Descrição
            st.markdown(
                f"<div style='text-align:center; font-size:0.73rem; color:#555555;"
                f"margin-top:6px;'>{DESCRICOES_LOTE[label]}</div>",
                unsafe_allow_html=True,
            )

            # Estimativa
            if total_xmls_preview > 0:
                lotes_est = math.ceil(total_xmls_preview / valor)
                est_txt   = f"📊 {fmt(lotes_est)} lotes"
            else:
                est_txt = "📊 aguardando arquivo"

            st.markdown(
                f"<div style='text-align:center; font-size:0.73rem;"
                f"color:{'#FF8000AA' if ativo else '#444444'}; margin-top:4px;'>"
                f"{est_txt}</div>",
                unsafe_allow_html=True,
            )

            # Botão de seleção
            btn_label = "✔ Selecionado" if ativo else "Selecionar"
            if st.button(btn_label, key=f"btn_{valor}", disabled=ativo):
                st.session_state.lote_selecionado = label
                st.rerun()

opcao_selecionada = st.session_state.lote_selecionado
files_per_batch   = OPCOES_LOTE[opcao_selecionada]

# Preview bar
if total_xmls_preview > 0:
    lotes_calc  = math.ceil(total_xmls_preview / files_per_batch)
    ultimo_lote = total_xmls_preview - (lotes_calc - 1) * files_per_batch
    st.markdown(f"""
    <div class="preview-bar">
      📈 &nbsp;
      <span><span class="pv-val">{fmt(total_xmls_preview)}</span> XMLs encontrados</span>
      &nbsp;▶&nbsp;
      <span><span class="pv-val">{fmt(lotes_calc)}</span> lotes de
      <span class="pv-val">{fmt(files_per_batch)}</span></span>
      &nbsp;▶&nbsp;
      <span>último lote: <span class="pv-val">{fmt(ultimo_lote)}</span> XMLs</span>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  STEP 3 — PROCESSAR
# ─────────────────────────────────────────────
st.markdown(
    '<div class="section-label" style="margin-top:24px">3 — Processar</div>',
    unsafe_allow_html=True,
)

st.markdown('<div class="btn-processar">', unsafe_allow_html=True)
process_btn = st.button(f"⚡  Gerar lotes de {opcao_selecionada} zipados individualmente")
st.markdown('</div>', unsafe_allow_html=True)

if process_btn:

    if uploaded_file is None:
        st.markdown(
            '<div class="tr-error">⚠️ Nenhum arquivo enviado. Faça o upload antes de processar.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    file_bytes = uploaded_file.getvalue()

    try:
        xml_files = ler_xmls_do_zip(file_bytes)
    except zipfile.BadZipFile:
        st.markdown(
            '<div class="tr-error">⚠️ O arquivo não é um ZIP válido ou está corrompido.</div>',
            unsafe_allow_html=True,
        )
        st.stop()
    except Exception as e:
        st.markdown(f'<div class="tr-error">⚠️ Erro ao ler o arquivo: {e}</div>', unsafe_allow_html=True)
        st.stop()

    if not xml_files:
        st.markdown(
            '<div class="tr-error">⚠️ Nenhum arquivo XML encontrado dentro do ZIP.</div>',
            unsafe_allow_html=True,
        )
        st.stop()

    total_files   = len(xml_files)
    total_batches = math.ceil(total_files / files_per_batch)
    groups        = [
        xml_files[i * files_per_batch: (i + 1) * files_per_batch]
        for i in range(total_batches)
    ]

    progress_bar = st.progress(0, text="Iniciando compactação dos lotes...")
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

    # Métricas
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total de XMLs", fmt(total_files))
    with c2:
        st.metric("Lotes gerados",  fmt(total_batches))
    with c3:
        st.metric("Último lote",    f"{fmt(len(groups[-1]))} XMLs")

    # Tabela
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Prévia dos lotes gerados</div>', unsafe_allow_html=True)

    rows = ""
    for i, group in enumerate(groups, start=1):
        is_last     = i == total_batches
        badge_class = "badge badge-ok" if is_last else "badge"
        obs = (
            f"Último lote ({fmt(len(group))} de {fmt(files_per_batch)})"
            if is_last else "Lote completo"
        )
        rows += f"""
        <tr>
          <td><code style="color:#FF8000">lote_{i:03d}.zip</code></td>
          <td><span class="{badge_class}">{fmt(len(group))} XMLs</span></td>
          <td style="color:#555555">{obs}</td>
        </tr>
        """

    st.markdown(f"""
    <table class="batch-table">
      <thead>
        <tr><th>Arquivo ZIP</th><th>Quantidade</th><th>Observação</th></tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # Resumo
    st.markdown(f"""
    <div class="tr-success">
      <strong>✅ Processamento concluído com sucesso!</strong><br>
      &bull; <strong>{fmt(total_files)}</strong> XMLs distribuídos em
             <strong>{fmt(total_batches)}</strong> lotes zipados<br>
      &bull; Cada lote contém até <strong>{fmt(files_per_batch)}</strong> arquivos XML já compactados<br>
      &bull; Último lote: <strong>{fmt(len(groups[-1]))}</strong> arquivo(s)<br>
      &bull; Estrutura: <code style="color:#90EE90">lotes_xml.zip</code>
             &rarr; <code style="color:#90EE90">lote_001.zip</code>,
             <code style="color:#90EE90">lote_002.zip</code> ...<br>
      &bull; Nenhum XML duplicado ou perdido
    </div>
    """, unsafe_allow_html=True)

    # Download
    nome_arquivo = opcao_selecionada.replace(".", "").replace(" ", "_")
    st.download_button(
        label=f"⬇️  Baixar lotes_xml.zip  ({fmt(total_batches)} lotes de {opcao_selecionada})",
        data=master_buf,
        file_name=f"lotes_xml_{nome_arquivo}.zip",
        mime="application/zip",
    )

# ─────────────────────────────────────────────
#  RODAPÉ
# ─────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#444444; font-size:0.75rem;
            border-top:1px solid #2A2A2A; padding-top:16px;">
  Domínio Sistemas &middot; Thomson Reuters &nbsp;|&nbsp;
  Divisor de XML em Lotes &nbsp;|&nbsp;
  <span style="color:#FF800088;">Uso interno</span>
</div>
""", unsafe_allow_html=True)
