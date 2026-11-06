# Telegram · Búsqueda de texto completo

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/search/

Busca mensajes guardados por formas de palabras, frases exactas, dominios y @nombres de usuario, mostrando primero los resultados más relevantes, con el índice vinculado al diario firmado.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentación](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigación](https://phishdestroy.github.io/TgWitness/es/docs/reference/investigation/)

![Investigación](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Análisis de archivos](https://phishdestroy.github.io/TgWitness/es/docs/reference/analysis/) · [OCR y transcripción locales](https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Vista previa.** En **«Diario»**, selecciona **«Mejor coincidencia · formas de la palabra»** junto al campo de búsqueda. Los resultados se ordenan mediante BM25 y coinciden con otras formas de la misma palabra: *«перевод»* encuentra *«переводом»* y *«переводы»*, *«transfer»* encuentra *«transfers»*, y una frase en chino se encuentra sin espacios. La opción **«Lo más reciente primero · texto exacto»** mantiene la búsqueda de subcadenas anterior en todo el registro.

El índice es un dato derivado. Se reconstruye a partir del diario firmado, nunca está firmado en sí mismo y nunca se incluye en una exportación. Los registros originales no se modifican.

**En esta página**

- [Sintaxis de búsqueda](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#search-syntax)
- [Idiomas](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#languages)
- [Dónde se encuentra el índice](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#where-the-index-lives)
- [Resultados y el diario firmado](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#results-and-the-signed-journal)
- [Texto reconocido](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#recognized-text)
- [Acceso](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#access)
- [Consultar el archivo y MCP](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#ask-the-archive-and-mcp)
- [Dependencias](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#dependencies)
- [Prueba de rendimiento](https://phishdestroy.github.io/TgWitness/es/docs/reference/search/#benchmark)

## Sintaxis de búsqueda

| Redactar | Resultados |
| --- | --- |
| `перевод карта` | Registros que contengan ambas palabras, en cualquier forma |
| `"переводом на карту"` | La frase exacta, en este orden |
| `бонус OR подарок` | Cualquiera de las dos palabras |
| `перевод -казино` | Registros sin la palabra excluida |
| `example.com` | El dominio y sus subdominios, incluso en enlaces ocultos y en las URL de los botones. |
| `@username`, `t.me/username` | Menciones y enlaces de la cuenta, así como los mensajes que envió. |
| `#tag` | El hashtag |
| `+79991234567`, una dirección de monedero, una dirección de correo electrónico | El mismo valor en texto o enlaces |
| `from:@username`, `from:123456` | Mensajes de ese remitente |
| `chat:-1001234567890` | Un chat; solo puede restringir tu propio acceso |
| `id:42` | Versiones guardadas del mensaje 42 |
| `since:2026-01-01 until:2026-01-31` | Período de observación: una fecha sin hora abarca todo el día. |
| `kind:edited` | Solo se permiten modificaciones (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Texto reconocido en lugar de, o junto con, los mensajes |

Las preposiciones y otras palabras funcionales se ignoran cuando hay otras palabras presentes. Las letras similares mezcladas en una palabra (una *«a»* latina dentro de una palabra cirílica), las letras Unicode de ancho completo y decorativas, así como los caracteres invisibles, se normalizan.

## Idiomas

El idioma se detecta en cada registro a partir de su escritura y sus letras:

| Script | Coincidencia |
| --- | --- |
| Cirílico | Lemas rusos y ucranianos con [pymorphy3](https://github.com/no-plagiarism/pymorphy3). Sin el diccionario ucraniano opcional, se utiliza un analizador morfológico ucraniano ligero. |
| Latín | Stemmer «Snowball» en inglés; se ignoran los signos diacríticos |
| Chino, japonés, coreano, tailandés, laosiano, jemer y birmano | Pares de caracteres superpuestos: se busca cualquier frase sin espacios. Las consultas en chino se dividen en palabras con Jieba. |
| Otros scripts | Palabras exactas |

El diccionario ucraniano (`pymorphy3-dicts-uk`) se distribuye bajo la licencia GPL-3.0, por lo que no viene instalado por defecto. Instálalo con `pip install "tgwitness[uk-dictionary]"`; el índice detecta el nuevo analizador y se reconstruye automáticamente.

## Dónde se encuentra el índice

| Modo | Almacenamiento | Uso |
| --- | --- | --- |
| En disco (predeterminado) | `search/fulltext.sqlite3` en el directorio del espacio de trabajo | Archivos de gran tamaño; resiste los reinicios. |
| Solo en memoria | No se guarda nada en el disco; se recrea en cada inicio. | No se guarda ninguna copia derivada del texto de los mensajes en el disco. |
| Desactivado | Sin índice; **primero lo más reciente ·** se mantiene **el texto exacto** | Instalaciones mínimas |

El administrador principal elige el modo en **Diario → Filtros → Índice de búsqueda** para cada espacio de trabajo. `TGWITNESS_FULLTEXT=disk|memory|off` Establece el valor por defecto para los espacios de trabajo que no tengan una opción propia. Al cambiar a «memoria» o desactivarlo, se elimina el archivo. El archivo de índice tiene la misma protección que el registro: se encuentra en el directorio de datos privados . No está cifrado y no forma parte de las copias de seguridad ni de las copias externas.

Los nuevos registros se indexan en segundo plano en cuestión de segundos; además, al realizar una búsqueda se indexa primero un pequeño historial acumulado, por lo que se encuentra un registro guardado hace un momento. Un diario existente se indexa tras la actualización sin bloquear el panel; hasta entonces, los resultados abarcan los registros indexados y el diario muestra el progreso. **La reconstrucción del índice** comienza de nuevo desde el primer registro.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` Es necesario detener el panel (de lo contrario, código de salida 3). Con `--json`, la salida estándar solo muestra el resultado; el progreso se envía a la salida de error estándar.

## Resultados y el diario firmado

El índice almacena el número de secuencia y el hash del último registro del diario que abarca y los compara con el diario cuando se abre. Un diario sustituido, restaurado o editado provoca una reconstrucción. Cada respuesta informa de esta posición, y cada resultado se lee desde el diario firmado mediante su número de secuencia: el índice decide qué registros mostrar y en qué orden, pero nunca su contenido. El acceso al chat se aplica al propio campo de chat del diario, no al contenido del índice.

## Texto reconocido

El OCR y las transcripciones permanecen en sus artefactos cifrados. Su índice existe únicamente en memoria y se reconstruye cuando finaliza un trabajo de reconocimiento. Aparece una coincidencia en su `media.saved` registro, etiquetado como «reconocimiento automático» con el motor, el modelo y un extracto; nunca se presenta como texto enviado en Telegram. El mismo índice sirve para **la búsqueda de texto reconocido**, que además sigue coincidiendo con subcadenas sin formato.

## Acceso

El acceso limitado al chat solo encuentra registros de sus chats, incluido el texto reconocido de sus archivos adjuntos. `chat:` y otros filtros solo pueden restringir ese conjunto. El estado del índice que se muestra al acceso limitado omite los totales del diario. Solo el administrador principal puede cambiar el modo o reconstruir el índice.

## Consulta el archivo y el MCP

Cuando **el archivo** esté completo, **la consulta** recuperará sus fuentes a partir de este índice: las mejores coincidencias en los chats seleccionados, contando cada texto guardado una sola vez. Se envían hasta 24 fuentes; los textos largos se recortan en torno a su coincidencia y se marcan como truncados. Las consultas sobre cambios recientes, versiones guardadas de un mensaje y búsquedas mientras el índice aún se está creando utilizan la recuperación cronológica anterior. La vista previa muestra qué método se ha utilizado.

Los clientes de MCP pueden llamar a `search_messages` con `ranked=true` y enviar mensajes con `next_offset`. Las conexiones con ámbito limitado solo reciben sus propios chats.

La paginación ordenada abarca, como máximo, los primeros resultados de 1,000, independientemente del tamaño de la página. Limita la consulta, el chat o el periodo para examinar más coincidencias. Las búsquedas más recientes primero ordenan los mensajes, los resultados de OCR y de transcripción antes de seleccionar cada página.

## Dependencias

| Paquete | Licencia | ¿Por qué? |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Lemas en ruso y ucraniano; los diccionarios se cargan localmente. |
| snowballstemmer | BSD-3-Cláusula | Raíces en inglés, Python puro |
| jieba | MIT | Segmentación de consultas en chino, Python puro (solo distribución del código fuente) |
| pymorphy3-dicts-uk (opcional) | GPL-3.0 | Diccionario completo de ucraniano |

Se requiere SQLite FTS5 con el `unicode61` tokenizador; forma parte de SQLite en las compilaciones actuales de Python. Sin él, la búsqueda de la mejor coincidencia indica que no está disponible.

## Prueba de rendimiento

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`Crea un registro firmado y determinista de mensajes mixtos en ruso, ucraniano, inglés, chino y japonés con enlaces e identificadores en 200 chats, genera el índice y mide la duración de búsquedas típicas (50 resultados, mediana de 7 ejecuciones).

Medido en Windows 11, Intel Core i9-13900K, 128 GB de RAM, Python 3.12.10, SQLite 3.49.1, datos en una unidad exFAT, analizador `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| Medida | Resultado |
| --- | --- |
| Registro firmado | 1 000 000 de mensajes, 1,50 GiB, escritos en 19 minutos |
| Creación de un índice a partir del registro | 71 s, unos 14 141 mensajes por segundo |
| Archivo de índice | 58 MiB, el 3,8 % del diario |
| Buscar justo después de un nuevo registro | Mediana de 8 ms, p95 de 9 ms |
| Búsqueda de subcadenas anterior, mismo diario | `перевод` 3,2 s, `银行转账` 2,6 s, `verify-account.example` 2,6 s |

| Buscar | Registros coincidentes | Mejor coincidencia, mediana | pág. 95 | Más recientes primero, mediana |
| --- | --- | --- | --- | --- |
| Palabras comunes y sus formas: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Dos palabras: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Palabra poco común: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Frase exacta: `"переказ коштів на картку"` | no se tiene en cuenta | 35 ms | 36 ms | 6 ms |
| Dominio con subdominios: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @nombredeusuario: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Chino sin espacios: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Japonés: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Raíz en inglés: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| O y exclusión: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Filtro de chat: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Filtro de periodo: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Una frase exacta se compara literalmente con los candidatos en orden de relevancia hasta que la página se llena, por lo que su total no se tiene en cuenta. Los tiempos aumentan con el número de registros coincidentes; restringir el chat o el periodo agiliza las búsquedas amplias. El corpus sintético repite un vocabulario reducido, por lo que las palabras comunes coinciden con muchos más registros que en los chats reales.
