# Acesso e permissões

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/reference/access/

Defina o escopo de acesso a contas e conversas, escolha permissões, limite sessões e endereços IP e revogue o acesso.

Conceda a um revisor acesso a um chat, a um analista permissão para exportar um caso ou a um operador o controle de contas selecionadas. Cada pessoa recebe seu próprio token. O token do painel principal permanece com o administrador.

[Configuração da conta](https://phishdestroy.github.io/TgWitness/pt/docs/reference/accounts/) · [Rotas de conexão](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/) · [Modelo de segurança](https://phishdestroy.github.io/TgWitness/pt/docs/reference/security/)

## Dois escopos, duas funções distintas

**O escopo da coleta** determina o que uma conta registra: chats selecionados, uma pasta do Telegram ou a conta inteira. **O escopo de acesso** determina quais dessas contas e chats registrados outra pessoa pode visualizar e utilizar. Conceder acesso não significa ingressar em um chat do Telegram, iniciar a coleta nem conceder permissões à conta do Telegram.

Um acesso pode abrir espaços de trabalho selecionados, chats selecionados dentro deles ou todos os espaços de trabalho. **Todos os espaços de trabalho, incluindo aqueles adicionados posteriormente**, também abrangem futuras contas. Selecione os espaços de trabalho explicitamente quando um caso deva se limitar a eles.

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

| Permissão | O que ela permite |
| --- | --- |
| `view` | Leia conversas autorizadas, mensagens capturadas, perfis, arquivos e registros filtrados do diário. Sempre incluídos. |
| `export` | É permitido exportar o histórico de bate-papos e os dossiês. A exportação de evidências de todo o espaço de trabalho requer acesso a todo o espaço de trabalho. |
| `sources` | Gerencie fontes, instantâneos e captura de perfis. O acesso limitado a conversas pode atuar apenas nas conversas permitidas; a descoberta de fontes em toda a conta e as configurações de escopo permanecem desativadas. |
| `collect` | Inicie ou interrompa um coletor. Requer acesso a todo o espaço de trabalho, pois a coleta afeta a conta. |
| `interact` | Realize interações compatíveis com o Telegram dentro do escopo de acesso. O acesso limitado ao chat não permite a visualização de links em toda a conta. |
| `settings` | Altere as configurações de coleta, registros de data e hora, notificações, cópias externas e parâmetros. Requer acesso a todo o espaço de trabalho. |
| `account` | Faça login ou logout do Telegram e gerencie as rotas de conexão. Requer acesso a todo o espaço de trabalho. |

As permissões e o escopo são verificados em conjunto. Marcar uma permissão não abre outros chats nem desbloqueia uma operação em todo o espaço de trabalho para um acesso limitado a um chat. Para uma exportação paralela, o acesso deve abranger o chat exportado em todas as contas selecionadas. Um acesso concedido não pode criar novos acessos, gerenciar as sessões de outras pessoas nem abrir o console de administrador.

### Três configurações úteis

| Pessoa | Escopo | Permissões |
| --- | --- | --- |
| Revisor | Conversas registradas de um caso | `view` |
| Analista preparando uma transferência de funções | As conversas a serem investigadas e exportadas | `view`, `export`; adicione `interact` apenas caso seja necessário agir por meio do Telegram |
| Operador de coleta | Espaços de trabalho selecionados na íntegra | `view`, `sources`, `collect`; adicione `settings` ou `account` somente quando necessário |

Estes são exemplos que o senhor configura por meio das caixas de seleção de permissão, e não funções fixas.

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

Edite uma entrada na **seção “Acessos”** para alterar seu escopo, permissões ou limites. As alterações de escopo e permissão são verificadas em solicitações subsequentes, incluindo solicitações de sessões que já estejam abertas. A revogação de um acesso encerra suas sessões e torna o token emitido inutilizável. **As sessões abertas** também permitem que o administrador encerre uma sessão individual sem revogar todo o acesso.

A revogação não permite recuperar arquivos que já tenham sido baixados por alguém. Sair da conta, bloquear o painel ou encerrar uma sessão não interrompe um coletor em execução.

## O que o administrador pode visualizar

**O registro, desde o início,** combina registros de processo com a atividade do diário de cada espaço de trabalho: logins, recusas, alterações de rota e ações do operador. Trata-se de um console na memória para o processo atual, e não de uma cópia permanente de todas as mensagens. Eventos de mensagens frequentes permanecem no diário, em vez de sobrecarregarem o console.

A emissão, alteração e revogação de acesso, bem como o início ou encerramento de sessões, também geram registros assinados no diário `access.*`. Os tokens não estão incluídos nesses registros. Os tokens emitidos e as credenciais de sessão são mantidos como hashes no cofre criptografado.

****Administrador principal e limite de confiança**** O token do painel principal permanece sem restrições. Os logins no navegador com ele criam sessões sujeitas aos limites de sessão configurados pelo administrador. Scripts que enviam o token principal diretamente mantêm acesso total e não são contabilizados como sessões do navegador. Trata-se de um controle de acesso no nível do aplicativo em uma única instalação. Todos os espaços de trabalho compartilham o processo do servidor; isso não representa isolamento em relação ao administrador do host. Mantenha o token principal, as sessões do Telegram, as chaves de assinatura e o diretório de dados em sigilo. Um token de testemunha é uma credencial separada de verificação de integridade/funcionamento, não um token de acesso ao painel.
