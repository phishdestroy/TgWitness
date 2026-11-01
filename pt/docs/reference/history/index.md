# Carregar histórico de origem

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/history/

Carregue mensagens anteriores de fontes habilitadas, pause e retome a gravação e verifique um relatório de progresso assinado.

Em **“Fontes”**, revise os chats habilitados, inicie a observação e, em seguida, selecione **“Carregar histórico completo**”. A execução fixa essa lista de fontes e importa as mensagens anteriores disponíveis para “Chats” e para o diário de observação assinado. A mídia utiliza as configurações de anexos existentes e a fila de download permanente. Isso é independente da exportação assinada em formato JSON/HTML por chat.

Para coleta em toda a conta, selecione **“Conta inteira”**, inicie a observação para carregar sua lista de fontes e revise essa lista antes de iniciar o histórico. O limite da lista de diálogos ainda se aplica (1.000 por padrão, ajustável em “Parâmetros”). Uma execução bem-sucedida não comprova que todas as conversas da conta foram listadas. Bate-papos descobertos ou ativados posteriormente exigem outra execução.

## Pausa, reinício e resultados parciais

- **Pausar o histórico** interrompe a leitura. **Continuar o histórico** retoma a partir da última mensagem gravada em cada fonte; reiniciar o aplicativo também deixa a execução em pausa até que seja retomada. Reinicie a observação primeiro. A retomada requer a mesma conta do Telegram.
- A observação da mensagem, o processamento do anexo e o registro do cursor ocorrem em uma única transação. Uma execução retomada não repete as observações já registradas. A captura em tempo real ou uma execução separada, iniciada explicitamente, pode observar a mesma mensagem de forma independente.
- Cada fonte define um ID máximo de mensagem na primeira leitura. As mensagens mais recentes pertencem à observação em tempo real, e não às páginas históricas restantes dessa fonte.
- Fontes inacessíveis e fontes desativadas durante a aquisição permanecem visíveis como falhadas ou ignoradas. Outras fontes continuam; o resultado geral fica incompleto.
- Os atrasos do FloodWait respeitam o intervalo de espera salvo na conta. Timeouts de transporte e pouco espaço em disco suspendem a execução, mantendo o cursor intacto. Retome após resolver a causa.
- **Encerrar esta execução do histórico** preserva as observações salvas. Isso não as remove nem cancela os downloads de anexos já enfileirados. Uma nova execução lê as fontes habilitadas novamente.

A conclusão do histórico descreve apenas as leituras do histórico. Os anexos podem permanecer pendentes, falhar ou ser excluídos pela política configurada. Verifique os recibos de mídia no registro e na fila de anexos; somente um recibo concluído com bytes preservados constitui um anexo salvo. A operação do histórico é uma solicitação explícita de instantâneo e é distinta das opções que selecionam categorias de eventos ao vivo futuros.

## Transferir e verificar

Salve o **relatório de progresso assinado** e, em seguida, use **a opção “Exportar evidências”** para baixar o registro e os anexos salvos. Uma exportação posterior de evidências pode incluir registros adicionais; o relatório vincula seus contadores ao prefixo do registro no momento em que foi criado. Execute o verificador a partir de uma cópia confiável desta versão:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Mantenha a impressão digital da chave de assinatura esperada de forma independente. O verificador verifica a assinatura do relatório, o arquivo de evidências, o ponto de verificação do relatório, o plano de origem, a conta e as contagens de mensagens salvas/indisponíveis. Sem o `--evidence`, ele verifica apenas o relatório assinado e sua consistência interna. As fases de progresso, títulos, cursores e resumos de anexos são declarações assinadas do coletor, não reconstruídas de forma independente por este verificador de relatórios. O verificador de evidências ainda verifica os bytes de mídia arquivados.

Nem a assinatura nem a finalização do histórico disponível comprovam a origem do Telegram, um instantâneo atômico ou a integridade histórica. As mensagens podem sofrer alterações durante a leitura; mensagens excluídas, edições intermediárias não visualizadas e bate-papos secretos não são recuperados. Um operador que controle a chave de assinatura pode falsificar um registro antes que existam compromissos externos. Utilize pontos de verificação mantidos separadamente ou uma testemunha independente para as propriedades documentadas de detecção de adulteração.

O cursor de aquisição representa o estado local da área de trabalho. A restauração de um arquivo ZIP de evidências, por si só, não restaura uma tarefa de aquisição pendente nem uma sessão do Telegram. Mantenha o backup da área de trabalho caso seja necessário dar continuidade à tarefa original.
