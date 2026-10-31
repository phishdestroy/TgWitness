# Formatos de contas e sessões

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/

Faça login por telefone, código QR ou chave de autenticação, importe sessões do Telethon, Pyrogram ou Telegram Desktop e gerencie várias contas.

O TgWitness faz login como uma **conta de usuário do Telegram** (não como um bot) via MTProto, utilizando o Telethon. Cada conta ocupa seu próprio **espaço de trabalho** (denominado *“workspace*” na API e nas ferramentas de linha de comando) com sua própria sessão, fontes, registro e chave de assinatura.

Arquivos de sessão, strings de sessão e chaves de autenticação são **autorizações de conta**: quem possuir uma delas poderá agir em nome dessa conta. Eles não contêm histórico de mensagens.

> [!AVISO] **Não utilize nada que o senhor não possa se dar ao luxo de perder.** Recomendamos veementemente que não conecte contas pessoais ou de qualquer outra forma valiosas, nem crie um ID de API / hash de API em uma conta que o senhor valorize. Não se trata de o TgWitness não ter sido testado: o Telegram restringe e bane permanentemente contas de forma imprevisível — para volumes de solicitações que ele considere excessivos, independentemente do cliente ou da finalidade, sem documentação adequada. Muitos banimentos são irreversíveis. Utilize contas dedicadas. O bom andamento dos testes depende do Telegram, não do software, e não garante nada para o futuro.

