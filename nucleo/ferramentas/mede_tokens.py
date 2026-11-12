#!/usr/bin/env python3
"""Mostra onde foi o seu uso de tokens no Claude Code: por conversa e por modelo, numa janela de dias. Só lê, nunca escreve.

Uso (no Windows, `python`; no Mac e no Linux, `python3`):
  python nucleo/ferramentas/mede_tokens.py                resumo dos últimos 7 dias
  python nucleo/ferramentas/mede_tokens.py --dias 30      outra janela
  python nucleo/ferramentas/mede_tokens.py --detalhe      mostra também as conversas e as pastas mais pesadas
  python nucleo/ferramentas/mede_tokens.py --pasta CAMINHO  se a pasta dos transcritos não estiver no lugar de sempre

O que é o "peso": o Claude cobra quatro tipos de token por preços diferentes. O peso põe os quatro na mesma régua, pela
razão de preço entre eles (entrada nova 1, escrever contexto 1,25, reler contexto 0,1, resposta 5). Ele serve para
comparar conversas entre si e ver o que puxa o uso. Ele NÃO é o percentual do seu plano: para isso, use `/usage` no
Claude Code.

A conta vem dos transcritos que o próprio Claude Code grava no seu computador (`.claude/projects/*.jsonl`).
Nada é enviado para fora e nenhum arquivo é alterado.
"""
import collections
import datetime
import glob
import json
import os
import pathlib
import sys

RAZAO = {"entrada": 1.0, "escrita": 1.25, "leitura": 0.1, "resposta": 5.0}


def argumento(nome, padrao=None):
    a = sys.argv
    return a[a.index(nome) + 1] if nome in a and len(a) > a.index(nome) + 1 else padrao


def pastas_possiveis():
    casa = pathlib.Path.home()
    cands = []
    for var in ("CLAUDE_CONFIG_DIR", "USERPROFILE", "HOME"):
        valor = os.environ.get(var) or ""
        for parte in valor.split(os.pathsep):
            if not parte:
                continue
            p = pathlib.Path(parte)
            cands += [p / "projects", p / ".claude" / "projects"]
    cands += [casa / ".claude" / "projects", casa / ".config" / "claude" / "projects"]
    vistas, unicas = set(), []
    for p in cands:
        if str(p) not in vistas:
            vistas.add(str(p))
            unicas.append(p)
    return unicas


def acha_pasta(dada):
    if dada:
        p = pathlib.Path(dada).expanduser()
        if not p.is_dir():
            print(f"não achei a pasta {p}")
            sys.exit(1)
        return p
    for p in pastas_possiveis():
        if p.is_dir() and next(p.glob("**/*.jsonl"), None):
            return p
    return None


def quando(texto):
    try:
        d = datetime.datetime.fromisoformat((texto or "").replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=datetime.timezone.utc)


def le_transcrito(caminho, inicio, fim):
    """Devolve (apelido, {id da resposta: (uso, modelo)}) das respostas dentro da janela."""
    apelido, respostas = None, {}
    try:
        with open(caminho, encoding="utf-8", errors="replace") as f:
            for linha in f:
                if '"usage"' not in linha and apelido is not None:
                    continue
                try:
                    d = json.loads(linha)
                except ValueError:
                    continue
                msg = d.get("message") or {}
                if apelido is None and d.get("type") == "user":
                    apelido = "trabalho à parte" if d.get("isSidechain") else "conversa"
                uso = msg.get("usage")
                if not uso or d.get("type") != "assistant":
                    continue
                t = quando(d.get("timestamp"))
                if not t or not (inicio <= t < fim):
                    continue
                respostas[msg.get("id") or d.get("uuid")] = (uso, msg.get("model") or "?")
    except OSError:
        return apelido, {}
    return apelido, respostas


def mil(n):
    return f"{n:,.0f}".replace(",", ".")


def pct(parte, total, casas=0):
    return f"{100 * parte / total:.{casas}f}%".replace(".", ",")


