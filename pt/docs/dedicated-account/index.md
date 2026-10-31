# Utilize uma conta separada. Nunca utilize a sua conta principal.

Canonical page: https://phishdestroy.github.io/TgWitness/pt/docs/dedicated-account/

Leia antes de conectar uma conta

Nosso conselho de não utilizar sua conta principal não é uma brincadeira. É a realidade.

Conta principal

- Com seu próprio hash do aplicativo, 99% das contas são desconectadas
- É comum que contas sejam banidas apenas por apresentarem baixo nível de confiança
- Usar sua conta principal é uma ideia verdadeiramente estúpida

Uma conta adicional com pares de ID de API pública/hash de API

- Mais de um milhão de contas foram registradas por meio desses pares de ID de API/hash de API
- Esses pares de ID de API/hash de API estão ativos há mais de 5 anos
- Ninguém pode ver nenhum dos seus dados por meio desses pares de API

01

## Por que o senhor não deve utilizar sua conta principal

Essas informações são precisas. Sabemos exatamente onde estão as armadilhas desses problemas.

1. ### Com seu próprio hash do aplicativo, 99% das contas são desconectadas

   Fazer login no my.telegram.org a partir de uma conta à qual o senhor não tem acesso, para obter um hash do aplicativo, e, em seguida, qualquer solicitação feita por meio desse hash do aplicativo significa que há 99% de chance de a conta estar desconectada. O senhor pode verificar isso.
2. ### É comum que contas sejam banidas apenas por apresentarem baixo nível de confiança

   As contas são banidas simplesmente porque o Telegram não confia nelas, e tais banimentos são frequentes. O senhor também pode verificar isso. Usar sua própria conta é uma ideia realmente tola.
