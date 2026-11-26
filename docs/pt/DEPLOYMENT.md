[TgWitness](../../README.md) / [Documentação](../README.md) / [Pasta](README.md)

![Implantação e recuperação](../assets/presentation/chapter-operate.svg)

[English](../DEPLOYMENT.md) · [Русский](../ru/DEPLOYMENT.md) · [Українська](../uk/DEPLOYMENT.md) · [Español](../es/DEPLOYMENT.md) · **Português (Brasil)** · [Türkçe](../tr/DEPLOYMENT.md) · [العربية](../ar/DEPLOYMENT.md) · [فارسی](../fa/DEPLOYMENT.md) · [اردو](../ur/DEPLOYMENT.md) · [हिन्दी](../hi/DEPLOYMENT.md) · [Bahasa Indonesia](../id/DEPLOYMENT.md) · [Tiếng Việt](../vi/DEPLOYMENT.md) · [简体中文](../zh/DEPLOYMENT.md)

# Implantação e operação

## Escolher uma instalação

Para o pacote portátil, extraia `TgWitness-<version>-windows-amd64-portable.zip` do
GitHub Releases. Para os demais métodos, baixe e extraia o arquivo ZIP com o código-fonte ou clone o
repositório e, em seguida, execute o seguinte a partir do diretório do projeto:

| Instalação | Início | Funciona em segundo plano? |
| --- | --- | --- |
| Pacote portátil do Windows | `TgWitness.cmd` | Não; mantenha a janela aberta. |
| Nativo do Windows | `Start.cmd` | Não; utilize a tarefa de logon opcional para execução em segundo plano. |
| Nativo para Linux/macOS | `sh start.sh` | Não; utilize o systemd/launchd para execução em segundo plano. |
| Docker em qualquer host compatível | `docker compose up -d --build --wait` | Sim, enquanto o daemon do Docker estiver em execução. |
| Utilitário do Docker no Windows | `scripts\Docker.cmd` | Sim; o helper aguarda a verificação do estado do servidor web. |
| Utilitário do Docker no Linux/macOS | `sh scripts/docker-start.sh` | Sim; o helper aguarda a verificação do estado do servidor web. |

Para um servidor em nuvem que um terceiro deva poder verificar — criado por meio da
API do provedor, sem SSH, acessível apenas por meio de um Cloudflare Tunnel — consulte
[implantação de alta segurança](../HIGH-ASSURANCE.md).

A inicialização nativa cria uma imagem privada `.venv` e instala as dependências fixadas.
O Docker as compila dentro da imagem, sem a necessidade do Python do host. A configuração inicial
requer acesso à Internet. Quando não é encontrado nenhum Python 3.11 ou superior, `Start.cmd` solicita autorização antes de
instalar o Python 3.12 para o usuário atual do Windows (winget; caso contrário, o instalador do python.org,
após verificar sua assinatura da Python Software Foundation); ele nunca solicita
privilégios de administrador. O Docker e os serviços do sistema operacional continuam sendo pré-requisitos.

As instalações nativas e portáteis utilizam `data/live` dentro de sua pasta. O Docker utiliza o volume denominado `tgwitness-data`
em `/data`. Trata-se de instalações separadas até que você migre deliberadamente o
diretório de dados completo. Não espere que um novo contêiner do Docker identifique as contas nativas
automaticamente.

## Requisitos de instalação

A instalação nativa requer o Python 3.11 ou versão posterior, juntamente com `venv` e `ensurepip`, acesso à Internet
para a instalação da primeira dependência e um diretório de projeto com permissão de gravação para
`.venv`. O painel incluído no pacote não requer o Node.js nem a compilação do front-end. Execute o iniciador a partir de
sua conta normal no sistema operacional; o TgWitness não exige privilégios de administrador/root.

- **Windows:** `Start.cmd` verifica `py -3`, depois `python`, em seguida as pastas padrão de instalação por usuário e
  “Program Files”, e requer a versão 3.11 ou posterior. Se nenhuma opção funcionar, ele
  oferece a instalação automática por usuário descrita acima. `py -3 start.py` também funciona.
  O pacote portátil não requer Python algum.
- **Linux:** `start.sh` verifica `python3.13`, `python3.12`, `python3.11`, `python3` e
  `python` e exibe o comando de instalação para apt, dnf, pacman, zypper, apk ou Homebrew
  quando nenhuma opção for adequada. As instalações no Debian/Ubuntu podem exigir o pacote
  `python3-venv` correspondente ao interpretador selecionado. O Python padrão mais antigo
  de uma distribuição deve ser substituído ou complementado pelo Python 3.11+.
