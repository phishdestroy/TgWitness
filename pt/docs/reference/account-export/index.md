# Exportação de contas

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/account-export/

Exporte o que uma conta pode ler no momento: escopo, tarefas retomáveis, um arquivo assinado e cópias de compartilhamento minimizadas.

Uma exportação de conta reserva essa conta exclusivamente. Pause explicitamente o monitoramento ou outra coleta antes de iniciar ou retomar; o aplicativo nunca a interrompe automaticamente.

Como administrador da instalação, selecione **“Comece aqui” → “Exportar minha conta**” ou **“Exportações” → “Conta do Telegram” → “Configurar exportação da conta**”. Faça login, se necessário, revise o escopo e inicie explicitamente a exportação. Não é necessária observação contínua. **“Observações salvas”** é uma exportação separada do diário existente; seu ZIP inclui todas as fontes, independentemente dos filtros do diário. Cada espaço de trabalho possui suas próprias tarefas, identidade de assinatura e armazenamento. O acesso concedido ao painel, incluindo uma autorização de exportação comum irrestrita, não permite acessar essas rotas válidas para toda a conta.

Os filtros de remetente e de texto são expandidos em **“Filtrar por remetente ou texto da mensagem**”. A seção **“Dados da conta e método de conexão”** contém categorias opcionais de contas e a opção “Takeout/sessão regular”; seu resumo mostra as opções ativas mesmo quando fechada. Fechar essas seções mantém suas configurações. Rascunhos de exportação e relatórios permanecem na sessão atual do painel ao alternar entre visualizações; eles não são salvos ao recarregar o navegador. Tarefas existentes continuam acessíveis a partir de qualquer uma das opções de exportação.

