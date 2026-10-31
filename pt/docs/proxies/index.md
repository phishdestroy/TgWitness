# Escolha um proxy

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/proxies/

Mantenha a conta conectada. Defina explicitamente quando sua rota poderá utilizar o endereço do servidor.

## Escolha primeiro o modo IP

01**Ocultar IP**

Utilize um proxy. Caso nenhum funcione, aguarde sem conexão direta com o Telegram.

02**Permitir alternativa**

Permitir conexão direta após o atraso configurado; retornar a um proxy funcional quando houver resposta.

03**Túnel / VPN**

Permita rotas diretas pela rede do provedor. Esta opção não instala nem verifica uma VPN.

A rota determina a conexão. O modo IP determina se uma conexão direta é permitida.

## Deixe que o pool mantenha a rota

1. Abra **a conta → Configurações → Configurações de conexão**.
2. Escolha o modo IP e **o MTProxy automático**, ou insira uma rota fixa.
3. Salve e execute **o teste de conexão com o Telegram**. Isso também funciona antes do login.
4. Após iniciar a coleta, verifique se uma mensagem de teste chega ao registro.

Os novos espaços de trabalho utilizam o MTProxy automático com a funcionalidade “Hide IP”. O conjunto combina quatro fontes públicas, verifica as entradas, mantém as rotas ativas e substitui os proxies com falha. Os downloads com falha mantêm os instantâneos anteriores.

## Utilize seu próprio proxy

Insira os detalhes de SOCKS5 ou HTTP CONNECT, cole um link de proxy do Telegram compatível ou forneça um catálogo de operadoras. Pause a observação antes de alterar uma rota ativa. Segredos TLS MTProxy falsos que começam com `ee` continuam sem suporte.

**Configurações de rotação, compartilhamento e repetição de tentativas**

Em **Parâmetros → MTProxy Automático**, defina limites de falha, tempos de espera, rotação planejada e número de contas por proxy. Um limite de compartilhamento igual a um faz com que a conta aguarde quando não houver entrada exclusiva disponível. Os intervalos de atualização da lista e de sondagem seguem os valores da área de trabalho principal. Proxies separados não garantem IPs de saída separados.

## Separar o Telegram de solicitações externas

O MTProxy transporta apenas o tráfego do Telegram. Carimbos de data/hora, notificações, cópias e verificações de fonte utilizam um proxy SOCKS5/HTTP separado, a rota SOCKS5/HTTP da conta ou a conexão direta, quando o modo IP o permitir. Essas solicitações externas podem ser desativadas.

Uma configuração explícita de `TGWITNESS_PROXY_FEED_PROXY` define a rota do downloader de feeds. A [testemunha independente](https://phishdestroy.github.io/TgWitness/pt/docs/witness/) mantém suas próprias configurações. Esses controles não instalam uma VPN no sistema nem redirecionam o tráfego do navegador.

Consulte [todos os modos, configurações padrão e listas de fontes](https://phishdestroy.github.io/TgWitness/pt/docs/reference/connection/#ip-modes), ou [escolha quem pode alterar a rota de uma conta](https://phishdestroy.github.io/TgWitness/pt/docs/access/).
