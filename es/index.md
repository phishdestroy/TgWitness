# Los mensajes cambian. Conserve lo que ha visto.

Canonical page: https://phishdestroy.github.io/TgWitness/es/

[Código abierto / v0.7.0](https://phishdestroy.github.io/TgWitness/es/docs/reference/changelog/)

Capture mensajes de Telegram, conserve sus modificaciones y exporte un registro firmado.

[Demostración disponible:](https://phishdestroy.github.io/TgWitness/demo/?lang=es)[Guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)

La demostración utiliza datos ficticios. No es necesario iniciar sesión en Telegram.

 [Captura con GitHub Actions (versión preliminar)](https://phishdestroy.github.io/TgWitness/es/docs/capture/) [Copia externa en S3: configuración y recuperación](https://phishdestroy.github.io/TgWitness/es/#s3)

UN MENSAJE A TRAVÉS DEL TIEMPO #0042

Northstar · InvestigaciónFuente ficticia / mensaje 42

1. **Mensaje observado:**09:41:02

   El informe comienza en 14:00.
2. **Edición conservada**09:43:18

   La sesión informativa comienza en 15:00.

   Se ha conservado la versión anterior
3. **Aviso de eliminación**10:06:45

   El contenido capturado permanece en su registro.

Tres observaciones. Una historia. EJEMPLO

El mensaje desaparece. El historial capturado permanece.

## Cada cambio registrado. Justo donde lo necesita.

Explore la interfaz con datos de demostración ficticios.

TgWitness / Chats guardadosSU ESPACIO DE TRABAJO DE OBSERVACIÓN

![Conversaciones de Telegram guardadas en el tema oscuro, con las modificaciones capturadas y los mensajes eliminados conservados en su contexto.](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Chats guardados: una vista de conversación familiar, con las modificaciones capturadas y los avisos de eliminación junto a los mensajes.

TgWitness / RegistroESPACIO DE TRABAJO LOCAL

![Registro con los mensajes observados, las modificaciones, los avisos de eliminación y los eventos cubiertos](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Registro: una cronología con función de búsqueda de lo que ha registrado su cuenta, incluidas las interrupciones.

TgWitness / Historial de edicionesESPACIO DE TRABAJO LOCAL

![Ventana emergente en la que se comparan las versiones capturadas, anterior y editada, de un mensaje](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Historial de ediciones: compare las versiones capturadas sin sobrescribir la observación anterior.

TgWitness / Exportaciones firmadasESPACIO DE TRABAJO LOCAL

![Espacio de trabajo de exportación que ofrece un archivo ZIP firmado, JSONL, CSV y un informe HTML sin conexión.](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Exportaciones firmadas: Llévese el registro consigo, con un manifiesto y un verificador independiente.

01 / CAPTURA

### Usted elige el alcance.

Chats seleccionados, una carpeta de Telegram o toda la cuenta. Un espacio de trabajo independiente para cada cuenta.

[Compare los modos de recopilación](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#scope)

02 / PRESERVAR

### Los cambios enriquecen la historia.

Las versiones «capturadas», los avisos de eliminación y las lagunas en la observación permanecen en el registro.

[Consulte la matriz de eventos](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#events)

03 / ENTREGA

### Un registro que viaja.

Archivo ZIP firmado, archivos conservados y un informe sin conexión. Protección con contraseña opcional.

[Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/exports/)

## Cambie un byte. La cadena se lo indicará.

Cada evento incluye un enlace al hash anterior y lleva una firma Ed25519.

![Los eventos capturados incluyen enlaces a hash anteriores, llevan firmas y se transmiten en un formato de exportación verificable.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modificación de un registro capturado altera su hash e invalida la verificación del registro vinculado.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un punto de control conservado por separado permite al destinatario comparar el registro exportado con una observación anterior.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Conozca qué establece cada mecanismo de verificación y cuáles son sus límites.

[Explore los ocho niveles de evidencia](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#levels)

## Listo para que lo revise otra persona.

Entregue las observaciones, los archivos y un informe HTML sin conexión en un único paquete firmado.

[Consulte el modelo de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

tgwitness-evidence.zipPAQUETE FIRMADO

- 01

  Observaciones originalesRegistros JSONL + tabla CSV
- 02

  Contexto legibleInforme HTML sin conexión + archivos multimedia conservados
- 03

  Verificación independienteManifiesto firmado + verificador independiente

Las firmas detectan la manipulación en relación con una clave de confianza. No demuestran el origen en Telegram ni garantizan una captura completa. El contenido del registro y los archivos multimedia requieren un almacenamiento cifrado que deberá proporcionar usted.

## Copias en S3. Comprobaciones externas.

Conserve copias cifradas y añada comprobaciones independientes.

Desactivado por defecto

### Copie todo a un almacenamiento compatible con S3

Exportaciones de registros, archivos, puntos de control con marca de tiempo y chats: se cifran antes de subirlos a AWS S3 o a un almacenamiento compatible.

**Configuración de almacenamiento y recuperación**

Cifrado del lado del cliente

`AES-256-GCM` cifra los objetos en este equipo. El proveedor recibe los objetos cifrados.

Copias programadas o manuales

Copie ahora o elija un intervalo de entre 1 y 1.440 minutos. Compruebe el progreso en el panel.

Object Lock

Seleccione los días de retención y un modo, siempre que el depósito lo admita. El panel indica si se ha confirmado la retención de un objeto cargado.

Recuperación verificada

Descargue la clave de cifrado y guárdela por separado. Restaure los datos en otro equipo; los archivos solo se publican tras su verificación.

![Panel completo de copias externas: punto final, región, depósito, claves de acceso, programación, controles de Object Lock y clave de recuperación](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

El panel completo con las opciones avanzadas desplegadas. No se muestran credenciales de almacenamiento.

Revistas y medios de comunicación`AES-256-GCM`Almacenamiento compatible con S3

[Configure S3 y restaure una copia](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3)[Consulte los detalles de la verificación:](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Qué no hace** No permite la recuperación de datos sin la clave de descifrado exportada ni sustituye a un testigo independiente.

### Notificaciones · Apprise

Alertas de problemas, cambios en los chats y resúmenes diarios a través de Apprise: aplicaciones de mensajería, correo electrónico o su propio webhook JSON.

**No realiza**: No envía el texto del mensaje a menos que active los extractos.

 [Configurar destinos de notificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/#notifications)

### Marcas de tiempo externas

Cálculo de hash de los puntos de control de marcas de tiempo con RFC 3161 y OpenTimestamps.

**Qué no hace** No considera un recibo pendiente del calendario como una marca de tiempo confirmada de Bitcoin.

 [Compruebe las pruebas de marca de tiempo:](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/)

### Testigo independiente

Un servidor independiente almacena las observaciones firmadas y puede publicar `TGW1` puntos de control.

**Qué no hace** No convierte dos espacios de trabajo en un mismo servidor colector en testigos independientes.

 [Configure un «witness»](https://phishdestroy.github.io/TgWitness/es/docs/witness/)

### Recuperación y lagunas evidentes

Reanudar tras el reinicio. Vuelve a comprobar y `coverage.json` muestre los mensajes recuperados y las lagunas.

**Qué no hace** No reconstruye todas las modificaciones que se han perdido ni todos los mensajes que han desaparecido.

 [Compruebe la continuidad y las lagunas](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#continuity)

## Su primer espacio de trabajo comienza aquí.

Pruebe primero la demo. Conecte una cuenta dedicada cuando esté listo. Windows, Linux, macOS o Docker.

[Lea la guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)

**Una sesión importada, un cliente en ejecución.**

No ejecute una clave TData/de sesión importada en Telegram Desktop y TgWitness al mismo tiempo. Telegram puede invalidar la autorización compartida (AUTH_KEY_DUPLICATED). Para un uso paralelo, cree un inicio de sesión independiente en TgWitness mediante teléfono o código QR.

[Lea la advertencia sobre la importación de sesiones](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es#session-warning)

**Échele un vistazo antes de conectarse.**

Pruebe el espacio de trabajo ficticio sin necesidad de tener una cuenta de Telegram.

[Acceda a la demostración en línea →](https://phishdestroy.github.io/TgWitness/demo/?lang=es)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Comandos de instalación local**

PASO 01

### Obtenga el código fuente.

[Descargue el archivo ZIP con el código fuente](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) y extráigalo, o clone el repositorio:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Para ejecutar el programa se requiere Python 3.11 o superior. El ejecutable de Windows ofrece la instalación en caso de que no se disponga de Python.

[Consulte las versiones](https://github.com/phishdestroy/TgWitness/releases)

¿No dispone de Python en Windows? [Descargue el paquete portátil](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), extráigalo y haga doble clic en «`TgWitness.cmd`».

PASO 02

### Elija cómo ejecutarla.

Haga doble clic en «`Start.cmd`» o ejecútelo en PowerShell:

```
.\Start.cmd
```

¿Solo está echando un vistazo? Haga doble clic en `scripts\Demo.cmd` para acceder a una demostración aislada. No es necesario iniciar sesión en Telegram.

Con Python 3.11+ y `venv`:

```
sh start.sh
```

Para abrir el registro ficticio, ejecute `sh start.sh --demo`.

Con Docker en ejecución y Compose 2.20 o superior instalado:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

El segundo comando muestra su token del panel privado. Guárdelo en su equipo.

Abra [127.0.0.1:8787](http://127.0.0.1:8787) tras el inicio.

Para instalaciones desde el código fuente, el token es `data/live/panel-token.txt`. Para iniciar sesión en Telegram, puedes utilizar la configuración de la API integrada o tu propio par de claves de [my.telegram.org](https://my.telegram.org). [Guía de configuración completa ↗](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/)

**TgWitness 0.7.0** [Novedades →](https://phishdestroy.github.io/TgWitness/es/docs/reference/changelog/) · [Características y limitaciones conocidas →](https://phishdestroy.github.io/TgWitness/es/docs/reference/features/)

## Instrucciones claras. Un siguiente paso útil.

[Explore las guías ↗](https://phishdestroy.github.io/TgWitness/es/docs/)

[### Modos, escenarios y niveles de prueba Cuatro modos de recopilación. Ocho niveles de verificación. Encuentre el flujo de trabajo adecuado para su caso.](https://phishdestroy.github.io/TgWitness/es/guides/modes.html)

[01 ### Conecte una cuenta Importación de datos de teléfono, códigos QR y sesiones compatibles.](https://phishdestroy.github.io/TgWitness/es/docs/accounts/)[02 ### Elija un proxy Listas públicas de MTProxy o su propia ruta.](https://phishdestroy.github.io/TgWitness/es/docs/proxies/)[03 ### Configurar un bot de TgWitness Puntos de control firmados en su canal de Telegram.](https://phishdestroy.github.io/TgWitness/es/docs/witness/)[04 ### Exportar y verificar Comparta el historial capturado y compruebe su integridad.](https://phishdestroy.github.io/TgWitness/es/docs/exports/)

## Trabaja con el archivo.

Cargar el historial, revisar las fuentes de IA, conectar un cliente MCP, reconocer los archivos multimedia guardados y enviar webhooks firmados.

Disponible en la fuente actual. La versión preliminar portátil 0.7.0 es anterior a estas herramientas.

[Explora el flujo de trabajo](https://phishdestroy.github.io/TgWitness/es/docs/archive/)

## Antes de empezar.

**¿Esta página está vinculada a Telegram?**

No. Se trata de una página estática del proyecto con ejemplos ficticios y capturas de pantalla. La aplicación real se ejecuta en su ordenador o servidor; el inicio de sesión se realiza allí.

**¿Puede recuperar mensajes eliminados antes de su captura?**

No. TgWitness conserva el contenido que su cuenta ha registrado mientras se estaba llevando a cabo la recopilación. Una instantánea posterior del historial no puede reconstruir las modificaciones que se hayan pasado por alto ni los mensajes eliminados.

**¿Está cifrado todo mi registro?**

Las credenciales de la cuenta y los secretos de firma se almacenan en una bóveda cifrada. Los mensajes y archivos adjuntos locales requieren un disco o volumen cifrado. Las exportaciones pueden utilizar, de forma opcional, un archivo ZIP con cifrado AES-256 protegido con contraseña.

**¿Está afiliada a Telegram?**

No. TgWitness es un proyecto independiente que utiliza Telethon, distribuido bajo la licencia MIT. Usted autoriza sus propias cuentas, ya sea mediante la configuración de la API integrada o utilizando su propio par de claves API.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore primero. Configúrela cuando esté listo.

[Demostración disponible:](https://phishdestroy.github.io/TgWitness/demo/?lang=es)[Guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)
