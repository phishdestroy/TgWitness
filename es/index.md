# Los mensajes cambian． Conserve lo que ha visto．

Canonical page: https://phishdestroy.github.io/TgWitness/es/

[Código abierto ／ v0.9.1](https://phishdestroy.github.io/TgWitness/es/docs/reference/changelog/)

Exporta chats de Telegram， conserva su historial y comparte un archivo firmado que otros puedan verificar．

[Demostración disponible：](https://phishdestroy.github.io/TgWitness/demo/?lang=es)[Guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)

Datos ficticios， sin iniciar sesión en Telegram．

 [Exportar una cuenta o chats seleccionados](https://phishdestroy.github.io/TgWitness/es/docs/reference/account-export/) [Captura con GitHub Actions （versión preliminar）](https://phishdestroy.github.io/TgWitness/es/docs/capture/) [Copia externa en S3： configuración y recuperación](https://phishdestroy.github.io/TgWitness/es/#s3)

UN MENSAJE A TRAVÉS DEL TIEMPO ＃0042

Northstar · InvestigaciónFuente ficticia ／ mensaje 42

1. **Mensaje observado：**09：41：02

   El informe comienza en 14：00．
2. **Edición conservada**09：43：18

   La sesión informativa comienza en 15：00．

   Se ha conservado la versión anterior
3. **Aviso de eliminación**10：06：45

   El contenido capturado permanece en su registro．

Tres observaciones． Una historia． EJEMPLO

El mensaje desaparece． El historial capturado permanece．

## Cada cambio registrado． Justo donde lo necesita．

La interfaz real， con datos inventados．

TgWitness ／ Chats guardadosSU ESPACIO DE TRABAJO DE OBSERVACIÓN

![Conversaciones de Telegram guardadas en el tema oscuro， con las modificaciones capturadas y los mensajes eliminados conservados en su contexto．](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Chats guardados Parece un chat normal， con las ediciones y los borrados justo al lado de los mensajes．

TgWitness ／ RegistroESPACIO DE TRABAJO LOCAL

![Registro con los mensajes observados， las modificaciones， los avisos de eliminación y los eventos cubiertos](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Diario Todo lo que vio su cuenta， con búsqueda y con los huecos marcados．

TgWitness ／ Historial de edicionesESPACIO DE TRABAJO LOCAL

![Ventana emergente en la que se comparan las versiones capturadas， anterior y editada， de un mensaje](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Historial de ediciones Versión antigua y nueva lado a lado， nada se sobrescribe．

TgWitness ／ Exportaciones firmadasESPACIO DE TRABAJO LOCAL

![Espacio de trabajo de exportación que ofrece un archivo ZIP firmado， JSONL， CSV y un informe HTML sin conexión．](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Exportaciones firmadas Llévese el diario， firmado y con su propio verificador．

Sigue el recorrido de un registro guardado a través del [«Case Board»](https://phishdestroy.github.io/TgWitness/es/docs/case-board/)， [el diseño del informe](https://phishdestroy.github.io/TgWitness/es/docs/reports/) y una [copia para compartir](https://phishdestroy.github.io/TgWitness/es/docs/handover/)． [Revisa los grupos de cuentas](https://phishdestroy.github.io/TgWitness/es/docs/groups/) en conjunto．

01 ／ CAPTURA

### Usted elige el alcance．

Unos pocos chats， una carpeta o la cuenta entera． Cada cuenta tiene su propio espacio．

[Compare los modos de recopilación](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#scope)

02 ／ PRESERVAR

### Los cambios enriquecen la historia．

Versiones， borrados y huecos se quedan en el diario．

[Consulte la matriz de eventos](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#events)

03 ／ ENTREGA

### Un registro que viaja．

ZIP firmado， archivos e informe sin conexión． Contraseña opcional．

[Exportar y verificar](https://phishdestroy.github.io/TgWitness/es/docs/exports/)

## Si se cambia un solo byte，
la verificación lo detectará．

Cada evento incluye un enlace al hash anterior y lleva una firma Ed25519．

![Los eventos capturados incluyen enlaces a hash anteriores， llevan firmas y se transmiten en un formato de exportación verificable．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![La modificación de un registro capturado altera su hash e invalida la verificación del registro vinculado．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Un punto de control conservado por separado permite al destinatario comparar el registro exportado con una observación anterior．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Sigue las comprobaciones desde un hash de archivo hasta un punto de control conservado por separado．

[Explore los ocho niveles de evidencia](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#levels)

## Listo para que lo revise otra persona．

Mensajes， archivos e informe sin conexión en un solo paquete firmado．

[Consulte el modelo de pruebas](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/)

tgwitness-evidence.zipPAQUETE FIRMADO

- 01

  Observaciones originalesRegistros JSONL ＋ tabla CSV
- 02

  Contexto legibleInforme HTML sin conexión ＋ archivos multimedia conservados
- 03

  Verificación independienteManifiesto firmado ＋ verificador independiente

El destinatario lo comprueba todo con su clave， y un punto de control guardado en otro sitio demuestra que nada se ha reescrito desde entonces． [Cómo funcionan las comprobaciones．](https://phishdestroy.github.io/TgWitness/es/docs/concepts/#layers)

## Copias en S3． Comprobaciones externas．

Conserve copias cifradas y añada comprobaciones independientes．

Desactivado por defecto

### Copie todo a un almacenamiento compatible con S3

Diario， archivos， puntos de control y exportaciones de chats， cifrados antes de ir a S3．

**Configuración de almacenamiento y recuperación**

Cifrado del lado del cliente

`AES-256-GCM` en su máquina． El proveedor solo ve texto cifrado．

Copias programadas o manuales

Copie ahora o cada 1 a 1440 minutos， con el progreso en el panel．

Object Lock

Elija los días y el modo de retención； el panel comprueba que de verdad se aplicaron．

Recuperación verificada

Guarde la clave aparte． Restaure donde quiera： los archivos solo salen tras la verificación．

![Panel completo de copias externas： punto final， región， depósito， claves de acceso， programación， controles de Object Lock y clave de recuperación](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

El panel completo con las opciones avanzadas desplegadas． No se muestran credenciales de almacenamiento．

Revistas y medios de comunicación`AES-256-GCM`Almacenamiento compatible con S3

[Configure S3 y restaure una copia](https://phishdestroy.github.io/TgWitness/es/docs/exports/#s3)[Consulte los detalles de la verificación：](https://phishdestroy.github.io/TgWitness/es/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Clave de recuperación** Guárdela aparte： sin ella la copia no se puede leer．

### Notificaciones · Apprise

Problemas， cambios en chats y un resumen diario a mensajería， correo o su propio webhook．

**Elija qué compartir** Sin texto de mensajes a menos que lo active．

 [Configurar destinos de notificación](https://phishdestroy.github.io/TgWitness/es/docs/reference/operations/#notifications)

### Marcas de tiempo externas

Cálculo de hash de los puntos de control de marcas de tiempo con RFC 3161 y OpenTimestamps．

**Siga el resultado** Compruebe la respuesta de la TSA o actualice el recibo de OpenTimestamps a una prueba en Bitcoin．

 [Compruebe las pruebas de marca de tiempo：](https://phishdestroy.github.io/TgWitness/es/docs/reference/timestamp/)

### Testigo independiente

Un servidor independiente almacena las observaciones firmadas y puede publicar `TGW1` puntos de control．

**Separe la referencia** Ejecútelo en otro host， con su propia clave y su propio diario．

 [Configure un «witness»](https://phishdestroy.github.io/TgWitness/es/docs/witness/)

### Recuperación y lagunas evidentes

Reanudar tras el reinicio． Vuelve a comprobar y `coverage.json` muestre los mensajes recuperados y las lagunas．

**Revise el intervalo** Mensajes recuperados y huecos registrados， lado a lado．

 [Compruebe la continuidad y las lagunas](https://phishdestroy.github.io/TgWitness/es/guides/modes.html#continuity)

## Su primer espacio de trabajo comienza aquí．

Pruebe primero la demo y conecte una cuenta de repuesto cuando esté listo．
Windows， Linux， macOS o Docker．

[Lea la guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)

**Una sesión importada， un cliente en ejecución．**

No use una TData o sesión importada en Telegram Desktop y en TgWitness a la vez： Telegram puede invalidar ambas （AUTH_KEY_DUPLICATED）． ¿Necesita las dos？ Inicie sesión en TgWitness por separado， con teléfono o QR．

[Lea la advertencia sobre la importación de sesiones](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es#session-warning)

**Échele un vistazo antes de conectarse．**

Pruebe el espacio de trabajo ficticio sin necesidad de tener una cuenta de Telegram．

[Acceda a la demostración en línea →](https://phishdestroy.github.io/TgWitness/demo/?lang=es)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Comandos de instalación local**

PASO 01

### Obtenga el código fuente．

[Descargue el archivo ZIP con el código fuente](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) y extráigalo， o clone el repositorio：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Necesita Python 3.11+． En Windows el lanzador ofrece instalarlo．

[Consulte las versiones](https://github.com/phishdestroy/TgWitness/releases)

PASO 02

### Elija cómo ejecutarla．

Haga doble clic en «`Start.cmd`» o ejecútelo en PowerShell：

```
.\Start.cmd
```

¿Solo está echando un vistazo？ Haga doble clic en `scripts\Demo.cmd` para acceder a una demostración aislada． No es necesario iniciar sesión en Telegram．

Con Python 3.11+ y `venv`：

```
sh start.sh
```

Para abrir el registro ficticio， ejecute `sh start.sh --demo`．

Con Docker en ejecución y Compose 2.20 o superior instalado：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

El segundo comando muestra su token del panel privado． Guárdelo en su equipo．

Abra [127.0.0.1:8787](http://127.0.0.1:8787) tras el inicio．

En instalaciones desde el código， el token está en `data/live/panel-token.txt`． Su propio par de API de [my.telegram.org](https://my.telegram.org) es opcional． [Guía completa ↗](https://phishdestroy.github.io/TgWitness/es/docs/reference/quickstart/)

**TgWitness 0.9.1** [Novedades →](https://phishdestroy.github.io/TgWitness/es/docs/reference/changelog/) · [Características y limitaciones conocidas →](https://phishdestroy.github.io/TgWitness/es/docs/reference/features/)

## Instrucciones claras． Un siguiente paso útil．

[Explore las guías ↗](https://phishdestroy.github.io/TgWitness/es/docs/)

[### Modos， escenarios y niveles de prueba Cuatro modos de recopilación． Ocho niveles de verificación． Encuentre el flujo de trabajo adecuado para su caso．](https://phishdestroy.github.io/TgWitness/es/guides/modes.html)

[01 ### Conecte una cuenta Importación de datos de teléfono， códigos QR y sesiones compatibles．](https://phishdestroy.github.io/TgWitness/es/docs/accounts/)[02 ### Elija un proxy Listas públicas de MTProxy o su propia ruta．](https://phishdestroy.github.io/TgWitness/es/docs/proxies/)[03 ### Configurar un bot de TgWitness Puntos de control firmados en su canal de Telegram．](https://phishdestroy.github.io/TgWitness/es/docs/witness/)[04 ### Exportar y verificar Comparta el historial capturado y compruebe su integridad．](https://phishdestroy.github.io/TgWitness/es/docs/exports/)

## Trabaja con el archivo．

Historial， IA con fuentes， MCP， OCR y webhooks firmados．

[Explora el flujo de trabajo](https://phishdestroy.github.io/TgWitness/es/docs/archive/)

## Antes de empezar．

**¿Esta página está vinculada a Telegram？**

No． Es una página estática con ejemplos ficticios． La aplicación se ejecuta en su máquina y es allí donde inicia sesión．

**¿Puede recuperar mensajes eliminados antes de su captura？**

No． Guarda lo que vio su cuenta mientras estaba en marcha． Una captura posterior no puede reconstruir ediciones perdidas ni mensajes borrados．

**¿Está cifrado todo mi registro？**

Las sesiones y las claves sí． Los mensajes y archivos no： use cifrado de disco． Las exportaciones pueden llevar contraseña AES－256．

**¿Está afiliada a Telegram？**

No． Es un proyecto independiente con licencia MIT basado en Telethon． Inicia sesión con sus propias cuentas．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Explore primero． Configúrela cuando esté listo．

[Demostración disponible：](https://phishdestroy.github.io/TgWitness/demo/?lang=es)[Guía de configuración](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=es)
