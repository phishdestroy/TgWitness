# Telegram · Descubra o que deu errado

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/troubleshooting/

Comece pelo sintoma e confira uma coisa de cada vez.

## O painel solicita um token

Ele pede o token do painel do arquivo que o inicializador mostrou. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Não é código do Telegram, nem token de bot, nem o da testemunha.

## O Telegram não estabelece conexão

Rode a verificação de conexão. Num proxy público, escolha outro e salve. Confira o tipo de proxy e o formato do segredo. Atualizar listas não troca a rota sozinho.

## Conectado, mas sem novas mensagens

1. A observação está rodando, no espaço certo?
2. A fonte está selecionada e visível para essa conta?
3. Envie uma mensagem única no seu grupo de teste e procure por ela.
4. Procure interrupções ou erros do Telegram no diário.

Um chat parado simplesmente não tem nada novo. Se a completude importa, faça um teste de entrega controlado.

## FloodWait ou uma lacuna após uma reinicialização

FloodWait é o Telegram dizendo "mais devagar". Espere passar e diminua a carga; reconectar não ajuda. Depois de reiniciar, o TgWitness recupera o que o Telegram ainda tem; o resto é lacuna, então anote.

## O bot está configurado, mas não publica nada

A testemunha está rodando, o bot pode postar no canal, ela alcança o coletor e o Bot API? Procure posts com falha no diário dela. Uma consulta do lado do coletor não significa que o post saiu.

## Onde está a integração com o token do GitHub?

**Em planejamento.** A seção “Extras” descreve o fluxo de trabalho proposto para a verificação de bifurcações e compilações. Atualmente, não há um formulário de token do GitHub nem atestado automatizado de que uma instalação em execução corresponda a um repositório. Consulte o [status atual dos recursos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/features/).

Vai relatar um bug? Versão, sistema, passos e um erro sem dados pessoais. Nunca coloque sessões, tokens, mensagens privadas ou o diretório de dados em uma issue pública.
