#!/usr/bin/env python3
"""
Guardrail Base (CI Semente) - Central de Inteligência (Hebel D2C)
Versão leve, unificada e sem dependências externas para CI rápida:
  1. Varredura básica de segredos e chaves de API em arquivos do repositório.
  2. Validação determinística de URLs/links em Landing Pages e arquivos Markdown.
  3. Verificação do teto estrito de 200 linhas para o arquivo de memória '00_CURRENT_STATE.md'.
  4. Conferência do enxugamento (--conferir-enxugamento REV): nada que estava no estado some de todos os documentos.

Exit Codes:
  0: Aprovado em todos os testes
  1: Falha em um ou mais critérios
"""

import os
import re
import sys
import socket
import subprocess
import argparse
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Teto máximo de linhas para arquivos de memória de estado
MAX_CURRENT_STATE_LINES = 200

# Extensões analisadas para segredos e links
TEXT_EXTENSIONS = {".md", ".json", ".txt", ".html", ".py", ".js", ".ts", ".yaml", ".yml", ".env", ".toml", ".sh"}
IGNORE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".idea", ".vscode", "brain"}

# Regex enxuto de segredos essenciais
ESSENTIAL_SECRET_RULES = [
    ("Google API Key", re.compile(r"\bAIza[0-9A-Za-z\-_]{35}\b")),
    ("OpenAI API Key", re.compile(r"\bsk-(?:proj-|admin-)?[a-zA-Z0-9_\-]{32,}\b")),
    ("Anthropic API Key", re.compile(r"\bsk-ant-[a-zA-Z0-9_\-]{32,}\b")),
    # 27/10/2026: os padrões abaixo vieram da suíte guardrail_seguranca.py (GitHub, AWS, Slack)
    ("GitHub Token", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,}\b")),
    ("GitHub Fine-Grained Token", re.compile(r"\bgithub_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}\b")),
    ("AWS Access Key ID", re.compile(r"(?<![A-Z0-9])(?:AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}(?![A-Z0-9])")),
    ("AWS Secret Access Key", re.compile(r"(?i)\b(?:aws_secret_access_key|aws_secret_key)\s*[:=]\s*[\"']?([A-Za-z0-9/+=]{40})[\"']?")),
    ("Slack Token", re.compile(r"\bxox[baprs]-[0-9a-zA-Z\-]{10,}\b")),
    ("Chave Privada", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |PGP )?PRIVATE KEY-----")),
    ("Bearer Token", re.compile(r"(?i)\bbearer\s+([a-zA-Z0-9_\-\.]{24,})\b")),
    ("Senha / Secret", re.compile(r"(?i)\b(?:api_key|secret_key|password|client_secret)\s*[:=]\s*[\"']([^\"'\r\n]{8,})[\"']"))
]

PLACEHOLDER_WORDS = ["your_key", "example", "dummy", "placeholder", "changeme", "process.env", "os.environ", "${", "<key>"]
URL_REGEX = re.compile(r"https?://[^\s<>\"')]+", re.IGNORECASE)


def is_placeholder(val: str) -> bool:
    low = val.lower()
    return any(p in low for p in PLACEHOLDER_WORDS)


def mask_secret(s: str) -> str:
    s = s.strip()
    if len(s) <= 8:
        return "*" * len(s)
    return f"{s[:4]}...{s[-4:]}"


def check_secrets_in_file(path: Path) -> List[str]:
    violations = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for idx, line in enumerate(f, 1):
                if "guardrail:ignore" in line:
                    continue
                for name, pat in ESSENTIAL_SECRET_RULES:
                    m = pat.search(line)
                    if m:
                        val = m.group(1) if m.groups() else m.group(0)
                        if not is_placeholder(val):
                            violations.append(f"{path.name}:{idx} [{name}] {mask_secret(val)}")
    except Exception as exc:
        violations.append(f"{path.name}: Erro de leitura ({exc})")
    return violations


