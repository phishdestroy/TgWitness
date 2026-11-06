# Investigue em todos os chats

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/cases/

Um caso inteiro entre canais, grupos, chats privados e bots: coletar, ligar os pontos, reconstruir a linha do tempo e entregar.

Um incidente inventado, do começo ao fim. Coleta, pesquisa e perfis de pessoas encontram os registros, o [Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/case-board/) organiza e o [Report studio](https://phishdestroy.github.io/TgWitness/pt/docs/reports/) apresenta.

CASO TRATADO / UM DESTINATÁRIO DE PAGAMENTO ALTERADO

### Um incidente. Quatro conversas. Um rastro a ser reconstruído.

Um post de canal aponta para um bot. Um grupo fala de um novo link de pagamento e o bot o mostra. O post é editado, um chat privado repete o link e uma mensagem do grupo some.

Quem publicou cada versão?Onde o link apareceu?Qual arquivo foi preservado?O que mudou e quando?

Carga de histórico, IA, MCP, OCR e webhooks: [Trabalhar o arquivo](https://phishdestroy.github.io/TgWitness/pt/docs/archive/).

## 1. Abranger toda a conta

Escopo de conta inteira só em conta dedicada. Uma conta principal usa chats escolhidos ou uma pasta.

1. [Conecte a conta](https://phishdestroy.github.io/TgWitness/pt/docs/accounts/) em um espaço próprio. Anote a referência do caso, o ID da conta, o espaço e a impressão digital da chave.
2. **Fontes → Escopo de observação → Modo investigação**: **Conta inteira**, os quatro tipos de fonte e **Ações próprias**. Cada chat novo tem o perfil e as últimas **200 mensagens visíveis** salvos. **Salvar escopo** e confirme.
3. **Carregar chats** e compare com a lista de chats da conta. O limite é de 1.000 diálogos (até 20.000 em **Parâmetros → Chats lidos da lista da conta**); os que ficarem de fora aparecem quando ficarem ativos.
4. **Configurações de gravação** → **Toda a atividade visível**, confira limites de anexos e espaço em disco. Inicie e teste com uma mensagem, uma edição e uma exclusão.

CanaisGruposConversas privadasBots

UMA CONTA / UMA CHAVE DE ASSINATURA**Todas as atividades visíveis na conta selecionada → um único registro**

Mensagens · edições · notificações de exclusão · reações visíveis · eventos relacionados à adesão · ações próprias

"Conta inteira" significa todos os chats que esta conta consegue abrir, menos as exclusões. Sem chats secretos. Chats novos entram conforme aparecem; o histórico antigo não é baixado sozinho.

## 2. Obter o histórico e preservar os arquivos

Crie uma coleção no Case Board e marque o que importa. Mantenha um registro de fontes: ID do chat, título, conta, papel, início da captura ao vivo, resultado do histórico, resultado de mídia e lacunas.

| Necessidade | Ação no painel | O que ela oferece |
| --- | --- | --- |
| Histórico em todos os chats ativados | Fontes → Carregar histórico completo | As mensagens anteriores disponíveis são inseridas no diário da área de trabalho, com opções de pausar/retomar e um relatório de progresso assinado. [Guia do histórico](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/). |
| Contexto do bate-papo existente no registro | Fontes → Configurações de registro → Instantâneo do histórico | Mensagens recentes como registros assinados. 500 por padrão, até 10.000 em **Parâmetros → Maior snapshot de histórico**. |
| Histórico completo, atualmente visível, de um chat | Exportação completa do chat → Exportar chat completo, ou Chats → Exportar chat | Um pacote assinado à parte com `chat.json` e `chat.html`, um por chat. |
| Contexto em que surge um novo chat | Âmbito de observação → Quando surge um novo chat ou bot | O perfil e até 1.000 mensagens recentes (200 no modo investigação). Não vale para chats existentes. |
| Bytes do anexo | Download de anexos visíveis + limites por tipo | Procure `media.saved` com SHA-256 e tamanho. Na fila, pulado ou com falha significa não salvo. |

Uma exportação de chat não entra no diário nem nos perfis de pessoas. Para pesquisar histórico antigo dentro do TgWitness, use **Carregar histórico completo** ou snapshots.

Aqui: o canal, o grupo, o chat com o bot e o chat privado, mais o arquivo da fatura e seu hash. O que foi excluído antes da captura já era.

## 3. Acompanhe a evolução da conversa e suas próprias ações

Deixe rodando. Marque com estrela os chats quentes como prioritários, ajuste as reverificações em **Configurações de gravação → Reverificação** e fique de olho em `recheck.completed`, FloodWait e resultados de mídia.

**Chats → Perfil → Salvar perfil agora** salva a descrição do chat, os comandos do bot e outros metadados.

**Seguir um bot ou aceitar um convite como parte do caso**

1. **Chats → Abrir link do Telegram**, salve a prévia primeiro. Link e prévia viram registros assinados.
2. Se precisar, **Entrar / abrir e observar** entra no chat ou inicia o bot com o parâmetro de início.
3. Para documentar uma ação, responda ou use **Pressionar botão** no painel. Você recebe `interaction.requested` e `interaction.result` com a resposta do bot.

São ações reais. Botões apertados em outro app não aparecem, só a resposta do bot. Sem web apps, pagamentos ou telefone/localização.

## 4. Acompanhe pessoas, links e arquivos nas conversas

1. **Diário**, **Todas as fontes**, pesquise uma frase, um domínio ou um usuário. Abra os resultados e mande-os **Para o quadro**.
2. **Chats → Pessoas → Ativar perfis**, escolha alguém: histórico de nomes, respostas, atividade, **Também em…**, links, carteiras, telefones. Abra os registros citados.
3. Siga o mesmo ID numérico de usuário em outros chats. Um nome, carteira ou avatar coincidente é pista, não prova.
4. Compare hashes de arquivos. Mesmo SHA-256 = mesmos bytes. Quem compartilhou é outra questão.

MAPA DO CASO / SIGA AS REFERÊNCIASCaso fictício · não se trata de um gráfico em tempo real

CANAL / ANÚNCIO**Original → destino editado**

Registros n.º 101, n.º 188; Mensagem n.º 84 · remetente não identificado

GRUPO / OPERAÇÕES**O usuário 71001 publica o novo link**

Registro nº 146 · mensagem nº 309 Recibo de arquivo salvo nº 151

BOT / CONVERSA SOBRE PEDIDOS**Um botão direciona para esse destino**

Registro nº 173 · mensagem nº 12 Metadados do botão “Retornar”

PRIVADO / ACOMPANHAMENTO**O usuário 71001 repete o destino**

Registro nº 205 · mensagem nº 922 Recibo do arquivo salvo nº 209

Quatro conversas trazem observações diferentes. Siga os registros de origem para cada conexão; a postagem no canal não tem remetente identificado.

Os IDs numéricos e as referências dos registros foram criados especialmente para este guia prático. Este mapa explicativo mostra como conectar resultados de pesquisa, perfis e registros inspecionados; o Case Board armazena os cartões correspondentes e as referências das fontes.

| Conexão | Observação complementar | Conclusão a ser mantida |
| --- | --- | --- |
| A mesma conta do Telegram | ID de usuário 71001 no grupo #146 e no chat privado #205 | O mesmo ID de remetente nos dois chats. Quem é na vida real é outra questão. |
| Destino repetido | `pay.example.invalid/new` no #146, metadados do botão #173, postagem editada #188 e #205 | O mesmo link em quatro lugares. Quem o controla exige outras fontes. |
| Mesmos bytes do arquivo | Valores SHA-256 idênticos nos recibos de mídia concluídos nº 151 e nº 209 | Os dois arquivos são idênticos byte a byte. |

Os perfis só cobrem quem escreveu algo *neste espaço*; não são uma lista de membros. Citações por fato: **Parâmetros → Registros citados por fato**.

## 5. Reconstruir a sequência e assinalar as lacunas

Versões em **Chats**, depois **Diário** com **Todas as fontes** + **Edições**, **Exclusões**, **Cobertura**. Coloque os dois horários na linha do tempo: a data do Telegram e quando foi observado.

1. 09:00 · #101**Postagem do canal capturada**

   O destino original é mantido.
2. 09:12 · #146 / #151**O grupo apresenta um link diferente**

   O usuário 71001 publica a postagem; o download de um anexo é concluído.
3. 09:16 · #173**O bot exibe o mesmo destino**

   Os metadados do teclado salvos contêm o link.
4. 09:20 · #188**Alterações no anúncio do canal**

   Tanto as observações originais quanto as editadas permanecem.
5. 09:24 · #205 / #209**O acompanhamento privado repete isso**

   O anexo salvo possui o mesmo SHA-256 completo que o nº 151.
6. 09:28 · #231**Chega a notificação de exclusão do grupo**

   A observação anterior mantém-se: não são fornecidos nem o autor da exclusão nem a hora exata da exclusão.

Tempos de observação e referências ilustrativos. Outros registros do diário ocorrem entre essas entradas.

A ordem do diário é a ordem de chegada, não necessariamente a ordem dos acontecimentos. Mantenha separados registros ao vivo, snapshots, mensagens recuperadas, exclusões e "não encontrado na reverificação" e marque cada lacuna como desconhecida.

## 6. Estender o caso a outras contas de coleta

Um espaço por conta, mesmos passos. Anote o papel e a impressão digital de cada um. Os números de mensagem são por conta, então indique sempre o espaço e o chat.

Um [grupo de contas](https://phishdestroy.github.io/TgWitness/pt/docs/groups/) mostra o status, compartilha configurações e exporta todo mundo junto, cada um com seu diário e sua chave. A linha do tempo entre contas você monta nas suas notas.

Caso longo? Acrescente uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/) e teste o que cada conta realmente captura.

## 7. Entregar um pacote de caso verificável

Um ZIP assinado de cada espaço (sempre o diário inteiro; filtros não importam), mais perfis de pessoas, exportações de chats e arquivos.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Envie as impressões digitais separadamente. Verifique tudo contra o próprio espaço:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Guarde a saída do verificador, os originais, a cobertura e o registro de entrega com suas conclusões. Escreva tudo no Report studio. Se o destinatário precisar de menos, prepare uma [entrega minimizada](https://phishdestroy.github.io/TgWitness/pt/docs/handover/).
