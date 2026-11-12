# Novidades da Central

O que mudou em cada versão, da mais nova para a mais antiga. A atualização mostra o trecho entre a sua versão e a nova.

## 1.2.0 — 2026-11-12

- **A conversa de todo dia agora é a mestre.** Ela decide, despacha e confere; tarefa grande vai para uma conversa nova
  com instrução curta e volta em poucas linhas. O Boa noite passou a reescrever um bilhete curto, o `00_SESSAO_MESTRE.md`,
  e a conferir que os combinados do dia estão escritos antes de a conversa ser limpa. O Bom dia abre vazio e lê o bilhete.
  O bilhete é seu: a atualização não toca nele. O molde está em `nucleo/modelos/00_SESSAO_MESTRE.md`.
- **Medidor de uso de tokens.** `python nucleo/ferramentas/mede_tokens.py` (no Mac e no Linux, `python3`) mostra onde foi o
  seu uso na semana, por conversa e por modelo, e explica o que pesa. Ele só lê os registros que o Claude Code já guarda no
  seu computador; nada sai daí. Uma vez por semana, o Bom dia dá a notícia em uma linha.
- **Regras novas no núcleo:** "A conversa mestre" e "Economia de tokens". O que mais consome o plano é reler o contexto a
  cada resposta, então trabalho que não precisa do histórico vai para conversa nova, saída de comando vai cortada e
  arquivo grande é lido por trecho.

## 1.1.1 — 2026-11-04

- O arquivo `LICENSE` ficou só com a licença MIT, como o GitHub espera, e a página do repositório passa a mostrar "MIT".
  O aviso sobre as habilidades que vêm de outros repositórios (offers e seo-audit) foi para o `TERCEIROS.md`. Nada muda no
  uso da Central.

## 1.1.0 — 2026-11-04

- Nova habilidade: auditoria de SEO do site (`seo-audit`). Diga "audita o SEO do meu site" e ela mostra o que impede o
  Google de achar e mostrar as suas páginas, em ordem de gravidade, com o plano para corrigir. Quando a empresa recebe
  cliente num endereço, confere também o Perfil da Empresa no Google. Origem: marketingskills, de Corey Haines (licença MIT).

## 1.0.0 — 2026-11-04

- Primeira versão distribuída pelo GitHub.
- A Central passa a separar o núcleo, que se atualiza, dos arquivos da sua empresa, que a atualização nunca toca.
- Novo comando "atualizar a Central". Ele mostra o que muda, pede o seu sim, guarda em `_arquivo/` o que você tiver mexido
  no núcleo e deixa voltar para a versão anterior.
- O Boa noite só envia a cópia de segurança para um repositório privado seu.
- Habilidades: diagnóstico da máquina, preço certo, orçamento e objeções, pauta do cliente, relatório do mês, ofertas e a
  agência de marca completa, com os cinco agentes.
