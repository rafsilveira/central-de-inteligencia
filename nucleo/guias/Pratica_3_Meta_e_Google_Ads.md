# Prática 3 — conectar o Meta Ads e o Google Ads à sua Central

O passo a passo da Prática 3 do curso Fábrica que Vende. No fim dele, a sua Central cria campanha
na Meta e no Google Ads pelo Claude Code, e você não gasta nada: sem cartão, com todas as campanhas pausadas.

**A regra da aula: primeiro a casa, depois o dinheiro.** Contas no nome da empresa, conexão provada,
medição ligada. Só depois disso alguém pensa em ativar anúncio.

**Quanto tempo leva:** de 1 a 2 horas de tela. Algumas etapas dependem de aprovação da plataforma
(a verificação da empresa na Meta, por exemplo, pode levar dias). Comece cedo e não conte com tudo no mesmo dia.

## Como usar este guia

Abra a sua Central no Claude Code e escreva:

> **vamos fazer a Prática 3: conectar o Meta Ads e o Google Ads, seguindo o guia nucleo/guias/Pratica_3_Meta_e_Google_Ads.md**

Ela vai junto com você, um passo por vez. Três dicas que resolvem quase tudo:

- **Travou numa tela? Mande um print** para a Central e diga "estou nesta página". Ela te diz onde clicar.
- **Os nomes das telas mudam.** A Meta às vezes mostra em português de Portugal ("utilizadores do sistema",
  "definições") ou em inglês. É o mesmo lugar.
- **Se você deu um nome diferente do que ela sugeriu** (no app ou no usuário do sistema), avise. Ela não enxerga a
  sua tela e vai continuar chamando pelo nome que sugeriu.

> **E o MCP oficial da Meta?** A Meta tem um servidor MCP oficial (`mcp.facebook.com/ads`), mas na gravação
> ele estava em beta e **não encontrou as contas de anúncio**. Por isso a conexão desta aula sai por um app seu.
> Quando você for fazer, peça à Central para testar o MCP primeiro: se ele listar a sua conta de anúncio, use-o e
> pule a parte 3. Se não listar, siga o guia como está.

---

## 1. Antes de começar — o que ter em mãos

- [ ] A Central instalada e a entrevista feita (Aula 0). É dela que a IA tira o contexto da sua empresa.
- [ ] O Claude Code (a IA precisa rodar comandos no seu computador).
- [ ] **O site no ar, com três páginas:** política de privacidade, termos de uso e como o cliente pede para apagar
      os dados dele. A Meta pede os três endereços para liberar o app (parte 3.6). Se faltar, peça à Central para
      escrever as páginas no seu site.
- [ ] Um e-mail da empresa e uma conta Google com esse e-mail.
- [ ] O celular à mão, para a verificação em duas etapas.
- [ ] **Verificação em duas etapas ligada** no Facebook e na conta Google. Conta de anúncio é dinheiro: sem duas
      etapas, quem roubar o seu login gasta no seu cartão.
- [ ] **Nenhum cartão.** Nesta aula você não cadastra forma de pagamento em lugar nenhum.
- [ ] O cofre pronto: em `06 — Scripts e Automações/Tokens e Configs/`, copie o `.env.example` para `.env`
      (se ainda não fez). É ali que as chaves vão morar.

---

## 2. Criar as contas — sem campanha e sem cartão

Esta parte é **à mão**. Criar a empresa na plataforma e dar acesso a pessoas é decisão de dono: a IA trabalha
dentro da casa, quem constrói a casa e entrega a chave é você. Peça à Central os links, se quiser.

### 2.1 Portfólio empresarial da Meta (o antigo Business Manager)

Em https://business.facebook.com:

1. **Confira antes se você já tem um portfólio** com o nome da empresa. Se tiver, use esse. Portfólio duplicado é
   o erro mais comum e não se desfaz fácil.
2. Se não tiver, crie um **no nome da empresa**, não no seu.
3. Ligue a **Página do Facebook** e o **Instagram** da empresa ao portfólio.
4. Em Pessoas, coloque **dois administradores**: você e uma pessoa de confiança. Conta com um dono só é a
   empresa refém de um login.
5. Já peça a **verificação da empresa** (Central de segurança). Ela leva dias e alguns passos da Meta dependem dela.

### 2.2 Conta de anúncio da Meta

