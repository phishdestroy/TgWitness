# Telegram · Mantenha a segurança

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/security/

O que sai da sua máquina, o que cada segredo abre e o que as proteções cobrem versus o que fica com você.

**127.0.0.1**endereço do painel por padrão

**256 bits**token de painel aleatório

**0**CDNs, análises ou fontes remotas

**Ed25519**assinatura em cada registro

## Onde tudo está disponível

O coletor, o painel e todos os registros ficam na sua máquina. Por padrão, só o Telegram é contatado; todo o resto é uma chave à parte.

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
- **Testemunha**Opcional · desativado por padrão

  Oferece pontos de verificação assinados e contadores de captura por meio de um token somente leitura. Não é capaz de ler conversas nem alterar configurações.

Padrão: apenas a conexão com o Telegram sai desta máquina.

Os destinos opcionais são configurados por espaço de trabalho. O texto das mensagens e as mídias são armazenados sem criptografia no diretório de dados: proteja-o com criptografia de disco e permissões de arquivo.

## O que cada segredo revela

| Secreto | Onde está armazenado | O que isso possibilita | Caso haja um vazamento |
| --- | --- | --- | --- |
| **Token do painel** | `panel-token.txt` no diretório de dados; o navegador guarda por aba | Tudo em todos os espaços | Pare o TgWitness, apague `panel-token.txt` e inicie de novo: você recebe um novo |
| **Sessão do Telegram** | Cofre, criptografado (`credentials.enc`) | A própria conta do Telegram | Encerre a sessão no Telegram em *Configurações → Dispositivos* |
| **Chave de assinatura** | Cofre, criptografado (`signing.enc`) | Assinar registros com a sua impressão digital | Pontos de verificação guardados em outro lugar, uma testemunha e carimbos de tempo ainda mostram o que existia antes |
| **Chave do cofre** | `vault.key` ao lado dos dados ou uma chave mestra externa | O cofre | Considere que a sessão e a chave de assinatura também vazaram |
| **Token Witness** | No servidor do TgWitness | Só leitura: pontos de verificação e estado | Apague na página da testemunha e crie um novo |
| **Texto para uso externo** | Vault; baixe-o uma vez para recuperação | A cópia externa | Quem também tiver o bucket pode descriptografar: considere a cópia exposta |

## O que as proteções abrangem

### Abrangido

- Um registro alterado, removido ou reordenado: a cadeia de hashes ou uma assinatura quebra.
- Um diário cortado ou reconstruído depois que você guardou um ponto de verificação em outro lugar: o ponto deixa de bater.
- Adivinhar o token: 256 bits aleatórios, comparação em tempo constante; 15 falhas por minuto e o endereço é bloqueado.
- Conteúdo hostil nos chats: texto continua texto, nunca HTML; anexos são baixados como arquivos; o painel não carrega nada de outros sites.
- Um diretório de dados roubado com chave de cofre externa: sessões e chaves continuam criptografadas.

### Fica a seu critério

- O token principal pode tudo. Dê aos outros acesso limitado e guarde o principal para você.
- Quem é administrador da máquina pode ler tudo e reassinar o diário. Guarde a impressão digital e os pontos de verificação em outro lugar.
- O TgWitness não criptografa mensagens nem mídia. Criptografe o disco e restrinja as permissões.
- HTTP puro fora do localhost vaza o token. Use HTTPS ou um túnel SSH.
- Assinaturas não dizem o que ficou de fora. Confira a cobertura e teste a entrega nas suas próprias contas e fontes.

[Compartilhe o acesso a um caso](https://phishdestroy.github.io/TgWitness/pt/docs/access/) com permissões, validade e limites de sessão.

## Reforçar a segurança de uma instalação

0 de 8 concluídos

1. **Use uma conta do Telegram dedicada**, nunca a principal.
2. **Mantenha o painel em 127.0.0.1.** Acesso remoto só por HTTPS (Caddy incluso) ou túnel SSH.
3. **Criptografe o disco** com o diretório de dados: mensagens e mídia ficam salvas como chegaram.
4. **Restrinja o diretório de dados** à conta de serviço (0700 no Unix, permissões de pasta no Windows).
5. **Guarde a chave do cofre em outro lugar** em servidores: defina `TGWITNESS_VAULT_KEY_FILE` antes da primeira inicialização.
6. **Guarde a impressão digital e os pontos de verificação** em outro sistema e rode uma testemunha em outro host.
7. **Nunca envie** chaves `data/`, de sessão, `panel-token.txt` ou do cofre para o GitHub ou para um chat.
8. **Não registre** cabeçalhos `Authorization` nem corpos de solicitação em um proxy reverso.

**É possível alterar o token do painel sem perder dados?**

Sim, ele só abre o painel. Pare o TgWitness, apague `panel-token.txt` e inicie de novo. Diário, sessões e chaves continuam. Se `TGWITNESS_TOKEN` estiver definido, esse valor vale no lugar do arquivo.

**Por que as mensagens não são criptografadas em repouso?**

O coletor precisa lê-los para pesquisar, comparar e exportar. Uma chave na mesma máquina não pararia quem já consegue ler essa máquina. A criptografia de disco cobre um disco roubado; as permissões, um em uso.

## Relatar uma vulnerabilidade

**Security → Report a vulnerability** no GitHub. Versão, impacto e uma reprodução mínima com dados fictícios. Nunca envie credenciais, pastas de contas ou evidências reais. Se o relato privado estiver desativado, abra uma issue pedindo um canal privado, sem detalhes do exploit.
