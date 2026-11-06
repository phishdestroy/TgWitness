# Configuração e verificação de relatórios

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/

Filtros de relatório, oito modelos, predefinições de conteúdo, históricos de alterações salvos e a avaliação incluída nas exportações assinadas.

Transforme as observações selecionadas em um relato legível do caso: sua questão, escopo, alterações salvas, gráficos, conclusões e referências de fontes. Cada relatório oferece ao destinatário uma maneira de verificar o material entregue e inspecionar a cobertura da coleta.

A seção **“Base de confiança e limitações”** aparece nos relatórios de diário, transferência, bate-papo, conta e compartilhamento. Os PDFs do diário e da transferência utilizam a mesma avaliação que seu arquivo “`report.json`” assinado. Os manifestos ZIP contêm o “`case_assessment`” no manifesto assinado. Essa avaliação acompanha o material exportado. As observações originais mantêm suas assinaturas existentes.

## Formatos dos documentos e ordem de leitura

### Estúdio de Relatórios

Abra **“Exportações” → “Configurar” e visualize a pré-visualização**. Navegue por **“Dados” → “Design e conteúdo” → “Pré-visualização**”:

1. Use todo o espaço de trabalho ou selecione conversas, autores, incluindo datas de observação em UTC e tipos de eventos. Carregue o catálogo para pesquisar conversas e autores, ou insira seus IDs do Telegram. Os filtros de autor correspondem aos IDs de remetentes registrados; um aviso de exclusão sem remetente não corresponde a um filtro de autor.
2. Escolha um layout de página e, em seguida, selecione gráficos, rótulos dos participantes, a transcrição e suas conclusões por escrito. Ao alterar o layout, essas opções são mantidas.
3. Gere a visualização. Ela mostra contagens reais, atividades, participantes, registros de amostra, alterações salvas e intervalos de números de mensagens ausentes. Alterar uma opção torna a visualização desatualizada. Salve antes de baixar o HTML, o PDF assinado, o JSON assinado ou o ZIP com as evidências.

A visualização dos dados conta o prefixo completo e estável do diário, não uma amostra inicial. Apenas as linhas de amostra exibidas e as listas longas são delimitadas; suas contagens omitidas são mostradas. Uma exportação posterior gera um novo instantâneo estável, portanto, a coleta em andamento pode aumentar os números. O escopo, as contagens e a identidade da fonte estão incluídos no relatório assinado. Abrir ou visualizar o formulário não o salva.

