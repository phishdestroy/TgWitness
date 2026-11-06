# Mantenha-o em funcionamento

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/server/

Mantenha o coletor no ar e os dados seguros entre reinicializações.

## Escolha um método de inicialização

Nativo: o [inicializador](https://phishdestroy.github.io/TgWitness/pt/docs/start/) mais os modelos de serviço em [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, a partir da pasta do projeto:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

O painel escuta em localhost:8787. Abra localmente ou por um túnel SSH, com o token do segundo comando.

## Mantenha todo o diretório de dados

Nativo: `data/live`. Docker: o volume `tgwitness-data`. Diários, sessões e chaves andam juntos. Uma exportação assinada é evidência, não backup.

1. Pare a coleta primeiro.
2. Copie o diretório de dados inteiro para um lugar seguro, fora do host.
3. Tente restaurar em uma instalação separada antes de confiar.

## Verifique após reiniciar o sistema

Confira o espaço e a chave, a conexão, as fontes e se mensagens novas chegam. O TgWitness recupera o que o Telegram ainda tem, não tudo o que aconteceu enquanto estava parado.

Contêiner "saudável" significa que o servidor web responde. Se a coleta funciona, quem diz é uma mensagem de teste e a testemunha.

## Publique apenas o que pretende

HTTPS, volumes, atualizações e restauração estão na referência de implantação. O que foi realmente testado: [registro de validação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/).