- [Visão geral](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#at-a-glance)
- [Antes de começar: ID da API e hash da API](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Número de telefone](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#phone-number) · [Código QR](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#qr-code) · [Chave de Autenticação + ID do DC](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#auth-key--dc-id)
- [Arquivos de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#pyrogram-session) · [Par de sessão + JSON](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#telethon-stringsession) · [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json)
- [Identifique o que o senhor possui](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#identify-what-you-have) · [Formatos não suportados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#unsupported-formats)
- [Várias contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#multiple-accounts) · [Mantendo os arquivos de contas em segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#keeping-account-files-safe) · [Solução de problemas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#troubleshooting)

## Visão geral

| O que o senhor tem | Guia em **“Adicionar conta”** | Você também precisará de |
| --- | --- | --- |
| O número de telefone e o acesso aos seus códigos de login | **Telefone** | Senha de autenticação de duas etapas (2FA), caso esteja ativada |
| Telegram aberto em outro dispositivo | **Código QR** | Senha de autenticação de duas etapas (2FA), caso esteja ativada |
| Um arquivo `.session` (Telethon ou Pyrogram) | **Arquivos** | Arquivo JSON complementar opcional para configurações do aplicativo |
| `.session` + `.json` com o mesmo nome | **Arquivos** (selecione ambos) | Normalmente, nada mais |
| Uma pasta “`tdata`” no Telegram Desktop | **Arquivos** (em formato ZIP) | A senha local do Desktop, caso tenha sido definida |
| Uma StringSession do Telethon (texto, `.txt`, `.tgwitness-session`) | **Arquivos** | Não é necessário um par de APIs separado |
| Um `.json` com uma sessão ou chave de autenticação | **Arquivos** | Não é necessário um par de APIs separado |
| Uma chave de autenticação (512 caracteres hexadecimais) e seu número DC | **Chave de autenticação** | ID de usuário opcional |

O TgWitness reconhece os arquivos pelo seu **conteúdo**, e não pelos nomes. Renomear um arquivo nunca o converte.

## Antes de começar: ID da API e hash da API

É possível fazer login sem criar um aplicativo da API do Telegram. Quando nenhum par for inserido, importado ou já estiver salvo no espaço de trabalho, o TgWitness seleciona um par de seu conjunto integrado de 50 pares de API públicos (`tgwitness/api_pool.py`) em ordem aleatória. Se o Telegram recusar um par (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), o próximo será tentado, até um máximo de oito por login; os pares recusados são ignorados até a reinicialização. O par utilizado no login é salvo com a conta e reutilizado para ela. Um **ID de API** e **um hash de API** identificam o aplicativo perante o Telegram; eles não autorizam uma conta por si só.

Para utilizar seu próprio aplicativo (a conta que o registra é a que corre risco; consulte [“Por que um conjunto de APIs integrado?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)”):

1. Acesse [my.telegram.org](https://my.telegram.org) e faça login com qualquer número de telefone de sua propriedade. O código é enviado pelo aplicativo do Telegram, e não por SMS.
2. Escolha **as ferramentas de desenvolvimento de API**.
3. Crie um aplicativo: qualquer título e nome abreviado (5 a 32 letras), plataforma **Desktop**. O URL e a descrição podem ficar em branco.
4. Copie **o api_id do aplicativo** (um número) e **o api_hash do aplicativo** (32 caracteres hexadecimais).

No painel, os campos **“ID da API” e “Hash”** estão localizados abaixo do formulário de login. É possível colar um único par `api_id:api_hash` no campo **“ID da API”** e ambos os campos serão preenchidos. Um único par pode ser utilizado para todas as suas contas. Após um login bem-sucedido, ele é salvo, criptografado, exclusivamente nesse espaço de trabalho e nunca é enviado de volta ao navegador.

Estão envolvidas três credenciais diferentes:

| Secreto | Abrir | Onde está disponível |
| --- | --- | --- |
| Token do painel | O painel web do TgWitness | `panel-token.txt` no diretório de dados, ou `TGWITNESS_TOKEN` |
| ID da API + hash | Nada por si só; identifica o aplicativo | Emparelhamento integrado, configurações importadas ou seu próprio aplicativo em my.telegram.org |
| Autorização de conta | A conta no Telegram | Criado por meio de login por telefone/QR ou importado como uma sessão |

Caso seja necessário acessar o Telegram por meio de um proxy, configure-o primeiro em **Conta → Configurações → Configurações de conexão → Alterar rota de conexão**.

## Número de telefone

1. Abra **a conta**, acesse a guia **“Telefone”** e insira o número no formato internacional, por exemplo, `+44 7700 900123`. Espaços e traços são removidos automaticamente.
2. Clique em **“Continuar**”. Os campos “ID da API” e “Hash” podem permanecer em branco.
3. Insira o código enviado pelo Telegram (geralmente para o aplicativo do Telegram; o envio por SMS não é garantido).
4. Caso a conta possua verificação em duas etapas, digite essa senha. Não se trata do token do painel nem da senha do dispositivo.
5. Verifique o ID da conta exibido após o login e, em seguida, selecione as fontes.

Os códigos de login e a senha de autenticação de duas etapas (2FA) nunca são gravados no disco.

## Código QR

Utilize esta opção quando a conta já estiver conectada em um celular ou em outro computador.

1. Guia **“Código QR”** → **Mostrar código QR**. O campo “ID da API + Hash” pode permanecer em branco.
2. No dispositivo em que está conectado: **Configurações → Dispositivos → Vincular dispositivo de desktop**, escaneie o código e confirme.
3. Insira a senha de autenticação de duas etapas (2FA) no TgWitness caso o Telegram a solicite.

A imagem do QR é gerada localmente. Os códigos expiram; clique em **“Gerar outro código QR”** para tentar novamente. Bloquear o painel, alternar de área de trabalho ou iniciar outro login cancela um código pendente.

## Chave de Autenticação + ID do DC

Uma Chave de Autorização (Auth Key) é a autorização bruta de 256 bytes por trás de cada sessão do Telegram, representada por **512 caracteres hexadecimais**, juntamente com o número do centro de dados **DC 1–5**.

1. Guia **“Chave de autenticação**”. Cole a chave completa; uma chave abreviada que contenha “`…`” não funcionará.
2. Selecione o DC ID fornecido com a chave.
3. Opcionalmente, insira o **ID do usuário**. O TgWitness recusará a conexão caso o Telegram identifique uma conta diferente.
4. **Conta no** Press **Connect**.

Uma chave de autenticação (512 caracteres) não é um hash de API (32 caracteres). A mesma chave também pode ser importada como JSON; consulte [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json).

## Arquivos de contas

Abra **“Adicionar conta” → “Arquivos”** e selecione até **quatro arquivos pertencentes a uma conta**, totalizando **8 MiB**; em seguida, pressione **“Conectar conta**”.

- Os arquivos são convertidos **na memória** do seu servidor TgWitness. Os arquivos enviados não são armazenados, os arquivos ZIP não são extraídos para o disco e nenhum serviço externo é acionado.
- A sessão resultante é então verificada com o Telegram. Se um arquivo indicar um ID de usuário, ele deverá corresponder à conta informada pelo Telegram.
- Arquivos que descrevem contas diferentes ou credenciais de API diferentes são rejeitados em vez de selecionar apenas uma.
- O campo **“Senha ou texto da sessão”** contém o campo de senha local do TData, um campo para colar um StringSession e **ler arquivos sem fazer login** (preenche o formulário sem entrar em contato com o Telegram).

### Telethon `.session`

|  |  |
| --- | --- |
| O que é | O banco de dados SQLite que as ferramentas baseadas no Telethon criam, por exemplo, `my_account.session` |
| Reconhecido por | Tabelas `sessions` (com `dc_id`, `server_address`, `port`, `auth_key`) e `version` = 7 ou 8 |
| Requisitos | Exatamente uma linha de sessão autorizada; um banco de dados fechado e completo |

Feche primeiro o programa que criou o arquivo. Se `my_account.session-journal` ou `my_account.session-wal` estiverem presentes ao lado dele, o banco de dados não está finalizado: abra e feche o cliente original corretamente. A exclusão desses arquivos sidecar pode deixar uma cópia corrompida.

### Pyrogram `.session`

|  |  |
| --- | --- |
| O que é | As ferramentas baseadas no Pyrogram criam um banco de dados SQLite |
| Reconhecido por | Tabela `sessions` com `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 ou 3 |
| Requisitos | Uma sessão **de usuário** autorizado na rede de produção. Sessões de bots e de servidores de dados de teste (DC) são rejeitadas |

O ID do usuário armazenado é verificado no Telegram durante o login.

### Par de sessão + JSON

As contas costumam ser distribuídas como dois arquivos com o mesmo nome, por exemplo, `447700900123.session` e `447700900123.json`. Selecione **ambos** de uma só vez.

- A partir do JSON, o TgWitness utiliza `app_id`/`api_id` e `app_hash`/`api_hash`, de modo que normalmente não é necessário digitar credenciais da API.
- Outros campos, como `phone`, `device`, `sdk`, `app_version`, `lang_pack` ou uma senha `twoFA` armazenada, são **ignorados**. Caso a conta possua autenticação de dois fatores (2FA), o TgWitness solicita que ela seja fornecida.
- Um arquivo JSON por si só é apenas metadados. Sem o arquivo de sessão, prossiga com o login por telefone ou QR.

### Telegram Desktop (TData)

TData é a pasta `tdata` do aplicativo Telegram Desktop (o aplicativo multiplataforma disponível em desktop.telegram.org).

| Sistema | Localização padrão do `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram portátil: ao lado do `Telegram.exe`) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Para importá-lo:

> **Aviso sobre sessões paralelas.** A importação de TData reutiliza a chave de autorização do Telegram Desktop; ela não cria um login independente. Não utilize essa chave no Desktop e no TgWitness simultaneamente. O Telegram pode invalidar a autorização com `AUTH_KEY_DUPLICATED`, tornando ambas as cópias inutilizáveis até um novo login.
>
>
>
> Encerre totalmente o Desktop, incluindo seu processo na bandeja do sistema, e mantenha essa cópia fechada enquanto o TgWitness utiliza a sessão importada. **Encerre a sessão, não faça logout nem revogue a sessão:** a revogação também invalida a cópia importada. Caso precise que ambos os clientes estejam em execução, faça login no TgWitness por telefone ou QR para criar sua própria autorização. Recomenda-se uma conta dedicada, mas isso não torna as chaves clonadas seguras para uso em paralelo.
>
>
>
> Isso também se aplica a arquivos importados `.session` , ao texto da StringSession e à chave de autenticação HEX. Outros clientes com suas próprias autorizações criadas de forma independente podem permanecer conectados. Consulte [a documentação do Telegram sobre AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. Encerre completamente o Telegram Desktop.
2. Crie um arquivo ZIP contendo **apenas** estes dois itens do `tdata`:

   - `key_datas`
   - o arquivo de 16 caracteres que termina em `s` ao lado dele, geralmente `D877F783D5D3EF8Cs`

   Compactar a pasta inteira com seu cache de mídia geralmente excede os limites (512 entradas, 32 MiB descompactados). 3. Selecione o arquivo ZIP em **“Arquivos**”. Se o Telegram Desktop tiver uma **senha local**, insira-a primeiro no campo **“Senha” ou “Texto da sessão**”. Essa não é a senha da autenticação de dois fatores (2FA).

Compatível: uma conta por arquivo, armazenamento moderno `key_datas`/`key_data0`/`key_data1`, senha local. Não compatível: pastas com várias contas conectadas, layouts mais antigos da versão para desktop, arquivos ZIP protegidos por senha e o aplicativo nativo separado para macOS “Telegram para macOS”.

### Telethon StringSession

Uma única linha de texto, geralmente começando com `1` e com cerca de 350 caracteres. Carregue- a como um arquivo `.txt` ou `.tgwitness-session` (no máximo 4 KiB) ou cole-a em **“Código de acesso” ou “Texto da sessão**”. Apenas strings do Telethon são aceitas; as strings do Pyrogram e do TDLib utilizam formatos diferentes.

### JSON da conta

Um objeto JSON, com no máximo **64 KiB**, em um arquivo com extensão **`.json`**.

| Campo (pseudônimos) | Significado |
| --- | --- |
| `api_id` (`app_id`) | ID do aplicativo, um número positivo |
| `api_hash` (`app_hash`) | Hash do aplicativo, 32 caracteres hexadecimais |
| `string_session` (`session_string`, `session`) | Texto da StringSession do Telethon, não um nome de arquivo |
| `auth_key` (`auth_key_hex`) + `dc_id` | Chave de autenticação completa de 512 caracteres e DC 1–5 |
| `user_id` (`id`) | Opcional; verificado no Telegram antes que a autorização seja salva |

Caso haja tanto um apelido quanto o nome principal, ambos devem coincidir. Exemplos:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

O primeiro exemplo preenche apenas as credenciais da API; faça login por telefone ou QR, ou adicione um arquivo de sessão. Listas em massa (um array JSON de contas) não são aceitas.

## Identifique o que o senhor possui

| Como pode ver | Trata-se de | Utilização |
| --- | --- | --- |
| `*.session`; ao abri-lo em um editor de texto, aparece `SQLite format 3` na parte superior | Telethon ou Pyrogram SQLite | **Arquivos** (detectados automaticamente) |
| Uma pasta `tdata` contendo `key_datas` | Telegram Desktop TData | Compacte dois arquivos em ZIP e, em seguida, **Arquivos** |
| Uma linha de texto começando com `1`, cerca de 350 caracteres | Telethon StringSession | **Arquivos** |
| `*.json` com `app_id`/`app_hash` | Metadados complementares | **Arquivos**, juntamente com sua sessão |
| `*.json` com `auth_key` ou `string_session` | JSON da conta | **Arquivos** |
| 512 caracteres `0-9a-f` | Chave de autenticação | **Chave de autenticação** |
| 32 caracteres `0-9a-f` | Hash da API | **ID da API + Hash** |
| `td.binlog` ou `db.sqlite` de um aplicativo TDLib | Armazenamento TDLib | Não compatível |
| `123456789:AA…` | Token do bot | Não compatível |

## Formatos não suportados

| Formato | Alternativa |
| --- | --- |
| Armazenamento TDLib (`td.binlog`) e exportações TDLib | Faça login por telefone ou QR |
| **Sequências** de sessão do Pyrogram | Utilize o arquivo Pyrogram `.session`, ou o código QR/telefone |
| TData com várias contas conectadas | Faça logout das outras contas no Telegram Desktop ou utilize o arquivo de sessão específico de cada conta |
| Tokens de bot | Não suportado: o TgWitness atua como uma conta de usuário |
| Listas em CSV/JSON de diversas contas | Adicione um espaço de trabalho por conta |
| Sessões de teste no DC ou com bots | Utilize uma conta de usuário de produção |

## Várias contas

Pressione **+** ao lado do seletor de conta ou abra **Conta → Configurações → Configurações de conexão → Espaços de trabalho**, insira um nome e faça login.

- Qualquer número de espaços de trabalho, incluindo o principal. Cada um possui sua própria sessão, rota de proxy, fontes, política de captura, registro, chave de assinatura, pontos de verificação e exportações.
- A troca da área de trabalho exibida não interrompe as demais.
- Um diário permanece vinculado à conta que o criou. O login com uma conta diferente requer outro espaço de trabalho, e uma conta não pode ser atribuída a dois espaços de trabalho.
- O token do painel principal controla todas as áreas de trabalho. [O acesso concedido](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) pode restringir o acesso de outras pessoas a contas e chats selecionados, com permissões e limites de sessão distintos.
- **A função “Contas”** renomeia um espaço de trabalho e exclui um espaço adicionado, juntamente com sua sessão, registro, fontes e chave de assinatura. O espaço de trabalho principal não pode ser excluído do painel.

### Importação em lote e grupos de contas

Use **Contas → Importar contas** para adicionar várias contas, combinar arquivos pelo nome e ver o resultado de cada login. Cada conta recebe seu próprio espaço de trabalho. Os grupos podem copiar configurações selecionadas de um modelo sem unir sessões, chaves ou evidências. Veja [o guia de importação e grupos](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) e [o painel do pool MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Sair

**Conta → Sair do Telegram** (com a observação pausada) solicita ao Telegram que encerre a sessão, de modo que ela também desapareça da seção **Configurações → Dispositivos** da conta e remova a sessão do cofre do espaço de trabalho. O registro, as fontes, as configurações e a chave de assinatura permanecem, e o registro registra o encerramento da sessão. O espaço de trabalho ainda pertence à sua conta: somente essa conta poderá se conectar a ele novamente. Se o Telegram não responder, a sessão ainda será removida aqui e o painel indicará isso; encerre-a no Telegram em **Configurações → Dispositivos**.

## Converta uma sessão do Telethon para o modo offline

O painel importa arquivos `.session` diretamente. Para uma conversão offline para um arquivo StringSession, execute a partir da pasta do projeto:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

O conversor lê apenas arquivos SQLite do Telethon (até 64 MiB), nunca modifica os dados de entrada, não realiza solicitações de rede e se recusa a sobrescrever um arquivo de saída já existente.

## Mantendo os arquivos de contas em segurança

- Trate cada `.session`, TData ZIP, StringSession, chave de autenticação e JSON de conta como uma senha. O TgWitness mantém a autorização importada em seu cofre criptografado; o(a) senhor(a) pode remover os arquivos originais posteriormente.
- Não execute a mesma autorização em dois programas ao mesmo tempo. O Telegram pode revogá-la (`AUTH_KEY_DUPLICATED`), e ambas as cópias deixarão de funcionar.
- Uma sessão expirada ou revogada não pode ser reativada por meio de conversão. Faça login novamente.

## Solução de problemas

| Mensagem ou sintoma | O que fazer |
| --- | --- |
| *Não é possível ler esta sessão. Feche o cliente original…* | O arquivo SQLite está aberto ou incompleto (sidecar `-journal`/`-wal`). Feche o programa original corretamente e copie o arquivo novamente. |
| *Esquemas SQLite do Telethon compatíveis: 7 e 8* / *Pyrogram … 2 e 3* | O arquivo foi criado por uma versão muito antiga ou desconhecida da biblioteca. Faça o login por telefone/QR em vez disso. |
| *Apenas sessões de usuários de produção autorizadas são suportadas* | O arquivo Pyrogram pertence a um bot ou à rede de testes. |
| *O arquivo TData ultrapassa 512 entradas ou 32 MiB* | Compacte apenas os arquivos `key_datas` e `D877F783D5D3EF8Cs`, e não a pasta inteira. |
| *Não é possível descriptografar o TData. Verifique a senha local do Desktop* | Insira a senha local do Telegram Desktop no campo **“Senha” ou “Texto da sessão**”. |
| *Importe uma conta do TData por vez* | O Telegram Desktop possuía várias contas; consulte [“Formatos não suportados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#unsupported-formats)”. |
| *Os arquivos selecionados descrevem diferentes contas ou credenciais de API* | Selecione arquivos de apenas uma conta. |
| *O JSON não contém credenciais ou autorizações de API compatíveis* | Verifique os nomes dos campos no [JSON da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#account-json). |
| *Apenas metadados da API* | O JSON não possui sessão. Adicione o arquivo `.session` ou utilize o telefone/QR. |
| *A chave de autenticação HEX deve conter todos os 512 caracteres hexadecimais* | A chave está truncada ou contém “`…`”. |
| O ID da conta não corresponde à conta importada | O ID de usuário do arquivo difere do que o Telegram informa; o arquivo pertence a outra conta. |
| A conta já pertence a outro espaço de trabalho | Abra esse espaço de trabalho em vez de adicionar a conta duas vezes. |
| Conectado, mas falta um grupo privado na lista de bate-papos em **“Fontes”** | Verifique a adesão. O seletor analisa as primeiras 1.000 conversas; aumente o limite na seção **“Parâmetros**”. |
| Falha na conexão via proxy | Verifique a rota e o modo de IP. O MTProxy automático tenta outra entrada que esteja funcionando. O modo “Ocultar IP” aguarda; o modo alternativo explicitamente selecionado pode se conectar diretamente após o atraso configurado. Consulte [os modos de roteamento](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes). |

Veja também: [conexão e segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) para proxies e criptografia, e [como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/) do que é capturado após o login.
