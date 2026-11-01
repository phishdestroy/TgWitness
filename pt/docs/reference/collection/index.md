# Como funciona a coleta

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/

Escopo de observação, atualizações em tempo real, novas verificações, anexos, ações próprias e o que significa uma lacuna, registro por registro.

O TgWitness registra o que uma conta conectada do Telegram observa. O registro preserva essas observações, sua sequência e o contexto fornecido com elas. Ele não infere ações não observadas a partir de uma mensagem ausente ou do fato de uma conta estar conectada.

## Do login ao registro

Diagrama de fluxo · Autorizar uma conta de usuário → Selecione grupos e canais acessíveis; Selecione grupos e canais acessíveis → Salvar configurações de eventos e anexos; Salvar configurações de eventos e anexos → Iniciar observação; Iniciar observação → Receba atualizações do cliente ativo; Receba atualizações do cliente ativo → Aplique a política de fontes e eventos; Aplique a política de fontes e eventos → Anexar uma observação assinada; Anexar uma observação assinada → Revisar ou exportar o registro; Anexar uma observação assinada → Processar qualquer anexo em fila; Processar qualquer anexo em fila → Anexe o resultado do download · Autorizar uma conta deusuário · Selecione grupos ecanais acessíveis · Salvar configuraçõesde eventos e anexos · Iniciar observação · Receba atualizações docliente ativo · Aplique a política defontes e eventos · Anexar uma observaçãoassinada · Revisar ou exportar oregistro · Processar qualqueranexo em fila · Anexe o resultado dodownload

**Diagrama em formato de texto**

1. Autorizar uma conta de usuário → Selecione grupos e canais acessíveis
2. Selecione grupos e canais acessíveis → Salvar configurações de eventos e anexos
3. Salvar configurações de eventos e anexos → Iniciar observação
4. Iniciar observação → Receba atualizações do cliente ativo
5. Receba atualizações do cliente ativo → Aplique a política de fontes e eventos
6. Aplique a política de fontes e eventos → Anexar uma observação assinada
7. Anexar uma observação assinada → Revisar ou exportar o registro
8. Anexar uma observação assinada → Processar qualquer anexo em fila
9. Processar qualquer anexo em fila → Anexe o resultado do download

Autorização, acesso a uma fonte, um coletor em funcionamento e entrega completa são questões distintas. Um login bem-sucedido não concede acesso a todos os grupos. Um transporte conectado não garante que todas as atualizações relevantes tenham chegado.

## Âmbito de observação: conversas selecionadas, uma pasta ou toda a conta

Fontes → **O escopo de observação** determina quais conversas um espaço de trabalho registra.

| Modo | Registros | Novas conversas |
| --- | --- | --- |
| Conversas selecionadas (padrão) | Apenas os chats que o senhor adicionar manualmente | Nunca adicionado automaticamente |
| Pasta do Telegram | Conversas em uma das pastas da conta: conversas incluídas por nome, além das categorias da pasta (contatos, não contatos, grupos, canais, bots), excluindo as conversas excluídas e, se a pasta assim o indicar, as conversas arquivadas | As conversas correspondentes são adicionadas assim que se tornam ativas; as conversas que o senhor adicionar à pasta no Telegram são capturadas em até uma hora |
| Conto completo | Todas as conversas que a conta recebe | Cada novo chat, grupo, chat privado ou bot é adicionado no momento em que sua primeira atualização é recebida |