def check_url_health(url: str, timeout: float = 5.0) -> Tuple[bool, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) HebelCISemente/1.0"
    }
    clean_url = url.rstrip(".,;:!?)")
    for method in ("HEAD", "GET"):
        req = urllib.request.Request(clean_url, headers=headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                code = resp.getcode()
                if 200 <= code < 400:
                    return True, f"HTTP {code}"
                return False, f"HTTP {code}"
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (405, 403):
                continue
            return False, f"HTTP {e.code}"
        except urllib.error.URLError as e:
            if isinstance(e.reason, socket.timeout):
                return False, "Timeout"
            return False, f"DNS/Conexão falhou ({e.reason})"
        except Exception as exc:
            return False, str(exc)
    return False, "Falha de rede"


def check_state_file_ceiling(filepath: Path, max_lines: int = MAX_CURRENT_STATE_LINES) -> Tuple[bool, int, str]:
    """
    Verifica se o arquivo de estado existe e se respeita o teto de linhas.
    Retorna (valido, total_linhas, mensagem).
    """
    if not filepath.exists():
        return True, 0, f"Arquivo {filepath.name} não encontrado (ignorado ou opcional)."

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            lines = sum(1 for _ in f)

        if lines > max_lines:
            return False, lines, (
                f"Arquivo '{filepath.name}' excede o teto de {max_lines} linhas "
                f"(atual: {lines} linhas). Condense a memória imediatamente!"
            )
        return True, lines, f"Arquivo '{filepath.name}' está dentro do limite ({lines}/{max_lines} linhas)."
    except Exception as exc:
        return False, 0, f"Erro ao inspecionar {filepath.name}: {exc}"


# Identificadores que não podem sumir num enxugamento: caminho, script, ID de workflow, versão
IDENT_REGEX = re.compile(r"`([^`\n]{4,160})`")


def _identificador(tok: str) -> bool:
    t = tok.strip(".,;:()")
    return bool(
        (re.fullmatch(r"[A-Za-z0-9]{16}", t) and re.search(r"[A-Z]", t) and re.search(r"[a-z]", t))
        or re.fullmatch(r"[0-9a-f]{8}", t)
        or re.search(r"\.(py|sh|mjs|js|service|timer)\b", t)
        or t.startswith(("/root/", "/var/", "/etc/", "/home/"))
    )


def check_pruning(root: Path, rev: str, state_name: str = "00_CURRENT_STATE.md") -> Tuple[bool, int, List[str]]:
    """
    Conferência do enxugamento: todo caminho, script, ID de workflow ou versão citado entre crases no estado
    da revisão `rev` (ex.: HEAD, antes de commitar o enxugamento) tem de existir em algum .md da Central hoje.
    Enxugar é mover, nunca apagar. Retorna (valido, total_identificadores, faltando).
    """
    try:
        antigo = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{state_name}"],
                                capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        return False, 0, [f"não consegui ler {state_name} em {rev}: {exc}"]

    toks = {p.strip(".,;:()") for t in IDENT_REGEX.findall(antigo) for p in t.split() if _identificador(p)}
    textos = []
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and d != ".git"]
        for f in files:
            if f.lower().endswith(".md"):
                try:
                    textos.append((Path(dirpath) / f).read_text(encoding="utf-8", errors="replace"))
                except OSError:
                    pass
    tudo = "\n".join(textos)
    faltando = sorted(t for t in toks if t not in tudo)
    return len(faltando) == 0, len(toks), faltando


