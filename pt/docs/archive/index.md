# Trabalhar com o arquivo

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/archive/

Encontre a mensagem. Verifique a fonte. Monte o caso.

Essas ferramentas estão disponíveis no ramo principal atual. A versão prévia portátil 0.7.0 é anterior a elas; use um checkout do código-fonte para esse fluxo de trabalho.

01**Incluir o histórico**

Carregue mensagens anteriores de suas fontes habilitadas na área de trabalho.

02**Siga as fontes**

Pesquise no arquivo e abra a mensagem salva associada a cada resultado.

03**Mantenha a transição clara**

Salve sua análise separadamente e exporte as evidências assinadas junto com ela.

Os registros capturados, o texto reconhecido e as conclusões dos analistas permanecem distintos.

## Carregar mensagens anteriores

1. **Fontes** abertas: analise os chats habilitados e inicie a observação.
2. Selecione **“Carregar histórico completo**”. A execução utiliza a lista de fontes selecionada naquele momento.
3. Utilize **“Pausar histórico”** e **“Continuar histórico”** conforme necessário. Após uma reinicialização, retome explicitamente.
4. Verifique os resultados por fonte e a fila de anexos. Salve o relatório de progresso assinado junto com a exportação das evidências.

Isso preenche a área de trabalho com as mensagens disponíveis. A exportação em HTML/JSON por conversa é uma operação separada. [Detalhes sobre histórico e recuperação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/).

## Pesquise primeiro, depois decida sobre a IA

1. Acesse**o arquivo**. Escolha um espaço de trabalho, bate-papos e período de observação.
2. Pesquise uma frase, um domínio ou um ID de mensagem. Abra o registro correspondente e suas versões salvas.
3. Para a análise por IA, o administrador primeiro configura um provedor. Revise **os dados enviados ao modelo** e desmarque os trechos indesejados antes de aprovar a solicitação.
4. Verifique as citações retornadas. Salve a resposta como um relatório e adicione sua própria revisão ou notas.

As buscas são realizadas localmente, sem IA. Os relatórios analíticos mantêm as referências das fontes e o histórico de revisões; eles são separados do registro assinado. [Configuração do provedor e relatórios](https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/).

## Escolha a conexão que você precisa

| Tarefa | Abrir | Configuração |
| --- | --- | --- |
| Leia conversas selecionadas de um cliente de IA | **Integrações → MCP** | [Instale o MCP extra, gere um token com escopo e conecte o cliente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/) |
| Reconhecer texto em arquivos de mídia salvos | Um registro `media.saved` → **Reconhecer anexo** | [Configure o Docker worker local e os arquivos de linguagem/modelo necessários](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/) |
| Envie eventos para o n8n ou para um SIEM | **Integrações → Webhooks de saída** | [Adicionar um destinatário, verificar o HMAC e deduplicar IDs de eventos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/webhooks/) |

**Qual token de acesso vai em qual lugar?**

O acesso ao painel é destinado às pessoas que estão analisando o caso. As conexões MCP recebem tokens de arquivo separados, apenas para leitura. Um receptor de webhook utiliza seu próprio segredo HMAC. Nenhum deles precisa de um arquivo de sessão do Telegram.

[Compartilhe o acesso ao painel](https://phishdestroy.github.io/TgWitness/pt/docs/access/) ou [configure um cliente MCP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/).

## Apresentar fontes e conclusões

Mantenha o relatório analítico revisado junto com o arquivo ZIP de evidências assinado. O relatório explica sua interpretação das fontes; o arquivo ZIP permite que o destinatário verifique o registro salvo em relação a uma assinatura digital e um ponto de verificação confiáveis e independentes.

[Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/exports/) · [Conduzir uma investigação completa](https://phishdestroy.github.io/TgWitness/pt/docs/cases/)