Em Configurações do negócio → Contas → Contas de anúncios → Adicionar → Criar uma conta de anúncios:

- Fuso horário de São Paulo e moeda em real (BRL). **Isso não muda depois.**
- **Não adicione forma de pagamento.**
- Anote o ID da conta (aparece como `act_` seguido de números). Ele vai para o `.env` na parte 3.5.

### 2.3 Conta do Google Ads, sem criar campanha

Em https://ads.google.com entre com a conta Google da empresa. O Google empurra você a criar uma campanha
já no cadastro. **Não crie.** Tem uma saída:

1. Na tela que pede o objetivo da campanha, procure **"Mudar para o Modo Especialista"** (costuma ficar no pé da
   página, em letra pequena).
2. Na tela seguinte, escolha **"Criar uma conta sem uma campanha"**.
3. Confirme país, fuso de São Paulo e moeda em real. **Não cadastre cartão.**
4. Anote o **ID do cliente** (o número no formato `123-456-7890`, no canto de cima da tela).

Se a saída não aparecer e o Google insistir na campanha, pare. Mande um print para a Central e procure o caminho
com ela. Não crie campanha só para passar da tela.

---

## 3. Conectar a Meta — app, usuário do sistema e token

**Por que três peças:** o **app** é quem conversa com a Meta. O **usuário do sistema** é um "funcionário robô"
do seu portfólio: não depende do seu login pessoal e não sai da empresa quando alguém sai. O **token** é a chave
desse funcionário. A Central usa o token, e o token só abre o que você atribuiu ao usuário do sistema.

### 3.1 Criar o app

Em https://developers.facebook.com/apps → **Criar app**:

1. Nome do app: algo como "Central [sua empresa]".
2. Caso de uso: **Outro**. Tipo do app: **Empresa**.
3. Ligue o app ao **portfólio da empresa** (o da parte 2.1). O Facebook pede a sua senha.
4. No painel do app, adicione o produto **Marketing API** → Configurar.
   Se aparecer um botão para criar campanha ali dentro, não clique: a campanha vem depois, pela Central.

### 3.2 Criar o usuário do sistema

Em Configurações do negócio → Usuários → **Usuários do sistema** → Adicionar:

- Nome: algo como "Central [sua empresa]".
- Função: **Funcionário**.
- Avise a Central o nome que você usou.

Recém-criado, ele não tem nenhum ativo e nenhum app. É o que vem agora.

### 3.3 Atribuir a conta de anúncio e o app ao usuário do sistema

Na lista de usuários do sistema, clique no que você criou → **Atribuir ativos**:

1. **Contas de anúncios** → a sua conta → marque **Gerenciar contas de anúncios** (controle total) → Atribuir.
2. **Apps** → o seu app → marque o controle total (**Desenvolver app**) → Atribuir.
3. Dê um refresh na página e confira que os dois aparecem na lista de ativos dele.

Mais tarde, quando a Central for publicar post ou ler formulário, volte aqui e atribua também a **Página**, o
**Instagram** e o **Pixel**. O que o usuário do sistema pode, a Central pode. O que ele não tem, ela não alcança.

### 3.4 Gerar o token e escolher as permissões

Ainda no usuário do sistema, clique em **Gerar token** (no alto, à direita):

1. Escolha **o app da parte 3.1**.
2. Validade: **60 dias** para testar. Para uso de verdade, existe **Nunca**, mas aí o token vale até alguém
   revogar, e guardar bem passa a ser obrigação.
3. Permissões. Comece pelo mínimo para campanhas:
   - `ads_management` e `ads_read` — criar e ler campanhas;
   - `business_management` — enxergar os ativos do portfólio;
   - `leads_retrieval` — só se for puxar os leads dos formulários (é o que alimenta a conversão offline, mais adiante no curso);
   - `pages_show_list`, `pages_read_engagement` e `pages_manage_ads` — só quando for anunciar com a Página ou publicar.

   Dá para marcar tudo, e funciona, mas cada permissão a mais é uma porta a mais se o token vazar.
4. Gerar token. A Meta pode pedir uma confirmação pelo celular, principalmente em conta nova.
5. **Copie o token. Não cole no chat.** Não cole em print, e-mail, WhatsApp nem documento.

### 3.5 O token no cofre (`.env`), fora do chat

Com o token copiado, escreva para a Central:

