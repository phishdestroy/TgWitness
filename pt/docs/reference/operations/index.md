# Fluxos de trabalho e operações

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/

Operação diária do painel: modos, categorias de monitoramento, parâmetros, notificações, exportações, backup e capacidade.

Para sua primeira conexão, utilize [contas e formatos de sessão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/). Para obter uma explicação sobre versões salvas, políticas de eventos e lacunas, consulte [como funciona a coleta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/). Este guia aborda a operação diária e a recuperação.

## Fluxo de trabalho do operador

Diagrama de fluxo · Escolha o armazenamento e a proteção da chave → Abra o painel com seu token; Abra o painel com seu token → Selecione um espaço de trabalho; Selecione um espaço de trabalho → Configurar rota direta ou via proxy; Configurar rota direta ou via proxy → Insira o número de telefone ou selecione arquivos / QR; Insira o número de telefone ou selecione arquivos / QR → Verifique a identidade da conta e selecione os grupos acessíveis; Verifique a identidade da conta e selecione os grupos acessíveis → Salve as políticas de eventos e anexos e, em seguida, inicie a observação; Salve as políticas de eventos e anexos e, em seguida, inicie a observação → Monitorar erros, acesso, filas e disco; Monitorar erros, acesso, filas e disco → Manter pontos de verificação independentes; Manter pontos de verificação independentes → Exportar e verificar o material · Escolha oarmazenamento e aproteção da chave · Abra o painel com seutoken · Selecione um espaço detrabalho · Configurar rota diretaou via proxy · Insira o número detelefone ou selecionearquivos / QR · Verifique a identidadeda conta e selecioneos grupos acessíveis · Salve as políticas deeventos e anexos e, emseguida, inicie aobservação · Monitorar erros,acesso, filas e disco · Manter pontos deverificaçãoindependentes · Exportar e verificar omaterial

**Diagrama em formato de texto**

1. Escolha o armazenamento e a proteção da chave → Abra o painel com seu token
2. Abra o painel com seu token → Selecione um espaço de trabalho
3. Selecione um espaço de trabalho → Configurar rota direta ou via proxy
4. Configurar rota direta ou via proxy → Insira o número de telefone ou selecione arquivos / QR
5. Insira o número de telefone ou selecione arquivos / QR → Verifique a identidade da conta e selecione os grupos acessíveis
6. Verifique a identidade da conta e selecione os grupos acessíveis → Salve as políticas de eventos e anexos e, em seguida, inicie a observação
7. Salve as políticas de eventos e anexos e, em seguida, inicie a observação → Monitorar erros, acesso, filas e disco
8. Monitorar erros, acesso, filas e disco → Manter pontos de verificação independentes
9. Manter pontos de verificação independentes → Exportar e verificar o material

Autorização, conectividade de transporte, acesso a um grupo e integridade da entrega são propriedades distintas. Um status de conexão verde não implica que todos os eventos tenham sido capturados.

## Compartilhe o trabalho sem compartilhar a chave principal

**Acesso** Aberto para fornecer a um revisor ou analista seu próprio token. Escolha as contas e os chats que eles podem acessar e, em seguida, permita a visualização, a exportação ou ações operacionais. Um operador que inicia ou interrompe a coleta precisa de acesso a todo o espaço de trabalho; um revisor pode ter acesso restrito a um único chat. Limites de sessão, validade e regras de IP são independentes da autorização da conta do Telegram. Consulte [acesso e permissões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/).

Utilize **“Sessões abertas”** para encerrar uma conexão ou revogar o acesso a fim de encerrar todas as suas sessões. O console do administrador reúne as atividades dos processos atuais em todas as áreas de trabalho. O encerramento da sessão mantém a coleta em execução.

## Modos de execução

| Modo | Ação | Comportamento |
| --- | --- | --- |
| Demonstração | scripts\Demo.cmd ou `--demo` | Dados sintéticos; conexões com contas reais desativadas |
| Observação | Iniciar observação | Registre as atualizações entregues para fontes selecionadas |
| Resumo histórico | Fontes → instantâneo do histórico | Até 500 mensagens atuais; sem reconstrução de todas as alterações anteriores |
| Pausa | Observação sobre a pausa | Interromper a coleta, mantendo os dados e as tarefas em fila |
| Revisão/transferência | Exportações | ZIP, JSONL/CSV/HTML, ponto de verificação, recibo de processamento e solicitação de carimbo de data/hora |
| Várias contas | Áreas de trabalho ou o botão superior **+** | Qualquer número de espaços de trabalho separados em um único processo |

