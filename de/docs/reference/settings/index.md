# Erste Einrichtung und Einstellungen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/

Der Einrichtungsassistent, Ziele, Benutzeroberflächenebenen, Verbindungswege und Einstellungen, die von einer Kontengruppe gemeinsam genutzt werden.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Konten](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/) · [Zusammenhang](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) · [Zugriff](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/)

Ein neuer Arbeitsbereich öffnet sich `/first-run`: Sprache und Zeit, Benutzeroberflächenebene, Ziel, Verbindung, Telegram und Chats. Jede Antwort wird auf dem Server gespeichert, sobald sie sich ändert, sodass beim Neuladen derselbe Schritt fortgesetzt wird. Der letzte Bildschirm listet die Antworten auf und ermöglicht es dir, zu jeder beliebigen davon zurückzukehren.

Sprache, IANA-Zeitzone, Design und Stufe werden pro Benutzer und pro Arbeitsbereich gespeichert. Die Standardeinstellungen sind die Browsersprache, die Zeitzone des Geräts, das Systemdesign und die einfache Benutzeroberfläche. Beim Ändern der Sprache bleibt die Panel-Sitzung erhalten. Die Zeiten im signierten Protokoll ändern sich nie.

`/settings` bearbeitet dieselben Datensätze wie der Assistent. Die Suche umfasst die Hauptfelder, Parameter und die erweiterten Formulare; ein verstecktes Feld kann geöffnet werden, ohne die Ebene zu ändern. Ebenen ändern lediglich die angezeigten Inhalte: Der Server prüft die Berechtigungen selbstständig. Die Sammlungseinstellungen und die erste Verbindung liegen in der Verantwortung des Arbeitsbereichsadministrators.

| Ebene | Felder | Seitenleiste |
| --- | --- | --- |
| Einfach | Nur das Wesentliche | Startseite, Chats, Änderungen, Archive, Einstellungen |
| Standard | Allgemeine Einstellungen mit Erläuterungen | Fügt Case Board, „Konten“ und „Zugriff“ hinzu |
| Experte | Alle Felder, Beschränkungen und technischen Details | Fügt „Quellen“, „Extras“, „Das Archiv befragen“, „Parameter“, „Konto“, „Systemprotokoll“ und „Integrationen“ hinzu |

Die [Panel-Anleitung](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/) beschreibt die einzelnen Abschnitte.

## Ziele

| Ziel | Sammlung | Dateien | Externe Dienste | Serveradresse |
| --- | --- | --- | --- | --- |
| Archivkopie | Aus; **„Start“** führt einen Export durch | Fotos bis zu 20 MB | Aus | Automatisch |
| Chats verfolgen | Kontinuierlich | Fotos und Videos mit einer Länge von bis zu 60 Sekunden bzw. einer Größe von bis zu 20 MB | Zeitstempel und Problembenachrichtigungen | Automatisch |
| Beweismittel | Kontinuierlich | Alle Dateien bis zu 1 GB | Zeitstempel, drand, Benachrichtigungen | Nein, ausblenden |

Als Beweismittel werden die externe Kopie, der Witness-Bot und die Code-Prüfung empfohlen. Speicher- und Benachrichtigungsadressen benötigen zunächst ein Ziel. Eine Funktion, die mit einem externen Dienst kommuniziert, fordert dazu auf, Anfragen außerhalb von Telegram zuzulassen; wenn man diese deaktiviert, wird angeboten, Zeitstempel, Benachrichtigungen und die externe Kopie ebenfalls zu deaktivieren.

Wenn das Ziel geändert wird, wird zunächst der Unterschied angezeigt, und manuelle Änderungen können beibehalten werden. Ein Feld, das vom Ziel abweicht, wird **mit „Von Ihnen geändert“** gekennzeichnet und kann wiederhergestellt werden. Die Einstellungsrevision verhindert, dass eine geprüfte Änderung eine Änderung überschreibt, die in einem anderen Reiter vorgenommen wurde.

## Zusammenhang

**„Automatic“** versucht es zunächst mit öffentlichen MTProxy-Servern, dann mit WARP und schließlich mit einer direkten Verbindung, wobei Letzteres nur dann zum Einsatz kommt, wenn die Serveradresse angezeigt werden darf. „Automatic“ und WARP können hash-geprüfte Komponenten installieren und den Server bei Cloudflare registrieren. WARP nutzt den vorhandenen wgcf/wireproxy-Manager und einen lokalen SOCKS5-Port; die Routing-Tabelle des Systems wird nicht verändert. Wenn externe Dienste benötigt werden, bevorzugt „Automatic“ WARP gegenüber MTProxy.

