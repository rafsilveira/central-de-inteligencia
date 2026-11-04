#!/usr/bin/env python3
"""Transforma um texto em contorno vetorial de verdade (path SVG), a partir de uma
fonte do Google Fonts ou de um arquivo de fonte local.

Por que isso existe: um `<text>` dentro de um SVG só aparece certo em quem tem a
fonte instalada. Logo não pode depender disso. Aqui as letras viram desenho.

Uso:
  python3 texto_para_vetor.py --familia Manrope --peso 800 --texto "Minha Marca" \\
      --tamanho 100 --cor "#006a65" --saida wordmark.svg
  python3 texto_para_vetor.py --arquivo fontes/Manrope_800.ttf --texto "ABC" --so-path

Saídas:
  - sem --so-path: um SVG completo, com viewBox colado no desenho;
  - com --so-path: só o `d="..."` do path, para colar dentro de um SVG maior.
  Em qualquer caso, imprime no stderr a largura, a altura e o viewBox calculados.

Dependências: fontTools (e brotli, se a fonte baixada vier em .woff2).
Se faltar: pip install fonttools brotli
"""
import argparse
import os
import re
import sys
import urllib.request

# UA antigo: faz o Google Fonts devolver .ttf, um arquivo só, com o alfabeto inteiro.
# UA moderno devolve .woff2 fatiado por idioma — aí é preciso escolher o pedaço latino.
UA_ANTIGO = "Mozilla/5.0 (X11; Linux x86_64)"
UA_NOVO = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/120.0 Safari/537.36")


def _escolher_arquivo(css):
    """Dentro do CSS do Google Fonts, acha a melhor url: .ttf primeiro; entre .woff2,
    o bloco do alfabeto latino."""
    blocos = re.findall(r"@font-face\s*\{(.*?)\}", css, re.S) or [css]
    melhor = None
    for b in blocos:
        url = re.search(r"url\((https://[^)]+\.(?:ttf|otf|woff2))\)", b)
        if not url:
            continue
        u = url.group(1)
        faixa = re.search(r"unicode-range:([^;]+);", b)
        faixa = faixa.group(1) if faixa else ""
        latino = ("U+0000-00FF" in faixa) or (faixa.strip() == "")
        nota = (2 if u.endswith((".ttf", ".otf")) else 0) + (1 if latino else 0)
        if melhor is None or nota > melhor[0]:
            melhor = (nota, u)
    return melhor[1] if melhor else None


def baixar_fonte(familia, peso, destino):
    """Baixa o arquivo de fonte do Google Fonts (grátis) e grava em `destino`."""
    url = "https://fonts.googleapis.com/css2?family={}:wght@{}".format(
        familia.replace(" ", "+"), peso
    )
    escolhida = None
    for ua in (UA_ANTIGO, UA_NOVO):
        req = urllib.request.Request(url, headers={"User-Agent": ua})
        css = urllib.request.urlopen(req, timeout=40).read().decode("utf-8")
        escolhida = _escolher_arquivo(css)
        if escolhida and escolhida.endswith((".ttf", ".otf")):
            break
    if not escolhida:
        raise SystemExit("O Google Fonts não devolveu arquivo de fonte para "
                         "{} peso {}. Confira o nome da família.".format(familia, peso))
    dados = urllib.request.urlopen(
        urllib.request.Request(escolhida, headers={"User-Agent": UA_NOVO}), timeout=40
    ).read()
    if escolhida.endswith(".woff2"):
        destino = os.path.splitext(destino)[0] + ".woff2"
    os.makedirs(os.path.dirname(os.path.abspath(destino)) or ".", exist_ok=True)
    with open(destino, "wb") as f:
        f.write(dados)
    print("fonte baixada: {}".format(escolhida), file=sys.stderr)
    return destino


