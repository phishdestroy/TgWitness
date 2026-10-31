# Um diário. Quatro modos de coleta. Oito níveis de verificação.

Canonical page: https://phishdestroy.github.io/TgWitness/pt/guides/modes.html

Modos, cenários e níveis de evidência

TgWitness registra o que a conta conectada observa. Um terceiro pode verificar a integridade do registro em relação a uma chave confiável independente.

[Modos de coleta](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#scope)[Cenários](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#scenarios)[Níveis de evidência](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#levels)

Visão geral de 3 a 5 minutos · exemplos fictícios · implementação atual

1. **Telegram**

   Atualizações visíveis na conta
2. **Coletor**

   Registros vinculados, cada um assinado
3. **Verificador**

   Chave confiável + limite mantido

`h₁ → h₂ → h₃ · Ed25519`A integridade é verificada. A origem do Telegram e a veracidade de uma mensagem continuam sendo questões distintas.

## Escolha o escopo de observação

Três escopos e uma predefinição de investigação. As exclusões e os tipos de fonte habilitados continuam válidos.

Padrão**Bate-papos selecionados**

Registros

Apenas fontes selecionadas manualmente.

Novas conversas

Não é adicionado automaticamente.

Opte por

Um conjunto conhecido de canais ou grupos. Nenhuma capacidade fixa de bate-papo foi definida.

**O que não faz** Ele não detecta outros chats nem preenche o histórico anterior.

Pasta de contas**Pasta do Telegram**

Registros

Inclusões de pastas e categorias, excluindo exclusões e conversas arquivadas, quando configuradas.

Novas conversas

Correspondência de conversas ativas; alterações nas pastas em até uma hora.

Opte por

Um analista já mantém uma pasta de caso. Confirme a coleta em uma conta dedicada.

**O que não faz** Isso não se aplica às condições variáveis muted/read da pasta.

Confirme o escopo**Conta completa**

Registros

Bate-papos visíveis na conta, incluindo conversas privadas e bots, dentro dos tipos selecionados.

Novas conversas

A ser adicionado quando a primeira atualização for disponibilizada.

Opte por

Uma conta dedicada à observação, incluindo uma conta que participe de um caso.

**O que não faz** Ele não entra em chats automaticamente nem contorna o acesso à fonte.

Configuração pré-definida para toda a conta**Modo de investigação**

Registros

Todos os tipos de fontes, ações próprias, perfis de fontes e as últimas 200 mensagens visíveis de fontes recém-descobertas.

Novas conversas

Um novo chat ou bot recebe um perfil e um instantâneo do histórico.

Opte por

Junte-se a uma equipe ou interaja com um bot por meio do painel. Revise e salve a predefinição.

**O que não faz** Ele não captura instantâneos de todos os chats existentes nem observa chamadas de retorno pressionadas em outro cliente.

Esses cartões são uma comparação local, não controles do coletor em tempo real. Eles não alteram uma conta.

**O que não faz** Nenhum modo lê conversas secretas, grava enquanto o processo está parado, junta-se a fontes por conta própria ou recupera histórico anterior além do solicitado snapshot/export.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/)

## Captura com GitHub Actions (prévia)

Um novo login no Telegram, uma conversa, um arquivo criptografado e procedência do GitHub.

