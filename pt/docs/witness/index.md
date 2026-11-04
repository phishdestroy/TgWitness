# Configure um bot do Witness

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/witness/

Um processo separado confere seu diário e publica pontos de verificação assinados em um canal.

## Dois servidores, duas chaves de assinatura

HOST A / COLLECTOR**Conta + registro**

Chave de assinatura do Coletor de sessões do Telegram

Endpoint de ponto de verificação somente leitura

← solicitar resposta assinada →

HOST B / WITNESS**Verificar + reter**

Impressão digital fixada do coletor; Chave de assinatura separada da testemunha

Registro próprio + token do bot

Witness → API do bot do Telegram →**Seu canal · publicações assinadas com TGW1**

O “witness” realiza as verificações por conta própria. O acesso do coletor é somente para leitura. A publicação pelo bot utiliza a conexão e o token do “witness”; nenhuma sessão de conta é concedida ao “witness”.

03 / DECISÕES DE CHECKPOINTRespostas ilustrativas

ÚLTIMA ACEITAÇÃO**120 registros**`head 9c7d…`

PRÓXIMA RESPOSTA**128 registros**`head a4f2…`

Aceito: a contagem aumenta, a assinatura é verificada e a chave corresponde. A testemunha mantém esse novo limite.

Todos os exemplos de respostas pressupõem uma assinatura válida e a chave fixada. Os hashes aqui apresentados são ilustrações abreviadas. Uma contagem maior, por si só, não pode provar que todo o prefixo antigo permanece inalterado; compare uma exportação com pontos de verificação retidos.

## Prepare um bot e um canal

Crie um bot com o BotFather e deixe-o postar no seu canal. Rode a testemunha em outro lugar: outro host, de preferência operado por outra pessoa, vale muito mais que um segundo processo ao lado do coletor.

## Três etapas em “Extras”

1. **Acesso só de leitura.** **Extras → Testemunha independente**, crie um token e salve o arquivo. Ele lê pontos de verificação e estado, nada mais.
2. **Canal e intervalo.** Canal do Telegram ou webhook do Discord, mais um endereço do coletor que a testemunha alcance. Salve o arquivo de configurações.
3. **Iniciar.** Coloque `witness.json`, `witness-token.txt` e `bot-token.txt` juntos no host da testemunha e rode:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Espere o primeiro post assinado no canal e guarde a impressão digital da testemunha em um lugar seguro.

Prefere Discord? Salve a URL do webhook como `discord-webhook.txt`. Uma testemunha posta em um só lugar; no Discord, verificações longas chegam como arquivo.

## Escolha a frequência de publicação

Postar cada verificação cria um registro externo constante: a cada cinco minutos são cerca de 288 posts por dia por espaço. As configurações avançadas permitem postar só em mudanças ou problemas, usar proxy ou um Bot API próprio.

**O que o bot, na verdade, atesta?**

Ela pede ao coletor um ponto de verificação assinado, confere com a chave esperada e mantém o próprio diário assinado, incluindo respostas perdidas e rejeitadas.

Ela confere o estado do diário; não observa o Telegram por conta própria. Para isso, faça um teste de entrega controlado.

## Verifique as evidências posteriormente

Guarde o diário da testemunha, os posts e as impressões digitais. [Como conferi-los](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#verify) com a exportação do coletor.
