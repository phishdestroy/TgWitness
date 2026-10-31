# Mantenha a segurança

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/security/

Conheça as rotas do Telegram, as listas públicas de proxies e os serviços externos opcionais. Saiba o que cada recurso desbloqueia, o que as proteções abrangem e o que fica a seu cargo.

**127.0.0.1**endereço do painel por padrão

**256 bits**token de painel aleatório

**0**CDNs, análises ou fontes remotas

**Ed25519**assinatura em cada registro

## Onde tudo está disponível

O coletor, seu painel e todos os registros salvos permanecem no computador ou servidor em que o programa é executado. O Telegram é o único destino por padrão; cada outro destino é uma opção separada.

06 / O QUE SAI DA MÁQUINASua instalação

SEU COMPUTADOR OU SERVIDOR

**Painel**127.0.0.1:8787 · token bearer

**Coletor**um cliente do Telegram por espaço de trabalho

DIRETÓRIO DE DADOS

**Registro**SQLite · encadeamento de hash · assinado

**Mídia**arquivos nomeados por SHA-256

**Cofre**Fernet · sessão, par de API, chave de assinatura, proxy

- **Telegram**Sempre · por meio de sua rota

  A conexão MTProto da conta: direta, SOCKS5, HTTP ou MTProxy. O modo “Ocultar IP” aguarda um proxy em funcionamento. O recurso de fallback direto requer um modo que o permita explicitamente.
- **Texto externo**Opcional · desativado por padrão

  O diário, os arquivos e os pontos de verificação são criptografados com AES-GCM antes do envio para um armazenamento compatível com S3. A chave permanece em seu poder; os anexos são nomeados por hashes chaveados, e não pelo hash de seu conteúdo.
- **Notificações**Opcional · desativado por padrão

  Problemas e contagem de alterações com títulos de bate-papo. Trechos de mensagens são enviados somente se você ativar essa função.
- **Autoridade de carimbo de data e hora**Opcional · desativado por padrão

  Apenas o SHA-256 de um ponto de verificação assinado e um nonce aleatório. Sem mensagens, sem nomes de chat.
- **Witness**Opcional · desativado por padrão

  Oferece pontos de verificação assinados e contadores de captura por meio de um token somente leitura. Não é capaz de ler conversas nem alterar configurações.

Padrão: apenas a conexão com o Telegram sai desta máquina.

Os destinos opcionais são configurados por espaço de trabalho. O texto das mensagens e as mídias são armazenados sem criptografia no diretório de dados: proteja-o com criptografia de disco e permissões de arquivo.

## O que cada segredo revela

| Secreto | Onde está armazenado | O que isso possibilita | Caso haja um vazamento |
| --- | --- | --- | --- |
| **Token do painel** | `panel-token.txt` no diretório de dados; o navegador o mantém apenas para a aba | Tudo em cada espaço de trabalho: ler e exportar, alterar o escopo, fazer login nas contas | Interrompa o TgWitness, exclua o `panel-token.txt` e reinicie-o: um novo token será criado |
| **Sessão do Telegram** | Cofre, criptografado (`credentials.enc`) | A própria conta do Telegram | Encerre a sessão no Telegram em *Configurações → Dispositivos* |
| **Chave de assinatura** | Cofre, criptografado (`signing.enc`) | Registros assinados que podem ser verificados por meio de sua assinatura digital | Pontos de verificação armazenados em outro local, uma testemunha e registros de data e hora mostram o que existia anteriormente |
| **Chave do cofre** | `vault.key` ao lado dos dados, ou uma chave mestra externa para um novo diretório de dados | Decifrando o cofre | Considere que a chave de sessão e a chave de assinatura também foram vazadas |
| **Token Witness** | No servidor do TgWitness | Somente leitura: pontos de verificação assinados e integridade | Exclua-o na página do Witness; crie um novo |
| **Texto para uso externo** | Vault; baixe-o uma vez para recuperação | Descriptografando a cópia externa | Quem quer que também possua os objetos armazenados pode descriptografá-los: considere essa cópia como exposta |

