# Formato das evidências

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/

Conteúdo do arquivo ZIP assinado, tipos de registros, recibos de processamento, perfis de usuários, cópias externas e verificação offline.

Uma observação não é uma conclusão. Um ID de remetente não é uma identidade no mundo real. A atualização do serviço visível na conta é a fonte; o Telegram não assina criptograficamente esses registros salvos para um investigador terceirizado.

## O que é assinado

| Material | Proteção | O que deve ser mantido |
| --- | --- | --- |
| Todas as observações do registro, incluindo eventos operacionais | Cadeia SHA-256 e uma assinatura Ed25519 por evento | `events.jsonl` original, a impressão digital da chave confiável, e um ponto de verificação retido |
| Conteúdo do arquivo ZIP de evidências | `manifest.sig` assina o manifesto canônico, que lista os hashes dos arquivos de conteúdo | O arquivo ZIP completo, incluindo seu manifesto e sua assinatura |
| Anexos preservados | SHA-256 e contagem de bytes em um evento `media.saved` assinado; hash do arquivo no manifesto ZIP assinado | Os bytes originais contidos no arquivo ZIP verificado |
| Checkpoint | Assinatura Ed25519 sobre o comprimento do registro, o hash do cabeçalho, a chave pública e a data de criação | Uma cópia independente mantida antes de uma alteração contestada |
| Comprovante de execução | Medições do coletor assinadas separadamente; também incluídas em um evento `process.started` assinado | O registro e o diário associado; as métricas são declaradas pelos próprios usuários |
| Arquivo CSV ou HTML independente | Sem assinatura criptográfica independente; os hashes dos eventos, por si só, são insuficientes | Utilize o arquivo exato contido no ZIP verificado para a verificação de integridade |
| Capturas de tela, impressões ou arquivos PDF gerados por um navegador | Sem assinatura do TgWitness na versão derivada | Mantenha o pacote original verificado e documente como a versão derivada foi criada |

O coletor verifica as assinaturas do registro antes de gerar cada formato de exportação. Essa verificação da fonte não cria uma assinatura em um arquivo CSV ou HTML baixado separadamente. Da mesma forma, uma assinatura válida de evento JSONL não fornece os bytes do anexo nem comprova, de forma independente, que todo o registro observado tenha sido fornecido.

## Transferência de investigação

