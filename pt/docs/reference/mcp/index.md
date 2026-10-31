# MCP somente leitura

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/mcp/

Conecte um cliente MCP a espaços de trabalho e chats selecionados com acesso temporário e revogável.

Conecte um cliente analista aos workspaces e chats selecionados. O TgWitness serve **Streamable HTTP em `/mcp` no processo do painel**. Cada conexão possui seu próprio token, validade e ferramentas permitidas. O MCP não pode enviar mensagens do Telegram, alterar configurações ou modificar o diário assinado.

[Guia de fluxo de trabalho](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Instalar e verificar

Use o ambiente Python que executa o painel. A partir de um checkout do código-fonte:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Reinicie o painel com seu diretório de dados habitual e argumentos de inicialização após a instalação. A verificação de prontidão deve incluir `[PASS] mcp: streamable-http available`. **Integrations → MCP** mostra o status de execução e um comando de instalação usando o executável Python real daquele servidor. **Re-check** atualiza esse status sem recarregar a página; isso não instala pacotes nem reinicia o servidor.

O extra MCP usa o [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) oficial. `deploy/constraints-mcp.txt` fixa o SDK testado e as dependências. Esses recursos exigem o código-fonte atual; a versão prévia portátil 0.7.0 é anterior a eles.

## Emitir uma conexão

1. Insira um rótulo e escolha os workspaces e chats que o cliente pode ler.
2. Selecione as ferramentas individualmente ou use uma predefinição. Apenas ferramentas implementadas são oferecidas.
3. Escolha 1, 7, 30 ou 90 dias, ou uma validade personalizada entre um minuto e 90 dias.
4. Pressione **Create connection**. O token aparece uma única vez ao lado da configuração do cliente.
5. Copie o token e a configuração e, em seguida, execute **Check connection**. Ele inicializa o MCP e lista as ferramentas permitidas; **nenhuma mensagem é lida**. O resultado mostra a versão do protocolo, nomes das ferramentas, contagem e tempo decorrido.
6. Pressione **Done** quando a credencial estiver salva. As atualizações automáticas preservam o formulário e o cartão exibido uma única vez. Bloquear o painel limpa os segredos exibidos.

A lista mostra o uso recente, a última ferramenta, o endereço e as requisições no último minuto. **Revoke** encerra o acesso. **Rotate token** revoga a credencial antiga e emite uma substituta com o mesmo escopo, ferramentas e validade; copie a substituta uma única vez. Tokens de login do painel e credenciais do Telegram não funcionam como tokens MCP.

## Conecte seu cliente

Selecione o cliente no painel e copie a configuração gerada. As configurações usam referências a segredos ou espaços reservados explícitos; o token é copiado separadamente.

| Cliente | Configuração | Conexão |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, cabeçalho bearer |
| Claude Desktop | `claude_desktop_config.json` | Ponte stdio local |
| Cursor | `.cursor/mcp.json` | HTTP com um cabeçalho de variável de ambiente |
| VS Code Local | `.vscode/mcp.json` | HTTP com uma entrada `promptString` de senha |
| Windsurf | `mcp_config.json` | HTTP com um espaço reservado para cabeçalho bearer |
| Outros clientes | URL e cabeçalho Authorization | Streamable HTTP |

O TgWitness usa tokens bearer, sem descoberta OAuth. Use a ponte stdio local para clientes cujo conector remoto exige OAuth. Para o VS Code, as variáveis de entrada aplicam-se ao ambiente **Local** e não são encaminhadas para sessões do Copilot. Referências de configuração: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

O ponto de entrada canônico para uma ponte local é:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Use o Python local do cliente com o extra MCP instalado. Defina `TGWITNESS_MCP_TOKEN` em seu ambiente protegido. Mantenha as credenciais fora dos argumentos de comando e URLs. `tgwitness-mcp` é o mesmo ponto de entrada. O módulo antigo `tgwitness.mcp_bridge` e o nome `TGWITNESS_ARCHIVE_TOKEN` permanecem como caminhos de compatibilidade com um aviso; novas configurações usam `mcp_server` e `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Encaminhe a rota `/mcp` do painel e preserve o cabeçalho bearer. Abrir as configurações de MCP como administrador registra a origem atual do painel para esta execução. Para ter um endereço estável disponível imediatamente após a reinicialização, configure `TGWITNESS_PUBLIC_URL` com a origem HTTPS do painel antes de iniciá-lo. Cabeçalhos Host e de encaminhamento arbitrários não registram um endereço confiável. As verificações de Host e Origin rejeitam origens de navegador não relacionadas. As respostas usam `Cache-Control: no-store`; valores de autorização nunca são registrados nos logs.

Um endereço `*.trycloudflare.com` é temporário. Quando uma reinicialização do túnel altera o hostname, atualize a URL pública configurada e a URL do MCP de cada cliente. Use um hostname estável para configurações de clientes salvas.

## Ferramentas e limites

| Ferramenta | Lê |
| --- | --- |
| `list_workspaces` | Workspaces concedidos |
| `list_chats` | Chats concedidos |
| `search_messages` | Texto de mensagens salvas dentro do período selecionado |
| `get_message_versions` | Versões capturadas e observações de exclusão |
| `get_message_context` | IDs de mensagens capturadas próximas |
| `get_journal_event` | Um registro higienizado com sua referência de origem |
| `get_capture_status` | Estado da coleta e registros de cobertura permitidos |

`tools/list` retorna apenas as ferramentas concedidas àquela conexão. Chamadas para outras ferramentas são recusadas. Ferramentas de contexto de grupo, episódio, terminologia e cadeia de respostas não são oferecidas nesta compilação; o backend separado de pacote de contexto delas não está incluído.

Cada leitura verifica o token, a ferramenta e o escopo de workspace/chat, inclusive após a conclusão do trabalho no banco de dados. Os limites são de 60 requisições por minuto, 50 registros por página, 64 KiB por resultado e um tempo limite de oito segundos para o arquivo. Uma chamada MCP que exceda o tempo limite retorna um erro de ferramenta solicitando um período menor ou um limite mais baixo.

Os resultados de mensagens contêm `untrusted_content: true`, IDs de workspace/chat/mensagem, sequência de eventos, hash salvo e um link para o painel. Objetos brutos do Telegram, hashes de acesso, sessões e chaves são omitidos. O truncamento de texto é sinalizado. Edições, avisos de exclusão e `missing_on_recheck` são observações distintas. Registros ausentes não provam que um evento nunca aconteceu.

Trate instruções dentro de mensagens capturadas como evidência, nunca como instruções para o cliente. O acesso somente leitura impede alterações no arquivo; o cliente ainda pode reter o conteúdo que tem permissão para ler. Hashes identificam registros salvos e apoiam verificações de integridade; eles não provam autoria no Telegram nem captura completa.
