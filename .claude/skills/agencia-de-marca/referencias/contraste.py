#!/usr/bin/env python3
"""Calcula o contraste entre duas cores pela regra de acessibilidade (WCAG 2.1) e,
quando a cor não passa, devolve a versão corrigida mais próxima da original.

Nunca escreva uma razão de contraste "de cabeça" no manual. Rode isto.

Uso:
  python3 contraste.py "#006a65" "#ffffff"
  python3 contraste.py --paleta "#006a65,#e2453f,#161a19" --fundos "#ffffff,#121715"
  python3 contraste.py --corrigir "#fb5454" --sobre "#ffffff" --alvo 4.5

Pisos da WCAG 2.1 AA:
  4,5:1  texto normal
  3,0:1  texto grande (24 px, ou 19 px em negrito), ícone, borda, elemento de interface
  7,0:1  AAA para texto normal
"""
import argparse
import sys


def ler_hex(c):
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6:
        raise SystemExit("Cor inválida: {!r} (use #rrggbb).".format(c))
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def para_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*(max(0, min(255, int(round(v)))) for v in rgb))


def luminancia(rgb):
    def canal(v):
        v = v / 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (canal(v) for v in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def razao(c1, c2):
    l1, l2 = luminancia(ler_hex(c1)), luminancia(ler_hex(c2))
    claro, escuro = max(l1, l2), min(l1, l2)
    return (claro + 0.05) / (escuro + 0.05)


def veredito(r):
    return ("AAA" if r >= 7 else
            "AA texto" if r >= 4.5 else
            "só texto grande e detalhe" if r >= 3 else
            "não passa")


def corrigir(cor, fundo, alvo=4.5, passos=400):
    """Escurece (fundo claro) ou clareia (fundo escuro) a cor até bater o alvo,
    mantendo o matiz. Devolve (hex_corrigido, razao) ou (None, melhor_razao)."""
    import colorsys
    r, g, b = (v / 255.0 for v in ler_hex(cor))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    escurecer = luminancia(ler_hex(fundo)) > 0.18
    melhor = (None, razao(cor, fundo))
    for i in range(1, passos + 1):
        passo = i / float(passos)
        nova_l = l * (1 - passo) if escurecer else l + (1 - l) * passo
        nr, ng, nb = colorsys.hls_to_rgb(h, nova_l, s)
        cand = para_hex((nr * 255, ng * 255, nb * 255))
        rz = razao(cand, fundo)
        if rz >= alvo:
            return cand, rz
        if rz > melhor[1]:
            melhor = (cand, rz)
    return melhor


def linha(c1, c2):
    r = razao(c1, c2)
    return "{} sobre {}: {:.2f}:1  ({})".format(c1, c2, r, veredito(r))


def main():
    p = argparse.ArgumentParser(description="Contraste WCAG entre cores.")
    p.add_argument("cores", nargs="*", help="duas cores: frente e fundo")
    p.add_argument("--paleta", help="lista de cores separadas por vírgula")
    p.add_argument("--fundos", default="#ffffff,#000000",
                   help="lista de fundos separados por vírgula")
    p.add_argument("--corrigir", help="cor a corrigir")
    p.add_argument("--sobre", default="#ffffff", help="fundo da correção")
    p.add_argument("--alvo", type=float, default=4.5)
    a = p.parse_args()

    if a.corrigir:
        atual = razao(a.corrigir, a.sobre)
        print(linha(a.corrigir, a.sobre))
        if atual >= a.alvo:
            print("já passa no alvo de {:.1f}:1. Não precisa corrigir.".format(a.alvo))
            return
        nova, rz = corrigir(a.corrigir, a.sobre, a.alvo)
        if nova is None:
            print("não dá para chegar a {:.1f}:1 mantendo o matiz. "
                  "Use essa cor só em detalhe grande, ou troque o fundo.".format(a.alvo))
        else:
            print("corrigida: {} -> {:.2f}:1 sobre {}".format(nova, rz, a.sobre))
        return

    if a.paleta:
        fundos = [f.strip() for f in a.fundos.split(",") if f.strip()]
        for c in [c.strip() for c in a.paleta.split(",") if c.strip()]:
            for f in fundos:
                print(linha(c, f))
        return

    if len(a.cores) != 2:
        p.print_help()
        sys.exit(2)
    print(linha(a.cores[0], a.cores[1]))


if __name__ == "__main__":
    main()
