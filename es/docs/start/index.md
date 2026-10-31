# Empiece en cuestión de minutos

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/start/

En primer lugar, examine un ejemplo práctico. A continuación, conecte su propia cuenta.

## Eche un vistazo sin necesidad de crear una cuenta

Descargue o clone el proyecto, instale **Python 3.11 o una versión posterior** y ejecute la demostración. El programa de inicio crea un entorno local e instala las dependencias fijadas.

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

El navegador abre un espacio de trabajo con mensajes ficticios. Abra una conversación, compare una modificación e inspeccione una exportación. El modo de demostración no se conecta a Telegram.

![Vista de conversación de TgWitness con mensajes de ejemplo](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Un espacio de trabajo de ejemplo. Su propio registro se inicia por separado.

## Cree su propio espacio de trabajo

Cierre el proceso de demostración y, a continuación, utilice el lanzador habitual:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Abra la dirección local que muestra el lanzador. Si se le solicita, introduzca el **token de acceso al panel** desde el archivo local indicado en el terminal. Esto desbloquea TgWitness; es un proceso independiente del inicio de sesión en Telegram.

## Capture su primer mensaje

1. [Conecte una cuenta de Telegram específica.](https://phishdestroy.github.io/TgWitness/es/docs/accounts/)
2. Seleccione un grupo o canal al que la cuenta tenga acceso y, a continuación, inicie la observación.
3. Envíe un nuevo mensaje a un grupo de prueba que usted controle y compruebe que aparece en el registro.

Para la instalación en un servidor, siga las instrucciones de [«Keep it running](https://phishdestroy.github.io/TgWitness/es/docs/server/)».
