# Trabalhar com o arquivo

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/archive/

Encontre a mensagem. Verifique a fonte. Monte o caso.

01**Incluir o histórico**

Traga para o espaço as mensagens antigas das suas fontes ativas.

02**Siga as fontes**

Pesquise e abra a mensagem salva por trás de cada resultado.

03**Mantenha a transição clara**

Sua análise em um arquivo, a evidência assinada ao lado.

Os registros capturados, o texto reconhecido e as conclusões dos analistas permanecem distintos.

## Carregar mensagens anteriores

1. **Fontes → Chats no escopo**: confira os chats ativos e inicie a observação.
2. **Carregar histórico completo**. Usa a lista de fontes como está agora.
3. **Pausar histórico** / **Continuar histórico** quando quiser. Depois de reiniciar, retome manualmente.
4. Confira o resultado por fonte e a fila de downloads e guarde o relatório de progresso assinado junto com a exportação.

Isso preenche o espaço. Exportar um único chat em HTML/JSON é outra coisa. [Detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/).

## Pesquise primeiro, depois decida sobre a IA

1. **Diário** pesquisa localmente, com filtros por fonte e data.
2. Pesquise uma frase ou um domínio e abra o registro e suas versões.
3. Para IA, o administrador configura um provedor em **Integrações**. Depois, **Perguntar ao arquivo**: escolha chats e um período, veja **Dados enviados ao modelo** e desmarque o que não deve sair.
4. Confira as citações, salve a resposta como relatório e acrescente suas notas.

A pesquisa não precisa de IA. Os relatórios guardam fontes e revisões, separados do diário assinado. [Configurar provedor](https://phishdestroy.github.io/TgWitness/pt/docs/reference/analysis/).

## Escolha a conexão que você precisa

| Tarefa | Abrir | Configuração |
| --- | --- | --- |
| Deixar um cliente de IA ler chats escolhidos | **Integrações → MCP** | [Instale o MCP, crie um token limitado e conecte](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/) |
| Reconhecer texto em arquivos de mídia salvos | Um registro `media.saved` → **Reconhecer anexo** | [Configure o worker local do Docker](https://phishdestroy.github.io/TgWitness/pt/docs/reference/media-analysis/) |
| Envie eventos para o n8n ou para um SIEM | **Integrações → Webhooks de saída** | [Adicione um receptor, confira o HMAC e descarte IDs repetidos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/webhooks/) |

**Qual token de acesso vai em qual lugar?**

O acesso ao painel é para pessoas. O MCP tem tokens próprios só de leitura e os webhooks, o próprio segredo HMAC. Nenhum precisa de uma sessão do Telegram.

[Compartilhe o acesso ao painel](https://phishdestroy.github.io/TgWitness/pt/docs/access/) ou [configure um cliente MCP](https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/).

## Apresentar fontes e conclusões

Coloque o relatório ao lado do ZIP assinado. O relatório é a sua leitura das fontes; o ZIP é o que o destinatário verifica.

[Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/exports/) · [Conduzir uma investigação completa](https://phishdestroy.github.io/TgWitness/pt/docs/cases/)
