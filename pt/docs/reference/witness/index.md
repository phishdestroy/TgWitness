# Testemunha independente

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/

Execute uma instância do TgWitness com sua própria chave e bot, publique pontos de verificação assinados em um canal e compare as exportações com esses pontos.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidências e verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

![Evidências e verificação](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) · [Alta segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/) · [Guia do painel](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#extras)

Uma testemunha mantém pontos de verificação assinados separadamente do coletor. Ela verifica a assinatura do coletor e a continuidade do diário, assina o resultado com sua própria chave e o publica em um canal do Telegram. Execute-a em um servidor separado com acesso somente leitura ao ponto de extremidade da testemunha do coletor.

Diagrama de fluxo · Coletor → Testemunha (ponto de verificação assinado: contagem de registros + hash do cabeçalho); Testemunha → Diário de evidências, chave própria; Testemunha → Canal do Telegram (postagem assinada por meio de seu próprio bot); Arquivo ZIP de evidências → verify.py; Diário de evidências, chave própria → verify.py; Canal do Telegram → verify.py (Exportação do Telegram Desktop ou página “t.me/s”) · Coletor · Testemunha · Diário de evidências,chave própria · Canal do Telegram · Arquivo ZIP de evidências · verify.py · ponto de verificação · assinado: contagem de · registros + hash do · cabeçalho · postagem assinada por meio · de seu próprio bot · Exportação do Telegram · Desktop ou página “t.me/s”

**Diagrama em formato de texto**

1. Coletor → Testemunha (ponto de verificação assinado: contagem de registros + hash do cabeçalho)
2. Testemunha → Diário de evidências, chave própria
3. Testemunha → Canal do Telegram (postagem assinada por meio de seu próprio bot)
4. Arquivo ZIP de evidências → verify.py
5. Diário de evidências, chave própria → verify.py
6. Canal do Telegram → verify.py (Exportação do Telegram Desktop ou página “t.me/s”)

**Nesta página**

- [O que a testemunha obtém e o que ela não obtém](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [O que ela verifica e registra](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#what-it-checks-and-records)
- [Executar uma testemunha](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#run-a-witness)
- [Página de prova pública para várias áreas de trabalho](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#verify)

## O que o TgWitness oferece e o que ele não oferece

| A testemunha possui | A testemunha nunca tem |
| --- | --- |
| Um **token de testemunho** somente leitura para um espaço de trabalho | As credenciais de sessão do Telegram ou da API do coletor |
| Sua própria chave Ed25519 e seu próprio registro | O cofre do coletor, a chave de assinatura ou o token do painel |
| Seu próprio token de bot do Telegram | Conteúdo da mensagem: o cabeçalho contém a contagem de registros e um hash |

O token é criado em **Extras → Testemunha independente**, exibido uma única vez e armazenado apenas como um SHA-256. Ele abre exatamente um endpoint, `GET /api/witness/head`, que retorna um ponto de verificação recém-assinado, além de contadores de coleções sem conteúdo assinados e o estado operacional. Ele não pode abrir o painel, ler o conteúdo das mensagens ou alterar configurações, e o token do painel não é aceito nesse local. Revogue um token na mesma página. O coletor registra quando uma nova chave de testemunha começa a verificar (`witness.seen`) e exibe a última verificação por token; uma testemunha que não tenha verificado em 2,5 intervalos é marcada como atrasada.

Novas testemunhas enviam um desafio aleatório em cada enquete; a declaração de captura o repete sob a assinatura do coletor. Os contadores estão vinculados ao ponto de verificação exato e são incluídos nas postagens assinadas das testemunhas. Cabeçalhos legados continuam sendo aceitos pela testemunha autônoma. O aumento do diário, por si só, nunca é contabilizado como uma nova mensagem.

## O que ela verifica e registra

A cada intervalo (10 minutos por padrão), o TgWitness:

1. busca o cabeçalho por conta própria (o coletor não pode inseri-lo nem ignorá-lo);
2. Verifica a assinatura do coletor, a chave fixada do coletor (`--collector-fingerprint`, ou a primeira chave encontrada), uma contagem não decrescente e um cabeçalho inalterado com uma contagem inalterada. As provas de inclusão e consistência de Merkle verificam se um diário crescente se estende até o ponto de verificação retido. Uma vez que as provas de continuidade tenham sido utilizadas, sua remoção é rejeitada;
3. anexa um registro assinado ao seu próprio diário: `witness.anchor` com status `ok`, `key_changed`, `rollback` (menos registros do que antes), `fork` (mesmo comprimento, cabeçalho diferente ) ou `invalid` (a resposta não passou na verificação), ou `witness.no_response` quando o coletor não respondeu;
4. publica o resultado no canal, assinado, incluindo “sem resposta” enquanto o TgWitness estiver em execução e puder acessar a API do bot. O ID da publicação é registrado (`witness.posted`), assim como uma publicação com falha (`witness.post_failed`).

Uma postagem tem a seguinte aparência; a última linha contém a declaração assinada:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Execute um testemunho

É necessário um bot do Telegram (crie um com @BotFather), um canal no qual esse bot seja administrador e o endereço do coletor acessível a partir do testemunho — via HTTPS fora de uma rede privada (consulte o perfil HTTPS na seção de [implantação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)).

Abra **Extras → Testemunha independente → Configurar** no painel. Três etapas abrangem o acesso somente leitura, seu canal e intervalo, e, por fim, a ativação da testemunha. A política de publicação, o proxy HTTP/SOCKS5 opcional e o endereço personalizado da API do bot estão nas **configurações avançadas**. O formulário baixa `witness.json` com a chave do coletor deste espaço de trabalho fixada. Baixe o token de somente leitura recém-criado com **“Salvar arquivo de acesso** como” `witness-token.txt`; coloque-o e um `bot-token.txt`arquivo criado no host da testemunha ao lado desse JSON. O coletor nunca recebe o token do bot. O download não inicia um serviço nem publica uma mensagem. Nenhuma testemunha de projeto hospedado é implicitamente cadastrada.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

O primeiro comando verifica os arquivos de configuração e os arquivos secretos sem solicitações de rede ou criação de chaves. Os caminhos no JSON são relativos a esse arquivo; os caminhos da CLI/ambiente são relativos ao diretório de trabalho. Mantenha a impressão digital da testemunha fora de seu host. O indicador de última sondagem do coletor confirma apenas uma solicitação; a publicação é relatada pelo Proof ou verificada no diário da testemunha e no canal.

Caso o painel permaneça atrás de um túnel SSH, exponha apenas o endpoint de testemunho delimitado em um nome de host HTTPS separado, conforme [este exemplo do Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). O espaço de trabalho padrão utiliza então `https://witness.example.org`; outros espaços de trabalho utilizam `https://witness.example.org/profiles/ID`. Os tokens continuam sendo necessários; o painel e suas outras rotas de API não são encaminhadas por esse host virtual.

Escolha `all` para pontos de verificação publicados regularmente. Um intervalo de cinco minutos significa cerca de 288 publicações por espaço de trabalho por dia. `changes`/`problems` deixam deliberadamente algumas verificações sem publicação. O MTProxy destina-se ao cliente do Telegram do coletor. A sondagem HTTP do Witness e a API HTTPS do Telegram para bots utilizam suas próprias rotas diretas/HTTP/SOCKS5 ([API do bot](https://core.telegram.org/bots/api)).

**Juntamente com o coletor, usando o Docker** (mesmo host — processo e chave independentes, mas o mesmo operador): insira os valores em `.env` e inicie o perfil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Ao utilizar uma imagem publicada, utilize o código `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**No servidor de terceiros** (uma testemunha independente de fato): copie o repositório para lá, defina `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` mais os três valores acima em `.env` e, em seguida,

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

ou sem o Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Publicar no Discord

Uma testemunha pode postar em um canal do Discord em vez de no Telegram. No Discord, abra **Editar Canal → Integrações → Webhooks**, crie um webhook e copie sua URL. No painel, escolha **Webhook do Discord · seu canal** na etapa 2. No servidor da testemunha, salve a URL como `discord-webhook.txt` ao lado de `witness.json`; ela nunca chega ao coletor.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Uma testemunha tem um único editor: um canal do Telegram ou um webhook do Discord, mas não ambos. As postagens contêm a mesma declaração assinada e não podem enviar notificações a ninguém. Uma postagem com mais de 2.000 caracteres, conforme o limite do Discord, é substituída por uma linha curta com a verificação completa anexada como `witness-check.txt`. Cada ID de postagem é registrado como `witness.posted`. `verify.py --channel`lê apenas exportações de canais do Telegram; portanto, para o Discord, mantenha o diário de testemunhas: ele contém todas as verificações.

### Opções

| Opção | Ambiente | Padrão | Significado |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Intervalo entre verificações: 1–1.440 |
| `--timeout` | `_TIMEOUT` | 30 | Tempo de espera para o coletor e a API do bot: 5–600 segundos |
| `--post` | `_POST` | `all` | `all`: todas as verificações; `changes`: uma nova questão ou um problema; `problems`: apenas problemas e respostas ausentes |
| `--title` | `_TITLE` | `TgWitness witness` | Primeiras palavras de cada postagem no canal |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Salve a chave do coletor em vez de confiar na primeira resposta |
| `--proxy` | `_PROXY` | direto | `socks5://host:port` ou `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Endereço da API do bot, por exemplo, um servidor local da API do bot |
| `--data-dir` | `_DATA` | `witness-data` | Chave de testemunho e registro |
| `--config` | `_CONFIG` | – | Arquivo JSON com qualquer uma das opções acima |

O endereço do coletor, os tokens e o canal provêm de `--collector`, `--token` ou `--token-file`, `--bot-token` ou `--bot-token-file`, `--discord-webhook-file` e `--channel`, ou `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` e `_CHANNEL`, o que mantém os segredos fora da lista de processos.

Um arquivo de configuração utiliza nomes de opções com sublinhados, além de “`texts`”, que substitui as palavras das publicações do canal:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Chaves `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. A linha de comando tem prioridade sobre o ambiente, e o ambiente sobre o arquivo. Opções desconhecidas ou chaves de texto interrompem o TgWitness com uma mensagem, em vez de serem ignoradas. A redação nunca afeta a verificação: o verify.py verifica o token assinado ao final de cada publicação. Com `--post changes` ou `problems`, as verificações que não foram publicadas ainda constam no diário de testemunhas e `verify.py` as lista como nunca publicadas; o registro inicial indica a política. Todas as verificações ainda aparecem no diário, portanto, menos publicações significam menos momentos independentes no Telegram, e não menos verificações.

Mesmo sem um canal, o TgWitness continua mantendo seu diário. Guarde a impressão digital da chave do TgWitness (`python -m tgwitness.witness fingerprint`) em outro local.

## Página pública de comprovação para vários espaços de trabalho

`python -m tgwitness.proof` O TgWitness monitora até 32 espaços de trabalho ao mesmo tempo e exibe uma página somente leitura com a verificação assinada mais recente de cada um. Cada espaço de trabalho recebe sua própria chave de testemunha e diário na pasta de dados, além de uma chave de coletor fixada; a publicação em um canal do Telegram é opcional para cada espaço de trabalho. Comece com o arquivo [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| Campo | Significado |
| --- | --- |
| `title` | Título da página, 1–100 caracteres |
| `data_dir` | Chaves e diários do Witness, relativos ao arquivo; padrão `proof-data` |
| `interval`, `timeout` | Minutos entre verificações (1–1.440, padrão 5); segundos de espera (5–600, padrão 20) |
| `workspaces[].id`, `label` | Alias curto em letras minúsculas e o nome exibido |
| `workspaces[].collector` | Endereço do coletor; outros espaços de trabalho terminam em `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Obrigatório, varia de acordo com cada espaço de trabalho |
| `workspaces[].token_file` | Arquivo com o token de testemunha somente leitura desse espaço de trabalho |
| `workspaces[].channel`, `bot_token_file` | Opcional, em conjunto: publique cada verificação em um canal |
| `workspaces[].proxy`, `bot_api` | Rota opcional e endereço da API do bot |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

O primeiro comando valida o arquivo e os arquivos de token sem estabelecer uma conexão. A página responde apenas aos métodos GET e HEAD:

- `/` Mostra todos os espaços de trabalho; um espaço de trabalho sem verificação por 2,5 intervalos é marcado como obsoleto.
- `/api/proof` retorna o mesmo que JSON.
- `/api/proof/<id>` baixa a declaração assinada mais recente (`tgwitness-public-proof-v1`): número e hash do registro de testemunha, status, chave do coletor fixada, ponto de verificação, contadores de coleta e se a publicação no canal foi bem-sucedida, assinada pela chave de testemunha daquele espaço de trabalho.
- `/healthz` Retorna o código de erro 503 quando o monitor de um espaço de trabalho é desativado.

Atribua à página seu próprio nome de host, como em [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). Para verificação, exporte o diário de testemunho de um espaço de trabalho com `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` e use-o conforme descrito abaixo.

## Verificar

Do lado da testemunha, exporte seu diário:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Em seguida, em qualquer lugar, com o arquivo ZIP assinado pelo coletor e o canal exportado do Telegram Desktop (*Exportar histórico de bate-papo* → JSON gera `result.json` ) ou sua página pública `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

O `verify.py` verifica o diário de testemunho (cadeia e assinaturas) e, em seguida, verifica se **cada cabeçalho**que **a testemunha observou faz parte do diário exportado**: o registro naquela contagem deve ter exatamente esse hash. Um cabeçalho que não corresponder falha na verificação — o diário foi alterado após a testemunha tê-lo observado. Ele também relata cabeçalhos vistos após a exportação, anomalias que a testemunha registrou, respostas que falharam, períodos cujos pontos de verificação correspondentes estão presentes nesta exportação (“Testemunhado de X a Y”) e lacunas. Pontos de verificação posteriores não prolongam esses períodos. O resultado inclui o último número de registro correspondente e o número de registros subsequentes sem um ponto de verificação correspondente. Apenas respostas assinadas pela própria chave da exportação são contabilizadas: uma exportação assinada por uma chave que a testemunha nunca viu é relatada como não testemunhada e, sem `--fingerprint`, seu signatário permanece não vinculado. Com o `--channel`, cada postagem assinada deve corresponder ao diário da testemunha registro por registro: postagens alteradas falham na verificação, e as postagens ausentes são listadas. Uma data em uma exportação JSON do Telegram fornecida é um metadado editável, fora do token de testemunha assinado. A correspondência com o token não autentica a data de publicação; o resultado relata explicitamente que a verificação da hora de publicação não foi realizada.

### Exigir um limite de exportação testemunhado

Para uma transferência que deva incluir um registro final testemunhado, adicione `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Isso requer a impressão digital da testemunha mantida de forma independente e um ponto de verificação correspondente exatamente no final desta exportação. Um ponto de verificação que abranja apenas um prefixo anterior é insuficiente. Interrompa a coleta, permita que a testemunha observe o estado final e exporte antes de novas gravações no diário; caso o diário seja alterado, mantenha outro ponto de verificação e exporte esse estado. Um ponto de verificação posterior, por si só, não pode verificar o hash final de uma exportação mais curta. Quando `--channel` também é fornecido, a ausência de postagens declaradas ou um conjunto de correspondências vazio fazem com que essa verificação rigorosa seja reprovada. Sem o sinalizador, as verificações de integridade comuns ainda relatam registros não testemunhados sem rejeitar um arquivo que, de outra forma, estaria intacto.

Mantenha o diário da testemunha e sua chave fixada separadamente. As verificações on-line confirmam a continuidade entre os pontos de verificação; a verificação off-line compara cada ponto de verificação retido com a exportação. Cabeças legadas sem provas de continuidade mantêm a comparação off-line e são relatadas sem a verificação de continuidade on-line. O relatório lista o tempo de inatividade da testemunha e as publicações com falha por intervalo.

### Selos diários e calendários de carimbos de data/hora indisponíveis

A testemunha sela o limite do diário do dia anterior (UTC) e envia o hash desse selo assinado para o OpenTimestamps. Um envio ao calendário é uma evidência pendente; apenas compromissos de Bitcoin verificados de forma independente recebem confirmação no verificador.

Se todos os calendários falharem, o selo assinado e a tentativa malsucedida permanecem no diário. A rotina de manutenção horária repete a tentativa desse registro original, inclusive após uma reinicialização ou uma mudança de data. Ele verifica no máximo 32 selos, envia no máximo duas submissões ausentes e gasta no máximo 60 segundos em novas tentativas por passagem. Um cursor persistente alterna entre os selos mais antigos. As submissões retidas seguem o caminho de atualização de prova existente.

Uma nova tentativa não reescreve o selo, não altera sua data original nem afirma que o calendário o recebeu anteriormente. Um compromisso posterior do Bitcoin continua sendo uma confirmação externa posterior. Provas ausentes permanecem como `none`; provas pendentes permanecem como `pending` até que o verificador as verifique de forma independente.
