# MCP somente leitura

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/

Conecte um cliente MCP a espaços de trabalho e chats selecionados com acesso temporário e revogável.

**Versão principal atual:** utilize uma cópia do código-fonte; a versão prévia portátil 0.7.0 é anterior a esse recurso.

[Guia de fluxo de trabalho](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Instale o servidor opcional a partir do diretório do projeto TgWitness:

```
python -m pip install '.[mcp]'
```

No painel, abra **Integrações → MCP**. Nomeie a conexão, selecione seus espaços de trabalho e chats e escolha um prazo de validade. Copie o token de arquivamento uma vez; ele não pode ser recuperado posteriormente. Revogue tokens perdidos e emita substitutos. Os tokens do painel e as credenciais do Telegram não são credenciais do MCP.

## Conectar um cliente

O painel gera `.vscode/mcp.json` para o **ambiente local do VS Code** usando sua [configuração documentada](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Salve o arquivo baixado nesse local, execute **o MCP: List Servers** e inicie o TgWitness. O VS Code solicita o token por meio de uma caixa de entrada de senha. O arquivo JSON baixado contém uma referência à solicitação, não o token. Use o executável Python do ambiente em que o MCP extra está instalado.

Para outros clientes da stdio, execute:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Defina `TGWITNESS_ARCHIVE_TOKEN` no ambiente protegido do cliente. Não o inclua em argumentos de comando ou URLs. A ponte faz a leitura por meio da API de arquivo autorizada do painel; ela não tem acesso direto ao banco de dados. O stdout transmite apenas mensagens MCP.

Para clientes remotos, execute o serviço ao lado do painel:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Encaminhe `/mcp` por meio de um proxy reverso HTTPS para `127.0.0.1:8766/mcp`, preservando o cabeçalho `Authorization: Bearer …`. Desative o registro de cabeçalhos de autorização e corpos de solicitação/resposta. Faça a ligação além do loopback somente quando necessário, usando `--host` e `--public-url`. O endpoint utiliza Streamable HTTP do [SDK oficial do MCP para Python](https://github.com/modelcontextprotocol/python-sdk). Ele suporta credenciais de portador configuradas explicitamente, não a descoberta por OAuth; clientes que exigem apenas OAuth não são suportados.

**A verificação do protocolo e o acesso** inicializam um cliente MCP real e listam as ferramentas. Isso não busca mensagens. Para uma verificação remota, o servidor MCP escolhido recebe o token de arquivo. Configure apenas um servidor que você opera ou no qual confia para esse escopo.

## Escopo e resultados

Ferramentas disponíveis: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` e `get_capture_status`. Não há ações no Telegram, alterações de configuração nem ferramentas de exportação em massa. A cada leitura, o acesso ao espaço de trabalho/bate-papo é verificado novamente; credenciais expiradas e revogadas deixam de funcionar. Os limites são de 60 solicitações de API por minuto por credencial, 50 registros por página, uma resposta de 64 KiB e um prazo de resposta da API de oito segundos.

Os resultados das mensagens incluem espaço de trabalho, IDs de bate-papo/mensagem, sequência de eventos, hash salvo, e um link para o painel. O usuário que abrir o link deve ter sua própria sessão autorizada no painel. Objetos brutos do Telegram, hashes de acesso, referências a arquivos, material da sessão e chaves são omitidos. A pesquisa examina o texto da mensagem, não os campos brutos. O texto é delimitado e o truncamento é marcado. Edições, notificações de exclusão do Telegram e `missing_on_recheck` permanecem como observações separadas. O acesso restrito ao chat não pode visualizar eventos operacionais em todo o espaço de trabalho; o status da captura marca explicitamente esse limite.

O texto do arquivo é considerado uma entrada não confiável. As instruções contidas nas mensagens não conferem nenhum alcance adicional e não devem ser tratadas como instruções do cliente. Um modelo de IA externo pode receber qualquer conteúdo que seu cliente MCP solicitar. O acesso somente leitura impede alterações no arquivo; ele não impede que um cliente retenha os dados que lê.

Os hashes identificam os registros salvos e permitem verificações de integridade. Eles não comprovam, por si só, a autoria no Telegram nem que todas as mensagens tenham sido capturadas.
