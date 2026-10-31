# Conecte uma conta

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/accounts/

Cada espaço de trabalho contém uma conta, seu registro e sua chave de assinatura.

## Escolha como fazer login

Crie **contas**, adicione um espaço de trabalho e abra suas configurações de conexão. Utilize uma conta dedicada para observação.

- **Código QR:** escaneie-o nas configurações do dispositivo do Telegram e confirme o novo login.
- **Número de telefone:** insira o número, o código enviado pelo Telegram e sua senha de verificação em duas etapas, caso esteja ativada.
- **Importação de sessão:** importe uma sessão compatível ou dados do Telegram Desktop de sua propriedade.

Escolha um perfil de API integrado ou insira seu próprio ID de API e hash. Um perfil de API identifica o cliente; ele não faz login em uma conta nem torna a conexão anônima.

**Precisa de um proxy primeiro?**

É possível [escolher e testar a rota de conexão](https://phishdestroy.github.io/TgWitness/pt/docs/proxies/) antes de fazer o login. Cada conta possui sua própria rota.

## Escolha o que deseja monitorar

1. Abra a lista de fontes e selecione os chats, grupos ou canais de que necessita.
2. Verifique as configurações de coleta, incluindo arquivos de mídia, antes de iniciar a observação.
3. Inicie o coletor e verifique sua conexão e atividade recente.

A conta deve ter acesso à fonte. Diferentes funções podem visualizar eventos distintos; o registro reflete o que essa conta recebeu.

Para um caso que abranja toda a conta, utilize **Fontes → Escopo de observação → Modo de investigação**, revise as configurações e clique em **Salvar escopo**. O [guia completo de investigação](https://phishdestroy.github.io/TgWitness/pt/docs/cases/) abrange todos os tipos de bate-papo visíveis, histórico antigo, perfis de pessoas, referências entre bate-papos e transferência de evidências.

## Verifique o caminho completo

Em um grupo de teste sob seu controle, envie uma mensagem exclusiva a partir de outra conta, edite-a e exclua-a. Confirme os três eventos no registro, em seguida, [exporte e verifique](https://phishdestroy.github.io/TgWitness/pt/docs/exports/) o registro.

O status “conectado” confirma a conexão. Uma mensagem de teste capturada confirma que um determinado evento chegou a este espaço de trabalho.

## Adicionar outra conta

Crie outro espaço de trabalho em **“Contas”** e repita a configuração. Guarde a impressão digital da chave de assinatura de cada conta para que possa identificar suas exportações posteriormente.
