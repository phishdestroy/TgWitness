# Configure um bot do Witness

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/witness/

Permita que um processo separado verifique o registro e publique pontos de verificação assinados em seu canal.

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

Crie um bot com o BotFather e permita que ele publique em um canal sob seu controle. Escolha um computador ou servidor para o TgWitness. Um host e um operador independentes proporcionam maior independência do que um segundo processo no servidor do coletor.

## Três etapas em “Extras”

1. **Acesso somente para leitura.** Abra **“Extras” → Um bot no seu canal**, crie um token de testemunha e salve o arquivo de acesso. Ele permite a leitura de pontos de verificação e do estado de integridade, mas não de conversas nem dos controles do coletor.
2. **Canal e intervalo.** Insira o canal e um endereço de coletor acessível a partir do TgWitness. Salve o arquivo de configurações.
3. **Inicialização.** Coloque `witness.json`, `witness-token.txt` e um `bot-token.txt` criados no servidor do TgWitness juntos. Execute os comandos abaixo no ambiente do projeto instalado.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

O download dos arquivos não inicia o witness. Verifique se a primeira postagem assinada aparece no canal e, em seguida, guarde separadamente a impressão digital da chave pública do witness.

## Escolha a frequência de publicação

A publicação de cada verificação cria um registro externo regular. Em intervalos de cinco minutos, isso equivale a cerca de 288 postagens por espaço de trabalho por dia. As configurações avançadas também oferecem a publicação de alterações ou problemas, um proxy e um endereço personalizado da API do bot.

**O que o bot, na verdade, atesta?**

A testemunha solicita ao coletor um ponto de verificação assinado, verifica-o em relação à chave esperada e mantém um registro assinado separado. Ela registra respostas ausentes e respostas rejeitadas, bem como verificações bem-sucedidas. A publicação ainda depende da testemunha estar em execução e ter acesso à API de bots do Telegram.

Ele verifica o estado do registro relatado pelo coletor. Não monitora de forma independente todas as mensagens do Telegram. Para isso, adicione o teste de entrega controlada.

## Verifique as evidências posteriormente

Mantenha o diário de evidências, as publicações do canal e as impressões digitais salvas de forma independente. O [procedimento completo de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/#verify) compara esses dados com a exportação assinada pelo coletor.