3. ### Chaves de sessão copiadas podem ser revogadas

   A execução simultânea de uma chave TData/sessão importada no Telegram Desktop e no TgWitness pode acionar o erro `AUTH_KEY_DUPLICATED`. O Telegram invalida essa autorização, de modo que ambas as cópias precisam de um novo login. Uma conta dedicada não impede que isso ocorra.

   Encerre completamente o cliente original e mantenha-o fechado enquanto utiliza sua sessão importada. Para uso paralelo, faça login no TgWitness por telefone ou QR para criar uma autorização separada; outros clientes autorizados separadamente podem permanecer conectados.

   [Leia o aviso sobre a importação de sessão](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=pt#session-warning)

Documentação do Telegram

- [Erros de logout: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Criação do hash do seu próprio aplicativo: obtenção do api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Por que o TgWitness funciona por meio de pares públicos de hash e ID de aplicativo

É por isso que desenvolvemos o TgWitness com base em pares públicos de hash de aplicativo/ID de aplicativo. Segundo nossa lógica, é menos provável que ocorram bloqueios com esses pares: mais de um milhão de contas do Telegram foram registradas por meio deles, e diversos programas diferentes funcionam com base neles. Segundo nossa lógica, isso é melhor do que trabalhar diretamente com um hash de aplicativo pessoal: esses pares estão ativos há mais de 5 anos, com certeza.

### Seu próprio novo par de ID de API/hash de API

Criado em my.telegram.org a partir da conta.

- Cerca de 99% dessas contas são desconectadas
- Um novo aplicativo, uma conta

### Pares de ID de API pública/hash de API do conjunto

Os mesmos pares de ID de API/hash de API que muitos programas utilizam.

- Mais de um milhão de contas registradas
- Muitos programas diferentes
- Esses pares de API vêm funcionando há mais de 5 anos

### Por que ninguém pode ver nenhum dos seus dados por meio desses pares de API

- #### O par da API é um nome, não uma chave

  O Telegram solicita o ID da API e o hash da API quando um programa se conecta e quando solicita um código de login. Esses dados identificam o aplicativo e não concedem acesso a nenhuma conta; a documentação do Telethon observa que um único par funciona com qualquer número de telefone.
- #### Sua chave de sessão nunca sai do seu servidor

  Ao fazer login, é criada uma chave de autorização por meio de uma troca de chaves Diffie–Hellman entre o seu TgWitness e o Telegram; a chave em si nunca é enviada. Documentação do Telegram: após a autorização, a chave passa a estar associada ao usuário, e todas as chamadas com essa chave são executadas em nome desse usuário. Outros programas com o mesmo par de chaves possuem suas próprias chaves e não podem utilizar a sua.
- #### O tráfego é criptografado com a sua chave

  Cada solicitação e resposta é criptografada com a chave de autorização da sessão, e não com o hash da API. Conhecer o hash da API não permite descriptografar nada.
- #### O proprietário de um par de ID de API/hash de API não vê nada

  O Telegram não dispõe de nenhum método que liste contas, sessões ou mensagens por ID de API. O proprietário de um par visualiza apenas as configurações do aplicativo em my.telegram.org.
- #### Apenas a sua conta tem acesso à identificação do aplicativo em questão

  Em Configurações → Dispositivos da sua própria conta, são listados o nome do aplicativo e o ID da API de cada sessão, além do dispositivo, endereço IP e datas. Ninguém mais tem acesso a essa lista.

Documentação do Telegram

- [Autorização do usuário: a chave fica vinculada ao usuário](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Criação da chave de autorização MTProto](https://core.telegram.org/mtproto/auth_key)
- [Criptografia MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [O que uma entrada de autorização (sessão) do Telegram contém](https://core.telegram.org/constructor/authorization)
- [Obtenção do api_id](https://core.telegram.org/api/obtaining_api_id)
- [Código-fonte aberto dos aplicativos do Telegram](https://telegram.org/apps#source-code)

Bibliotecas e tópicos de discussão

- [Telethon: fazendo login no Telegram](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: credenciais de API de aplicativos oficiais](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: o `api_hash` deve ser mantido em sigilo?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Os mesmos pares de ID de API/hash de API em outros programas 7

Os pares de ID de API/hash de API dos aplicativos oficiais do Telegram são públicos e estão integrados a muitos programas e bibliotecas independentes:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Uma publicação no fórum que lista os pares de ID de API/hash de API dos aplicativos oficiais do Telegram, publicada para o registro de contas

03

## Formas de criar uma conta adicional

Uma conta do Telegram precisa de um número de telefone para receber o código de login. Escolha de acordo com o tempo de validade desejado para a conta.

- Melhor opção

  ### SIM pré-pago ou eSIM

  ********

  Por quanto tempo isso dura

  Desde que você mantenha o saldo em dia

  Tenha em mente

  O mais confiável: o Telegram aceita melhor números de celular reais. Um número que a operadora retira de circulação é atribuído a outra pessoa.
- ### Um aplicativo com números de telefone virtuais

  ********

  Por quanto tempo isso dura

  Desde que o aplicativo mantenha o número de telefone

  Tenha em mente

  O Telegram pode recusar um número virtual, não enviar o código ou limitar a nova conta imediatamente; alguns aplicativos recuperam números que não são utilizados.
- ### Aluguel de número de telefone

  ********

  Por quanto tempo isso dura

  Para o período de aluguel

  Tenha em mente

  Quando terminar, o número passa para o próximo cliente.
- ### Ativação única

  ********

  Por quanto tempo isso dura

  Apenas um código de login

  Tenha em mente

  O número retorna ao pool imediatamente, muitas vezes acompanhado de um histórico de proprietários anteriores. Defina a senha da nuvem antes de qualquer outra coisa.

Quem quer que venha a possuir o número posteriormente poderá solicitar um código de login. Uma senha na nuvem (verificação em duas etapas) impede que essa pessoa faça login; sem ela, a conta pertence ao próximo proprietário do número.

Documentação do Telegram

- [Perguntas frequentes sobre spam: números virtuais e proprietários anteriores](https://telegram.org/faq_spam)
- [Verificação em duas etapas](https://core.telegram.org/api/srp)

### Números +888 alugados (Fragment)

Alguns mercados e serviços oferecem o aluguel temporário dos números oficiais +888 do Telegram por meio da Fragment.

Preço aproximado: US$ 20 por dia.

- O senhor pode registrar uma conta diretamente no Telegram Web ou no Telegram Desktop.
- O senhor pode excluir contas associadas ao número e criar novas contas.
- Essas contas geralmente passam por menos verificações antifraude, mas não oferecem imunidade nem privilégios especiais.

O número não é seu. Após o término do aluguel, o proprietário poderá reivindicá-lo. Defina uma senha de nuvem imediatamente e não considere a conta como de longo prazo.

Ter o número +888 em seu nome ou utilizar um chip pré-pago sob seu controle continua sendo a opção mais confiável.

### Contas prontas disponíveis em mercados online

Algumas plataformas de comércio (por exemplo, G2G ou Z2U) vendem contas do Telegram prontas — novas, antigas ou com arquivos de sessão.

- [G2G: listagens de contas do Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Listas de contas do Telegram](https://www.z2u.com/telegram/accounts-5-15140)

NUNCA UTILIZE SUA CONTA PRINCIPAL! Uma conta dedicada obtida dessa forma ainda é mais segura do que inserir sua conta principal do Telegram no TgWitness.

#### Avisos antes da compra

- Isso viola os Termos de Serviço do Telegram.
- Muitas contas são registradas em massa (registro automático) ou possuem um histórico desconhecido.
- Alguns vendedores ainda podem ter acesso à recuperação.
- Contas provenientes desses mercados são frequentemente banidas ou restritas posteriormente.
- Evite marketplaces que vendam abertamente programas de roubo de senhas, ferramentas de phishing ou contas claramente roubadas.
- A compra de uma conta — mesmo que anunciada como de “registro automático” — em plataformas que vendem abertamente ferramentas de phishing, programas de roubo de dados, sessões roubadas ou contas violam não apenas os Termos de Serviço do Telegram, mas também as leis da maioria dos países. Isso pode, posteriormente, invalidar suas evidências. Escolha com cuidado.

#### Caso utilize esta opção

1. Trate a conta como descartável.
2. Encerre todas as outras sessões, defina uma senha na nuvem e altere os métodos de recuperação imediatamente.
3. Utilize de 2 a 3 contas de diferentes provedores ou contas que o(a) senhor(a) mesmo(a) tenha registrado.

**Premium, exclusão e o prazo de sete dias**

Se a conta tiver o Premium, alguém com acesso ao número de telefone não poderá excluir a conta imediatamente. O(a) senhor(a) receberá uma notificação e terá sete dias antes da exclusão.

Isso é importante porque sua investigação depende da conta: o senhor tem tempo para preparar uma substituição.

**Contas novas e credenciais de API**

Caso obtenha e utilize seu próprio api_id/api_hash de uma conta nova que você mesmo tenha registrado usando um número de um serviço de SMS, a conta será desconectada na primeira solicitação de API ou autorização de sessão. Tenha isso em mente ao planejar uma investigação.

04

## Criação da conta

Desde a obtenção de um número de telefone até o primeiro chat registrado.

1. ### Obtenha um número de telefone

   Um SIM pré-pago ou eSIM quando a conta precisa ter longa duração; um aluguel ou uma ativação única para um trabalho de curta duração. Os serviços estão listados abaixo.
2. ### Cadastre-se separadamente da sua conta principal

   Cadastre-se no aplicativo oficial do Telegram em um dispositivo separado, emulador ou perfil de celular, e não junto à sua conta principal.
3. ### Proteja a conta com uma senha na nuvem

   Defina imediatamente uma senha para a nuvem e um e-mail de recuperação que não seja utilizado em nenhum outro lugar.
4. ### Restrinja as configurações de privacidade da conta

   Número de telefone: **“Ninguém**”, “Encontre-me pelo meu número”, **“Meus contatos**”, “Visto pela última vez”, “Fotos de perfil” e “Biografia”: **“Ninguém”** ou **“Meus contatos”**; desative a sincronização de contatos.
5. ### Evite que a conta se autodestrua

   Defina a autodestruição da conta para o período mais longo, de modo que uma interrupção do TgWitness não resulte na perda da sua conta.
6. ### Crie um perfil neutro para a conta

   Sem nome, foto, nome de usuário ou biografia de suas outras contas, nem contatos pessoais.
7. ### Aqueça a nova conta aos poucos

   No início, participe apenas de alguns chats por dia. As novas contas que se apressam são as primeiras a sofrerem restrições.
8. ### Não compartilhe nada com bots

   Nunca clique em “Compartilhar número de telefone” ou “Compartilhar localização” para um bot. Abra links e Mini Apps por meio de uma VPN ou proxy nesse dispositivo.
9. ### Conecte a conta ao TgWitness

   Em seu próprio espaço de trabalho, conecte-se por meio de **Conta → Código QR** e, em seguida, selecione **Fontes → Modo de investigação**. O aplicativo é onde você atua; o TgWitness é o registro.

Documentação do Telegram

- [Verificação em duas etapas](https://core.telegram.org/api/srp)
- [Configurações de privacidade](https://core.telegram.org/api/privacy)
- [Autodestruição da conta em caso de inatividade](https://core.telegram.org/method/account.setAccountTTL)

05

## Serviços de números de telefone

Estas são as opções para começar. Os países, os preços e a aceitação de um determinado número pelo Telegram mudam com frequência; portanto, verifique antes de efetuar o pagamento.

### SIM pré-pago e eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Pré-pago

  Plano PayGo, muito econômico
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Pré-pago
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Pré-pago
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Pré-pago
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Aplicativos com números de telefone virtuais 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Apenas nos EUA; o cadastro requer um número de telefone dos EUA
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  O número será recuperado caso o senhor não o utilize
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Outros países
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Serviço pago

  Com um período de teste
- [Hushedhushed.com](https://hushed.com)

  - Muitos países
  - Serviço pago

  Preço baixo
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Números de celular europeus em um aplicativo
- [Sonetelsonetel.com](https://sonetel.com)

  - Muitos países
  - Um número gratuito
- [Zadarmazadarma.com](https://zadarma.com)

  - Muitos países

  Números de telefone virtuais

### Aluguel de números de telefone e ativações únicas 12

O aluguel de um número de telefone garante que ele permaneça à sua disposição por semanas ou meses. Uma ativação única fornece um único código de login: defina a senha da nuvem imediatamente após o registro.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Aluguel de número
  - Ativações únicas
- [SMSPVAsmspva.com](https://smspva.com)

  - Aluguel de número
  - Ativações únicas
- [5SIM5sim.net](https://5sim.net)

  - Aluguel de número
  - Ativações únicas
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Aluguel de número
  - Ativação única
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Aluguel de número
  - Ativações únicas
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Aluguel de número
  - Ativações únicas
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Aluguel de número
  - Ativações únicas
- [365SMS365sms.org](https://365sms.org)

  - Aluguel de número
  - Ativações únicas
- [SIMSMSsimsms.org](https://simsms.org)

  - Aluguel de número
  - Ativações únicas
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Ativação única
- [SMS-MANsms-man.com](https://sms-man.com)

  - Ativação única
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Ativação única
