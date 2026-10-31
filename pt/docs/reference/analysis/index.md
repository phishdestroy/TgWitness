# Análise de arquivos

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/

Pesquise mensagens salvas, analise contribuições de IA e mantenha relatórios analíticos com suas referências de fonte.

**Versão principal atual:** utilize uma cópia do código-fonte; a versão prévia portátil 0.7.0 é anterior a esse recurso.

[Guia de fluxo de trabalho](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Use o **Diário** para pesquisa local sem IA. Para usar **Consulte o arquivo**, primeiro habilite e configure um provedor em **Integrações**. O seletor de área de trabalho escolhe a conta; o formulário seleciona os chats e o período de observação. A recuperação é executada localmente. Uma frase exata ou um domínio restringe a recuperação; um ID de mensagem solicita versões salvas. Analise os trechos e abra seus registros no diário ou o contexto. Não há banco de dados vetorial nem ação automática no Telegram.

## Provedores e consentimento

A IA vem desativada em todos os espaços de trabalho. Somente o administrador principal pode configurar o modelo, o endpoint, a chave de API criptografada, os limites de contexto/saída, o tempo limite e o limite diário de solicitações. A chave nunca é devolvida ao navegador. Deixe o campo da chave em branco para manter a chave atual ou remova-a explicitamente.

O Ollama utiliza seu [endpoint `/api/chat`](https://docs.ollama.com/api/chat) documentado com saída JSON sem streaming. Seu endereço padrão é `http://127.0.0.1:11434` no servidor do TgWitness. O operador pode alterá-lo usando `TGWITNESS_AI_LOCAL_ENDPOINT`; este não é um endereço controlado pelo modelo. Instale você mesmo o modelo selecionado. O TgWitness não o baixa automaticamente.

O provedor compatível espera uma URL base terminada em `/v1` e o [protocolo Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, modo de resposta JSON, `max_completion_tokens` e `choices[0].message.content`. Serviços que não possuam esses campos não são suportados. O teste de conexão envia texto sintético e conta para o limite de solicitações.

Cada solicitação utiliza a rota externa configurada no espaço de trabalho. Uma rota bloqueada ou um MTProxy exclusivo para o Telegram resulta em erro; não há repetição direta da tentativa. Um endereço Ollama local deliberadamente configurado permite um destino privado, mantendo o uso da rota escolhida. Para outros serviços privados, aplica-se a opção de adesão ao destino privado no nível do servidor já existente. O painel exibe o endpoint efetivamente configurado.

Antes da geração, **os dados enviados ao modelo** mostram a solicitação: pergunta, trechos marcados, tipos de eventos, horários de observação e marcadores de cobertura. Sessões do Telegram, campos brutos, chaves de provedores, bytes de anexos e o diário completo não fazem parte desse contexto. Desmarque as fontes indesejadas e, em seguida, aprove explicitamente o processamento. Provedores externos podem reter o conteúdo enviado de acordo com suas próprias políticas. Execução local significa que o endpoint é local; isso não é uma garantia quanto ao comportamento de um serviço configurado de forma independente.

Há, no máximo, duas solicitações simultâneas ao provedor globalmente e uma por espaço de trabalho. Uma pré-visualização expira após dez minutos e pode gerar uma resposta. São exibidas as contagens de tokens informadas pelo provedor; uma estimativa de custo aparece somente quando as tarifas de entrada e saída tiverem sido configuradas. Tentativas malsucedidas também consomem o orçamento diário de solicitações. Nenhuma nova tentativa automática gasta orçamento adicional.

## Fontes e limitações

A recuperação examina o texto das mensagens salvas por meio de uma busca lexical delimitada. Ela retorna até 24 fontes e sinaliza trechos truncados ou conjuntos de resultados incompletos. O período refere-se ao **tempo de observação**, não a uma afirmação de que o histórico do Telegram seja completo. Eventos com cobertura em todo o espaço de trabalho são excluídos do acesso restrito ao chat. Dados ausentes são descritos como “não encontrados” no arquivo disponível.

O modelo não recebe ferramentas. Seus IDs de origem são verificados em relação aos registros selecionados, os hashes são verificados novamente e as sequências citadas devem constar nesses registros. IDs desconhecidos, citações alteradas e alegações sem referência invalidam a resposta. O aplicativo cria links; URLs gerados pelo modelo não são usados como citações. Essas verificações comprovam a existência da fonte e a precisão da citação, não a veracidade de uma inferência. Analise as inferências em relação aos registros antes de confiar nelas.

## Relatórios

Salve uma resposta revisada como um relatório analítico separado. Ele inclui o resumo do modelo, a cronologia observada, links e identificadores extraídos, registros de edição/exclusão, limites de cobertura e hashes dos eventos de origem. O provedor, o modelo, o endpoint, a hora e a versão do modelo de prompt acompanham o relatório. Nenhuma identidade é combinada automaticamente.

As revisões e anotações dos analistas são armazenadas separadamente do resumo do modelo. Os relatórios ficam em arquivos derivados criptografados, com um índice fora do fluxo de eventos assinado; os eventos e mídias originais não são alterados. Somente o proprietário ou administrador pode abrir um relatório, e o acesso à fonte é verificado novamente. O download também requer permissão de exportação. A versão 1 não assina relatórios nem sugere que as conclusões do modelo sejam evidências verificadas. Limites: 100 relatórios por espaço de trabalho e 100 revisões de analistas por relatório.

Para OCR manual e transcrições, consulte [o processamento de mídia](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/). Para acesso de clientes, consulte [o MCP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/).