- **Os tipos de fonte** (canais, grupos, conversas privadas, bots) restringem os modos de pasta e de conta inteira. As conversas selecionadas podem ser de qualquer tipo, incluindo conversas privadas e bots.
- **As conversas excluídas** nunca são registradas, em nenhum modo. Nos modos “Pasta” e “Conta inteira”, as opções *“Excluir”* e *“Remover”* em uma fonte a colocam nesta lista, de modo que o escopo não a adiciona novamente. Selecionar o chat novamente manualmente (em “Fontes” ou em “Chats”) o retira da lista. A lista armazena até 5.000 chats; além desse limite, *a opção “Remover”* é recusada e o chat pode ser pausado em vez disso.
- **Ações próprias** (ativadas por padrão): mensagens enviadas por esta conta, suas edições e seus toques no botão do teclado de resposta. Quando desativado, as mensagens enviadas e as edições são ignoradas.
- A mudança para uma pasta ou para toda a conta requer confirmação: esses modos registram conversas privadas e mensagens de terceiros e devem ser utilizados exclusivamente em uma conta dedicada. A confirmação e todas as alterações de escopo são registros assinados pelo `scope.changed`.
- As conversas adicionadas pelo escopo aparecem como fontes marcadas *como “auto”*, registradas como `scope.applied` (no início e a cada hora) ou `source.discovered` (uma nova conversa durante a observação). Ao voltar para as conversas selecionadas, todas as fontes adicionadas automaticamente são pausadas.

O que esses modos não podem fazer:

- **As conversas secretas** são criptografadas de ponta a ponta entre dois dispositivos e nunca chegam ao TgWitness, em nenhum modo.
- **Nada é registrado enquanto o TgWitness não estiver em execução.** Após uma reinicialização, ele solicita ao Telegram as atualizações perdidas e verifica novamente as conversas, mas o Telegram não retorna todas as informações após longas interrupções de serviço. Os relatórios e o `verify.py` mostram esses períodos como lacunas (consulte [a cobertura](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)).
- Apenas as primeiras 1.000 conversas são listadas inicialmente (o limite está definido em **“Parâmetros”**); as conversas mais antigas são adicionadas assim que se tornarem ativas novamente. O histórico anterior de uma conversa adicionada não é recuperado — faça um instantâneo do histórico ou uma exportação completa da conversa quando necessário.
- Condições de pastas que mudam constantemente (silenciadas, lidas) não são aplicadas: tais conversas continuam sendo monitoradas.
- **Os botões do bot embutidos (callback)** pressionados em outro aplicativo são invisíveis para uma segunda sessão; a resposta ou edição do bot é registrada. As teclas pressionadas no teclado de resposta chegam como mensagens enviadas e são identificadas como `button_press`.
- Mais conversas significam mais solicitações. O Telegram restringe contas cujo volume considera excessivo, o que constitui mais um motivo para utilizar contas dedicadas.

## Escopo e seleção de eventos

Cada espaço de trabalho possui suas próprias fontes. O TgWitness não participa de grupos, não aceita convites nem lista todos os membros automaticamente. As fontes já devem estar acessíveis à conta. Ao iniciar, o coletor verifica as fontes selecionadas em relação às conversas visíveis da conta; as primeiras 1.000 conversas são inspecionadas, a menos que **a opção Parâmetros → Conversas lidas da lista da conta** indique o contrário. Uma fonte ausente é marcada como **“acesso não confirmado”**, não se presumindo que tenha removido o usuário.

| Contexto | Coleta | Efeito quando desativado |
| --- | --- | --- |
| Novas mensagens | Mensagens entregues normalmente | Edições ou exclusões posteriores podem não ter texto capturado anteriormente para comparação. |
| Edições | Versões editadas das mensagens fornecidas | Alterações intermediárias não são reconstruídas posteriormente. |
| Exclusões | Notificações de exclusão com escopo definido e notificações sem escopo definido no nível da conta | Notificações de exclusão não são adicionadas ao registro. |
| Reações | Instantâneos de reações fornecidos | Não são adicionadas atualizações separadas sobre reações. |
| Associação | Envio de mensagens de serviço aos membros e atualizações aos participantes | Essas observações sobre a adesão não foram incluídas. |

As configurações se aplicam a todas as fontes selecionadas na área de trabalho. Salve o formulário para aplicar as alterações; as alterações são registradas com valores assinados de “antes” e “depois”. Desativar uma categoria não remove registros anteriores. Reativá-la não repõe as atualizações perdidas.

Registros operacionais e outros eventos de serviço do grupo permanecem separados dessas configurações. Mensagens de serviço relacionadas à adesão podem criar registros de mensagens quando a adesão estiver ativada, mesmo que a captura padrão de novas mensagens esteja desativada. Objetos do Telegram capturados mantêm metadados incorporados; uma configuração não constitui uma regra de supressão.

