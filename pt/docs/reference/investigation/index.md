# Modo de investigação

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/investigation/

Investigações completas de contas, abrangendo canais, grupos, conversas privadas e bots, desde a definição do escopo até a elaboração de um dossiê de caso verificado.

Acompanhe um caso em canais, grupos, conversas privadas e bots, desde a aquisição inicial até uma linha do tempo referenciada e uma transferência verificável. A versão interativa do site está disponível em `/docs/cases/`; [instruções para visualização prévia](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Caso prático: uma mudança de destino ao longo de quatro conversas

Um anúncio indica um bot. Um grupo de operações discute um novo destino de pagamento, o teclado do bot o exibe e uma mensagem privada de acompanhamento o repete. O anúncio é então editado e uma mensagem do grupo desaparece.

As perguntas são: o que foi observado antes e depois da alteração, quais contas do Telegram publicaram cada item, onde o destino apareceu, quais bytes do anexo foram preservados e quais intervalos permanecem desconhecidos?

Todos os nomes, IDs, horários e referências do registro neste exemplo são fictícios. O fluxo de trabalho utiliza recursos atuais; o mapa do caso é uma ilustração, não um gráfico automático gerado pelo aplicativo.

Diagrama de fluxo · Canais → Diário do espaço de trabalho; Grupos → Diário do espaço de trabalho; Conversas privadas → Diário do espaço de trabalho; Bots → Diário do espaço de trabalho; Diário do espaço de trabalho → Pesquisar todas as fontes; Diário do espaço de trabalho → Perfis de pessoas com referências aos registros; Diário do espaço de trabalho → Versões salvas e recibos de anexos; Pesquisar todas as fontes → Linha do tempo do analista e registro de fontes; Perfis de pessoas com referências aos registros → Linha do tempo do analista e registro de fontes; Versões salvas e recibos de anexos → Linha do tempo do analista e registro de fontes; Diário do espaço de trabalho → Arquivo ZIP de evidências assinadas; Linha do tempo do analista e registro de fontes → Transferência de casos com artefatos verificados separadamente; Arquivo ZIP de evidências assinadas → Transferência de casos com artefatos verificados separadamente · Canais · Grupos · Conversas privadas · Bots · Diário do espaço detrabalho · Pesquisar todas as fontes · Perfis de pessoas comreferências aos registros · Versões salvas e recibosde anexos · Arquivo ZIP de evidênciasassinadas · Linha do tempo do analistae registro de fontes · Transferência de casos comartefatos verificadosseparadamente

**Diagrama em formato de texto**

1. Canais → Diário do espaço de trabalho
2. Grupos → Diário do espaço de trabalho
3. Conversas privadas → Diário do espaço de trabalho
4. Bots → Diário do espaço de trabalho
5. Diário do espaço de trabalho → Pesquisar todas as fontes
6. Diário do espaço de trabalho → Perfis de pessoas com referências aos registros
7. Diário do espaço de trabalho → Versões salvas e recibos de anexos
8. Pesquisar todas as fontes → Linha do tempo do analista e registro de fontes
9. Perfis de pessoas com referências aos registros → Linha do tempo do analista e registro de fontes
10. Versões salvas e recibos de anexos → Linha do tempo do analista e registro de fontes
11. Diário do espaço de trabalho → Arquivo ZIP de evidências assinadas
12. Linha do tempo do analista e registro de fontes → Transferência de casos com artefatos verificados separadamente
13. Arquivo ZIP de evidências assinadas → Transferência de casos com artefatos verificados separadamente

## 1. Defina o caso e reúna todo o relato

1. Conecte a conta de coleta em seu próprio espaço de trabalho. Em notas externas do caso, registre a referência do caso, o ID da conta, o espaço de trabalho, o início da observação e a impressão digital confiável da chave de assinatura.
2. **Fontes** abertas **→ Escopo de observação → Modo de investigação**. A predefinição seleciona **“Conta inteira”**, canais/grupos/conversas privadas/bots, ações próprias, perfis de fontes e as últimas 200 mensagens visíveis para fontes recém-descobertas. Analise-o, pressione **“Salvar escopo**” e conclua a confirmação do escopo.
3. **Carregue as conversas** e compare as fontes com a lista de diálogos da conta. Verifique as exclusões. **Parâmetros →** O número padrão de **bate-papos lidos da lista da conta** é 1.000 e permite até 20.000. As fontes que excederem o limite da lista são adicionadas quando se tornam ativas. Registre o que foi efetivamente enumerado.
4. Nas **configurações de gravação**, selecione **“Todas as atividades visíveis”** e salve as configurações de monitoramento. Verifique os tipos e limites de anexos, bem como o espaço livre em disco.
5. Inicie a observação. Valide uma nova mensagem controlada, uma edição e uma exclusão e, em seguida, registre as referências do teste e quaisquer falhas.

O escopo de conta completa registra as atividades visíveis na conta, de acordo com as configurações salvas. A ferramenta não acessa chats secretos nem entra automaticamente em todos os grupos vinculados. Além disso, não recupera todas as conversas existentes. Consulte [o escopo de coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account).

## 2. Inventariar todas as fontes e obter o contexto histórico

Mantenha um registro de fontes com uma linha por conversa:

| Campo | Registrar |
| --- | --- |
| Identidade | Espaço de trabalho, ID da conta, ID numérico do chat, título e tipo |
| Visibilidade | Afiliação/função, acesso confirmado ou não confirmado, exclusões |
| Captura em tempo real | Data de início, tipos de eventos selecionados e alterações posteriores na política |
| Histórico do registro | Instantâneo solicitado/concluído, limite, tempo e referências de registro |
| Histórico completo | Nome do arquivo de exportação assinado por conversa, limites e conclusão/falha |
| Anexos | Recibos de mídia concluídos, hashes, tamanhos e resultados ignorados/com falha |
| Cobertura | Interrupções de serviço, captação incompleta, FloodWait, mensagens indisponíveis e outras lacunas |

Utilize o método de aquisição adequado para cada fonte:

- **A função “Carregar histórico completo** em **Fontes”** (`main` atual) carrega as mensagens anteriores disponíveis das fontes habilitadas no diário da área de trabalho. Ela oferece suporte à pausa/retomada e a um relatório de progresso assinado. Consulte [aquisição de histórico](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/).
- **O instantâneo do histórico** salva as mensagens visíveis mais recentes no diário de observação. Seu limite máximo padrão é 500; **em Parâmetros → Maior instantâneo do histórico,** é possível aumentar esse número para 10.000. Trata-se de observações do histórico atual, e não de edições reconstruídas.
- **Exportação completa do chat → Exportar chat completo**, ou **Chats → Exportar chat**, extrai o histórico atualmente visível de um chat para um pacote separado assinado `chat.json` / `chat.html`. Repita o procedimento para as fontes do caso e mantenha cada resultado.
- **Quando um novo chat ou bot aparece,** é possível salvar seu perfil e até 1.000 mensagens recentes; o modo de investigação seleciona 200. Os chats existentes não recebem essa captura retroativamente quando o modo é ativado.
- **O download de anexos visíveis** preserva os bytes de acordo com a política configurada. É necessário um recibo `media.saved` preenchido com SHA-256 e contagem de bytes. Uma tarefa na fila, uma miniatura ou um nome de arquivo não constituem o anexo preservado.

A exportação completa de um chat **não** preenche o registro nem os perfis das pessoas com todas as suas mensagens. Use **“Carregar histórico completo”** ou “instantâneos limitados do registro” para o histórico que você precisa analisar dentro do TgWitness. Verifique a lista de fontes ativadas antes de iniciar uma execução do histórico. Nenhuma das duas opções recupera material que o Telegram não retorna mais.

## 3. Preservar a evolução do caso e as interações deliberadas

Marque os chats de casos ativos como fontes prioritárias. Revise os intervalos de verificação, a atualização contínua e os resultados de mídia. Mantenha o coletor em funcionamento enquanto utiliza a conta. Utilize **Chats → Perfil → Salvar perfil agora** para reter metadados da fonte, tais como descrições e comandos de bot. Isso é distinto dos perfis de pessoas derivados de mensagens salvas.

Quando o caso envolver acompanhar uma fonte ou interagir com um bot:

1. **Abrir link do Telegram → Salvar pré-visualização** registra o link fornecido e a pré-visualização exibida antes de uma ação.
2. **A função “Join / open and observe”** executa o “join/open” e envia o parâmetro de inicialização de um bot, quando fornecido. Uma solicitação de adesão aguardando aprovação é registrada como pendente.
3. Respostas de texto emitidas pelo painel e cliques em botões suportados mantêm `interaction.requested` e `interaction.result`. Os recibos de retorno de chamada podem manter o texto do pop-up exibido, o estado do alerta e a URL.

Essas são ações reais da conta. Os cliques de retorno em outro aplicativo do Telegram não são visíveis ao coletor, embora as mensagens ou edições resultantes possam ser. O minicliente não executa fluxos de trabalho relacionados a aplicativos web, pagamentos, telefone ou localização. Para obter informações sobre o comportamento exato, consulte [as interações do painel](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/#act-from-the-panel).

## 4. Relacione observações entre conversas

No **“Journal”**, selecione **“Todas as fontes”** e pesquise o conteúdo registrado. Abra os registros correspondentes e anote o espaço de trabalho, o chat, o ID da mensagem, a sequência e o hash do registro.

Em um chat relevante, abra **Pessoas → Ativar perfis** e examine uma pessoa:

- Nomes/nomes de usuário observados ao longo do tempo e o ID numérico do Telegram.
- Relações de resposta com referências aos registros de origem.
- **Também em…** outros chats neste diário do espaço de trabalho onde esse ID escreveu.
- Atividades, edições/exclusões e carteiras, telefones, nomes de usuário e links mencionados.
- Metadados de avatares salvos e avatares semelhantes armazenados em cache, com suas origens distintas.

Abra os registros citados antes de utilizar um perfil derivado em uma conclusão. Os perfis abrangem pessoas com mensagens salvas, e não todos os membros do grupo. **Parâmetros → Registros citados por fato** limitam a lista de referências, e não a contagem de atividades subjacentes. Menções e semelhança de avatares são pistas; elas não estabelecem propriedade nem identidade.

No exemplo prático:

| Link | Registros | Observação fundamentada |
| --- | --- | --- |
| A mesma conta de remetente | Grupo n.º 146 e acompanhamento privado n.º 205 | Ambos fornecem o ID do remetente do Telegram 71001 |
| Mesmo destinatário | #146, teclado do bot #173, edição de canal #188, mensagem privada #205 | Todos contêm `pay.example.invalid/new`; a propriedade/controle não está estabelecida |
| O mesmo arquivo salvo | Recibos de mídia concluídos n.º 151 e n.º 209 | Os valores SHA-256 completos coincidem para os bytes preservados |
| Atribuição do canal | #101 e #188 | Não atribua uma publicação do canal ao usuário 71001 sem que o remetente esteja identificado |

Compare os hashes dos anexos e as referências das mensagens a eles associadas. Arquivos idênticos não indicam um criador, remetente ou operador comum. Nomes iguais e avatares semelhantes, por si só, não permitem associar dois IDs do Telegram a uma única pessoa.

## 5. Criar a linha do tempo entre conversas

Utilize as versões salvas nos **Chats** e seus links **de registro no Diário #…** No **Diário**, combine **todas as fontes** com **as edições**, **exclusões** e **cobertura**. Mantenha tanto o `source_at`, quando fornecido, quanto o `observed_at`.

| Tempo de observação ilustrativo | Referência | Observação |
| --- | --- | --- |
| 09:00 | Canal #101 | Destino original capturado |
| 09:12 | Grupo n.º 146; mídia n.º 151 | Novo destino publicado; download do arquivo concluído |
| 09:16 | Bot nº 173 | O teclado aponta para o novo destino |
| 09:20 | Canal #188 | Anúncio editado; ambas as versões salvas permanecem |
| 09:24 | Privado #205; mídia #209 | O mesmo ID de remetente repete o destino; os mesmos bytes do arquivo são preservados |
| 09:28 | Grupo nº 231 | Notificação de exclusão recebida; autor da exclusão e horário exato da exclusão desconhecidos |

Outros registros ocorrem entre essas referências de exemplo. Os números de sequência ordenam as observações; instantâneos do histórico podem conter datas de origem mais antigas e chegar posteriormente aos eventos em tempo real. Distinga entre instantâneos, mensagens recuperadas, notificações de exclusão e resultados de “ausência na verificação posterior”. Marque lacunas de cobertura como intervalos desconhecidos. A aquisição posterior do histórico não estabelece retroativamente uma observação ininterrupta.

## 6. Adicionar perspectivas de contas sem perder sua origem

Utilize um espaço de trabalho separado para cada conta distinta e repita seu inventário. Mantenha o ID da conta, a função, a impressão digital da chave de assinatura e as referências de origem em cada comparação. Os números das mensagens não são identificadores globais entre bate-papos/contas.

A correlação entre espaços de trabalho é realizada em notas de caso externas ou em ferramentas de análise. Atualmente, o TgWitness não dispõe de pesquisa global entre espaços de trabalho, linha do tempo unificada, gráfico de investigação ou arquivo de casos combinado. A exportação para várias contas de **um** canal/supergrupo é uma operação distinta, não uma fusão dos registros das contas.

Para trabalhos mais extensos, mantenha os limites com uma [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/). Utilize verificações de entrega controladas para validar o caminho de captura e a visibilidade de cada conta.

## 7. Reunir e verificar a transferência do caso

Mantenha esses elementos reunidos em um diretório de casos organizado por um analista:

| Material | Objetivo |
| --- | --- |
| Notas de caso e registro de fontes | Questões, política de coleta, acesso/função, conclusões, explicações alternativas e lacunas |
| Linha do tempo | Referências tanto às datas quanto ao espaço de trabalho/bate-papo/mensagem/sequência para cada entrada |
| Arquivo ZIP de evidências assinadas por espaço de trabalho | Registro completo, manifesto e mídia preservada incluída; os filtros do painel não restringem a exportação do registro |
| Arquivos de perfis de pessoas assinados separadamente | Referências derivadas verificadas em relação às evidências correspondentes do espaço de trabalho |
| Exportações completas e assinadas de conversas | Aquisição do histórico visível atual, separada do registro de observação |
| Impressões digitais confiáveis e pontos de verificação anteriores | Identidade-chave e limites do registro mantido |
| Artefatos do Witness, se configurados | Registro separado, postagens assinadas e impressão digital da testemunha |
| Resultados da verificação e hashes dos arquivos entregues | O que foi verificado, quais bytes foram transferidos e para quem |

A partir de uma instalação confiável, com nomes de arquivos e a impressão digital real de cada espaço de trabalho:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conserve os resultados reais da verificação e os artefatos originais. O diretório de casos de nível superior, o registro de fontes e as conclusões dos analistas são mantidos externamente; cada artefato do TgWitness possui sua própria assinatura e procedimento de verificação.

## Adapte a investigação

| Caso | Rastrear | Entregar |
| --- | --- | --- |
| Contestação de pedidos/pagamentos por meio de bot | Anúncio de entrada → visualização do link salvo → parâmetro de inicialização do bot → versões para mensagens e teclado → recibos de retorno de chamada do painel → acompanhamento de conversas privadas/em grupo | Cronologia observada de ofertas/respostas e fontes verificadas; um link de pagamento, por si só, não comprova a realização de um pagamento |
| Mensagens removidas após um incidente | Todos os chats afetados → originais/edições salvas → resultados de exclusão ou ausência na verificação posterior → mídia preservada → cobertura e outras perspectivas da conta | Versões preservadas e intervalos desconhecidos explicitados; nenhum agente de exclusão inventado |
| Um participante altera seus nomes nos diferentes chats | ID numérico do remetente → histórico de nomes/nomes de usuário → respostas → outros chats observados → destinos/arquivos citados | Uma linha do tempo da atividade de uma conta do Telegram citada, com hipóteses sobre identidade e relações no mundo real mantidas separadas |

[Referência da coleção](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/) · [Verificação de perfis de pessoas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#people-profiles) · [Transferência de evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#investigation-handoff) · [Validação concluída](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/)
