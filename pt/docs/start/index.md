# Comece em poucos minutos

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/start/

Primeiro, explore um exemplo prático. Em seguida, conecte sua própria conta.

## Navegue pelo site sem precisar de uma conta

Baixe ou clone o projeto, instale **o Python 3.11 ou versão posterior** e execute a demonstração. O iniciador cria um ambiente local e instala as dependências indicadas.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

O navegador abre uma área de trabalho com mensagens fictícias. Abra uma conversa, compare uma edição e examine uma exportação. O modo de demonstração não se conecta ao Telegram.

![Visualização de conversas no TgWitness com exemplos de mensagens](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Um exemplo de área de trabalho. Seu próprio registro é iniciado separadamente.

## Crie seu próprio espaço de trabalho

Encerre o processo de demonstração e, em seguida, utilize o iniciador normal:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Abra o endereço local exibido pelo iniciador. Se solicitado, insira o **token de acesso ao painel** a partir do arquivo local indicado no terminal. Isso desbloqueia o TgWitness; trata-se de um processo distinto do login no Telegram.

## Registre sua primeira mensagem

1. [Conecte uma conta dedicada do Telegram.](https://phishdestroy.github.io/TgWitness/pt/docs/accounts/)
2. Selecione um grupo ou canal ao qual a conta tenha acesso e, em seguida, inicie a observação.
3. Envie uma nova mensagem em um grupo de teste sob seu controle e verifique se ela aparece no registro.

Para a instalação em servidor, siga as instruções em [“Keep it running](https://phishdestroy.github.io/TgWitness/pt/docs/server/)”.
