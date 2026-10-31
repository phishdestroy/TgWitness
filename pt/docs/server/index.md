# Mantenha-o em funcionamento

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/server/

Mantenha o coletor disponível e seus dados intactos mesmo após reinicializações.

## Escolha um método de inicialização

Para uma instalação nativa, utilize o [iniciador](https://phishdestroy.github.io/TgWitness/pt/docs/start/) e os exemplos de serviço na [pasta `deploy/`.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) Para o Docker, instale o Docker com o Compose e execute a partir do diretório do projeto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

O painel padrão escuta no endereço de loopback do host, na porta 8787. Abra-o localmente ou por meio de um túnel SSH. Utilize o token do segundo comando para desbloquear o painel.

## Mantenha todo o diretório de dados

As instalações nativas utilizam o `data/live`. O Docker utiliza o volume persistente `tgwitness-data`. Mantenha os registros, as sessões de conta, as chaves e o estado operacional reunidos. Uma exportação assinada constitui uma evidência útil, mas não é um backup completo da instalação.

1. Interrompa a coleta antes de realizar um backup consistente.
2. Copie todo o diretório de dados privados para um armazenamento protegido fora do servidor.
3. Teste a restauração em uma instalação isolada antes de confiar no backup.

## Verifique após reiniciar o sistema

Confirme o espaço de trabalho e a chave esperados, a conexão com o Telegram, as fontes selecionadas e a captura de novas mensagens. O estado salvo do MTProto e a função de recuperação ajudam a recuperar atualizações que o Telegram ainda mantém. Não é possível reconstruir todas as atualizações expiradas ou uma edição excluída antes da captura.

O bom funcionamento do contêiner significa que o servidor web responde. Utilize uma mensagem controlada e uma verificação de testemunho para avaliar a coleta e a publicação externa.

## Publique apenas o que pretende

A referência de implantação inclui exemplos de HTTPS, comandos de volume persistente, atualizações e etapas de restauração. São fornecidos comandos do Docker para a implantação; o [registro de validação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/) atual identifica os ambientes efetivamente testados.