O acesso à demonstração local é aberto automaticamente, sem a necessidade de inserção manual de token. Ele utiliza um recurso válido durante toda a duração do processo, restrito exclusivamente ao acesso direto por loopback a uma demonstração sintética isolada; o token do painel principal não é divulgado. Espaços de trabalho reais e o acesso à demonstração remota ou via proxy mantêm a autenticação por token. O acesso à demonstração não concede nenhuma autorização no Telegram.

## Categorias de monitoramento

![Configurações de monitoramento por conta com dados de origem sintéticos](https://phishdestroy.github.io/TgWitness/assets/sources.png)

Em **Fontes → Configurações de captura → Escolha quais alterações preservar**, selecione novas mensagens, edições, notificações de exclusão, atualizações de reações e eventos de participação de forma independente. A configuração padrão mantém todas as categorias. A opção **“Mensagens, edições e exclusões”** mantém o contexto original ao desativar atualizações separadas de reações e de membros. **“Todas as atividades visíveis”** restaura todas as cinco. As predefinições alteram o formato; pressione **“Salvar configurações de monitoramento”** para aplicar.

A política salva se aplica a todas as fontes selecionadas naquele espaço de trabalho. Outros espaços de trabalho mantêm suas próprias configurações. Cada alteração efetiva registra valores assinados de “antes” e “depois” ; a política atual também é incluída nos recibos de processo e nos registros de início de observação . Desativar uma categoria não exclui observações anteriores. Reativá-la não recupera as alterações perdidas. Nesta versão, não há substituição de categoria por grupo.

Mantenha as novas mensagens ativadas quando o conteúdo anterior for relevante: um aviso de exclusão não pode recuperar texto que nunca foi capturado. Registros operacionais/de cobertura e outros eventos de serviço em grupo são sempre retidos. Instantâneos explícitos do histórico são separados da seleção de categorias em tempo real e podem incluir mensagens de serviço. Essas configurações não ocultam metadados de reações/membros incorporados a um objeto do Telegram que, de outra forma, teria sido capturado.

Um instantâneo do histórico pode colocar anexos na fila enquanto estiver em pausa. Inicie a observação para processá-los. Estar na fila não significa que foram baixados. Um arquivo original indisponível não é substituído por uma versão editada mais recente; os resultados são registrados separadamente.

**O botão “Lock”** limpa o acesso do navegador e os campos secretos, mas mantém a coleta em execução. Fechar uma aba também mantém o processo em execução. Interromper o processo ou serviço em Python interrompe a coleta, independentemente do estado do navegador.

A exclusão de um espaço de trabalho adicional interrompe seu coletor e remove seus dados locais. Se um arquivo bloqueado ou um erro no sistema de arquivos interromper a remoção, o painel relatará a falha e manterá o espaço de trabalho listado como indisponível (`DeletionPending`). Feche os programas que estejam mantendo seus arquivos e tente novamente **a exclusão**. Reiniciar o TgWitness mantém esse espaço de trabalho desativado e não recria seu diário ou suas chaves parcialmente removidos. Uma exclusão bem-sucedida é registrada somente após a remoção do diretório; cópias exportadas ou armazenadas em backup separadamente permanecem sujeitas à sua própria política de retenção.

## Notificações

Abra **“Fontes” → “Notificações” → “Alertas” e um resumo diário**. O TgWitness utiliza o Apprise para enviar alertas para o Matrix, Telegram, Discord, Slack, ntfy, e-mail e outros serviços compatíveis. É possível adicionar vários destinos a um único espaço de trabalho.

1. Insira uma URL de destino do Apprise por linha. Utilize o [catálogo de serviços e os formatos de URL](https://appriseit.com/services/) correspondentes ao seu serviço.
2. Ative a opção **“Enviar notificações**” e, em seguida, selecione alertas de problemas, alterações nos chats monitorados e um resumo diário. A hora do resumo utiliza a hora do servidor.
3. Ative a opção **“Incluir trechos curtos”** se desejar que o texto salvo de mensagens excluídas e editadas apareça nos alertas.
4. Clique em **“Salvar notificações**” e, em seguida, em **“Enviar teste”** para verificar a entrega.

Para seu próprio receptor, utilize [o webhook JSON](https://appriseit.com/services/json/) do Apprise. Por exemplo, `jsons://notify.example.org/tgwitness` envia JSON por HTTPS para esse ponto de extremidade. Este é um exemplo fictício; substitua-o pelo seu próprio destino.

Os destinos e as configurações pertencem ao espaço de trabalho selecionado. As notificações de alteração abrangem suas fontes monitoradas, incluindo bate-papos recém-adicionados. O sino na barra superior também lista problemas recentes e alterações nos bate-papos.

Na demonstração, os controles de notificação estão visíveis, mas o envio está desativado. Configure a entrega em um espaço de trabalho real. As notificações utilizam a rota Direct, SOCKS5 ou HTTP desse espaço de trabalho; o MTProxy não pode transmiti-las. Destinos que não sejam HTTP, como o SMTP, exigem uma rota direta.

## Layout do painel

![Espaço de trabalho de conexão utilizando dados sintéticos](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**O diário** apresenta observações, pesquisas e filtros. Uma edição abre as versões capturadas; uma exclusão abre o conteúdo anterior, se disponível. Atribuições desconhecidas permanecem explícitas. As contagens estão disponíveis na seção **“Visão geral”**; os detalhes da aquisição permanecem no guia local.

**A seção “Fontes”** contém o escopo de observação (conversas selecionadas, uma pasta do Telegram ou toda a conta), conversas acessíveis de todos os tipos, fontes selecionadas com estrelas de prioridade, configurações de anexos e reavaliação, além de instantâneos do histórico. As fontes privadas são selecionadas por diálogo/ID sem um link público. O status de acesso descreve a verificação mais recente, e não permissões permanentes.

**A seção “Bate-papos → Pessoas”** lista todos aqueles cujas mensagens foram salvas; com os perfis das pessoas ativados para o bate-papo, um clique abre o perfil dessa pessoa com links para os registros do diário.

**O Witness** cria tokens de testemunho somente leitura, mostra quando cada testemunho foi verificado pela última vez e fornece os comandos e opções para executar um ([testemunho independente](https://phishdestroy.github.io/TgWitness/pt/docs/reference/witness/)).

**A seção “Parâmetros”** contém todos os limites e ritmos do ambiente de trabalho que não constam em outra página: quantos diálogos são lidos, com que frequência a lista de bate-papos é relida, intervalos de heartbeat e checkpoint, o buffer de inicialização, como as novas verificações distribuem suas solicitações (primeiro atraso, bate-papos por passagem, pausa entre bate-papos, mensagens recuperadas e solicitadas novamente), reserva de disco, tempos de espera e novas tentativas de downloads, o que os perfis de usuários procuram (incluindo suas próprias expressões regulares), tamanho e frequência das notificações, limites de instantâneos, arquivos ZIP e downloads no navegador, além de tempos de espera e novas tentativas do cliente do Telegram. Cada campo exibe seu intervalo e valor padrão; os campos alterados são marcados e podem ser restaurados um por um ou todos de uma vez. Cada alteração é registrada como “`parameters.changed`” com os valores anteriores e posteriores, e os registros de início de observação indicam os valores em vigor. Os valores passam a vigorar a partir de seu próximo uso; os tempos limite e novas tentativas do cliente, a partir da próxima conexão. Intervalos de verificação, tipos e tamanhos de anexos, evidências e intervalos de cópia externa permanecem em suas respectivas páginas e podem assumir qualquer valor dentro de seu intervalo, não apenas as predefinições.

O ícone de sino na barra superior lista problemas e alterações recentes nos chats monitorados; as mensagens não lidas são contabilizadas até serem marcadas como lidas. As alterações são agrupadas por chat e por hora (“12 excluídas, 1 editada, 0 não encontradas”), e problemas como o logout ou disco cheio permanecem na lista, independentemente do volume de atividade nos chats.

**A criação da conta** começa no campo do número de telefone. **Continuar** leva diretamente à inserção do código, solicitando credenciais de API somente quando estas estiverem ausentes. QR e importação de arquivo são abas alternativas. As credenciais de API salvas são reutilizadas apenas dentro de seu próprio espaço de trabalho. A tela de entrada não possui barra lateral, estatísticas ou seções de configuração. O ícone de **Configurações** abre os controles de API, proxy, armazenamento e contas adicionais. Novas instalações começam aqui; contas conectadas sem fontes selecionadas iniciam em **“Escolher chats**”. Alterar a rota requer observação em pausa e cancela o login inacabado. Um registro existente não pode ser vinculado silenciosamente a uma conta diferente do Telegram.

**A exportação** verifica a integridade do diário e gera arquivos portáteis. O ID da área de trabalho pode ser passado para a CLI de download. Cada exportação atribui um prefixo completo ao diário; eventos posteriores são incluídos em uma exportação subsequente. Os filtros de pesquisa não alteram o escopo do pacote. Informações detalhadas sobre assinatura e cobertura encontram-se na seção **“Verificação e limitações**”.

O painel exibe o status do coletor, mídias em fila/com falha, as mídias pendentes mais antigas, espaço livre em disco, pausas nas solicitações e fontes cujo acesso não está confirmado na seção **“Integridade do coletor**”. Esses detalhes aparecem inicialmente recolhidos e ocultos na seção “Conta”. Um cartão de configuração mostra a próxima etapa: conectar uma conta, escolher fontes ou iniciar a observação. A lista de contas é um instantâneo no momento do carregamento; o espaço de trabalho selecionado é atualizado periodicamente. Este não é um monitor de SLA multiprocessos.

A interface do usuário utiliza recursos locais e renderização de texto para o conteúdo de origem. Os layouts para desktop e para telas estreitas baseados no Chromium foram testados. Esta não é uma certificação completa de acessibilidade; a avaliação de usabilidade por leitores de tela e por usuários humanos continua sendo um trabalho à parte.

## Ambientes de implantação

| Ambiente | Instalação | Status da verificação |
| --- | --- | --- |
| PC/servidor Windows | Python 3.11+, scripts\Setup.cmd/Start.cmd, diretório de dados privado | Testado localmente no Windows/Python 3.12 |
| Servidor Linux/VPS | Ambiente virtual Python (venv), usuário de serviço dedicado, HTTPS/SSH | Exemplos de código, CI e systemd são fornecidos; não executados neste servidor |
| macOS | Venv do Python, processo em primeiro plano ou agente de usuário | Exemplo do `launchd` fornecido; é necessária uma verificação separada da instalação |
| Docker/Compose | Volume persistente, um trabalhador | São fornecidas a definição e a verificação de tempo de execução da CI; o Docker não está disponível localmente |
| Navegador do celular | Conecte-se ao painel protegido em um servidor em funcionamento | Layout estreito baseado no Chromium testado; o coletor não funciona no iOS/Android |

Portabilidade significa que não há exigência de serviço em nuvem ou compilação de front-end. Cada alvo ainda precisa de dependências compatíveis de Python/criptografia, disco local e acesso à rede. Consulte [o arquivo DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/deployment/) e [os modelos de serviço](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Os espaços de trabalho compartilham CPU, memória e um ciclo de eventos. Para isolamento de processos, utilize instâncias, portas, diretórios de dados e autorizações de conta distintas. Não há um painel unificado entre instâncias separadas. Nunca direcione vários workers para um único banco de dados.

## Verificações iniciais e exportações

Execute o comando `python start.py --check` antes de iniciar um ambiente preparado. Adicione o `--json` para verificações legíveis por máquina ou forneça os parâmetros `--data-dir`, `--host` e `--port` pretendidos. O comando verifica os pré-requisitos sem a necessidade de fazer login no Telegram ou criar um diário. Ele não verifica um diário nem comprova a prontidão para a captura; a verificação do diário é executada durante a inicialização do aplicativo. Uma porta ocupada pode ser simplesmente uma instância já existente.

Os navegadores compatíveis com a API de Acesso ao Sistema de Arquivos salvam as exportações por meio de um fluxo gravável. Outros navegadores armazenam em buffer no máximo 128 MiB. Utilize a CLI de streaming para exportações maiores ou para navegadores sem streaming de arquivos:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Adicione `--profile ID` em “Exports” para um espaço de trabalho secundário. Utilize `--url https://server` para acesso remoto. O HTTP simples é aceito apenas para destinos de loopback. O token é lido a partir de um arquivo e enviado em um cabeçalho, não sendo exibido nem inserido em uma URL. Redirecionamentos são recusados. Destinos existentes não são sobrescritos. As transferências com falha removem seu arquivo parcial temporário. O SHA-256 relatado é uma soma de verificação da transferência; verifique o arquivo ZIP assinado separadamente com uma impressão digital/ponto de verificação confiável.

## Backup, restauração e interrupções

1. Pause a observação e interrompa o processo de forma limpa.
2. Copie todo o diretório de dados: bancos de dados, WAL/SHM, se houver, mídia, `credentials.enc`, `signing.enc`, `network.enc`, chaves/metadados do cofre, token, pontos de verificação e todos os diretórios `profiles/`.
3. Para o modo de chave externa, preserve separadamente a chave mestra e mantenha cada `vault.external.json`. A geração de uma nova chave não permite recuperar os segredos antigos.
4. Restaure enquanto o destino estiver parado; configure a chave original, restrinja o acesso e verifique a integridade antes de retomar.
5. Registre o tempo de inatividade e os resultados da verificação. Um instantâneo do histórico não pode comprovar que não ocorreram exclusões durante a interrupção.

Os arquivos ZIP de evidências excluem sessões e chaves privadas e não constituem backups completos do serviço. Quatro elementos são protegidos de maneira diferente:

| O que | Proteção |
| --- | --- |
| Arquivos exportados sem senha (padrão) | Não é criptografado. É assinado, de modo que as alterações são detectáveis, mas qualquer pessoa que possua o arquivo pode lê-lo |
| Arquivos exportados com senha | Caso defina uma senha, a exportação finalizada será mantida inalterada em um arquivo ZIP com criptografia AES-256 do WinZip, que pode ser aberto pelo 7-Zip e pelo WinRAR; a senha não é armazenada ([tratamento de provas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)) |
| O banco de dados do registro e os anexos salvos no disco | Não é criptografado pelo TgWitness; utilize um disco ou volume criptografado |
| Sessões do Telegram e chaves de assinatura | Criptografado no diretório de dados (`credentials.enc`, `signing.enc`, `network.enc`) |

Um backup completo corresponde ao diretório de dados suspenso descrito acima, e não a uma exportação. Utilize armazenamento protegido e um mecanismo de transferência controlado para ambos. As exportações temporárias do servidor ficam armazenadas no diretório `temporary-exports/` de cada espaço de trabalho; as respostas concluídas são eliminadas, e os arquivos de exportação interrompidos são removidos na próxima inicialização, enquanto o bloqueio da instância desse espaço de trabalho estiver ativo.

A restauração da conexão não garante a recuperação de alterações intermediárias. Tarefas de mídia persistentes e a posição de atualização do Telegram sobrevivem à reinicialização; consulte [o formato de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#durable-collection-and-process-receipts-02).

## Capacidade e retenção

Limites padrão, todos alteráveis em **“Parâmetros**”: as primeiras 1.000 conversas, 500 mensagens por instantâneo, 4 GiB de conteúdo ZIP assinado não compactado (arquivos maiores requerem `verify.py --max-gib N`) e um fallback do navegador de 128 MiB. Anexos ocupam de 1 a 2.000 MiB por tipo em **Fontes → Anexos**. A CLI de download tem como padrão 5 GiB transferidos. O espaço em disco disponível pode ser um limite inferior. Reserve espaço para registros, mídia, WAL, exportações temporárias e backups. As exportações utilizam o volume de dados em vez do limite de 512 MiB do Compose (`/tmp`).

Meça eventos por segundo, tempo de espera na fila, bytes de mídia e latência do disco, em vez de contar apenas os grupos. Benchmarks locais sintéticos não garantem a entrega no Telegram. Não há exclusão automática de retenção. A remoção da parte final de um registro invalida sua relação com os pontos de verificação retidos.

Já existem verificações prioritárias: as fontes marcadas com estrela são verificadas a cada 15 minutos por padrão, as demais a cada 6 horas (consulte [os níveis de verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/collection/#recheck-tiers)). Existem exportações protegidas por senha, conforme descrito acima. Aceitação em tempo real do Telegram/proxy, reprodução duradoura, registro de administração e sondagem de reações, workers isolados, criptografia do registro local e da mídia pelo próprio TgWitness e revisão independente continuam sendo trabalhos separados. O acesso restrito está documentado em [“Acesso e permissões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/)”. Consulte [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) e [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/pt/docs/reference/verification/).
