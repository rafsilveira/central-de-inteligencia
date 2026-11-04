#!/usr/bin/env python3
"""Atualizador da Central de Inteligência (núcleo da Hebel D2C).

Troca só os arquivos do núcleo, que são os que existem no repositório público da semente, pela versão estável escolhida.
Os arquivos da empresa (todo o resto da pasta) não são lidos nem escritos.

Uso (no Windows o comando é "python"; no Mac e no Linux, "python3"):
  python nucleo/atualizar.py                        ensaio: mostra o que mudaria, sem mudar nada
  python nucleo/atualizar.py --aplicar              aplica (só depois do sim do dono)
  python nucleo/atualizar.py --para 1.0.0 --aplicar vai para uma versão escolhida (serve para voltar)
  python nucleo/atualizar.py --verificar            para o Bom dia: no máximo uma vez por semana, avisa se há versão nova
  python nucleo/atualizar.py --preparar             liga o git e deixa a semente só para receber (a habilidade iniciar-central chama)
  python nucleo/atualizar.py --conferir-copia       antes do push: recusa se a cópia de segurança for um repositório público

Só usa a biblioteca padrão do Python e o git.
"""
import argparse
import datetime
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parent.parent
REMOTO = "semente"
REFS = "refs/semente/"
PUSH_DESLIGADO = "DESLIGADO--a-semente-so-recebe"
MARCA_VERIFICACAO = "central_ultima_verificacao"  # fica dentro de .git/, fora do versionamento
SEMANA = 7 * 24 * 3600

# Caminhos que são sempre da empresa. Se a semente trouxer um arquivo num deles, ele é ignorado e o dono é avisado.
PROTEGIDOS = [re.compile(p) for p in (
    r"^00_", r"^0[1-9] ", r"^[1-9][0-9] ", r"^_arquivo/", r"^marca/", r"(^|/)\.env$", r"^\.claude/skills/casa-",
    r"^\.claude/settings", r"(^|/)\.git(/|$)")]


class Erro(Exception):
    pass


def git(*args, entrada=None, binario=False, checar=True, tempo=None):
    try:
        r = subprocess.run(["git", "-C", str(RAIZ), "-c", "core.quotepath=off", *args],
                           input=entrada, capture_output=True, timeout=tempo)
    except subprocess.TimeoutExpired:
        raise Erro("o git demorou demais para responder (internet lenta ou fora do ar?)")
    if checar and r.returncode != 0:
        raise Erro(f"git {' '.join(args[:2])}: {r.stderr.decode('utf-8', 'replace').strip()}")
    return r.stdout if binario else r.stdout.decode("utf-8", "replace")


def origem_padrao():
    f = RAIZ / "nucleo" / "ORIGEM"
    if not f.exists():
        return ""
    for linha in f.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if linha and not linha.startswith("#"):
            return linha
    return ""


def normaliza_url(url):
    u = url.strip().lower()
    u = re.sub(r"^git@([^:]+):", r"https://\1/", u)
    u = re.sub(r"^ssh://git@", "https://", u)
    u = re.sub(r"^https?://[^@/]+@", "https://", u)  # tira usuário/token de URL
    return u.rstrip("/").removesuffix(".git")


def versao_de_texto(t):
    m = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", t.strip())
    return tuple(map(int, m.groups())) if m else None


def txt(v):
    return ".".join(map(str, v)) if v else "nenhuma"


def versao_instalada():
    f = RAIZ / "VERSAO"
    return versao_de_texto(f.read_text(encoding="utf-8")) if f.exists() else None


def tem_repo():
    return (RAIZ / ".git").exists()


def garantir_repo():
    if not shutil.which("git"):
        raise Erro("o git não está instalado neste computador. Instale em https://git-scm.com e rode de novo.")
    if not tem_repo():
        git("init", "-q")
        git("symbolic-ref", "HEAD", "refs/heads/main")
        print("Liguei o git nesta pasta (ela ainda não tinha).")
    if not git("config", "user.email", checar=False).strip():
        git("config", "user.name", "Central de Inteligência")
        git("config", "user.email", "central@computador.local")


def garantir_remoto(url):
    if not url:
        raise Erro("não sei de onde vem a semente: o arquivo nucleo/ORIGEM está vazio.")
    remotos = git("remote").split()
    if REMOTO not in remotos:
        if "origin" in remotos and normaliza_url(git("remote", "get-url", "origin").strip()) == normaliza_url(url):
            git("remote", "rename", "origin", REMOTO)
        else:
            git("remote", "add", REMOTO, url)
    elif normaliza_url(git("remote", "get-url", REMOTO).strip()) != normaliza_url(url):
        git("remote", "set-url", REMOTO, url)
    git("remote", "set-url", "--push", REMOTO, PUSH_DESLIGADO)


