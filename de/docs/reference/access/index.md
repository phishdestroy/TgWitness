# Zugriff und Berechtigungen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/access/

Legen Sie den Zugriff auf Konten und Chats fest, wählen Sie Berechtigungen aus, beschränken Sie Sitzungen und IP-Adressen und entziehen Sie den Zugriff.

Gewähren Sie einem Prüfer Zugriff auf einen Chat, einem Analysten die Berechtigung zum Exportieren eines Falls oder einem Operator die Kontrolle über ausgewählte Konten. Jede Person erhält ihr eigenes Token. Das Haupt- Panel-Token verbleibt beim Administrator.

[Einrichtung eines Kontos](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/) · [Verbindungswege](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/) · [Sicherheitsmodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/security/)

## Zwei Anwendungsbereiche, zwei unterschiedliche Aufgabenbereiche

**Der Erfassungsumfang** bestimmt, was ein Konto aufzeichnet: ausgewählte Chats, einen Telegram-Ordner oder das gesamte Konto. **Der Zugriffsumfang** legt fest, welche dieser aufgezeichneten Konten und Chats eine andere Person einsehen und nutzen kann. Die Gewährung von Zugriff bedeutet nicht, dass man einem Telegram-Chat beitritt, die Erfassung startet oder Berechtigungen für das Telegram-Konto erhält.

Ein Zugriff kann ausgewählte Arbeitsbereiche, ausgewählte Chats innerhalb dieser oder alle Arbeitsbereiche umfassen. **Alle Arbeitsbereiche, einschließlich später hinzugefügter,** decken auch zukünftige Konten ab. Wählen Sie Arbeitsbereiche ausdrücklich aus, wenn ein Fall auf diese beschränkt bleiben soll.

## Jemandem Zugriff gewähren

1. Melden Sie sich als Hauptadministrator an und öffnen Sie **„Zugriff**“.
2. Geben Sie unter **„Jemandem Zugriff gewähren**“ einen Namen ein, den Sie im Protokoll wiedererkennen werden.
3. Wählen Sie die Arbeitsbereiche und, falls erforderlich, die einzelnen Chats aus.
4. Wählen Sie aus, was diese Person tun könnte. **Die Ansicht** ist stets enthalten.
5. Legen Sie die Gültigkeitsdauer, die Anmelde-/Sitzungslimits und die zulässigen Adressen nach Bedarf fest.
6. Klicken Sie auf **„Zugriff erstellen**“. Kopieren Sie das Token jetzt: Es wird nur einmal angezeigt.
7. Senden Sie die Panel-Adresse und das Token privat. Der Empfänger gibt dieses Token auf der normalen Anmeldeseite ein; er benötigt weder Ihr Haupt-Panel-Token noch eine Telegram-Sitzung.

Öffnen Sie das Fenster mit dem ausgestellten Token in einer separaten Browsersitzung und überprüfen Sie die sichtbaren Chats sowie die zulässigen Aktionen, bevor Sie es weitergeben.

## Wählen Sie die Berechtigungen aus

| Genehmigung | Was es ermöglicht |
| --- | --- |
| `view` | Lesen Sie freigegebene Chats, erfasste Nachrichten, Profile, Dateien und gefilterte Protokollaufzeichnungen. Immer enthalten. |
| `export` | Der Export von Chat-Verläufen und Dossiers ist zulässig. Für den Export von Beweismaterial aus dem gesamten Arbeitsbereich ist Zugriff auf den gesamten Arbeitsbereich erforderlich. |
| `sources` | Verwalten Sie Quellen, Momentaufnahmen und Profilerfassungen. Der auf Chats beschränkte Zugriff ist nur in zugelassenen Chats möglich; die kontoweite Quellenerkennung und die Umfangseinstellungen bleiben deaktiviert. |
| `collect` | Einen Collector starten oder stoppen. Erfordert Zugriff auf den gesamten Arbeitsbereich, da die Erfassung Auswirkungen auf das Konto hat. |
| `interact` | Führen Sie unterstützte Telegram-Interaktionen innerhalb des Zugriffsumfangs durch. Bei einem auf den Chat beschränkten Zugriff können keine kontoweiten Link-Vorschauen genutzt werden. |
| `settings` | Ändern Sie die Erfassungseinstellungen, Zeitstempel, Benachrichtigungen, externe Kopien und Parameter. Erfordert Zugriff auf den gesamten Arbeitsbereich. |
| `account` | Melden Sie sich bei Telegram an oder ab und verwalten Sie Verbindungswege. Erfordert Zugriff auf den gesamten Arbeitsbereich. |

Berechtigungen und Geltungsbereich werden gemeinsam geprüft. Das Aktivieren einer Berechtigung führt nicht dazu, dass andere Chats geöffnet werden oder bei einem auf einen Chat beschränkten Zugriff eine arbeitsbereichsweite Aktion freigeschaltet wird. Für einen parallelen Export muss der Zugriff den exportierten Chat in jedem ausgewählten Konto abdecken. Ein erteilter Zugriff darf keine neuen Zugriffe erstellen, keine Sitzungen anderer Personen verwalten oder die Administratorkonsole öffnen.

### Drei nützliche Konfigurationen

