# Implantação de alta segurança

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/

Um servidor seguro, disponível 24 horas por dia, 7 dias por semana, na Hetzner ou na Phala Cloud, DNS Gateway e verificações que terceiros podem repetir.

Um diário assinado comprova que os registros não foram alterados **após** a assinatura. Para casos graves, a próxima questão é se alguém poderia ter manipulado os dados **antes** da assinatura: quem executou o coletor, em qual máquina e se alguém fez login nele. Esse modo opcional implanta o coletor de forma que um terceiro possa verificar isso, utilizando registros mantidos pelo provedor de nuvem e pela Cloudflare, em vez de confiar apenas na palavra do operador.

O uso normal local e do Docker permanece inalterado. Nada aqui é executado a menos que você faça a implantação com `python -m tgwitness.cloud`, e o coletor lê seu host somente quando a implantação define `TGWITNESS_ASSURANCE`.

Diagrama de fluxo · Operador → Servidor, firewall sem regras de entrada (API do provedor); Operador → Túnel e DNS (API da Cloudflare); Servidor, firewall sem regras de entrada → Túnel e DNS (somente saída); Servidor, firewall sem regras de entrada → Chave de assinatura criada no servidor; Verifier, tokens somente leitura → Log do provedor e firewall; Verifier, tokens somente leitura → Endereço do conector de túnel e tráfego de entrada; Verifier, tokens somente leitura → Declaração assinada /api/assurance; Verifier, tokens somente leitura → Arquivo ZIP de evidências · Operador · Verifier, tokens somenteleitura · Servidor, firewall semregras de entrada · Log do provedor e firewall · Endereço do conector detúnel e tráfego de entrada · Declaração assinada/api/assurance · Arquivo ZIP de evidências · Túnel e DNS · Chave de assinatura criadano servidor · API do provedor · API da Cloudflare · somente saída

**Diagrama em formato de texto**

1. Operador → Servidor, firewall sem regras de entrada (API do provedor)
2. Operador → Túnel e DNS (API da Cloudflare)
3. Servidor, firewall sem regras de entrada → Túnel e DNS (somente saída)
4. Servidor, firewall sem regras de entrada → Chave de assinatura criada no servidor
5. Verifier, tokens somente leitura → Log do provedor e firewall
6. Verifier, tokens somente leitura → Endereço do conector de túnel e tráfego de entrada
7. Verifier, tokens somente leitura → Declaração assinada /api/assurance
8. Verifier, tokens somente leitura → Arquivo ZIP de evidências

## O que um verificador pode conferir

| Reivindicação | Como isso é verificado | Mantido por |
| --- | --- | --- |
| O servidor foi criado por meio da API do provedor em um momento específico | O objeto “Servidor” e sua criação no próprio log do provedor | Provedor |
| Ninguém utilizou os caminhos de acesso do provedor | Registro de solicitações do console, recuperação, redefinição de senha, reconstrução, ISO, imagens e backups | Provedor |
| Nada conseguiu se conectar a ele | O firewall do provedor não possui regras de entrada; o SSH fica oculto desde a primeira inicialização | Provedor (firewall), host (SSH) |
| O acesso ao painel é feito exclusivamente por meio do túnel | O tráfego de entrada do túnel é encaminhado exclusivamente para o painel; o conector é executado a partir do endereço do servidor | Cloudflare |
| Este software específico é executado | O hash assinado da árvore de código-fonte do coletor é igual a um checkout do commit implantado | Collector, verificado em relação ao Git |
| A chave de assinatura foi criada nesse servidor | A chave assina uma declaração indicando o ID do servidor do provedor e o hash do `cloud-init` que recebeu | Collector, verificado em relação ao provedor |
| O diário pertence a essa chave e a esse servidor | Cada início de processo na evidência ZIP contém a medição do host para aquele servidor | Evidências ZIP |

As métricas do host (ouvintes e processos SSH, sessões atuais, logins no `wtmp`, a inicialização) são relatadas pelo próprio coletor e são assinadas a cada início de processo e nos `host.state` registros sempre que houver alterações. Um usuário com privilégios de root no servidor poderia falsificá-las; elas complementam os registros do provedor e da Cloudflare, em vez de substituí-los.

## Provedores