**As exclusões em conversas privadas e grupos comuns** são registradas como IDs de mensagem sem uma conversa associada. Essas conversas compartilham uma sequência de IDs de mensagem válida para toda a conta; portanto, quando uma mensagem com esse ID foi salva anteriormente, sua conversa é identificada: a exclusão é registrada nessa conversa, com o `chat_resolution` explicando como. Os IDs nunca salvos permanecem como uma **exclusão sem escopo,** com uma fonte desconhecida explícita; o coletor não faz suposições. O Telegram nunca informa quem excluiu uma mensagem; quando a mensagem excluída foi enviada por esta conta, o registro indica isso (`deleted_message_was_outgoing`) sem nomear o autor da exclusão.

## Ações próprias

As mensagens enviadas pela conta observada são identificadas como `outgoing`. Uma edição de uma mensagem enviada indica que, em chats privados e grupos, apenas seu autor pode editá-la, enquanto as postagens em canais podem ser editadas por outros administradores. Quando uma mensagem enviada repete o texto de um botão do teclado de respostas mais recente salvo naquele chat, ela recebe a marcação `button_press`, acompanhada de um link para o registro do teclado.

A exclusão de ações próprias também se aplica a novas verificações em segundo plano e ao histórico automático de novas conversas. As mensagens enviadas que foram ignoradas avançam a posição da nova verificação, de modo que não possam bloquear mensagens recebidas posteriormente. Ações explícitas no painel e instantâneos do histórico solicitados manualmente permanecem registrados.

## Modo de investigação: ingressar em grupos e interagir com bots

**Fontes → Escopo de observação → O modo de investigação** prepara o escopo para uma conta dedicada que participa de chats em grupo, inicia bots e envia mensagens para eles: toda a conta, todos os tipos de fonte, ações próprias e, para cada chat ou bot que aparecer, seu perfil e suas últimas 200 mensagens visíveis. Revise o formulário e clique em **“Salvar escopo”**; a mudança para toda a conta solicita a confirmação habitual.

- **Botões.** Os botões abaixo de uma mensagem são mantidos junto a ela e exibidos em **“Chats**”: links, aplicativos web, links de login, textos para copiar, dados de retorno de chamada, consultas embutidas, solicitações de número de telefone ou localização. Os links são exibidos como texto e nunca são abertos pelo painel. Quando um bot altera apenas os botões (um novo link de pagamento), isso constitui uma nova versão da mensagem, tanto em atualizações em tempo real quanto em novas verificações.
- **Novos chats e bots.** Nos modos “pasta” e “conta inteira”, **quando um novo chat ou bot aparece**, ele é salvo imediatamente após seu surgimento:

  - seu perfil como um registro `source.profile`: descrição do bot e comandos, o texto “Sobre” de um usuário, grupo ou canal, membros, chat vinculado e link de convite quando o Telegram fornecer um;
  - suas mensagens visíveis mais recentes (até 1.000) como um instantâneo do histórico marcado como `new_chat`: as mensagens anteriores de um chat em grupo ao qual acabou de entrar, ou o que um bot disse antes que a observação percebesse o chat. Mensagens já salvas em tempo real não são repetidas.

  As conversas que já constam da lista quando o modo é ativado são adicionadas sem capturas de tela. Um FloodWait interrompe esse processo, que é retomado posteriormente; as falhas são registradas e a gravação em tempo real da conversa continua. - **Perfis sob solicitação. Conversas → Perfil → Salvar perfil agora** salva o perfil atual de qualquer fonte; o mais recente é exibido acima das mensagens. - **Não visível.** Botões embutidos (callback) pressionados em outro aplicativo do Telegram, o pop-up ou o link com o qual um bot responde a tal pressão, bem como links de convite usados em outro aplicativo, não chegam ao TgWitness. O que o bot envia ou edita posteriormente é registrado.

### Ato do painel

**A seção “Bate-papos”** agora inclui um minicliente que utiliza a conta do Telegram do espaço de trabalho selecionado:

