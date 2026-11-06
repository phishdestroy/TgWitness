# Acesso e permissões

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/

Defina o escopo de acesso a contas e conversas, escolha permissões, limite sessões e endereços IP e revogue o acesso.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentação](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

Conceda a um revisor acesso a um chat, a um analista permissão para exportar um caso ou a um operador o controle de contas selecionadas. Cada pessoa recebe seu próprio token. O token do painel principal permanece com o administrador.

[Configuração da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/) · [Rotas de conexão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) · [Modelo de segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/)

## Dois escopos, duas funções distintas

**O escopo da coleta** determina o que uma conta registra: chats selecionados, uma pasta do Telegram ou a conta inteira. **O escopo de acesso** determina quais dessas contas e chats registrados outra pessoa pode visualizar e utilizar. Conceder acesso não significa ingressar em um chat do Telegram, iniciar a coleta nem conceder permissões à conta do Telegram.

Um acesso pode abrir espaços de trabalho selecionados, chats selecionados dentro deles, todos os espaços de trabalho ou todas as contas de um [grupo de contas](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/#bulk-import-and-account-groups). **Todos os espaços de trabalho, incluindo aqueles adicionados posteriormente**, também abrangem contas futuras. Um acesso a grupo também abrange contas adicionadas a esse grupo posteriormente. Selecione espaços de trabalho explicitamente quando um caso deva se limitar a eles.

## Conceda acesso a alguém

1. Faça login como administrador principal e acesse a seção **“Acesso**”.
2. Em **“Conceder acesso a alguém**”, insira um nome que o senhor reconheça no registro.
3. Selecione os espaços de trabalho e, quando necessário, os chats individuais.
4. Selecione o que essa pessoa pode fazer. A opção **“Visualizar”** está sempre incluída.
5. Defina o prazo de validade, os limites de login/sessão e os endereços permitidos conforme necessário.
6. Clique em **“Criar acesso**”. Copie o token agora: ele é exibido apenas uma vez.
7. Envie o endereço do painel e o token de forma privada. O destinatário insere esse token na página normal de login; ele não precisa do seu token principal do painel nem de uma sessão do Telegram.

Abra o painel com o token emitido em uma sessão separada do navegador e verifique os chats visíveis e as ações permitidas antes de entregá-lo.

## Selecione as permissões

Para uma demonstração pública apenas em texto, use **a “Vitrine pública”** em vez do acesso comum de revisor. Ela mostra canais públicos explicitamente selecionados, edições e exclusões retidas e estatísticas assinadas, com os campos de autor ocultados e os arquivos fechados no limite da API. [Crie e verifique uma vitrine](https://phishdestroy.github.io/TgWitness/pt/docs/reference/showcase/).

| Permissão | O que ela permite |
| --- | --- |
| `view` | Leia conversas autorizadas, mensagens capturadas, perfis, arquivos e registros filtrados do diário. Sempre incluídos. |
| `export` | É permitido exportar o histórico de bate-papos e os dossiês. A exportação de evidências de todo o espaço de trabalho requer acesso a todo o espaço de trabalho. |
| `sources` | Gerencie fontes, instantâneos e captura de perfis. O acesso limitado a conversas pode atuar apenas nas conversas permitidas; a descoberta de fontes em toda a conta e as configurações de escopo permanecem desativadas. |
| `collect` | Inicie ou interrompa um coletor. Requer acesso a todo o espaço de trabalho, pois a coleta afeta a conta. |
| `interact` | Realize interações compatíveis com o Telegram dentro do escopo de acesso. O acesso limitado ao chat não permite a visualização de links em toda a conta. |
| `settings` | Altere as configurações de coleta, registros de data e hora, notificações, cópias externas e parâmetros. Requer acesso a todo o espaço de trabalho. |
| `account` | Faça login ou logout do Telegram e gerencie as rotas de conexão. Requer acesso a todo o espaço de trabalho. |
| `board.read` | Leia as anotações do Case Board apenas dentro do espaço de trabalho e dos chats permitidos. |
| `board.write` | Adicione marcadores, destaques, trechos, comentários e status de abertura/revisão. Também requer o ``board.read``. |
| `board.manage` | Gerencie coleções, status finais da equipe e cartões de outros participantes. Também requer permissão de leitura/gravação no quadro. |

As permissões e o escopo são verificados em conjunto. Marcar uma permissão não abre outros chats nem desbloqueia uma operação em todo o espaço de trabalho para um acesso limitado a um chat. Para uma exportação paralela, o acesso deve abranger o chat exportado em todas as contas selecionadas. Um acesso concedido não pode criar novos acessos, gerenciar as sessões de outras pessoas nem abrir o console de administrador.

### Três configurações úteis

| Pessoa | Escopo | Permissões |
| --- | --- | --- |
| Revisor | Conversas registradas de um caso | `view` |
| Analista preparando uma transferência de funções | As conversas a serem investigadas e exportadas | `view`, `export`; adicione `interact` apenas caso seja necessário agir por meio do Telegram |
| Operador de coleta | Espaços de trabalho selecionados na íntegra | `view`, `sources`, `collect`; adicione `settings` ou `account` somente quando necessário |

As predefinições iniciais do formulário do Access também incluem o Painel de Casos: o revisor pode ler, o analista pode ler e escrever, e o operador pode gerenciá-lo. As predefinições permanecem editáveis, e as permissões existentes não são automaticamente ampliadas. Consulte [o Painel de Casos](https://phishdestroy.github.io/TgWitness/pt/docs/reference/case-board/) para conhecer os escopos de bate-papo herdados e a privacidade da exportação.

## Limites e sessões

| Contexto | Como funciona |
| --- | --- |
| Sessões paralelas | Limite o número de sessões simultâneas a 1–100. Ao atingir o limite, recuse o próximo login ou encerre a sessão mais antiga. |
| É permitido o acesso com login | Limite o número de utilizações bem-sucedidas do token para iniciar sessões. As sessões existentes não são encerradas apenas porque o último login permitido foi utilizado. |
| Válido até | Prazo de validade absoluto para o acesso. Acessos expirados não podem efetuar login nem continuar a fazer solicitações. |
| Minutos sem atividade | Tempo limite de inatividade da sessão, de 5 minutos a 30 dias. Solicitações bem-sucedidas prolongam esse tempo; um painel aberto pode manter-se ativo por meio de polling. |
| Endereços permitidos | Aceite endereços IP específicos ou sub-redes CIDR. Deixe em branco para permitir qualquer endereço, a menos que a vinculação ao primeiro login esteja ativada. |
| Vincular ao primeiro login | O primeiro login bem-sucedido define o endereço permitido para esse acesso. |

O IP é o endereço do cliente visualizado pelo aplicativo. Caso esteja atrás de um proxy reverso ou túnel, verifique o endereço exibido em **“Sessões abertas”** antes de basear-se nas regras de IP: caso contrário, pode parecer que vários usuários compartilham o endereço do proxy.

## Alterar ou revogar o acesso

Edite uma entrada em **“Acesso concedido”** para alterar seu escopo, permissões ou limites. Alterações no escopo e nas permissões são verificadas em solicitações subsequentes, incluindo solicitações de sessões que já estejam abertas. A revogação de um acesso encerra suas sessões e torna o token emitido inutilizável. **A opção “Sessões abertas”** também permite que o administrador encerre uma sessão individual sem revogar todo o acesso.

As cópias de exportação salvas mantêm seu criador, espaço de trabalho, escopo do chat e as permissões necessárias. Um usuário com acesso concedido pode listar ou baixar suas próprias cópias apenas enquanto essas permissões ainda estiverem válidas; cópias contendo o Case Board também exigem a permissão ``board.read``. O administrador pode recuperar todas as cópias. Cópias mais antigas sem esses metadados e pacotes de grupo são exclusivas do administrador. Os tickets de download e as respostas de arquivos preparadas verificam novamente o acesso após a preparação do arquivo, antes do envio de seus bytes.

A revogação não permite recuperar arquivos que já tenham sido baixados por alguém. Sair da conta, bloquear o painel ou encerrar uma sessão não interrompe um coletor em execução.

## O que o administrador pode visualizar

Revisores e analistas recebem o andamento da coleta sem pontos de extremidade de proxy, diagnósticos de pool, caminhos de servidor ou erros brutos de conexão. Os diagnósticos de conexão exigem a permissão `account` em todo o espaço de trabalho. A leitura de notificações, cópias externas e configurações de parâmetros exige a permissão `settings`.

As cadeias de caracteres completas do navegador User-Agent não são retidas nas sessões de acesso. Uma atualização também as remove do cache mutável da sessão. O log do processo do painel oculta literais de IP, credenciais de URL e segredos rotulados. Os logs de serviço locais e os registros de diário previamente assinados não são reescritos. As regras de acesso e os registros de login assinados ainda utilizam o endereço do cliente.

### Substituir a chave principal

Use **Acesso → Meus limites → Reemitir chave de administrador** ou execute `tgwitness token rotate` a partir de uma instalação gerenciada enquanto o painel estiver em execução. Todas as sessões existentes do navegador são encerradas, incluindo as abertas com tokens de colegas. O navegador solicitante recebe uma nova sessão; salve a nova chave de administrador antes de ocultá-la. Os tokens de colegas emitidos permanecem válidos até que sejam revogados separadamente. Uma instalação que utilize o comando ``TGWITNESS_TOKEN`` deve alterar essa configuração de ambiente e reiniciar.

### Limites de solicitação e proxy

A API admite até 600 solicitações por minuto por IP do cliente. Dez autenticações rejeitadas em um minuto acionam um período de espera exponencial, que varia de um segundo a cinco minutos. Uma tentativa malsucedida após o período de espera aumenta a duração; dez minutos sem nenhuma tentativa malsucedida reinicia a escalada. As rejeições retornam HTTP 429 e `Retry-After`. Os limites ficam na memória, compartilhados entre os espaços de trabalho em um processo do painel; a reinicialização os zera. As transmissões ao vivo são limitadas a quatro por token de portador e 32 para o processo do painel. Abrir uma transmissão também consome o limite de solicitações da API.

Os corpos das solicitações têm um prazo de recebimento de 60 segundos (8 segundos para MCP). Cada aplicativo limita os corpos incompletos a 32 solicitações e 64 MiB de cota reservada de rota. Corpos com tamanho excessivo retornam 413, corpos com tempo de espera esgotado retornam 408 e capacidade de corpo esgotada retorna 503 com “`Retry-After`”.

Os cabeçalhos de IP encaminhados são ignorados, a menos que o par TCP real pertença a `TGWITNESS_TRUSTED_PROXIES` (IPs separados por vírgulas ou CIDRs). Defina `TGWITNESS_PROXY_HEADER` como `x-forwarded-for` ou `cf-connecting-ip`. O XFF é percorrido do proxy mais próximo em direção ao primeiro par não confiável. Metadados de endereços confiáveis malformados ou duplicados são rejeitados, portanto não podem herdar um endereço de proxy da lista de permissões. O túnel rápido gerenciado confia no conector local do Cloudflare; a configuração de domínio próprio confia no Caddy local. Implantações diretas não confiam em nenhum proxy por padrão. Se você mesmo estiver iniciando o Uvicorn, desative o processamento de cabeçalhos de proxy para que esse limite receba o par real.

O `TGWITNESS_PANEL_ALLOWED_IPS` restringe todo o acesso ao painel, incluindo o do administrador, aos IPs ou CIDRs listados. A sonda de identidade de roteamento do instalador permanece pública e não retorna dados da conta. Inclua a rota administrativa local necessária antes de ativar a lista de permissões. O guia **START-HERE** de uma instalação gerenciada inclui as instruções de configuração e recuperação do serviço.

Um seletor de consulta da API `ws` deve identificar o espaço de trabalho no caminho da solicitação; seletores desconhecidos, incompatíveis e duplicados são rejeitados com o código 404.

Os scripts e estilos do painel contêm metadados de integridade SHA-384. Um mapa de importação também abrange módulos JS importados localmente em navegadores que suportam a integridade do mapa de importação. A resposta de linguagem gerada dinamicamente é separada. Essas verificações detectam a substituição de recursos em relação à página entregue; elas não estabelecem confiança em um servidor comprometido que possa substituir tanto a página quanto seus hashes.

**O registro, desde o início,** combina registros de processo com a atividade do diário de cada espaço de trabalho: logins, recusas, alterações de rota e ações do operador. Trata-se de um console na memória para o processo atual, e não de uma cópia permanente de todas as mensagens. Eventos de mensagens frequentes permanecem no diário, em vez de sobrecarregarem o console.

A emissão, alteração e revogação de acesso, bem como o início ou encerramento de sessões, também geram registros assinados no diário `access.*`. Os tokens não estão incluídos nesses registros. Os tokens emitidos e as credenciais de sessão são mantidos como hashes no cofre criptografado.

****Administrador principal e limite de confiança****

The main panel token remains unrestricted. Browser sign-ins with it create sessions subject to the administrator's configured session limits. Scripts sending the main token directly retain full access and are not counted as browser sessions.

This is application-level access control in one installation. All workspaces share the server process; this is not isolation from the host administrator. Keep the main token, Telegram sessions, signing keys and data directory private. A witness token is a separate checkpoint/health credential, not a panel access token.