def run_base_guardrail(
    target_dir: Path,
    state_file_path: Optional[Path] = None,
    max_state_lines: int = MAX_CURRENT_STATE_LINES,
    skip_network: bool = False,
    timeout: float = 5.0,
    pruning_rev: Optional[str] = None
) -> Dict:
    errors: List[str] = []
    warnings: List[str] = []

    this_file = os.path.abspath(__file__)
    all_files: List[Path] = []

    for root, dirs, files in os.walk(target_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith(".")]
        for f in files:
            p = Path(root) / f
            if os.path.abspath(p) == this_file:
                continue
            if p.suffix.lower() in TEXT_EXTENSIONS or p.name.startswith(".env"):
                all_files.append(p)

    # 1. Checagem de segredos
    secrets_found = []
    for fpath in all_files:
        viols = check_secrets_in_file(fpath)
        secrets_found.extend(viols)

    if secrets_found:
        errors.append(f"Segredos/chaves detectados ({len(secrets_found)} ocorrências):\n    - " + "\n    - ".join(secrets_found))

    # 2. Checagem do teto de linhas do 00_CURRENT_STATE.md
    if state_file_path is None:
        state_file_path = target_dir / "00_CURRENT_STATE.md"

    state_ok, state_lines, state_msg = check_state_file_ceiling(state_file_path, max_state_lines)
    if not state_ok:
        errors.append(f"[TETO MEMÓRIA] {state_msg}")

    # 2b. Conferência do enxugamento: enxugar é mover, nunca apagar
    pruning_msg = "não pedida"
    if pruning_rev:
        pruning_ok, pruning_total, faltando = check_pruning(target_dir, pruning_rev, state_file_path.name)
        pruning_msg = f"{pruning_total - len(faltando)}/{pruning_total} identificadores de {pruning_rev} ainda em algum documento"
        if not pruning_ok:
            errors.append(f"[ENXUGAMENTO] {len(faltando)} de {pruning_total} identificadores do estado em {pruning_rev} "
                          "sumiram de todos os documentos (mova o texto para um histórico em vez de apagar):\n    - "
                          + "\n    - ".join(faltando[:30]))

    # 3. Checagem de links em Landing Pages e Markdowns
    tested_urls = 0
    if not skip_network:
        urls_to_test = set()
        for fpath in all_files:
            # Foco em landing pages e documentação markdown
            if fpath.suffix.lower() in {".md", ".html"}:
                try:
                    with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                        for u in URL_REGEX.findall(text):
                            if "guardrail:ignore" not in u and not is_placeholder(u):
                                urls_to_test.add(u)
                except Exception:
                    pass

        tested_urls = len(urls_to_test)
        broken_urls = []
        for u in urls_to_test:
            ok, msg = check_url_health(u, timeout=timeout)
            if not ok:
                broken_urls.append(f"{u} -> {msg}")

        if broken_urls:
            errors.append(f"Links quebrados ou inacessíveis ({len(broken_urls)}):\n    - " + "\n    - ".join(broken_urls))

    return {
        "passed": len(errors) == 0,
        "files_scanned": len(all_files),
        "state_file_lines": state_lines,
        "state_msg": state_msg,
        "pruning_msg": pruning_msg,
        "urls_tested": tested_urls,
        "errors": errors,
        "warnings": warnings
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="Guardrail Base para CI Semente - Hebel D2C")
    parser.add_argument("--todos", action="store_true", help="Executa todas as validações determinísticas (segredos, links e teto de memória)")
    parser.add_argument("--path", default=".", help="Diretório raiz a verificar (padrão: .)")
    parser.add_argument("--state-file", help="Caminho para o 00_CURRENT_STATE.md")
    parser.add_argument("--max-state-lines", type=int, default=MAX_CURRENT_STATE_LINES, help="Teto de linhas do estado")
    parser.add_argument("--skip-network", action="store_true", help="Ignora verificação HTTP de links")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout de verificação HTTP")
    parser.add_argument("--conferir-enxugamento", metavar="REV",
                        help="Revisão do git com o estado de antes (ex.: HEAD) — confere que nenhum caminho, script ou ID sumiu")

    args = parser.parse_args()
    root_path = Path(args.path).resolve()

    # Se executado de dentro de subpasta (ex: 06 — Scripts e Automações/guardrails), busca a raiz da Central
    if not (root_path / "00_CURRENT_STATE.md").exists():
        for parent in Path(__file__).resolve().parents:
            if (parent / "00_CURRENT_STATE.md").exists():
                root_path = parent
                break

    state_path = Path(args.state_file).resolve() if args.state_file else root_path / "00_CURRENT_STATE.md"

    skip_network = args.skip_network and not args.todos

    res = run_base_guardrail(
        target_dir=root_path,
        state_file_path=state_path,
        max_state_lines=args.max_state_lines,
        skip_network=skip_network,
        timeout=args.timeout,
        pruning_rev=args.conferir_enxugamento
    )

    print("=" * 70)
    print("GUARDRAIL BASE - CI SEMENTE (HEBEL D2C)")
    print(f"Diretório raiz: {root_path}")
    print(f"Arquivos verificados: {res['files_scanned']}")
    print(f"Status Memória: {res['state_msg']}")
    print(f"Enxugamento: {res['pruning_msg']}")
    print(f"Links testados: {res['urls_tested']}")
    print("=" * 70)

    if res["passed"]:
        print("[OK] Todos os guardrails base da CI Semente foram APROVADOS.")
        return 0

    print(f"\n[FALHA] Foram encontradas {len(res['errors'])} falhas nos guardrails:\n")
    for e in res["errors"]:
        print(f"[X] {e}\n")

    return 1


if __name__ == "__main__":
    sys.exit(main())