[Abrir o assistente de captura](https://phishdestroy.github.io/TgWitness/pt/docs/capture/)

## O que é registrado

Apenas as observações entregues ou explicitamente solicitadas são registradas. Atribuições desconhecidas permanecem desconhecidas.

 Captura de opções · ilustração localNovas mensagensEdiçõesExclusõesReaçõesAfiliação

O painel aplica essas opções por espaço de trabalho. Desativar uma delas mantém os registros existentes; reativá-la não reconstrói eventos perdidos.

**Matriz de eventos: material salvo e incógnitas remanescentes**

| Categoria | Salvo | Ainda é desconhecido |
| --- | --- | --- |
| Mensagem | Texto, IDs, metadados do remetente, contexto da resposta e envelope de atualização original. | Não há assinatura do Telegram verificável por terceiros. |
| Editar | Todas as versões observadas, sem sobrescrever as anteriores. | Edições intermediárias podem passar despercebidas; o remetente não é necessariamente o editor. |
| Exclusão | Aviso, além do texto salvo anteriormente, se disponível. | O eliminador e o horário exato da ação não são fornecidos. |
| Exclusão fora do escopo | Aviso no nível da conta; o par desconhecido permanece explícito. | Sem suposições sobre conversas. A correlação utiliza IDs salvos anteriormente no âmbito da conta, sempre que possível. |
| Reação | Contadores entregues e identidades recentes visíveis. | Nem todos os reatores são visíveis; uma lista completa disponível requer consultas separadas. |
| Afiliação | Mensagens de serviço entregues e atualizações dos participantes. | A função e o tipo de chat limitam a visibilidade; o silêncio não implica ausência. |
| Anexo | Descritor da versão original, bytes salvos, SHA-256 e resultados das tentativas. | Um arquivo que desapareceu pode estar indisponível; uma versão mais recente não o substitui. |
| Instantâneo do histórico | Mensagens atualmente visíveis, marcadas como observações do histórico. | Edições anteriores e conteúdo excluído não são reconstruídos. |
| Ações próprias | Saída messages/edits e os metadados correspondentes do teclado de resposta button_press . | Os callbacks acionados em outro cliente do Telegram não são visíveis. |
| Botões do bot | Metadados de callback, URL, aplicativo web e solicitação são retidos junto com a mensagem. | URLs e phone/location solicitações são texto, não são abertas nem executadas automaticamente. |

### Limites padrão para anexos

Fotos

20 MiB

Vídeo

100 MiB

Arquivos

50 MiB

Animações

20 MiB

Notas em vídeo

50 MiB

Voz

20 MiB

Áudio

50 MiB

Adesivos

5 MiB

**O que não faz** Um switch não suprime metadados incorporados nem desativa registros operacionais. A captura não identifica um agente que não tenha sido fornecido pelo Telegram.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/)

## Utilize a autorização de que dispõe

Cada conta possui seu próprio espaço de trabalho, diário, chave de assinatura, rota e fila.

### Telefone + código

Insira 2FA quando estiver habilitado.

### QR código

Faça a leitura a partir de um dispositivo autorizado; 2FA pode ainda ser necessário.

### Telethon .session

Importe o arquivo de sessão da conta.

### Pyrogram .session

Importe o Pyrogram .

### TData ZIP

Uma conta do Desktop suportada; senha local, se definida.

### StringSession texto

Cole um Telethon StringSession.

### .session + .json

Selecione a sessão e os metadados associados correspondentes.

### Chave de autenticação HEX + DC ID

Importe a autorização da conta com seu identificador de data center.

**API par**

Seu próprio API par é opcional. Na ausência dele, TgWitness o sistema utiliza um conjunto de pares públicos, incluindo pares do Telegram Desktop oficial.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy é experimental; as listas públicas integradas MTProxy estão disponíveis. Uma rota de proxy com falha não recorre a uma conexão direta.

Dois espaços de trabalho em uma mesma máquina não constituem duas testemunhas independentes.

**O que não faz** A importação não contorna a autorização do Telegram, 2FA nem formatos de sessão não suportados. As contas continuam compartilhando o processo do aplicativo.

[Formatos de conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/)

## Aja a partir do painel

Envie ou responda, pressione um botão do bot atual, salve uma pré-visualização do link e, em seguida, entre explicitamente em um chat ou inicie um bot com seu parâmetro de inicialização.

`interaction.preview``interaction.requested``interaction.result`

Os recibos de pré-visualização, solicitação e resultado são assinados. Antes de um botão ser pressionado, o servidor busca a mensagem novamente e rejeita um teclado alterado. O texto e as URLs de retorno de chamada permanecem como contexto registrado.

**O que não faz** Sem aplicativos web, pagamentos, phone/location compartilhamento ou consultas embutidas. Exibir uma URL não a abre.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/)

## Recuperação e continuidade

As lacunas são mostradas, não ocultadas.

### Retomar a posição salva

Após a reinicialização, o Telegram é solicitado a buscar atualizações perdidas. A retenção finita e as diferenças expiradas podem deixar lacunas.

### Verifique novamente as mensagens visíveis

Padrões: fontes prioritárias a cada 15 minutos, outras a cada 6 horas. Os resultados incluem message.recovered e message.missing_on_recheck.

### Leia coverage.json

Períodos de observação, lacunas com justificativas e IDs não observados acompanham a exportação assinada. Um registro ausente na nova verificação não constitui um aviso de exclusão.

**O que não faz** Um instantâneo posterior do histórico não apaga uma interrupção nem recupera todas as versões perdidas. O cursor salvo não constitui uma confirmação sem perdas da aceitação do diário.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

## Sete níveis. Perguntas diferentes.

Cada mecanismo responde a uma questão delimitada. Configure serviços externos separadamente e mantenha suas âncoras de confiança fora do coletor.

