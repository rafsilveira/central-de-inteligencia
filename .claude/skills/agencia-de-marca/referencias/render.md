# Comandos que a agência usa para ver o que desenhou

Nenhum agente desta agência entrega arquivo que não abriu. Estes são os comandos,
todos conferidos numa máquina Linux comum. Em Mac e Windows muda só o nome do
programa (`chrome` em vez de `chromium`).

## 1. O que precisa estar instalado

| Para quê | Programa | Como instalar se faltar |
|---|---|---|
| SVG → PNG, HTML → PDF | chromium (ou Chrome) | `apt-get install -y chromium-browser` · `snap install chromium` · Mac: já tem o Chrome |
| conferir o PDF | poppler (`pdfinfo`, `pdftoppm`, `pdftotext`) | `apt-get install -y poppler-utils` |
| texto virar vetor, juntar imagens | python3 com `fonttools`, `brotli`, `pillow` | `pip install fonttools brotli pillow` |
| alternativa ao chromium para o PDF | weasyprint | `pip install weasyprint` |

**Sempre avise o dono antes de instalar**, numa linha: "preciso instalar o chromium
para gerar o PDF — tudo bem?" Se ele não puder instalar nada, o manual sai em HTML e
o PDF fica como pendência; diga isso, não entregue em silêncio.

## 2. SVG → PNG (variantes do logo, prévias)

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --default-background-color=00000000 \
  --window-size=LARGURA,ALTURA --force-device-scale-factor=4 \
  --screenshot=saida.png  /caminho/absoluto/do/arquivo.svg
```

- `LARGURA,ALTURA` = o tamanho do `viewBox` do SVG. O PNG sai nesse tamanho
  multiplicado pelo `--force-device-scale-factor` (4 = PNG grande, bom para impressão).
- `--default-background-color=00000000` deixa o fundo transparente. Para ver a versão
  sobre fundo claro, troque por `ffffffff`.
- **O caminho precisa ser absoluto.** O chromium instalado por snap não enxerga `/tmp`
  nem pasta fora da pasta pessoal: se der `ERR_FILE_NOT_FOUND`, copie o arquivo para
  dentro da pasta do projeto (ou da pasta pessoal) e rode de novo.

Para o favicon de 32 px, gere sem escala e olhe o resultado de verdade:

```bash
chromium --headless --no-sandbox --disable-gpu --hide-scrollbars \
  --default-background-color=00000000 --window-size=32,32 \
  --screenshot=favicon_32.png /caminho/simbolo.svg
```

## 3. Juntar as três direções num quadro só (`direcoes.png`)

```python
python3 - <<'PY'
from PIL import Image, ImageDraw
nomes = ["Direção 1 — <nome>", "Direção 2 — <nome>", "Direção 3 — <nome>"]
imgs = [Image.open(f"marca/ciclo/direcao_{i}.png").convert("RGBA") for i in (1, 2, 3)]
alvo_h = 420
redim = []
for im in imgs:
    larg = int(im.width * alvo_h / im.height)
    redim.append(im.resize((larg, alvo_h), Image.LANCZOS))
pad, topo, base = 80, 60, 110
larg_total = sum(i.width for i in redim) + pad * 4
tela = Image.new("RGB", (larg_total, alvo_h + topo + base), "white")
x = pad
d = ImageDraw.Draw(tela)
for im, nome in zip(redim, nomes):
    tela.paste(im, (x, topo), im)
    d.text((x, topo + alvo_h + 40), nome, fill="#333333")
    x += im.width + pad
tela.save("marca/ciclo/direcoes.png")
print("ok", tela.size)
PY
```

## 4. HTML → PDF (o manual)

Use o script pronto, que junta as páginas, embute imagens e fontes, imprime e confere:

```bash
python3 .claude/skills/agencia-de-marca/referencias/juntar_manual.py \
  --pasta marca/manual --fontes marca/arquivos/fontes --pdf marca/Manual_de_Marca.pdf
```

Ele imprime o número de páginas, o tamanho da página e os problemas encontrados.
Página certa: **1920 x 1080 pts** (paisagem 16:9), o mesmo tamanho de um manual de
designer. Se o número de páginas do PDF for maior que o número de arquivos em
`partes/`, alguma página transbordou: ache qual e corte texto (nunca diminua a fonte
abaixo de 24 px).

Por baixo, o comando é este — serve se precisar rodar na mão:

```bash
chromium --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=20000 \
  --print-to-pdf=/caminho/Manual_de_Marca.pdf  /caminho/manual.html
```

## 5. Olhar as páginas (obrigatório antes de entregar)

```bash
pdfinfo marca/Manual_de_Marca.pdf                       # páginas e tamanho
pdftotext -layout marca/Manual_de_Marca.pdf - | head -80  # o texto saiu?
pdftoppm -r 40 -png -f 1 -l 8 marca/Manual_de_Marca.pdf marca/ciclo/pagina
```

Depois **abra os PNGs gerados** (a ferramenta de leitura de arquivo mostra imagem) e
confira: nada cortado na borda, logo no lugar, cor certa, texto legível.

## 6. Fonte dentro do arquivo

As fontes ficam em `marca/arquivos/fontes/` com o nome `Familia_Peso.ttf`
(ex.: `Manrope_800.ttf`). O `texto_para_vetor.py` baixa do Google Fonts e guarda lá;
o `juntar_manual.py` embute no HTML. Assim o manual abre igual em qualquer máquina,
inclusive sem internet.

## 7. Quando o chromium não existe mesmo

1. `pip install weasyprint` e rode `juntar_manual.py` de novo: ele usa o weasyprint
   sozinho (o resultado é um pouco mais simples, mas sai).
2. Sem nenhum dos dois: entregue `marca/manual/manual.html` e diga ao dono que basta
   abrir no navegador e mandar imprimir em PDF, paisagem, sem margem.
