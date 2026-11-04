#!/usr/bin/env python3
"""Junta as páginas do manual num HTML só e imprime o PDF em paisagem 16:9.

O diagramador escreve UMA página por arquivo em `partes/NN_nome.html`, cada uma
assim:

    <section class="pagina">
      <div class="cabecalho"><span class="marca">NOME DA MARCA</span><span>Paleta de cores</span></div>
      ... conteúdo ...
      <div class="num"></div>
    </section>

Este script:
  1. ordena os arquivos pelo número do nome;
  2. embute imagens (png/jpg/svg) e fontes (.ttf/.otf/.woff2) dentro do HTML, para o
     arquivo ficar inteiro num lugar só e o navegador não depender de caminho;
  3. gera `manual.html`;
  4. imprime `Manual_de_Marca.pdf` com o chromium (ou weasyprint, se for o que houver);
  5. confere o número de páginas e o tamanho da página, e reclama se estiver errado.

Uso:
  python3 juntar_manual.py --pasta marca/manual --pdf marca/Manual_de_Marca.pdf
  python3 juntar_manual.py --pasta marca/manual --so-html      # só monta o HTML

Estrutura esperada dentro de --pasta:
  partes/01_capa.html, partes/02_indice.html, ...
  marca.css          (as variáveis --marca-* desta marca; opcional mas recomendado)
  ../arquivos/...    (logos e imagens; qualquer caminho relativo funciona)
"""
import argparse
import base64
import glob
import mimetypes
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE_CSS = os.path.join(AQUI, "manual_base.css")

CHROMIUMS = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
             "chrome"]