1. ### Registrar

   SHA-256 cadeia + Ed25519 por evento; o primeiro previous_hash é composto por 64 zeros.

   **Verificações por terceiros** Ordenação e assinaturas sob a chave coletora fixada.

   **O que não faz** Isso não comprova a origem do Telegram nem sua integridade.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Contêiner

   manifest.json lista os hashes dos arquivos; manifest.sig assina-o. media.saved vincula os bytes do anexo a um evento.

   **Verificações por terceiros** Os arquivos fornecidos estão em conformidade com o manifesto assinado e os recibos de mídia.

   **O que não faz** Ele não assina um arquivo baixado separadamente CSV, HTML ou captura de tela baixada separadamente.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Limite mantido

   Ponto de verificação na inicialização, a cada 5 minutos por padrão, e encerramento ordenado. Mantenha uma cópia em outro local.

   **Verificações por terceiros** A exportação posterior está de acordo com o comprimento e o cabeçalho retidos anteriormente; é possível detectar uma reversão.

   **O que não faz** Ele não detecta a substituição tanto do diário quanto de todos os pontos de verificação retidos.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Tempo externo

   O modo de evidência envia um ponto de verificação SHA-256 às RFC 3161 autoridades (FreeTSA, DigiCert) e OpenTimestamps calendários.

   **Verificações por terceiros** Uma resposta TSA verificada data esses bytes; uma OpenTimestamps prova os vincula ao Bitcoin.

   **O que não faz** Ele não trata uma solicitação preparada ou um recebimento pendente do calendário como um carimbo de data/hora confirmado.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Testemunha independente

   Host separado, endpoint de leitura exclusiva com escopo definido, desafio novo e seu próprio key/journal e TGW1 publicações no canal.

   **Verificações por terceiros** Heads aceitos anteriormente; status ok, key_changed, reversão, bifurcação, inválido e no_response.

   **O que não faz** Isso não transforma dois espaços de trabalho em um único host coletor em testemunhas independentes.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Réplica externa

   S3Cópia compatível com [...], criptografada com AES-256-GCM; Object Lock quando o bucket oferecer suporte a isso.

   **Verificações por terceiros** A função `Restore` publica arquivos somente após a verificação bem-sucedida do diário, do ponto de verificação e da mídia preservada.

   **O que não faz** Ele não restaura sem a chave exportada nem presume a retenção sem verificar a resposta do armazenamento.

   **Comando de verificação**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Executar proveniência

   Recibo de execução assinado: hashes de código-fonte, versões de dependências e contexto do processo. Auto-relatado.

   **Verificações por terceiros** O que o coletor de assinaturas relatou sobre sua própria execução.

   **O que não faz** Ele não fornece atestado independente do processo nem exclui a possibilidade de comprometimento antes do registro.

   **Comando de verificação**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### O que nenhum nível comprova

Entrega de todas as atualizações do Telegram; a veracidade do texto; que o ID do remetente identifique uma pessoa real; ausência de comprometimento do coletor antes do registro; admissibilidade em tribunal.

[Testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/)

Experimento SHA-256 experimento

### Tente alterar o registro 2

O próximo registro mantém o link salvo anteriormente. Alterar o texto altera o hash calculado do registro 2.

Texto do registro 2

Registro 1`h1`Começa com 64 zeros

Registro 2`h2`Inclui os arquivos salvos h1

Registro 3`h3`Inclui os arquivos salvos h2

Exemplo estático: h2 abrange “Encontro às 11h”. Alterar esse texto altera h2; o registro 3 ainda faz referência ao que foi salvo h2.

**Inspecione os resumos completos**

Hash do registro 2 salvo

`SHA-256(e₂)`

Hash recalculado do registro 2

`SHA-256(e₂)`

Este exemplo calcula hashes, não assinaturas. O verificador real compara cada assinatura e link com a chave confiável.

 [Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/how-it-works/)

## Escolha um caminho por meio das evidências

Situações fictícias. Inicie a coleta antes do evento relevante; preserve os limites e as lacunas juntamente com o conteúdo.

### Um canal altera os detalhes de pagamento

Modo → eventos

Bate-papos selecionados → mensagens, edições, exclusões.

Saída

Versões de publicações e anexos observados por hash.

Verificação

Assinado ZIP + ponto de verificação retido + resposta TSA verificada.

**O que não faz** Ele não recupera um original que nunca foi capturado.

### As mensagens desaparecem após um incidente

Modo → eventos