| Person | Geltungsbereich | Berechtigungen |
| --- | --- | --- |
| Rezensent | Aufgezeichnete Chats aus einem Fall | `view` |
| Analyst, der eine Übergabe vorbereitet | Die zu untersuchenden und zu exportierenden Chats | `view`, `export`; fügen Sie `interact` nur hinzu, falls diese über Telegram agieren sollen |
| Erfassungsoperator | Ausgewählte vollständige Arbeitsbereiche | `view`, `sources`, `collect`; fügen Sie `settings` oder `account` nur bei Bedarf hinzu |

Dies sind Beispiele, die Sie über die Kontrollkästchen für Berechtigungen konfigurieren; es handelt sich nicht um festgelegte Rollen.

## Beschränkungen und Sitzungen

| Einleitung | So funktioniert es |
| --- | --- |
| Parallelsitzungen | Begrenzen Sie die Anzahl gleichzeitiger Sitzungen auf 1–100. Bei Erreichen der Obergrenze lehnen Sie die nächste Anmeldung ab oder beenden Sie die älteste Sitzung. |
| Anmeldungen sind zulässig | Die Anzahl der erfolgreichen Verwendungen des Tokens zum Starten von Sitzungen ist begrenzt. Bestehende Sitzungen werden nicht beendet, nur weil die letzte zulässige Anmeldung genutzt wurde. |
| Gültig bis | Eine absolute Ablauffrist für den Zugriff. Bei abgelaufenem Zugriff ist eine Anmeldung oder die weitere Übermittlung von Anfragen nicht mehr möglich. |
| Minuten ohne Aktivität | Zeitlimit für Inaktivität in einer Sitzung: von 5 Minuten bis zu 30 Tagen. Erfolgreiche Anfragen verlängern dieses Limit; ein geöffnetes Fenster kann durch regelmäßige Abfragen seine Aktivität aufrechterhalten. |
| Zulässige Adressen | Geben Sie bestimmte IP-Adressen oder CIDR-Subnetze an. Lassen Sie das Feld leer, um alle Adressen zuzulassen, sofern die Bindung bei der ersten Anmeldung nicht aktiviert ist. |
| Bei der ersten Anmeldung verknüpfen | Bei der ersten erfolgreichen Anmeldung wird die zulässige Adresse für diesen Zugriff festgelegt. |

Die IP-Adresse ist die vom Programm erkannte Client-Adresse. Wenn Sie sich hinter einem Reverse-Proxy oder einem Tunnel befinden, überprüfen Sie bitte die unter **„Offene Sitzungen“** angezeigte Adresse, bevor Sie sich auf IP-Regeln verlassen: Andernfalls könnte es den Anschein haben, dass sich mehrere Benutzer die Adresse des Proxys teilen.

## Zugriff ändern oder widerrufen

Bearbeiten Sie einen Eintrag unter **„Zugriffe“**, um dessen Geltungsbereich, Berechtigungen oder Einschränkungen zu ändern. Änderungen am Geltungsbereich und an den Berechtigungen werden bei nachfolgenden Anfragen überprüft, einschließlich Anfragen aus bereits geöffneten Sitzungen. Der Widerruf eines Zugriffs beendet dessen Sitzungen und macht das ausgestellte Token unbrauchbar. **Bei geöffneten Sitzungen** kann der Administrator auch eine einzelne Sitzung beenden, ohne den gesamten Zugriff zu widerrufen.

Durch eine Widerrufung können bereits heruntergeladene Dateien nicht wiederhergestellt werden. Das Abmelden, das Sperren des Fensters oder das Beenden einer Sitzung stoppt einen laufenden Collector nicht.

## Was der Administrator sehen kann

**Das Protokoll seit dem Start** kombiniert Prozessprotokolle mit Protokollaktivitäten aus jedem Arbeitsbereich: Anmeldungen, Ablehnungen, Routenänderungen und Bedieneraktionen. Es handelt sich um eine In-Memory-Konsole für den aktuellen Prozess, nicht um eine dauerhafte Kopie jeder einzelnen Nachricht. Häufig auftretende Nachrichtenereignisse verbleiben im Protokoll, anstatt die Konsole zu überfüllen.

Das Erteilen, Ändern und Widerrufen von Zugriffsrechten sowie das Starten oder Beenden von Sitzungen führen ebenfalls zur Erstellung signierter `access.*`-Protokollaufzeichnungen. Token sind in diesen Aufzeichnungen nicht enthalten. Ausgegebene Token und Sitzungszugangsdaten werden als Hash-Werte im verschlüsselten Tresor gespeichert.

****Hauptadministrator und Vertrauensgrenze**** Das Haupt-Panel-Token unterliegt keinen Einschränkungen. Bei der Anmeldung über den Browser mit diesem Token werden Sitzungen erstellt, die den vom Administrator konfigurierten Sitzungslimits unterliegen. Skripte, die das Haupt-Token direkt übermitteln, behalten den uneingeschränkten Zugriff und werden nicht als Browsersitzungen gezählt. Dies ist eine Zugriffskontrolle auf Anwendungsebene innerhalb einer Installation. Alle Arbeitsbereiche nutzen gemeinsam den Serverprozess; es handelt sich hierbei nicht um eine Isolierung vom Host-Administrator. Bewahren Sie das Haupt-Token, die Telegram-Sitzungen, die Signaturschlüssel und das Datenverzeichnis vertraulich auf. Ein Witness-Token ist eine separate Kontroll- bzw. Integritätsbescheinigung, kein Panel-Zugriffstoken.
