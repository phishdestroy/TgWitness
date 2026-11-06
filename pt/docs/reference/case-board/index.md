# Referência ao Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/

Marcadores, destaques exatos, trechos de ação, discussões, acesso restrito e o histórico de anotações assinadas utilizado pelo Case Board.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/pt/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

O Case Board oferece à equipe de investigação uma visão de trabalho compartilhada do material salvo. Marque uma observação, destaque uma passagem exata, salve uma série de ações e discuta-as com os colegas. Os cartões mantêm suas referências de fonte e o histórico de revisões assinado. As anotações da equipe permanecem no espaço de trabalho, identificáveis separadamente das observações originais do Telegram.

[Modelo de evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) · [Acesso](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/) · [Relatórios](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/)

![Feed de investigação sintética](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

**On this page**

- [Work with a case](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/#work-with-a-case)
- [Permissions](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/#permissions)
- [Stored contracts](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/#stored-contracts)
- [API and exports](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/#api-and-exports)
- [Operating limits](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/#operating-limits)

## Trabalhar com um caso

Abra **Investigação → Case Board** no modo Padrão ou Especialista. O idioma segue o do painel. Use **o** **botão** **“Para o quadro”** ao lado de um registro do diário ou de uma mensagem de bate-papo salva, ou selecione-o e pressione **B**. O marcador é adicionado à Caixa de Entrada com um clique. Edite seu título, rótulos e nota, ou mova-o para uma coleção. Um cartão alterado anexa uma revisão assinada; removê-lo preserva o histórico.

Para um primeiro caso, escolha uma coleta e adicione os registros que respondam a uma pergunta. Use os comentários para revisar a interpretação e, em seguida, **a opção “Apresentação”** para percorrer os cartões e o contexto da fonte. Escolha o material do “Case Board” separadamente no [“Report Studio”](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/) ao preparar o produto final. Salvar uma fatia não configura automaticamente os filtros de dados de um relatório.

Selecione o texto dentro de uma mensagem de bate-papo salva para exibir **“Destaque → quadro**”. Selecione a cor e adicione uma nota. O servidor verifica a citação exata e a versão salva, incluindo emojis, texto RTL e marcas de combinação. A interface não mapeia uma seleção por meio de texto mascarado ou transformado.

Clique com a tecla Shift pressionada em dois registros em um chat para usar **o “Slice between**”, utilize **o “Slice by time**” ou salve os filtros atuais do “Journal” para chat, período e tipo de evento. Um “slice” salvo possui seu próprio predicado de autoridade: abri-lo no “Journal” também aplica múltiplos chats, limites de número de mensagens e filtros de atores . A opção **“Mostrar registros adicionados desde o marcador”** isola as adições posteriores. Alterar os filtros do Journal encerra a fatia. Em “Pessoas”, **a opção “Dividir as ações desta pessoa”** usa o ID do ator registrado; ela não presume que o autor da mensagem tenha editado, excluído ou reagido a uma mensagem.

A caixa de diálogo de seleção exibe uma prévia das contagens antes de permitir a criação. “`all`” inclui todos os tipos registrados, incluindo capturas de tela, edições, exclusões, reações, atualizações de participação/serviço, ações próprias, botões, resultados de mídia, mensagens recuperadas e tipos de eventos futuros. A seleção descreve observações salvas. Os avisos de exclusão de bate-papos desconhecidos constituem um contexto separado, disponível apenas para acesso a todo o espaço de trabalho, nunca atribuídos a um dos bate-papos selecionados.

As coleções têm um escopo de chat declarado. Um escopo vazio significa todo o espaço de trabalho. Uma coleção não pode conter cartões fora de seu escopo; um participante com acesso limitado a um chat não pode ler uma coleção mais ampla. A Caixa de Entrada é uma coleção virtual para cartões não atribuídos. A pesquisa e os filtros abrangem apenas cartões visíveis; threads e menções herdam o acesso do cartão pai. Comentários removidos têm uma marca de remoção na discussão. Nenhum histórico de visualização é registrado.

**A apresentação** abre todos os cartões da coleção escolhida, com as visualizações “Cartão”, “Contexto da fonte” e “Comentários da equipe”, além dos controles de teclado “Anterior”/“Próximo”. Ela não oferece controles de edição. O feed comum é paginado; a apresentação carrega sua lista em páginas e recupera os detalhes de um cartão por vez.

## Permissões

Todas as operações exigem acesso a “`view`”, ao escopo da área de trabalho/chat e a “`board.read`”. “`board.write`” adiciona cartões, comentários, movimentações e status de “aberto”/“revisado”. “`board.manage`” permite o gerenciamento da coleta, status de “confirmado”/“rejeitado”, revisões e remoção de cartões de outras pessoas. Um status é uma decisão da equipe, não um resultado de verificação criptográfica.

Acesse as configurações pré-definidas do formulário: Revisor = leitura; Analista = leitura/gravação; Operador = leitura/gravação/gerenciamento, além de suas permissões existentes. As concessões existentes não conferem novos direitos automaticamente. O administrador principal possui todos os direitos e publica como **Administrador principal**. Use concessões nomeadas para atribuição. As menções listam apenas os acessos atuais capazes de ler o cartão pai completo.

Uma autorização para o chat A não pode obter um cartão ou fragmento para A+B, mesmo adivinhando seu ID ou fornecendo um `target.chat_id` falso. Os metadados do alvo são resolvidos a partir do hash do evento assinado no servidor. Coleções, contagens de discussões, cartões relacionados e notificações em tempo real são filtrados antes da resposta. exportações exigem `export`, bem como `board.read`; um exportador existente sem acesso ao quadro recebe o arquivo de evidências comum, sem as notas da equipe. O SSE verifica novamente as autorizações atuais antes de cada lote.

## Contratos armazenados

Assim como as observações, as anotações são gravadas de forma transacional em uma tabela SQLite de apenas acréscimo no espaço de trabalho. O arquivo `annotations.jsonl` é sua exportação canônica exata a partir do mesmo instantâneo de leitura que o `events.jsonl`. Não há um segundo repositório de anotações concorrente nem nenhum evento de diário no `board.activity`.

Cada linha contém exatamente:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

O exemplo abreviado acima ilustra o envelope; as cargas úteis reais incluem suas configurações padrão de modelo e campos de destino resolvidos pelo servidor. Os esquemas de solicitação da API estão em [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json), gerados a partir dos modelos Pydantic em tempo de execução pelo script `python tools/build_board_schemas.py`. Campos de solicitação extras são rejeitados. Os IDs são gerados no lado do servidor quando omitidos. Autoria, hora, instantâneo e assinatura não podem ser fornecidos pelo chamador. Os IDs de concessão nomeados seguem o formato hexadecimal de 16 caracteres existente do Access; os IDs de cartão têm 32 caracteres hexadecimais.

O JSON canônico é em UTF-8, com chaves de objeto ordenadas, sem espaços entre tokens, Unicode sem escape, e sem NaN/infinitos. O hash da anotação é o SHA-256 do objeto canônico contendo o `format: "tgwitness-annotations-v1"` e todos os sete campos do envelope até o `previous_hash`. Essa tag de formato separa seu domínio de hash das observações. A assinatura é Ed25519 sobre os 32 bytes brutos do hash. A sequência começa em 1. As revisões mantêm o ID do cartão e nomeiam o hash de anotação anterior em “`supersedes`”; elas não podem alterar o escopo do chat. Movimentações, status e remoções são registros separados. A tabela SQLite rejeita UPDATE e DELETE.

O arquivo `case-board.json` contém `{statement, signature}`. A declaração canônica é assinada pela chave do espaço de trabalho e contém `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` e `state`. O estado é uma reprodução determinística: `annotations_head`, uma matriz ordenada de `items` (coleções, cartões, comentários, incluindo tombstones) e `status_history`. Os itens mantêm seu último hash de anotação, sequência, autor e hora, bem como o criador original e a hora de criação ao longo das revisões. A reprodução verifica revisões, pais, referências de coleções e IDs de ação duplicados. O ``manifest.json`` e novos pontos de verificação também vinculam o ``annotations_head``. Mantenha um ponto de verificação de forma independente para detectar truncamento ou reescrita com uma chave de assinatura copiada.

### Versões em texto

`range.start` é um deslocamento de ponto de código Unicode com base em zero, `length` é uma contagem positiva de pontos de código, e `quote` deve ser igual à substring exata de `payload.text` ou `payload.caption` no evento de destino. Não é aplicada nenhuma normalização NFC/NFKC, conversão de maiúsculas/minúsculas ou normalização de grafemas. As fatias de string do Python e o ``Array.from(text)`` do JavaScript implementam a mesma indexação. A combinação de marcas e emojis ZWJ pode ocupar vários pontos de código. ``range.version`` é o hash do evento de destino, não a versão atual da mensagem nem o deslocamento de entidade UTF-16 do Telegram. Edições posteriores nunca reposicionam um destaque automaticamente.

### Identidade e hora do segmento

A `query` aceita exatamente um `chat_id` ou `chat_ids` não vazios, `from`/`to` inclusivos opcionais, limites inclusivos de ID de mensagem (apenas um chat), `kinds: "all"` ou tipos de curinga exatos/com prefixo, `actors` explícitos, `search`, `hide_system` e `include_unscoped`. Os grupos de tipos de diário se expandem para seus predicados exatos. A pesquisa utiliza a pesquisa de carga útil do diário com NFC/sem distinção de maiúsculas e minúsculas, sem alterar o texto-fonte assinado. As datas exigem um fuso horário e são normalizadas para UTC. As datas filtram **`observed_at`**. O ``source_at`` do Telegram é exibido separadamente. Uma exclusão sem um carimbo de data/hora de origem não tem hora de exclusão inventada. Um registro tardio observado fora de um intervalo de tempo não entra nele; um intervalo de IDs de mensagem pode incluir uma exclusão posterior para esses IDs de mensagem.

O `snapshot` fixa a hora de criação, a sequência do diário/limite de hash, a contagem de correspondências, a primeira/última sequência e o `result_hash`. Este último é o SHA-256 da matriz JSON canônica em UTF-8 dos hashes de eventos correspondentes classificados lexicograficamente, incluindo `[]` para uma fatia vazia. Ele também contém contagens exatas de tipos e uma miniatura do tempo de observação com 24 intervalos. Uma fatia armazena uma consulta, não registros duplicados da fonte . Na exportação, `board/slices/<id>.json` lista os hashes atuais e as sequências adicionadas/removidas. O verificador reconstrói o resultado original no momento da criação e, em seguida, o resultado atual. Registros adicionados são relatados como um fato de alteração. A remoção de um evento original rompe a cadeia de evidências imutável; ela não é aceita silenciosamente como uma remoção comum de uma fatia.

Os instantâneos de reações apresentam listas incompletas de participantes recentes. O explorador compara instantâneos adjacentes do mesmo chat/mensagem, incluindo um antecessor fora do intervalo, e relata as diferenças agregadas nas contagens **entre as observações**. Não se afirma que os participantes recentes ausentes tenham removido uma reação. O primeiro instantâneo não possui um estado anterior inferido. As observações dos atores permanecem atribuídas ao instantâneo no qual foram fornecidas, e não a um momento de ação inventado.

## API e exportações

`GET /api/board` aceita collection/chat/author/label/state/from/to/q/kind/comments, offset/limit e a ordem mais recente/mais antiga. `GET /api/board/card/{id}` retorna um cartão, pré-visualização da fonte, thread, histórico de status e cartões relacionados. A subrota dos participantes retorna opções de menções elegíveis. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` acrescenta um registro. `POST /api/board/slice-preview` calcula uma consulta. Os registros da fatia são paginados em `GET /api/board/slice/{id}/records`; o recálculo sempre usa o snapshot de leitura estável atual. `/api/stream` em tempo real emite notificações do `board` sem carga útil, separadamente dos cursores do diário.

`GET /api/board/export` retorna um documento assinado. O acesso restrito ao chat recebe uma **divulgação** assinada e claramente identificada, nunca as anotações de outro chat nem a cadeia completa. Os arquivos ZIP com evidências completas contêm o arquivo `annotations.jsonl`, o `case-board.json` assinado e anexos JSON de trechos. As configurações de relatório em HTML/PDF/JSON permitem selecionar “sem quadro”, marcadores/segmentos sem discussão ou cartões com comentários. A seção separa explicitamente as opiniões da equipe das observações. Os filtros de dados do relatório também restringem as notas legíveis; os arquivos-fonte completos e assinados no ZIP de evidências permanecem intactos.

`GET /api/board/slice/{id}/export` gera um trecho JSON assinado de `tgwitness-board-selection-v1`; `?format=csv` gera uma tabela prática sem uma assinatura independente. Mantenha o JSON e o ZIP:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

A verificação de seleção autentica a declaração assinada, os registros de fonte exatos e a integridade de sua consulta no limite especificado. O arquivo ZIP de evidências pode ser mais recente, mas deve conter esse prefixo. Um alvo pendente é relatado explicitamente. Um instantâneo de fatia original diferente, uma anotação alterada, um estado de reprodução incompatível ou uma fonte alterada resultam em falha. Arquivos antigos sem anotações mantêm seu comportamento de verificação existente.

A opção padrão para a transferência é **“Não incluir**”. A inclusão explícita projeta cartões através dos registros já minimizados, omite alvos inacessíveis/omitidos, retém destaques cujo texto de origem foi minimizado, limpa o texto da equipe com as mesmas regras de menção/contato e, opcionalmente, substitui rótulos de investigadores por R01, R02… nos metadados e ocorrências conhecidas nas notas. Nenhum arquivo original ` `annotations.jsonl`` é divulgado. O sidecar assinado ``tgwitness-case-board-handover-v1`` e o relatório contêm o mesmo material minimizado. As contagens de fatias descrevem apenas os registros divulgados, com os detalhes originais do autor do snapshot/consulta retidos. Nomes em texto livre desconhecidos pelo minimizador ainda requerem revisão, assim como ocorre em transferências comuns. Esta versão derivada não pretende preservar as assinaturas das anotações originais após a supressão.

## Limites operacionais

Os parâmetros incluem limites flexíveis de 10.000 cartões e 50.000 comentários, uma página de fatia com até 5.000 registros e controle de visualização de mídia. Os limites flexíveis emitem avisos sem excluir o histórico. As páginas de feed têm no máximo 200 cartões. Trechos de fatias JSON independentes são limitados a 64 MiB; restrinja a consulta ou use o ZIP assinado para materiais maiores. O verificador independente limita a reprodução de anotações a 256 MiB. Nenhuma notificação externa de comentários está habilitada ou implementada pelo Case Board.

A aceitação automatizada do recurso utiliza dados fictícios e um transporte simulado do Telegram para verificar o armazenamento, o acesso, a renderização e as exportações. Consulte [o escopo de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) para conhecer o alcance das verificações das evidências.