- **macOS:** instale uma distribuição atual do Python 3.11+; não presuma que um interpretador fornecido pelo sistema operacional
  atenda aos requisitos. Utilize `python3 start.py` a partir do diretório do projeto.
- **Docker:** utilize o Docker Engine/Desktop com o Compose v2.20 ou mais recente. O Docker Desktop
  deve utilizar contêineres Linux no Windows. O contêiner instala suas
  próprias dependências do Python; o host não necessita de uma instalação separada do Python.

## Computador local

Utilize `Start.cmd` no Windows ou `sh start.sh` no Linux/macOS. `scripts\Setup.cmd` ou
`sh start.sh --setup-only` preparam
o ambiente. O executável instala as dependências na primeira utilização; as execuções posteriores
reutilizam o ambiente. É necessário acesso à Internet para a configuração e para a coleta de dados do Telegram,
mas a visualização de registros existentes e a criação de exportações funcionam offline.

Execute `python start.py --check` após a configuração para verificar as dependências locais, o Ed25519,
o armazenamento, a configuração da chave e o endereço de escuta sem iniciar um coletor.
Utilize `--json` para obter uma saída estruturada. Passe os parâmetros pretendidos `--data-dir`, `--host` e
`--port`. A verificação não instala pacotes, não cria um diário nem se conecta ao Telegram;
não se trata de uma qualificação de integridade ou cobertura. A inicialização verifica separadamente
os diários existentes. `python start.py --help` também evita a instalação.

Após executar o start.py, execute os comandos auxiliares com `.venv\Scripts\python.exe` no
Windows ou `.venv/bin/python` no Linux/macOS, ou ative primeiro esse ambiente.
Os exemplos `python -m ...` a seguir pressupõem que o ambiente esteja ativo.

~~~sh
python -m tgwitness --data-dir /caminho/para/dados/privados --host 127.0.0.1 --port 8787
~~~

