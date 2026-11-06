# Instalar, verificar e atualizar

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/installation/

Instale com um único comando, verifique assinaturas e hashes, atualize e remova uma instalação.

[Projeto](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Introdução rápida](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/) · [Implantação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)

## Instale com um único comando

O instalador guiado inclui um ambiente de execução Python privado. Use o mesmo endereço para instalações futuras: cada publicação atualiza o instalador, os hashes, as assinaturas e as informações de compilação em conjunto.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Em um servidor Ubuntu, execute como root para instalar um serviço em segundo plano. Em um computador desktop, execute como seu usuário normal.

**Windows (PowerShell ou Prompt de Comando):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Não é necessário nenhum administrador no Windows. O processo filho do PowerShell mantém seu terminal aberto com o resultado. O Python e as dependências permanecem na instalação.

No Ubuntu, escolha **“Este computador**”, **“Link HTTPS temporário”** ou **“Domínio próprio**”. O instalador exibe o endereço do painel e a chave de acesso. Para obter um link temporário, abra esse endereço HTTPS no seu navegador e insira a chave. Com acesso local em um servidor remoto, use um encaminhamento SSH a partir do seu computador (`ssh -L 8787:127.0.0.1:8787 user@server`) e abra `http://127.0.0.1:8787`. No macOS e no Windows, o painel local abre no seu navegador; mantenha o terminal em execução.

Faça login no Telegram no painel e escolha o que coletar. A instalação por si só não inicia a coleta do Telegram.

## Onde tudo funciona

`get.destroy.tools` É um **Cloudflare Worker que fornece downloads estáticos**. Não possui o painel TgWitness, nem sessão do Telegram, nem banco de dados de evidências do usuário. Não é roteado para um VPS do projeto. O aplicativo é executado na máquina em que você executa o comando.

| Instalação | Programa | Dados |
| --- | --- | --- |
| Ubuntu como root | `/opt/tgwitness` | Serviço do sistema: `/var/lib/tgwitness-<installation ID>`; use `tgwitness paths` para o caminho exato. |
| Usuário de Linux / macOS | `~/.local/share/tgwitness` | `data/live` nessa instalação. |
| Usuário do Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` nessa instalação. |

Defina `TGWITNESS_INSTALL_DIR` para escolher outra pasta. As versões instaladas e os dados são separados. O instalador não envia suas contas, mensagens ou chaves para o site de download. Ao escolher um túnel do Cloudflare, o tráfego do painel passa pelo Cloudflare; ao usar seu próprio domínio, o tráfego é direcionado para o seu próprio servidor.

Cada instalação inclui os arquivos **START-HERE.html** e **START-HERE.txt**, com caminhos locais, comandos e links para o repositório. Execute `tgwitness guide` para abrir o guia. No Windows, use `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` no PowerShell.

## Configurações de pesquisa de texto completo

[A pesquisa de texto completo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/search/) (visualização) não requer configuração. Seu índice é criado em segundo plano após uma atualização.

| Variável ou comando | Efeito |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Padrão: o índice é mantido em `search/fulltext.sqlite3` de cada espaço de trabalho |
| `TGWITNESS_FULLTEXT=memory` | Não há arquivo de índice; o índice é reconstruído a cada inicialização |
| `TGWITNESS_FULLTEXT=off` | Sem índice; apenas pesquisa por texto exato |
| `tgwitness index status` | Indexar o estado de cada espaço de trabalho |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Recriar todos os índices a partir do diário assinado |

A escolha do administrador em **Diário → Filtros → Índice de pesquisa** substitui a variável para aquele espaço de trabalho. Os comandos localizam o diretório de dados da instalação que os executa; em outros casos, adicione `--data-dir` o caminho de `tgwitness paths`. Para obter um dicionário completo de ucraniano (dados GPL-3.0), instale `pymorphy3-dicts-uk` no ambiente Python da instalação.

## Acesso por linha de comando

A [linha de](https://phishdestroy.github.io/TgWitness/pt/docs/reference/cli/) [comando](https://phishdestroy.github.io/TgWitness/pt/docs/reference/cli/) (pré-visualização) lê o arquivo em busca de scripts e agentes.

| Variável | Efeito |
| --- | --- |
| `TGWITNESS_URL` | Endereço do painel para `tgwitness search`, `context`, `messages`, `stats` e `export`; padrão `http://127.0.0.1:8787` quando um token estiver definido |
| `TGWITNESS_MCP_TOKEN` | Arquive o token de conexão em **Integrações → MCP**, compartilhado com os clientes do MCP; `--token-file` em vez disso, lê-o de um arquivo |
| `TGWITNESS_DATA` | O diretório de dados é lido diretamente quando nenhum `--data-dir`, URL ou token for fornecido |

## Verifique antes de executar

O comando de uma linha confia no HTTPS para seu script inicial. Esse script verifica SHA-256 e a assinatura RSA do projeto no aplicativo e nas restrições antes da instalação. Você também pode baixar e verificar o script inicial primeiro.

