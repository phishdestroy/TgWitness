# Wählen Sie einen Proxy

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/proxies/

Halten Sie das Konto online und entscheiden Sie selbst, ob es jemals die IP Ihres Servers zeigen darf.

## Wählen Sie zunächst den IP-Modus aus

01**Adresse ausblenden**

Nur Proxy. Wenn keiner geht, wartet es.

02**Direkt als letztes Mittel**

Geht nach einer Verzögerung direkt und kehrt zu einem Proxy zurück, sobald einer funktioniert.

03**Server hinter einem Tunnel oder VPN**

Direkt ist in Ordnung. Ein VPN wird dabei weder eingerichtet noch geprüft.

Die Route bestimmt die Verbindung. Der IP-Modus legt fest, ob eine direkte Verbindung zulässig ist.

## Lassen Sie den Pool die Route verwalten

1. **Konto → Einstellungen → Verbindungseinstellungen**.
2. IP-Modus und **Automatischer MTProxy** wählen, oder eine feste Route.
3. Speichern, **Telegram-Verbindung testen** (geht auch vor der Anmeldung).
4. Erfassung starten und sich selbst eine Testnachricht schicken.

Neue Arbeitsbereiche starten mit automatischem MTProxy und **Adresse verbergen**. Der Pool nutzt vier öffentliche Listen, prüft Server, behält die guten und tauscht tote aus.

## Verwenden Sie Ihren eigenen Proxy

SOCKS5, HTTP CONNECT, ein Telegram-Proxy-Link oder ein Betreiberkatalog. Vor dem Wechsel die Beobachtung pausieren. Fake-TLS-Geheimnisse (`ee`…) funktionieren nicht.

**Einstellungen für Rotation, Weitergabe und Wiederholungsversuche**

**Parameter → Automatischer MTProxy**: Fehlerschwellen, Wartezeiten, Rotation, Konten pro Proxy. Limit 1 heißt, ein Konto wartet, statt zu teilen. Verschiedene Proxys können trotzdem dieselbe Ausgangs-IP haben.

## Trennung von Telegram von externen Anfragen

MTProxy transportiert nur Telegram. Zeitstempel, Benachrichtigungen, Kopien und Code-Prüfungen laufen über einen separaten SOCKS5/HTTP-Proxy, die SOCKS5/HTTP-Route des Kontos oder direkt, wenn der Modus es erlaubt. Oder schalten Sie sie ab.

`TGWITNESS_PROXY_FEED_PROXY` legt die Route für Listen-Downloads fest. Der [Zeuge](https://phishdestroy.github.io/TgWitness/de/docs/witness/) hat eigene Einstellungen. Nichts davon berührt Ihren Browser oder das Systemnetz.

Mehr: [Modi und Standardwerte](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes), [wer Routen ändern darf](https://phishdestroy.github.io/TgWitness/de/docs/access/).