1. Registre a referência do caso, o operador, o ID numérico da conta do Telegram, as fontes selecionadas, a política de coleta e o período de coleta em suas anotações do caso. O TgWitness preserva as observações; a atribuição de casos e os registros de custódia são gerenciados fora do aplicativo. Qualifique a configuração de coleta pretendida por meio do [procedimento de aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
2. Mantenha a impressão digital da chave pública do espaço de trabalho de forma independente antes de confiar em suas exportações. Salve pontos de verificação assinados fora do coletor durante a coleta. Registre interrupções e os limites de visibilidade da conta.
3. Exporte um arquivo **ZIP assinado** e guarde o comprovante de execução assinado. Utilize um ponto de verificação no limite do registro exportado ou antes dele. Um ponto de verificação posterior pode rejeitar corretamente uma exportação anterior por ser muito curta. As exportações incluem o registro completo da área de trabalho, independentemente dos filtros do painel; revise o material antes de compartilhá-lo.
4. Peça ao destinatário que verifique o arquivo ZIP com uma cópia confiável do verificador e a impressão digital/ponto de verificação fornecida de forma independente. A partir de um checkout confiável com seu ambiente Python ativo:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Os relatórios de saída bem-sucedidos apresentam os códigos `key_pinned: true` e `checkpoint_checked: true` quando ambas as entradas são fornecidas e aceitas. Preserve o resultado da verificação.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Registre o SHA-256 do arquivo, o limite de exportação, a data de transferência, o remetente e o destinatário em seu registro de custódia. Mantenha o pacote original intacto e trabalhe com cópias. Compartilhe os arquivos de evidência, em vez do diretório de dados privados do aplicativo, que também contém sessões de conta e segredos de assinatura. Para a transferência, uma exportação pode ser colocada em um arquivo ZIP protegido por senha com criptografia AES-256. A senha protege apenas a confidencialidade e não é armazenada; o destinatário extrai o arquivo e verifica a exportação assinada em seu interior, que permanece inalterada.
   2. Caso seja necessária uma marcação de tempo independente, siga o [procedimento da RFC 3161](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/) e mantenha a solicitação, o ponto de verificação, as informações da CA confiável e a resposta verificada da autoridade. A simples preparação de uma solicitação não garante a obtenção de um carimbo de data e hora.

A verificação bem-sucedida estabelece a integridade em relação à chave do coletor confiável e ao limite definido. A veracidade da fonte, a entrega completa do Telegram, a data e hora confiáveis e a admissibilidade legal exigem evidências separadas. Esta versão ainda não concluiu a qualificação em ambiente real do Telegram nem uma avaliação forense/de segurança independente.

Uma chave de coletor copiada pode assinar um registro de substituição falsificado. A verificação em relação a um ponto de verificação ou registro de testemunha mantido de forma independente detecta um prefixo anterior alterado; a verificação da assinatura por si só não é capaz disso. Uma testemunha corrige o que o coletor apresentou, portanto, ela não estabelece de forma independente a veracidade dos registros falsificados antes de seu primeiro ponto de verificação externo. Os relatórios de implantação na nuvem verificam a configuração e as medições relatadas pelo coletor; eles não comprovam que uma chave privada nunca tenha sido copiada durante o processo de inicialização.

As notificações enviadas por meio do Apprise contêm nomes e contagens de espaços de trabalho e chats; pequenos trechos de mensagens excluídas e editadas são adicionados somente quando o operador ativa essa função (desativada por padrão). Trata-se de um sinal de conveniência, não de prova: a entrega não é garantida, e somente o registro e suas exportações assinadas registram o que foi observado. Com um proxy do espaço de trabalho, as notificações utilizam a mesma rota; serviços que não possam utilizá-la, bem como rotas do MTProxy, são recusados.

## Canonização de eventos

A entrada de hash consiste exatamente nos seguintes campos:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Serialize utilizando JSON compatível com Python em UTF-8, com chaves de objetos ordenadas, sem escape de ASCII, sem espaços em branco irrelevantes e sem NaN/infinito:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

O SHA-256 desses bytes torna-se o hash do evento. A assinatura é gerada pelo algoritmo Ed25519 sobre os 32 bytes brutos do hash e, em seguida, codificada em base64. O primeiro `previous_hash` é composto por 64 zeros. Os números de sequência começam em 1 e aumentam em 1. Todos os eventos, incluindo os operacionais, compartilham uma única cadeia. Não há supressão de entregas duplicadas: observações repetidas são recibos distintos, não uma alegação de ações distintas no Telegram.

As datas brutas do Telegram são strings ISO; os campos binários tornam-se objetos contendo bytes_base64. O texto da mensagem, entidades, descritores de mídia, metadados de resposta, reações e ações de serviço são mantidos nos metadados brutos da mensagem quando fornecidos.

observed_at é o relógio de parede UTC do coletor. source_at é uma data fornecida pelo Telegram, quando disponível. As notificações de exclusão não fornecem uma hora exata de exclusão; portanto, source_at permanece nulo. A ordem de recepção do transporte não corresponde necessariamente à ordem dos eventos na fonte. Os instantâneos do histórico utilizam datas de fonte mais antigas, mas horários de observação atuais.

## Semântica dos atores

message.new actor_id é o remetente da mensagem. message.edited não possui um editor inferido; payload.sender_id registra o remetente da mensagem observada. Exclusão O `actor_id` permanece nulo. As mensagens do serviço de associação mantêm o remetente e o tipo de ação, sem converter toda remoção em uma saída voluntária. As atualizações brutas dos participantes mantêm o `actor_id` conforme fornecido. Os instantâneos de reação não inventam um agente de alteração.

As notificações de exclusão para conversas privadas e grupos comuns contêm apenas IDs de mensagem. Essas conversas compartilham uma sequência de IDs válida para toda a conta; portanto, um ID identifica uma única mensagem dessa conta. Quando uma mensagem com esse ID foi salva anteriormente neste registro, a exclusão é registrada nesse chat como message.deleted, com o nome do método payload.chat_resolution. Os IDs que nunca foram salvos são mantidos como deletion.unscoped, sem chat_id; nada é inferido. Canais e supergrupos numeram as mensagens por bate-papo e nunca são mapeados dessa forma. Quando a mensagem excluída foi enviada pela conta observada, payload.deleted_message_was_outgoing é verdadeiro; o autor da exclusão ainda não é fornecido.

## Cobertura: continuidade, lacunas e IDs não observados

Cada arquivo ZIP assinado contém o `coverage.json`; o relatório em HTML abre com o mesmo resumo, e o `verify.py` o recalcula a partir do `events.jsonl`, em vez de confiar no arquivo:

- **Observado continuamente de X a Y.** Um período começa com `observation.started` e termina com uma pausa, uma interrupção, uma perda de conexão com o Telegram, um logout, um início de processo sem uma parada ordenada ou mais de três minutos sem qualquer registro durante a observação (os sinais de vida são registrados a cada minuto; portanto, o silêncio significa que o processo parou, travou ou que o computador entrou em modo de suspensão). Quando o intervalo entre sinais de vida é alterado em **“Parâmetros”**, cada sinal de vida registra essa alteração, e o silêncio permitido passa a ser de três intervalos, nunca inferior a três minutos.
- **As lacunas** indicam o intervalo de tempo entre períodos, acompanhado do motivo. Uma lacuna ainda em aberto no último registro é marcada como `not_resumed_by_last_record`.
- **IDs de mensagens não observadas.** Para canais e supergrupos, que numeram as mensagens por bate-papo, os IDs ausentes entre os observados são listados como intervalos. Eles são relatados como não*observados* — excluídos, nunca entregues ou fora do histórico salvo — nunca como excluídos. Bate-papos privados e grupos comuns compartilham uma sequência válida para toda a conta; portanto, lacunas nesses casos não têm significado e não são listadas.
- Notificações de lacunas no nível do chat (por exemplo, o Telegram solicitando a recuperação de diferenças em um canal) são contabilizadas como notas; elas não interrompem a cobertura global.

A cobertura descreve o que esse coletor registrou. Não constitui prova de que o Telegram tenha entregue todas as atualizações durante um período contínuo.

## Produtor

O manifesto assinado dos arquivos ZIP de evidências, exportações de bate-papos, registros de testemunhas e a declaração dos arquivos de perfil de pessoas contêm `producer` : software, versão, projeto (PhishDestroy), página inicial e repositório de código-fonte. O relatório em HTML exibe a mesma linha, e `verify.py` a imprime como parte do que foi verificado. Arquivos criados antes da existência desse campo são verificados como anteriormente e são relatados como não indicando um produtor.

## Perfis de pessoas

Um arquivo de perfil (`tgwitness-dossier-v1`, JSON) é gerado mediante solicitação a partir de registros já presentes no diário para um chat; nada é obtido do Telegram e o conteúdo do perfil nunca é gravado no diário (a ativação e desativação de perfis são registradas como `dossier.changed`). Para cada pessoa com uma mensagem salva, ele lista o nome e o histórico de nomes de usuário, as marcações do Telegram (bot, golpe, falso, premium, verificado, restrito, excluído) conforme exibidas no momento do salvamento, as identificadores de foto, SHA-256 e hash perceptual (pHash, compatível com `imagehash.phash`) do avatar a partir do cache local de avatares com avatares semelhantes, atividade (primeira e última mensagem, contagens, compartilhamentos editados e excluídos, mensagens por hora UTC), quem responde a quem, outros chats neste diário em que a pessoa escreveu e carteiras mencionadas (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; endereços Base58Check são validados por checksum), números de telefone, nomes de usuário e links, incluindo links ocultos atrás de texto.

Cada fato indica os registros do diário (`seq`) dos quais se origina, e `record_hashes` contém o hash de cada registro referenciado. A declaração é assinada com a chave do espaço de trabalho:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

Verifica a assinatura, verifica a própria exportação das evidências (assinatura, cadeia de hash e arquivos) e se todos os registros referenciados existem inalterados nessa exportação do mesmo espaço de trabalho. Os hashes de avatares são identificados como provenientes do cache local (não de registros do diário). As menções são correspondências de padrões — pistas a serem verificadas, não fatos comprovados. Os perfis são ativados por chat, podem ser exportados como um ZIP com criptografia AES-256 e senha, e são excluídos quando desativados ou quando o chat é removido das fontes.

## Testemunha independente

Um diário de testemunho (`tgwitness-witness-v1`) e suas publicações no canal são comparados com uma exportação de evidências com `verify.py --witness … --channel …`; consulte [testemunho independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/).

## Manifesto e pontos de verificação

O arquivo `manifest.json` inclui o formato, a hora da exportação, a chave pública, a impressão digital, o comprimento do registro, o hash do cabeçalho, o escopo, o produtor, as limitações e o SHA-256 de cada elemento de conteúdo, exceto os próprios ``manifest.json`` e ``manifest.sig``. O arquivo `manifest.sig` é a assinatura Ed25519 em base64 sobre o JSON canônico do manifesto. O verificador rejeita membros inesperados ou ausentes, nomes duplicados, arquivos corrompidos, sequência ou cadeia interrompida, assinaturas inválidas e incompatibilidade com um ponto de verificação fornecido. Ele nunca extrai caminhos de arquivos compactados. Limita o tamanho total declarado sem compactação a 4 GiB; o `--max-gib N` permite arquivos compactados maiores, criados com um limite **de parâmetros** aumentado.

Obtenha o código verificador a partir de uma versão confiável ou de uma cópia independente revisada. Um verificador dentro de um arquivo não confiável é um material executável fornecido pelo autor desse arquivo; sua presença é uma conveniência de portabilidade, não uma âncora de confiança independente.

Um ponto de verificação assina uma declaração contendo a chave pública, o tamanho do registro, o hash inicial e a hora de criação. O verificador pode conferir se um arquivo posterior contém o mesmo prefixo. Mantenha um ponto de verificação fora do coletor antes de uma alteração contestada: um invasor que controle tanto o arquivo quanto o ponto de verificação pode substituir ambos.

Uma assinatura válida de uma chave não fixada estabelece apenas consistência interna. Mesmo uma chave fixada não pode comprovar a veracidade do conteúdo da fonte se o coletor ou a chave tiverem sido comprometidos antes do registro. O carimbo de data e hora externo e a captura confiável são requisitos separados. O TgWitness não garante a admissibilidade ou a certificação forense.

## Anexos

Os arquivos são identificados por SHA-256 na pasta media/. Um evento media.saved vincula um hash e o comprimento em bytes a um evento de mensagem específico. Os nomes dos arquivos brutos são metadados, nunca caminhos locais. Os bytes de mídia são baixados de forma assíncrona; portanto, a exclusão imediata pode impedir a captura. A coleta desativada, arquivos com tamanho excessivo ou desconhecido, falhas no download e downloads interrompidos são exibidos como resultados. Uma falha no processo pode deixar arquivos parciais sem referência; eles não são incluídos nas exportações.

O exportador ZIP verifica os arquivos de mídia armazenados em relação aos seus nomes. As exportações em JSONL, CSV e HTML verificam as assinaturas dos eventos, mas não incluem os bytes de mídia. Os relatórios derivados são recursos de conveniência; o arquivo events.jsonl é a representação oficial dos eventos.

## Recibos de coleta e processamento duradouros (0,2)

Uma tarefa de mídia e seu evento de mensagem são confirmados em uma única transação. A tarefa armazena o descritor original da mensagem do Telegram; a observação assinada vincula seu SHA-256, conta e política de tamanho. A recuperação verifica essa vinculação antes do download. Ela nunca busca a mensagem atual e substitui silenciosamente por um anexo mais recente. Tarefas interrompidas são repetidas, enquanto a falha permanente permanece como um resultado explícito.

Cada espaço de trabalho possui seu próprio diário e identidade de assinatura. Um evento `process.started` inclui um ID de execução, relógios locais, versões de dependências, hashes de arquivos-fonte, conta/escopo inicial, e configurações de captura. Os heartbeats incluem o ID de execução, o tempo monotônico e o estado da fila. O comprovante do processo também pode ser baixado como uma declaração assinada separadamente. As medições de arquivos são auto-relatadas e não constituem um atestado de hardware confiável.

Pontos de verificação automáticos são retidos localmente na inicialização, a cada cinco minutos durante a observação (**Parâmetros → Ponto de verificação assinado a cada**) e ao encerramento ordenado. A verificação na inicialização e a exportação comparam o registro com o ponto de verificação local mais recente retido. Isso permite detectar uma reversão do banco de dados quando o ponto de verificação permanece intacto; um operador que controle ambos ainda pode substituir ambos. A retenção independente e os carimbos de data e hora externos confiáveis continuam sendo requisitos distintos.

Após uma reinicialização, a posição de atualização salva do Telegram é retomada (`catch_up_from` em `observation.started`) e as atualizações perdidas são solicitadas. Uma verificação periódica registra `message.recovered` para mensagens perdidas e `message.missing_on_recheck` quando o Telegram não retorna mais uma mensagem salva; este último não é um aviso de exclusão e não indica quem excluiu nem a hora.

### Cópia e restauração externas (S3)

A cópia externa (Exportações, desativada por padrão) envia segmentos do registro, arquivos preservados e pontos de verificação com seus carimbos de data e hora, bem como exportações concluídas de conversas, para um armazenamento compatível com S3, criptografados com AES-256-GCM antes do envio, utilizando uma chave mantida no cofre do espaço de trabalho; a retenção por Object Lock se aplica quando o bucket for compatível. Sem a chave baixada, a cópia não pode ser lida. Restaure e verifique com `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

A restauração requer um diretório comum vazio. Os arquivos baixados e os objetos descriptografados permanecem em um armazenamento temporário privado até que todo o diário e todos os pontos de verificação retidos sejam validados. Caminhos de objetos inseguros, intervalos de segmentos inconsistentes e diários com duração inferior a um ponto de verificação são rejeitados; em caso de falha na verificação, nenhum arquivo restaurado é publicado. As verificações de retenção comparam o modo Object Lock e a data retornados com o prazo enviado no momento do upload (tolerância de arredondamento de um segundo). Um prazo expirado, inválido ou reduzido não é considerado como verificado. O status informa o objeto amostrado cuja retenção foi lida para aquela passagem de upload.

O progresso da cópia está restrito ao destino e à chave de criptografia. A alteração do endpoint, do bucket ou do prefixo inicia uma cópia completa do registro, das mídias e dos pontos de verificação retidos localmente para esse destino. O progresso antigo não restrito é preservado, mas reproduzido uma única vez após a atualização. As exportações históricas de bate-papos já removidas da caixa de saída local permanecem em seu destino anterior.

Mídias locais ausentes ou corrompidas são relatadas como erro da passagem e mantêm o cursor de mídia antes delas, de modo que o arquivo seja tentado novamente na próxima passagem; os arquivos, pontos de verificação e exportações posteriores a elas ainda são copiados. A restauração verifica todas as referências de mídia preservadas em relação aos hashes descriptografados e aos tamanhos registrados. Segmentos idênticos e sobrepostos do diário provenientes de uploads interrompidos são desduplicados; sobreposições conflitantes são rejeitadas. Os pontos de verificação criados durante um upload são adiados até que os registros do diário a que se referem tenham sido copiados, de modo que uma passagem concluída não publique um ponto de verificação antes de seu diário.

### Exportação contínua de instantâneos

As exportações em tempo real utilizam um instantâneo de leitura estável do SQLite. Sua parte inicial pode ser mais antiga do que o diário ativo atual quando o download for concluído. Um ponto de verificação criado após esse instantâneo pode indicar corretamente que o arquivo é menor; compare com um ponto de verificação no prefixo exportado ou anterior a ele, e não com um ponto de verificação posterior arbitrário.

## Preparação da RFC 3161 e verificação de respostas (0.2)

O modo de evidência (desativado por padrão) envia apenas o SHA-256 de cada ponto de verificação assinado às autoridades listadas na RFC 3161 e aos calendários do OpenTimestamps, pela rota do espaço de trabalho e nunca pelo MTProxy. As respostas são mantidas no `checkpoints/anchors/`, exportadas e verificadas pelo `verify.py` (o `--tsa-ca` verifica a assinatura TSA; confirme as provas do OpenTimestamps com o `ots upgrade` e o `ots verify`).

O painel prepara um arquivo de solicitação contendo os bytes canônicos do arquivo checkpoint.json, uma impressão digital da mensagem SHA-256 e um nonce aleatório no arquivo timestamp.tsq, somas de verificação e instruções. Nenhuma solicitação de rede é feita. A preparação não constitui um carimbo de data/hora confiável.

O `python -m tgwitness.anchor verify` chama o OpenSSL duas vezes: uma vez em relação aos bytes do ponto de verificação e outra em relação à solicitação original. É necessário um arquivo de CA confiável explicitamente; os certificados incluídos não são automaticamente considerados confiáveis. A verificação da solicitação é opcional na interface de linha de comando (CLI); portanto, mantenha e forneça a opção --request para verificar o nonce. O resultado indica se a verificação foi realizada. A assinatura do ponto de verificação do coletor e o registro ainda devem ser verificados separadamente com a impressão digital confiável do coletor.

O verificador atual não obtém informações de revogação nem implementa validação de arquivamento de longo prazo após o vencimento do certificado. Não equipare a verificação bem-sucedida da assinatura a um carimbo de data e hora qualificado ou à admissibilidade legal. Nenhuma TSA independente foi contatada durante o desenvolvimento. Consulte [o procedimento](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/).
