# Vitrine pública

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/showcase/

Publique mensagens salvas de canais públicos selecionados e instantâneos assinados por meio de links com validade limitada e revogáveis.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**Acessar → Vitrine pública** cria uma página separada, somente para leitura, utilizando o sistema de tokens de acesso existente. Ela lê as observações salvas na instalação. Ela não inicia um coletor, não faz login no Telegram nem adquire um canal para um visitante.

## Publicar uma página

1. Salve um perfil de origem para cada canal público que você deseja exibir. Um canal deve ter um nome de usuário público em seu perfil salvo mais recente; grupos e chats privados não são elegíveis.
2. Abra **Acesso → Vitrine pública** (ou `/showcase-manage.html`) como administrador.
3. Selecione canais em até 16 espaços de trabalho, insira o título da página pública e escolha um prazo de validade do link de 1, 7 ou 30 dias. Os rótulos internos dos espaços de trabalho não são publicados. É possível incluir até 64 canais.
4. Revise o texto dos canais selecionados para publicação e, em seguida, clique em **“Visualizar registros selecionados**”. A visualização utiliza a mesma projeção do lado do servidor que a página do visitante.
5. Clique em **“Criar link de vitrine**”. Copie o link enquanto ele estiver visível. Abra-o em um navegador separado para revisar a página do destinatário antes de distribuí-la.

O link contém um token de acesso em seu fragmento de URL. A página remove o fragmento antes de fazer solicitações à API e o troca por uma sessão do navegador. Qualquer pessoa que possua o link pode abrir o material selecionado até o vencimento ou a revogação. Novos links permitem 100 sessões simultâneas, cada uma com duração máxima de uma hora. Os controles de acesso existentes também podem impor restrições de endereço e limites de login por meio da API de concessão. O acesso normal de revisor é um modo diferente e ainda inclui as mensagens e arquivos originais permitidos.

## O que os visitantes veem

| Visível | Mantido em sigilo |
| --- | --- |
| Títulos selecionados de canais públicos, nomes de usuário e datas de observação de perfis | Identidades de contas, rótulos internos do espaço de trabalho e fontes não selecionadas |
| Texto capturado e cada edição salva | IDs estruturados de remetentes, nomes, nomes de usuário, números de telefone e valores de perfil |
| Observações sobre exclusões com o texto salvo anteriormente, se disponível | Anexos, avatares, miniaturas, nomes de arquivos e conteúdos originais |
| Marcadores indicando que um autor/perfil ou anexo foi registrado | Metadados de encaminhamento e resposta, rotas de rede, endereços IP e credenciais |
| Contagem de eventos em canais selecionados, alternâncias de coleção atuais, intervalo de heartbeat e de checkpoint | Controles de coleta e APIs comuns para exportação de evidências |
| Assinatura digital, ponto de verificação do diário e prova de consistência | Chaves de assinatura e sessões do Telegram |

**O texto das mensagens públicas não é anonimizado automaticamente.** Um nome, menção, número de telefone ou link incluído na mensagem permanece como parte desse texto. `Redacted`Isso se aplica aos campos estruturados de autor/perfil. Revise o conteúdo efetivamente selecionado antes de publicá-lo, incluindo edições e exclusões preservadas.

A elegibilidade reflete o **perfil de origem salvo mais recente**, e não uma consulta em tempo real no Telegram. Se um perfil subsequente não tiver mais um nome de usuário de canal público, novas solicitações excluem o canal. Atualize os perfis de origem quando a visibilidade pública for alterada. Os leitores podem já ter material salvo que receberam anteriormente.

Os registros originais assinados permanecem inalterados. A projeção exibida é assinada separadamente e contém hashes que fazem referência aos registros originais. A assinatura da projeção autentica a declaração exibida; não se trata da assinatura do evento original sobre bytes ocultados.

## Verifique as assinaturas e a continuidade

Expanda **“Fingerprint & signed checkpoint”** e baixe um instantâneo. Após uma atualização da página, o download inclui o instantâneo anterior do navegador e uma prova de consistência de Merkle entre os limites de seus registros. A atualização automática ocorre uma vez por minuto enquanto a página estiver visível e exibindo sua primeira página de observações.

Com o TgWitness instalado, verifique o arquivo baixado offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

A impressão digital deve provir de uma referência confiável separada. Para comparar com um instantâneo que você mesmo reteve, use `--previous earlier.json`; isso substitui o instantâneo anterior contido no download. A prova atual deve começar nesse limite mantido. Clientes autenticados podem solicitar essa prova usando `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Um diário mais curto retorna um código de erro HTTP 409 em vez de redefinir silenciosamente o limite.

O ponto de verificação assinado é gravado no **diário completo do coletor**, incluindo sua contagem de registros e o hash opaco do cabeçalho. As contagens de mensagens exibidas se aplicam apenas aos canais públicos selecionados. A página nunca lista o conteúdo dos outros diários. Essas são contagens de eventos, não contagens de mensagens únicas. As configurações descrevem a configuração atual, não todos os intervalos de gravação anteriores.

A verificação de assinatura e consistência pode detectar alterações em relação a um limite mantido. Ela não recontabiliza de forma independente os contadores assinados, não certifica a origem do Telegram, não demonstra captura ininterrupta nem substitui uma testemunha independente. Para essa revisão, utilize o [verificador de evidências](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [a testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/) e [o registro em escala testada](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/). Instalações sintéticas são visivelmente identificadas como sintéticas.

## Revogar ou hospedar a página

Use **a opção “Revogar”** no gerenciador de vitrines ou na seção **“Acesso”** existente para encerrar o link e encerrar todas as suas sessões. O visitante limpa os registros exibidos quando uma solicitação detecta que o acesso foi encerrado. A validade e as permissões são verificadas a cada solicitação. As autorizações de vitrine não podem ser convertidas em acesso comum ao painel no local; crie uma nova autorização para alterar os modos.

Hospede a página por meio do endereço HTTPS existente na instalação. A publicação de um link não abre uma nova porta, não cria um túnel nem altera o DNS. O HTML e a API permanecem na instalação do usuário. Um visitante da vitrine não pode usar as APIs comuns de mensagem, perfil, mídia, exportação ou gerenciamento com esse acesso.