def milhao(n):
    return f"{n / 1e6:,.1f} M".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    if "--ajuda" in sys.argv or "-h" in sys.argv or "--help" in sys.argv:
        print(__doc__)
        return
    dias = float(argumento("--dias", "7"))
    quantos = int(argumento("--quantos", "10"))
    pasta = acha_pasta(argumento("--pasta"))
    if pasta is None:
        print("Não achei os transcritos do Claude Code neste computador (procurei em `.claude/projects` na sua pasta de\n"
              "usuário). Se você sabe onde eles estão, rode de novo com --pasta CAMINHO.")
        return
    fim = datetime.datetime.now(datetime.timezone.utc)
    inicio = fim - datetime.timedelta(days=dias)

    por_conversa = collections.defaultdict(collections.Counter)
    por_modelo = collections.defaultdict(collections.Counter)
    por_projeto = collections.defaultdict(collections.Counter)
    ja_contadas = set()
    arquivos = sorted(glob.glob(os.path.join(str(pasta), "**", "*.jsonl"), recursive=True))
    for caminho in arquivos:
        try:
            if os.path.getmtime(caminho) < inicio.timestamp():
                continue
        except OSError:
            continue
        apelido, respostas = le_transcrito(caminho, inicio, fim)
        respostas = {k: v for k, v in respostas.items() if k not in ja_contadas}
        ja_contadas.update(respostas)
        if not respostas:
            continue
        projeto = os.path.basename(os.path.dirname(caminho))[-40:]
        chave = (projeto, apelido or "conversa", os.path.basename(caminho)[:8])
        for uso, modelo in respostas.values():
            n = {"entrada": uso.get("input_tokens") or 0,
                 "escrita": uso.get("cache_creation_input_tokens") or 0,
                 "leitura": uso.get("cache_read_input_tokens") or 0,
                 "resposta": uso.get("output_tokens") or 0}
            n["peso"] = sum(RAZAO[k] * v for k, v in n.items())
            n["respostas"] = 1
            for alvo in (por_conversa[chave], por_modelo[modelo], por_projeto[projeto]):
                alvo.update(n)

    total = sum(v["peso"] for v in por_conversa.values())
    print(f"Uso do Claude Code — últimos {dias:g} dia(s): {inicio.strftime('%d/%m')} a {fim.strftime('%d/%m/%Y')} (horário UTC)")
    print(f"Transcritos lidos de: {pasta}")
    if not total:
        print("Nenhuma resposta do Claude nessa janela. Tente --dias 30.")
        return
    conv = sum(1 for k in por_conversa if k[1] == "conversa")
    print(f"Conversas com uso na janela: {conv} (mais {len(por_conversa) - conv} trabalhos à parte, de agentes e subtarefas)")
    print()
    print(f"Peso total: {milhao(total)} — régua para comparar, não é o percentual do plano (para isso, /usage)")
    fatias = collections.Counter()
    for v in por_conversa.values():
        for k in RAZAO:
            fatias[k] += RAZAO[k] * v[k]
    rotulo = {"leitura": "reler o contexto", "escrita": "escrever o contexto", "resposta": "a resposta",
              "entrada": "o pedido novo"}
    print("Onde o peso foi: " + " · ".join(f"{rotulo[k]} {pct(fatias[k], total)}"
                                           for k, _ in fatias.most_common()))
    respostas = sum(v["respostas"] for v in por_conversa.values())
    lidos = sum(v["leitura"] for v in por_conversa.values())
    print(f"Contexto relido por resposta: {mil(lidos / max(respostas, 1))} tokens em média, em {mil(respostas)} respostas")
    print("Por modelo: " + " · ".join(f"{m[:24]} {pct(v['peso'], total)}"
                                      for m, v in sorted(por_modelo.items(), key=lambda x: -x[1]["peso"])[:4]))
    maiores = sorted(por_conversa.items(), key=lambda x: -x[1]["peso"])[:3]
    print("As mais pesadas: " + " · ".join(
        f"{pct(v['peso'], total)} {k[0]} ({k[1]} {k[2]})" for k, v in maiores))
    print()
    print("Como gastar menos: trabalho que não precisa do histórico vai para conversa nova com instrução curta; saída de\n"
          "comando cortada; arquivo lido por trecho. Conversa comprida relê todo o contexto a cada resposta: é o que mais pesa.")

    if "--detalhe" in sys.argv:
        print(f"\n== as {quantos} conversas mais pesadas")
        for k, v in sorted(por_conversa.items(), key=lambda x: -x[1]["peso"])[:quantos]:
            print(f"  {pct(v['peso'], total, 1):>6} | {k[0][:40]:<40} {k[1]:<16} {k[2]} | respostas {v['respostas']:4d} | "
                  f"relido {milhao(v['leitura']):>9} | resposta {milhao(v['resposta']):>8}")
        print(f"\n== as {quantos} pastas mais pesadas")
        for p, v in sorted(por_projeto.items(), key=lambda x: -x[1]["peso"])[:quantos]:
            print(f"  {pct(v['peso'], total, 1):>6} | {p[:50]:<50} | respostas {v['respostas']:4d} | peso {milhao(v['peso']):>9}")


if __name__ == "__main__":
    main()