- Escreva uma mensagem em texto simples ou selecione **“Responder”** em uma mensagem salva. A mensagem de saída gerada é registrada mesmo quando o escopo exclui atualizações de saída.
- Pressione **o botão “Press”** abaixo de um botão de retorno de chamada ou de texto atual. O servidor busca a mensagem novamente e recusa a ação se o conteúdo digitado diferir da versão salva. Os recibos de retorno de chamada mantêm o texto do pop-up do Telegram, o sinalizador de alerta e a URL; a resposta também é exibida abaixo da conversa. As URLs permanecem como texto selecionável e não são abertas automaticamente.
- Expanda **o link “Abrir no Telegram**”, insira `@username`, um link público `https://t.me/name`, `https://t.me/+invite` / `joinchat/invite` ou um link de bot com `?start=parameter` e pressione **“Salvar pré-visualização**”. O link original e a pré-visualização do Telegram são assinados antes da adesão. **Ao ingressar/abrir e observar**, o sistema ingressa no grupo/canal ou abre o usuário/bot, adiciona o chat como uma fonte habilitada e envia `/start` a um bot, incluindo seu parâmetro de inicialização. Uma solicitação de adesão aguardando aprovação do administrador é registrada como pendente, e não como adesão.

Ative a opção **“Iniciar observação”** para capturar respostas recebidas em tempo real. As ações do painel funcionam enquanto a observação estiver pausada, mas, nesse caso, apenas as respostas diretas têm garantia de serem salvas. Fontes recém-adicionadas utilizam a configuração do perfil/histórico definido quando a observação estiver em andamento. Quando uma fonte estiver pausada, ative-a em **“Fontes”** antes de enviar ou pressionar seus botões.

`interaction.preview`, `interaction.requested` e `interaction.result` são eventos comuns assinados do diário incluídos nas exportações de evidências. As solicitações identificam a conta, a mensagem/botão ou o registro de visualização e se a observação estava em execução. Os recibos distinguem entre sucesso, rejeição, aprovação pendente e um resultado desconhecido. Uma solicitação interrompida pode ter chegado ao Telegram: verifique o chat antes de iniciar uma nova ação. Reutilizar um ID de solicitação recupera seu recibo salvo sem repetir a ação, inclusive após a reinicialização. O painel retém o ID após uma resposta ambígua para a mesma ação durante a sessão da página atual. Ele também retém esse ID quando a atualização da visualização falha após uma ação bem-sucedida: o recibo permanece visível, e clicar novamente o recupera. Os RPCs de callback e de adesão têm uma única tentativa; as leituras com possibilidade de repetição mantêm sua política de repetição configurada. A troca de chats limpa imediatamente o rascunho e o destinatário da resposta e desativa o envio até que a nova conversa seja carregada.

Este minicliente lida com texto e botões de retorno de chamada. Aplicativos da web, solicitações de login/telefone/localização, pagamentos, consultas embutidas e anexos ainda exigem um cliente do Telegram; os metadados dos botões salvos permanecem visíveis. Os novos controles utilizam texto em inglês.

## Níveis de verificação

As novas verificações solicitam novamente ao Telegram as mensagens perdidas, as edições e as mensagens que ele não retorna mais. As fontes marcadas com um asterisco são fontes **prioritárias**, verificadas novamente a cada 15 minutos por padrão; todas as outras fontes, a cada 6 horas. Os chats selecionados começam como fontes prioritárias, enquanto os chats adicionados por meio de uma pasta ou da conta inteira são considerados fontes regulares. No máximo, 30 fontes são verificadas novamente por ciclo e o restante aguarda até o minuto seguinte; após uma reconexão, as fontes prioritárias são verificadas primeiro. Ambos os intervalos são definidos em Fontes → Configurações de gravação → Verificação adicional (0 desativa um nível) e são registrados como `recheck.changed`.