> **Estou com o token da Meta copiado. Cria um script que me pede o token no terminal, sem mostrar na tela, e grava no .env como META_ACCESS_TOKEN.**

Ela escreve um script em Python que lê o token pelo terminal, com a digitação escondida, e grava no `.env`.
Rode o script e cole o token **no terminal, quando ele pedir**. A conversa com a IA nunca vê o token.

Depois, os dados que não são segredo, que pode dizer no chat:

> **O ID da minha conta de anúncio é <ID_DA_CONTA> e o app se chama <NOME_DO_APP>. Grava no .env e confere se você enxerga a conta, sem mostrar o token.**

No `.env`, fica assim (com os seus valores, nunca no git):

```
META_ACCESS_TOKEN=<SEU_TOKEN>
META_AD_ACCOUNT_ID=act_<ID_DA_CONTA>
META_APP_ID=<ID_DO_APP>
```

### 3.6 Colocar o app em modo público (Ao vivo)

Sem isso, o app fica em modo de desenvolvimento e a criação de anúncio esbarra. Na gravação este passo foi
esquecido, e foi o teste da parte 4 que avisou. É por isso que sempre se testa.

Em https://developers.facebook.com/apps → o seu app → **Configurações do app → Básico**:

1. **URL da Política de Privacidade** do seu site.
2. **URL dos Termos de Serviço**.
3. **Exclusão de dados do usuário**: o endereço da página que explica como pedir para apagar os dados.
4. **Categoria**: Negócios e páginas.
5. **Ícone do app** (1024 × 1024).
6. **Salvar alterações.** Depois, mude a chave **Modo do app** para **Ao vivo** (Live).

Se a Meta pedir a verificação da empresa para liberar algum acesso, faça (parte 2.1, item 5). Ela demora.

---

## 4. Provar a conexão — uma campanha de teste, pausada

Antes de confiar, prove. Peça à Central:

> **Cria uma campanha de teste na Meta, PAUSADA, na conta <ID_DA_CONTA>, só para provar a conexão. Nome: "TESTE — não ativar". Não ative nada e não ponha forma de pagamento.**

Depois abra o Gerenciador de Anúncios, dê um refresh e confira:

- [ ] A campanha apareceu, na conta certa.
- [ ] **Está pausada.** Se a Central também criou conjunto e anúncio (acontece, mesmo pedindo só a campanha),
      confira que **tudo** está pausado.
- [ ] Deu erro? Leia a mensagem com a Central. O mais comum é app fora do modo Ao vivo (parte 3.6) ou ativo
      não atribuído ao usuário do sistema (parte 3.3).

Pronto: a Central cria campanha na Meta. A campanha de teste pode ser apagada ou ficar pausada com o nome de teste.

---

## 5. O Pixel da Meta no site

O pixel mede quem visita o site e o que faz lá. **Ele vem antes do anúncio:** quando você ligar o primeiro
anúncio, já vai saber quantas visitas e cadastros teve sem gastar nada. Esse é o seu número de antes.

1. No Gerenciador de Eventos → **Conectar dados** (ou "Associar dados") → **Web**.
2. **Confira se já existe um conjunto de dados** (é o nome novo do pixel) do seu site. A Meta às vezes cria um
   sozinha. Se existir, use esse, não crie dois.
3. Se não existir, crie um com o nome do site e escolha **Configurar o Pixel da Meta** → **instalar o código
   manualmente** → copie o código base.
4. Entregue à Central: **"Instala este código do Pixel da Meta no `<head>` de todas as páginas do site."**
   O código do pixel não é segredo (ele fica público no seu site), então pode colar no chat. Se a Central fez o
   seu site (Prática 2), ela mesma instala.
5. **Atribua o pixel:** em Configurações do negócio → Fontes de dados → Conjuntos de dados → o seu pixel:
   ligue à **conta de anúncio** e atribua ao **usuário do sistema** (parte 3.3).
6. A Meta vai oferecer a **API de Conversões**. Pode associar agora ou depois. Ela entra de verdade na aula de
   conversão offline.
7. Confira: abra o site em outra aba e, no Gerenciador de Eventos, veja o evento PageView chegar (aba **Testar
   eventos**). Em poucos dias a visão geral mostra quantos eventos o site já tem, sem anúncio nenhum.

Guarde o ID do pixel no `.env` para a Central achar depois: `META_PIXEL_ID=<ID_DO_PIXEL>`.

