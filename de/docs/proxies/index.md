# Wählen Sie einen Proxy

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/proxies/

Halten Sie die Verbindung zum Konto aufrecht. Legen Sie ausdrücklich fest, wann dessen Route die Adresse des Servers nutzen darf.

## Wählen Sie zunächst den IP-Modus aus

01**IP verbergen**

Verwenden Sie einen Proxy. Sollte keiner funktionieren, warten Sie, ohne eine direkte Verbindung zu Telegram herzustellen.

02**Fallback zulassen**

Nach Ablauf der konfigurierten Verzögerung den direkten Zugriff zulassen; zu einem funktionierenden Proxy zurückkehren, sobald einer antwortet.

03**Tunnel / VPN**

Erlauben Sie direkte Verbindungen durch das Netzwerk des Hosts. Bei dieser Option wird kein VPN installiert oder überprüft.

Die Route bestimmt die Verbindung. Der IP-Modus legt fest, ob eine direkte Verbindung zulässig ist.

## Lassen Sie den Pool die Route verwalten

1. Öffnen Sie **„Konto“ → „Einstellungen“ → „Verbindungseinstellungen**“.
2. Wählen Sie den IP-Modus und **„Automatic MTProxy“** oder geben Sie eine feste Route ein.
3. Speichern Sie **die Telegram-Verbindung** und führen Sie **den Test** durch. Dies funktioniert auch vor der Anmeldung.
4. Überprüfen Sie nach dem Start der Erfassung, ob eine Testnachricht im Protokoll eingeht.

Neue Arbeitsbereiche nutzen automatisch MTProxy mit „Hide IP“-Funktion. Der Pool kombiniert vier öffentliche Quellen, prüft Einträge, behält funktionierende Routen bei und ersetzt ausgefallene Proxys. Bei fehlgeschlagenen Downloads bleiben die vorherigen Snapshots erhalten.

## Verwenden Sie Ihren eigenen Proxy

Geben Sie SOCKS5- oder HTTP-CONNECT-Daten ein, fügen Sie einen unterstützten Telegram-Proxy-Link ein oder geben Sie einen Betreiberkatalog an. Unterbrechen Sie die Überwachung, bevor Sie eine aktive Route ändern. Gefälschte TLS-MTProxy-Schlüssel, die mit „`ee`“ beginnen, werden weiterhin nicht unterstützt.

**Einstellungen für Rotation, Weitergabe und Wiederholungsversuche**

Legen Sie unter **„Parameter“ → „Automatischer MTProxy“** Fehlergrenzen, Wartezeiten, geplante Rotation und die Anzahl der Konten pro Proxy fest. Bei einer Freigabebegrenzung von „1“ muss ein Konto warten, wenn kein exklusiver Zugang verfügbar ist. Die Intervalle für die Listenaktualisierung und die Abfrage richten sich nach den Werten des Hauptarbeitsbereichs. Separate Proxys garantieren keine separaten Ausgangs-IP-Adressen.

## Trennung von Telegram von externen Anfragen

MTProxy leitet ausschließlich Telegram-Datenverkehr weiter. Zeitstempel, Benachrichtigungen, Kopien und Quellenprüfungen nutzen einen separaten SOCKS5/HTTP-Proxy, die SOCKS5/HTTP-Route des Kontos oder „Direct“, sofern der IP-Modus dies zulässt. Diese externen Anfragen können deaktiviert werden.

Ein expliziter `TGWITNESS_PROXY_FEED_PROXY`-Befehl konfiguriert die Route des Feed-Downloaders. Der [unabhängige Witness](https://phishdestroy.github.io/TgWitness/de/docs/witness/) behält seine eigenen Einstellungen bei. Diese Steuerelemente installieren kein System-VPN und leiten den Browser-Datenverkehr nicht um.

Sehen Sie sich [alle Modi, Standardeinstellungen und Quellenlisten](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/#ip-modes) an oder [legen Sie fest, wer die Route eines Kontos ändern darf](https://phishdestroy.github.io/TgWitness/de/docs/access/).
