# Armazenamento e recuperação

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/

Backups, transferência de arquivos mais antigos para a nuvem, cópias sob o Object Lock e recuperação em um novo computador.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Implantação e recuperação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)

![Implantação e recuperação](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

O painel separa três tarefas:

| Tarefa | O que ela faz |
| --- | --- |
| Mantenha um backup | Copie o diário assinado, os pontos de verificação, os arquivos preservados e as exportações na fila para o destino S3 configurado. |
| Espaço local gratuito | Copie os anexos mais antigos selecionados para o S3 ou para um servidor remoto na nuvem via rclone, recupere-os na íntegra, verifique os bytes criptografados e, em seguida, remova a cópia local verificada. |
| Mantenha uma cópia para fins de prova | Configure o S3 Object Lock e verifique o status de retenção retornado. O serviço deve confirmar o modo e a data solicitados. |

A liberação de espaço nunca exclui nem reescreve o diário assinado. Cada anexo mantém sua imagem original SHA-256 e um comprovante de recuperação. A compactação gzip opcional ocorre antes da criptografia autenticada. Os nomes dos arquivos na nuvem não contêm nomes do Telegram, IDs de bate-papo ou nomes originais dos anexos. Um anexo pode ter até 32 GiB.

Uma resposta de upload, por si só, não constitui permissão para excluir um arquivo. TgWitness baixa o objeto criptografado completo e verifica seu tamanho; SHA-256 salva o comprovante e, em seguida, verifica os bytes locais novamente imediatamente antes da remoção. Uma falha no upload, uma leitura diferente ou uma transferência cancelada mantêm o arquivo local no lugar. Se um backup de evidência ativado ainda não tiver copiado esse arquivo, a remoção também aguarda até que isso ocorra.

**Nesta página**

- [Quando o disco estiver ficando cheio](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#when-the-disk-is-filling-up)
- [Conectar um destino](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#connect-a-destination)
- [Manter o arquivo de recuperação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#keep-the-recovery-file)
- [Recuperação após perda da instalação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#recover-after-losing-the-installation)
- [Bot de operador e avisos de conclusão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/storage/#operator-bot-and-completion-notices)

## Quando o disco está ficando cheio

Os downloads de anexos são pausados abaixo do espaço definido em **Parâmetros → Anexos → espaço livre em disco** (1 GiB por padrão), mantendo a fila. As observações de texto continuam. Isso independe das notificações: desativá-las não desativa a reserva de download nem as proteções do armazenamento.

Para agir antes, habilite **Executar automaticamente**, escolha **Remover o arquivo local para liberar espaço** e habilite **Iniciar uma transferência extra quando houver pouco espaço em disco**. Por padrão, a regra opcional começa abaixo de 5120 MiB livres e processa lotes até atingir 10240 MiB. Ambos os limites são configuráveis. Usa o mesmo destino, idade mínima dos arquivos, limite do lote, verificação por releitura completa e requisitos de backup das evidências da execução manual. Nunca habilita um destino sozinha. As verificações ocorrem a cada 30 segundos; um erro ou falta de progresso adia a próxima tentativa por cinco minutos. O estado e o horário da nova tentativa sobrevivem à reinicialização. Quando a regra está inativa, as execuções agendadas mantêm seu intervalo normal.

O painel mostra espaço livre, reserva de empacotamento, se a regra está pronta e arquivos ignorados por falta de espaço temporário. Empacotamento e restauração verificam a necessidade máxima de espaço temporário antes de começar e o espaço disponível durante a gravação. A reserva é a configurada para downloads, com mínimo de 64 MiB nas operações de armazenamento. Não é uma cota do sistema de arquivos: outro processo pode consumir espaço entre verificações.

A compressão Gzip é sem perdas e se aplica a objetos remotos; não reduz o diário ativo nem cria arquivos compactados locais. JPEG, vídeos e ZIP podem diminuir muito pouco ou crescer ligeiramente. Com compressão habilitada, o empacotamento pode precisar temporariamente de aproximadamente duas vezes o tamanho do anexo mais a reserva. Escolha um limite de início adequado aos maiores arquivos. Arquivos grandes demais são mantidos e informados; os menores e as cópias remotas já verificadas ainda podem liberar espaço. Uma cópia verificada permite remover o arquivo local sem outro arquivo de empacotamento. A restauração também precisa de espaço temporário e pode ser recusada até ele estar disponível.

Se não houver arquivos elegíveis para mover ou nenhum destino estiver configurado, o TgWitness não poderá recuperar espaço automaticamente. O gerenciamento de armazenamento nunca reduz nem reescreve o diário assinado. Ele continua precisando de espaço para novas observações de texto.

## Conecte um destino

Em **Extras → Armazenamento e espaço em disco → Gerenciar armazenamento**, escolha a tarefa e o destino, salve-a e, em seguida, selecione **Testar upload e download**. O teste faz o upload de uma pequena amostra aleatória e a lê de volta. Ele não utiliza conteúdo do Telegram.

Para o S3, use o endpoint, a região e o bucket reais do provedor. Wasabi, Backblaze, Cloudflare R2 e outros serviços compatíveis utilizam as mesmas configurações do S3. Uma API compatível, por si só, não implica suporte ao Object Lock. O modo de governança pode permitir que um administrador autorizado ignore a retenção; o modo de conformidade possui diferentes restrições. Verifique o status do Object Lock retornado antes de confiar na retenção.

Para um destino do rclone, crie um remoto usando a configuração de provedor do rclone e cole a seção desse remoto `[name]` seção desse remoto no painel. O auxiliar instalado oferece suporte a MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud e os outros provedores exibidos no seletor. As credenciais são salvas no cofre criptografado deste espaço de trabalho. As atualizações do OAuth são salvas de volta no cofre. As credenciais não são adicionadas aos eventos do diário nem incluídas nos downloads de recuperação.

O auxiliar é instalado dentro do espaço de trabalho, com uma versão fixada e SHA-256. Ele não é adicionado ao PATH do sistema. Os arquivos de configuração e de trabalho são arquivos temporários dentro desse espaço de trabalho. Remotos baseados em comandos e em arquivos locais são rejeitados. Atualmente, o rclone requer uma rota **Direct** explicitamente selecionada para solicitações externas. Use o armazenamento S3 nativo para uma rota SOCKS5 ou HTTP do espaço de trabalho; o rclone não ignora silenciosamente uma rota indisponível.

## Guarde o arquivo de recuperação

Selecione **“Salvar arquivo de recuperação”** após copiar os arquivos e guarde-o em um local separado da instalação. Ele contém a chave de descriptografia e os recibos assinados dos objetos, portanto, trate-o como um backup de chave privada. Mantenha a configuração remota original e as credenciais de destino separadamente também. Um arquivo de recuperação criado antes de uma cópia posterior não contém o recibo desse arquivo posterior.

A impressão digital da chave de assinatura já deve estar registrada separadamente. Uma assinatura verificada apenas em relação à chave fornecida dentro do mesmo arquivo não determina de quem é o arquivo de recuperação.

Para recuperar recibos de armazenamento ausentes em um espaço de trabalho existente, abra **“Recuperar arquivos a partir de um arquivo de recuperação salvo**” e selecione o arquivo. O painel verifica a assinatura e exige a mesma chave de assinatura do espaço de trabalho. Ele não aceita a substituição por uma chave de armazenamento diferente. Em seguida, escolha **“Restaurar todos os arquivos**”. A restauração suspende a regra de armazenamento automático para que a próxima execução agendada não possa remover imediatamente os arquivos restaurados novamente. Reative a regra quando terminar de usar as cópias locais.

A restauração verifica o texto cifrado, autentica a descriptografia, descompacta, se necessário, e verifica o texto simples original SHA-256 antes de colocar um arquivo em `media/`. Um objeto remoto corrompido nunca substitui um arquivo local. Um arquivo local existente com bytes diferentes é mantido para análise, em vez de ser sobrescrito.

## Recuperação após perda da instalação

Instale o TgWitness em outra máquina. Use o arquivo de recuperação privado, a impressão digital registrada separadamente e as credenciais de destino originais:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Para o S3, `--credentials` aponta para um arquivo JSON privado com `access_key` e `secret_key`; o arquivo de recuperação assinado fornece as configurações de destino. O comando usa uma conexão externa direta e baixa o auxiliar fixado quando um remoto do rclone precisa dele. Ele rejeita um diretório de saída já existente.

Os bytes originais recuperados são gravados em `recovered-attachments/media/`, nomeados por seus SHA-256s. `recovery-log.jsonl` é um registro não assinado das operações de recuperação. O comando não recria um diário assinado perdido nem sua chave de assinatura. Mantenha um backup completo do espaço de trabalho para esses fins. Um arquivo de recuperação de armazenamento não é um backup completo do espaço de trabalho .

## Bot de comando e notificações de conclusão

O bot do Telegram pertence ao operador. Crie-o por meio do BotFather e defina seu token, o chat de destino e os IDs de usuários do Telegram explicitamente permitidos no painel. Tanto o remetente quanto o chat devem corresponder. Mensagens encaminhadas e comandos de outros bots são ignorados.

`/status` e `/stats` estão disponíveis no modo padrão, que exibe apenas o status. O modo de controle opcional adiciona `/pause`, `/resume` e `/copy`. `/copy` solicita a tarefa de armazenamento configurada; isso não significa que um upload remoto já tenha sido concluído. Os comandos não podem fornecer URLs, arquivos ou programas de shell arbitrários.

Use as configurações de notificação separadas para alertas e conclusão de tarefas. As notificações de conclusão distinguem uma exportação de conta com lacunas de uma exportação completa e mostram o histórico e as contagens de armazenamento. Trechos de mensagens não são incluídos, a menos que sejam ativados separadamente nas configurações de notificação. O seletor de serviços é gerado a partir do catálogo real do Apprise instalado, em vez de um conjunto fixo de exemplos de provedores.