**Escolha a versão destinada ao destinatário.** Os gráficos e a transcrição utilizam os registros selecionados. Integridade, custódia e cobertura descrevem o diário de origem completo. O arquivo ZIP de provas contém seus registros originais e anexos. Utilize [uma transferência minimizada](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#handover-extract) quando o destinatário deva receber apenas dados selecionados e permitidos.

### Leia as edições, exclusões e IDs ausentes

Uma edição mostra o texto salvo **“Antes”** e **“Depois”** e destaca as palavras alteradas. Uma exclusão mostra a última versão salva antes do aviso. Se nenhum conteúdo anterior tiver sido capturado, o relatório indica isso. Ao selecionar apenas edições ou exclusões, as versões anteriores permanecem disponíveis como contexto explicitamente identificado fora dos filtros. Mensagens não relacionadas não são adicionadas a esses históricos.

**IDs de mensagens não observadas** são lacunas entre números conhecidos nos chats selecionados e o intervalo de IDs derivado da data. Cada registro de fonte conhecido é verificado antes de declarar um número como não observado: filtrar outro autor, um tipo de evento ou uma data não pode criar uma lacuna falsa. Mensagens salvas adjacentes são rotuladas como contexto. Um número ausente não comprova que uma mensagem existiu ou foi excluída; avisos de exclusão e novas verificações malsucedidas permanecem como tipos de eventos distintos.

### Escolha um design

Estão disponíveis oito modelos de página para relatórios em HTML (diário e bate-papo individual) e PDF assinado. Eles utilizam os mesmos registros e cálculos, com capas, tipografia, títulos de capítulos, tabelas e espaçamento diferentes.

| Design | Estilo de leitura |
| --- | --- |
| Clássico | Um dossiê tradicional com capa escura e seções numeradas. |
| Editorial | Uma página de rosto com serifa emoldurada, margens largas e uma barra de capítulos estreita. |
| Resumo | Uma capa compacta com lombada azul-marinho, títulos curtos e tabelas com espaçamento reduzido. |
| Análises | Capa no estilo de pesquisa, tabelas modulares e figuras em fonte monoespaçada. |
| Técnico | Um registro pautado, uma barra de referência numerada e tabelas de comparação precisas. |
| Visão geral | Uma capa panorâmica, espaçamento generoso e figuras de resumo em destaque. |
| Série de leitura | Uma barra lateral e capítulos agrupados para conclusões, escopo, alterações e o diário de observações. |
| Ledger e margem | Capítulos numerados com margens amplas, tabelas e gráficos precisos e uma transcrição separada das mensagens. |

O design é salvo por área de trabalho e registrado no manifesto de exportação assinado. O HTML funciona offline, suporta temas claros e escuros e se adapta a telas estreitas e a idiomas escritos da direita para a esquerda. Os PDFs nativos utilizam fontes integradas; o design editorial inclui a fonte Noto Serif sob sua licença SIL Open Font License integrada. As séries de leitura e o “Ledger & margin” também se aplicam a visões gerais de contas, bate-papos de contas e compartilhamento de cópias.

Os PDFs em chinês, japonês e coreano também precisam de uma fonte adequada no servidor, como a Noto Sans CJK, instalada em todo o sistema ou colocada no diretório `TGWITNESS_FONT_DIR`. Quando ela não estiver disponível, o arquivo ZIP mantém os relatórios em HTML e JSON.

Esses dois designs incluem um diário legível sem JavaScript. Para grandes exportações, essa visualização contém até 500 registros completos dentro de um limite de entrada de 8 MiB; o relatório indica o limite e fornece links para o visualizador completo e os registros de origem. O diretório de contas e o índice de relações descrevem essa mesma amostra de leitura, não todos os participantes. Os gráficos do diário completo mantêm seu escopo definido separadamente.

### Selecione o conteúdo

| Índice predefinido | Incluído por padrão |
| --- | --- |
| Dossiê do caso | Atividade, horários de observação, participantes, conversas e a transcrição do registro. |
| Resumo | Uma visão geral das atividades sem classificações dos participantes nem a transcrição. |
| Revisão de atividades | Atividades, horários de observação, participantes, conversas e composição, com referências às fontes e números exatos. |
| Relatório personalizado | Sua própria combinação de gráficos, transcrições e visualizações. |

Alterar uma predefinição mantém seu layout, os detalhes do caso e a análise escrita. Verificações de integridade, cobertura, limitações e instruções de verificação permanecem em cada layout. Os registros de origem no arquivo ZIP permanecem inalterados quando um gráfico ou transcrição é ocultado.

As **“Notas de Exame”** opcionais contêm a pergunta, o método, os resultados e a conclusão redigidos pelo autor do relatório. Cite o arquivo de origem e os números dos registros nos resultados. A assinatura preserva essas declarações do autor juntamente com o relatório; as observações da fonte e a interpretação do autor permanecem identificáveis. As transferências simplificadas omitem essas notas privadas e os gráficos completos do diário. As opções de gráficos e exames se aplicam aos relatórios do diário.

Selecione a atividade ao longo do tempo, o mapa de calor de dia da semana/hora em UTC, as classificações dos participantes, as classificações dos chats e a composição dos registros. Escolha de 5 a 30 grupos classificados e pseudônimos neutros dos participantes ou IDs de conta. Remetentes desconhecidos e os demais participantes aparecem em linhas separadas. Os pseudônimos afetam apenas os gráficos; os registros de origem ainda contêm suas identidades.

A visualização do design é atualizada a partir do rascunho não salvo, utilizando a capa de produção, a análise e os componentes de gráficos, limitada às correspondências nos primeiros 50.000 registros de origem. A visualização de dados abaixo calcula a seleção completa. Ela é explicitamente não assinada e não mantém as edições. Os botões “Capa” e “Gráficos” alternam entre as seções. Esta não é uma visualização completa do PDF. **“Salvar configurações do relatório”** aplica as opções a exportações futuras; arquivos assinados existentes são imutáveis. O PDF utiliza a capa escolhida, tipografia, layout de capítulos e os mesmos agregados selecionados que o HTML e o JSON assinado.

A avaliação de confiabilidade, as limitações de cobertura e as instruções de verificação permanecem presentes. Ocultar gráficos ou a transcrição legível não remove as linhas de fontes oficiais do arquivo ZIP. Séries de gráficos desativadas são omitidas do JSON analítico; use uma exportação minimizada para restringir a divulgação dos registros de origem.

Os filtros de seleção de dados se aplicam aos relatórios de registro; as exportações de contas e compartilhamentos mantêm seu próprio escopo de aquisição e divulgação.

As preferências compartilhadas de design/gráficos são mantidas nas novas exportações de bate-papos/contas e nas visualizações de compartilhamento de contas. As configurações de idioma e privacidade da conta e do compartilhamento permanecem independentes; notas privadas de casos e de análise não são copiadas para essas exportações. Os relatórios de conta e de compartilhamento permanecem em HTML, protegidos por seu manifesto de arquivo assinado. O diário, a transferência de diário minimizada e os kits de bate-papo único também fornecem PDFs assinados.

### O que os gráficos mostram

A atividade do diário e os mapas de calor contabilizam **observações** novas, históricas, recuperadas, editadas, excluídas e ausentes na nova verificação, de acordo com a hora da observação do coletor em UTC. Heartbeats e recibos de anexos são excluídos. As classificações dos participantes contam apenas observações de mensagens novas, históricas e recuperadas: um remetente não é declarado como editor ou exclusor. Observações repetidas podem descrever a mesma mensagem do Telegram.

A análise de registros mantém contagens por tipo, referências ao primeiro/último registro e o SHA-256 do arquivo de origem ` `events.jsonl``. As figuras incluem valores exatos em HTML e PDF. Os intervalos diários passam a ser mensais após 366 dias registrados; os gráficos combinam esses dados em, no máximo, 36 intervalos de largura igual. Mais de 100.000 identificadores distintos ou 1.200 meses fazem com que o gráfico afetado fique indisponível, enquanto as contagens gerais exatas permanecem disponíveis.

Os gráficos de instantâneos e compartilhamento de contas contam apenas as linhas de mensagens não relacionadas ao serviço incluídas, utilizando a hora registrada das mensagens. Os agregados de compartilhamento são calculados após a supressão e a filtragem. Esses gráficos utilizam, no máximo, 90 intervalos de data UTC de largura igual e retêm até 10.000 valores de agrupamento; contagens excedentes são explicitamente declaradas e reconciliadas. O último intervalo pode ser mais curto. Datas desconhecidas ou imprecisas não são incluídas nos gráficos de tempo.

Um intervalo vazio significa que não há observações incluídas; consulte a cobertura para verificar se há lacunas. Esses gráficos descrevem as atividades salvas. Remetentes desconhecidos permanecem em uma categoria separada, e cada verificação é relatada individualmente.

Quando incluído, o arquivo `analytics.json` é protegido pelos hashes assinados do arquivo. O `report.json` do diário incorpora o mesmo agregado selecionado. A verificação de assinatura detecta bytes alterados. Para verificar os números, recalcule os agregados do diário com `report_analytics.Analytics` e `selected`, ou os agregados do snapshot com `snapshot_analytics.collect` e `project`.

### Anomaly indicators

**Preview.** Evidence reports add an **Anomaly indicators** section computed by registered processors (`tgwitness/metrics/`, one file per metric). The report names every processor that ran with its version, and prints its method under its table, so the computation can be repeated from `events.jsonl` with `tgwitness.metrics.run`.

| Processor | O que ele mostra |
| --- | --- |
| `first_time_posters_over_time` v1 | First-time posters and messages per UTC day．A flag requires at least five first-time posters and three times their median，with message volume at most 1.5 times its median．The baseline uses at least seven observed days within the previous 14 calendar days，after seven days of warm-up． |
| `service_vs_message_ratio` v1 | Distinct saved message numbers per chat and the share used by service messages. It describes a numbering; it does not explain a particular missing number. |
| `join_leave_per_month` v1 | Joins, departures and removals or bans per month, one per person, chat, change and day. |
| `pinned_per_month` v1 | Pin service messages, unpin notices, and pinned messages added or removed between chat-state snapshots, per month. |

**Parameters → Report metrics** selects processors and the number of displayed rows， including in filtered reports．Daily and monthly tables show recent rows，service-share tables rank chats by saved message count．Totals cover every row．

A partir de uma versão do código-fonte, crie todos os oito designs listados acima a partir da mesma revista fictícia:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Abra o arquivo `index.html` resultante para comparar relatórios HTML completos, PDFs assinados e arquivos ZIP. Cada layout utiliza o mesmo diário de origem. Use um novo diretório de saída para cada execução, de modo que os exemplos assinados anteriormente sejam preservados.

![Dossiê HTML fictício](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

O HTML começa com uma capa do caso e números-chave. O mapa de evidências numerado contém links para cada conclusão, seus fatos de apoio, limites e revisão independente. Registros pesquisáveis e referências estáveis aos registros permanecem disponíveis no visualizador offline. O design se adapta a telas estreitas, tanto em temas quanto em navegadores sem JavaScript.

O PDF assinado possui uma capa A4 exclusiva, referência do relatório e código QR, um resumo executivo, um mapa de evidências, conclusões numeradas e marcadores de documentos. Seus cabeçalhos e rodapés identificam o relatório. Um código QR identifica o material; ele não é um resultado de verificação independente. As impressões do navegador são distintas deste PDF assinado criptograficamente.

A linha do tempo de observação posiciona os períodos de observação registrados e as interrupções no mesmo eixo UTC. Espaços em branco não significam cobertura inferida; as tabelas detalhadas mantêm os intervalos exatos. O arquivo ZIP contém os relatórios legíveis, o JSON assinado, os registros de origem e as instruções de verificação.

Crie um dossiê novo e fictício em inglês/russo/alemão com o ambiente de desenvolvimento instalado:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Cada diretório de idioma contém `report.html`, `report.pdf`, `report.json` e `dossier.zip`. Os diretórios de amostra existentes nunca são sobrescritos. Nenhuma conta do Telegram, serviço externo de registro de data e hora ou conexão de rede é utilizada para criá-lo.

![Primeiras três páginas do PDF fictício assinado](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Análise de um caso concreto

Para um diário com 1.200 entradas e um carimbo de data/hora validado na entrada 1.000, o relatório identifica 200 entradas posteriores fora do intervalo desse carimbo de data/hora. Trata-se de um limite superior para a existência de um ponto de verificação, não de uma prova da hora de envio de cada mensagem . Se outros três arquivos de carimbo de data/hora falharem na validação ou não puderem ser validados, eles são contados separadamente e não podem fornecer uma conclusão positiva.

Um carimbo de data/hora válido deve satisfazer todas estas verificações: sua impressão corresponde ao ponto de verificação, sua assinatura está encadeada a uma raiz TSA confiável no momento do carimbo, e a assinatura, a chave, a contagem e o cabeçalho do ponto de verificação correspondem exatamente ao prefixo do diário. A simples análise de um carimbo de data/hora ou a posse de um recibo OTS não é suficiente. O leitor deve escolher de forma independente a raiz TSA confiável e repetir a verificação. O OTS precisa de sua própria verificação de confirmação do Bitcoin.

| Status do relatório | Significado |
| --- | --- |
| Verificado durante a exportação | O exportador realizou a verificação indicada; ainda é necessária uma repetição independente. |
| Registrado; revisão necessária | A observação subjacente ou a declaração do operador é registrada; não se trata de uma confirmação independente. |
| Não incluído neste texto | O texto não apresenta nenhuma evidência que comprove essa afirmação. Ele não afirma que não exista em nenhum outro lugar. |
| Não verificado de forma independente | O relatório não fornece um resultado de verificação independente. |
| Incompleto ou indisponível | Falta algum material ou verificação obrigatória, ou ela está incompleta ou não foi bem-sucedida. |

Analise cada verificação separadamente, juntamente com a cobertura da coleta registrada.

## O que uma configuração robusta deve preservar

1. Antes de confiar na coleta, guarde a impressão digital da chave do coletor por meio de um canal confiável separado. Compare essa referência com a chave de assinatura da exportação.
2. Mantenha pontos de verificação com carimbos de data/hora independentes e, quando utilizado, um diário de testemunho fora do controle administrativo do coletor. Compare-os com o diário exportado para verificar seus limites anteriores.
3. Escopo da aquisição de registros, lacunas, filtros, limites e alterações na coleta. Explique os períodos ausentes relevantes para a alegação em questão, mantendo uma distinção clara entre IDs de mensagens não observadas, avisos de exclusão e novas verificações malsucedidas.
4. Preserve os arquivos ZIP originais e seus hashes. Registre cada detentor, transferência, data e finalidade. Mantenha as declarações atribuídas aos operadores e as notas do caso junto com eles.
5. Para mensagens de voz confidenciais, preserve e verifique de forma independente a citação, o desafio, a cadeia de certificados da Intel, as medições, a fonte exata e as condições de manuseio das chaves. Mantenha o resultado da verificação do atestado junto com os artefatos revisados.

Consulte [o escopo de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope) para as verificações de aquisição, integridade do arquivo, tempo e cobertura da coleta em cada modo.

## Revisão do destinatário

Utilize uma instalação confiável do TgWitness e uma impressão digital obtida de forma independente:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

O arquivo ZIP do Witness deve provir de uma fonte independente e confiável; preserve também sua chave e sua proveniência. Mantenha os comandos, a versão da ferramenta, as saídas, os hashes de entrada revisados e as questões não resolvidas. A verificação do Beacon é uma verificação online separada; o renderizador de relatórios nunca entra em contato com um serviço apenas para exibir um relatório.

Em caso de controvérsia sobre uma mensagem específica, cite a referência do arquivo, o arquivo oficial e a referência do registro; em seguida, descreva o período relevante, as lacunas de cobertura, a seleção e o material corroborativo. Para uma cópia compartilhada, analise também a transformação registrada e suas referências ao arquivo de origem. Filtros privados e mapeamentos de identidade permanecem fora da avaliação pública.

A verificação do PDF assinado detecta alterações nos bytes abrangidos. Mantenha o arquivo digital original e o resultado da verificação juntamente com quaisquer capturas de tela ou cópias impressas para leitura.