Ihr eigener Proxy akzeptiert `tg://proxy`, `socks5://`, `http://` und `https://`. Das Zertifikat eines HTTPS- Proxys wird überprüft, bevor Anmeldedaten an ihn gesendet werden.

Eine Verbindungsprüfung ist fünf Minuten lang gültig und an die Route, die Richtlinie und die Antworten des Assistenten gebunden; eine Änderung einer dieser Komponenten erfordert eine neue Prüfung. **Die Option „Ohne Prüfung fortfahren“** ist verfügbar und ersetzt nicht die Telegram-Anmeldung. Die gewählte Route wird im Hintergrund erneut überprüft, und „Automatic“ führt seine Kette nach einem Verbindungsabbruch erneut aus. Wenn kein öffentlicher Proxy antwortet, wird die Zählung rot angezeigt, begleitet von WARP- und Neuüberprüfungsaktionen.

## Kontogruppen

Konten in einer Gruppe nutzen gemeinsame Einstellungen. Öffnen Sie **„Konten“ → „Gruppen und gemeinsame Einstellungen“ → „Gemeinsame Einstellungen**“ oder **„Gruppeneinstellungen“** auf der Einstellungsseite eines Kontos.

Die Gruppe teilt das Ziel, gespeicherte Dateien, Zeitstempel, Drand, Problembenachrichtigungen, externe Kopien, Anfragen außerhalb von Telegram, den IP-Modus, die Aufzeichnungsinhalte, den Zeitplan für die erneute Überprüfung, Benachrichtigungsregeln, Berichtseinstellungen, Parameter und die Verbindungsroute. Benachrichtigungsempfänger, Proxy-Anmeldedaten und die Anmeldung bleiben pro Konto bestehen, ebenso wie das Starten und Anhalten der Erfassung.

- Jedes Mitglied folgt der Gruppe. Unter „Einstellungen“ wird ein Wert festgelegt: 🔗 **Aus der Gruppe** oder ✏️ **Eigener Wert**; mit **„Zurück zum Gruppenwert“** wird der ursprüngliche Wert wiederhergestellt.
- Eine Änderung listet die betroffenen Konten auf (**gilt für 2 von 3 Konten**) und fragt jedes Konto einzeln ab, bevor ein eigener Wert ersetzt wird. Nicht markierte Konten behalten ihren Wert bei.
- Ein Parameter, den die Gruppe nicht teilt, bleibt **Nicht geteilt: Jedes Konto behält seine eigenen Werte bei**, bis Sie auf **Diesen Wert teilen** klicken.
- **Beim Kopieren der Einstellungen eines Kontos** werden die Werte des ausgewählten Kontos als Einstellungen der Gruppe übernommen.
- Ein Konto, das in eine Gruppe verschoben wird, wird gefragt: **„Die Werte der Gruppe übernehmen?“** Andernfalls behält es seine eigenen Werte bei, gekennzeichnet mit ✏️. Später hinzugefügte Konten beginnen mit den Werten der Gruppe.
- Ein Beobachtungskonto behält seinen IP-Modus bei, bis es pausiert wird.

Jede Änderung wird im signierten Protokoll des Hauptarbeitsbereichs und jedes Mitglieds, das davon betroffen ist, festgehalten. Beim Löschen einer Gruppe bleiben deren Konten und deren aktuelle Werte erhalten.

Die Gruppenseite `/groups/<id>` zeigt die Mitglieder, was Aufmerksamkeit erfordert und die Chats, die mehrere Konten sehen. Siehe [Kontengruppen](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/#bulk-import-and-account-groups).

## Vorhandene Arbeitsbereiche

Ein Arbeitsbereich mit einer laufenden Sitzung oder einer zuvor abgeschlossenen Einrichtung zeigt den Assistenten nicht an. Seine Werte werden beim Laden der Seite nicht durch ein Ziel ersetzt. Das Ausblenden eines Feldes deaktiviert die Funktion nicht und löscht auch nicht deren Wert.

Die Schätzung von Umfang und Zeitaufwand basiert auf bis zu drei ausgewählten Chats und bis zu 20 Nachrichten aus jedem Chat. Es handelt sich um eine Schätzung: Sie berücksichtigt weder die Telegram-Limits noch die Geschwindigkeit eines bestimmten Servers oder die Dateien in jedem Chat.
