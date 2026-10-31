# Investigue em todos os chats

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/cases/

Trabalhe um caso inteiro abrangendo canais, grupos, conversas privadas e bots: colete, conecte, reconstrua e entregue as evidências.

Este passo a passo acompanha um incidente fictício ao longo de toda a sua evolução. Ele utiliza os recursos reais de coleta, pesquisa, perfil de pessoas e exportação. O mapa do caso é um exemplo de documentação; suas conclusões e o registro do caso são mantidos fora do aplicativo.

CASO TRATADO / UM DESTINATÁRIO DE PAGAMENTO ALTERADO

### Um incidente. Quatro conversas. Um rastro a ser reconstruído.

Um anúncio no canal indica um bot. Um grupo de operações discute um novo link de pagamento. Uma mensagem privada de acompanhamento repete essa informação. Posteriormente, o anúncio é editado e uma mensagem do grupo desaparece.

Quem publicou cada versão?Onde o link apareceu?Qual arquivo foi preservado?O que mudou e quando?

Para carregamento do histórico, revisão opcional de fontes por IA, MCP, OCR e webhooks de saída, consulte [“Trabalhar com o arquivo](https://phishdestroy.github.io/TgWitness/pt/docs/archive/)”.

## 1. Abranger toda a conta

1. [Conecte a conta de coleta](https://phishdestroy.github.io/TgWitness/pt/docs/accounts/) em seu próprio espaço de trabalho. Registre a referência do caso, o ID da conta, o nome do espaço de trabalho e a impressão digital da chave de assinatura em suas anotações do caso.
2. **Fontes** abertas **→ Escopo de observação → Modo de investigação**. Analise **toda a conta**, todos os quatro tipos de fonte e **as ações próprias**. Esta predefinição permite salvar o perfil de uma nova fonte e suas últimas **200 mensagens visíveis**. Clique em **“Salvar escopo”** e conclua a confirmação do escopo.
3. Clique em **“Carregar conversas**”. Compare as fontes com a lista de diálogos da conta e verifique as exclusões. Em **“Parâmetros” → “Conversas lidas da lista da conta**”, ajuste o limite inicial da lista, se necessário: o padrão é 1.000 diálogos, configurável até 20.000. As conversas que excederem o limite serão detectadas assim que se tornarem ativas.
4. Nas **configurações de gravação**, selecione e salve **“Todas as atividades visíveis**”. Verifique os tipos de anexos, os limites de tamanho e o espaço livre em disco. Inicie a observação e valide uma mensagem controlada, bem como edições e exclusões, antes de confiar na configuração.

CanaisGruposConversas privadasBots

UMA CONTA / UMA CHAVE DE ASSINATURA**Todas as atividades visíveis na conta selecionada → um único registro**

Mensagens · edições · notificações de exclusão · reações visíveis · eventos relacionados à adesão · ações próprias

A opção “Conta completa” abrange os chats aos quais esta conta tem acesso, com os tipos de fonte e exclusões configurados. Os chats secretos não estão disponíveis. Novas caixas de diálogo são adicionadas à medida que as atualizações são disponibilizadas; ativar este modo não faz com que o histórico completo de todos os chats existentes seja baixado automaticamente.

## 2. Obter o histórico e preservar os arquivos

Crie um registro de fontes para toda a investigação. Atribua a cada conversa uma linha com seu ID numérico, título, conta, acesso/função, início em tempo real, aquisição do histórico, resultado de mídia e lacunas conhecidas. Marque uma fonte como adquirida somente após verificar o resultado relevante.

| Necessidade | Ação no painel | O que ela oferece |
| --- | --- | --- |
| Histórico em todos os chats ativados | Fontes → Carregar histórico completo | Funcionalidade principal atual: as mensagens anteriores disponíveis são inseridas no diário da área de trabalho, com opções de pausar/retomar e um relatório de progresso assinado. [Guia do histórico](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/). |
| Contexto do bate-papo existente no registro | Fontes → Configurações de registro → Instantâneo do histórico | Mensagens visíveis recentes como observações assinadas. Limite máximo padrão de 500; em **Parâmetros → “Maior instantâneo do histórico”**, é possível aumentar esse limite para até 10.000. |
| Histórico completo, atualmente visível, de um chat | Exportação completa do chat → Exportar chat completo, ou Chats → Exportar chat | Um pacote assinado separado com `chat.json` e `chat.html`. Repita para cada fonte; mantenha os resultados de sucesso/falha. |
| Contexto em que surge um novo chat | Âmbito de observação → Quando surge um novo chat ou bot | Um perfil da fonte e até 1.000 mensagens recentes visíveis; o modo de investigação seleciona 200. As conversas existentes não recebem esses dados retroativamente. |
| Bytes do anexo | Download de anexos visíveis + limites por tipo | Verifique se há o código `media.saved`, seu SHA-256 e a contagem de bytes. Um download em fila, ignorado ou com falha não é considerado um arquivo preservado. |

A exportação completa de um chat é um instantâneo separado; ela não importa todo o histórico para o diário nem para os perfis das pessoas. Use a opção **“Carregar histórico completo** em todas as fontes ativadas” ou instantâneos de diário delimitados para o material histórico que você precisa pesquisar no TgWitness. Verifique a lista de fontes antes de iniciar a execução.

No caso em análise, obtenha o canal de anúncios, o grupo de operações, a conversa com o bot e o acompanhamento privado. Preserve os bytes e o hash do anexo da fatura. O histórico disponível atualmente não permite reconstruir uma mensagem excluída antes da captura nem uma edição intermediária que o Telegram não retorne mais.

## 3. Acompanhe a evolução da conversa e suas próprias ações

Mantenha a observação em andamento à medida que o caso se desenvolve. Marque com estrela os chats ativos do caso como fontes prioritárias; configure as verificações de fontes prioritárias e outras fontes em **Configurações de gravação → Verificação**. Analise `recheck.completed`, a atualização contínua, o FloodWait e os resultados de mídia à medida que o trabalho avança.

Utilize **“Bate-papos” → “Perfil” → “Salvar perfil agora”** para manter as descrições de fonte atuais, os comandos do bot e outros metadados fornecidos pelo Telegram. Esse perfil de fonte é distinto dos perfis de pessoas criados a partir das mensagens do registro.

**Seguir um bot ou aceitar um convite como parte do caso**

1. Em **“Chats” → “Abrir link do Telegram”**, salve primeiro a visualização. O link original e a visualização gerada tornam-se registros assinados.
2. Caso a investigação assim o exija, **o comando “Join / open” permite** acessar ou abrir a fonte e inicia um bot com o parâmetro de inicialização fornecido. Uma solicitação de acesso pendente permanece pendente no registro.
3. Para uma ação que precise ser documentada, utilize a resposta de texto do painel ou o comando **“Pressar botão” (**compatível). O registro mantém `interaction.requested` e `interaction.result`, incluindo o texto ou URL de retorno da chamada.

Esses controles executam ações reais no Telegram. Um botão de retorno pressionado em um aplicativo diferente do Telegram não é visível para o coletor; a mensagem ou edição subsequente do bot pode ser. Aplicativos da web, pagamentos e solicitações de telefone/localização estão fora do minicliente.

## 4. Acompanhe pessoas, links e arquivos nas conversas

1. Abra **o Diário**, deixe o filtro de fontes em **“Todas as fontes”** e pesquise uma frase específica, um domínio, um nome de usuário ou um identificador salvo. Abra cada registro correspondente e anote o chat, o ID da mensagem e o número de sequência do diário.
2. Para acessar um chat específico, abra **Chats → Pessoas → Ativar perfis** e, em seguida, selecione uma pessoa. Analise o histórico de nomes/nomes de usuário, relações de respostas, atividade, **além de “Também em…” —** outros chats observados e links extraídos, carteiras ou números de telefone. Abra os registros do diário citados.
3. Acompanhe o mesmo ID numérico de usuário do Telegram em outros chats neste espaço de trabalho. Considere um nome correspondente, uma menção à carteira ou um avatar semelhante como uma pista a ser verificada. Um endereço mencionado não comprova a propriedade; um avatar semelhante não comprova que se trate da mesma pessoa.
4. Compare os valores SHA-256 dos anexos preservados entre os registros. Hashes iguais confirmam a identidade dos bytes dos arquivos salvos. Analise os registros das mensagens e dos remetentes associados antes de chegar a uma conclusão sobre quem os compartilhou.

MAPA DO CASO / SIGA AS REFERÊNCIASCaso fictício · não se trata de um gráfico em tempo real

CANAL / ANÚNCIO**Original → destino editado**

Registros n.º 101, n.º 188; Mensagem n.º 84 · remetente não identificado

GRUPO / OPERAÇÕES**O usuário 71001 publica o novo link**

Registro nº 146 · mensagem nº 309 Recibo de arquivo salvo nº 151

BOT / CONVERSA SOBRE PEDIDOS**Um botão direciona para esse destino**

Registro nº 173 · mensagem nº 12 Metadados do botão “Retornar”

PRIVADO / ACOMPANHAMENTO**O usuário 71001 repete o destino**

Registro nº 205 · mensagem nº 922 Recibo do arquivo salvo nº 209

Quatro conversas trazem observações diferentes. Siga os registros de origem para cada conexão; não atribua a postagem do canal ao usuário 71001 sem um remetente identificado.

Os IDs numéricos e as referências dos registros são fictícios para este guia prático. Este mapa explica o fluxo de trabalho de um analista utilizando pesquisa, perfis e análise de registros; o aplicativo não gera um gráfico global de investigação.

| Conexão | Observação complementar | Conclusão a ser mantida |
| --- | --- | --- |
| A mesma conta do Telegram | ID de usuário 71001 no grupo #146 e no chat privado #205 | O mesmo ID de remetente fornecido foi publicado em ambos os chats. A identidade no mundo real continua sendo uma questão à parte. |
| Destino repetido | `pay.example.invalid/new` no #146, metadados do botão #173, postagem editada #188 e #205 | O mesmo destino aparece em quatro contextos observados. Isso, por si só, não determina quem o controla. |
| Mesmos bytes do arquivo | Valores SHA-256 idênticos nos recibos de mídia concluídos nº 151 e nº 209 | Os dois anexos preservados são idênticos em termos de bytes. Os nomes dos arquivos ou as miniaturas, por si só, não seriam suficientes para comprovar isso. |

Os perfis de pessoas abrangem autores com mensagens salvas naquele chat e os relacionam a outros chats no *mesmo diário do espaço de trabalho*. Eles não constituem um diretório completo de membros. Os hashes dos avatares provêm de um cache local separado; as citações de perfis têm um limite configurável em **Parâmetros → Registros citados por fato**.

## 5. Reconstruir a sequência e assinalar as lacunas

Na seção **“Chats”**, examine as versões salvas e seus links **“Registro do Diário nº…”** Na seção **“Diário**”, utilize **“Todas as fontes”,** além de **“Edições”**, **“Exclusões”** e **“Cobertura**”. Elabore uma linha do tempo do caso utilizando tanto a data fornecida pelo Telegram quanto a hora de observação do coletor.

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

A sequência do registro segue a ordem de recebimento, não necessariamente as ações originais no Telegram. Um instantâneo mais antigo do histórico pode aparecer após uma mensagem em tempo real mais recente. Mantenha distintas as observações em tempo real, os instantâneos, as mensagens recuperadas, os avisos de exclusão e as mensagens “ausentes na verificação posterior”. Adicione um intervalo explícito de dados desconhecidos sempre que a cobertura apresentar uma lacuna; um instantâneo posterior não apaga essa lacuna.

## 6. Estender o caso a outras contas de coleta

Adicione um espaço de trabalho para cada conta distinta e repita o inventário de escopo e histórico. Registre a afiliação/função e a impressão digital da chave de assinatura de cada uma. Mantenha os identificadores qualificados por espaço de trabalho e chat: o mesmo número de mensagem não é um identificador global entre contas.

Compare observações relevantes em suas anotações de caso ou ferramentas de análise, mantendo a referência da conta e do registro para cada linha. Atualmente, o TgWitness não oferece uma pesquisa global, linha do tempo unificada, gráfico de pessoas ou arquivo de casos entre espaços de trabalho. A exportação completa de várias contas de um canal ou supergrupo é um recurso separado; não se trata de uma fusão de todos os registros das contas.

Durante trabalhos mais longos, inclua uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/) para manter os limites estabelecidos anteriormente. Utilize o piloto de entrega controlada para qualificar as rotas de captura e a visibilidade das contas.

## 7. Entregar um pacote completo e verificável do caso

Exporte um arquivo ZIP do registro assinado de cada espaço de trabalho. Ele contém o registro completo, independentemente dos filtros de pesquisa do painel. Exporte separadamente os perfis das pessoas relevantes, mantenha cada pacote completo do histórico de bate-papo e preserve as evidências completas dos anexos.

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

Mantenha impressões digitais confiáveis por meio de um canal separado. A partir de uma instalação confiável, verifique cada artefato em relação à identidade de seu próprio espaço de trabalho:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Verifique os resultados reais do verificador, preserve os originais e mantenha o relatório de cobertura, as falhas de aquisição e o registro de transferência juntamente com suas conclusões. A pasta principal do caso e as conclusões do analista são compiladas externamente; os artefatos individuais do TgWitness possuem suas próprias assinaturas.

## Utilize o mesmo método para outras investigações

**Uma contestação de pedido ou pagamento gerada por bot**

**Pergunta:** o que o bot prometeu, qual destino do botão foi fornecido e o que mudou posteriormente?

**Rastreamento:** postagem de entrada no canal → visualização do link do bot salvo → parâmetro de inicialização do bot → mensagens e versões de teclado → qualquer recibo de retorno de chamada emitido pelo painel → acompanhamento em grupo/privado. Correlacione cada destino ao seu registro de origem; mantenha as descrições de perfil e as mídias completas.

**Apresentar:** uma linha do tempo da oferta observada e das respostas, as referências das fontes e as exportações verificadas. Um link de pagamento exibido não constitui prova de que um pagamento tenha ocorrido.

**Mensagens removidas após um incidente entre chats**

**Pergunta:** o que já havia sido observado antes que as mensagens relevantes desaparecessem?

**Rastreamento:** todos os chats afetados → mensagens originais → edições entregues → notificações de exclusão ou resultados posteriores de “ausência na nova verificação” → anexos preservados → cobertura em torno do incidente. Compare as observações de contas independentes com a visibilidade declarada por elas.

**Apresente:** uma sequência de versões preservadas e intervalos desconhecidos explicitados. Não transforme a ausência de uma mensagem no histórico em prova de que uma determinada pessoa a excluiu.

**Um participante altera seus nomes em vários chats**

**Pergunta:** qual atividade observada pertence à mesma conta do Telegram, apesar da mudança de nome?

**Rastreamento:** ID numérico do remetente → histórico de nomes/nomes de usuário salvos → respostas → outros chats no espaço de trabalho → destinos mencionados e arquivos salvos. Verifique os registros de origem para cada conexão identificada; mantenha contas semelhantes separadas.

**Resultado:** uma linha do tempo com as atividades citadas da conta e hipóteses separadas sobre as relações. A semelhança de nomes e o pHash do avatar são pistas, não provas de identidade.
