# Descubra o que deu errado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/troubleshooting/

Comece pelo sintoma. Verifique uma camada de cada vez.

## O painel solicita um token

Utilize o token do painel do arquivo local exibido pelo iniciador. Para o Docker, execute `docker compose exec tgwitness cat /data/panel-token.txt`. Um código de login do Telegram, um token do BotFather e um token de testemunha somente para leitura têm finalidades diferentes.

## O Telegram não estabelece conexão

Abra as configurações de conexão e execute a verificação de conexão. Caso esteja utilizando um proxy público, tente outra entrada e salve a rota explicitamente. Verifique o tipo de proxy e o formato de chave secreta compatível. Atualizar uma lista pública não altera a rota da conta.

## Conectado, mas sem novas mensagens

1. Verifique se a observação está sendo executada no espaço de trabalho correto.
2. Confirme se a fonte está selecionada e visível para essa conta.
3. Envie uma nova mensagem exclusiva em um grupo controlado e procure por esse texto exato.
4. Analise o registro operacional para identificar interrupções, atrasos no trabalho ou erros do Telegram.

Os instantâneos históricos e os eventos de novas mensagens são distintos. Uma fonte inativa pode ser conectada sem gerar novas mensagens. Utilize um teste de entrega controlada quando a integridade dos dados for essencial.

## FloodWait ou uma lacuna após uma reinicialização

O FloodWait significa que o Telegram exige uma pausa. Aguarde o período indicado e revise a carga de trabalho de coleta; reconexões repetidas não removem o limite. O estado de atualização salvo ajuda a recuperar o atraso após uma reinicialização, mas atualizações expiradas e algumas janelas de interrupção continuam sendo limitações. Registre a lacuna em vez de tratar o registro como completo.

## O bot está configurado, mas não publica nada

Certifique-se de que o processo do Witness esteja realmente em execução, que o bot possa publicar no canal e que o Witness consiga se comunicar com o coletor e a API do bot. Verifique o diário em busca de publicações com falha. Uma consulta bem-sucedida ao coletor, por si só, não confirma uma publicação no canal.

## Onde está a integração com o token do GitHub?

**Em planejamento.** A seção “Extras” descreve o fluxo de trabalho proposto para a verificação de bifurcações e compilações. Atualmente, não há um formulário de token do GitHub nem atestado automatizado de que uma instalação em execução corresponda a um repositório. Consulte o [status atual dos recursos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/features/).

Ao relatar um problema, inclua a versão, o sistema operacional, as etapas e uma descrição do erro com informações confidenciais ocultadas. Evite divulgar sessões, tokens, mensagens privadas e o diretório de dados em tickets públicos.
