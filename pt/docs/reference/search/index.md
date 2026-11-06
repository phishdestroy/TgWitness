# Pesquisa de texto completo

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/search/

Encontre mensagens salvas por formas de palavras, frases exatas, domínios e @nomes de usuário, com as melhores correspondências exibidas primeiro, tendo o índice vinculado ao diário assinado.

[Análise de arquivos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/) · [OCR local e transcrição](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Pré-visualização.** No **“Diário”**, selecione **“Melhor correspondência · formas da palavra”** ao lado do campo de pesquisa. Os resultados são classificados pelo BM25 e correspondem a outras formas da mesma palavra: *“перевод”* encontra *“переводом”* e *“переводы”*, *“transfer”* encontra *“transfers”*, uma frase em chinês é encontrada sem espaços. A opção **“Mais recentes primeiro · texto exato”** mantém a pesquisa anterior de subcadeias de caracteres em todo o registro.

O índice é um dado derivado. Ele é reconstruído a partir do diário assinado, nunca é assinado por si só e nunca é incluído em uma exportação. Os registros originais não sofrem alterações.

## Sintaxe de pesquisa

| Escrever | Resultados |
| --- | --- |
| `перевод карта` | Registros que contenham ambas as palavras, em qualquer forma |
| `"переводом на карту"` | A frase exata, nesta ordem |
| `бонус OR подарок` | Qualquer uma das palavras |
| `перевод -казино` | Registros sem a palavra excluída |
| `example.com` | O domínio e seus subdomínios, inclusive em links ocultos e URLs de botões |
| `@username`, `t.me/username` | Menções e links da conta, além das mensagens que ela enviou |
| `#tag` | A hashtag |
| `+79991234567`, um endereço de carteira, um endereço de e-mail | O mesmo valor em texto ou links |
| `from:@username`, `from:123456` | Mensagens desse remetente |
| `chat:-1001234567890` | Um chat; ele só pode restringir o seu próprio acesso |
| `id:42` | Versões salvas da mensagem 42 |
| `since:2026-01-01 until:2026-01-31` | Período de observação; uma data sem horário abrange o dia inteiro |
| `kind:edited` | Apenas edições (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Texto reconhecido em vez de, ou junto com, mensagens |

Preposições e outras palavras funcionais são ignoradas quando outras palavras estão presentes. Letras semelhantes misturadas em uma palavra (um *“a”* latino dentro de uma palavra cirílica), letras Unicode de largura total e decorativas, bem como caracteres invisíveis, são normalizadas.

## Idiomas

O idioma é detectado em cada registro a partir de seu script e das letras:

| Script | Correspondência |
| --- | --- |
| Cirílico | Lemas em russo e ucraniano com [o pymorphy3](https://github.com/no-plagiarism/pymorphy3). Sem o dicionário opcional de ucraniano, é utilizado um stemmer ucraniano simplificado |
| Latim | Stemmer “Snowball” em inglês; os diacríticos são ignorados |
| Chinês, japonês, coreano, tailandês, laosiano, khmer, birmanês | Pares de caracteres sobrepostos: qualquer frase é encontrada sem espaços. As consultas em chinês são divididas em palavras com o jieba |
| Outros scripts | Palavras exatas |

O dicionário ucraniano (`pymorphy3-dicts-uk`) é distribuído sob a licença GPL-3.0, portanto, não vem instalado por padrão. Instale-o com `pip install "tgwitness[uk-dictionary]"`; o índice reconhece o novo analisador e se recompila automaticamente.

## Onde fica o índice

| Modo | Armazenamento | Utilização |
| --- | --- | --- |
| No disco (padrão) | `search/fulltext.sqlite3` no diretório do espaço de trabalho | Arquivos grandes; resiste a reinicializações |
| Apenas na memória | Nada fica armazenado no disco; é reconstruída a cada inicialização | Nenhuma cópia derivada do texto da mensagem no disco |
| Desativado | Sem índice; **Mais recentes primeiro · o texto exato** permanece | Instalações mínimas |

O administrador principal escolhe o modo em **Diário → Filtros → Índice de pesquisa** para cada espaço de trabalho. `TGWITNESS_FULLTEXT=disk|memory|off` Define o padrão para espaços de trabalho que não tenham sua própria escolha. Mudar para “memória” ou desativar exclui o arquivo. O arquivo de índice tem a mesma proteção que o diário: ele fica no diretório de dados privados . Não é criptografado e não faz parte de backups nem de cópias externas.

Novos registros são indexados em segundo plano em questão de segundos; uma pesquisa também indexa primeiro um pequeno acúmulo de registros, de modo que um registro salvo há pouco tempo seja encontrado. Um diário existente é indexado após a atualização sem bloquear o painel; até então, os resultados abrangem os registros indexados e o diário mostra o andamento. **A reconstrução do índice** recomeça a partir do primeiro registro.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` é necessário que o painel seja encerrado (caso contrário, código de saída 3). Com `--json`, a saída padrão contém apenas o resultado; o progresso é direcionado para a saída de erro padrão.

## Resultados e o diário assinado

O índice armazena o número de sequência e o hash do último registro do diário que ele abrange e os verifica em relação ao diário quando este é aberto. Um diário substituído, restaurado ou editado provoca uma reconstrução. Cada resposta relata essa posição, e cada ocorrência é recuperada do diário assinado por meio de seu número de sequência: o índice decide quais registros exibir e em que ordem, mas nunca seu conteúdo. O acesso ao chat é aplicado ao próprio campo de chat do diário, não ao conteúdo do índice.

## Texto reconhecido

O OCR e as transcrições permanecem em seus artefatos criptografados. Seu índice existe apenas na memória e é reconstruído quando uma tarefa de reconhecimento é concluída. Uma correspondência aparece em seu `media.saved` registro, rotulado como “reconhecimento automático”, com o mecanismo, o modelo e um trecho; nunca é apresentado como texto enviado no Telegram. O mesmo índice serve para a função **“Pesquisar texto reconhecido**”, que também continua a encontrar subcadeias de caracteres simples.

## Acesso

O acesso restrito ao chat localiza apenas registros de seus chats, incluindo o texto reconhecido de seus anexos. `chat:` e outros filtros podem apenas restringir esse conjunto. O status do índice exibido para o acesso restrito omite os totais do diário. Somente o administrador principal pode alterar o modo ou reconstruir o índice.

## Consulte o arquivo e o MCP

**A consulta ao arquivo** recupera suas fontes a partir desse índice quando ele estiver completo: as melhores correspondências entre os chats selecionados, com cada texto salvo contado uma única vez. São enviadas até 24 fontes; textos longos são cortados em torno de sua correspondência e marcados como truncados. Consultas sobre alterações recentes, versões salvas de uma mensagem e pesquisas enquanto o índice ainda está sendo construído utilizam a recuperação cronológica anterior. A visualização prévia mostra qual método foi utilizado.

Os clientes MCP podem chamar `search_messages` com `ranked=true` e acessar com `next_offset`. Conexões com escopo restrito recebem apenas seus chats.

Ranked pagination covers at most the first 1,000 results, regardless of page size. Narrow the query, chat or period to inspect further matches. Newest-first searches order messages, OCR and transcription results before selecting each page.

## Dependências

| Pacote | Licença | Por que |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lemas em russo e ucraniano; os dicionários são carregados localmente |
| snowballstemmer | BSD-3-Cláusula | Radicais em inglês, Python puro |
| jieba | MIT | Segmentação de consultas em chinês, Python puro (apenas distribuição do código-fonte) |
| pymorphy3-dicts-uk (opcional) | GPL-3.0 | Dicionário completo de ucraniano |

É necessário o SQLite FTS5 com o `unicode61` tokenizador; ele faz parte do SQLite nas versões atuais do Python. Sem ele, a pesquisa de melhor correspondência informa que não está disponível.

## Avaliação comparativa

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`Cria um diário assinado determinístico com mensagens mistas em russo, ucraniano, inglês, chinês e japonês, com links e identificadores em 200 chats, constrói o índice e mede o tempo de pesquisas típicas (50 resultados, mediana de 7 execuções).

Testado no Windows 11, Intel Core i9-13900K, 128 GB de RAM, Python 3.12.10, SQLite 3.49.1, dados em uma unidade exFAT, analisador `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Medida | Resultado |
| --- | --- |
| Diário assinado | 1.000.000 de mensagens, 1,50 GiB, gravadas em 19 minutos |
| Criação de índice a partir do diário | 71 s, cerca de 14.141 mensagens por segundo |
| Arquivo de índice | 58 MiB, 3,8% do diário |
| Pesquisar logo após um novo registro | Mediana de 8 ms, p95 de 9 ms |
| Pesquisa de subcadeia anterior, mesmo diário | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Pesquisar | Registros correspondentes | Melhor correspondência, mediana | p95 | Mais recentes primeiro, mediana |
| --- | --- | --- | --- | --- |
| Palavras comuns e suas formas: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Duas palavras: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Palavra rara: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Frase exata: `"переказ коштів на картку"` | não contabilizado | 35 ms | 36 ms | 6 ms |
| Domínio com subdomínios: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @username: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chinês sem espaços: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japonês: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Raiz em inglês: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| OU e exclusão: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filtro de bate-papo: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filtro de período: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Uma frase exata é verificada literalmente nos candidatos em ordem de classificação até que a página esteja cheia; portanto, seu total não é contabilizado. O tempo de resposta aumenta com o número de registros correspondentes; restringir o chat ou o período torna as buscas amplas mais rápidas. O corpus sintético repete um vocabulário reduzido, de modo que palavras comuns correspondem a muito mais registros do que em chats reais.