Este fluxo de trabalho exporta os dados atualmente acessíveis à conta conectada. Por padrão, utiliza-se [o Telegram Takeout](https://core.telegram.org/api/takeout); não se trata de um backup de dados do Telegram indisponíveis ou excluídos. Bate-papos secretos, histórico inacessível e edições anteriores não são recuperados. O Telegram pode impor um período de espera antes do início do Takeout. O painel exibe esse tempo de espera; ele não altera o método de transporte silenciosamente. A opção explícita da API regular tem cobertura diferente e registra categorias não suportadas.

Takeout is the official export API also used by Telegram Desktop. TgWitness can write Desktop-compatible JSON directly from its own acquisition; importing someone else's archive is not required. Chat and message IDs are available through both transports. A public chat or permission to forward does not guarantee a faster export or remove Takeout's approval delay. Measure the same scope and media settings before comparing speed.

For up to 20 explicitly selected chat IDs, regular-API export resolves those peers directly before considering the account's complete dialog inventory. A readable public channel can therefore be exported without joining it, even when it is absent from the dialog list. Uncached peers fall back to the ordinary inventory. The archive filter remains enforced: if Telegram does not return a dialog and archived chats are excluded, the unknown archive status is recorded as an omission. Takeout keeps its split-range inventory procedure. Neither path joins chats or changes forwarding permissions. In Desktop-compatible JSON, channels that Telegram marks `left` appear under `left_chats`, including readable public channels the account has not joined.

Both `FLOOD_WAIT` and `FLOOD_PREMIUM_WAIT` pause requests for the full server-requested period. The account's deadline is persisted across reconnects and restarts; a shorter later wait cannot shorten it. Retries are bounded, cancellation preserves sealed pages, and API credentials are not rotated to bypass a rate limit. No Premium purchase is made.

## Escolha o que será coletado

| Contexto | Significado |
| --- | --- |
| Objetivo | Registre por que essa aquisição é necessária. Não inclua nomes desnecessários ou detalhes confidenciais do caso aqui. |
| Idioma do relatório | Escolha o idioma dos rótulos do relatório legível. O texto original da mensagem permanece inalterado; os rótulos do modelo não traduzidos utilizam o inglês. O idioma é definido pelas opções da tarefa assinada. |
| Tipos de chat / IDs de chat | Todos os tipos selecionados ou apenas os chats listados; as “Mensagens Salvas” pertencem a chats privados. Os chats arquivados podem ser selecionados separadamente. |
| Datas | UTC. As datas do calendário “De” e “Até” do painel estão ambas incluídas. A API utiliza intervalos inclusivos `from_utc` e exclusivos `to_utc`; o painel envia o início do dia seguinte à data “Até”. Um limite vazio deixa esse lado sem restrições. |
| IDs de remetentes | Apenas mensagens dos remetentes listados; uma lista vazia inclui todos os remetentes. |
| O texto contém | Expressões literais que não diferenciam maiúsculas de minúsculas são combinadas com “OU”. Condições de remetente/data/mensagem própria são combinadas com “E”. |
| Mensagens próprias | Mantenha apenas as mensagens enviadas. |
| Tipos de mídia | Selecione categorias de anexos ou desmarque todas para evitar o download de arquivos de mensagens. |
| Limites de arquivos / mídia total | MiB por arquivo e GiB total de mídia baixada. Textos, recibos, relatórios legíveis e sobrecarga de ZIP exigem espaço adicional em disco. |
| Categorias de contas | Perfil, contatos, fotos de perfil, stories, metadados de sessão e outros dados do Takeout possuem controles separados. |

A predefinição **“Minimize”** desativa arquivos e metadados de contas. Os filtros de remetente/conteúdo são aplicados antes das páginas de mensagens retidas e dos downloads de mídia. O Telegram ainda transmite páginas do histórico da API contendo mensagens necessárias para avaliar esses filtros: a filtragem não garante que mensagens não selecionadas nunca entrem na memória do processo. Outras observações em andamento no espaço de trabalho têm seu próprio escopo e configurações de retenção.

O histórico de fotos de perfil e as histórias não são selecionados por padrão. Desative também o perfil e os contatos quando o caso precisar apenas de mensagens. Se anexos ou metadados forem desnecessários, excluí-los durante a aquisição evita a retenção de outra cópia privada nesta exportação.

Photo payloads use the still-image variant identified in their metadata and hash manifests, including photos with an animated avatar variant. That animation is not substituted for the selected still image. A shorter or longer payload than the observed size is recorded as a failed attachment, and a changed representation during file-reference renewal is rejected. These failures leave the archive partial while retaining the message records. Independent verification also rejects saved attachments whose signed length contradicts their observed size or representation, including in older archives.

## Resumo, cobertura e verificação

Cada tarefa congela suas opções e a identidade da conta. O inventário e as páginas capturadas são assinados; os recibos das páginas registram hashes, cursores, horários, resultados de anexos e seus recibos anteriores. Somente páginas confirmadas avançam no progresso. A função “Reiniciar/Retomar” verifica esses registros antes de continuar. Uma conta alterada, uma página assinada alterada ou uma cadeia de recibos inconsistente é rejeitada. As opções não podem ser editadas no meio de uma aquisição: inicie outra tarefa para outro escopo.

A função “Pausar” interrompe a operação da conta em execução. Reiniciar o aplicativo deixa o trabalho inacabado disponível para retomada explícita. Uma sessão do Takeout expirada requer uma retomada explícita; alterar os intervalos de divisão do Telegram pode exigir uma nova aquisição. A função “Retomar” mantém as observações anteriores, de modo que uma exportação de longa duração não é um instantâneo atômico único. Outras operações de alteração de conta e exportações conflitantes são bloqueadas durante a aquisição. Aguarde a conclusão da compactação antes de excluir um espaço de trabalho.

A função “Retomar” verifica o conteúdo já capturado antes de continuar. Arquivos grandes em armazenamento lento podem exceder o tempo de espera configurado **Parâmetros → Tempo limite de ação do painel** (120 segundos por padrão). Aumente essa configuração antes de tentar novamente; o cancelamento ou a interrupção do armazenamento deixa uma tarefa em pausa, e verificações de integridade com falha resultam em uma tarefa com falha acompanhada de uma explicação. A verificação deve ser concluída ou interrompida com segurança antes que os arquivos possam ser fechados. Nenhuma afirmação sobre a taxa de processamento de contas grandes foi validada pelas verificações sintéticas.

O painel distingue um escopo selecionado e concluído de um arquivo parcial e registra omissões e falhas na leitura. Arquivos deliberadamente excluídos são diferentes de arquivos com falha ou indisponíveis. Verifique a cobertura mesmo quando a verificação de integridade for bem-sucedida. Nenhum leitor local pode comprovar que o Telegram retornou todas as mensagens que já existiram.

ZIPs concluídos permanecem disponíveis para downloads repetidos e por intervalo HTTP. Um arquivo de conta contém `manifest.json`, `manifest.sig`, assinados `job.json`, `inventory.json`, `receipts/`, oficiais `data/*.jsonl`, selecionado `media/`, HTML legível e um verificador. Fixe a impressão digital do coletor por meio de um canal independente e, em seguida, verifique usando uma instalação confiável:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Para arquivos cujo conteúdo expandido exceda 4 GiB, defina um limite explícito adequado `--max-gib`. O painel verifica seus arquivos locais autenticados e completos usando o tamanho expandido declarado e o resumo publicado ZIP; a CLI externa mantém seu limite de tamanho independente. Verifique antes de abrir o HTML legível. O verificador integrado ao arquivo é prático, mas um verificador obtido de forma independente evita a necessidade de confiar no código executável fornecido junto com a evidência.

A assinatura Ed25519 e os hashes SHA-256 detectam alterações após o coletor ter gravado os bytes relevantes. Eles **não** comprovam que o Telegram assinou essas mensagens, que o operador do coletor agiu com honestidade, que o histórico da conta está completo ou que um tribunal aceitará o material. Os horários de captura são baseados no relógio do coletor. Carimbos de data e hora independentes e a proveniência independente da aquisição devem ser avaliados separadamente.

## Prepare uma divulgação para um advogado ou outro destinatário

Após baixar uma exportação concluída, mantenha o arquivo original ZIP e abra `index.html` a partir de uma cópia extraída. O relatório explica seu escopo, cobertura disponível e limites. Suas referências de registro combinam a referência do arquivo, o caminho do documento e o número do registro, para que o destinatário possa localizar a mesma entrada no HTML ou na impressão. Para ver um exemplo prático, [abrir o relatório fictício](https://phishdestroy.github.io/TgWitness/demo/report/).

A partir de uma exportação de conta concluída, selecione **“Preparar uma cópia para compartilhamento**”. Isso gera um derivado assinado separado. A fonte ZIP permanece inalterada e privada; não a envie junto com um derivado minimizado, a menos que o destinatário esteja autorizado a receber seu conteúdo completo. Escolha o idioma do relatório separadamente. Alterar o idioma ou qualquer configuração de seleção requer outra visualização prévia antes da criação.

1. Insira a finalidade da divulgação e selecione datas, IDs de remetentes e critérios de texto literal.
2. Escolha entre manter as identidades, revelar apenas os participantes listados ou pseudonimizar todos. Em qualquer um dos modos de pseudonimização, os IDs/títulos das conversas e os IDs das mensagens também são substituídos. Os pseudônimos permanecem estáveis dentro de uma divulgação e mudam entre divulgações preparadas independentemente.
3. Mantenha o texto da mensagem, omita-o totalmente ou adicione nomes/frases literais para mascarar. Nos modos privados, a ferramenta também mascara nomes de remetentes ocultos conhecidos e nomes de usuário alternativos, IDs de remetente com token completo, nomes de bate-papos diretos, links, endereços de e-mail e sequências semelhantes a números de telefone. A correspondência de nomes conhecidos lida com a conversão de maiúsculas e minúsculas do Unicode, incluindo `Straße`/`STRASSE`. Títulos genéricos de grupos/canais não são removidos automaticamente do texto da mensagem. Se o limite de mascaramento de identidades conhecidas for excedido, restrinja a exportação de origem ou omita o texto; a ferramenta se recusa a ignorar silenciosamente nomes posteriores. Essas são regras de melhor esforço, não de anonimização geral.
4. Deixe os arquivos de fora, a menos que o destinatário precise deles. Os originais incluídos mantêm seus pixels, áudio, texto e metadados. Eles **não** são anonimizados pela ferramenta.
5. Visualize as contagens, os avisos e exemplos de mensagens transformadas e, em seguida, confirme explicitamente a criação. As amostras são limitadas a 12 mensagens e 2.000 caracteres de texto cada. Trata-se de uma amostra, não de uma revisão completa do resultado. Alterar as configurações requer uma nova visualização. Uma visualização expira após 15 minutos e está vinculada àquela sessão do administrador e à imagem original exata ZIP; ela não pode ser reutilizada após a criação. Uma nova visualização invalida a anterior para o mesmo trabalho e sessão.
6. Confira o resultado completo `index.html` e `messages.jsonl` localmente antes de entregá-lo. Se ele revelar informações desnecessárias, crie uma nova divulgação com exclusões mais rigorosas. Não edite a imagem assinada ZIP no local.

### Mensagens excluídas pela seleção

**Pré-visualização.** Uma divulgação não parece completa quando não está. Dentro de cada chat que contenha pelo menos uma mensagem divulgada, as mensagens que não foram incluídas na seleção aparecem como marcadores, `[withheld by selection — rule: sender]` (ou `text`, `period`). Escolha **“Mensagens excluídas pela seleção**”: um marcador para cada sequência de mensagens ocultadas consecutivas (padrão) ou um para cada mensagem. Os marcadores contêm apenas a regra e uma contagem, nunca texto, remetente, data ou arquivos. Bate-papos sem nada divulgado são totalmente excluídos, de modo que o pacote não revela que eles existem.

Respostas divulgadas indicam o que respondem: uma mensagem incluída nesta cópia, uma mensagem excluída pela seleção ou uma mensagem que não consta na exportação de origem (excluída antes da exportação ou nunca exportada; a exportação não permite distinguir qual das duas). Uma mensagem omitida à qual uma resposta divulgada se refere sempre recebe seu próprio marcador, de modo que a resposta aponta para um registro que explica por que ela está vazia. Esses três estados são distintos das exclusões e lacunas na coleta, que pertencem à exportação de origem.

Em `messages.jsonl` (formato `tgwitness-account-disclosure-v2`) cada mensagem possui `state`: `disclosed`, ou `withheld` com `rules` e `count`. Uma resposta divulgada possui `reply_to` com o alvo `id` e `state` (`disclosed`, `withheld`, `not_in_source`). O manifesto contabiliza mensagens, bate-papos, mídias e `withheld` mensagens. `verify.py` Rejeita um marcador que contenha conteúdo e uma resposta que aponte para um registro ausente do pacote; os pacotes da versão 1 são verificados como antes.

O formato minimizado omite perfis de conta estruturados, contatos, avatares, sessões, stories, objetos brutos do Telegram, cabeçalhos de encaminhamento, citações de respostas, cartões de contato e metadados de localização. Ele exclui os arquivos JSONL originais, configurações de filtro privadas, chave de pseudônimo e mapa de identidade. Textos selecionados, identidades explicitamente retidas e arquivos incluídos ainda podem conter os mesmos nomes, IDs ou frases usados nesses filtros; eles precisam de revisão separada. A política privada e a chave de pseudônimo são mantidas criptografadas no cofre local da tarefa; a exclusão da tarefa limpa seus registros de divulgação privada associados. A política pública registra o número de filtros, em vez dos valores dos filtros. A finalidade declarada é pública no manifesto e no HTML: critérios privados explícitos e, em modos pseudonimizados, identidades ocultas conhecidas também são mascaradas ali, inclusive quando o texto da mensagem é omitido. Mantenha a finalidade livre de detalhes pessoais desnecessários; o contexto de identificação desconhecido pode permanecer.

Seu manifesto vincula os arquivos derivados, a política pública e o hash da imagem original ZIP. A verificação permite confirmar a integridade e, se a fonte for fornecida localmente, a correspondência do link de origem:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

A vinculação à fonte não prova, por si só, que a transformação selecionou todos os itens necessários ou removeu todos os detalhes identificadores. O texto-fonte original não está incorporado como prova. É necessária uma nova análise para se chegar a essa conclusão.

## Compartilhamento e captura hospedada

Select the messages and files the recipient needs, review the complete sharing copy, and retain the source separately. Record the delivered ZIP's hash so the recipient can identify and verify that exact copy. Pseudonymization replaces the selected identifiers; included text and original files remain part of the review.

GitHub Actions supports full-account and selected-chat exports through Takeout or the regular API, plus a one-chat event journal. The [hosted capture guide](https://phishdestroy.github.io/TgWitness/docs/capture/) explains settings verification and the 120-minute limit. To verify a sharing copy derived from hosted capture, check its source hash against the original archive and verify that archive's attestation with the [mode-specific checks](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#verification-scope).

[Formato das evidências](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/) · [Relatórios de casos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-reports/)