As mensagens perdidas são recuperadas a partir do ponto em que a verificação anterior foi interrompida, até no máximo o número definido em **Parâmetros → novas mensagens por nova verificação** (1.000 por padrão) por verificação. Após uma longa interrupção, a reverificação, portanto, preenche toda a lacuna, mesmo quando mensagens em tempo real mais recentes do que a lacuna foram salvas primeiro. Um chat que ainda está em processo de atualização é verificado novamente no minuto seguinte, em vez de aguardar seu intervalo de nível; `recheck.completed` exibe `continues_after` até que a verificação seja concluída.

As comparações incluem o texto das mensagens, entidades, teclados (incluindo remoção) e conteúdo/identidade dos anexos. A simples alteração de hashes de acesso a arquivos ou de referências a arquivos não constitui uma edição, nem o que o Telegram preenche automaticamente: o carregamento de uma pré-visualização de link, visualizações de stories, mídias pagas desbloqueadas por esta conta, o recebimento de uma fatura. Cada versão salva em “Chats” possui um link para seu registro completo no diário, incluindo metadados de mídia.

## Histórico de mensagens e atribuição

Suponha que o coletor observe “Reunião às 10h”, depois veja “Reunião às 11h” e, em seguida, receba um aviso de exclusão. Ele anexa três observações distintas. O texto original permanece, a edição é uma versão separada e o aviso registra que foi observada uma exclusão.

Caso a coleta tenha começado após o desaparecimento da primeira versão, esse texto não estará disponível. Caso tenham ocorrido várias edições enquanto o processo estava offline, apenas as versões observadas posteriormente podem ser salvas. Um aviso de exclusão não permite recuperar conteúdo que nunca foi capturado.

O remetente da mensagem não é automaticamente o editor. O Telegram geralmente não fornece a identidade da pessoa que excluiu uma mensagem nem a hora exata da exclusão. Atores desconhecidos permanecem desconhecidos. Os instantâneos de reações e as atualizações dos participantes contêm apenas as contagens e as identidades que o Telegram torna visíveis para a conta.

Os números de sequência indicam a ordem de observação. O carimbo de data e hora UTC do coletor corresponde ao seu relógio local; um carimbo de data e hora da fonte do Telegram é armazenado separadamente, quando fornecido. Nenhum dos dois é um carimbo de data e hora independente e confiável.

## Instantâneos do histórico

Uma captura instantânea solicita as mensagens visíveis mais recentes de uma fonte habilitada, até 500 por solicitação. Os resultados são rotulados como observações do histórico. Eles podem se sobrepor à captura em tempo real, e as observações repetidas são mantidas como registros separados.

Os instantâneos seguem a política de anexos, mas permanecem separados das alternâncias de eventos em tempo real. Eles não reconstroem mensagens excluídas nem versões intermediárias perdidas. É possível solicitar um instantâneo enquanto o sistema estiver em pausa; quaisquer anexos na fila aguardam até que a observação comece e o processo de download seja executado.

## Tratamento de anexos

O download de anexos está ativado por padrão e é pausado quando resta menos de 1 GiB de espaço livre em disco. O coletor realiza o registro das mensagens e a tarefa de download simultaneamente. A tarefa mantém o descritor de mídia original e a política de tamanho, de modo que um anexo editado posteriormente não seja substituído silenciosamente.

Os downloads são executados após a captura da mensagem. Um download concluído cria um registro `media.saved` com seu SHA-256 e contagem de bytes. Tarefas ignoradas, com falha, repetidas e interrompidas apresentam resultados distintos. Uma tarefa na fila não constitui prova de que o arquivo foi preservado. O arquivo concluído também deve corresponder à contagem de bytes no descritor do anexo original observado. Uma resposta curta ou inesperadamente longa não é registrada como mídia preservada.

