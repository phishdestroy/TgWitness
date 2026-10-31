# OCR y transcripción locales

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/reference/media-analysis/

Reconoce las imágenes y el audio capturados mediante un «worker» local; mantiene el texto derivado vinculado a su archivo de origen.

**Versión principal actual:** utiliza una copia del código fuente; la versión preliminar portátil 0.7.0 es anterior a esta función.

[Guía de flujo de trabajo](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Abre un registro del diario `media.saved`, elige **«Reconocer archivo adjunto**» y, a continuación, selecciona «OCR» o «transcripción» en **«Preguntar al archivo**». El procesamiento es manual y local. No hay modo de almacenamiento en la nube ni subida automática. Los bytes originales del archivo adjunto y el `media_sha256` permanecen inalterados; el texto reconocido se marca explícitamente como reconocimiento automático y se almacena por separado con el hash de origen, la versión del motor o modelo, el idioma, los parámetros y la hora de finalización. Las transcripciones conservan las marcas de tiempo devueltas.

Busca en estos resultados utilizando **la opción «Buscar texto reconocido»** y el filtro «OCR/transcripción». Se trata de una búsqueda independiente de datos derivados; no convierte automáticamente el reconocimiento automático en texto original de Telegram ni lo añade a los eventos firmados.

## Configurar el «worker» opcional

La versión 1 requiere un servidor Linux con un daemon de Docker local. Las instalaciones en Windows pueden ejecutar TgWitness dentro de un entorno de máquina virtual Linux o WSL con su propio daemon local. El panel nunca descodifica por sí mismo un archivo adjunto no fiable.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Configura estas variables en el entorno del servicio TgWitness y reinícialo. El socket del daemon viene por defecto en `/var/run/docker.sock`; en las implementaciones sin privilegios de root se puede establecer en `TGWITNESS_DOCKER_SOCKET`. El worker utiliza explícitamente ese socket de Unix en lugar de un contexto remoto de Docker. No expongas una API de Docker a los usuarios del panel ni montes su socket dentro del contenedor de reconocimiento.

Para la transcripción, instala por separado un modelo de Whisper compatible con CTranslate2 y, a continuación, configura `TGWITNESS_WHISPER_MODEL_DIR` en su directorio. El trabajador lo carga con `local_files_only=True`; el modelo seleccionado y los datos de entrada se montan en modo de solo lectura. Consulta la [documentación del motor sobre la carga de modelos](https://github.com/SYSTRAN/faster-whisper). La imagen de OCR suministrada incluye datos de entrenamiento en inglés y ruso. Incorpora otro idioma a tu imagen cuando sea necesario; los códigos de idioma siguen [la CLI de Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

No se recurre a ningún modelo durante el procesamiento. La configuración de compilación/descarga puede utilizar la red; cada contenedor de reconocimiento tiene la conexión a red desactivada. Instala la imagen antes de habilitarla; el entorno de ejecución utiliza `--pull=never`.

## Límites y recuperación

El contenedor se ejecuta como un usuario sin privilegios, con un root de solo lectura, capacidades restringidas, `no-new-privileges` , un núcleo de CPU, 2 GiB de memoria, un límite de PID y un sistema de archivos temporal acotado. Solo se montan una copia verificada del archivo seleccionado y un directorio de modelos opcional. La base de datos, el almacén y la sesión del recopilador no se montan. Los [parámetros de ejecución de Docker](https://docs.docker.com/reference/cli/docker/container/run/) imponen estos límites; se trata de un límite del contenedor, no de un enclave de hardware.

Los archivos tienen un límite de 50 MiB, las imágenes de 20 millones de píxeles, el audio de 30 minutos con una duración conocida y el procesamiento de cinco minutos. Solo se ejecuta un trabajador a la vez, con un máximo de 20 tareas en cola o en ejecución y 100 tareas retenidas por espacio de trabajo. La opción «Cancelar» detiene el contenedor; «Reintentar» crea un nuevo trabajo vinculado al intento anterior. Los trabajos interrumpidos se marcan tras el reinicio. El procesamiento puede fallar cuando un modelo no se ajusta a los límites configurados; no se ejecuta de forma silenciosa sin aislamiento.
