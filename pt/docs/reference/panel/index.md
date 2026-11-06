# Guia do painel

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/

Todas as telas do painel: bate-papos, diário, fontes, exportações, Extras, modos de proteção e verificação de código.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Primeira configuração e ajustes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/) · [Contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/) · [Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) · [Relatórios de casos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/)

O que cada tela faz, o que ela grava no diário assinado e onde está o guia detalhado. O painel exibe um espaço de trabalho por vez: uma conta do Telegram com suas próprias fontes, diário e chave de assinatura. O seletor na parte superior da barra lateral alterna entre os espaços de trabalho. O endereço contém o espaço de trabalho (`?ws=…`); enquanto o endereço, o seletor e a conta carregada não coincidirem, as ações permanecem bloqueadas.

Use [Compare collection methods](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md) to choose between live observation, full history, fresh account/chat exports and saved-record handover. The Exports page includes the same comparison above its download controls.

**On this page**

- [Find your way](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#find-your-way)
- [Start here](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#start-here)
- [Chats](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#chats)
- [Journal](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#journal)
- [Sources](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#sources)
- [Exports](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#exports)
- [Settings, accounts and connection](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#settings-accounts-and-connection)
- [Extras](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#extras)
- [Protection modes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#protection-modes)
- [More tools](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#more-tools)

## Navegue pelo site

As seções diárias ficam na parte superior da barra lateral, **“Contas”** está em **“Espaço de trabalho”** , e todo o restante está em **“Mais ferramentas e configurações** ”. O seletor **de nível de interface** na barra superior determina quantas seções são exibidas:

| Nível | Seções na barra lateral |
| --- | --- |
| Simples | Página inicial, Conversas, Alterações, Arquivos e Configurações |
| Padrão | Além disso, Case Board, Contas e Acesso |
| Especialista | Além disso, há as seções Fontes, Extras, Pergunte ao arquivo, Parâmetros, Conta, Log do sistema e Integrações |

Chamadas simples: Comece aqui, Diário e **Página inicial** de exportações, **Alterações** e **Arquivos**. Um nível apenas oculta seções. Um recurso oculto continua funcionando, e o servidor verifica cada permissão por conta própria. Nível, idioma, tema e fuso horário são salvos por operador e espaço de trabalho; consulte [as configurações](https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/).

A barra superior também possui:

- **Vá para uma seção** (Ctrl+K ou ⌘K no Mac): encontre um chat, um parâmetro ou um registro do diário por `#number`. As setas movem a seleção, Enter abre e Esc fecha.
- **Notificações**: problemas e alterações no chat extraídos do diário. A opção **“Marcar tudo como lido”** zera o contador, e **“Regras de notificação”** abre as regras. O envio para o Telegram, Discord ou e-mail é configurado em [Extras → Notificações](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#notifications).
- O indicador de conexão para este espaço de trabalho. **O status do coletor,** abaixo da barra superior, divide-o em conexão com o Telegram, recebimento de eventos, fontes e fila de anexos.
- **Bloquear**: fecha o painel neste navegador. A coleção continua em execução no servidor.
- O modo de proteção ao lado do número da versão; consulte [os modos de proteção](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#protection-modes).

O espaço de trabalho de demonstração contém mensagens fictícias e nunca se conecta ao Telegram. Ações que alterariam um espaço de trabalho real são recusadas nesse ambiente.

## Comece aqui

Escolha uma tarefa. A opção **“Exportar minha conta”** baixa o que a conta pode ler no momento. A **opção “Acompanhar uma investigação”** registra novas mensagens, edições observadas e notificações de exclusão dos chats que você escolher. O cartão de configuração mostra as três etapas: conectar a conta, escolher fontes, iniciar a observação. A pergunta de objetivo permanece nesta página até que você a responda ou a pule. Um novo espaço de trabalho abre a [primeira configuração](https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/) em vez disso.

## Bate-papos

Conversas salvas, em modo somente leitura por padrão.

- Pesquise na lista por nome ou ID. **A opção “Escolher”** adiciona ou remove conversas monitoradas. A função “**Abrir link do Telegram”** aceita um nome de usuário ou link de convite e salva uma pré-visualização no diário. **“Entrar/abrir e observar”** entra na conversa e a adiciona às suas fontes; abrir um bot o envia `/start`.
- O cabeçalho do chat conta as mensagens **excluídas, o texto mantido**, **as excluídas antes do salvamento** e **as não encontradas na nova verificação**. A lista de chats e as notificações usam as mesmas definições. Uma mensagem excluída aparece em vermelho e mantém seu texto salvo; uma mensagem editada mantém todas as versões salvas. Cada exclusão indica o que se sabe: quando foi visualizada, que o Telegram não informa quem a excluiu ou que apenas a notificação foi recebida.
- **O histórico de carregamento** traz as últimas 100, 250 ou 500 mensagens para esta visualização e para o diário. Para carregar todas as fontes ativadas, use [Fontes → Histórico completo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#sources).
- **A exportação do chat** baixa todo o histórico visível como um `chat.json` e `chat.html`. Várias contas conectadas podem dividir o trabalho: cada uma baixa seu próprio intervalo de números de mensagens e assina sua parte, e a conta que inicia a exportação assina o arquivo. Veja como [exportar um chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md).
- **A seção “Pessoas”** lista todos aqueles com mensagens salvas neste chat. Os perfis das pessoas estão desativados por padrão, pois se tratam de dados pessoais de terceiros. Quando estão ativados para um chat, um perfil mostra nome e histórico de nomes de usuário, sinalizadores do Telegram, hashes de avatares, atividade, quem responde a quem, outros chats observados e carteiras, telefones, nomes de usuário e links mencionados. Cada fato aponta para seu registro. **A exportação de perfis** salva um arquivo assinado, opcionalmente em uma senha ZIP; desativar os perfis exclui o arquivo de perfil. Veja [os perfis das pessoas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#people-profiles).
- **A opção “Salvar perfil” agora** registra um instantâneo do perfil do chat ou do bot: descrição, membros, link de convite e comandos do bot.

### Somente leitura, envio e segredos

Dois botões acima das mensagens protegem a conta e o leitor:

- **O modo “Somente leitura”** fica ativado quando um chat é aberto. Desative-o para enviar mensagens ou clicar nos botões do bot . Cada ação exibe a pergunta **“Enviar como @conta?**” ou **“Clicar neste botão do bot como @conta?**”, informando que os participantes do chat verão a ação e que ela será registrada no diário assinado. **A opção “Não perguntar novamente por 10 minutos neste chat”** ignora a pergunta por um tempo. O envio fica desativado para a meta **“Evidências para um caso**”, no painel e na API.
- **O “Mask secrets”** oculta o que se parece com uma senha, um código de login, uma chave de API ou hash, um token de bot, uma string de sessão, uma chave privada, um JWT ou um número de cartão de pagamento (os números de cartão são verificados com a soma de Luhn). **A opção “Show”** revela um valor; a revelação é registrada no diário. O desativamento do mascaramento para este navegador também é registrado. Apenas a exibição muda: os registros originais e todas as exportações mantêm o texto completo.

## Registro

Todos os registros que o espaço de trabalho assinou, com os mais recentes em primeiro lugar.

- **A visão geral** contabiliza as mensagens observadas, as edições registradas, os avisos de exclusão e as fontes selecionadas.
- **Linha do tempo de eventos** filtra por tipo de evento (todos, edições, exclusões, reações, participação, cobertura), por texto e por fonte. **Carregar eventos anteriores** volta à página anterior.
- Abra um registro para ver seus detalhes, hash e carga útil. **O link para este registro** é um endereço que abre o mesmo registro. Eventuais segredos são ocultados nesta visualização; as exportações mantêm o original.
- O diário é do tipo “somente adição”: nada no painel edita ou exclui um registro. Verifique isso em **Exportações → Verificar diário** ou `python -m tgwitness.verify`; consulte [exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/).

## Fontes

Quais conversas esse espaço de trabalho registra e o que ele mantém delas. As alterações se aplicam às atividades futuras; os registros salvos permanecem.

**A função “Atualizar lista de bate-papos”** lê os bate-papos e as pastas da conta. Ela não baixa mensagens.

### Escopo

- **O que esta conta registra** : **Conversas selecionadas** (apenas os chats que você adicionar), **Pasta do Telegram** (uma das pastas da conta, incluindo chats adicionados a ela posteriormente) ou **Conta completa** (todos os chats, além de cada novo chat, grupo, chat privado ou bot assim que aparecerem). **Modo de investigação** é para uma conta dedicada: ela registra tudo o que a conta visualiza, suas próprias mensagens e cliques nos botões, e salva imediatamente o perfil de cada novo chat e as mensagens visíveis anteriores. A imagem [guia dedicado à conta](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) explica por que nunca se deve usar sua conta principal.
- **Os tipos de fonte** limitam os modos de pasta e de conta inteira a canais, grupos, conversas privadas e bots. **“Ações próprias”** adiciona as mensagens, edições e digitações no teclado de resposta da própria conta.
- **Quando um novo chat ou bot aparece**: salve seu perfil e até o número escolhido de suas últimas mensagens visíveis.

Limites: conversas secretas nunca chegam a TgWitness. Nada é registrado enquanto TgWitness não estiver em execução; após uma reinicialização, ele recupera apenas o que o Telegram ainda retorna, e o relatório mostra a lacuna. Conversas além do limite da lista de conversas (1.000 diálogos, a menos que alterado em Parâmetros) são adicionadas assim que se tornarem ativas. Botões do bot embutidos pressionados em outro aplicativo ficam invisíveis; a resposta do bot é registrada.

### Bate-papos abrangidos

Filtre por status (**Ativado**, **Pausado**, **Prioridade**, **Excluído**, **Acesso não confirmado**, **Ignorado**) e tipo; em seguida, execute uma ação na seleção: ativar, pausar, marcar ou remover prioridade, excluir do escopo ou remover. O ícone de status mostra apenas o estado; as ações estão no menu de cada linha, com uma descrição do que elas fazem. A pausa e a exclusão solicitam confirmação, inclusive em lote. A remoção de uma fonte solicita seu nome e exclui os perfis das pessoas relacionadas; seus registros salvos permanecem no diário.

Uma fonte que não aparece na lista de bate-papos da conta é **recebendo atualizações, fora da lista de bate-papos**, enquanto os registros continuam chegando; caso contrário, **acesso não confirmado**. **Conversas disponíveis** adiciona bate-papos com **Adicionar selecionados** ou **Adicionar todos os resultados**.

### Histórico completo

Carrega o histórico disponível de todas as fontes ativadas nas conversas e no diário. O progresso é mantido após uma reinicialização; os anexos seguem suas configurações de mídia. Veja [o histórico da fonte](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/).

### Gravação

- **Escolha quais alterações preservar**: novas mensagens, edições, avisos de exclusão, reações visíveis, entradas e saídas. Uma predefinição altera o formulário; a opção **“Salvar configurações de registro”** a aplica. Reativar uma categoria não recupera eventos perdidos.
- **Preserve a mídia quando disponível**: baixe anexos com tamanho máximo por arquivo, defina por tipo de 1 a 2.000 MiB e limite a duração do vídeo em segundos (0 significa sem limite). Cada tentativa de download tem seu resultado registrado.
- **Recheck**: verifica os chats prioritários a cada poucos minutos, os demais chats raramente, para que a conta fique dentro dos limites do FloodWait do Telegram. O valor 0 desativa um grupo. Marque os chats prioritários com a estrela na lista; o número de chats por rodada e a pausa entre os chats estão em Parâmetros. Consulte [a coleção](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/).

## Exportações

**A seção “Downloads”** prepara os arquivos; **o “Relatório de compilação”** define a aparência dos relatórios.

| O que | Use-o para | Guia |
| --- | --- | --- |
| Exportação de contas | Um instantâneo atualizado do que a conta pode ler agora | [Exportação de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/account-export/) |
| Compartilhamento de cópia | Uma versão simplificada de uma exportação de conta concluída | [Divulgação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Assinado ZIP | Diário, relatório, anexos e ferramentas de verificação dentro de um limite fixo do diário | [Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) |
| Relatório em HTML, PDF e JSON | Um relatório selado e legível | [Relatórios de casos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/) |
| JSONL, CSV | Registros originais com assinaturas; uma planilha com fórmulas protegidas | [Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) |
| Trecho da transferência | Apenas os chats, o período e as pessoas de que o destinatário precisa | [Evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#investigation-handoff) |
| Exportação de bate-papo | Um chat assinado `chat.json` e `chat.html` | [Exportar um chat](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Criptografar os downloads acima com uma senha** (12 caracteres ou mais) salva um arquivo AES-256 ZIP que o 7-Zip ou o WinRAR abrem. O arquivo assinado dentro dele permanece inalterado. A senha não é armazenada.
- **As exportações preparadas** mantêm até 20 arquivos dentro de 2 GiB, além do mais recente, para downloads repetidos, cada um com seu SHA-256. A preparação de um arquivo não garante a entrega.
- Quando o navegador recusa a caixa de diálogo de salvamento, o painel recorre a um download comum.
- **Sua identidade de assinatura** exibe a impressão digital da chave. As opções **“Salvar ponto de verificação**” e “Baixar **recibo de execução assinado”** fornecem registros para serem mantidos fora do coletor. A opção “Preparar **solicitação de carimbo de data/hora”** cria uma solicitação RFC 3161 sem entrar em contato com nenhum serviço.

## Configurações, contas e conexão

- **Configurações**: objetivo, conexão, o que registrar e a interface. Consulte [a primeira configuração e as definições](https://phishdestroy.github.io/TgWitness/pt/docs/reference/settings/).
- **Contas**: cada espaço de trabalho com seu estado, fontes, eventos e fila de anexos. Filtre por **“Precisa de atenção**”, **“Em coleta”**, **“Offline” ou “Pausado”** ou **“Não conectado”**, pause ou retome uma seleção, importe arquivos de contas em massa e gerencie grupos. Consulte [contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/).
- **Conta**: login e a rota de conexão desta conta. Direta, um perfil do WireGuard, seu próprio proxy, o pool público do MTProto ou o WARP; prepare e verifique uma rota, em seguida, aplique-a a esta conta, a um grupo ou a todas as contas. Consulte [conexão e proxies](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) e [proxies](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md).

## Extras

Opcional: basta uma conta e algumas fontes para começar a coletar. Apenas a opção que você escolher abre suas configurações, e nada é conectado automaticamente. O cartão **“Nível de proteção”,** na parte superior, mostra o [modo de proteção](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#protection-modes).

| Cartão | O que ela oferece | Guia |
| --- | --- | --- |
| Armazenamento e espaço em disco | Backups, transferência de arquivos mais antigos para sua nuvem, uma cópia de evidência que não pode ser excluída | [Armazenamento](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/) |
| Objetivo e nível de proteção | Configurações sugeridas para sua meta e duas escalas | [abaixo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#goal-and-protection-level) |
| Notificações | Problemas, mensagens alteradas e um resumo diário; seu próprio bot de controle | [abaixo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#notifications) |
| Evidências e backups | Registros de data e hora, mais testemunhas e uma cópia criptografada armazenada externamente | [abaixo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#evidence-and-backups) |
| Servidor 24 horas por dia, 7 dias por semana | Um servidor na nuvem sem SSH, criado e excluído a partir do painel | [Alta segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#from-the-panel) |
| Testemunha independente | Verificações assinadas publicadas no seu canal do Telegram ou no Discord | [Witness](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/) |
| Verificação de código | Compara o programa em execução com um commit público no GitHub | [abaixo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/panel/#code-check) |

### Objetivo e nível de proteção

Quatro perguntas:

1. **Para que serve?** Um registro pessoal, uma investigação ou provas para um caso.
2. **O que você pretende monitorar?** Algumas conversas (até cerca de 50), muitas conversas (até cerca de 500) ou contas inteiras. Isso define o limite da lista de conversas para 1.000, 3.000 ou 20.000.
3. **Fotos e arquivos?** Apenas texto, fotos e mídias curtas (fotos de até 20 MB, vídeos de até 100 MB) ou tudo (vídeos e documentos de até 1 GB cada). A opção “Tudo” com contas completas também mantém 4 GiB de espaço livre em disco.
4. **Onde ela será executada?** Neste computador ou em um servidor que fica sempre ligado.

A sugestão lista carimbos de data/hora independentes, drand e a lista de dispositivos do Telegram, cada um com uma linha explicando o que ele acrescenta. Os carimbos de data/hora são gerados a cada 60, 30 ou 10 minutos para um registro pessoal , uma investigação ou prova; o drand e a lista de dispositivos precisam de carimbos de data/hora. **Aplique** alterações apenas a esses itens, à política de anexos e aos dois parâmetros acima. Cada alteração é um registro no diário, além de `setup.applied`. Notificações, uma cópia externa, um servidor, DNS de gateway, a verificação de código e uma testemunha são oferecidos como próximas etapas com seus próprios formulários.

Duas escalas são calculadas com base no que está definido, e não na meta:

| Escala | Pontos |
| --- | --- |
| Credibilidade | Diário assinado 1, carimbos de data/hora 3, drand 1, lista de dispositivos 1, verificação de código que corresponde a 1, sondagem de testemunhas 1, servidor atestado 2, log de DNS do Gateway 1 |
| Confiabilidade | Servidor sempre ativo 3, cópia externa 3, Object Lock 1, notificações de problemas 1 |

80% ou mais de leituras **no máximo**, 50% **alto**, 25% **moderado**, abaixo disso **é básico**. Atualmente, a confiabilidade leva em conta um servidor sempre ativo, conforme a resposta à pergunta 4, antes que qualquer servidor seja verificado.

### Notificações

As notificações são enviadas pelo Apprise para o Telegram, Discord, Slack, ntfy, e-mail, Matrix e mais de 100 outros serviços. Escolha um serviço, preencha um ou dois campos e envie um teste, ou cole os endereços do Apprise diretamente.

- **Problemas**: disco quase cheio, conta desconectada, erros de coleta, cópia ou registro de data e hora . Em um servidor isolado, uma porta SSH aberta ou um login também constituem um problema.
- **Alterações**: mensagens excluídas, editadas e ausentes nos chats observados, agrupadas em uma notificação por verificação (a cada minuto, a menos que alterado em Parâmetros).
- **Tarefas concluídas**: histórico, exportações e cópias de armazenamento.
- **Resumo diário** na hora escolhida, de acordo com o horário do servidor.

As notificações exibem nomes de chats e contagens. Trechos de mensagens estão desativados por padrão; quando estão ativados, o texto das mensagens sai deste computador.

**Seu bot operador** é um bot criado por você mesmo no @BotFather que responde `/status` e `/stats`, e, opcionalmente, `/pause`, `/resume` e `/copy`. Apenas o chat listado e os IDs de usuário do Telegram podem usá-lo; o texto da conversa permanece no espaço de trabalho. Use um bot separado se outro aplicativo já receber seus comandos. Consulte [notificações](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) e [bot operador](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#operator-bot-and-completion-notices).

### Evidências e backups

- **Carimbos de data/hora independentes** enviam apenas o SHA-256 de cada ponto de verificação assinado para as autoridades da RFC 3161 e para os calendários do OpenTimestamps, a cada 5 a 1.440 minutos. **O Anchor agora** está executando uma rodada. Veja [os carimbos de data/hora](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/).
- **Mais testemunhas**, cada uma desativada até ser selecionada: a rodada mais recente do drand, a lista do Telegram de dispositivos conectados sem endereços IP e o log do Cloudflare Gateway das consultas DNS do servidor. Veja [os registros opcionais](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **O backup criptografado** copia o diário, os arquivos, os pontos de verificação e as exportações de bate-papos para um armazenamento compatível com S3 (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Tudo é criptografado primeiro nesta máquina. **Baixe a chave de criptografia** e mantenha-a em local separado: sem ela, a cópia não pode ser lida. O Object Lock no modo Governança ou Conformidade impede que os objetos sejam excluídos por um número definido de dias. Consulte [a cópia externa](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Verificação de código

Verifica se o programa instalado corresponde a uma versão publicada.

1. Insira um repositório do GitHub (o oficial já está preenchido) e uma tag, um branch ou um commit.
2. **O `Check now`** consulta a API do GitHub, por meio da rota deste espaço de trabalho para solicitações externas, para obter a lista de arquivos desse commit. Ele compara o ID do blob do Git de cada arquivo de programa avaliado com o commit. Uma cópia do Windows com finais de linha convertidos ainda é compatível.
3. O resultado lista arquivos alterados, adicionais e ausentes (até 50 de cada) e é salvo como um `source.checked` registro de diário.

O resultado é considerado atual apenas enquanto os arquivos do programa em execução permanecerem inalterados: verifique novamente após uma atualização. Não é necessário nenhum token e apenas repositórios públicos funcionam; chats e credenciais não são enviados. Uma correspondência identifica o código no disco. Não se trata de atestado de hardware; para isso, consulte [o Phala Cloud](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Modos de proteção

O seletor ao lado do número da versão mostra o modo escolhido e quantas das 18 camadas de proteção estão ativas, por exemplo `🟠 Witnessed 9/18`. **Para alterar o modo** em **Extras → Nível de proteção**, abra o menu de opções. Cada modo descreve um alvo e lista o que ainda está faltando; o registro, a assinatura e as configurações salvas são os mesmos em todos os modos.

| Modo | Para | Adiciona |
| --- | --- | --- |
| 🟢 Fácil | Acompanhar um chat e manter uma cópia | Bate-papos, o diário e as exportações de bate-papos; a assinatura ocorre em segundo plano |
| 🟡 Assinado | Envia relatórios para uma plataforma, um provedor de hospedagem ou uma central de denúncias | Arquivo assinado, verificação de diário, pontos de verificação, extrato de transferência |
| 🟠 Testemunhado | Casos em que alguém pode alegar que o registro foi alterado | Uma testemunha independente que publica cabeçalhos de diário assinados |
| 🔴 Pronto para uso em tribunal | Provas para um advogado, a polícia ou um tribunal | Carimbos de data e hora, uma cópia criptografada armazenada externamente, detalhes do caso em relatórios |
| 🟣 Verificado pelo GitHub | Registros cujo software qualquer pessoa deve poder verificar | Verificação de código e captura do GitHub Actions |
| ⚫ Mossad | Casos de alto risco contra um adversário com recursos financeiros consideráveis | Um servidor seguro 24 horas por dia, 7 dias por semana, um endereço IP oculto e todas as 18 camadas |

As camadas: cada registro assinado e encadeado; um recibo de execução assinado; anexos salvos com SHA-256; pontos de verificação assinados; novas verificações; alertas de problemas; acesso de testemunha somente para leitura; uma testemunha realizando verificações conforme o cronograma; carimbos de data/hora RFC 3161; provas OpenTimestamps; um carimbo de data/hora mais recente verificado; uma cópia criptografada fora do local; detalhes do caso em relatórios; uma verificação de correspondência de código ; o Telegram nunca vê o IP desta máquina; solicitações externas por meio de um proxy; Object Lock na cópia; um servidor selado com registros do provedor. Uma camada desativada possui **a opção “Configurar”**, que abre seu formulário. Escolher um modo inferior solicita confirmação e não exclui nada.

## Mais ferramentas

**Extras → Independent capture**: connect a separate browser or AyuGram recorder, pin its signing key, select capture options, start/pause, take snapshots and download verified signed archives. Each recorder has its own manual login, route, journal and key. Both connections start disabled. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md).

- **Consulte o arquivo**: pesquise observações salvas, analise as fontes e, em seguida, decida se deseja enviá-las a um modelo de IA. Veja [a análise do arquivo](https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/) e [o OCR e a transcrição locais](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/).
- **Parâmetros**: limites e ritmo de coleta, novas verificações, downloads, perfis, notificações e exportações. Pesquise por nome, exiba os valores de **Apenas alterados** e prepare as configurações padrão como um rascunho com **Restaurar padrões…**. **Salvar parâmetros** aplica os valores a partir do próximo uso, e cada alteração é um registro no diário.
- **Acesso**: tokens separados para revisores, analistas e operadores, limitados a determinados espaços de trabalho, chats e permissões. Consulte [a seção de acesso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/).
- **Log do sistema** : o que este processo fez desde que foi iniciado (conexões, alterações de proxy, logins, recusas, alterações de configurações) com os endereços IP ocultos. A opção **“Seguir novas linhas”** mantém a linha mais recente em exibição. As mensagens permanecem apenas no diário.
- **Integrações**: o provedor de IA, conexões [MCP somente leitura](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/) e [webhooks assinados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/webhooks/).
- **Case Board**: notas privadas da equipe, favoritos e trechos ao lado das evidências. Veja [Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/).
- **Capturas do GitHub Actions** em “Exports”: um chat capturado do seu fork. Veja [captura selada](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md).
