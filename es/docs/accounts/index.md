# Conecte una cuenta

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/accounts/

Cada espacio de trabajo alberga una cuenta, su registro y su clave de firma.

## Elija cómo iniciar sesión

Abra **una cuenta**, añada un espacio de trabajo y acceda a su configuración de conexión. Utilice una cuenta específica para la observación.

- **Código QR:** escanéelo desde los ajustes del dispositivo en Telegram y confirme el nuevo inicio de sesión.
- **Número de teléfono:** introduzca el número, el código que envía Telegram y su contraseña de verificación en dos pasos, si está activada.
- **Importación de sesiones:** importe una sesión compatible o datos de Telegram Desktop que le pertenezcan.

Elija un perfil de API integrado o introduzca su propio ID de API y hash. Un perfil de API identifica al cliente; no inicia sesión en una cuenta ni hace que la conexión sea anónima.

**¿Necesita primero un proxy?**

Puede [elegir y probar la ruta de conexión](https://phishdestroy.github.io/TgWitness/es/docs/proxies/) antes de iniciar sesión. Cada cuenta tiene su propia ruta.

## Elija qué desea supervisar

1. Abra la lista de fuentes y seleccione los chats, grupos o canales que necesite.
2. Revise la configuración de la recopilación, incluidos los archivos multimedia, antes de iniciar la observación.
3. Inicie el recopilador y compruebe su conexión y su actividad reciente.

La cuenta debe poder acceder a la fuente. Los distintos roles pueden ver diferentes eventos; el registro refleja lo que recibió dicha cuenta.

Para un caso que abarque toda la cuenta, utilice **«Fuentes» → «Ámbito de observación» → «Modo de investigación**», revise la configuración y pulse **«Guardar ámbito**». La [guía completa de la investigación](https://phishdestroy.github.io/TgWitness/es/docs/cases/) abarca todos los tipos de chats visibles, el historial antiguo, los perfiles de los usuarios, las referencias entre chats y la transferencia de pruebas.

## Compruebe la ruta completa

En un grupo de prueba que usted controle, envíe un mensaje único desde otra cuenta, edítelo y elimínelo. Confirme los tres eventos en el registro, y a continuación [exporte y verifique](https://phishdestroy.github.io/TgWitness/es/docs/exports/) el registro.

El estado «conectado» confirma la conexión. Un mensaje de prueba capturado confirma que un evento concreto ha llegado a este espacio de trabajo.

## Añada otra cuenta

Cree otro espacio de trabajo en **«Cuentas»** y repita la configuración. Conserve la huella digital de la clave de firma de cada cuenta para poder identificar sus exportaciones posteriormente.
