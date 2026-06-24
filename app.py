import streamlit as st
import zipfile
import math
import os
import io
import xml.etree.ElementTree as ET


st.set_page_config(
    page_title="Domínio Sistemas | Utilitário XML",
    page_icon="📂",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', 'Segoe UI', sans-serif !important; }
  .stApp { background-color: #1A1A1A !important; }
  .block-container { max-width: 820px !important; padding: 2.5rem 2rem 3rem 2rem !important; }

  .tr-header { display:flex; align-items:center; gap:14px; margin-bottom:6px; }
  .tr-logo-dots {
    display:grid; grid-template-columns:repeat(4,8px);
    grid-template-rows:repeat(4,8px); gap:3px;
  }
  .tr-dot     { width:8px; height:8px; border-radius:50%; background:#FF8000; opacity:0.9; }
  .tr-dot.dim { opacity:0.25; }
  .tr-dot.mid { opacity:0.55; }
  .tr-brand      { display:flex; flex-direction:column; line-height:1.1; }
  .tr-brand-main { font-size:1.3rem; font-weight:700; color:#F0F0F0; letter-spacing:-0.3px; }
  .tr-brand-sub  { font-size:0.72rem; color:#FF8000; letter-spacing:2px; text-transform:uppercase; }
  .tr-divider {
    height:2px;
    background:linear-gradient(90deg,#FF8000 0%,#FF800044 60%,transparent 100%);
    margin:14px 0 28px 0; border-radius:2px;
  }

  .section-label {
    font-size:0.72rem; font-weight:600; color:#FF8000;
    letter-spacing:1.8px; text-transform:uppercase; margin-bottom:10px;
  }

  .tr-info {
    background:#1E1E1E; border-left:3px solid #FF8000;
    border-radius:0 8px 8px 0; padding:14px 18px;
    margin-bottom:24px; font-size:0.85rem; color:#AAAAAA; line-height:1.8;
  }
  .tr-info strong { color:#F0F0F0; }

  .tr-success {
    background:#0D1F0D; border:1px solid #2A5A2A; border-left:4px solid #4CAF50;
    border-radius:0 8px 8px 0; padding:14px 18px;
    margin:20px 0; font-size:0.85rem; color:#90EE90; line-height:1.9;
  }
  .tr-success strong { color:#AAFFAA; }

  .tr-error {
    background:#2A1A1A; border-left:3px solid #FF4444;
    border-radius:0 8px 8px 0; padding:14px 18px;
    margin:12px 0; font-size:0.85rem; color:#FF9999;
  }

  .integrity-box {
    border-radius:10px; padding:18px 20px;
    margin:20px 0; font-size:0.85rem; line-height:1.9;
  }
  .integrity-ok {
    background:#0D1F0D; border:1px solid #2A5A2A; border-left:4px solid #4CAF50;
  }
  .integrity-fail {
    background:#1F0D0D; border:1px solid #5A2A2A; border-left:4px solid #FF4444;
  }
  .integrity-ok   strong { color:#90EE90; }
  .integrity-fail strong { color:#FF9999; }
  .integrity-ok   span   { color:#6DBF6D; }
  .integrity-fail span   { color:#FF8888; }

  .preview-bar {
    background:#1E1E1E; border:1px solid #2A2A2A; border-radius:8px;
    padding:12px 16px; margin-top:8px; margin-bottom:8px;
    font-size:0.83rem; color:#888888;
  }
  .pv-val { color:#FF8000; font-weight:700; font-size:1rem; }

  .batch-table {
    width:100%; border-collapse:collapse;
    margin:16px 0 24px 0; font-size:0.82rem;
  }
  .batch-table th {
    background:#2A2A2A; color:#FF8000; font-weight:600;
    text-transform:uppercase; letter-spacing:1px;
    padding:10px 14px; text-align:left; border-bottom:1px solid #3A3A3A;
  }
  .batch-table td { padding:9px 14px; color:#CCCCCC; border-bottom:1px solid #2A2A2A; }
  .batch-table tr:last-child td { border-bottom:none; }
  .batch-table tr:hover td      { background:#242424; }

  .badge     { display:inline-block; background:#FF800022; color:#FF8000;
               border:1px solid #FF800055; border-radius:20px;
               padding:2px 10px; font-size:0.75rem; font-weight:600; }
  .badge-ok  { background:#00AA4422 !important; color:#4CAF50 !important;
               border-color:#4CAF5055 !important; }

  div[data-testid="stVerticalBlockBorderWrapper"] {
    background:#242424 !important; border:2px solid #333333 !important;
    border-radius:12px !important; transition:all 0.2s !important;
  }
  div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color:#FF8000 !important; box-shadow:0 4px 20px #FF800033 !important;
  }

  .stButton > button {
    width:100% !important; background:transparent !important;
    color:#777777 !important; border:1px solid #333333 !important;
    border-radius:8px !important; padding:8px !important;
    font-size:0.78rem !important; font-weight:500 !important;
    transition:all 0.2s !important; margin-top:4px !important;
  }
  .stButton > button:hover {
    background:#FF800015 !important; color:#FF8000 !important;
    border-color:#FF8000 !important;
  }

  .btn-processar .stButton > button {
    background:linear-gradient(135deg,#FF8000 0%,#E06000 100%) !important;
    color:#FFFFFF !important; border:none !important;
    border-radius:8px !important; padding:14px 20px !important;
    font-size:0.95rem !important; font-weight:600 !important; margin-top:8px !important;
  }
  .btn-processar .stButton > button:hover {
    background:linear-gradient(135deg,#FF9520 0%,#FF8000 100%) !important;
    box-shadow:0 4px 20px #FF800055 !important;
  }

  .stDownloadButton > button {
    width:100% !important; background:#242424 !important;
    color:#FF8000 !important; border:1.5px solid #FF8000 !important;
    border-radius:8px !important; padding:13px 20px !important;
    font-size:0.95rem !important; font-weight:600 !important; transition:all 0.2s !important;
  }
  .stDownloadButton > button:hover {
    background:#FF800015 !important; box-shadow:0 4px 20px #FF800033 !important;
  }

  [data-testid="stProgressBar"] > div { background:#333333 !important; border-radius:4px !important; }
  [data-testid="stProgressBar"] > div > div {
    background:linear-gradient(90deg,#FF8000,#FFB347) !important; border-radius:4px !important;
  }

  [data-testid="metric-container"] {
    background:#242424 !important; border:1px solid #333333 !important;
    border-radius:10px !important; padding:16px 20px !important;
  }
  [data-testid="metric-container"] label {
    color:#888888 !important; font-size:0.75rem !important;
    text-transform:uppercase !important; letter-spacing:1px !important;
  }
  [data-testid="stMetricValue"] {
    color:#FF8000 !important; font-size:1.8rem !important; font-weight:700 !important;
  }

  [data-testid="stFileUploaderDropzone"] {
    background-color:#242424 !important; border:1.5px dashed #444444 !important; border-radius:10px !important;
  }
  [data-testid="stFileUploaderDropzone"] p   { color:#888888 !important; }
  [data-testid="stFileUploaderDropzone"] svg { fill:#FF8000 !important; }

  div[data-baseweb="radio"] label {
    color:#CCCCCC !important;
  }

  div[data-testid="stCheckbox"] label {
    color:#CCCCCC !important;
  }

  #MainMenu { visibility:hidden; } footer { visibility:hidden; } header { visibility:hidden; }
  hr { border-color:#333333 !important; margin:24px 0 !important; }
  ::-webkit-scrollbar       { width:6px; }
  ::-webkit-scrollbar-track { background:#1A1A1A; }
  ::-webkit-scrollbar-thumb { background:#444444; border-radius:3px; }
  ::-webkit-scrollbar-thumb:hover { background:#FF8000; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# CONSTANTES
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
# FUNÇÕES GERAIS
# ─────────────────────────────────────────────

def fmt(n: int) -> str:
    return f"{n:,}".replace(",", ".")


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


def limpar_nome_zip(nome: str) -> str:
    nome = nome.replace(".", "").replace(" ", "_")
    nome = nome.replace("/", "_").replace("\\", "_")
    return nome


# ─────────────────────────────────────────────
# FUNÇÕES PARA REMOVER PIPE
# ─────────────────────────────────────────────

def normalizar_descricao_produto(texto):
    """
    Remove PIPE e espaços duplicados.
    """

    if texto is None:
        return ""

    texto = texto.replace("|", "")
    texto = " ".join(texto.split())

    return texto


def extrair_namespace(root):
    namespace = ""

    if root.tag.startswith("{"):
        namespace = root.tag.split("}")[0] + "}"

    return namespace


def remover_pipe_xml(xml_bytes: bytes, nome_arquivo: str):
    """
    Remove o caractere | da tag xProd.
    Também remove espaços duplicados automaticamente.
    """

    alteracoes = []

    try:
        tree = ET.ElementTree(ET.fromstring(xml_bytes))
        root = tree.getroot()
        namespace = extrair_namespace(root)

        chave_nfe = ""
        numero_nota = ""
        modelo = ""
        natureza_operacao = ""

        inf_nfe = root.find(f".//{namespace}infNFe")
        if inf_nfe is not None:
            chave_nfe = inf_nfe.attrib.get("Id", "").replace("NFe", "")

        ide = root.find(f".//{namespace}ide")
        if ide is not None:
            n_nf = ide.find(f"{namespace}nNF")
            mod = ide.find(f"{namespace}mod")
            nat_op = ide.find(f"{namespace}natOp")

            if n_nf is not None and n_nf.text:
                numero_nota = n_nf.text

            if mod is not None and mod.text:
                modelo = mod.text

            if nat_op is not None and nat_op.text:
                natureza_operacao = nat_op.text

        produtos = root.findall(f".//{namespace}prod")

        for prod in produtos:
            xprod = prod.find(f"{namespace}xProd")
            cprod = prod.find(f"{namespace}cProd")
            ncm = prod.find(f"{namespace}NCM")
            cfop = prod.find(f"{namespace}CFOP")

            if xprod is not None and xprod.text:
                descricao_original = xprod.text
                descricao_corrigida = normalizar_descricao_produto(descricao_original)

                if descricao_original != descricao_corrigida:
                    xprod.text = descricao_corrigida

                    alteracoes.append({
                        "arquivo": nome_arquivo,
                        "numero_nota": numero_nota,
                        "modelo": modelo,
                        "chave_nfe": chave_nfe,
                        "natureza_operacao": natureza_operacao,
                        "codigo_produto": cprod.text if cprod is not None and cprod.text else "",
                        "ncm": ncm.text if ncm is not None and ncm.text else "",
                        "cfop": cfop.text if cfop is not None and cfop.text else "",
                        "descricao_original": descricao_original,
                        "descricao_corrigida": descricao_corrigida,
                    })

        houve_alteracao = len(alteracoes) > 0

        if houve_alteracao:
            output = io.BytesIO()
            tree.write(
                output,
                encoding="utf-8",
                xml_declaration=True
            )
            xml_corrigido = output.getvalue()
        else:
            xml_corrigido = xml_bytes

        return xml_corrigido, houve_alteracao, alteracoes, None

    except Exception as e:
        return xml_bytes, False, [], str(e)


def gerar_csv_alteracoes(relatorio):
    colunas = [
        "arquivo",
        "numero_nota",
        "modelo",
        "chave_nfe",
        "natureza_operacao",
        "codigo_produto",
        "ncm",
        "cfop",
        "descricao_original",
        "descricao_corrigida",
    ]

    texto = ";".join(colunas) + "\n"

    for item in relatorio:
        linha = []

        for coluna in colunas:
            valor = str(item.get(coluna, ""))
            valor = valor.replace(";", ",")
            valor = valor.replace("\n", " ")
            valor = valor.replace("\r", " ")
            linha.append(valor)

        texto += ";".join(linha) + "\n"

    return texto.encode("utf-8-sig")


def processar_zip_removendo_pipe(zip_bytes: bytes):
    """
    Recebe um ZIP com XMLs e retorna:
    - ZIP corrigido
    - relatório de alterações
    - erros
    - total_xmls
    - notas_alteradas
    - itens_alterados
    """

    relatorio = []
    erros = []
    total_xmls = 0
    notas_alteradas = 0
    itens_alterados = 0

    entrada_buf = io.BytesIO(zip_bytes)
    saida_buf = io.BytesIO()

    with zipfile.ZipFile(entrada_buf, "r") as zip_in:
        nomes_xml = [
            n for n in zip_in.namelist()
            if n.lower().endswith(".xml")
            and "__MACOSX" not in n
            and not os.path.basename(n).startswith(".")
        ]

        total_xmls = len(nomes_xml)

        with zipfile.ZipFile(saida_buf, "w", zipfile.ZIP_DEFLATED) as zip_out:
            for nome_xml in nomes_xml:
                try:
                    xml_bytes = zip_in.read(nome_xml)

                    xml_corrigido, houve_alteracao, alteracoes, erro = remover_pipe_xml(
                        xml_bytes,
                        os.path.basename(nome_xml)
                    )

                    arcname = os.path.basename(nome_xml)
                    zip_out.writestr(arcname, xml_corrigido)

                    if erro:
                        erros.append({
                            "arquivo": nome_xml,
                            "erro": erro
                        })

                    if houve_alteracao:
                        notas_alteradas += 1
                        itens_alterados += len(alteracoes)
                        relatorio.extend(alteracoes)

                except Exception as e:
                    erros.append({
                        "arquivo": nome_xml,
                        "erro": str(e)
                    })

    saida_buf.seek(0)

    return {
        "zip_corrigido": saida_buf.getvalue(),
        "relatorio": relatorio,
        "erros": erros,
        "total_xmls": total_xmls,
        "notas_alteradas": notas_alteradas,
        "itens_alterados": itens_alterados,
    }


# ─────────────────────────────────────────────
# FUNÇÕES DE DIVISÃO
# ─────────────────────────────────────────────

def validar_integridade(zip_original_bytes: bytes, zip_master_bytes: bytes) -> dict:
    originais = ler_xmls_do_zip(zip_original_bytes)
    total_original = len(originais)
    nomes_originais = set(os.path.basename(n) for n in originais)

    total_contado = 0
    nomes_contados = set()
    lotes_info = []

    master_buf = io.BytesIO(zip_master_bytes)

    with zipfile.ZipFile(master_buf, "r") as master_zip:
        lote_names = sorted([n for n in master_zip.namelist() if n.endswith(".zip")])

        for lote_name in lote_names:
            lote_bytes = master_zip.read(lote_name)
            lote_buf = io.BytesIO(lote_bytes)

            with zipfile.ZipFile(lote_buf, "r") as lote_zip:
                xmls_no_lote = [
                    n for n in lote_zip.namelist()
                    if n.lower().endswith(".xml")
                    and not os.path.basename(n).startswith(".")
                ]

                total_contado += len(xmls_no_lote)

                for x in xmls_no_lote:
                    nomes_contados.add(os.path.basename(x))

                lotes_info.append({
                    "nome": lote_name,
                    "quantidade": len(xmls_no_lote),
                })

    duplicados = total_contado - len(nomes_contados)
    perdidos = nomes_originais - nomes_contados
    extras = nomes_contados - nomes_originais
    diferenca = total_contado - total_original

    return {
        "total_original": total_original,
        "total_contado": total_contado,
        "diferenca": diferenca,
        "duplicados": duplicados,
        "perdidos": sorted(perdidos)[:20],
        "extras": sorted(extras)[:20],
        "total_perdidos": len(perdidos),
        "total_extras": len(extras),
        "lotes_info": lotes_info,
        "ok": (
            total_original == total_contado
            and duplicados == 0
            and len(perdidos) == 0
        ),
    }


def gerar_lotes_zip(zip_bytes: bytes, files_per_batch: int, remover_pipe_antes=False):
    """
    Divide XMLs em lotes.
    Se remover_pipe_antes=True, remove PIPE dos XMLs antes de gerar os lotes.
    """

    xml_files = ler_xmls_do_zip(zip_bytes)

    if not xml_files:
        raise ValueError("Nenhum XML encontrado no ZIP.")

    total_files = len(xml_files)
    total_batches = math.ceil(total_files / files_per_batch)

    groups = [
        xml_files[i * files_per_batch: (i + 1) * files_per_batch]
        for i in range(total_batches)
    ]

    relatorio_pipe = []
    erros_pipe = []
    notas_alteradas = 0
    itens_alterados = 0

    src_buf = io.BytesIO(zip_bytes)
    master_buf = io.BytesIO()

    with zipfile.ZipFile(src_buf, "r") as src_zip:
        with zipfile.ZipFile(master_buf, "w", zipfile.ZIP_DEFLATED) as master_zip:
            for idx, group in enumerate(groups, start=1):
                batch_buf = io.BytesIO()

                with zipfile.ZipFile(batch_buf, "w", zipfile.ZIP_DEFLATED) as batch_zip:
                    for xml_path in group:
                        data = src_zip.read(xml_path)
                        arcname = os.path.basename(xml_path)

                        if remover_pipe_antes:
                            xml_corrigido, houve_alteracao, alteracoes, erro = remover_pipe_xml(
                                data,
                                arcname
                            )

                            data = xml_corrigido

                            if erro:
                                erros_pipe.append({
                                    "arquivo": xml_path,
                                    "erro": erro
                                })

                            if houve_alteracao:
                                notas_alteradas += 1
                                itens_alterados += len(alteracoes)
                                relatorio_pipe.extend(alteracoes)

                        batch_zip.writestr(arcname, data)

                master_zip.writestr(f"lote_{idx:03d}.zip", batch_buf.getvalue())

    master_buf.seek(0)

    return {
        "master_bytes": master_buf.getvalue(),
        "groups": groups,
        "total_files": total_files,
        "total_batches": total_batches,
        "relatorio_pipe": relatorio_pipe,
        "erros_pipe": erros_pipe,
        "notas_alteradas": notas_alteradas,
        "itens_alterados": itens_alterados,
    }


# ─────────────────────────────────────────────
# HEADER
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
st.markdown("## Utilitário de XMLs Fiscais")
st.markdown(
    "<p style='color:#888888; font-size:0.9rem; margin-top:-10px; margin-bottom:24px;'>"
    "Remova o caractere PIPE das descrições dos produtos ou divida XMLs em lotes compactados."
    "</p>",
    unsafe_allow_html=True,
)

st.markdown("""
<div class="tr-info">
  <strong>📌 Como funciona</strong><br>
  &bull; Envie um <strong>.zip</strong> contendo XMLs fiscais<br>
  &bull; Escolha entre <strong>remover PIPE</strong> ou <strong>dividir XMLs em lotes</strong><br>
  &bull; A remoção de PIPE atua somente na tag <strong>&lt;xProd&gt;</strong><br>
  &bull; Ao remover PIPE, os espaços duplicados são corrigidos automaticamente
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MODO DE OPERAÇÃO
# ─────────────────────────────────────────────

st.markdown('<div class="section-label">1 — Modo de operação</div>', unsafe_allow_html=True)

modo_operacao = st.radio(
    "Escolha o que deseja fazer",
    [
        "Remover PIPE dos XMLs",
        "Dividir XMLs em lotes",
    ],
    horizontal=True,
)

st.markdown('<div class="section-label" style="margin-top:24px">2 — Arquivo de entrada</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Selecione ou arraste o arquivo ZIP com os XMLs",
    type=["zip"],
    help="Apenas arquivos .zip são aceitos.",
)

total_xmls_preview = 0

if uploaded_file is not None:
    try:
        total_xmls_preview = len(ler_xmls_do_zip(uploaded_file.getvalue()))

        st.markdown(f"""
        <div class="preview-bar">
          📦 &nbsp; Arquivo carregado com
          <span class="pv-val">{fmt(total_xmls_preview)}</span> XMLs encontrados.
        </div>
        """, unsafe_allow_html=True)

    except Exception:
        total_xmls_preview = 0
        st.markdown(
            '<div class="tr-error">⚠️ Não foi possível ler o ZIP enviado.</div>',
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────
# MODO 1 — REMOVER PIPE
# ─────────────────────────────────────────────

if modo_operacao == "Remover PIPE dos XMLs":

    st.markdown(
        '<div class="section-label" style="margin-top:24px">3 — Remoção de PIPE</div>',
        unsafe_allow_html=True,
    )

    st.markdown("""
    <div class="tr-info">
      Esta opção gera um novo ZIP com os XMLs corrigidos.<br>
      São removidos os caracteres <strong>|</strong> apenas da tag <strong>&lt;xProd&gt;</strong>.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="btn-processar">', unsafe_allow_html=True)
    process_btn_pipe = st.button("⚡ Remover PIPE e gerar ZIP corrigido")
    st.markdown('</div>', unsafe_allow_html=True)

    if process_btn_pipe:

        if uploaded_file is None:
            st.markdown(
                '<div class="tr-error">⚠️ Nenhum arquivo enviado. Faça o upload antes de processar.</div>',
                unsafe_allow_html=True,
            )
            st.stop()

        file_bytes = uploaded_file.getvalue()

        try:
            resultado = processar_zip_removendo_pipe(file_bytes)

            st.session_state["pipe_processado"] = True
            st.session_state["pipe_resultado"] = resultado

        except zipfile.BadZipFile:
            st.markdown(
                '<div class="tr-error">⚠️ Arquivo ZIP inválido ou corrompido.</div>',
                unsafe_allow_html=True,
            )
            st.stop()

        except Exception as e:
            st.markdown(
                f'<div class="tr-error">⚠️ Erro ao processar o ZIP: {e}</div>',
                unsafe_allow_html=True,
            )
            st.stop()

    if st.session_state.get("pipe_processado"):

        resultado = st.session_state["pipe_resultado"]

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("XMLs processados", fmt(resultado["total_xmls"]))
        with c2:
            st.metric("Notas alteradas", fmt(resultado["notas_alteradas"]))
        with c3:
            st.metric("Itens alterados", fmt(resultado["itens_alterados"]))
        with c4:
            st.metric("Erros", fmt(len(resultado["erros"])))

        if resultado["notas_alteradas"] > 0:
            st.markdown(f"""
            <div class="tr-success">
              <strong>✅ Remoção concluída!</strong><br>
              &bull; <strong>{fmt(resultado["notas_alteradas"])}</strong> nota(s) alterada(s)<br>
              &bull; <strong>{fmt(resultado["itens_alterados"])}</strong> item(ns) alterado(s)<br>
              &bull; Espaços duplicados foram corrigidos automaticamente
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="tr-success">
              <strong>✅ Processamento concluído!</strong><br>
              Nenhuma descrição com PIPE foi encontrada nos XMLs.
            </div>
            """, unsafe_allow_html=True)

        if resultado["relatorio"]:
            with st.expander("📋 Ver relatório de alterações"):
                st.dataframe(resultado["relatorio"], use_container_width=True)

            csv_bytes = gerar_csv_alteracoes(resultado["relatorio"])

            st.download_button(
                label="⬇️ Baixar relatório CSV de alterações",
                data=csv_bytes,
                file_name="relatorio_remocao_pipe.csv",
                mime="text/csv",
            )

        if resultado["erros"]:
            with st.expander("⚠️ Ver erros encontrados"):
                st.dataframe(resultado["erros"], use_container_width=True)

        st.download_button(
            label="⬇️ Baixar XMLs corrigidos em ZIP",
            data=resultado["zip_corrigido"],
            file_name="xmls_corrigidos_sem_pipe.zip",
            mime="application/zip",
        )


# ─────────────────────────────────────────────
# MODO 2 — DIVIDIR XMLS
# ─────────────────────────────────────────────

if modo_operacao == "Dividir XMLs em lotes":

    st.markdown(
        '<div class="section-label" style="margin-top:24px">3 — Tamanho do lote</div>',
        unsafe_allow_html=True,
    )

    if "lote_selecionado" not in st.session_state:
        st.session_state.lote_selecionado = "5.000 XMLs"

    opcoes_list = list(OPCOES_LOTE.keys())
    valores_list = list(OPCOES_LOTE.values())

    col1, col2, col3 = st.columns(3)

    for col, label, valor in zip([col1, col2, col3], opcoes_list, valores_list):
        with col:
            with st.container(border=True):
                ativo = label == st.session_state.lote_selecionado
                num_color = "#FF8000" if ativo else "#555555"

                st.markdown(
                    f"<div style='text-align:center; font-size:1.8rem; font-weight:700;"
                    f"color:{num_color}; line-height:1; margin-bottom:2px;'>"
                    f"{label.replace(' XMLs','')}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    "<div style='text-align:center; font-size:0.68rem; color:#666666;"
                    "text-transform:uppercase; letter-spacing:1.2px;'>XMLs por lote</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(
                    f"<div style='text-align:center; font-size:0.73rem; color:#555555;"
                    f"margin-top:6px; min-height:32px'>{DESCRICOES_LOTE[label]}</div>",
                    unsafe_allow_html=True,
                )

                if total_xmls_preview > 0:
                    lotes_est = math.ceil(total_xmls_preview / valor)
                    est_txt = f"📊 {fmt(lotes_est)} lotes"
                    est_color = "#FF8000AA" if ativo else "#444444"
                else:
                    est_txt = "📊 aguardando arquivo"
                    est_color = "#444444"

                st.markdown(
                    f"<div style='text-align:center; font-size:0.73rem;"
                    f"color:{est_color}; margin-top:4px;'>{est_txt}</div>",
                    unsafe_allow_html=True,
                )

                btn_label = "✔ Selecionado" if ativo else "Selecionar"
                if st.button(btn_label, key=f"btn_{valor}", disabled=ativo):
                    st.session_state.lote_selecionado = label
                    st.rerun()

    opcao_selecionada = st.session_state.lote_selecionado
    files_per_batch = OPCOES_LOTE[opcao_selecionada]

    if total_xmls_preview > 0:
        lotes_calc = math.ceil(total_xmls_preview / files_per_batch)
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

    st.markdown(
        '<div class="section-label" style="margin-top:24px">4 — Opções adicionais</div>',
        unsafe_allow_html=True,
    )

    remover_pipe_antes_dividir = st.checkbox(
        "Remover PIPE das descrições dos produtos antes de dividir os XMLs",
        value=False,
        help="Se marcado, o sistema remove o caractere | da tag xProd antes de gerar os lotes.",
    )

    st.markdown(
        '<div class="section-label" style="margin-top:24px">5 — Processar</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="btn-processar">', unsafe_allow_html=True)
    process_btn_dividir = st.button(
        f"⚡ Gerar lotes de {opcao_selecionada} zipados individualmente"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if process_btn_dividir:

        if uploaded_file is None:
            st.markdown(
                '<div class="tr-error">⚠️ Nenhum arquivo enviado. Faça o upload antes de processar.</div>',
                unsafe_allow_html=True,
            )
            st.stop()

        file_bytes = uploaded_file.getvalue()

        try:
            progress_bar = st.progress(0, text="Iniciando processamento...")
            progress_bar.progress(0.25, text="Lendo XMLs do ZIP...")

            resultado_divisao = gerar_lotes_zip(
                zip_bytes=file_bytes,
                files_per_batch=files_per_batch,
                remover_pipe_antes=remover_pipe_antes_dividir,
            )

            progress_bar.progress(0.80, text="Validando lotes gerados...")

            st.session_state["divisao_processado"] = True
            st.session_state["zip_original_bytes"] = file_bytes
            st.session_state["zip_master_bytes"] = resultado_divisao["master_bytes"]
            st.session_state["groups"] = resultado_divisao["groups"]
            st.session_state["total_files"] = resultado_divisao["total_files"]
            st.session_state["total_batches"] = resultado_divisao["total_batches"]
            st.session_state["opcao_selecionada"] = opcao_selecionada
            st.session_state["files_per_batch"] = files_per_batch
            st.session_state["remover_pipe_antes_dividir"] = remover_pipe_antes_dividir
            st.session_state["relatorio_pipe_divisao"] = resultado_divisao["relatorio_pipe"]
            st.session_state["erros_pipe_divisao"] = resultado_divisao["erros_pipe"]
            st.session_state["notas_alteradas_divisao"] = resultado_divisao["notas_alteradas"]
            st.session_state["itens_alterados_divisao"] = resultado_divisao["itens_alterados"]

            progress_bar.progress(1.0, text="Processamento concluído!")

        except zipfile.BadZipFile:
            st.markdown(
                '<div class="tr-error">⚠️ Arquivo ZIP inválido ou corrompido.</div>',
                unsafe_allow_html=True,
            )
            st.stop()

        except Exception as e:
            st.markdown(
                f'<div class="tr-error">⚠️ Erro ao processar: {e}</div>',
                unsafe_allow_html=True,
            )
            st.stop()

    if st.session_state.get("divisao_processado"):

        master_bytes = st.session_state["zip_master_bytes"]
        file_bytes_orig = st.session_state["zip_original_bytes"]
        groups = st.session_state["groups"]
        total_files = st.session_state["total_files"]
        total_batches = st.session_state["total_batches"]
        opcao_selecionada = st.session_state["opcao_selecionada"]
        files_per_batch = st.session_state["files_per_batch"]
        remover_pipe_antes_dividir = st.session_state["remover_pipe_antes_dividir"]

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric("Total de XMLs", fmt(total_files))
        with c2:
            st.metric("Lotes gerados", fmt(total_batches))
        with c3:
            st.metric("Último lote", f"{fmt(len(groups[-1]))} XMLs")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">✅ Validador de integridade</div>', unsafe_allow_html=True)

        with st.spinner("Verificando integridade dos lotes gerados..."):
            v = validar_integridade(file_bytes_orig, master_bytes)

        vc1, vc2, vc3, vc4 = st.columns(4)

        with vc1:
            st.metric("XMLs originais", fmt(v["total_original"]))
        with vc2:
            st.metric("XMLs nos lotes", fmt(v["total_contado"]))
        with vc3:
            st.metric(
                "Diferença",
                fmt(abs(v["diferenca"])),
                delta=None if v["diferenca"] == 0 else f"{v['diferenca']:+d}",
            )
        with vc4:
            st.metric("Duplicados", str(v["duplicados"]))

        if v["ok"]:
            st.markdown(f"""
            <div class="integrity-box integrity-ok">
              <strong>✅ Integridade confirmada — nenhum XML perdido ou duplicado!</strong><br>
              <span>
                &bull; XMLs no arquivo original: <strong>{fmt(v['total_original'])}</strong><br>
                &bull; XMLs distribuídos nos lotes: <strong>{fmt(v['total_contado'])}</strong><br>
                &bull; Diferença: <strong>0</strong> — 100% dos arquivos foram preservados<br>
                &bull; Duplicados detectados: <strong>0</strong>
              </span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="integrity-box integrity-fail">
              <strong>⚠️ Atenção — inconsistência detectada!</strong><br>
              <span>
                &bull; XMLs no arquivo original: <strong>{fmt(v['total_original'])}</strong><br>
                &bull; XMLs distribuídos nos lotes: <strong>{fmt(v['total_contado'])}</strong><br>
                &bull; Diferença: <strong>{v['diferenca']:+d}</strong><br>
              </span>
            </div>
            """, unsafe_allow_html=True)

        if remover_pipe_antes_dividir:
            st.markdown('<div class="section-label">🧹 Remoção de PIPE aplicada</div>', unsafe_allow_html=True)

            notas_alt = st.session_state["notas_alteradas_divisao"]
            itens_alt = st.session_state["itens_alterados_divisao"]
            erros_pipe = st.session_state["erros_pipe_divisao"]
            relatorio_pipe = st.session_state["relatorio_pipe_divisao"]

            pc1, pc2, pc3 = st.columns(3)

            with pc1:
                st.metric("Notas alteradas", fmt(notas_alt))
            with pc2:
                st.metric("Itens alterados", fmt(itens_alt))
            with pc3:
                st.metric("Erros PIPE", fmt(len(erros_pipe)))

            if relatorio_pipe:
                with st.expander("📋 Ver relatório de PIPE removido"):
                    st.dataframe(relatorio_pipe, use_container_width=True)

                st.download_button(
                    label="⬇️ Baixar relatório CSV de PIPE removido",
                    data=gerar_csv_alteracoes(relatorio_pipe),
                    file_name="relatorio_pipe_removido_lotes.csv",
                    mime="text/csv",
                )

            if erros_pipe:
                with st.expander("⚠️ Ver erros na remoção de PIPE"):
                    st.dataframe(erros_pipe, use_container_width=True)

        with st.expander("📋 Ver detalhamento por lote"):
            rows = ""

            for i, (lote, group) in enumerate(zip(v["lotes_info"], groups), start=1):
                is_last = i == total_batches
                badge_class = "badge badge-ok" if is_last else "badge"

                obs = (
                    f"Último lote ({fmt(len(group))} de {fmt(files_per_batch)})"
                    if is_last else "Lote completo"
                )

                match = "✅" if lote["quantidade"] == len(group) else "⚠️"

                rows += f"""
                <tr>
                  <td><code style="color:#FF8000">{lote['nome']}</code></td>
                  <td><span class="{badge_class}">{fmt(lote['quantidade'])} XMLs</span></td>
                  <td style="color:#555555">{obs}</td>
                  <td style="text-align:center">{match}</td>
                </tr>
                """

            st.markdown(f"""
            <table class="batch-table">
              <thead>
                <tr>
                  <th>Arquivo ZIP</th>
                  <th>Quantidade</th>
                  <th>Observação</th>
                  <th style="text-align:center">OK?</th>
                </tr>
              </thead>
              <tbody>{rows}</tbody>
            </table>
            """, unsafe_allow_html=True)

        extra_pipe_txt = ""

        if remover_pipe_antes_dividir:
            extra_pipe_txt = (
                f"<br>&bull; PIPE removido antes da divisão em "
                f"<strong>{fmt(st.session_state['notas_alteradas_divisao'])}</strong> nota(s)"
            )

        st.markdown(f"""
        <div class="tr-success">
          <strong>✅ Processamento concluído!</strong><br>
          &bull; <strong>{fmt(total_files)}</strong> XMLs distribuídos em
                 <strong>{fmt(total_batches)}</strong> lotes zipados<br>
          &bull; Cada lote contém até <strong>{fmt(files_per_batch)}</strong> arquivos XML<br>
          &bull; Último lote: <strong>{fmt(len(groups[-1]))}</strong> arquivo(s)
          {extra_pipe_txt}<br>
          &bull; Estrutura: <code style="color:#90EE90">lotes_xml.zip</code>
                 &rarr; <code style="color:#90EE90">lote_001.zip</code>,
                 <code style="color:#90EE90">lote_002.zip</code> ...
        </div>
        """, unsafe_allow_html=True)

        nome_arquivo = limpar_nome_zip(opcao_selecionada)

        sufixo_pipe = "_sem_pipe" if remover_pipe_antes_dividir else ""

        st.download_button(
            label=f"⬇️ Baixar lotes_xml.zip  ({fmt(total_batches)} lotes de {opcao_selecionada})",
            data=master_bytes,
            file_name=f"lotes_xml_{nome_arquivo}{sufixo_pipe}.zip",
            mime="application/zip",
        )


# ─────────────────────────────────────────────
# RODAPÉ
# ─────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#444444; font-size:0.75rem;
            border-top:1px solid #2A2A2A; padding-top:16px;">
  Domínio Sistemas &middot; Thomson Reuters &nbsp;|&nbsp;
  Utilitário de XMLs Fiscais &nbsp;|&nbsp;
  <span style="color:#FF800088;">Uso interno</span>
</div>
""", unsafe_allow_html=True)
