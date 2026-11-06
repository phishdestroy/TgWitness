# Carregar histórico de origem

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/

Carregue mensagens anteriores de fontes habilitadas, pause e retome a gravação e verifique um relatório de progresso assinado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Coleção](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Coleção](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

Em **Fontes**, revise os chats habilitados, pause a observação, escolha API Padrão ou exportação Takeout e, em seguida, escolha **Carregar histórico completo**. A execução corrige essa lista de fontes e lê as mensagens anteriores disponíveis nos Chats e no diário de observação assinado. A mídia utiliza as configurações de anexos existentes e a fila de download permanente. Isso é independente da exportação assinada em JSON/HTML por chat.

Para coleta em toda a conta, selecione **Conta inteira**, inicie a observação para carregar sua lista de fontes e revise essa lista antes de iniciar o histórico. O limite da lista de diálogos ainda se aplica (1,000 por padrão, ajustável em Parâmetros). Uma execução bem-sucedida não prova que todos os diálogos da conta foram listados. Bate-papos descobertos ou ativados posteriormente precisam de outra execução. Pause a observação antes de iniciar o histórico; uma aquisição abrange uma conta por vez.

Escolha de um a cinco processadores de anexos e se deseja preservar as Ações Recentes disponíveis e comparar versões salvas anteriormente. A exportação pode exigir aprovação no Telegram e uma espera especificada pelo servidor. Essas opções permanecem fixas ao retomar a operação. Consulte [o comportamento de preenchimento retroativo e o contrato de evidências](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) para detalhes sobre transporte, repetição de tentativas e confiança.

## Pausa, reinício e resultados parciais

- **Histórico de pausa** interrompe a leitura. **Histórico de continuação** retoma a partir da última mensagem confirmada em cada fonte; reiniciar o aplicativo também mantém a execução em pausa até que seja retomada. A retomada requer a mesma conta do Telegram inativa.
- A observação da mensagem, o processamento do anexo e o registro do cursor ocorrem em uma única transação. Uma execução retomada não repete as observações já registradas. A captura em tempo real ou uma execução separada, iniciada explicitamente, pode observar a mesma mensagem de forma independente.
- Cada fonte (cada intervalo dividido do Telegram no Takeout) define um ID de mensagem máximo na primeira leitura. As mensagens mais recentes pertencem à observação em tempo real, e não às páginas históricas restantes dessa fonte.
- Fontes inacessíveis e fontes desativadas durante a aquisição permanecem visíveis como falhadas ou ignoradas. Outras fontes continuam; o resultado geral fica incompleto.
- Os atrasos do FloodWait respeitam o backoff da conta salva. Falhas transitórias são repetidas até cinco vezes; esgotamento e pouco espaço em disco causam uma pausa, mantendo o cursor intacto.
- **Encerrar esta execução do histórico** preserva as observações salvas. Não as remove nem cancela tarefas de anexação da API padrão. Encerrar o Takeout marca seus arquivos Takeout restantes como ignorados; pausar permite que sejam retomados. Uma nova execução lê novamente as fontes habilitadas.

A conclusão do histórico descreve apenas as leituras do histórico. Os anexos podem permanecer pendentes, falhar ou ser excluídos pela política configurada. Verifique os recibos de mídia no registro e na fila de anexos; somente um recibo concluído com bytes preservados constitui um anexo salvo. A operação do histórico é uma solicitação explícita de instantâneo e é distinta das opções que selecionam categorias de eventos ao vivo futuros.

## Transferir e verificar

Salve o **relatório de progresso assinado** e, em seguida, use **a opção “Exportar evidências”** para baixar o registro e os anexos salvos. Uma exportação posterior de evidências pode incluir registros adicionais; o relatório vincula seus contadores ao prefixo do registro no momento em que foi criado. Execute o verificador a partir de uma cópia confiável desta versão:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Mantenha a impressão digital esperada da chave de assinatura de forma independente. O verificador verifica a assinatura do relatório, o arquivo de evidências, o ponto de verificação do relatório, o plano de origem, a conta e as contagens de mensagens salvas/indisponíveis. Novas execuções também vinculam o progresso da fonte e as opções a eventos de cursor assinados. Sem o `--evidence`, ele verifica apenas o relatório assinado e sua consistência interna. Os campos de progresso legados e os resumos de anexos permanecem como declarações assinadas do coletor. O verificador de evidências verifica os bytes de mídia arquivados.

Nem a assinatura nem a conclusão do histórico disponível comprovam a origem do Telegram, um instantâneo atômico ou a integridade histórica. As mensagens podem sofrer alterações durante a leitura; mensagens excluídas e edições intermediárias fora das Ações Recentes disponíveis, bem como das Conversas Secretas, não são recuperadas. Um operador que controle a chave de assinatura pode fabricar um registro antes que existam compromissos externos. Utilize pontos de verificação mantidos separadamente ou uma testemunha independente para as propriedades documentadas de detecção de adulteração.

O cursor de aquisição representa o estado local da área de trabalho. A restauração de um arquivo ZIP de evidências, por si só, não restaura uma tarefa de aquisição pendente nem uma sessão do Telegram. Mantenha o backup da área de trabalho caso seja necessário dar continuidade à tarefa original.