Variáveis de ambiente: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN.
TGWITNESS_VAULT_KEY_FILE seleciona o modo de chave externa para uma nova instalação; consulte [Chave mestra externa](../SECURITY-MODEL.md#external-master-key).
TGWITNESS_TOKEN, se fornecido, deve conter pelo menos 24 caracteres; utilize um valor aleatório
criptograficamente seguro. Na ausência desse valor, o aplicativo gera um token aleatório de 256 bits no arquivo panel-token.txt.
A substituição de variáveis de ambiente não reescreve esse arquivo. Reinicie o sistema para alternar as credenciais.

Exatamente um processo pode ser o proprietário de um diretório de dados. Um bloqueio de arquivo do sistema operacional multiplataforma impede
gravações simultâneas acidentais. Utilize um único worker do Uvicorn. O painel pode gerenciar qualquer número de
espaços de trabalho, com diretórios adicionais de espaços de trabalho em profiles/<id>/.
Para instâncias de serviço separadas, utilize diretórios e portas distintos. Os arquivos WAL do SQLite devem ser armazenados em um
armazenamento local persistente, e não em um sistema de arquivos de rede. Não compartilhe um único volume entre réplicas.

## Pacote portátil para Windows

Cada versão do GitHub inclui `TgWitness-<version>-windows-amd64-portable.zip` e seu
`.sha256`. Ela contém o ambiente de execução oficial e incorporável do Python 3.12, proveniente do site python.org
(soma de verificação fixada em `tools/build_portable.py`), o TgWitness e suas dependências fixadas,
e três executáveis:

| Arquivo | Objetivo |
| --- | --- |
| `TgWitness.cmd` | Inicie o painel; as opções adicionais são repassadas, por exemplo, `TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | Inicie a demonstração sintética em `data\demo` |
| `TgWitness-Check.cmd` | Execute a verificação de prontidão sem iniciar |

O dicionário de morfologia russo fixado e os perfis de cor em PDF estão incluídos no pacote para
uso offline. A compilação permite apenas os caminhos de arquivo conhecidos dentro dos diretórios de dependências
`data`; arquivos inesperados nesses diretórios causam falha na compilação.

Extraia todo o arquivo compactado para uma pasta gravável, como `Documents\TgWitness`; não o execute
de dentro do ZIP nem da pasta “Arquivos de Programas”. O ambiente de execução utiliza um caminho de módulos isolado,
portanto, outras instalações do Python e `PYTHONPATH` não o afetam. Os dados permanecem na
pasta `data` do pacote. Para atualizar, encerre o TgWitness, extraia a nova versão para uma nova
pasta e copie a pasta `data` para lá.

Compile você mesmo no Windows de 64 bits com o Python 3.12:

~~~sh
python tools/build_portable.py
~~~

## Contêiner

```sh
docker compose up -d --build --wait
```

Isso cria um volume persistente nomeado para /data.
A porta da web é mapeada para 127.0.0.1:8787. O processo é executado com o UID 10001, com
capacidades restritas, um sistema de arquivos raiz somente leitura e os diretórios /data e /tmp graváveis.
`--wait` verifica a integridade do servidor web antes de retornar; a autorização e a
entrega do Telegram aparecem no painel. Os auxiliares fornecidos utilizam um tempo limite de prontidão de 180 segundos
após a compilação. Os downloads iniciais de dependências podem demorar mais do que isso.

Ambos os arquivos Compose básicos utilizam o nome do projeto `tgwitness`; portanto, a extração de uma nova versão
para outro diretório não seleciona automaticamente um novo volume de dados. Mantenha apenas uma
implantação ativa para esse projeto. Para instalações independentes, utilize um
`docker compose -p NAME ...` exclusivo e uma porta de host diferente, e mantenha ambos nas atualizações.
Para uma implantação mais antiga que utilize um nome de projeto diferente, continue usando seu nome original
com `-p`; `docker compose ls` lista os projetos existentes.

Copie `deploy/env.example` para `.env` e altere `TGWITNESS_PORT` para utilizar uma porta de loopback
diferente. Por exemplo, `TGWITNESS_PORT=8788` expõe o painel em
`http://127.0.0.1:8788`; o contêiner continua escutando na porta 8787. `.env` é ignorado pelo Git.

Recuperar o token inicial:

~~~sh
docker compose exec tgwitness cat /data/panel-token.txt
~~~

Comandos úteis:

```sh
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` reinicia o coletor após uma falha ou reinicialização do daemon do Docker.
Em um servidor Linux, habilite o Docker na inicialização usando o gerenciador de serviços
da sua distribuição, geralmente `sudo systemctl enable --now docker`. No Windows/macOS, habilite
a configuração “iniciar ao fazer login” do Docker Desktop. O logout do desktop, o modo de suspensão ou um
pode interromper a coleta. Um contêiner explicitamente parado permanece
parado até que você o inicie novamente.

O volume /tmp está limitado a 512 MiB na configuração de exemplo. A construção da exportação
utiliza, em vez disso, o `temporary-exports/` de cada espaço de trabalho no diretório persistente /data. Reserve espaço
nesse local para exportações simultâneas, crescimento do diário/WAL, mídia e backups.
O lançador utiliza o arquivo deploy/constraints.txt para fixar versões qualificadas de dependências de tempo de execução.
O Docker e os servidores de alta segurança são instalados a partir de deploy/requirements.lock e
deploy/build.lock com o comando pip --require-hashes: cada arquivo de pacote deve corresponder a um SHA-256
registrado no commit; assim, um arquivo substituído no PyPI ou em um espelho é rejeitado. Pacotes que
fornecem apenas o código-fonte (jieba, pyaes) são compilados com as ferramentas de configuração fixadas no arquivo deploy/build.lock
(`--no-build-isolation`) pelo iniciador, pelo compilador portátil do Windows e pelo Dockerfile,
de modo que o pip não resolve um ambiente de compilação separado e não fixado. A imagem base do Python
e os pacotes do sistema operacional ainda exigem qualificação de lançamento independente.

Não utilize o comando `docker compose down -v`, a menos que pretenda destruir o diário e as chaves.
O relatório de integridade do contêiner informa a disponibilidade do servidor web, e não se refere à captura bem-sucedida do Telegram.
Verifique o estado do coletor do painel, o sinal de vida, os erros e os eventos de cobertura.

### Perfil de testemunha independente

O serviço opcional `witness` executa uma [testemunha independente](../WITNESS.md) em seu próprio
contêiner, com sua própria chave e diário no volume `witness-data` e apenas um token de testemunha somente para leitura
para o coletor. Crie o token no painel em **Mais ferramentas → Extras → Testemunha independente**, adicione-o
com um token de bot e um canal para `.env` e, em seguida, inicie o perfil:

```sh
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

O serviço acessa o coletor dentro da rede Compose em `http://tgwitness:8787`
(`TGWITNESS_WITNESS_COLLECTOR`
o substitui; por exemplo, `/profiles/<workspace ID>`
para
outro espaço de trabalho). Para uma testemunha em um servidor separado, administrado por outra pessoa, utilize
`deploy/compose/compose.witness.yaml`
nesse servidor, com `TGWITNESS_WITNESS_COLLECTOR`
definido como o endereço HTTPS
do coletor; esse arquivo contém apenas a testemunha.

## Instalar uma imagem publicada

Copie `deploy/env.example` para `.env`. Defina `TGWITNESS_IMAGE` como a versão publicada, utilizando
o caminho do repositório em **letras minúsculas**, por exemplo:

```dotenv
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:1.0.2
TGWITNESS_PORT=8787
```

Execute este arquivo sozinho, em vez de `compose.yaml`:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Não é necessário ter código-fonte, Python ou compilador no host. O fluxo de trabalho de lançamento
é voltado para contêineres Linux AMD64 e ARM64, incluindo a VM Linux do Docker Desktop.
Utilize uma tag de versão ou `ghcr.io/owner/repository@sha256:...` a partir do resumo do fluxo de trabalho.
Não há configuração de tag móvel `latest` nem de atualização autônoma de aplicativos. As
variantes de imagem e de código-fonte utilizam o mesmo volume de dados quando o nome do projeto coincide.

## HTTPS automático em um servidor

Utilize um servidor com o Docker, um domínio sob seu controle e armazenamento local persistente.
Direcione os registros A/AAAA do domínio para o servidor; publique o registro AAAA somente se o IPv6 chegar
até ele. Permita o tráfego de entrada nas portas TCP 80 e 443 e o tráfego de saída de DNS/HTTPS para emissão de certificados.
Outros serviços não devem já estar utilizando essas portas.

Copie `deploy/env.example` para `.env` e defina um nome de host, sem esquema nem caminho:

```dotenv
TGWITNESS_DOMAIN=watch.your-domain.org
```

Inicie a compilação do código-fonte com a sobreposição HTTPS:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

Para uma imagem publicada, utilize `deploy/compose/compose.image.yaml` como primeiro arquivo. Mantenha
ambos os argumentos `-f` para comandos posteriores de status, logs, atualização e parada.

O Caddy obtém e renova um certificado, redireciona HTTP para HTTPS e encaminha
as solicitações para o coletor na rede privada do Compose. O estado do certificado possui
seu próprio volume persistente. A porta direta do host do coletor permanece restrita ao loopback.
A configuração fornecida do Caddy não habilita o registro de acesso.

Abra `https://watch.your-domain.org` e insira o token do painel. A verificação de prontidão
abrange os contêineres; a emissão de certificados e a acessibilidade externa dependem do DNS
e do firewall. Se o HTTPS não estiver pronto, verifique o DNS, as regras do firewall e:

```sh
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

A imagem do Caddy fornecida vem logo após a tag `2-alpine`. Ao executar o comando “pull”, essa imagem é atualizada;
fixe um resumo testado em sua implantação caso necessite de versões fixas da infraestrutura.

## Atualizações e backups

Preserve o nome do projeto Compose e o volume de dados ao longo das atualizações. Primeiro, interrompa o
coletor e faça um backup completo. Para a implantação padrão baseada na fonte:

```sh
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Utilize um novo destino de backup a cada vez, fora do repositório, e proteja-o como
material de acesso à conta. O caminho de exemplo é meramente ilustrativo; utilize seu próprio local privado
de backup. Copie o diretório inteiro, incluindo arquivos ocultos, todas as áreas de trabalho, chaves,
diários e mídias. Faça o backup da chave mestra do cofre externo separadamente, caso esteja configurada.
Um arquivo ZIP de evidências não é um backup de aplicativo restaurável. Para HTTPS, preserve também
os volumes do Caddy caso precise manter o estado do certificado/conta.

Para uma implantação a partir do código-fonte, obtenha os arquivos da nova versão e execute:

```sh
docker compose up -d --build --wait
```

Para a implantação de uma imagem, altere `TGWITNESS_IMAGE` para a versão desejada e, em seguida, execute:

```sh
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Utilize também o(s) arquivo(s) Compose da sua instalação para os comandos de parada/cópia acima.
Mantenha `.env`, a configuração personalizada e o mesmo nome do projeto. `down` mantém os
volumes nomeados; **`down -v` os exclui**. Não copie `.venv` entre sistemas operacionais
ou versões do Python. Para atualizações nativas, interrompa o TgWitness, faça backup de todo o seu diretório de dados,
substitua os arquivos de origem e execute `python start.py --setup-only` antes de iniciar o programa.

Verifique o acesso ao painel, a identidade da conta, o estado de observação e a cobertura após uma
atualização. Após a reinicialização, o TgWitness retoma a posição salva da atualização do Telegram e
solicita as atualizações perdidas durante o processo. Uma reversão pode
exigir o backup pré-atualização caso uma versão futura altere os formatos de armazenamento.

## Servidor remoto

Mantenha o serviço vinculado ao loopback e utilize um túnel SSH, ou termine a conexão HTTPS em um
proxy reverso. O arquivo Compose básico é apenas local; a sobreposição opcional
`deploy/compose/compose.https.yaml` fornece o Caddy para um domínio configurado.
Mantenha o token de portador fora das URLs e dos logs do proxy. Um proxy reverso deve limitar
o tamanho das solicitações e as taxas de conexão. Não exponha o HTTP simples à Internet.

São fornecidos exemplos para o systemd, uma tarefa de logon do Windows, um agente de usuário do macOS e o Caddy
em [deploy/](../../deploy/README.md). Verifique e adapte seus caminhos antes da instalação.
Trata-se de modelos fornecidos, e não de configurações específicas da plataforma executadas localmente. Nenhum
serviço ou tarefa em segundo plano é registrado pelo iniciador padrão.

No Windows, uma execução sem janela `pythonw.exe` armazena os diagnósticos de inicialização/servidor em
`logs/server.log`, no diretório de dados (5 MiB por arquivo, dois backups alternados).
As execuções no console mantêm os registros do console. O registro de acesso HTTP está desativado em ambos os
modos. Proteja os registros junto com o diretório de dados e analise-os antes de compartilhá-los.

## Reinício e lacunas

O último estado de observação solicitado é armazenado. Se a observação estava ativa,
o sistema tenta, na inicialização, se reconectar e retomar as fontes selecionadas. A pausa manual cancela
essa intenção. Uma tentativa de reinício malsucedida é registrada e exibida no painel.

O TgWitness armazena a posição de atualização do Telegram para a conta e para cada canal
(pts, qts, seq e data) no cofre do espaço de trabalho e a restaura na próxima inicialização.
O cliente, então, solicita as atualizações perdidas enquanto o processo estava interrompido, e a
reverificação periódica recupera as mensagens perdidas e registra aquelas salvas que o Telegram já
não retorna. As conversas são recarregadas na inicialização. A cada inicialização, é registrado o
cabeçalho do diário anterior, o limite de conexão offline e a posição de atualização a partir da qual a operação foi retomada.
O monitor verifica a conectividade a cada 10 segundos e adiciona um sinal de vida a cada minuto
(**Mais ferramentas → Parâmetros → Registrar atividade a cada**).
Desconexões e períodos de silêncio são registrados como lacunas de cobertura, juntamente com o motivo.
Instantâneos do histórico são armazenados como observações separadas do histórico atual ao lado dos registros em tempo real.

A fila de mídia é armazenada no banco de dados SQLite de cada espaço de trabalho. Uma mensagem e sua tarefa
são confirmadas de forma atômica. As tarefas em execução que forem interrompidas são recuperadas para uma nova tentativa na inicialização.
Cada download possui um tempo limite básico de 120 segundos, acrescido do tempo necessário para transferir seu tamanho a uma taxa de 256 KiB/s, e um
limite de 1 a 2.000 MiB por tipo de anexo; o tempo limite, a velocidade e as tentativas de repetição estão em **Mais ferramentas → Parâmetros**. O coletor
ignora arquivos cujo tamanho é desconhecido. A pausa mantém o trabalho na fila. A repetição utiliza o
descritor de arquivo original observado, nunca a versão mais recente de uma mensagem editada posteriormente.
Falhas temporárias têm um número limitado de repetições; as pausas do FloodWait de mídia sobrevivem à reinicialização.
A recuperação de mídia é independente da recuperação de atualizações do Telegram e não pode recriar arquivos que tenham desaparecido.

## Backup, restauração e capacidade

`tgwitness backup FOLDER`
copia o diretório de dados enquanto o painel continua em execução:
primeiro os pontos de verificação, depois os arquivos SQLite por meio da API de backup online, em seguida as chaves, mídias e
perfis, de modo que nenhum ponto de verificação copiado seja mais recente do que o diário copiado. `backup-manifest.json`
lista o SHA-256 de cada arquivo e os cabeçalhos do diário. Para restaurar, interrompa o TgWitness e substitua
todo o diretório de dados por essa pasta. Na próxima inicialização, é registrado que o diário foi restaurado
a partir de uma cópia mais antiga. Esse registro compara o diário com o cabeçalho mantido em
`TGWITNESS_STATE_DIR`
, uma pasta fora do diretório de dados: o volume `tgwitness-state`
no
Compose, `/var/lib/tgwitness-state`
nas unidades do systemd e na pasta de estado local do usuário
nos demais casos. Sem uma pasta de estado gravável, a restauração não é detectada e o log indica isso uma vez.

Sem o comando, interrompa o processo antes de copiar o **diretório de dados inteiro**, incluindo vault.key,
signing.enc, credentials.enc, arquivos do banco de dados SQLite e WAL, mídia, token, pontos de verificação,
e todos os subdiretórios de “profiles/”. Restaure
a cópia completa enquanto o serviço de destino estiver parado. A falta de chaves do cofre ou
a incompatibilidade de chaves de assinatura causam falha na inicialização; não gere novas chaves para forçar o acesso.

Mantenha os backups secretos criptografados e com acesso controlado. Os arquivos ZIP de evidências são artefatos de revisão portáteis,
não backups de aplicativos nem de sessões do Telegram.
Não há exclusão automática por retenção. Planeje o espaço em disco para todas as mensagens, metadados brutos,
arquivos de mídia, exportações temporárias e backups.

Verificação de inicialização e exportação de registros de fluxo, em vez de carregar o diário inteiro.
Uma exportação fixa um instantâneo de leitura, enquanto novas gravações no WAL podem continuar; exportações de longa duração
podem reter páginas do WAL, portanto, a capacidade do disco ainda é importante. Os arquivos ZIP têm limite máximo de 4 GiB
descompactados, para corresponder à configuração padrão do verificador independente; **Mais ferramentas → Parâmetros → Maior ZIP assinado**
aumenta esse limite, e tais arquivos são verificados com `verify.py --max-gib N`. Outros formatos não têm limite de contagem de eventos.
Os navegadores compatíveis transmitem blocos de resposta para um arquivo selecionado pelo usuário. Outros navegadores
armazenam em buffer no máximo 128 MiB e direcionam transferências maiores para a CLI autenticada:

~~~sh
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
~~~

Utilize `--profile ID`, obtido em **Exportações → ID da área de trabalho**, para outra área de trabalho,
`--format zip|jsonl|csv|html`, `--url https://your-server` para um servidor remoto ou
`--max-mib` para alterar o limite de transferência de 5 GiB. O HTTP simples é permitido apenas para
loopback. Os tokens são transmitidos nos cabeçalhos, redirecionamentos são recusados, arquivos existentes
não são sobrescritos e downloads incompletos não são publicados como arquivos concluídos.
Caso TGWITNESS_TOKEN substitua o token gerado, utilize um arquivo protegido separadamente
contendo esse valor ativo: o arquivo panel-token.txt não é reescrito pela substituição.
O SHA-256 do comando é apenas uma soma de verificação da transferência; verifique independentemente o ZIP assinado.

O painel exibe mídias em fila/com falha, as mídias pendentes mais antigas, espaço livre em disco, pausas em solicitações do Telegram
e fontes cujo acesso não foi confirmado. Esses diagnósticos não constituem
um monitor completo de entrega de ponta a ponta. Os espaços de trabalho compartilham um processo; uma conta com atividade excessiva pode
ainda assim afetar os demais. Processos de trabalho separados, retenção/rotação, recuperação de atualizações duráveis
e qualificação completa da implantação permanecem. O acesso restrito ao painel está documentado
em [acesso e permissões](../ACCESS.md); pontos de verificação independentes são abordados no
[guia de testemunhas](../WITNESS.md).

Procedimentos detalhados: [conexão/segurança](../CONNECTION-SECURITY.md) e
[modos de operação](../OPERATIONS.md).
