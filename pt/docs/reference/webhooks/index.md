# Webhooks de saída

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/webhooks/

Envie eventos específicos para destinatários HTTPS com assinaturas HMAC, tentativas de reenvio e status de entrega.

**Versão principal atual:** utilize uma cópia do código-fonte; a versão prévia portátil 0.7.0 é anterior a esse recurso.

[Guia de fluxo de trabalho](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Abra **“Integrações” → “Webhooks de saída”** no espaço de trabalho selecionado. Adicione um receptor HTTPS, escolha eventos de coleta/mídia/exportação e, opcionalmente, selecione chats para novas observações e alterações. O texto da mensagem está desativado por padrão. Ativar trechos adiciona no máximo 1.000 caracteres aos eventos de alteração de mensagem; campos brutos do Telegram e credenciais nunca são enviados.

Copie o segredo HMAC uma vez para a configuração protegida do receptor. Ele está criptografado no cofre do TgWitness e não pode ser recuperado pelo painel. Remova e recrie um destino para alterná-lo. **Envie** às filas **de teste sintéticas** um teste sem conteúdo de bate-papo; atualize o status de entrega para ver o resultado.

A entrega amplia o ciclo de notificações existente em conjunto com o Apprise. Ela utiliza a rota externa do espaço de trabalho e as restrições existentes para destinos privados. Não há nenhum redirecionamento ou alternativa direta a seguir. As URLs não devem conter credenciais, cadeias de consulta ou fragmentos; endereços privados exigem a ativação da rede no nível do servidor, e não uma configuração que o usuário do painel possa ignorar.

## Carga útil e assinatura

Esquema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Cada carga útil contém `event_id`, `timestamp`, `workspace`, `type`, `synthetic` e contadores. Os eventos baseados no registro incluem sua sequência e hash. A conclusão da exportação completa e os testes sintéticos são eventos de entrega, sem referência inventada ao registro assinado. Os avisos de exclusão do Telegram e `missing_on_recheck` permanecem como tipos distintos.

O cabeçalho `X-TgWitness-Signature` é `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Calcule o HMAC sobre os bytes exatos `timestamp + "." + raw_request_body`, usando o segredo exibido como bytes UTF-8. Compare as assinaturas em tempo constante antes de analisar ou agir sobre o corpo da mensagem. Rejeite carimbos de data/hora com mais de cinco minutos de diferença em relação ao seu relógio. O carimbo de data/hora é atualizado a cada tentativa de entrega.

Use `event_id` como chave de idempotência no armazenamento durável, com uma restrição atômica de exclusividade antes dos efeitos colaterais. Uma assinatura válida, por si só, não impede que uma solicitação recente seja reproduzida. Mantenha os IDs processados pelo menos durante toda a janela de repetição; retenha-os por mais tempo se o destinatário puder reprocessar eventos armazenados.

## Novas tentativas

As entregas são enfileiradas de forma duradoura antes das solicitações HTTP. Elas utilizam a semântica “pelo menos uma vez”: uma confirmação perdida ou uma reinicialização podem fazer com que um evento seja entregue novamente com o mesmo ID. Há oito tentativas com recuo exponencial, começando em 15 segundos e com limite máximo de uma hora. O sucesso requer uma resposta 2xx. Tarefas esgotadas deixam um erro visível; a entrega não é garantida após o término das tentativas.

A fila comporta 1.000 entregas. Quando estiver cheia, a varredura dos eventos do diário é pausada e retomada assim que houver espaço disponível. A conclusão de uma exportação completa que não possa ser colocada na fila gera um erro visível na fila. São tentadas até cinco entregas por ciclo de notificação, e os 100 registros mais recentes das tentativas são mantidos. A remoção de um destino também remove suas entregas pendentes.

## Exemplo do n8n

Importe [o fluxo de trabalho de exemplo](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Ele está inativo e não contém segredos nem ações subsequentes. Defina `TGWITNESS_WEBHOOK_SECRET` no ambiente do worker do n8n, permita o acesso a esse ambiente e habilite o `crypto` como built-in para o nó Code. O exemplo utiliza a opção raw-body do nó Webhook, verifica a assinatura e a validade e confirma eventos validados. Isso corresponde à [implementação documentada](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) do nó.

Antes de adicionar gravações ou notificações do SIEM, inclua um armazenamento idempotente e duradouro, indexado por `event_id`. Restrinja a edição do fluxo de trabalho do n8n e a retenção do registro de execução de acordo com os dados que você escolheu enviar. O TgWitness não adiciona comandos de entrada.
