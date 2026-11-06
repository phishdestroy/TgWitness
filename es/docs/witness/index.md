# Telegram · Configurar un bot de TgWitness

Canonical page: https://phishdestroy.github.io/TgWitness/es/docs/witness/

Un proceso aparte comprueba su diario y publica puntos de control firmados en un canal.

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

Cree un bot con BotFather y deje que publique en su canal. Ejecute el testigo en otro sitio: otro host, idealmente gestionado por otra persona, vale mucho más que un segundo proceso junto al recolector.

## Tres pasos en «Extras»

1. **Acceso de solo lectura.** **Extras → Testigo independiente**, cree un token y guarde el archivo. Lee puntos de control y estado, nada más.
2. **Canal e intervalo.** Canal de Telegram o webhook de Discord, más una dirección del recolector accesible para el testigo. Guarde el archivo de ajustes.
3. **Lanzar.** Ponga `witness.json`, `witness-token.txt` y `bot-token.txt` juntos en el host del testigo y ejecute:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Espere a la primera publicación firmada en el canal y guarde la huella del testigo en un lugar seguro.

¿Prefiere Discord? Guarde la URL del webhook como `discord-webhook.txt`. Un testigo publica en un solo sitio; en Discord las comprobaciones largas llegan como archivo.

## Elija la frecuencia de publicación

Publicar cada comprobación deja un registro externo constante: cada cinco minutos son unas 288 publicaciones al día por espacio. Los ajustes avanzados permiten publicar solo con cambios o problemas, usar un proxy o un Bot API propio.

**¿Qué es lo que certifica realmente el bot?**

Pide al recolector un punto de control firmado, lo comprueba con la clave esperada y lleva su propio diario firmado, incluidas las respuestas perdidas y rechazadas.

Comprueba el estado del diario; no vigila Telegram por sí mismo. Para eso, haga una prueba de entrega controlada.

## Compruebe las pruebas más adelante

Guarde el diario del testigo, las publicaciones y las huellas. [Cómo comprobarlos](https://phishdestroy.github.io/TgWitness/es/docs/reference/witness/#verify) frente a la exportación del recolector.
