# Utilice una cuenta independiente. Nunca utilice su cuenta principal.

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/dedicated-account/

Lea esto antes de vincular una cuenta

Nuestro consejo de que no utilice su cuenta principal no es una broma. Es una realidad.

Cuenta principal

- Con su propio «app hash», el 99 % de las cuentas se desconectan
- Son frecuentes las suspensiones de cuentas simplemente por un nivel bajo de confianza
- Utilizar su cuenta principal es una idea verdaderamente estúpida

Una cuenta adicional con pares de ID de API pública/hash de API

- Se han registrado más de un millón de cuentas a través de estos pares de ID de API/hash de API
- Estos pares de ID de API/hash de API llevan más de cinco años en funcionamiento
- Nadie puede ver ninguno de sus datos a través de estos pares de API

01

## Por qué no debe utilizar su cuenta principal

Se trata de información precisa. Sabemos exactamente dónde residen las dificultades de estos problemas.

1. ### Con su propio «app hash», el 99 % de las cuentas se desconectan

   Si inicia sesión en my.telegram.org desde una cuenta a la que no tiene acceso para obtener un hash de la aplicación, y a continuación realiza cualquier solicitud a través de dicho hash, existe un 99 % de probabilidades de que la cuenta quede desconectada. Puede comprobarlo.
2. ### Son frecuentes las suspensiones de cuentas simplemente por un nivel bajo de confianza

   Las cuentas son bloqueadas simplemente porque Telegram no confía en ellas, y dichos bloqueos son frecuentes. También puede comprobarlo usted mismo. Utilizar su propia cuenta es una idea realmente estúpida.
