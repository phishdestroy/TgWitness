# As mensagens mudam. Guarde o que o senhor viu.

Canonical page: https://phishdestroy.github.io/TgWitness/pt/

[Código aberto / v0.7.0](https://phishdestroy.github.io/TgWitness/pt/docs/reference/changelog/)

Capture mensagens do Telegram, preserve suas alterações e exporte um registro assinado.

[Acesse a demonstração](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)[Guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)

A demonstração utiliza dados fictícios. Não é necessário fazer login no Telegram.

 [Captura com GitHub Actions (prévia)](https://phishdestroy.github.io/TgWitness/pt/docs/capture/) [Cópia externa no S3: configuração e recuperação](https://phishdestroy.github.io/TgWitness/pt/#s3)

UMA MENSAGEM, ATRAVÉS DO TEMPO #0042

Northstar · PesquisaFonte/mensagem fictícia 42

1. **Mensagem observada:**09:41:02

   O resumo começa em 14:00.
2. **Edição preservada**09:43:18

   O resumo começa em 15:00.

   Versão anterior mantida
3. **Aviso de exclusão**10:06:45

   O conteúdo capturado permanece no seu registro.

Três observações. Uma história. EXEMPLO

A mensagem desaparece. O histórico capturado permanece.

## Cada alteração capturada. Exatamente onde o senhor precisa.

Navegue pela interface com dados de demonstração fictícios.

TgWitness / Conversas salvasSEU ESPAÇO DE TRABALHO DE OBSERVAÇÃO

![Conversas do Telegram salvas no tema escuro, com edições capturadas e mensagens excluídas mantidas em seu contexto](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Conversas salvas Uma visualização familiar das conversas, com edições capturadas e avisos de exclusão ao lado das mensagens.

TgWitness / RegistroESPAÇO DE TRABALHO LOCAL

![Registro contendo mensagens observadas, edições, notificações de exclusão e eventos de cobertura](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Registro: uma linha do tempo pesquisável do que sua conta observou, incluindo interrupções.

TgWitness / Histórico de ediçõesESPAÇO DE TRABALHO LOCAL

![Janela de detalhes comparando as versões anteriores capturadas e as versões editadas de uma mensagem](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Histórico de edições Compare versões capturadas sem sobrescrever a observação anterior.

TgWitness / Exportações assinadasESPAÇO DE TRABALHO LOCAL

![Exportação do espaço de trabalho, oferecendo um arquivo ZIP assinado, JSONL, CSV e um relatório HTML offline](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Exportações assinadas Leve o registro com você, acompanhado de um manifesto e de um verificador independente.

01 / CAPTURA

### O senhor escolhe o escopo.

Bate-papos selecionados, uma pasta do Telegram ou toda a conta. Um espaço de trabalho separado para cada conta.

[Compare os modos de coleta](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#scope)

02 / PRESERVAR

### As alterações enriquecem a narrativa.

As versões capturadas, os avisos de exclusão e as lacunas de observação permanecem no diário.

[Consulte a matriz de eventos](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#events)

03 / ENTREGA

### Um registro que se propaga.

Arquivo ZIP assinado, arquivos preservados e um relatório offline. Proteção por senha opcional.

[Exportar e verificar](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)

## Altere um byte. A cadeia informa a você.

Cada evento possui um link para o hash anterior e contém uma assinatura Ed25519.

![Os eventos capturados contêm links para hashes anteriores, possuem assinaturas e são exportados de forma verificável.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![A alteração de um registro capturado altera seu hash e invalida a verificação do registro vinculado.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Um ponto de verificação mantido separadamente permite que o destinatário compare o registro exportado com uma observação anterior.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Veja o que cada mecanismo de verificação estabelece e quais são os seus limites.

[Explore os oito níveis de evidência](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#levels)

## Pronto para uma revisão por outra pessoa.

Entregue as observações, os arquivos e um relatório HTML offline em um único pacote assinado.

[Leia o modelo de evidência](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/)

tgwitness-evidence.zipPACOTE ASSINADO

- 01

  Observações originaisRegistros em JSONL + tabela em CSV
- 02

  Contexto de fácil compreensãoRelatório HTML offline + mídia preservada
- 03

  Verificação independenteManifesto assinado + verificador independente

As assinaturas detectam adulterações em relação a uma chave confiável. Elas não comprovam a origem do Telegram nem garantem a captura completa. O conteúdo do registro e as mídias precisam de armazenamento criptografado fornecido por você.

## Cópias no S3. Verificações externas.

Mantenha cópias criptografadas e adicione verificações independentes.

Desativado por padrão

### Copie tudo para um armazenamento compatível com S3

Diários, arquivos, pontos de verificação com registro de data e hora e exportações de bate-papos — criptografados antes do envio para o AWS S3 ou armazenamento compatível.

**Configurações de armazenamento e recuperação**

Criptografia no lado do cliente

O `AES-256-GCM` criptografa objetos nesta máquina. O provedor recebe objetos criptografados.

Cópias programadas ou manuais

Copie agora ou escolha um intervalo de 1 a 1.440 minutos. Verifique o andamento no painel.

Object Lock

Selecione os dias de retenção e um modo, desde que o bucket ofereça suporte a isso. O painel informa se a retenção foi confirmada para um objeto enviado.

Recuperação verificada

Baixe a chave de criptografia e guarde-a em local separado. Faça a restauração em outro computador; os arquivos só são publicados após verificação.

![Painel completo de cópia externa: endpoint, região, bucket, chaves de acesso, programação, controles de Object Lock e chave de recuperação](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

O painel completo com opções avançadas está expandido. Nenhuma credencial de armazenamento é exibida.

Revista e mídia`AES-256-GCM`Armazenamento compatível com S3

[Configure o S3 e restaure uma cópia](https://phishdestroy.github.io/TgWitness/pt/docs/exports/#s3)[Leia os detalhes da verificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/evidence/#off-site-copy-and-restore-s3)

**O que não faz** A ferramenta não restaura as mensagens sem a chave de descriptografia exportada nem substitui uma testemunha independente.

### Notificações · Apprise

Alertas de problemas, alterações no chat e resumos diários via Apprise: aplicativos de mensagens, e-mail ou seu próprio webhook JSON.

**Não faz**: não envia o texto da mensagem, a menos que você habilite os trechos.

 [Configurar destinos de notificação](https://phishdestroy.github.io/TgWitness/pt/docs/reference/operations/#notifications)

### Carimbos de data e hora externos

Hashes de pontos de verificação com data e hora usando RFC 3161 e OpenTimestamps.

**O que não faz** Ele não considera um recibo pendente no calendário como um carimbo de data/hora confirmado do Bitcoin.

 [Verifique as provas de data e hora](https://phishdestroy.github.io/TgWitness/pt/docs/reference/timestamp/)

### Testemunha independente

Um servidor separado armazena as observações assinadas e pode publicar `TGW1` pontos de verificação.

**O que não faz** Isso não transforma dois espaços de trabalho em um único host coletor em testemunhas independentes.

 [Configure um Witness](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)

### Recuperação e lacunas visíveis

Retomar após reinicialização. Verifica novamente e `coverage.json` exiba as mensagens recuperadas e as lacunas.

**O que não faz** A ferramenta não reconstrói todas as edições perdidas ou mensagens que desapareceram.

 [Verifique a continuidade e as lacunas](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html#continuity)

## Seu primeiro espaço de trabalho começa aqui.

Experimente primeiro a demonstração. Conecte uma conta dedicada quando estiver pronto. Windows, Linux, macOS ou Docker.

[Leia o guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)

**Uma sessão importada, um cliente em execução.**

Não execute uma chave TData/sessão importada no Telegram Desktop e no TgWitness ao mesmo tempo. O Telegram pode invalidar a autorização compartilhada (AUTH_KEY_DUPLICATED). Para uso paralelo, crie um login separado no TgWitness por telefone ou QR.

[Leia o aviso sobre a importação de sessão](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt#session-warning)

**Dê uma olhada antes de se conectar.**

Experimente o ambiente de trabalho fictício sem uma conta do Telegram.

[Acesse a demonstração online →](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Comandos de instalação local**

PASSO 01

### Acesse o código-fonte.

[Baixe o arquivo ZIP com o código-fonte](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) e extraia-o, ou clone o repositório:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

A execução do código-fonte requer o Python 3.11 ou superior. O instalador do Windows oferece a instalação caso o Python não esteja presente.

[Navegue pelas versões](https://github.com/phishdestroy/TgWitness/releases)

Não possui o Python no Windows? [Baixe o pacote portátil](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), extraia-o e clique duas vezes em “`TgWitness.cmd`”.

PASSO 02

### Escolha como executar.

Clique duas vezes em `Start.cmd` ou execute no PowerShell:

```
.\Start.cmd
```

Está apenas explorando? Clique duas vezes em `scripts\Demo.cmd` para acessar uma demonstração isolada. Não é necessário fazer login no Telegram.

Com Python 3.11+ e `venv`disponíveis:

```
sh start.sh
```

Para abrir o registro fictício, execute `sh start.sh --demo`.

Com o Docker em execução e o Compose 2.20+ instalado:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

O segundo comando exibe o token do seu painel privado. Guarde-o em seu computador.

Acesse [127.0.0.1:8787](http://127.0.0.1:8787) após a inicialização.

Para instalações a partir do código-fonte, o token é `data/live/panel-token.txt`. O login no Telegram pode ser feito usando as configurações da API integrada ou seu próprio par de chaves obtido em [my.telegram.org](https://my.telegram.org). [Guia completo de configuração ↗](https://phishdestroy.github.io/TgWitness/pt/docs/reference/quickstart/)

**TgWitness 0.7.0** [Novidades →](https://phishdestroy.github.io/TgWitness/pt/docs/reference/changelog/) · [Recursos e limitações conhecidas →](https://phishdestroy.github.io/TgWitness/pt/docs/reference/features/)

## Instruções claras. Um próximo passo útil.

[Explore os guias ↗](https://phishdestroy.github.io/TgWitness/pt/docs/)

[### Modos, cenários e níveis de evidência Quatro modos de coleta. Oito níveis de verificação. Encontre o fluxo de trabalho adequado para o seu caso.](https://phishdestroy.github.io/TgWitness/pt/guides/modes.html)

[01 ### Conecte uma conta Importação por telefone, QR e sessões compatíveis.](https://phishdestroy.github.io/TgWitness/pt/docs/accounts/)[02 ### Escolha um proxy Listas públicas do MTProxy ou sua própria rota.](https://phishdestroy.github.io/TgWitness/pt/docs/proxies/)[03 ### Configure um bot do Witness Pontos de verificação assinados em seu canal do Telegram.](https://phishdestroy.github.io/TgWitness/pt/docs/witness/)[04 ### Exportar e verificar Compartilhe o histórico capturado e verifique sua integridade.](https://phishdestroy.github.io/TgWitness/pt/docs/exports/)

## Trabalhe com o arquivo.

Carregar histórico, revisar fontes de IA, conectar um cliente MCP, reconhecer mídias salvas e enviar webhooks assinados.

Disponível na fonte atual. A versão prévia portátil 0.7.0 é anterior a essas ferramentas.

[Explore o fluxo de trabalho](https://phishdestroy.github.io/TgWitness/pt/docs/archive/)

## Antes de começar.

**Esta página está vinculada ao Telegram?**

Não. Esta é uma página estática do projeto com exemplos fictícios e capturas de tela. O aplicativo propriamente dito é executado no seu computador ou servidor; o login é feito nesse local.

**É possível recuperar mensagens excluídas antes da captura?**

Não. O TgWitness retém o conteúdo que sua conta observou enquanto a coleta estava em andamento. Um instantâneo posterior do histórico não pode reconstruir edições perdidas ou mensagens excluídas.

**Todo o meu diário está criptografado?**

As credenciais da conta e os segredos de assinatura são armazenados em um cofre criptografado. As mensagens locais e os anexos requerem um disco ou volume criptografado. As exportações podem, opcionalmente, utilizar um arquivo ZIP AES-256 protegido por senha.

**Esta ferramenta é afiliada ao Telegram?**

Não. O TgWitness é um projeto independente que utiliza o Telethon, distribuído sob a Licença MIT. O senhor autoriza suas próprias contas, utilizando as configurações da API integrada ou seu próprio par de chaves de API.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore primeiro. Configure quando estiver pronto.

[Acesse a demonstração](https://phishdestroy.github.io/TgWitness/demo/?lang=pt)[Guia de configuração](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt)
