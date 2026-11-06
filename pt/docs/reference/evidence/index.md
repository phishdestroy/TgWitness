# Formato das evidências

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/

Conteúdo do arquivo ZIP assinado, tipos de registros, recibos de processamento, perfis de usuários, cópias externas e verificação offline.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Evidências e verificação](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

O TgWitness preserva as observações do Telegram visíveis na conta em um diário assinado. Os destinatários podem verificar os registros, anexos e relatórios salvos em relação a uma chave de coletor confiável e, em seguida, comparar o diário com um ponto de verificação mantido de forma independente. Esta página descreve os formatos, as verificações e o material a ser mantido para a entrega.

Os usuários podem começar com o **VERIFY.cmd** no Windows: ele solicita o arquivo ZIP original e a impressão digital da chave obtida de forma independente, exibe um resultado explicado e salva um relatório de verificação separado. Consulte os executáveis de verificação [e o ambiente de execução portátil](https://github.com/phishdestroy/TgWitness/blob/main/docs/VERIFICATION_LAUNCHER.md) para obter informações sobre configuração e limites de confiança.

**Nesta página**

- [O que está assinado](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#what-is-signed)
- [Comparando exportações de bate-papos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#comparing-chat-exports)
- [Transferência da investigação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#investigation-handoff)
- [Trecho de transferência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#handover-extract)
- [Relatórios legíveis](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#readable-reports)
- [Canonização de eventos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#event-canonicalization)
- [Semântica do ator](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#actor-semantics)
- [Cobertura: continuidade, lacunas e IDs não observados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids)
- [Produtor](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#producer)
- [Perfis de pessoas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#people-profiles)
- [Testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#independent-witness)
- [Manifesto e pontos de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#manifest-and-checkpoints)
- [Escopo da verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope)
- [Anexos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#attachments)
- [Recibos de coleta e processamento duráveis (0.2)](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#durable-collection-and-process-receipts-02)
- [Preparação da RFC 3161 e verificação da resposta (0.2)](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)
- [Registros opcionais no modo de evidência: drand e dispositivos do Telegram](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)

## O que é assinado

| Material | Proteção | O que deve ser mantido |
| --- | --- | --- |
| Todas as observações do registro, incluindo eventos operacionais | Cadeia SHA-256 e uma assinatura Ed25519 por evento | `events.jsonl` original, a impressão digital da chave confiável, e um ponto de verificação retido |
| Conteúdo do arquivo ZIP de evidências | `manifest.sig` assina o manifesto canônico, que lista os hashes dos arquivos de conteúdo | O arquivo ZIP completo, incluindo seu manifesto e sua assinatura |
| Anexos preservados | SHA-256 e contagem de bytes em um evento `media.saved` assinado; hash do arquivo no manifesto ZIP assinado | Os bytes originais contidos no arquivo ZIP verificado |
| Ponto de verificação | Assinatura Ed25519 sobre o comprimento do registro, o hash do cabeçalho, a chave pública e a data de criação | Uma cópia independente mantida antes de uma alteração contestada |
| Comprovante de execução | Registro assinado da versão do coletor, hashes dos arquivos-fonte e configurações iniciais, também incluídos no `process.started` | O recibo, o diário associado e as evidências do ambiente para o modo de verificação selecionado |
| Relatórios legíveis: `report.html` e suas partes, `report.json`, `report.pdf`, `chat.pdf` | Um selo Ed25519 por arquivo sobre seu conteúdo; o PDF também contém uma assinatura padrão PDF (consulte [Relatórios legíveis](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#readable-reports)) | O arquivo tal como foi recebido e a impressão digital da chave confiável; o arquivo ZIP descrito nele |
| CSV independente | Sem assinatura criptográfica independente; os hashes dos eventos, por si só, são insuficientes | Utilize o arquivo exato contido no ZIP verificado para a verificação de integridade |
| Capturas de tela, impressões ou arquivos PDF gerados por um navegador | Sem assinatura do TgWitness na versão derivada | Mantenha o pacote original verificado e documente como a versão derivada foi criada |

O coletor verifica as assinaturas do diário antes de gerar cada formato de exportação. Relatórios legíveis em HTML e PDF possuem seus próprios selos; o CSV independente é verificado como parte de um ZIP assinado. Mantenha o ZIP para preservar os bytes do anexo e o manifesto, e um ponto de verificação separado para comparar o diário com um limite anterior.

## Comparando exportações de bate-papos

Verifique e compare dois arquivos ZIP de exportação de bate-papo assinados com impressões digitais dos signatários mantidas de forma independente:

```
python -m tgwitness.verify first.zip --compare second.zip \
  --fingerprint FIRST_TRUSTED_KEY_SHA256 --compare-fingerprint SECOND_TRUSTED_KEY_SHA256
```

Quando ambos os arquivos registram os mesmos IDs numéricos de conta e de chat, os registros são emparelhados pelo ID da mensagem. **Inalterado** significa igualdade do registro JSON completo salvo: texto completo, autor, datas, destinatário da resposta, metadados aninhados e campos desconhecidos estão todos incluídos. A ordem das chaves do objeto JSON não importa; campos ausentes, valores nulos, tipos de valor e ordem da matriz, sim. A pré-visualização de 300 caracteres serve apenas para exibição. As entradas alteradas identificam o `changed_fields` de nível superior diferente, incluindo alterações invisíveis nessa pré-visualização. IDs de mensagem duplicados são rejeitados, em vez de se sobrescreverem mutuamente durante a correspondência.

Uma diferença pode ser um nome de exibição alterado, contagem de visualizações, anotação de coleção ou outros metadados de observação. Por si só, isso não comprova uma edição no Telegram, não identifica quem fez a alteração nem prova qual arquivo contraditório está correto. Registros não analisados permanecem na comparação; a igualdade de sua representação salva não significa que sua carga útil do Telegram tenha sido decodificada.

Para identidades de conta/bate-papo diferentes ou ausentes, a ferramenta encontra apenas possíveis correspondências usando remetente, texto completo, hash do arquivo, tipo de mídia e uma tolerância de tempo de cinco segundos. Ela relata **Correspondência**, e não **Inalterado**. Esses candidatos não estabelecem a identidade da mensagem nem a igualdade de todos os metadados. Registros não analisados permanecem sem correspondência. As diferenças nos registros emparelhados continuam listadas em `changed`, inclusive no modo de conteúdo; essas diferenças não comprovam edições na mesma mensagem. Com `--json`, `matched` conta os pares e `unchanged` conta os pares cujos registros completos salvos são iguais. Nenhuma das contagens comprova a identidade da mensagem no modo de conteúdo. A saída existente `changed_fields` e a saída inteira `unchanged` permanecem compatíveis com resultados de comparação anteriores. O formato de arquivo e a verificação de assinatura permanecem inalterados.

## Transferência de investigação

1. Registre a referência do caso, o operador, o ID numérico da conta do Telegram, as fontes selecionadas, a política de coleta e o período de coleta nas notas do seu caso. O TgWitness preserva observações e oferece suporte a notas e coletas vinculadas a fontes no [Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/). Mantenha os registros de transferência e custódia junto com os materiais do seu caso. Verifique a configuração de coleta pretendida com o [procedimento de aceitação em tempo real](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md).
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

A verificação bem-sucedida estabelece a integridade em relação à chave do coletor confiável e ao limite retido. Consulte [o escopo da verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) para conhecer as suposições de confiança e [os resultados da validação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/) das verificações realizadas.

## Trecho da transferência

Um arquivo ZIP assinado contém todo o registro do espaço de trabalho. Quando um tribunal, um advogado ou uma unidade de combate a abusos precisa apenas de algumas conversas, de um período específico ou de determinadas pessoas, a opção **“Exportações → Extrato de transferência”** prepara uma cópia reduzida (`tgwitness-handover-v1`) de acordo com as regras de divulgação selecionadas. O operador indica a finalidade e escolhe as conversas, um período opcional (UTC), as pessoas às quais o extrato se refere, o que acontece com todos os demais (exibidos, substituídos por pseudônimos P01, P02… ou excluídos ), quais textos de mensagens permanecem, quais anexos e fotos de perfil são incluídos e se os números de telefone e endereços de e-mail nos textos são mascarados. A finalidade e essas regras constam no manifesto assinado e no relatório; o diário registra “`handover.exported`” com o acesso que o preparou e o SHA-256 do arquivo, não o conteúdo.

O ``verify.py`` verifica um extrato de duas maneiras. Um registro exibido como inalterado é verificado na íntegra: seu conteúdo é comparado com seu hash, sua assinatura Ed25519 e seu link para um antecessor incluído. Um registro minimizado mantém o hash e a assinatura originais, de modo que a assinatura ainda é validada, mas os campos ocultados não podem ser recalculados a partir dele; o registro indica o que foi ocultado e o relatório marca isso. O manifesto indica a extensão do diário e o cabeçalho com a assinatura do coletor sobre esse cabeçalho, além de contar os registros omitidos; o arquivo `coverage.json` descreve as conversas escolhidas. Nomes dentro de nomes de arquivos não são detectados. Revise os arquivos finais antes de compartilhá-los: texto livre, nomes de arquivos e anexos selecionados ainda podem identificar pessoas. Guarde o ZIP completo e assinado: a extração é uma divulgação, não um substituto.

## Relatórios de fácil compreensão

As evidências assinadas, a transferência e os arquivos ZIP de bate-papos contêm relatórios legíveis em HTML e JSON, além de PDF quando as fontes necessárias estiverem disponíveis, no idioma selecionado para o relatório. Cada relatório é selado com a chave Ed25519 do espaço de trabalho e pode ser verificado separadamente: ` `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]``.

- `report.html` / `chat.html`: a instrução de selagem (`tgwitness-report-seal-v1`) fecha o arquivo e assina o SHA-256 de cada byte anterior a ela. Diários e bate-papos longos são divididos em partes de um tamanho configurável (Configurações do relatório, de 500 a 100.000 registros; 5.000 por padrão): `records/records-0001.html` ou `messages/messages-0001.html`, cada uma selada com seu número, intervalo e o total, e listada com seu SHA-256 no manifesto assinado. Séries de sinais de vida do coletor são exibidas como uma única linha, a menos que as configurações do relatório as listem uma a uma.
- `report.json` (`tgwitness-report-json-v1`, chaves `format`, `report`, `seal`): o selo assina o SHA-256 do JSON canônico do `report`, para que os fatos possam ser lidos por sistemas de instâncias e scripts e uma seleção para proteção de dados possa ser feita a partir deles, enquanto o arquivo assinado permanece intacto.
- `report.pdf` / `chat.pdf`: um documento formal para impressão e arquivamento, assinado duas vezes sobre os mesmos bytes, todo o arquivo, exceto o valor da assinatura (`/ByteRange`). A assinatura padrão PDF (`adbe.pkcs7.detached`, CMS com SHA-256 e ECDSA P-256) utiliza um certificado de assinatura de documentos autoemitido armazenado no cofre da área de trabalho; seu número de série de assunto é a impressão digital da chave Ed25519 . O selo Ed25519 é transportado dentro do CMS como o atributo não assinado `2.25.240684792623320047764573196045913242332` e identifica o certificado SHA-256 com `"content": "pdf-byte-range"`, de modo que a chave Ed25519 atesta a autenticidade do certificado. Um leitor PDF mostra se o arquivo foi alterado após a assinatura e considera o signatário desconhecido até que o certificado seja considerado confiável; compare a impressão digital Ed25519 em vez disso. PDFs em chinês, japonês e coreano precisam de uma fonte no servidor (ou no `TGWITNESS_FONT_DIR`); sem ela, o ZIP contém apenas os relatórios HTML e JSON .

Em um canal ou supergrupo, Telegram numera as mensagens 1, 2, 3… em ordem. Uma exportação de bate-papo lista o primeiro e o último número, quantas mensagens estão presentes e cada sequência de números ausentes em `message-ids.json` , o manifesto e o cabeçalho `chat.json` , além de marcar cada lacuna onde ela ocorre na transcrição. `verify.py` recomeça a contagem a partir de `chat.json` . Um número ausente é uma mensagem que Telegram não retornou (excluída antes da exportação ou não visível para a conta); em bate-papos privados e grupos básicos, os números são compartilhados por todos os bate-papos da conta e as lacunas não são contadas.

Após ler o histórico, a exportação solicita novamente ao Telegram cada número ausente, por número (`channels.getMessages`, até os números 10,000). O resultado está em `message-ids.json` e no relatório. Uma resposta vazia registra que o número não está disponível para esta conta no momento da nova verificação; ela não especifica a causa. Uma mensagem retornada na nova verificação é adicionada à exportação e marcada como `found_on_recheck`.

Cada relatório começa com **. Em resumo,**: um parágrafo, seguido do que o material mostra e do que ele não mostra (quem está por trás de uma conta, integridade da entrega, exclusões antes da observação, hora sem carimbo de data/hora). O selo da própria página fica âmbar quando o navegador verifica a assinatura do selo, e não a página: um navegador não fornece à página seus próprios bytes. Ele fica verde somente quando o leitor arrasta o arquivo para a verificação no final da página e todos os bytes correspondem, e somente se a página exibida for esse arquivo; caso contrário, ele fica vermelho.

Cada relatório identifica o programa com exatidão: o commit do Git quando o coletor é executado a partir de um checkout ou quando o instalador define `TGWITNESS_COMMIT`, e o SHA-256 de seus arquivos-fonte (`source_tree_sha256`, o JSON canônico do caminho → SHA-256 de cada arquivo `.py`, `.js`, `.css`, `.html` e `.svg` no pacote), que um checkout desse commit reproduz, a menos que os arquivos tenham sido alterados. O cliente Telegram é nomeado com base em sua biblioteca, camada de API e centro de dados. Quando a observação começa e quando uma exportação de chat inicia e termina, o coletor solicita ao Telegram sua hora (`updates.getState`, segundos inteiros ) e registra a hora do Telegram menos o relógio do coletor, com a incerteza decorrente da ida e volta; os relatórios mostram essas medições na seção “Cadeia de custódia”. Uma exportação de bate-papo também registra quando leu o histórico, além das datas das mensagens.

### Visualizador de relatórios offline e guia de arquivamento

Extraia o ZIP completo antes de abrir `chat.html` ou `report.html`. O visualizador oferece pesquisa, filtros, participantes, indicadores, detalhes do registro e seleções de JSON/CSV sem a necessidade de um servidor. Mantenha `viewer/` e `media/` ao lado do relatório. As seleções são derivadas: use `verify.py SELECTION.json
--evidence ARCHIVE.zip` para compará-las com o arquivo assinado. O verificador verifica o ID do relatório, a chave de assinatura, o limite do arquivo e cada item selecionado; itens editados, ausentes e duplicados são rejeitados. As notas de seleção e a hora de criação permanecem como metadados não assinados.

Lacunas no número de mensagens são exibidas apenas para um feed de bate-papo completo, não filtrado e em ordem crescente. Ocultar uma categoria ou não conseguir carregar um bloco de dados não deve transformar uma linha omitida em evidência de uma mensagem ausente . Os destaques de pesquisa operam em texto simples antes do escape “HTML”, preservando a marcação literal.

O navegador verifica as assinaturas do manifesto, o ID e a chave do relatório, bem como todos os hashes de arquivos listados. Ele rejeita estruturas ZIP ambíguas ou malformadas, nomes duplicados e caminhos inseguros, e limita os arquivos a 256 MiB e o conteúdo total declarado a 4 GiB. Use o verificador independente para arquivos maiores. Essa verificação do navegador complementa as verificações do verificador quanto às cadeias de registros e à semântica dos dados.

O `README.txt` contém um guia de introdução, um inventário de arquivos alinhado, instruções de verificação e notas sobre o formato dos dados no idioma do relatório, seguidas por um guia completo em inglês. O `SHA256SUMS` abrange os arquivos listados nele, excluindo o próprio, o `manifest.json` e o `manifest.sig`; o manifesto assinado também abrange o `SHA256SUMS`. Mantenha o ZIP original inalterado e salve os arquivos de trabalho fora da pasta extraída. Os relatórios do PDF incluem marcadores de seção e identificação do caso/relatório nas páginas seguintes.

### O chat no momento da exportação

A exportação de um chat registra o que Telegram informou sobre o chat no momento em que a exportação foi iniciada: as próprias etiquetas de Telegram (`scam`, `fake`, `restricted` com seus motivos, `verified`), nomes de usuário, descrição, número de membros e administradores, a discussão vinculada, proteção de conteúdo, se novos membros veem mensagens anteriores e a partir de qual mensagem esta conta tem acesso ao histórico (`available_min_id`), a data da mensagem 1, quando se trata da criação do chat, e o SHA-256 da foto do chat (salva em `media/`). Registra a posição da conta exportadora no chat: função, data de adesão, quem a convidou e, no caso de um administrador, seus direitos. Uma solicitação que o Telegram recusa é indicada em seu lugar.

Quando a conta que realiza a exportação é um administrador, a exportação lê o registro de administração do chat (Telegram, mantido por cerca de 48 horas) para `admin-log.json`: exclusões e edições, com o conteúdo e a conta responsável pela ação. Esse é o único registro de uma exclusão que indica quem a realizou.

### Indicadores

A lista de relatórios e o arquivo contêm, como `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) e `indicators.misp.json` (evento MISP ), o que uma equipe de combate a abusos pode analisar nas mensagens registradas: links e domínios (mesmo aqueles ocultos atrás de texto, em botões e em visualizações de links), endereços de criptomoedas, nomes de usuário e links de convite Telegram , números de telefone, endereços de e-mail e imagens salvas. Endereços de Bitcoin, Litecoin, Dogecoin e TRON são listados apenas quando sua soma de verificação base58 é válida, endereços segwit quando sua soma de verificação bech32 ou bech32m é válida e endereços TON quando seu CRC é válido; endereços EVM e Solana são marcados como não verificados. As imagens contêm SHA-256 e um hash perceptual (dHash, 64 bits) que cópias recomprimidas ou redimensionadas mantêm praticamente inalterado. Os relatórios registram indicadores para que não sejam abertos acidentalmente (`hxxps[://]example[.]com` ); os arquivos mantêm os valores como estavam. Cada indicador é marcado como desconhecido e não apto para detecção automática (STIX , `indicator_types: unknown` , MISP , `to_ids: false` ; distribuição para a própria organização): o fato de estar listado significa que uma mensagem o continha, não que seja malicioso. Um link cujo texto exibe um endereço diferente daquele que ele abre é marcado no relatório.

Os relatórios PDF terminam com uma declaração do examinador a ser assinada à mão, uma lista de verificação para um notário ou perito judicial e um código QR (também na primeira página) com o ID do relatório, a impressão digital da chave e o SHA-256 dos dados oficiais, de modo que uma cópia impressa remeta de volta ao seu arquivo.

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

Um aviso sem escopo não confirma que uma mensagem nunca foi salva: um bate-papo correspondente pode estar fora do escopo da observação atual, ou uma correspondência única pode estar indisponível. A nova verificação de ausência continua sendo uma observação separada de uma notificação de exclusão nas contagens de relatórios, filtros e rótulos. Uma recuperação posterior elimina o estado atual de ausência, preservando a verificação anterior malsucedida no histórico assinado; nenhuma das observações constitui um aviso de exclusão.

Vários IDs resolvidos para o mesmo chat a partir de uma notificação são agrupados como `deletion.batch`, independentemente de sua quantidade. A notificação não indica se todo o histórico foi apagado, quem realizou a exclusão ou se ela se aplicou a todos os participantes. Mensagens enviadas salvas não alteram esses limites. Diários mais antigos podem conter eventos `history.cleared` inferidos a partir de lotes de dez ou mais IDs, com texto explicativo atribuindo a exclusão ao outro participante. Essas inferências não são suportadas pela atualização. Preserve esses registros assinados originais, mas trate-os como notificações de exclusão agrupadas; a interface atual os rotula de acordo.

## Cobertura: continuidade, lacunas e IDs não observados

Cada arquivo ZIP assinado contém o `coverage.json`; o relatório em HTML abre com o mesmo resumo, e o `verify.py` o recalcula a partir do `events.jsonl`, em vez de confiar no arquivo:

- **Observado continuamente de X a Y.** Um período começa com `observation.started` e termina com uma pausa, uma interrupção, uma perda de conexão com o Telegram, um logout, um início de processo sem uma parada ordenada ou mais de três minutos sem qualquer registro durante a observação (os sinais de vida são registrados a cada minuto; portanto, o silêncio significa que o processo parou, travou ou que o computador entrou em modo de suspensão). Quando o intervalo entre sinais de vida é alterado em **“Parâmetros”**, cada sinal de vida registra essa alteração, e o silêncio permitido passa a ser de três intervalos, nunca inferior a três minutos.
- **As lacunas** indicam o intervalo de tempo entre períodos, acompanhado do motivo. Uma lacuna ainda em aberto no último registro é marcada como `not_resumed_by_last_record`.
- **IDs de mensagens não observadas.** Para canais e supergrupos, que numeram as mensagens por bate-papo, os IDs ausentes entre os observados são listados como intervalos. Eles são relatados como não*observados* — excluídos, nunca entregues ou fora do histórico salvo — nunca como excluídos. Bate-papos privados e grupos comuns compartilham uma sequência válida para toda a conta; portanto, lacunas dentro de um desses bate-papos não significam nada e não são listadas ali.
- Notificações de lacunas no nível do chat (por exemplo, o Telegram solicitando a recuperação de diferenças em um canal) são contabilizadas como notas; elas não interrompem a cobertura global.

### Números de mensagens ausentes (`gap_summary`)

**Pré-visualização.** `coverage.json` → `gap_summary` Mede os números atribuídos pelo Telegram que este coletor nunca detectou. O Telegram numera as mensagens uma vez por canal ou supergrupo e uma vez por conta em chats privados, bots e grupos comuns. Um número entre duas mensagens observadas pode ser observado ou estar faltando; um intervalo contíguo é uma afirmação positiva de que todas as mensagens numeradas nesse intervalo foram observadas. Uma lacuna não indica nenhum agente nem motivo.

| Campo | Significado |
| --- | --- |
| `status` | `on`, ou `off` quando desativado em **Parâmetros → Análise de lacunas** |
| `parameters` | Os parâmetros que geraram o resultado, para que ele possa ser repetido |
| `chats[]` | Uma entrada por canal ou supergrupo, cada uma numerada separadamente |
| `account` | A sequência, em toda a conta, de conversas privadas, bots e grupos comuns |
| `status` (por sequência) | `applicable`, ou `not_applicable` com `reason` |
| `observed_from`, `observed_to`, `span` | Primeiro e último número observado e o tamanho do intervalo |
| `observed`, `observed_without_content` | Números observados; aqueles conhecidos apenas por meio de um registro de exclusão ou de nova verificação |
| `missing`, `density`, `gap_ranges`, `largest_gap` | Números nunca observados, sua proporção no intervalo, quantas execuções, a execução mais longa |
| `clusters[]` | Lacunas listadas: `low`, `high`, `missing`, e os números observados adjacentes `after` / `before` com seus horários de observação |
| `service_estimate` | Somente quando ativado: quantos números ausentes seriam mensagens de serviço, considerando sua proporção observada. Nunca subtraído de `missing` |

A validade é derivada do diário, nunca é presumida:

- **Canais e supergrupos** são medidos por conversa, inclusive na exportação de conversas selecionadas. Os registros selecionados pelo remetente constituem a medição `not_applicable`.
- **A sequência em toda a conta** é medida apenas da primeira à última mensagem que chegou enquanto a coleta de toda a conta estava ativada e incluiu chats privados, bots, grupos comuns e as próprias mensagens da conta, sem excluir nenhum desses chats (`scope.changed`). Números indicados por `deletion.unscoped` contagem são considerados observados sem conteúdo. Uma exportação ou transferência de chats selecionados não pode medi-la. Se a coleta de toda a conta foi desativada e reativada, uma nota indica que os números usados nesse intervalo aparecem como lacunas.
- As mensagens de serviço são registros do diário com números próprios, portanto, preenchem suas lacunas por conta própria; a estimativa opcional serve apenas como contexto.

`verify.py` recalcula `gap_summary` a partir `events.jsonl` com os parâmetros no `coverage.json` (valores padrão para arquivos mais antigos) e imprime a linha referente a toda a conta em seu resumo de cobertura. O `get_capture_status`(MCP e a linha de comando) retorna a mesma medição para os chats que um acesso pode ler; a sequência de toda a conta apenas para acessos que abranjam todo o espaço de trabalho.

Observações repetidas de uma mensagem de serviço contam apenas uma vez, e a estimativa do serviço da conta utiliza apenas números dentro do intervalo medido. Um escopo aplicado deve preservar explicitamente as próprias mensagens da conta antes que a medição em toda a conta seja habilitada; registros mais antigos sem essa informação não podem estabelecer essa condição. A interrupção da observação não amplia o intervalo medido, e sua retomada é registrada. A consulta ao arquivo em tempo real tem um limite de tempo, incluindo a varredura do banco de dados, e marca uma medição inacabada como parcial.

O Telegram documenta as [sequências separadas de IDs de mensagens](https://core.telegram.org/api/updates#message-id-sequences). Esses números descrevem observações; eles não identificam quem realizou a exclusão nem determinam por que um número está ausente.

Quando o Telegram deixa de aceitar a conta, o registro `coverage.gap` que encerra a observação contém o `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` ou `not_authorized`) e o Telegram erro; o `verify.py` indica a causa do encerramento do período.

A cobertura combina períodos de observação registrados, interrupções e resultados das mensagens. Avalie-a em conjunto com os chats selecionados, o período e a política de anexos; a operação contínua, por si só, não garante a entrega completa das atualizações do Telegram.

## Produtor

O manifesto assinado dos arquivos ZIP de evidências, exportações de bate-papos, registros de testemunhas e a declaração dos arquivos de perfil de pessoas contêm `producer` : software, versão, projeto (PhishDestroy), página inicial e repositório de código-fonte. O relatório em HTML exibe a mesma linha, e `verify.py` a imprime como parte do que foi verificado. Arquivos criados antes da existência desse campo são verificados como anteriormente e são relatados como não indicando um produtor.

Cada registro `observation.started` também identifica o cliente Telegram que realizou a observação: seu `api_id` (nunca o hash), seja esse um par público integrado ou o próprio aplicativo da operadora, a descrição do cliente enviada na solicitação de conexão do Telegram e o tipo de rota de conexão com o modo IP (sem endereço de proxy ou senha). O relatório e o `custody.json` listam todos os clientes e rotas distintos com a data em que foram registrados, bem como as vezes em que nenhum proxy listado respondeu e o Telegram detectou o endereço do servidor. Os registros anteriores a este confirmam isso.

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

Execute a verificação a partir da versão TgWitness instalada ou de um checkout revisado. A cópia incluída no arquivo permite o uso portátil; compare essa cópia com sua instalação confiável antes de executá-la.

Um ponto de verificação assina uma declaração contendo a chave pública, o comprimento do diário, o hash do cabeçalho e a hora de criação. O verificador pode conferir se um arquivo posterior contém o mesmo prefixo. Mantenha o ponto de verificação fora do coletor, para que a verificação posterior compare o arquivo com uma referência mantida separadamente dele.

## Escopo da verificação

A verificação analisa o arquivo e o modo de coleta utilizado para produzi-lo. Escolha o modo cujo limite de confiança corresponda ao caso e, em seguida, mantenha suas entradas de verificação.

| Modo de coleta | O que o verificador verifica | Entradas de verificação e limite de confiança |
| --- | --- | --- |
| Área de trabalho local | Registrar assinaturas, cadeia de hash, manifesto e bytes de anexos | Impressão digital do coletor mantida de forma independente; o administrador do host controla a chave de assinatura local |
| Espaço de trabalho local com uma testemunha independente | As verificações do arquivo, além da conformidade com um prefixo de registro anterior mantido pela testemunha | Chave de testemunha e registros confiáveis separadamente; o ponto de verificação vincula o prefixo já observado |
| [Captura do GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) | Atestado no GitHub do resumo do arquivo, do fluxo de trabalho aprovado e dos commits do coletor, do executador hospedado, da origem recente da sessão/chave e da integridade interna do arquivo | Política de verificador confiável, repositório de chamadores e pacote de atestados do GitHub; a coleta é executada sob o fluxo de trabalho fixado |
| [Implantação na nuvem](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/) | Registros do ciclo de vida e de acesso do provedor, estado do firewall e do Cloudflare, além do registro de execução assinado pelo coletor | Consultas somente de leitura ao provedor e à Cloudflare; a disponibilidade de verificações individuais depende do provedor |
| [VM confidencial Intel TDX](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx) | Citar a assinatura e o status da plataforma, vinculando-os à declaração do coletor, à composição e às medições do sistema operacional | Cadeia de confiança da Intel e métricas de implantação esperadas; mantenha os resultados de todas as verificações TDX exigidas |

Na aquisição selada, o coletor aprovado recebe dados por meio de uma conexão autenticada do Telegram dentro do ambiente verificado. O atestado vincula o arquivo a essa execução, de modo que a verificação abrange tanto a aquisição quanto a integridade posterior do arquivo. Isso depende do código aprovado e da cadeia de confiança da plataforma listada acima. A verificação de captura do GitHub requer uma sessão criada dentro da execução e rejeita capturas de sessões importadas.

O recibo de execução registra a versão do coletor, os hashes dos arquivos e as configurações de inicialização. A proveniência do GitHub e as medições TDX fornecem as verificações de ambiente; o registro de validação  identifica as configurações testadas.

O TgWitness assina as observações que coleta; o Telegram e os autores das mensagens não emitem essas assinaturas. Em um espaço de trabalho local, o material criado antes do primeiro ponto de verificação independente ainda depende do coletor e de seu detentor de chave. Os registros de cobertura descrevem o escopo selecionado e os resultados da coleta, enquanto os carimbos de data e hora externos verificados fixam no tempo o limite do arquivo ou diário confirmado.

## Anexos

Os arquivos são identificados por SHA-256 na pasta media/. Um evento media.saved vincula um hash e o comprimento em bytes a um evento de mensagem específico. Os nomes dos arquivos brutos são metadados, nunca caminhos locais. Os bytes de mídia são baixados de forma assíncrona; portanto, a exclusão imediata pode impedir a captura. A coleta desativada, arquivos com tamanho excessivo ou desconhecido, falhas no download e downloads interrompidos são exibidos como resultados. Uma falha no processo pode deixar arquivos parciais sem referência; eles não são incluídos nas exportações.

O exportador ZIP verifica os arquivos de mídia armazenados em relação aos seus nomes. As exportações em JSONL, CSV e HTML verificam as assinaturas dos eventos, mas não incluem os bytes de mídia. Os relatórios derivados são recursos de conveniência; o arquivo events.jsonl é a representação oficial dos eventos.

Uma exportação completa do chat salva os anexos, de acordo com as configurações de anexos do espaço de trabalho, na pasta media/, nomeados como SHA-256. Cada registro de mensagem em chat.json indica o nome do arquivo (`file`, `file_sha256`) ou o motivo de sua ausência (`file_status`), juntamente com o que o leitor viu ao redor do texto: links atrás do texto, origem do encaminhamento, botões de bot, assinatura, visualizações e o temporizador de exclusão automática. `verify.py` verifica se todos os arquivos nomeados estão no manifesto assinado sob aquele hash.

## Recibos de coleta e processamento duradouros (0,2)

Uma tarefa de mídia e seu evento de mensagem são confirmados em uma única transação. A tarefa armazena o descritor original da mensagem do Telegram; a observação assinada vincula seu SHA-256, conta e política de tamanho. A recuperação verifica essa vinculação antes do download. Ela nunca busca a mensagem atual e substitui silenciosamente por um anexo mais recente. Tarefas interrompidas são repetidas, enquanto a falha permanente permanece como um resultado explícito.

Cada espaço de trabalho possui seu próprio diário e identidade de assinatura. Um evento `process.started` inclui um ID de execução, relógios locais, versões de dependências, hashes de arquivos-fonte, conta/escopo inicial, e configurações de captura. Os heartbeats incluem o ID de execução, o tempo monotônico e o estado da fila. O comprovante de execução também pode ser baixado como um documento assinado separadamente. Para verificação do ambiente de execução, combine-o com o atestado do GitHub ou as verificações TDX descritas no escopo de verificação .

Pontos de verificação automáticos são mantidos localmente na inicialização, a cada cinco minutos durante a observação (**Parâmetros → Ponto de verificação assinado a cada**) e ao encerramento ordenado. A verificação na inicialização e a exportação comparam o diário com o ponto de verificação local mais recente mantido. Isso permite detectar um revertimento do banco de dados quando o ponto de verificação sobrevive. A retenção independente mantém essa referência disponível fora do espaço de trabalho; um carimbo de data/hora externo verificado, além disso, a fixa no tempo.

Após uma reinicialização, a posição de atualização salva do Telegram é retomada (`catch_up_from` em `observation.started`) e as atualizações perdidas são solicitadas. Uma verificação periódica registra `message.recovered` para mensagens perdidas e `message.missing_on_recheck` quando o Telegram não retorna mais uma mensagem salva; este último não é um aviso de exclusão e não indica quem excluiu nem a hora.

### Cópia e restauração externas (S3)

A cópia externa (Exportações, desativada por padrão) envia segmentos do registro, arquivos preservados e pontos de verificação com seus carimbos de data e hora, bem como exportações concluídas de conversas, para um armazenamento compatível com S3, criptografados com AES-256-GCM antes do envio, utilizando uma chave mantida no cofre do espaço de trabalho; a retenção por Object Lock se aplica quando o bucket for compatível. Sem a chave baixada, a cópia não pode ser lida. Restaure e verifique com `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

A restauração requer um diretório comum vazio. Os arquivos baixados e os objetos descriptografados permanecem em um armazenamento temporário privado até que todo o diário e todos os pontos de verificação retidos sejam validados. Caminhos de objetos inseguros, intervalos de segmentos inconsistentes e diários com duração inferior a um ponto de verificação são rejeitados; em caso de falha na verificação, nenhum arquivo restaurado é publicado. As verificações de retenção comparam o modo Object Lock e a data retornados com o prazo enviado no momento do upload (tolerância de arredondamento de um segundo). Um prazo expirado, inválido ou reduzido não é considerado como verificado. O status informa o objeto amostrado cuja retenção foi lida para aquela passagem de upload.

Mídias locais ausentes ou corrompidas são relatadas como erro da passagem e mantêm o cursor de mídia antes delas, de modo que o arquivo seja tentado novamente na próxima passagem; os arquivos, pontos de verificação e exportações posteriores a elas ainda são copiados. A restauração verifica todas as referências de mídia preservadas em relação aos hashes descriptografados e aos tamanhos registrados. Segmentos idênticos e sobrepostos do diário provenientes de uploads interrompidos são desduplicados; sobreposições conflitantes são rejeitadas. Os pontos de verificação criados durante um upload são adiados até que os registros do diário a que se referem tenham sido copiados, de modo que uma passagem concluída não publique um ponto de verificação antes de seu diário.

### Exportação contínua de instantâneos

As exportações em tempo real utilizam um instantâneo de leitura estável do SQLite. Sua parte inicial pode ser mais antiga do que o diário ativo atual quando o download for concluído. Um ponto de verificação criado após esse instantâneo pode indicar corretamente que o arquivo é menor; compare com um ponto de verificação no prefixo exportado ou anterior a ele, e não com um ponto de verificação posterior arbitrário.

## Preparação da RFC 3161 e verificação de respostas (0.2)

O modo de evidência (desativado por padrão) envia apenas o SHA-256 de cada ponto de verificação assinado às autoridades listadas na RFC 3161 e aos calendários do OpenTimestamps, pela rota do espaço de trabalho e nunca pelo MTProxy. As respostas são mantidas no `checkpoints/anchors/`, exportadas e verificadas pelo `verify.py` (o `--tsa-ca` verifica a assinatura TSA; confirme as provas do OpenTimestamps com o `ots upgrade` e o `ots verify`).

O painel prepara um arquivo de solicitação contendo os bytes canônicos do arquivo checkpoint.json, uma impressão digital da mensagem SHA-256 e um nonce aleatório no arquivo timestamp.tsq, somas de verificação e instruções. Nenhuma solicitação de rede é feita. A preparação não constitui um carimbo de data/hora confiável.

O `python -m tgwitness.anchor verify` chama o OpenSSL duas vezes: uma vez em relação aos bytes do ponto de verificação e outra em relação à solicitação original. É necessário um arquivo de CA confiável explicitamente; os certificados incluídos não são automaticamente considerados confiáveis. A verificação da solicitação é opcional na interface de linha de comando (CLI); portanto, mantenha e forneça a opção --request para verificar o nonce. O resultado indica se a verificação foi realizada. A assinatura do ponto de verificação do coletor e o registro ainda devem ser verificados separadamente com a impressão digital confiável do coletor.

A verificação checa a assinatura da resposta, os bytes do ponto de verificação e, quando fornecida, a solicitação original sob a confiança da CA especificada. As verificações de revogação e a validação do arquivamento de longo prazo após o vencimento do certificado estão fora do escopo do verificador atual. Consulte o [procedimento](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/) e [os resultados da validação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/).

## Registros opcionais no modo de evidência: dispositivos drand e Telegram

Mais dois registros podem ser executados nas mesmas passagens que os carimbos de data e hora. Ambos estão desativados por padrão e só entram em vigor enquanto o modo de evidência estiver ativado: Extras → Evidências e backups → **Mais testemunhas · opcional**, ou `"drand": true` e `"devices": true` em `POST /api/evidence`. Uma falha não interrompe a outra nem os carimbos de data/hora; o painel mostra o resultado mais recente de cada uma abaixo do formulário.

**drand** (`beacon.drand` ). Cada passagem grava a rodada mais recente da drand quicknet, a aleatoriedade pública da League of Entropy (uma rodada a cada 3 segundos), no diário: `chain` , `round` , `randomness` , `signature` , `round_time` e o `relay` que respondeu. Uma rodada verificada e imprevisível fornece uma referência temporal inferior para o material subsequente vinculado por hash. Um carimbo de data/hora verificado em um ponto de verificação posterior fornece uma referência temporal superior. Essas verificações delimitam o material vinculado; a cobertura da coleta é avaliada separadamente. O coletor consulta primeiro o `drand.cloudflare.com` e, em seguida, os retransmissores da Protocol Labs, por meio da rota do espaço de trabalho, com uma solicitação por passagem.

O `verify.py` verifica se cada valor aleatório corresponde ao SHA-256 de sua assinatura e se o tempo da rodada está correto, além de relatar as rodadas, o maior intervalo sem uma rodada e o atraso do relógio do coletor em relação ao drand. Ele não verifica a assinatura BLS. O `--check-drand` compara as rodadas com um relé da Cloudflare e um relé da Protocol Labs, todos eles ou uma amostra aleatória de 100 em um diário extenso; uma rodada que apresentar divergência falha na verificação.

Dispositivos **, Telegram,** (`account.devices`). Cada passagem lê as sessões da conta com `account.getAuthorizations`; a lista Telegram exibida em Configurações → Dispositivos é registrada: na íntegra quando houver alteração desde a passagem anterior, com os hashes de sessão `added` e `removed`, caso contrário, apenas sua contagem e SHA-256. Modelo do dispositivo, plataforma, aplicativo e versão, data de criação e última atividade, país e região são mantidos; endereços IP não são, pois as exportações de evidências saem de seu controle. A própria sessão do coletor permanece ativa o tempo todo, portanto, apenas a atividade de outras sessões conta como uma alteração. O `verify.py` relata a frequência com que a lista foi registrada e cada sessão nova e encerrada. Ele lê a lista apenas enquanto a observação está em andamento.

O que eles não mostram: o drand comprova apenas a ordem dos registros em relação ao tempo público, e a lista de dispositivos é a declaração do Telegram por meio do coletor, assinada pelo coletor como qualquer outro registro.

**Log do Cloudflare Gateway** (`cloudflare.gateway_dns`). Para um servidor que realiza a resolução por meio do Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/pt/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)), cada passagem copia o que o Gateway registrou desde a cópia anterior: um registro por janela de no máximo três horas com `from`, `until`, o `location_id`, o `address` do servidor quando houver um definido e o `queries` como `[at, name, type, rcode, decision, colo]`, mesmo quando não houver nenhum. Configure-o em **(log do Cloudflare Gateway)**: conta, localização, endereço opcional e um token somente leitura (Leitura de Análise de Conta Analytics Read; Zero Trust PII Read para manter um endereço de uma localização compartilhada). O painel verifica esses dados com uma solicitação antes de salvar; o token permanece criptografado e nunca entra no registro. O `verify.py` lista as janelas, os nomes mais pesquisados e qualquer momento não coberto por nenhuma cópia; um registro cuja contagem não corresponda às suas consultas é rejeitado. Uma janela que contenha mais de uma página de consultas em um único segundo mantém essa página e indica que o restante está faltando. A cópia é a resposta da Cloudflare por meio do coletor, assinada pelo coletor; em até 24 horas, qualquer pessoa com um token somente leitura pode compará-la com a Cloudflare.