def texto_para_path(caminho_fonte, texto, tamanho, tracking=0.0):
    """Devolve (d_do_path, largura_total, (xmin, ymin, xmax, ymax))."""
    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.misc.transform import Transform

    fonte = TTFont(caminho_fonte, fontNumber=0)
    glifos = fonte.getGlyphSet()
    cmap = fonte.getBestCmap()
    upem = fonte["head"].unitsPerEm
    escala = tamanho / float(upem)

    caneta = SVGPathPen(glifos, ntos=lambda v: "{:.2f}".format(v))
    limites = BoundsPen(glifos)
    x = 0.0
    for ch in texto:
        nome = cmap.get(ord(ch))
        if nome is None:
            raise SystemExit("A fonte não tem o caractere {!r}. "
                             "Troque de peso/família ou tire o caractere.".format(ch))
        glifo = glifos[nome]
        # y invertido: no SVG o eixo cresce para baixo.
        t = Transform(escala, 0, 0, -escala, x, 0)
        glifo.draw(TransformPen(caneta, t))
        glifo.draw(TransformPen(limites, t))
        x += glifo.width * escala + tracking
    if limites.bounds is None:
        raise SystemExit("Texto sem desenho nenhum (só espaços?).")
    return caneta.getCommands(), x, limites.bounds


def main():
    p = argparse.ArgumentParser(description="Texto em contorno vetorial (path SVG).")
    p.add_argument("--familia", help="família do Google Fonts, ex.: Manrope")
    p.add_argument("--peso", default="700", help="peso, ex.: 400, 700, 800")
    p.add_argument("--arquivo", help="arquivo de fonte local (.ttf/.otf/.woff2)")
    p.add_argument("--cache", default="marca/arquivos/fontes",
                   help="pasta onde guardar a fonte baixada")
    p.add_argument("--texto", required=True)
    p.add_argument("--tamanho", type=float, default=100.0)
    p.add_argument("--tracking", type=float, default=0.0,
                   help="espaço extra entre letras, nas mesmas unidades de --tamanho")
    p.add_argument("--cor", default="#000000")
    p.add_argument("--margem", type=float, default=0.0)
    p.add_argument("--so-path", action="store_true", help="imprime só o d= do path")
    p.add_argument("--saida", default="-")
    a = p.parse_args()

    caminho = a.arquivo
    if not caminho:
        if not a.familia:
            raise SystemExit("Passe --familia (Google Fonts) ou --arquivo (fonte local).")
        base = os.path.join(a.cache, "{}_{}".format(a.familia.replace(" ", "_"), a.peso))
        caminho = next((base + e for e in (".ttf", ".otf", ".woff2")
                        if os.path.exists(base + e)), None)
        if caminho is None:
            caminho = baixar_fonte(a.familia, a.peso, base + ".ttf")

    d, largura, (xmin, ymin, xmax, ymax) = texto_para_path(
        caminho, a.texto, a.tamanho, a.tracking
    )
    m = a.margem
    vb = "{:.2f} {:.2f} {:.2f} {:.2f}".format(
        xmin - m, ymin - m, (xmax - xmin) + 2 * m, (ymax - ymin) + 2 * m
    )
    print("largura_avanco={:.2f} largura_desenho={:.2f} altura_desenho={:.2f} viewBox=\"{}\"".format(
        largura, xmax - xmin, ymax - ymin, vb), file=sys.stderr)

    if a.so_path:
        saida = 'd="{}"'.format(d)
    else:
        saida = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="{}">\n'
                 '  <path d="{}" fill="{}"/>\n</svg>\n').format(vb, d, a.cor)

    if a.saida == "-":
        sys.stdout.write(saida)
    else:
        os.makedirs(os.path.dirname(os.path.abspath(a.saida)) or ".", exist_ok=True)
        with open(a.saida, "w", encoding="utf-8") as f:
            f.write(saida)
        print("gravado: {}".format(a.saida), file=sys.stderr)


if __name__ == "__main__":
    main()