Os limites são definidos **por tipo**: fotos, vídeos, GIFs e animações, mensagens de vídeo circulares, mensagens de voz, música e áudio, adesivos e arquivos. Cada tipo pode ser desativado e possui seu próprio limite de tamanho, variando de 1 a 2.000 MiB; novos espaços de trabalho começam com 20 MiB para fotos, 100 MiB para vídeos, 50 MiB para arquivos, áudio e vídeos circulares, 20 MiB para mensagens de voz e GIFs e 5 MiB para adesivos. Novos espaços de trabalho mantêm GIFs e adesivos desativados até que sejam ativados. Espaços de trabalho com políticas salvas antes da implementação dos limites por tipo mantêm todos os tipos ativados e conservam seu único limite para cada tipo. *O tamanho máximo de arquivo* define todos os tipos de uma só vez. Um tipo desativado gera um registro `media.skipped`; arquivos de tamanho desconhecido ou acima do limite não são baixados. Arquivos grandes recebem tempo extra de download com base em seu tamanho e em uma velocidade de referência de 256 KiB/s. As tarefas sobrevivem à reinicialização, mas referências expiradas, acesso perdido ou arquivos excluídos ainda podem impedir a recuperação. Tarefas em espera mantêm o limite salvo com elas, de modo que um aumento no limite se aplica apenas a novos arquivos. Desativar um tipo ou reduzir seu limite também ignora os arquivos em espera que ele exclui, cada um com um registro `media.skipped`; desativar os downloads pausa a fila até que sejam reativados.

## Pausar, bloquear, desconectar e reiniciar

| Ação ou condição | Efeito |
| --- | --- |
| Alternar entre áreas de trabalho | Altera a exibição do painel; os demais coletores mantêm seu estado. |
| Bloqueie o painel ou feche uma aba | Mantém o servidor e a observação em funcionamento. |
| Observação sobre a pausa | Interrompe esse coletor e preserva o trabalho de anexos em fila. |
| Desativar uma fonte | Interrompe futuras capturas programadas; as tarefas de mídia agendadas para essa função ficam em espera enquanto ela estiver desativada. |
| Remover uma fonte | A ferramenta desconsidera-a como fonte e exclui os perfis de seus usuários; os registros já salvos permanecem no diário de gravação exclusiva. Seus anexos ainda pendentes são registrados como falhados (`source_removed`). Nos modos “pasta” e “conta inteira”, ela também é excluída. |
| Alterar a rota de conexão | Exige uma pausa, encerra clientes antigos e cancela logins inacabados. |
| Encerre o processo do Python | Interrompe todas as áreas de trabalho; nenhuma observação é feita enquanto estiver offline. |
| Reinício após observação ativa | Tenta retomar o escopo salvo utilizando a sessão salva. Uma pausa manual cancela essa intenção. |

O coletor registra desconexões detectadas, novas tentativas, erros, inicializações/interrupções e sinais de vida. Interrupções breves podem passar despercebidas pelas verificações periódicas de conectividade. Após uma reinicialização, as atualizações perdidas são solicitadas a partir da posição de atualização salva e os chats observados são verificados novamente periodicamente; consulte [o formato de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#durable-collection-and-process-receipts-02). Um instantâneo fornece contexto; ele não prova que uma lacuna foi reparada.

## Isolamento e verificação de contas

Cada espaço de trabalho possui seu próprio diário, autorização, chave de assinatura, política e fila. Apenas seu cliente ativo pode contribuir com observações em tempo real. Clientes rejeitados, pendentes, substituídos e em teste de conexão não podem gravar atualizações em tempo real em seu diário. Contas diferentes podem observar o mesmo grupo, mas seus diários permanecem separados.

Cada evento inclui o hash anterior e uma assinatura Ed25519. As exportações abrangem todo o diário da área de trabalho por meio de um número de sequência fixo. Os filtros do painel não filtram a exportação; a coleta pode continuar além de seus limites enquanto ela está sendo preparada.

**A verificação do registro** verifica a cadeia de eventos e as assinaturas por meio do limite exibido. Seu resultado é apagado quando o espaço de trabalho é alterado, e o painel identifica novos registros adicionados após a verificação. A exportação em ZIP também verifica as mídias coletadas.

Uma assinatura válida atesta a integridade em relação à chave confiável, e não à origem do Telegram ou à veracidade do conteúdo. Mantenha as impressões digitais e os pontos de verificação de forma independente. Consulte o [modelo de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/), [as operações diárias](https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/) e [o procedimento de aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) para conhecer os requisitos de confiança e entrega.