| `--provider` | Credenciais | Acesso somente para leitura do Verificador | Log do provedor para o verificador | Mantido para |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Token de leitura do mesmo projeto | Ações do servidor e do firewall | Enquanto os recursos existirem |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Token de acesso pessoal somente para leitura | Ações do Droplet | Enquanto o Droplet existir |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` escopos somente leitura | Eventos de conta, versões de regras de firewall | 90 dias |
| `vultr` | `VULTR_API_KEY` | Usuário com acesso de leitura e a `activity_logs` permissão | Registro de atividades da conta (método, caminho, agente) | 30 dias, ou mais com uma assinatura do registro de auditoria |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Histórico de eventos do CloudTrail | 90 dias |
| `phala` | `PHALA_CLOUD_API_KEY` | Uma chave de API do mesmo espaço de trabalho | Revisões do aplicativo: alterações na composição e no ambiente, reinicializações, atualizações do sistema operacional | Embora o aplicativo exista |
| `generic` | nenhum | nenhum | nenhum: **autoatestado** | – |

Use um projeto, equipe, conta ou subconta dedicada para cada caso: o acesso somente para leitura do verificador exibe, então, apenas essa implantação. As credenciais são lidas a partir `--provider-token-file` da variável acima, nunca da linha de comando. Para a AWS, o arquivo contém `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; a região é `--location`.

O que os registros de cada provedor não conseguem mostrar é impresso em todos os relatórios. Resumindo: a Hetzner registra solicitações do console; o Recovery Console da DigitalOcean, o Lish/Glish da Linode e o console web da Vultr não são registrados como tal, portanto, o acesso root é bloqueado na primeira inicialização e um login no console exigiria uma redefinição de senha ou uma alteração na inicialização, o que é registrado. A Vultr retorna o endereço do console para qualquer chave capaz de ler a instância; nem o registro nem o relatório o armazenam.

## VM confidencial na Phala Cloud (Intel TDX)

