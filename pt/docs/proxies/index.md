# Telegram · Escolha um proxy

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/proxies/

Mantenha a conta online e decida você se ela pode algum dia mostrar o IP do seu servidor.

## Escolha primeiro o modo IP

01**Ocultar o endereço**

Só proxy. Se nenhum funcionar, espera.

02**Recurso direto como último recurso**

Vai direto depois de um atraso e volta a um proxy assim que um funcionar.

03**Servidor atrás de um túnel ou VPN**

Direto pode. Não configura nem verifica a VPN por você.

A rota determina a conexão. O modo IP determina se uma conexão direta é permitida.

## Deixe que o pool mantenha a rota

1. **Conta → Configurações → Configurações de conexão**.
2. Escolha o modo de IP e **MTProxy automático**, ou uma rota fixa.
3. Salve e use **Testar conexão com o Telegram** (funciona também antes do login).
4. Comece a coletar e envie uma mensagem de teste para você mesmo.

Espaços novos começam no MTProxy automático com **Ocultar o endereço**. O pool usa quatro listas públicas, testa servidores, fica com os bons e troca os que caíram.

## Utilize seu próprio proxy

SOCKS5, HTTP CONNECT, um link de proxy do Telegram ou um catálogo do operador. Pause a observação antes de trocar. Segredos Fake TLS (`ee`…) não funcionam.

**Configurações de rotação, compartilhamento e repetição de tentativas**

**Parâmetros → MTProxy automático**: limites de falha, esperas, rotação e contas por proxy. Limite 1 significa que a conta espera em vez de compartilhar. Proxies diferentes ainda podem ter o mesmo IP de saída.

## Separar o Telegram de solicitações externas

O MTProxy só carrega o Telegram. Carimbos de tempo, notificações, cópias e verificação de código passam por um proxy SOCKS5/HTTP separado, pela rota SOCKS5/HTTP da conta ou direto, se o modo permitir. Ou desligue-os.

`TGWITNESS_PROXY_FEED_PROXY` define a rota para baixar as listas. A [testemunha](https://phishdestroy.github.io/TgWitness/pt/docs/witness/) tem configurações próprias. Nada disso mexe no seu navegador ou na rede do sistema.

Mais: [modos e padrões](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes), [quem pode mudar rotas](https://phishdestroy.github.io/TgWitness/pt/docs/access/).