def buscar(url):
    garantir_remoto(url)
    git("fetch", "--quiet", "--no-tags", REMOTO, "+refs/tags/v*:refs/semente/v*", tempo=120)


def versoes_disponiveis():
    vs = {}
    for linha in git("for-each-ref", "--format=%(refname)", REFS).splitlines():
        v = versao_de_texto(linha[len(REFS):])
        if v:
            vs[v] = linha
    return vs


def lista(ref):
    return [p for p in git("ls-tree", "-r", "-z", "--name-only", ref).split("\0") if p]


def conteudo(ref, caminho):
    return git("cat-file", "blob", f"{ref}:{caminho}", binario=True)


def igual(a, b):
    return a.replace(b"\r\n", b"\n") == b.replace(b"\r\n", b"\n")


def protegido(caminho):
    partes = caminho.split("/")
    return caminho.startswith("/") or ".." in partes or any(r.search(caminho) for r in PROTEGIDOS)


def novidades(ref, de, ate):
    """Trechos do NOVIDADES.md da versão de destino entre a versão instalada (exclusive) e a de destino (inclusive)."""
    try:
        texto = conteudo(ref, "NOVIDADES.md").decode("utf-8", "replace")
    except Erro:
        return ""
    blocos, atual, guardar = [], [], False
    for linha in texto.splitlines():
        m = re.match(r"^##\s+v?(\d+\.\d+\.\d+)", linha)
        if m:
            if guardar and atual:
                blocos.append("\n".join(atual).rstrip())
            v = versao_de_texto(m.group(1))
            guardar = v is not None and (de is None or v > de) and v <= ate
            atual = [linha]
        elif guardar:
            atual.append(linha)
    if guardar and atual:
        blocos.append("\n".join(atual).rstrip())
    return "\n\n".join(blocos)


def planejar(alvo_ref, atual_ref):
    novos = lista(alvo_ref)
    velhos = set(lista(atual_ref)) if atual_ref else set()
    p = {"trocar": [], "novo": [], "apagar": [], "guardar": [], "ignorado": [], "iguais": 0}
    for c in novos:
        if protegido(c):
            p["ignorado"].append(c)
            continue
        f = RAIZ / c
        dado = conteudo(alvo_ref, c)
        if not f.exists():
            p["novo"].append(c)
            continue
        local = f.read_bytes()
        if igual(local, dado):
            p["iguais"] += 1
            continue
        p["trocar"].append(c)
        if not (atual_ref and c in velhos and igual(local, conteudo(atual_ref, c))):
            p["guardar"].append(c)  # mudança do dono no núcleo, ou arquivo dele no mesmo caminho
    for c in sorted(velhos - set(novos)):
        f = RAIZ / c
        if protegido(c) or not f.exists():
            continue
        if not igual(f.read_bytes(), conteudo(atual_ref, c)):
            p["guardar"].append(c)
        p["apagar"].append(c)
    return p


def escolher(args):
    url = args.origem or origem_padrao()
    garantir_repo()
    buscar(url)
    vs = versoes_disponiveis()
    if not vs:
        raise Erro("a semente ainda não tem nenhuma versão publicada.")
    if args.para:
        alvo = versao_de_texto(args.para)
        if alvo not in vs:
            raise Erro(f"a versão {args.para} não existe. Existem: {', '.join(txt(v) for v in sorted(vs))}.")
    else:
        alvo = max(vs)
    instalada = versao_instalada()
    atual_ref = vs.get(instalada)
    return instalada, alvo, vs[alvo], atual_ref