Com `--provider phala` o coletor é executado em uma máquina virtual confidencial Intel TDX na [Phala Cloud](https://phala.com/), gerenciada pelo dstack. O host e a equipe da Phala não podem ler sua memória, e o processador assina um atestado do que a máquina inicializou. O verificador não aceita a palavra da Phala: `tgwitness.tdx` verifica cada atestado por conta própria, até a Intel SGX Root CA fixada, comparando-o com as listas de revogação da Intel e os dados de plataforma assinados pela Intel, e rejeita máquinas que possam ser depuradas ou migradas.

| Entrada de relatório | O que ele mostra |
| --- | --- |
| `tdx_binding` | O atestado abrange a declaração assinada do coletor e o valor aleatório desta solicitação |
| `tdx_quote` | A Intel garante a certificação; ela só é aprovada quando a Intel classifica a plataforma como atualizada |
| `tdx_compose_hash` | O RTMR3, reproduzido a partir do log de eventos do dstack, mede a composição do aplicativo que o coletor relata |
| `tdx_compose` | Esse código é, byte por byte, o mesmo que o código do commit implantado compila: arquivos-fonte fixados por hash, ambas as imagens por digest, sem nenhum outro código |
| `tdx_identity` | A certificação é fornecida pelo aplicativo e pela instância implantados, com chaves do KMS da Phala e um disco criptografado |
| `tdx_os` | Com `--tdx-measurements`, MRTD e RTMR0-2 equivalem aos valores calculados a partir da imagem do sistema operacional dstack (`dstack-mr measure --json`) |

Cada inicialização do coletor registrada no diário traz esse atestado, de modo que `verify --evidence` verifica cada inicialização. A lista de revisões do aplicativo do Phala serve como log do provedor: se a composição tiver sido alterada após a implantação, o relatório falha.

No painel, selecione **“Máquina virtual confidencial · Phala Cloud”** em **“Extras”** → **“Servidor 24/7”** e cole uma chave de API do Phala Cloud; o túnel rápido funciona da mesma forma que no Hetzner. Na linha de comando:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` lê os certificados e as listas de revogação da Intel a partir de um arquivo, em vez de baixá-los do site da Intel. O Gateway DNS não está disponível aqui: o Phala não possui firewall do provedor para tráfego de saída.

Um atestado não pode descartar uma falha no módulo TDX ou no microcódigo da Intel, nem o acesso físico ao barramento de memória. Quem controla o aplicativo na conta do Phala pode implantar outra composição; ela aparece como uma nova revisão com um novo hash de composição. O host controla a fonte de tempo da máquina e a rede.

## Antes de começar

1. Uma zona do Cloudflare, seu ID de conta e um token de API com permissões para **“Cloudflare Tunnel Edit**”, **“Zone Read”** e **“DNS Edit**”, fornecido com `--cloudflare-token-file` ou `CLOUDFLARE_API_TOKEN`. Para o verificador: **Cloudflare Tunnel Read**, **DNS Read** e, para o log de auditoria, **Account Settings Read**. Sem um domínio, um [túnel rápido](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#quick-tunnel-without-a-domain) não precisa de nada disso.
2. Credenciais do provedor com acesso de gravação a um projeto dedicado; `lock` usa o mesmo:

   - Hetzner: token de API com permissão de leitura e gravação;
   - DigitalOcean: token de acesso pessoal com permissão de gravação;
   - Linode: token de acesso pessoal com `linodes`, `firewall` e `events` escopo de leitura/gravação;
   - Vultr: chave de API de uma conta dedicada ou subconta;
   - AWS: credenciais do IAM permitidas `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` e `ec2:RevokeSecurityGroupIngress`.
3. O commit a ser executado. Uma tag de lançamento é resolvida uma única vez para seu commit com `git ls-remote`; o servidor sempre recebe apenas o commit de 40 caracteres.

## No painel

No seu próprio computador, **Extras → Servidor 24/7** executa o mesmo `deploy` para a Hetzner em três etapas: escolha Europa ou Estados Unidos, cole um token da Hetzner (Leitura e Gravação) e, em seguida, verifique o tipo de servidor, o preço mensal, o endereço e a versão que o painel encontrou com esse token. Nada é criado antes de você confirmar. O painel mostra cada etapa conforme `deploy` é relatado e, em seguida, o endereço, o token do painel e a impressão digital da chave de assinatura. Sem um domínio, o servidor recebe um [túnel rápido](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **em “Seus servidores” → “Encontrar o endereço atual”,** ele é consultado novamente após uma reinicialização. Para um endereço fixo sob seu próprio domínio, abra **“Opcional · seu próprio domínio”** e adicione um token do Cloudflare (o link preparado seleciona “Leitura da Zona”, “Edição de DNS” e “Edição do Túnel do Cloudflare”).

Os tokens são transmitidos a cada solicitação da aba do navegador para TgWitness no mesmo computador e não são gravados em nenhum lugar; o registro de implantação, o cloud-init editado, o token do painel e, para um túnel rápido, a chave de endereço são mantidos `deployments/NAME` dentro do diretório de dados. O painel oferece isso apenas ao administrador principal em uma conexão direta de loopback (`127.0.0.1`, sem cabeçalhos de proxy ou túnel); um painel acessado pela rede exibe os comandos em vez disso. A versão é padronizada para a tag de lançamento do painel em execução, resolvida por meio da API do GitHub. Localização, tipo de servidor e preço vêm da API da Hetzner: `cpx22` onde estiver disponível; caso contrário, o tipo x86 mais barato com pelo menos 2 GB de memória.

## Túnel rápido sem domínio

`--quick-tunnel` substitui `--zone`, `--cloudflare-account` e `--panel-host`; nenhuma conta ou token do Cloudflare está envolvido:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

No servidor, o cloudflared abre um [túnel rápido](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) para o painel: um endereço aleatório `https://….trycloudflare.com` que muda sempre que o cloudflared ou o servidor é reiniciado. Um pequeno serviço no servidor publica cada endereço em um tópico aleatório do ntfy.sh , assinado (HMAC-SHA256) com uma chave que só o diretório de implantação possui (`address-key.txt`), e o repete a cada três horas, pois o ntfy.sh mantém as postagens por 12. `deploy` e **o “Find the current address”** aceitam apenas postagens assinadas, de modo que uma postagem falsificada não pode enviar você e seu token do painel para o endereço de outra pessoa. O tópico fica registrado e no cloud-init publicado: quem quer que os tenha pode ler o endereço atual, que ainda solicita o token do painel. O servidor não mantém nenhuma porta de entrada de qualquer forma.

Quanto custa: nenhuma conta do Cloudflare mantém registros de um túnel rápido, portanto `verify` os relatórios sobre o túnel, o conector e a verificação de DNS aparecem como indisponíveis e o resultado é, na melhor das hipóteses, `incomplete`; os registros do provedor, o firewall, a declaração assinada, as medições do host e a comparação do instalador são verificados normalmente. A comparação de bytes com o instalador de referência requer um commit implantado que já conheça `--quick-tunnel`; um checkout da versão 0.7.0 compila o instalador do domínio e relata a diferença. A Cloudflare não oferece garantia de tempo de atividade para os túneis rápidos, permite 200 solicitações em andamento e não transmite Server-Sent Events; portanto, as atualizações em tempo real do painel (versões posteriores à 0.7.0) podem não chegar por meio de um deles, e a visualização precisa ser recarregada; essa parte ainda não foi testada. Para um caso que precise permanecer ativo, use seu próprio domínio.

## Implantar

Veja tudo o que será enviado primeiro. `plan` Não faz nenhuma solicitação ao provedor nem à Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Em seguida, faça a implantação com as mesmas opções e as credenciais:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Tipos de servidor para começar: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` e `--image` por padrão, o Ubuntu 24.04 de cada provedor em uma região europeia.

`--repository` pega o commit de outro repositório Git https, sem credenciais na URL (por padrão `https://github.com/phishdestroy/TgWitness.git`). `deploy` também aceita `--out` para outro diretório de implantação (padrão `deployments/NAME`; um diretório que já contenha uma implantação é recusado) e `--wait`, o tempo em minutos a ser aguardado pela declaração assinada do coletor: 1 a 240, padrão 20, ou 60 para `generic`.

O comando:

1. cria um túnel Cloudflare cujo ingresso encaminha o nome de host do painel para o próprio painel e, se fornecido, o nome de host da testemunha para `/api/witness/head` e `/api/assurance` somente;
2. cria registros CNAME proxy para esses nomes de host, rejeitando nomes que já existam;
3. cria um firewall de provedor sem regras de entrada e um servidor atrás dele sem chave SSH, sem backups, sem agente de console e com o cloud-init que oculta o SSH, bloqueia o root, instala `cloudflared`, busca exatamente o commit, verifica-o e inicia TgWitness como um serviço systemd reforçado;
4. aguarda a declaração assinada do coletor e verifica se ela menciona este servidor e o hash deste cloud-init.

`deployments/case-2026-11/` em seguida, contém:

| Arquivo | Índice | Compartilhar? |
| --- | --- | --- |
| `deployment.json` | IDs, hashes, as chamadas de API realizadas (método, caminho, status) e a primeira declaração assinada | Sim, com o verificador |
| `cloud-init.redacted.yaml` | O comando exato do `cloud-init` com seus dois segredos substituídos por `REDACTED` | Sim |
| `panel-token.txt` | O token do painel | Não |

A senha de root do provedor, o token do túnel e o token do painel nunca são gravados `deployment.json`. Publique a impressão digital do coletor exibida no final por meio de um canal que você não controle sozinho, por exemplo, um canal de testemunhas ou uma mensagem ao destinatário.

Faça login no Telegram em `https://case.example.org` com o token do painel, conforme descrito no [guia da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/). As ações do painel são registradas no diário assinado; elas não são sessões SSH. Uma [testemunha](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/) pode consultar `https://case-witness.example.org`.

Não há SSH: se o bootstrap falhar, o coletor nunca responderá. Exclua o servidor e implemente novamente, ou use uma implantação de depuração para identificar a causa.

### Segredos nos dados do usuário

O cloud-init contém dois segredos: o token do painel e o token do túnel do Cloudflare. A chave de assinatura não está entre eles; ela é criada no servidor. Hetzner, DigitalOcean e Linode não retornam dados do usuário por meio de suas APIs. O Vultr os retorna para qualquer chave que possa ler a instância, e o EC2 por meio `DescribeInstanceAttribute`. Para a AWS, forneça ao verificador apenas as três ações da tabela, nunca `ec2:Describe*`. Para o Vultr, suponha que a chave do verificador possa ler ambos os tokens. Um token de túnel permite que alguém execute um segundo conector: `verify` relata qualquer conector que não esteja no servidor, e as declarações do coletor não podem ser falsificadas dessa forma, pois cada uma assina um desafio novo. Com `--quick-tunnel` o segundo segredo é, na verdade, a chave de endereço: quem quer que a leia pode enviar um endereço falso que o painel aceitaria.

A declaração pública do coletor omite o endereço do servidor e as fontes dos logins; ambos permanecem no registro assinado.

## Depuração de implantação e bloqueio

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` mantém o SSH para uma chave de um endereço ou de uma rede pequena, no máximo um /24 para IPv4 ou um /48 para IPv6. `KEY` já está registrado junto ao provedor: o nome ou ID de uma chave SSH no projeto Hetzner, o ID ou impressão digital de uma chave SSH na equipe DigitalOcean, um nome de usuário Linode cujas chaves SSH do perfil são adicionadas ao root, o ID de uma chave SSH na conta Vultr ou o nome de um par de chaves EC2 na região. Essas opções não se aplicam a `generic`. Essa implantação é registrada como `debug` e **nunca** é relatada como de alta segurança. Quando terminar, execute `sudo tgwitness-lock` como o último comando da última sessão SSH e, em seguida:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

O firewall perde todas as regras de entrada. Os relatórios mostram, então, quando o SSH foi permitido e quando foi bloqueado; essa janela permanece visível.

## Remover uma implantação

`destroy` Exclui o servidor e seu firewall, identificados pelo rótulo da implantação, de modo que uma implantação que falhou no meio do processo também seja removida; em seguida, os registros DNS que apontam para seu túnel e o próprio túnel. O diário do servidor e a chave de assinatura são excluídos junto com ele: exporte as evidências primeiro. O registro permanece, marcado `removed`, com as chamadas de API da remoção.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

A remoção por meio da API está implementada para a Hetzner. Para outros provedores `destroy` , antes de excluir qualquer coisa, o sistema identifica o rótulo a ser excluído no console do provedor. Um servidor instalado manualmente (`generic`) perde apenas seu túnel e seus registros de DNS. Uma implantação rápida de túnel não requer token do Cloudflare: seu túnel termina no servidor, e suas postagens expiram do ntfy.sh em 12 horas.

## Qualquer servidor (autocertificado)

`--provider generic` é para um servidor adquirido ou instalado manualmente. `deploy` cria o túnel e o DNS, grava `install.sh` (privado) e `install.redacted.sh` (para publicar), e aguarda. Copie `install.sh` para um servidor Ubuntu 24.04 recém-instalado e execute-o lá:

```
sudo bash install.sh
```

Ele registra o host tal como estava (logins, contas, `authorized_keys`, soquetes de escuta, serviços, tarefas agendadas, pacotes), instala o commit, ativa o firewall do host, se exclui , mascara o SSH e encerra a sessão. O relatório para tal servidor é, na melhor das hipóteses, **AUTOATESTADO**: quem quer que tenha executado o instalador já possuía privilégios de root antes disso, e nenhum registro do provedor está disponível para o verificador. Ainda assim, é melhor do que um servidor sem explicação: o inventário, o hash do instalador e todos os logins posteriores são assinados.

## Verificar

O verificador precisa `deployment.json`o instalador publicado, credenciais somente leitura e, de preferência, um checkout do commit e uma evidência ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Todos os valores do provedor e da Cloudflare são solicitados pelo verificador naquele momento; o registro fornece apenas os IDs a serem consultados. O código de saída é 0 para **APROVADO**, 1 para **REPROVADO** e 2 para **REVISÃO**, **INCOMPLETO** ou **AUTOATESTADO**. `--fingerprint` deve vir de um canal independente ; sem ele, a chave é comparada apenas com o registro do operador. `python verify.py` ainda verifica a evidência ZIP por conta própria, como em [Evidence](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/).

As ações do provedor são classificadas: criação e inicialização dentro de 30 minutos após a criação são aprovadas; console, recuperação, redefinição de senha, reconstrução, ISO, imagens, instantâneos, backups, Systems Manager, EC2 Instance Connect e aberturas de firewall são reprovadas; ações relacionadas à energia e qualquer coisa inesperada são marcadas para revisão. Uma ação desconhecida nunca passa despercebida.

## Relatório para entrega de provas

`--report report.md` escreve o relatório em Markdown e `report.json` ao lado dele:

1. resultado, impressão digital da chave do coletor, implantação, provedor, commit, servidor, firewall, túnel;
2. cada verificação com seu status e fonte (API do provedor, API do Cloudflare, relatório do coletor, diário de evidências);
3. o registro do provedor com a avaliação de cada ação e, quando o provedor o registra, o autor;
4. os endpoints da Cloudflare que armazenam as conexões, a configuração e o log de auditoria do túnel;
5. a declaração assinada do coletor;
6. o que o relatório estabelece e o que ele não estabelece;
7. comandos para reproduzi-lo e o SHA-256 de cada arquivo que foi fornecido.

Entregue o relatório, `report.json`, `deployment.json`, o instalador publicado e as evidências ZIP. Elabore o relatório com antecedência: os registros dos provedores são mantidos por períodos limitados.

## Cloudflare como testemunha externa

Tudo aqui é opcional. Mesmo sem uma conta no Cloudflare, o servidor continua funcionando, e duas dessas opções funcionam hoje:

| O que | O que ele mostra | Em TgWitness |
| --- | --- | --- |
| Túnel rápido ou o túnel do seu domínio | O acesso ao painel é feito exclusivamente por meio do túnel | o assistente de servidor, veja acima |
| drand relay `drand.cloudflare.com` | os registros após uma rodada do drand são mais recentes do que ele: o diário foi escrito à medida que as coisas aconteciam | modo de evidência, **Mais testemunhas**, sem conta ([formato](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Notificações sobre o estado do túnel | quando o túnel estava fora do ar, por e-mail ou webhook da Cloudflare | configure-os no painel do Cloudflare |
| Gateway DNS (`--gateway-dns`, ou **Cloudflare Gateway DNS** no assistente) | todos os nomes que o servidor consultou, respondidos pela Cloudflare via TLS; o firewall da Hetzner não permite que o DNS acesse mais nada; se uma política do Gateway poderia reescrever as respostas | Hetzner, plano Zero Trust gratuito, sem domínio; `verify` verifica o firewall, a localização, o registro de logs, as políticas, as consultas do servidor e o log de auditoria; o modo de evidência copia o log para o diário |
| Gateway com o Cloudflare: um cliente no servidor, um firewall de saída que permite apenas o Cloudflare | todas as conexões feitas pelo servidor, não apenas as de DNS | ainda não desenvolvido |
| Acesso na parte frontal do painel | quem acessou o painel e quando | não implementado: requer seu próprio domínio |
| Registro de comandos SSH | cada comando em uma sessão de depuração | ainda não desenvolvido |

O Logpush, que manteria a cópia própria da Cloudflare no R2, é um recurso Enterprise: no plano gratuito, a Cloudflare responde `logpush is not enabled for this account`. Seu log do Gateway permanece por 24 horas nesse local; portanto, o modo de evidência o copia para o diário assinado (**o log do Cloudflare Gateway das consultas DNS deste servidor**, um token somente leitura com o recurso “Account Analytics Read”).

Sem um plano Zero Trust, uma conta possui um único endereço DNS. Quando a Cloudflare recusa outro, o servidor compartilha o endereço existente e suas consultas são diferenciadas por meio desse endereço; esse filtro também requer o Zero Trust PII Read e `destroy` deixa uma localização compartilhada. Uma consulta de log abrange no máximo três horas, portanto, a cópia e a `verify` leitura do dia em intervalos de três horas.

O Gateway DNS abrange o resolvedor do sistema. O DNS sobre HTTPS na porta 443 para outro resolvedor e conexões a um endereço que não foi consultado em lugar algum (os data centers do Telegram, por exemplo) não constam em seu log.

A Cloudflare não tem acesso ao conteúdo criptografado do Telegram, a outros dispositivos na conta do Telegram (a lista de dispositivos do modo de evidência os registra a partir do lado do Telegram) nem ao hipervisor do provedor.

## O que isso não estabelece

- O provedor e sua equipe controlam o hipervisor, os discos e a rede.
- As medições do servidor são auto-relatadas pelo coletor.
- Os conteúdos das regras de firewall anteriores não constam em todos os logs dos provedores; apenas a Linode mantém as versões das regras.
- Isso não traz nada de novo sobre a autenticidade das mensagens; consulte a seção [“Evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)”.

Ainda não foi testado com contas reais: uma implantação em seu próprio domínio (túnel do Cloudflare e DNS), os outros provedores, uma implantação de depuração e `lock`, uma conta do Telegram nesse servidor, e as atualizações em tempo real de versões posteriores por meio de um túnel rápido. Verifique a primeira implantação em cada provedor com `plan`, uma implantação de depuração e `verify` antes de confiar nela em um caso.
