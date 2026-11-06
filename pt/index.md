# As mensagens mudam． Guarde o que o senhor viu．

Canonical page: https://phishdestroy.github.io/TgWitness/pt/

[Código aberto ／ v0.9.1](https://phishdestroy.github.io/TgWitness/pt/docs/reference/changelog/)

Exporte conversas do Telegram， preserve seu histórico e compartilhe um arquivo assinado que outras pessoas possam verificar．

[Acesse a demonstração](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)[Guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)

Dados fictícios， sem login no Telegram．

 [Exportar uma conta ou chats selecionados](https://phishdestroy.github.io/TgWitness/pt/docs/reference/account-export/) [Captura com GitHub Actions （prévia）](https://phishdestroy.github.io/TgWitness/pt/docs/capture/) [Cópia externa no S3： configuração e recuperação](https://phishdestroy.github.io/TgWitness/pt/#s3)

UMA MENSAGEM， ATRAVÉS DO TEMPO ＃0042

Northstar · PesquisaFonte／mensagem fictícia 42

1. **Mensagem observada：**09：41：02

   O resumo começa em 14：00．
2. **Edição preservada**09：43：18

   O resumo começa em 15：00．

   Versão anterior mantida
3. **Aviso de exclusão**10：06：45

   O conteúdo capturado permanece no seu registro．

Três observações． Uma história． EXEMPLO

A mensagem desaparece． O histórico capturado permanece．

## Cada alteração capturada． Exatamente onde o senhor precisa．

A interface real， com dados inventados．

TgWitness ／ Conversas salvasSEU ESPAÇO DE TRABALHO DE OBSERVAÇÃO

![Conversas do Telegram salvas no tema escuro， com edições capturadas e mensagens excluídas mantidas em seu contexto](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Chats salvos Parece um chat comum， com edições e exclusões logo ao lado das mensagens．

TgWitness ／ RegistroESPAÇO DE TRABALHO LOCAL

![Registro contendo mensagens observadas， edições， notificações de exclusão e eventos de cobertura](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Diário Tudo o que sua conta viu， pesquisável， com as lacunas marcadas．

TgWitness ／ Histórico de ediçõesESPAÇO DE TRABALHO LOCAL

![Janela de detalhes comparando as versões anteriores capturadas e as versões editadas de uma mensagem](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Histórico de edições Versão antiga e nova lado a lado， nada é sobrescrito．

TgWitness ／ Exportações assinadasESPAÇO DE TRABALHO LOCAL

![Exportação do espaço de trabalho， oferecendo um arquivo ZIP assinado， JSONL， CSV e um relatório HTML offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Exportações assinadas Leve o diário com você， assinado e com o próprio verificador．

Acompanhe um registro salvo por meio do [Case Board](https://phishdestroy.github.io/TgWitness/pt/docs/case-board/)， [da elaboração do relatório](https://phishdestroy.github.io/TgWitness/pt/docs/reports/) e de uma [cópia para compartilhamento](https://phishdestroy.github.io/TgWitness/pt/docs/handover/)． [Analise grupos de contas](https://phishdestroy.github.io/TgWitness/pt/docs/groups/) em conjunto．

01 ／ CAPTURA

### O senhor escolhe o escopo．

Alguns chats， uma pasta ou a conta inteira． Cada conta tem seu próprio espaço．

[Compare os modos de coleta](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#scope)

02 ／ PRESERVAR

### As alterações enriquecem a narrativa．

Versões， exclusões e lacunas ficam todas no diário．

[Consulte a matriz de eventos](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#events)

03 ／ ENTREGA

### Um registro que se propaga．

ZIP assinado， arquivos e relatório offline． Senha opcional．

[Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)

## Altere um byte．
A verificação irá indicar．

Cada evento possui um link para o hash anterior e contém uma assinatura Ed25519．

![Os eventos capturados contêm links para hashes anteriores， possuem assinaturas e são exportados de forma verificável．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![A alteração de um registro capturado altera seu hash e invalida a verificação do registro vinculado．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Um ponto de verificação mantido separadamente permite que o destinatário compare o registro exportado com uma observação anterior．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Siga as verificações desde o hash de um arquivo até um ponto de verificação mantido separadamente．

[Explore os oito níveis de evidência](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#levels)

## Pronto para uma revisão por outra pessoa．

Mensagens， arquivos e relatório offline em um único pacote assinado．

[Leia o modelo de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

tgwitness-evidence.zipPACOTE ASSINADO

- 01

  Observações originaisRegistros em JSONL ＋ tabela em CSV
- 02

  Contexto de fácil compreensãoRelatório HTML offline ＋ mídia preservada
- 03

  Verificação independenteManifesto assinado ＋ verificador independente

O destinatário confere tudo com a sua chave， e um ponto de verificação guardado em outro lugar mostra que nada foi reescrito desde então． [Como as verificações funcionam．](https://phishdestroy.github.io/TgWitness/pt/docs/concepts/#layers)

## Cópias no S3． Verificações externas．

Mantenha cópias criptografadas e adicione verificações independentes．

Desativado por padrão

### Copie tudo para um armazenamento compatível com S3

Diário， arquivos， pontos de verificação e exportações de chats， criptografados antes de ir para o S3．

**Configurações de armazenamento e recuperação**

Criptografia no lado do cliente

`AES-256-GCM` na sua máquina． O provedor só vê texto cifrado．

Cópias programadas ou manuais

Copie agora ou a cada 1 a 1.440 minutos， com o progresso no painel．

Object Lock

Escolha os dias e o modo de retenção； o painel confere se realmente pegou．

Recuperação verificada

Guarde a chave separadamente． Restaure em qualquer lugar： os arquivos só saem depois da verificação．

![Painel completo de cópia externa： endpoint， região， bucket， chaves de acesso， programação， controles de Object Lock e chave de recuperação](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

O painel completo com opções avançadas está expandido． Nenhuma credencial de armazenamento é exibida．

Revista e mídia`AES-256-GCM`Armazenamento compatível com S3

[Configure o S3 e restaure uma cópia](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3)[Leia os detalhes da verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Chave de recuperação** Guarde－a separadamente； sem ela a cópia fica ilegível．

### Notificações · Apprise

Problemas， mudanças nos chats e um resumo diário para mensageiros， e－mail ou seu próprio webhook．

**Escolha o que compartilhar** Sem texto de mensagens， a menos que você ative．

 [Configurar destinos de notificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/#notifications)

### Carimbos de data e hora externos

Hashes de pontos de verificação com data e hora usando RFC 3161 e OpenTimestamps．

**Acompanhe o resultado** Confira a resposta da TSA ou atualize o recibo do OpenTimestamps para uma prova em Bitcoin．

 [Verifique as provas de data e hora](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/)

### Testemunha independente

Um servidor separado armazena as observações assinadas e pode publicar `TGW1` pontos de verificação．

**Separe a referência** Rode em outro host， com chave e diário próprios．

 [Configure um Witness](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)

### Recuperação e lacunas visíveis

Retomar após reinicialização． Verifica novamente e `coverage.json` exiba as mensagens recuperadas e as lacunas．

**Revise o intervalo** Mensagens recuperadas e lacunas registradas lado a lado．

 [Verifique a continuidade e as lacunas](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#continuity)

## Seu primeiro espaço de trabalho começa aqui．

Experimente a demo primeiro e conecte uma conta reserva quando estiver pronto．
Windows， Linux， macOS ou Docker．

[Leia o guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)

**Uma sessão importada， um cliente em execução．**

Não use uma TData ou sessão importada no Telegram Desktop e no TgWitness ao mesmo tempo： o Telegram pode derrubar as duas （AUTH_KEY_DUPLICATED）． Precisa das duas？ Entre no TgWitness separadamente， por telefone ou QR．

[Leia o aviso sobre a importação de sessão](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt#session-warning)

**Dê uma olhada antes de se conectar．**

Experimente o ambiente de trabalho fictício sem uma conta do Telegram．

[Acesse a demonstração online →](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Comandos de instalação local**

PASSO 01

### Acesse o código－fonte．

[Baixe o arquivo ZIP com o código－fonte](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) e extraia－o， ou clone o repositório：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Precisa de Python 3.11+． No Windows， o inicializador oferece a instalação．

[Navegue pelas versões](https://github.com/phishdestroy/TgWitness/releases)

PASSO 02

### Escolha como executar．

Clique duas vezes em `Start.cmd` ou execute no PowerShell：

```
.\Start.cmd
```

Está apenas explorando？ Clique duas vezes em `scripts\Demo.cmd` para acessar uma demonstração isolada． Não é necessário fazer login no Telegram．

Com Python 3.11+ e `venv`disponíveis：

```
sh start.sh
```

Para abrir o registro fictício， execute `sh start.sh --demo`．

Com o Docker em execução e o Compose 2.20+ instalado：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

O segundo comando exibe o token do seu painel privado． Guarde－o em seu computador．

Acesse [127.0.0.1:8787](http://127.0.0.1:8787) após a inicialização．

Em instalações pelo código－fonte， o token fica em `data/live/panel-token.txt`． Seu próprio par de API do [my.telegram.org](https://my.telegram.org) é opcional． [Guia completo ↗](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)

**TgWitness 0.9.1** [Novidades →](https://phishdestroy.github.io/TgWitness/pt/docs/reference/changelog/) · [Recursos e limitações conhecidas →](https://phishdestroy.github.io/TgWitness/pt/docs/reference/features/)

## Instruções claras． Um próximo passo útil．

[Explore os guias ↗](https://phishdestroy.github.io/TgWitness/pt/docs/)

[### Modos， cenários e níveis de evidência Quatro modos de coleta． Oito níveis de verificação． Encontre o fluxo de trabalho adequado para o seu caso．](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html)

[01 ### Conecte uma conta Importação por telefone， QR e sessões compatíveis．](https://phishdestroy.github.io/TgWitness/pt/docs/accounts/)[02 ### Escolha um proxy Listas públicas do MTProxy ou sua própria rota．](https://phishdestroy.github.io/TgWitness/pt/docs/proxies/)[03 ### Configure um bot do Witness Pontos de verificação assinados em seu canal do Telegram．](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)[04 ### Exportar e verificar Compartilhe o histórico capturado e verifique sua integridade．](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)

## Trabalhe com o arquivo．

Histórico， IA com fontes， MCP， OCR e webhooks assinados．

[Explore o fluxo de trabalho](https://phishdestroy.github.io/TgWitness/pt/docs/archive/)

## Antes de começar．

**Esta página está vinculada ao Telegram？**

Não． É uma página estática com exemplos fictícios． O aplicativo roda na sua máquina e é lá que você faz login．

**É possível recuperar mensagens excluídas antes da captura？**

Não． Ele guarda o que sua conta viu enquanto estava rodando． Um snapshot posterior não consegue reconstruir edições perdidas nem mensagens excluídas．

**Todo o meu diário está criptografado？**

Sessões e chaves， sim． Mensagens e arquivos， não： use criptografia de disco． Exportações podem ter senha AES－256．

**Esta ferramenta é afiliada ao Telegram？**

Não． É um projeto independente， com licença MIT， feito sobre o Telethon． Você entra com suas próprias contas．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore primeiro． Configure quando estiver pronto．

[Acesse a demonstração](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)[Guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)