def mostrar(instalada, alvo, alvo_ref, plano):
    print("Central de Inteligência: atualização do núcleo")
    if instalada is None:
        print(f"Esta pasta não diz qual versão tem. A versão de destino é a {txt(alvo)}.")
    elif alvo == instalada:
        print(f"Você está na versão {txt(alvo)}, que é a de destino.")
    elif alvo > instalada:
        print(f"Você está na versão {txt(instalada)}. A de destino é a {txt(alvo)}.")
    else:
        print(f"Você está na versão {txt(instalada)} e vai VOLTAR para a {txt(alvo)}.")
    if instalada is None or alvo > instalada:
        trecho = novidades(alvo_ref, instalada, alvo)
        if trecho:
            print("\nO que muda (do NOVIDADES.md):\n")
            print("\n".join("  " + l for l in trecho.splitlines()))
    n = len(plano["trocar"]) + len(plano["novo"]) + len(plano["apagar"])
    print(f"\nArquivos do núcleo: {len(plano['trocar'])} trocados, {len(plano['novo'])} novos, "
          f"{len(plano['apagar'])} removidos, {plano['iguais']} iguais. Os seus arquivos não são tocados.")
    if plano["guardar"]:
        print(f"\nVocê tinha mudado {len(plano['guardar'])} arquivo(s) do núcleo. A sua versão vai para "
              f"_arquivo/AAAA-MM/minhas_mudancas_no_nucleo/ antes da troca:")
        for c in plano["guardar"]:
            print("  " + c)
        print("Para manter um comportamento seu, escreva a regra no 00_MASTER_GUIDELINE.md ou crie uma habilidade em "
              ".claude/skills/casa-<nome>/.")
    if plano["ignorado"]:
        print("\nA semente trouxe arquivo(s) num caminho que é seu. Não troquei (avise a Hebel):")
        for c in plano["ignorado"]:
            print("  " + c)
    return n


def aplicar(instalada, alvo, alvo_ref, atual_ref, plano):
    if git("diff", "--cached", "--name-only", checar=False).strip():
        raise Erro("há arquivos preparados para commit (git add) que não são da atualização. "
                   "Faça o Boa noite antes e rode de novo.")
    agora = datetime.datetime.now()
    guarda = RAIZ / "_arquivo" / agora.strftime("%Y-%m") / "minhas_mudancas_no_nucleo" / agora.strftime("%Y-%m-%d_%H%M%S")
    mexidos = []
    for c in plano["guardar"]:
        destino = guarda / c
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(RAIZ / c, destino)
        mexidos.append(destino.relative_to(RAIZ).as_posix())
    for c in plano["trocar"] + plano["novo"]:
        f = RAIZ / c
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(conteudo(alvo_ref, c))
        mexidos.append(c)
    rastreados = set(p for p in git("ls-files", "-z").split("\0") if p)
    for c in plano["apagar"]:
        f = RAIZ / c
        f.unlink()
        pasta = f.parent
        while pasta != RAIZ and pasta.is_dir() and not any(pasta.iterdir()):
            pasta.rmdir()
            pasta = pasta.parent
        if c in rastreados:
            mexidos.append(c)
    # conferência: cada arquivo do núcleo agora é igual ao da versão de destino
    for c in plano["trocar"] + plano["novo"]:
        if not igual((RAIZ / c).read_bytes(), conteudo(alvo_ref, c)):
            raise Erro(f"a conferência falhou em {c}. Nada foi commitado; rode de novo ou peça ajuda.")
    if mexidos:
        git("add", "-A", "--pathspec-from-file=-", "--pathspec-file-nul",
            entrada="\0".join(":(literal)" + c for c in mexidos).encode("utf-8"))
        msg = f"Central: núcleo {txt(instalada)} -> {txt(alvo)}"
        r = subprocess.run(["git", "-C", str(RAIZ), "commit", "-q", "-m", msg], capture_output=True)
        if r.returncode != 0 and b"nothing to commit" not in r.stdout + r.stderr:
            raise Erro("os arquivos foram trocados, mas o commit falhou: " + r.stderr.decode("utf-8", "replace").strip())
    print(f"\nPronto: a Central está na versão {txt(alvo)}.")
    if plano["guardar"]:
        print(f"Sua versão dos arquivos que você tinha mudado ficou em {guarda.relative_to(RAIZ).as_posix()}/.")
    if instalada and instalada != alvo:
        print(f"Para voltar: python nucleo/atualizar.py --para {txt(instalada)} --aplicar")
    if not git("log", "-1", "--format=%h", checar=False).strip():
        print("Atenção: esta pasta ainda não tem commit. O próximo Boa noite salva os seus arquivos no git.")


def verificar(args):
    if not tem_repo() or not shutil.which("git"):
        return 0
    marca = RAIZ / ".git" / MARCA_VERIFICACAO
    if not args.forcar and marca.exists() and time.time() - marca.stat().st_mtime < SEMANA:
        return 0
    try:
        buscar(args.origem or origem_padrao())
    except Erro:
        return 0  # sem internet não atrapalha o Bom dia
    marca.write_text(datetime.datetime.now().isoformat(timespec="minutes"), encoding="utf-8")
    vs = versoes_disponiveis()
    instalada = versao_instalada()
    if vs and (instalada is None or max(vs) > instalada):
        print(f"Há versão nova da Central: {txt(max(vs))} (você está na {txt(instalada)}). "
              f"Diga \"atualizar a Central\" para ver o que muda antes de decidir.")
    return 0