---

## 6. Conectar o Google Ads — a API pelo Google Cloud

No Google o desenho é o mesmo da Meta: um "app" seu (um projeto no Google Cloud) com uma credencial, e você
autoriza esse app a mexer na sua conta do Google Ads. **A conta do Google Ads precisa existir antes** (parte 2.3).

### 6.1 Projeto no Google Cloud

Em https://console.cloud.google.com, com a conta Google da empresa:

1. No seletor de projeto, no alto, → **Novo projeto**. Nome: algo como "central-[sua-empresa]".
2. Confira que é esse projeto que está selecionado antes de seguir.

### 6.2 Ativar a Google Ads API

APIs e serviços → **Biblioteca** → procure **Google Ads API** → **Ativar**.

### 6.3 Tela de consentimento (OAuth)

Procure **Google Auth Platform** (é a antiga "Tela de consentimento OAuth") → Primeiros passos:

1. **Informações do app:** nome do app e e-mail de suporte.
2. **Público-alvo:** Externo.
3. **Dados de contato:** o e-mail da empresa.
4. Concluir.
5. Em **Público-alvo → Usuários de teste**, adicione o e-mail da conta Google que tem acesso ao Google Ads.

Atenção: enquanto o app estiver no status **Teste**, a autorização costuma vencer em 7 dias e a Central perde o
acesso. Para uso do dia a dia, em Público-alvo, clique em **Publicar app** (Em produção). Para uso interno com
uma conta só, o Google não exige revisão.

### 6.4 Cliente OAuth

Em Google Auth Platform → **Clientes** → **Criar cliente**:

1. Tipo de aplicativo: **App para computador**.
2. Nome: qualquer um. → Criar.
3. **Baixe o JSON.** Ele tem a chave secreta do cliente: é segredo.
4. Salve o arquivo dentro de `06 — Scripts e Automações/Tokens e Configs/` e diga à Central **o nome do arquivo**.
   Não abra o arquivo no chat nem cole o conteúdo dele.

### 6.5 Token de desenvolvedor (confira se ainda pede)

A API do Google Ads, por muito tempo, pediu também um **token de desenvolvedor**, que fica na **Central de API**
de uma conta de administrador do Google Ads (Administrador → Central de API). O Google tem mudado essa regra.
Peça à Central:

> **Confere na documentação atual do Google se a conexão com a Google Ads API ainda pede token de desenvolvedor e, se pedir, me diz onde pegar e qual nível de acesso eu preciso.**

Se pedir, o token novo costuma nascer com acesso só a contas de teste. O acesso para a sua conta real é pedido
ao Google e leva alguns dias. Ele vai para o `.env` pelo mesmo jeito da parte 3.5 (script no terminal, nunca no chat).

### 6.6 Autorizar e guardar no cofre

Peça à Central:

> **Usa o JSON do cliente OAuth que está em Tokens e Configs para me autorizar no Google Ads. Abre o navegador para eu entrar e grava o resultado no .env, sem mostrar nada na tela. O ID da minha conta do Google Ads é <ID_DO_CLIENTE>.**

O navegador abre, você entra com a conta Google da empresa e permite o acesso. A Central grava no `.env`:

```
GOOGLE_ADS_CLIENT_ID=<ID_DO_CLIENTE_OAUTH>
GOOGLE_ADS_CLIENT_SECRET=<CHAVE_SECRETA_DO_CLIENTE>
GOOGLE_ADS_REFRESH_TOKEN=<SEU_REFRESH_TOKEN>
GOOGLE_ADS_DEVELOPER_TOKEN=<SEU_TOKEN_DE_DESENVOLVEDOR>
GOOGLE_ADS_CLIENT_CUSTOMER_ID=<ID_DA_CONTA_GOOGLE_ADS>
```

### 6.7 Provar a conexão

> **Cria uma campanha de teste no Google Ads, PAUSADA, só para provar a conexão. Nome: "TESTE — não ativar". Orçamento mínimo, não ative nada.**

Abra o Google Ads, dê um refresh e confira: a campanha está lá, na conta certa, **pausada**.

---

## 7. O que fica DESLIGADO no fim da aula, de propósito

