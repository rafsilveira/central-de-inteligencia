---
name: atualizar-central
description: Traz a versão nova do núcleo da Central (regras, habilidades, guias) sem mexer nos arquivos da empresa. Use quando o dono disser "atualizar a Central", "tem versão nova?", "volte a Central para a versão anterior", ou quando o Bom dia avisar que saiu versão nova.
---

# Atualizar a Central

A atualização troca só o núcleo. Os arquivos da empresa (`00_CURRENT_STATE.md`, `00_MASTER_GUIDELINE.md`, as pastas
numeradas, `marca/`, `_arquivo/`, o `.env`) não são lidos nem escritos. Quem faz o trabalho é o `nucleo/atualizar.py`,
sempre do mesmo jeito. Você não troca arquivo do núcleo à mão.

No Windows, o comando é `python`. No Mac e no Linux, `python3`.

## Passos

1. **Ensaio.** Rode `python nucleo/atualizar.py`. Ele não muda nada. Mostra a versão de agora, a nova, o que muda (do
   `NOVIDADES.md`) e quais arquivos do núcleo o dono tinha mexido.
2. **Conte ao dono em linguagem simples**: o que melhora, se algum arquivo mexido por ele vai para `_arquivo/` e que os
   arquivos da empresa não são tocados. Pergunte: **"Posso atualizar?"**
3. **Só com o sim**, rode `python nucleo/atualizar.py --aplicar`. Ele troca os arquivos, confere cada um e faz o commit.
4. Diga o resultado e como voltar (o próprio script mostra o comando).
5. Se o dono tinha mexido no núcleo, ofereça levar o que ele queria para o lugar certo: uma regra no `00_MASTER_GUIDELINE.md`
   ou uma habilidade em `.claude/skills/casa-<nome>/`.

## Voltar para uma versão anterior

`python nucleo/atualizar.py --para <versão>` para o ensaio. Depois do sim, a mesma linha com `--aplicar`. As versões
disponíveis aparecem na mensagem de erro se o dono pedir uma que não existe.

## Quando dá erro

- **"há arquivos preparados para commit"**: rode o Boa noite (habilidade `rotina-diaria`) e tente de novo.
- **git ou Python faltando**: explique como instalar (git em https://git-scm.com, Python em https://www.python.org) e espere.
- **sem internet**: diga que a atualização fica para depois. Nada foi mudado.
- **"a semente trouxe arquivo num caminho que é seu"**: nada foi trocado nesse caminho. Conte ao dono e não mexa.