def repositorio_publico(url):
    """True se o GitHub responde o repositório sem login (é público); False se não (privado ou inexistente);
    None se não deu para saber (outro servidor, sem internet)."""
    m = re.match(r"^https://github\.com/([^/]+)/([^/]+)$", normaliza_url(url))
    if not m:
        return None
    req = urllib.request.Request(f"https://api.github.com/repos/{m.group(1)}/{m.group(2)}",
                                 headers={"User-Agent": "central-de-inteligencia-atualizador",
                                          "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return not json.load(r).get("private", False)
    except urllib.error.HTTPError as e:
        return False if e.code == 404 else None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None


def conferir_copia(args):
    """0 = pode enviar; 2 = não envie (público ou é a semente); 3 = não há cópia configurada; 4 = não deu para conferir."""
    if not tem_repo() or "origin" not in git("remote").split():
        print("Não há cópia de segurança configurada (remote \"origin\"). Ficou salvo só neste computador.")
        return 3
    url = git("remote", "get-url", "--push", "origin").strip()
    if normaliza_url(url) == normaliza_url(args.origem or origem_padrao()):
        print("PARE: o \"origin\" aponta para a semente pública da Hebel. Não envie os seus arquivos para lá.")
        return 2
    publico = repositorio_publico(url)
    if publico:
        print(f"PARE: a sua cópia de segurança ({normaliza_url(url)}) é um repositório PÚBLICO no GitHub. "
              "Os dados da sua empresa ficariam abertos para qualquer pessoa. Torne o repositório privado antes de enviar.")
        return 2
    if publico is None and "github.com" in normaliza_url(url):
        print("Não consegui conferir no GitHub se a sua cópia é privada (sem internet?). Envie só se tiver certeza.")
        return 4
    return 0


def preparar(args):
    garantir_repo()
    url = args.origem or origem_padrao()
    buscar(url)
    vs = versoes_disponiveis()
    print(f"Git ligado. A semente ({normaliza_url(url)}) fica só para receber atualizações: o envio para ela está desligado.")
    print(f"Versão desta pasta: {txt(versao_instalada())}. Mais nova publicada: {txt(max(vs)) if vs else 'nenhuma'}.")
    if "origin" in git("remote").split():
        conferir_copia(args)
    return 0


def main():
    for s in (sys.stdout, sys.stderr):
        if hasattr(s, "reconfigure"):
            s.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="Atualizador do núcleo da Central de Inteligência")
    ap.add_argument("--aplicar", action="store_true", help="aplica a atualização (sem isto é só ensaio)")
    ap.add_argument("--para", metavar="VERSAO", help="versão de destino (padrão: a mais nova)")
    ap.add_argument("--verificar", action="store_true", help="para o Bom dia: avisa se há versão nova, no máximo 1x por semana")
    ap.add_argument("--forcar", action="store_true", help="com --verificar: confere mesmo que já tenha conferido esta semana")
    ap.add_argument("--preparar", action="store_true", help="liga o git e deixa a semente só para receber")
    ap.add_argument("--conferir-copia", action="store_true", help="antes do push: recusa cópia de segurança pública")
    ap.add_argument("--origem", help=argparse.SUPPRESS)  # para testes: outro endereço da semente
    args = ap.parse_args()
    try:
        if args.verificar:
            return verificar(args)
        if args.conferir_copia:
            return conferir_copia(args)
        if args.preparar:
            return preparar(args)
        instalada, alvo, alvo_ref, atual_ref = escolher(args)
        plano = planejar(alvo_ref, atual_ref)
        n = mostrar(instalada, alvo, alvo_ref, plano)
        if n == 0:
            print("\nNada a trocar.")
            return 0
        if not args.aplicar:
            print("\nIsto foi um ensaio: nada mudou. Para aplicar: python nucleo/atualizar.py --aplicar"
                  + (f" --para {txt(alvo)}" if args.para else ""))
            return 0
        aplicar(instalada, alvo, alvo_ref, atual_ref, plano)
        return 0
    except Erro as e:
        print(f"Não atualizei: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