- [ ] **Nenhum cartão** na Meta nem no Google. Sem forma de pagamento, nada gasta, mesmo que alguém (ou a IA) erre.
- [ ] **Todas as campanhas pausadas**, inclusive as de teste. Ativar campanha é com uma pessoa, na tela da plataforma.
- [ ] **Nada de "Impulsionar publicação".** É o botão mais caro da internet: gasta sem você ter decidido o
      público, o objetivo e o que vai medir.
- [ ] **No dia em que puser cartão, a primeira coisa é o limite de gastos:** na Meta, Configurações de pagamento →
      **Limite de gastos da conta**; no Google Ads, um orçamento da conta com teto. É o teto para quando alguém errar.
- [ ] Escreva a regra no `00_MASTER_GUIDELINE.md` da sua Central, para ela valer em toda conversa:
      **"Toda campanha nasce pausada. Ativar, aumentar orçamento ou pôr cartão é decisão do dono."**

---

## 8. Checklist de segurança

- [ ] **Token, chave secreta e JSON nunca no chat**, em print, e-mail, WhatsApp ou documento. Só no `.env`
      e na pasta `Tokens e Configs/`, por script no terminal.
- [ ] **Apareceu na tela, numa gravação, numa live ou num print? Revogue e gere outro.** Apagar o print não
      adianta: quem viu, viu.
      - Meta: no usuário do sistema → **Revogar tokens** → gere um novo (parte 3.4) e rode o script de novo (parte 3.5).
      - Google: no Google Cloud → Clientes → o seu cliente → gere uma nova chave secreta e apague a antiga; ou remova
        o acesso do app na sua conta Google (Segurança → Apps de terceiros com acesso). **Revogue primeiro e só
        depois autorize de novo** (parte 6.6): revogar depois derruba também a autorização nova.
- [ ] **O `.env` e o JSON fora do git.** O `.gitignore` da semente já ignora os dois. Se mudar os nomes, confira.
- [ ] **Dois administradores** no portfólio da Meta e acesso de um segundo administrador no Google Ads.
- [ ] **Verificação em duas etapas** em todo login que mexe com anúncio.
- [ ] **Menor permissão possível.** O usuário do sistema só com os ativos que a Central usa hoje.
- [ ] **Uma conta de cada vez, e só a da empresa certa.** Se o seu login enxerga contas de outro negócio, peça à
      Central a lista de contas que ela vê e confira que só aparece a certa.
- [ ] **Revisão de acessos todo mês:** Meta → Configurações do negócio → Usuários e Integrações; Google → Segurança
      → apps com acesso à conta. O que ninguém usa sai.
- [ ] Antes de salvar a Central no git, rode o guardrail, que procura chave vazada:
      `python nucleo/guardrails/validador_base.py --todos` (no Mac e no Linux, `python3`)

---

## 9. Checklist final

- [ ] Portfólio da Meta no nome da empresa, com Página, Instagram e dois administradores.
- [ ] Conta de anúncio da Meta criada, fuso de São Paulo, real, **sem cartão**.
- [ ] Conta do Google Ads criada **sem campanha** e **sem cartão**.
- [ ] App na Meta, com Marketing API, em modo **Ao vivo**.
- [ ] Usuário do sistema com a conta de anúncio e o app atribuídos.
- [ ] Token da Meta no `.env`, gravado pelo terminal, nunca no chat.
- [ ] Campanha de teste na Meta criada pela Central e **pausada**.
- [ ] Pixel da Meta no site, ligado à conta de anúncio, recebendo eventos.
- [ ] Projeto no Google Cloud, Google Ads API ativada, tela de consentimento e cliente OAuth.
- [ ] Credenciais do Google no `.env` e o JSON na pasta `Tokens e Configs/`.
- [ ] Campanha de teste no Google Ads criada pela Central e **pausada**.
- [ ] Nenhum token apareceu na tela, ou, se apareceu, já foi revogado e trocado.
- [ ] A regra "toda campanha nasce pausada" escrita no `00_MASTER_GUIDELINE.md`.

## Depois

Com as plataformas conectadas, a Central passa a ter dados para trabalhar. O próximo passo do curso é para onde
a campanha leva (site, WhatsApp, formulário) e como saber qual campanha vende: a conversão offline.

A ferramenta não faz milagre. A IA tira a labuta de operar; quem sabe o que o seu produto entrega, para quem e
por quê, é você. Quanto mais disso estiver escrito na sua Central, melhores as campanhas que ela monta.