Pasta ou conta inteira → todas as categorias de eventos.

Saída

Originais salvos, avisos de exclusão e cobertura com lacunas.

Verificação

Assinado ZIP + diário de testemunho independente.

**O que não faz** Ela não identifica quem excluiu a partir de uma notificação que não indica nenhum agente.

### Investigue um bot de loja

Modo → eventos

Configuração pré-definida de investigação → botões, visualizações de links e ativação explícita do bot.

Saída

Recibos de interação assinados, callbacks retornados e perfis salvos.

Verificação

Assinado ZIP; verifique qualquer dossiê em relação ao ZIP.

**O que não faz** Ele não abre um aplicativo web de bot, não efetua pagamentos nem registra callbacks de outro cliente.

### Um participante altera seus nomes entre as conversas

Modo → eventos

Qualquer escopo → metadados sender/profile metadados.

Saída

Histórico de nomes/nomes de usuário por ID numérico, links “também em” e pistas extraídas.

Verificação

Dossiê JSON verificado em relação ao documento assinado ZIP.

**O que não faz** Isso não transforma uma carteira, uma sequência de caracteres semelhante à de um telefone ou um nome de usuário em identidade comprovada.

### Observação de longo prazo com uma cópia externa

Modo → eventos

Qualquer escopo → Modo de evidência e uma S3 réplica com suporte a Object Lock.

Saída

Cópia criptografada, pontos de verificação retidos e respostas com carimbo de data/hora.

Verificação

Restaure com a chave exportada e, em seguida, verifique sem o servidor original.

**O que não faz** Isso não substitui uma testemunha independente nem uma chave de descriptografia mantida separadamente.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/investigation/)

## Entregue um pacote verificável

Forneça o original assinado, uma impressão digital da chave mantida de forma independente, o ponto de verificação relevante e o resultado da verificação.

- Assinado ZIP
- JSONL
- CSV
- HTML
- Ponto de verificação
- Confirmação de execução
- Exportação de bate-papos: chat.json / chat.html
- Dossiê JSON
- Protegido por senha AES-256 ZIP
- Exportações separadas para várias contas
- CLI de streaming: 5 GiB limite padrão

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Obtenha o verificador a partir de uma cópia confiável, e não do arquivo que está sendo verificado.

**O que não faz** Autônomo CSV e HTML não são contêineres assinados. Uma senha protege a confidencialidade da transferência, não a autenticidade. Exportações múltiplas não unificam os diários das contas.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

## Compare o artefato entregue

Artefatos básicos sem sistemas adicionais de assinatura, carimbo de data/hora ou testemunha. Os scripts e registradores variam de acordo com a implementação; “parcial” significa limitado ao material capturado ou visível.

| Abordagem | Edições / exclusões | Assinatura do registro | Tempo externo | Testemunha independente | Cobertura / lacunas | Verificação sem autor |
| --- | --- | --- | --- | --- | --- | --- |
| Exportação do Telegram Desktop | Parcial | Não | Não | Não | Não | Não |
| Telethon script de snapshot | Parcial | Não | Não | Não | Não | Não |
| Registrador de exclusões: registro de texto | Parcial | Não | Não | Não | Não | Não |
| Capturas de tela / captura da web | Parcial | Não | Não | Não | Não | Não |
| TgWitness com extras configurados | Parcial | Sim | Sim | Sim | Parcial | Sim |

**O que não faz** A tabela não avalia todos os scripts ou produtos de registro. As verificações opcionais de tempo e de testemunhas exigem seus próprios serviços e âncoras de confiança; nenhuma delas estabelece a verdade da fonte.

[Leia os detalhes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

## Mantenha os limites de acordo com as evidências

A verificação é útil quando seu escopo permanece explícito.

- As conversas secretas não estão disponíveis.
- Nada é registrado enquanto o processo estiver parado; a recuperação é limitada.
- Um registro verificado não é prova de que seu conteúdo seja verdadeiro.
- Um operador com a chave pode assinar qualquer conteúdo. Testemunhas independentes e carimbos de data/hora restringem a substituição posterior, não a captura inicial desonesta.
- Utilize uma conta dedicada, não sua conta principal.
- O Telegram pode restringir contas devido ao volume de solicitações.

**O que não faz** Nenhum modo ou nível de evidência estabelece admissibilidade legal, entrega completa do Telegram ou identidade no mundo real.

[Guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)[Conta dedicada](https://phishdestroy.github.io/TgWitness/pt/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)[INVESTIGATION.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/investigation/)