# Windows e Mac: o Chrome/Edge não fica no PATH, então procuramos nos lugares de instalação.
CAMINHOS_FIXOS = [
    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
    os.path.expandvars(r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"),
    os.path.expandvars(r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def achar_chromium():
    for c in CHROMIUMS + ["msedge"]:
        caminho = shutil.which(c)
        if caminho:
            return caminho
    for caminho in CAMINHOS_FIXOS:
        if "%" not in caminho and os.path.isfile(caminho):
            return caminho
    return None


def data_uri(caminho):
    tipo = mimetypes.guess_type(caminho)[0] or "application/octet-stream"
    with open(caminho, "rb") as f:
        return "data:{};base64,{}".format(tipo, base64.b64encode(f.read()).decode("ascii"))


def embutir_imagens(html, base_dir):
    """Troca src="arquivo.png" por src="data:image/png;base64,...". Deixa http(s) e
    data: como estão."""
    faltando = []

    def troca(m):
        aspas, alvo = m.group(1), m.group(2)
        if alvo.startswith(("data:", "http:", "https:", "#")):
            return m.group(0)
        caminho = os.path.normpath(os.path.join(base_dir, alvo))
        if not os.path.exists(caminho):
            faltando.append(alvo)
            return m.group(0)
        return 'src={0}{1}{0}'.format(aspas, data_uri(caminho))

    html = re.sub(r'src=(["\'])([^"\']+)\1', troca, html)
    return html, faltando


def css_das_fontes(pasta_fontes):
    """Monta @font-face embutidos a partir dos arquivos em pasta_fontes.
    Nome do arquivo manda: `Manrope_800.ttf` vira família "Manrope", peso 800."""
    if not pasta_fontes or not os.path.isdir(pasta_fontes):
        return ""
    regras = []
    for arq in sorted(glob.glob(os.path.join(pasta_fontes, "*"))):
        ext = os.path.splitext(arq)[1].lower()
        if ext not in (".ttf", ".otf", ".woff2", ".woff"):
            continue
        nome = os.path.splitext(os.path.basename(arq))[0]
        partes = nome.rsplit("_", 1)
        familia = partes[0].replace("_", " ")
        peso = partes[1] if len(partes) > 1 and partes[1].isdigit() else "400"
        formato = {".ttf": "truetype", ".otf": "opentype",
                   ".woff2": "woff2", ".woff": "woff"}[ext]
        regras.append(
            '@font-face{{font-family:"{}";font-weight:{};font-style:normal;'
            'font-display:block;src:url({}) format("{}");}}'.format(
                familia, peso, data_uri(arq), formato)
        )
    return "\n".join(regras)


def montar(pasta, pasta_fontes=None):
    partes_dir = os.path.join(pasta, "partes")
    arquivos = sorted(glob.glob(os.path.join(partes_dir, "*.html")))
    if not arquivos:
        raise SystemExit("Nenhuma página em {}. O diagramador escreve uma página por "
                         "arquivo, com nome NN_nome.html.".format(partes_dir))

    avisos = []
    corpo = []
    for arq in arquivos:
        with open(arq, encoding="utf-8") as f:
            trecho = f.read().strip()
        n = trecho.count('class="pagina')
        if n != 1:
            avisos.append("{}: {} blocos .pagina (o certo é 1 por arquivo)".format(
                os.path.basename(arq), n))
        sem_numero = ("pagina--capa" in trecho or "pagina--divisoria" in trecho
                      or "pagina--contracapa" in trecho)
        if 'class="num"' not in trecho and not sem_numero:
            avisos.append("{}: sem <div class=\"num\"></div> (a página sai sem número)"
                          .format(os.path.basename(arq)))
        corpo.append("<!-- {} -->\n{}".format(os.path.basename(arq), trecho))

    with open(BASE_CSS, encoding="utf-8") as f:
        css = f.read()
    marca_css_path = os.path.join(pasta, "marca.css")
    if os.path.exists(marca_css_path):
        with open(marca_css_path, encoding="utf-8") as f:
            css += "\n\n/* marca.css */\n" + f.read()
    else:
        avisos.append("sem marca.css: o manual sai com as cores neutras do padrão")

    fontes = css_das_fontes(pasta_fontes)

    html = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<title>Manual de Marca</title>\n<style>\n{}\n</style>\n<style>\n{}\n</style>\n"
            "</head>\n<body>\n{}\n</body>\n</html>\n").format(
        fontes, css, "\n".join(corpo))

    html, faltando = embutir_imagens(html, partes_dir)
    for alvo in dict.fromkeys(faltando):
        avisos.append("imagem não encontrada, ficou como link quebrado: {}".format(alvo))

    return html, len(arquivos), avisos


def imprimir_pdf(html_path, pdf_path):
    """Tenta chromium; se o chromium não conseguir ler o caminho (snap não enxerga
    /tmp nem pasta fora da home), repete a partir da home. Por último, weasyprint."""
    chrome = achar_chromium()
    tentativas = []
    if chrome:
        tentativas.append(("chromium", html_path, pdf_path))
        casa = os.path.join(os.path.expanduser("~"), ".cache", "agencia-de-marca")
        tentativas.append(("chromium-na-home", os.path.join(casa, "manual.html"),
                           os.path.join(casa, "manual.pdf")))
    for modo, origem, destino in tentativas:
        if origem != html_path:
            os.makedirs(os.path.dirname(origem), exist_ok=True)
            shutil.copyfile(html_path, origem)
        cmd = [chrome, "--headless", "--no-sandbox", "--disable-gpu",
               "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
               "--virtual-time-budget=20000",
               "--print-to-pdf=" + os.path.abspath(destino), os.path.abspath(origem)]
        subprocess.run(cmd, capture_output=True, timeout=900)
        if os.path.exists(destino) and os.path.getsize(destino) > 2000:
            if destino != pdf_path:
                shutil.copyfile(destino, pdf_path)
            return modo
    if shutil.which("weasyprint"):
        subprocess.run(["weasyprint", html_path, pdf_path], capture_output=True, timeout=900)
        if os.path.exists(pdf_path):
            return "weasyprint"
    return None


def conferir(pdf_path, paginas_esperadas):
    if not shutil.which("pdfinfo"):
        return ["pdfinfo não instalado: não deu para conferir páginas e tamanho "
                "(apt-get install -y poppler-utils)"]
    saida = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
    problemas = []
    m = re.search(r"Pages:\s+(\d+)", saida)
    paginas = int(m.group(1)) if m else 0
    if paginas != paginas_esperadas:
        problemas.append("o PDF saiu com {} páginas e as partes são {}: alguma página "
                         "transbordou".format(paginas, paginas_esperadas))
    if paginas < 36:
        problemas.append("só {} páginas: o mínimo do manual é 36".format(paginas))
    m = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", saida)
    if m:
        larg, alt = float(m.group(1)), float(m.group(2))
        if larg <= alt:
            problemas.append("a página saiu em retrato ({} x {}): o manual é paisagem"
                             .format(larg, alt))
        elif abs((larg / alt) - 16 / 9) > 0.02:
            problemas.append("a página não está em 16:9 ({} x {})".format(larg, alt))
    print(saida.strip())
    return problemas


def main():
    p = argparse.ArgumentParser(description="Monta e imprime o manual de marca.")
    p.add_argument("--pasta", default="marca/manual")
    p.add_argument("--fontes", default="marca/arquivos/fontes")
    p.add_argument("--html", default=None, help="padrão: <pasta>/manual.html")
    p.add_argument("--pdf", default="marca/Manual_de_Marca.pdf")
    p.add_argument("--so-html", action="store_true")
    a = p.parse_args()

    html, n, avisos = montar(a.pasta, a.fontes)
    destino_html = a.html or os.path.join(a.pasta, "manual.html")
    os.makedirs(os.path.dirname(os.path.abspath(destino_html)) or ".", exist_ok=True)
    with open(destino_html, "w", encoding="utf-8") as f:
        f.write(html)
    print("{} páginas juntadas em {} ({:.1f} MB)".format(
        n, destino_html, os.path.getsize(destino_html) / 1e6))

    for av in avisos:
        print("  aviso: " + av)

    if a.so_html:
        return 0

    os.makedirs(os.path.dirname(os.path.abspath(a.pdf)) or ".", exist_ok=True)
    modo = imprimir_pdf(destino_html, a.pdf)
    if not modo:
        print("NÃO saiu PDF. Instale o chromium (apt-get install -y chromium-browser, "
              "ou snap install chromium) ou o weasyprint (pip install weasyprint) e "
              "rode de novo.", file=sys.stderr)
        return 1
    print("PDF: {} (por {})".format(a.pdf, modo))
    problemas = conferir(a.pdf, n)
    for pr in problemas:
        print("  PROBLEMA: " + pr)
    return 1 if problemas else 0


if __name__ == "__main__":
    sys.exit(main())