3. ### Las claves de sesión copiadas pueden revocarse

   El uso simultáneo de una clave TData/de sesión importada en Telegram Desktop y TgWitness puede provocar el error `AUTH_KEY_DUPLICATED`. Telegram invalida dicha autorización, por lo que ambas copias necesitan un nuevo inicio de sesión. Disponer de una cuenta dedicada no evita que esto ocurra.

   Cierre completamente el cliente original y manténgalo cerrado mientras utiliza su sesión importada. Para un uso paralelo, inicie sesión en TgWitness mediante teléfono o código QR para crear una autorización independiente; los demás clientes con autorización independiente pueden permanecer conectados.

   [Lea la advertencia sobre la importación de sesiones](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es#session-warning)

Documentación de Telegram

- [Errores al cerrar sesión: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Creación de su propio hash de aplicación: obtención del api_id](https://core.telegram.org/api/obtaining_api_id)

02

## Por qué TgWitness funciona mediante pares públicos de hash de aplicación e ID de aplicación

Por ello hemos desarrollado TgWitness basándonos en pares públicos de hash de aplicación e ID de aplicación. Según nuestra lógica, con ellos es menos probable que se produzcan bloqueos: se han registrado más de un millón de cuentas de Telegram a través de estos pares, y muchos programas diferentes funcionan mediante ellos. Según nuestra lógica, esto es mejor que trabajar directamente con un hash de aplicación personal: estos pares llevan en funcionamiento más de cinco años con toda seguridad.

### Su propio par nuevo de ID de API/hash de API

Creado en my.telegram.org desde la cuenta.

- Alrededor del 99 % de estas cuentas se desconectan
- Una nueva aplicación, una cuenta

### Pares de ID de API pública/hash de API del conjunto

Se trata de los mismos pares de ID de API/hash de API que utilizan muchos programas.

- Más de un millón de cuentas registradas
- Numerosos programas diferentes
- Estos pares de API llevan más de cinco años en funcionamiento.

### Por qué nadie puede ver ninguno de sus datos a través de estos pares de API

- #### El par de la API es un nombre, no una clave

  Telegram solicita el ID de la API y el hash de la API cuando un programa se conecta y cuando solicita un código de inicio de sesión. Estos identifican la aplicación y no otorgan acceso a ninguna cuenta; la documentación de Telethon señala que un par de estos datos funciona con cualquier número de teléfono.
- #### Su clave de sesión nunca sale de su servidor

  Al iniciar sesión se crea una clave de autorización mediante un intercambio Diffie-Hellman entre su TgWitness y Telegram; la clave en sí nunca se envía. Según la documentación de Telegram: tras la autorización, la clave queda asociada al usuario, y cada llamada realizada con esta clave se ejecuta en nombre de dicho usuario. Otros programas con el mismo par de claves disponen de sus propias claves y no pueden utilizar la suya.
- #### El tráfico se cifra con su clave

  Cada solicitud y respuesta se cifra con la clave de autorización de la sesión, no con el hash de la API. Conocer el hash de la API no permite descifrar nada.
- #### El propietario de un par de ID de API/hash de API no ve nada

  Telegram no dispone de ningún método que permita listar cuentas, sesiones o mensajes por ID de API. El propietario de un par solo puede ver la configuración de su aplicación en my.telegram.org.
- #### Solo su cuenta puede ver de qué aplicación se trata

  En «Configuración» → «Dispositivos» de su propia cuenta se muestra una lista con el nombre de la aplicación y el ID de API de cada sesión, así como el dispositivo, la dirección IP y las fechas. Nadie más tiene acceso a esta lista.

Documentación de Telegram

- [Autorización del usuario: la clave queda vinculada al usuario](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Creación de la clave de autorización MTProto](https://core.telegram.org/mtproto/auth_key)
- [Cifrado MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Qué contiene una entrada de autorización (sesión) de Telegram](https://core.telegram.org/constructor/authorization)
- [Obtención del api_id](https://core.telegram.org/api/obtaining_api_id)
- [Código fuente de las aplicaciones de Telegram](https://telegram.org/apps#source-code)

Bibliotecas y hilos de debate

- [Telethon: iniciar sesión en Telegram](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: credenciales de API de las aplicaciones oficiales](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: ¿debería mantenerse en secreto el «api_hash»?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Los mismos pares de ID de API/hash de API en otros programas 7

Los pares de ID de API/hash de API de las aplicaciones oficiales de Telegram son públicos y están integrados en numerosos programas y bibliotecas independientes:

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

  Una publicación en el foro en la que se enumeran los pares de ID de API y hash de API de las aplicaciones oficiales de Telegram, publicada con el fin de registrar cuentas

03

## Formas de crear una cuenta adicional

Una cuenta de Telegram requiere un número de teléfono en el que se reciba el código de inicio de sesión. Elija en función del tiempo que deba permanecer activa la cuenta.

- La mejor opción

  ### SIM de prepago o eSIM

  ********

  Cuánto tiempo dura

  Siempre y cuando mantenga su saldo al día

  Tenga en cuenta

  Lo más fiable: Telegram acepta mejor los números de móvil reales. Un número que la operadora retira se asigna a otra persona.
- ### Una aplicación con números de teléfono virtuales

  ********

  Cuánto tiempo dura

  Siempre que la aplicación conserve el número de teléfono

  Tenga en cuenta

  Telegram puede rechazar un número virtual, no enviar el código o limitar la nueva cuenta de inmediato; algunas aplicaciones recuperan los números que no se utilizan.
- ### Alquiler de números de teléfono

  ********

  Cuánto tiempo dura

  En cuanto al periodo de alquiler

  Tenga en cuenta

  Cuando finaliza, el número pasa al siguiente cliente.
- ### Activación única

  ********

  Cuánto tiempo dura

  Solo un código de inicio de sesión

  Tenga en cuenta

  El número vuelve al fondo común de inmediato, a menudo con un historial de propietarios anteriores. Configure la contraseña de la nube antes de nada.

Quien obtenga el número de teléfono posteriormente podrá solicitar un código de inicio de sesión. Una contraseña en la nube (verificación en dos pasos) impide que esa persona inicie sesión; sin ella, la cuenta pasa a pertenecer al siguiente propietario del número.

Documentación de Telegram

- [Preguntas frecuentes sobre el spam: números virtuales y propietarios anteriores](https://telegram.org/faq_spam)
- [Verificación en dos pasos](https://core.telegram.org/api/srp)

### Números +888 alquilados (Fragment)

Algunos mercados y servicios ofrecen el alquiler temporal de los números oficiales +888 de Telegram a través de Fragment.

Precio aproximado: 20 dólares estadounidenses al día.

- Puede registrar una cuenta directamente en Telegram Web o en Telegram Desktop.
- Puede eliminar cuentas del número y crear otras nuevas.
- Estas cuentas suelen estar sujetas a menos controles antifraude, pero no otorgan inmunidad ni privilegios especiales.

El número no es suyo. Una vez finalizado el alquiler, el propietario podrá reclamarlo. Establezca una contraseña de la nube de inmediato y no considere la cuenta como algo a largo plazo.

Seguir siendo el titular del número +888 o utilizar una tarjeta SIM de prepago que usted controle sigue siendo más fiable.

### Cuentas ya creadas procedentes de mercados online

Algunas plataformas de venta (por ejemplo, G2G o Z2U) comercializan cuentas de Telegram ya creadas: nuevas, con antigüedad o con archivos de sesión.

- [G2G: listados de cuentas de Telegram](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Listados de cuentas de Telegram](https://www.z2u.com/telegram/accounts-5-15140)

¡NUNCA UTILICE SU CUENTA PRINCIPAL! Una cuenta específica obtenida de esta manera sigue siendo más segura que introducir su cuenta principal de Telegram en TgWitness.

#### Advertencias antes de la compra

- Esto incumple las Condiciones de servicio de Telegram.
- Muchas cuentas se han registrado de forma masiva (registro automático) o tienen un historial desconocido.
- Es posible que algunos vendedores sigan teniendo acceso de recuperación.
- Las cuentas de dichos mercados suelen ser bloqueadas o restringidas posteriormente.
- Evite los mercados en los que se vendan abiertamente programas de robo de credenciales, herramientas de phishing o cuentas claramente robadas.
- La compra de una cuenta —incluso una anunciada como de «registro automático»— en plataformas que venden abiertamente herramientas de phishing, programas de robo de datos, sesiones robadas o cuentas infringes no solo las Condiciones de servicio de Telegram, sino también la legislación de la mayoría de los países. Esto puede invalidar posteriormente sus pruebas. Elija con cuidado.

#### Si utiliza esta opción

1. Trate la cuenta como si fuera desechable.
2. Cierre todas las demás sesiones, establezca una contraseña en la nube y cambie los métodos de recuperación de inmediato.
3. Utilice entre 2 y 3 cuentas de diferentes proveedores o cuentas que haya registrado usted mismo.

**Premium, la eliminación y el plazo de siete días**

Si la cuenta dispone de Premium, una persona con acceso al número de teléfono no podrá eliminar la cuenta de forma inmediata. Recibirá una notificación y dispondrá de siete días antes de que se produzca la eliminación.

Esto es importante porque su investigación depende de la cuenta: dispone de tiempo para preparar un sustituto.

**Cuentas nuevas y credenciales de API**

Si obtiene y utiliza su propio «api_id»/«api_hash» de una cuenta nueva que haya registrado usted mismo utilizando un número de un servicio de SMS, la cuenta se cerrará en la primera solicitud de API o autorización de sesión. Tenga esto en cuenta a la hora de planificar una investigación.

04

## Creación de la cuenta

Desde la obtención de un número de teléfono hasta el primer chat registrado.

1. ### Obtenga un número de teléfono

   Una tarjeta SIM de prepago o una eSIM cuando la cuenta deba tener una larga vigencia; un alquiler o una activación única para un trabajo de corta duración. A continuación se enumeran los servicios.
2. ### Regístrese con una cuenta independiente de su cuenta principal

   Regístrese en la aplicación oficial de Telegram en un dispositivo independiente, un emulador o un perfil de teléfono, no junto a su cuenta principal.
3. ### Proteja la cuenta con una contraseña en la nube

   Establezca de inmediato una contraseña para la nube y una dirección de correo electrónico de recuperación que no utilice en ningún otro sitio.
4. ### Restrinja la configuración de privacidad de la cuenta

   Número de teléfono: **«Nadie**», «Encuéntreme por mi número», **«Mis contactos**», «Última conexión», «Fotos de perfil» y «Biografía»: **«Nadie»** o **«Mis contactos»**; desactive la sincronización de contactos.
5. ### Evite que la cuenta se autodestruya

   Configure la autodestrucción de la cuenta en el plazo más largo posible, de modo que, si TgWitness deja de funcionar, no pierda la cuenta.
6. ### Configure un perfil neutro para la cuenta

   No se incluyen nombres, fotos, nombres de usuario ni biografías de sus otras cuentas, ni contactos personales.
7. ### Deje que la nueva cuenta se «caliente»

   Al principio, únase solo a unos pocos chats al día. Las cuentas nuevas que se precipitan son las primeras en sufrir restricciones.
8. ### No comparta nada con los bots

   No pulse nunca «Compartir número de teléfono» ni «Compartir ubicación» en un bot. Abra los enlaces y las miniaplicaciones a través de una VPN o un proxy en ese dispositivo.
9. ### Conecte la cuenta a TgWitness

   En su propio espacio de trabajo, conéctese a través de **Cuenta → Código QR** y, a continuación, pulse **Fuentes → Modo de investigación**. La aplicación es donde usted actúa; TgWitness es el registro.

Documentación de Telegram

- [Verificación en dos pasos](https://core.telegram.org/api/srp)
- [Configuración de privacidad](https://core.telegram.org/api/privacy)
- [Autodestrucción de la cuenta en caso de inactividad](https://core.telegram.org/method/account.setAccountTTL)

05

## Servicios de números de teléfono

Estas son las opciones con las que puede empezar. Los países, los precios y la aceptación de un número concreto por parte de Telegram cambian con frecuencia, por lo que le recomendamos que lo compruebe antes de realizar el pago.

### Tarjetas SIM de prepago y eSIM 11

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
  - Prepago

  Plan PayGo, muy económico
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prepago
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prepago
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prepago
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Aplicaciones con números de teléfono virtuales 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Solo para EE. UU.; para registrarse es necesario disponer de un número de teléfono estadounidense.
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  El número se recupera si no lo utiliza.
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
  - Otros países
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
  - Servicio de pago

  Con un periodo de prueba
- [Hushedhushed.com](https://hushed.com)

  - Muchos países
  - Servicio de pago

  Precio reducido
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

  Números de móvil europeos en una aplicación
- [Sonetelsonetel.com](https://sonetel.com)

  - Muchos países
  - Un número gratuito
- [Zadarmazadarma.com](https://zadarma.com)

  - Muchos países

  Números de teléfono virtuales

### Alquiler de números de teléfono y activaciones de un solo uso 12

Al alquilar un número de teléfono, este seguirá siendo suyo durante semanas o meses. Una activación de un solo uso proporciona un único código de inicio de sesión: establezca la contraseña de la nube inmediatamente después de registrarse.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Alquiler de números
  - Activaciones de un solo uso
- [SMSPVAsmspva.com](https://smspva.com)

  - Alquiler de números
  - Activaciones de un solo uso
- [5SIM5sim.net](https://5sim.net)

  - Alquiler de números
  - Activaciones de un solo uso
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Alquiler de números
  - Activación de un solo uso
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Alquiler de números
  - Activaciones de un solo uso
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Alquiler de números
  - Activaciones de un solo uso
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Alquiler de números
  - Activaciones de un solo uso
- [365SMS365sms.org](https://365sms.org)

  - Alquiler de números
  - Activaciones de un solo uso
- [SIMSMSsimsms.org](https://simsms.org)

  - Alquiler de números
  - Activaciones de un solo uso
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Activación de un solo uso
- [SMS-MANsms-man.com](https://sms-man.com)

  - Activación de un solo uso
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Activación de un solo uso