## O que as proteções abrangem

### Abrangido

- Um registro alterado, removido ou reordenado em uma exportação: a cadeia de hash ou a assinatura não é mais válida.
- Um registro que foi reduzido ou reconstruído após um ponto de verificação ter sido mantido em outro local: o ponto de verificação retido não corresponde mais.
- Adivinhação do token do painel: 256 bits aleatórios, comparados em tempo constante; após 15 falhas por minuto, um endereço é recusado.
- Conteúdo hostil de bate-papo: o texto é inserido como texto, nunca como HTML; os anexos são baixados como arquivos; o painel não carrega nada de outros sites.
- Um diretório de dados copiados com uma chave de cofre externa: as sessões e as chaves de assinatura permanecem criptografadas sem a chave mestra.

### Fica a seu critério

- O token do painel principal detém controle total. Conceda a outras pessoas acesso restrito às contas, conversas e ações de que necessitem; mantenha a chave principal em sigilo.
- Um administrador do sistema pode ler todo o conteúdo, bem como reescrever e assinar novamente o registro. Mantenha a impressão digital e os pontos de verificação em outro sistema.
- O texto das mensagens e as mídias não são criptografados pelo TgWitness. Utilize criptografia de disco e permissões rigorosas.
- O uso de HTTP simples fora do localhost expõe o token na rede. Utilize HTTPS ou um túnel SSH.
- As assinaturas comprovam que o que foi registrado não foi alterado, e não que todos os eventos do Telegram tenham sido registrados.

[Compartilhe o acesso a um caso](https://phishdestroy.github.io/TgWitness/pt/docs/access/) com permissões, prazo de validade e limites de sessão. Um token de testemunha continua sendo uma credencial separada.

## Reforçar a segurança de uma instalação

0 de 8 concluídos

1. **Utilize uma conta dedicada do Telegram** — nunca a sua conta principal. O token do painel e a sessão proporcionam controle total sobre ela.
2. **Mantenha o painel no endereço 127.0.0.1.** Acesse-o remotamente apenas por meio de HTTPS (a configuração do Caddy incluída) ou de um túnel SSH.
3. **Criptografe o disco** que contém o diretório de dados: o texto das mensagens e as mídias são armazenados exatamente como chegaram.
4. **Restrinja o diretório de dados** à conta de serviço. Novos diretórios recebem o modo 0700 no Unix; no Windows, defina as permissões da pasta.
5. **Mantenha a chave mestra do cofre em outro local** nos servidores: defina ``TGWITNESS_VAULT_KEY_FILE`` antes de criar o diretório de dados.
6. **Salve a impressão digital da chave de assinatura e os pontos de verificação** em outro sistema e adicione uma testemunha em outro servidor.
7. **Nunca envie** chaves `data/`, de sessão, `panel-token.txt` ou do cofre para o GitHub ou para um chat.
8. **Não registre** cabeçalhos `Authorization` nem corpos de solicitação em um proxy reverso.

**É possível alterar o token do painel sem perder dados?**

Sim. O token apenas abre o painel. Encerre o TgWitness, exclua `panel-token.txt` do diretório de dados e reinicie-o; o registro, as sessões e as chaves permanecem inalterados. Com `TGWITNESS_TOKEN` definido, o valor da variável de ambiente é utilizado em vez do arquivo.

**Por que as mensagens não são criptografadas em repouso?**

O coletor deve lê-las para pesquisar, comparar versões e exportar. Criptografá-las com uma chave na mesma máquina traria pouca proteção contra alguém capaz de acessar essa máquina. A criptografia de disco protege um disco desligado ou roubado; permissões rigorosas protegem um disco em funcionamento.

## Relatar uma vulnerabilidade

Utilize **Segurança → Relatar uma vulnerabilidade** no repositório do GitHub. Inclua a versão, o impacto e uma reprodução sintética mínima. Nunca envie credenciais, diretórios de contas ou arquivos de evidências reais. Caso o relatório privado não esteja disponível, abra uma solicitação pedindo um canal privado sem detalhes da exploração.
