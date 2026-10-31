# Configurar un bot de TgWitness

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/witness/

Permita que un proceso independiente compruebe el registro y publique puntos de control firmados en su canal.

## Dos servidores, dos claves de firma

ALOJAMIENTO / RECOPILADOR**Cuenta + registro**

Clave de firma del recopilador de sesiones de Telegram

Punto final de control de solo lectura

← Solicitar respuesta firmada →

HOST B / WITNESS**Verificar + conservar**

Huellas digitales de los recopiladores fijadas. Clave de firma de testigo independiente.

Registro propio + token del bot

Witness → API de bot de Telegram →**Su canal · publicaciones firmadas con TGW1**

El «witness» realiza las comprobaciones por sí mismo. El acceso del recopilador es de solo lectura. La publicación del bot utiliza la conexión y el token del «witness»; no se concede ninguna sesión de cuenta al «witness».

03 / DECISIONES EN LOS PUNTOS DE CONTROLRespuestas ilustrativas

ÚLTIMA VERSIÓN ACEPTADA**120 registros**`head 9c7d…`

PRÓXIMA RESPUESTA**128 registros**`head a4f2…`

Aceptado: el recuento aumenta, la firma se verifica y la clave coincide. El testigo conserva este nuevo límite.

Todos los ejemplos de respuesta dan por supuesta una firma válida y la clave fijada. Los hash que aparecen aquí son ejemplos abreviados. Un recuento mayor por sí solo no puede demostrar que todo el prefijo anterior se mantenga inalterado; compare una exportación con los puntos de control conservados.

## Prepare un bot y un canal

Cree un bot con BotFather y permítale publicar en un canal que usted controle. Elija un ordenador o un servidor para el «witness». Un host y un operador independientes proporcionan una mayor independencia que un segundo proceso en el servidor del recopilador.

## Tres pasos en «Extras»

1. **Acceso de solo lectura.** Abra **«Extras» → Un bot en su canal**, cree un token de testigo y guarde el archivo de acceso. Permite consultar los puntos de control y el estado del sistema, pero no las conversaciones ni los controles del recopilador.
2. **Canal e intervalo.** Introduzca el canal y una dirección de recopilación accesible desde el testigo. Guarde el archivo de configuración.
3. **Puesta en marcha.** Coloque juntos los archivos «`witness.json`», «`witness-token.txt`» y «`bot-token.txt`» creados en el servidor de Witness. Ejecute los siguientes comandos en el entorno del proyecto instalado.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

La descarga de los archivos no inicia el proceso de «witness». Compruebe que la primera publicación firmada aparece en el canal y, a continuación, guarde por separado la huella digital de la clave pública del «witness».

## Elija la frecuencia de publicación

La publicación de cada comprobación genera un registro externo periódico. A intervalos de cinco minutos, esto supone unas 288 entradas por espacio de trabajo al día. La configuración avanzada también ofrece la posibilidad de publicar cambios o problemas, un proxy y una dirección API de bot personalizada.

**¿Qué es lo que certifica realmente el bot?**

El testigo solicita al recopilador un punto de control firmado, lo verifica con la clave esperada y mantiene un registro firmado independiente. Registra tanto las respuestas que faltan y las rechazadas como las comprobaciones realizadas con éxito. La publicación sigue dependiendo de que el testigo esté en funcionamiento y pueda acceder a la API de bots de Telegram.

Comprueba el estado del registro notificado por el recopilador. No supervisa de forma independiente cada mensaje de Telegram. Para ello, añada la prueba de entrega controlada.

## Compruebe las pruebas más adelante

Conserve el registro de pruebas, las publicaciones del canal y las huellas digitales guardadas de forma independiente. El [procedimiento de verificación completo](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#verify) las compara con la exportación firmada por el recopilador.