A chave de lançamento pública é [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Seu SHA-256 é:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Guarde essa impressão digital de uma revisão do repositório em que você confia. Uma soma de verificação proveniente do mesmo servidor de download detecta uma incompatibilidade; a chave pública, cuja confiabilidade é verificada de forma independente, é o que autentica a assinatura de uma versão.

Use um diretório novo e vazio para os downloads de verificação abaixo.

**Linux / macOS — execute em um diretório de downloads novo e vazio** (requer curl e OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

A `&&` cadeia é interrompida antes da execução se um download, uma verificação de impressão digital da chave ou de assinatura falhar. Se houver uma publicação entre o download do script e sua assinatura, baixe ambos novamente. Instaladores antigos mantêm suas URLs de pacotes imutáveis.

**Windows — verifique a imagem SHA-256 antes de executar:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Compare o hash com a `install.ps1` linha. Para uma verificação independente da assinatura, use o OpenSSL (por exemplo, no Git Bash) e a mesma impressão digital da chave pública acima:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

A própria instalação no Windows verifica as assinaturas dos pacotes com o .NET e não requer o OpenSSL. Trata-se de assinaturas RSA-3072 independentes / SHA-256, e não de Authenticode. O [manifesto](https://get.destroy.tools/manifest.json) registra a versão do software, o commit exato do Git, o ID de lançamento imutável e o SHA-256 de cada artefato. A página contém um link para a fonte correspondente. O manifesto e a lista de checksums também possuem assinaturas independentes (`manifest.json.sig` e `SHA256SUMS.txt.sig`).

## Atualizar uma instalação existente

**Uma nova publicação atualiza o site de download; os programas instalados são atualizados quando você executa o instalador novamente.** Não há atualizador automático nem reinício automático de uma coleção em execução. O canal atual do instalador é **o “preview”**; ele segue versões publicadas e verificadas de `main`, cujo commit pode ser mais recente do que a última versão numerada do GitHub. A versão da página provém de `pyproject.toml`; seu commit e o ID da compilação distinguem as atualizações dentro da mesma versão de pré-visualização.

Use a mesma pasta de instalação e o mesmo usuário do sistema operacional de antes. Faça backup do diretório de dados completo com a coleta interrompida; `tgwitness paths` identifica-o. Uma exportação assinada não é um backup completo da instalação.

**Instalação como root no Ubuntu em `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Após uma instalação bem-sucedida:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Para a instalação em Linux/macOS, use a configuração original `TGWITNESS_INSTALL_DIR` ou as configurações padrão e execute o primeiro comando de instalação novamente. Feche um painel em primeiro plano antes da atualização e reinicie-o depois. Para um serviço configurado no Linux, execute o comando `tgwitness restart` comando.

**Windows:** feche o painel em execução, execute o comando de instalação do Windows novamente e, em seguida, abra `bin\tgwitness.cmd` na mesma instalação. O instalador mantém os dados, sessões, configurações de acesso e chaves de assinatura. Ele alterna o iniciador somente após o novo ambiente passar nas verificações; uma instalação com falha mantém o iniciador anterior em vigor. Guarde o backup pré-atualização para alterações no formato de armazenamento.

## Comandos de uso diário no Ubuntu

| Comando | Resultado |
| --- | --- |
| `tgwitness open` | URL atual do painel e chave de acesso. |
| `tgwitness paths` | Caminhos exatos dos programas, dados e guias. |
| `tgwitness guide --print` | Instruções de operação offline. |
| `tgwitness status` / `tgwitness logs` | Disponibilidade / registros de serviço. |
| `tgwitness stop` / `tgwitness start` | Interromper/retomar o serviço; reter dados. |
| `tgwitness token rotate` | Substitua a chave de administrador e encerre as sessões do navegador. |
| `tgwitness tunnel off` | Desative o túnel rápido público; mantenha o painel local. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Crie um link de túnel rápido / substitua seu endereço. |

Consulte a seção [“Acesso”](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) para obter informações sobre tokens de colegas, sessões e restrições de IP, e a seção [“Publicação do instalador”](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) para conhecer o fluxo de trabalho de lançamento do GitHub para o Cloudflare.

## Remover TgWitness

Não há desinstalador: basta fechar o painel e excluir suas pastas. A exclusão da pasta de dados destrói definitivamente os diários, as chaves de assinatura, as sessões do Telegram e os arquivos salvos. Antes disso:

1. Exporte o que você precisar (**Exportações → Baixar ZIP assinado**) e mantenha a impressão digital da chave de assinatura e os pontos de verificação fora desta máquina. Para manter o próprio espaço de trabalho, copie toda a pasta de dados com a coleta interrompida.
2. Exclua os servidores criados em **Extras → Servidor 24/7** na seção **Seus servidores** ou com `python -m tgwitness.cloud destroy`; o provedor os cobra até que sejam excluídos.
3. Encerre a sessão de cada conta no Telegram em **Configurações → Dispositivos**. A exclusão dos arquivos não encerra a sessão no lado do Telegram.

**Instalação como root no Ubuntu.** Observe a pasta de dados, interrompa o serviço e, em seguida, remova o serviço, as pastas e o atalho:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Instalação para usuários de Linux ou macOS.** Feche o painel. Um serviço de usuário configurado no Linux é interrompido com `systemctl --user disable --now tgwitness-<ID>`; sua unidade está em `~/.config/systemd/user/`. Em seguida, exclua `~/.local/share/tgwitness` (ou o seu `TGWITNESS_INSTALL_DIR`) e o `~/.local/bin/tgwitness` atalho.

**Windows.** Feche o painel e exclua `%LOCALAPPDATA%\TgWitness` (ou o seu `TGWITNESS_INSTALL_DIR`). O instalador não adiciona nenhum serviço, tarefa agendada ou atalho.
