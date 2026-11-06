# Telegram · Chats secretos: implementação e demonstração

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/secret-chats/

Compreenda a implementação separada do Secret Chat, experimente a interface fictícia e analise os defeitos pendentes.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Status verificado em 6 de novembro de 2026:** existe uma implementação separada do Secret Chat em desenvolvimento. Ela ainda não foi incorporada ao `main` publicado em `3d23e52b647b`. O coletor comum e a exportação via Takeout não coletam Secret Chats. O cenário do site interativo demonstra a interface com dados fictícios; ele não permite a comunicação pelo Telegram.

## Onde a implementação está localizada

O commit `0e60f88e` adicionou **Sources → Pseudo-secret** no ramo de desenvolvimento local `fix/panel-routes-sessions`. O snapshot verificado é `bb8788fb685c`. Sua implementação inclui `tgwitness/secret_chats.py`, rotas do aplicativo, `tgwitness/static/views/secret-chats.js` e testes dedicados.

O complemento opcional `secret-chats` nesse ramo utiliza [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), fixado em `d87bf037b90060383c7b704d8a06ebb98c621c6f`. A biblioteca implementa o protocolo de bate-papo ponta a ponta do Telegram na autorização Telethon existente da conta. A instalação dessa biblioteca por si só não adiciona a integração ausente ao `main`.

## O que a interface de desenvolvimento faz

| Ação | Comportamento registrado |
| --- | --- |
| Inicie um bate-papo pelo nome de usuário ou ID do usuário | Envie uma solicitação; o outro participante deve aceitá-la. |
| Aceitar uma solicitação recebida | TgWitness passa a ser o ponto de extremidade de recebimento desse chat. A aceitação automática é uma configuração separada, desativada por padrão. |
| Enviar ou receber uma mensagem | Adicione um registro `secret_chat.message` de saída ou entrada e exiba-o na conversa. |
| Receber um anexo | Descriptografe-os, armazene seus bytes por SHA-256 e registre `secret_chat.file`. |
| Receber um aviso de temporizador ou de exclusão | Registrar o aviso e manter o conteúdo capturado anteriormente. |
| Revisar a conversa | Exiba mensagens, arquivos, avisos e a visualização da chave. A aba aberta é atualizada a cada quatro segundos. |

Em uma versão de desenvolvimento que contenha a integração, o operador habilita o módulo para a conta selecionada e o conecta. Iniciar, aceitar e enviar exigem permissão para interagir e que a proteção de somente leitura da conta esteja desativada. O outro participante deve aceitar um novo chat de saída. Esses controles não estão presentes no aplicativo publicado na revisão acima.

Apenas os chats criados ou aceitos por esta sessão TgWitness são abrangidos. Os chats secretos existentes em um celular permanecem nesse dispositivo. A importação de uma sessão não fornece suas chaves de criptografia separadas. O material de chave e os contadores dos chats secretos são armazenados no cofre do espaço de trabalho; as mensagens preservadas e os arquivos descriptografados seguem as proteções normais de armazenamento do espaço de trabalho.

## Demonstração no site

O cenário “**Try Secret Chat**” do site apresenta uma conversa fictícia. Ele permite que o leitor inicie uma solicitação, simule sua aceitação, envie uma mensagem de exemplo, receba uma resposta e um arquivo pré-definidos e inspecione um cronômetro e um aviso de exclusão. Uma solicitação recebida também pode ser aceita. Os controles identificam explicitamente as ações simuladas dos pares.

Este cenário é executado na memória do navegador. Ao reiniciar ou recarregar a página, ele é apagado. Ele não faz login, não entra em contato com o Telegram, não cria chaves de criptografia reais nem altera os downloads de amostras assinadas. As mensagens exibidas não constituem evidências assinadas. O cenário demonstra a interação pretendida; não certifica que a implementação do desenvolvimento esteja pronta.

## Verificações e defeitos pendentes

Os cinco testes existentes abrangem a persistência de chaves criptografadas, o ciclo de vida e os registros de mensagens, a política de aceitação de entradas, o envio somente leitura e a exportação de anexos. Eles foram aprovados em relação à biblioteca fixada durante a revisão de 6 de novembro. Três verificações sintéticas adicionais reproduziram defeitos no mesmo snapshot:

| Conclusão | Consequência |
| --- | --- |
| Fechamento contorna o `read_only` | O caminho de fechamento pode executar uma ação remota quando as interações devem ser bloqueadas. |
| A detecção de duplicatas pesquisa apenas registros recentes do 500 | Uma reprodução mais antiga pode criar uma duplicata após a reinicialização. |
| Um download de anexo com falha remove sua entrada pendente | Uma falha temporária faz com que a tarefa de repetição seja perdida. |

Essas são falhas conhecidas, também registradas na auditoria [publicada](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md). Cinco testes aprovados não abrangem essas falhas. A análise utilizou espaços de trabalho sintéticos e simulações de operações do Telegram; ela não repetiu um handshake em ambiente real nem qualificou a implantação em produção.
