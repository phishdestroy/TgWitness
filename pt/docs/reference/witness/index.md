# Testemunha independente

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/

Execute uma instância do TgWitness com sua própria chave e bot, publique pontos de verificação assinados em um canal e compare as exportações com esses pontos.

[Configuração do bot e do proxy em russo](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Um coletor assina seu próprio diário; portanto, quem quer que controle o coletor e sua chave poderia, em princípio, reescrever ou truncar o diário e assiná-lo novamente. Uma testemunha torna isso detectável. Trata-se de um processo separado — outro contêiner, ou melhor, um servidor operado por outra pessoa — que, a cada poucos minutos, busca o cabeçalho do diário assinado do coletor, assina o que observou com sua própria chave, mantém isso em seu próprio diário e o publica em um canal do Telegram.

Diagrama de fluxo · Coletor → Witness (ponto de verificação assinado: contagem de registros + hash do cabeçalho); Witness → Diário de evidências, chave própria; Witness → Canal do Telegram (postagem assinada por meio de seu próprio bot); Arquivo ZIP de evidências → verify.py; Diário de evidências, chave própria → verify.py; Canal do Telegram → verify.py (Exportação do Telegram Desktop ou página “t.me/s”) · Coletor · Witness · Diário de evidências,chave própria · Canal do Telegram · Arquivo ZIP de evidências · verify.py · ponto de verificação · assinado: contagem de · registros + hash do · cabeçalho · postagem assinada por meio · de seu próprio bot · Exportação do Telegram · Desktop ou página “t.me/s”

**Diagrama em formato de texto**

1. Coletor → Witness (ponto de verificação assinado: contagem de registros + hash do cabeçalho)
2. Witness → Diário de evidências, chave própria
3. Witness → Canal do Telegram (postagem assinada por meio de seu próprio bot)
4. Arquivo ZIP de evidências → verify.py
5. Diário de evidências, chave própria → verify.py
6. Canal do Telegram → verify.py (Exportação do Telegram Desktop ou página “t.me/s”)

## O que o TgWitness oferece e o que ele não oferece

| A testemunha possui | A testemunha nunca tem |
| --- | --- |
| Um **token de testemunho** somente leitura para um espaço de trabalho | As credenciais de sessão do Telegram ou da API do coletor |
| Sua própria chave Ed25519 e seu próprio registro | O cofre do coletor, a chave de assinatura ou o token do painel |
| Seu próprio token de bot do Telegram | Conteúdo da mensagem: o cabeçalho contém a contagem de registros e um hash |

O token é criado na página **“Witness”** do painel, exibido uma única vez e armazenado apenas como um SHA-256. Ele abre exatamente um endpoint, `GET /api/witness/head`, que retorna um ponto de verificação recém-assinado, além de contadores de coleta sem conteúdo assinados e informações sobre a integridade operacional. Ele não pode abrir o painel, ler o conteúdo das mensagens ou alterar configurações, e o token do painel não é aceito nesse local. Revogue um token na mesma página. O coletor registra quando uma nova chave de testemunha começa a verificar (`witness.seen`) e mostra a última verificação por token; uma testemunha que não tenha sido verificada em 2,5 intervalos é marcada como vencida.

Novas testemunhas enviam um desafio aleatório em cada enquete; a declaração de captura o repete sob a assinatura do coletor. Os contadores estão vinculados ao ponto de verificação exato e são incluídos nas postagens assinadas das testemunhas. Cabeçalhos legados continuam sendo aceitos pela testemunha autônoma. O aumento do diário, por si só, nunca é contabilizado como uma nova mensagem.

## O que ela verifica e registra

A cada intervalo (10 minutos por padrão), o TgWitness:

1. busca o cabeçalho por conta própria (o coletor não pode inseri-lo nem ignorá-lo);
2. verifica a assinatura do coletor, a chave fixada do coletor (`--collector-fingerprint`, ou a primeira chave encontrada), uma contagem não decrescente e um cabeçalho inalterado com uma contagem inalterada;
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

Abra **Extras → Um bot no seu canal → Configure um bot** no painel. Três etapas abrangem o acesso somente leitura, o seu canal e o intervalo, seguidas do lançamento do witness. A política de publicação, o proxy HTTP/SOCKS5 opcional e o endereço personalizado da API do bot encontram-se nas **configurações avançadas** . O formulário baixa o `witness.json` com a chave do coletor deste espaço de trabalho fixada. Baixe o token de somente leitura recém-criado com **“Salvar arquivo de acesso** como `witness-token.txt` ”; coloque-o e um `bot-token.txt` criado no host da testemunha ao lado desse JSON. O coletor nunca recebe o token do bot. O download não inicia um serviço nem publica uma mensagem. Nenhuma testemunha de projeto hospedado é implicitamente cadastrada.

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

O endereço do coletor, os tokens e o canal provêm de `--collector`, `--token` ou `--token-file`, `--bot-token` ou `--bot-token-file` e `--channel`, ou `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` e `_CHANNEL`, o que mantém os segredos fora da lista de processos.

Um arquivo de configuração utiliza nomes de opções com sublinhados, além de “`texts`”, que substitui as palavras das publicações do canal:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

Chaves `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. A linha de comando tem prioridade sobre o ambiente, e o ambiente sobre o arquivo. Opções desconhecidas ou chaves de texto interrompem o TgWitness com uma mensagem, em vez de serem ignoradas. A redação nunca afeta a verificação: o verify.py verifica o token assinado ao final de cada publicação. Com `--post changes` ou `problems`, as verificações que não foram publicadas ainda constam no diário de testemunhas e `verify.py` as lista como nunca publicadas; o registro inicial indica a política. Todas as verificações ainda aparecem no diário, portanto, menos publicações significam menos momentos independentes no Telegram, e não menos verificações.

Mesmo sem um canal, o TgWitness continua mantendo seu diário. Guarde a impressão digital da chave do TgWitness (`python -m tgwitness.witness fingerprint`) em outro local.

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

O sinalizador garante a consistência com os registros de testemunho fornecidos e fixados. O operador ainda deve comprovar a independência da testemunha e preservar seus registros separadamente. Ele não atesta a veracidade das mensagens, a coleta completa nem um tempo de execução medido de forma independente.

Uma testemunha mostra o que o coletor relatou naqueles momentos e que as exportações posteriores estão de acordo com isso. Ela não demonstra que o coletor registrou tudo o que o Telegram entregou, nem que o conteúdo das mensagens seja verdadeiro. Uma testemunha executada pelo mesmo operador na mesma máquina é menos confiável do que uma executada por outra pessoa.

O simples aumento no número de registros não é suficiente para comprovar a continuidade de gravação exclusiva online: a comparação offline deve verificar se cada hash de prefixo retido corresponde à exportação completa do coletor. O tempo de inatividade do Witness e falhas na publicação deixam intervalos sem referências externas. Postagens ausentes podem ser relatadas com base em um diário do Witness retido; nem um canal nem um servidor controlado pelo mesmo operador constituem um arquivo imutável de terceiros.
