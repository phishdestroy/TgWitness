# Telegram · Línea de comandos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/cli/

Buscar, leer el contexto, contabilizar la actividad y exportar mensajes guardados desde scripts y agentes, con salida en formato --json, códigos de salida estables y tokens de solo lectura con ámbito limitado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Integraciones con archivos](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[MCP de solo lectura](https://phishdestroy.github.io/TgWitness/es/docs/reference/mcp/) · [Búsqueda de texto completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Vista previa.** `tgwitness search`, `context`, `messages`, `stats` y `export` leer las observaciones guardadas para scripts y agentes de IA. No pueden enviar nada a Telegram, cambiar la configuración ni modificar el diario firmado.

Con `--json`, la salida estándar (stdout) contiene exactamente un documento JSON (`export` escribe líneas JSON). El progreso, las sugerencias y los errores se envían a stderr. Los códigos de salida son estables:

| Código | Significado |
| --- | --- |
| `0` | Éxito, incluido un resultado vacío |
| `1` | Error: panel inaccesible, datos ilegibles, exportación interrumpida |
| `2` | Error de uso o solicitud no válida: fecha incorrecta, opción desconocida, índice de búsqueda desactivado |
| `3` | No disponible en este momento: el espacio de trabajo está abierto en un panel en ejecución, o el panel solicita que se vuelva a intentar más tarde (límite de frecuencia, tiempo de espera agotado). |
| `4` | Acceso denegado: token ausente, caducado o revocado; un chat fuera de su ámbito de aplicación; una herramienta que no lo permite. |

## Dos formas de leerlo

**A través del panel (`--url`).** El comando utiliza la misma API de archivo con ámbito que MCP. Crea una conexión en **Integraciones → MCP**: elige espacios de trabajo y chats, herramientas y una fecha de caducidad; a continuación, copia el token una vez. La conexión es de solo lectura, está limitada a esos chats, tiene un límite de 60 solicitudes por minuto y puede revocarse o rotarse en cualquier momento. Los tokens de inicio de sesión del panel y las credenciales de Telegram no funcionan aquí.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Un panel remoto requiere HTTPS; el HTTP sin cifrar solo se acepta para `127.0.0.1`, `localhost` y `::1`. Se ignoran las variables de entorno de proxy y se rechazan las redirecciones, por lo que el token solo llega a la dirección que indiques.

**Directamente desde un espacio de trabajo detenido (`--data-dir`).** Lee el directorio de datos con acceso local completo, sin necesidad de un token. Úsalo en una copia del directorio de datos o mientras la recopilación esté detenida. Los registros firmados nunca se modifican; al igual que en el panel, al abrir un espacio de trabajo es posible que se actualicen sus índices derivados. Cuando el panel tiene el espacio de trabajo abierto, el comando finaliza con código `3`; léalo a través del panel. Si no `--data-dir`, `TGWITNESS_DATA`, `./data/live` se utiliza el directorio de datos de la instalación en la que se ejecuta el comando.

`--workspace ID` selecciona un espacio de trabajo (por defecto `default`). `tgwitness messages
--workspaces` muestra los que puedes leer.

## Comandos

| Comando | Resultado |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Se mostrarán primero los resultados más relevantes, incluyendo variantes de palabras, frases exactas entre comillas, dominios y `@username` ([sintaxis](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Texto exacto, de más reciente a más antiguo, sin el índice |
| `tgwitness context CHAT_ID MESSAGE_ID` | Mensajes guardados dentro de un margen de diez ID de mensaje a cada lado |
| `tgwitness messages` | Chats que puedes leer |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Mensajes guardados del chat, ordenados de más reciente a más antiguo |
| `tgwitness messages CHAT_ID --message ID` | Cada versión guardada y cada registro de eliminación de un mensaje |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Estadísticas de actividad, a continuación |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Observaciones guardadas como líneas JSON en orden de registro. |

Las fechas son `2026-10-01` (medianoche UTC) o en formato ISO con la zona horaria, `2026-10-01T09:00+03:00`. Para `search`, `messages` y `export` se selecciona la hora de la observación. Las páginas admiten hasta 50 registros: sigue `next_offset` (`--offset`) para la búsqueda por orden de relevancia y `next_before` (`--before`) en otros lugares.

La búsqueda por relevancia se detiene en 1,000 resultados. La última página puede ser más corta que `--limit`; limita la consulta, el chat o el periodo cuando existan más observaciones coincidentes.

Cada resultado de mensaje incluye `untrusted_content: true`los ID del espacio de trabajo, del chat y del mensaje, la secuencia del registro, el hash del registro guardado y un enlace al panel. Las modificaciones, los avisos de eliminación y `missing_on_recheck` son registros independientes. La ausencia de un registro no demuestra que un evento no haya ocurrido nunca.

### Estadísticas de actividad

`stats` Cuenta las observaciones guardadas para un chat, un remitente o todos los chats incluidos en el ámbito de aplicación:

- mensajes por hora UTC y por día de la semana (empezando por el lunes), horas y días de mayor actividad;
- editados, eliminados y `missing_on_recheck` compartidos;
- remitentes con el recuento de mensajes y las horas del primer y último mensaje;
- los dominios más frecuentes y `@handles`, contados una vez por mensaje en todas sus versiones guardadas;
- Cobertura: `coverage.gap` registros y, para acceder a todo el espacio de trabajo, períodos sin señal de vida del colector conectado (`collector_liveness`).

El periodo selecciona **la hora del mensaje indicada por Telegram**. El recuento de horas y días de la semana puede ayudar a estimar la zona horaria del remitente, pero no la determina. Las cifras se calculan a petición a partir del registro y no se almacenan. Cada resultado indica el encabezado del registro que abarca cuando el acceso abarca todo el espacio de trabajo. La lectura se detiene tras cinco segundos a través del panel, o `--timeout` segundos a nivel local (por defecto, 30); entonces `complete` es «false» y `partial` se indica el primer registro que no se ha leído. En ese caso, solo se contan los registros más recientes.

### Exportar

`export` Escribe un objeto JSON por cada observación guardada (mensajes nuevos, instantáneas, modificaciones, mensajes recuperados, avisos de eliminación, `missing_on_recheck` y registros de archivos multimedia guardados) en el orden del registro. Cada línea tiene los mismos campos que el resto de resultados, con el texto completo. Al `--output`, el archivo se guarda con un `.partial` nombre y solo se renombra tras el registro de finalización del panel; una exportación interrumpida no deja ningún archivo y sale con el código `1`. `--output` nunca sobrescribe un archivo existente. Con `--output` y `--json`, la salida estándar muestra un resumen: recuento de registros, última secuencia del diario y, para el acceso a todo el espacio de trabajo, el encabezado del diario.

Para realizar una exportación a través del panel se necesita una conexión que permita **exportar mensajes (solo desde la línea de comandos)**; esta opción no está seleccionada por defecto. Este archivo es una copia de trabajo, no una prueba: para una entrega verificable, utiliza la exportación firmada en **«Exportaciones»**, que `python -m tgwitness.verify`se verifica.

El panel vuelve a comprobar el acceso antes de emitir cada registro, incluido el registro de finalización. Un acceso revocado o caducado da lugar a una exportación incompleta. Las lecturas diferidas de páginas comparten el límite del proceso de archivo con otras consultas y tienen un tiempo de espera limitado.

## Habilidad del agente

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) indica a un agente cómo utilizar estos comandos, cómo citar los registros y cómo tratar el texto capturado. Los agentes que lean `.agents/skills` lo cargan desde una copia del repositorio. Para Claude Code, copia la `tgwitness-cli` carpeta en `.claude/skills/` en tu proyecto o `~/.claude/skills/`.

## MCP y la línea de comandos

Ambos utilizan las mismas conexiones, comprobaciones de ámbito y límites. Los resultados de MCP se limitan a una página de 64 KiB, por lo que MCP no ofrece exportación masiva; la línea de comandos los transmite en tiempo real. `get_activity_stats` está disponible para ambos.
