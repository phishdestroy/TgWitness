# Ein Konto verbinden

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/accounts/

Ein Arbeitsbereich umfasst ein Konto, dessen Protokoll und dessen Signaturschlüssel.

## Wählen Sie Ihre Anmeldemethode

Eröffnen Sie **Konten**, fügen Sie einen Arbeitsbereich hinzu und öffnen Sie dessen Verbindungseinstellungen. Verwenden Sie für die Beobachtung ein eigens dafür vorgesehenes Konto.

- **QR-Code:** Scannen Sie diesen über die Geräteeinstellungen von Telegram und bestätigen Sie die neue Anmeldung.
- **Telefonnummer:** Geben Sie die Nummer, den von Telegram gesendeten Code und Ihr Passwort für die zweistufige Verifizierung ein, sofern diese aktiviert ist.
- **Sitzungsimport:** Importieren Sie eine unterstützte Sitzung oder Ihre eigenen Telegram-Desktop-Daten.

Wählen Sie ein integriertes API-Profil aus oder geben Sie Ihre eigene API-ID und Ihren eigenen Hash ein. Ein API-Profil identifiziert den Client; es meldet sich nicht bei einem Konto an und macht die Verbindung auch nicht anonym.

**Benötigen Sie zunächst einen Proxy?**

Sie können [die Verbindungsroute vor der Anmeldung auswählen und testen](https://phishdestroy.github.io/TgWitness/de/docs/proxies/). Jedes Konto verfügt über eine eigene Route.

## Wählen Sie aus, was Sie überwachen möchten

1. Öffnen Sie die Quellenliste und wählen Sie die gewünschten Chats, Gruppen oder Kanäle aus.
2. Überprüfen Sie vor Beginn der Überwachung die Erfassungseinstellungen, einschließlich der Medien.
3. Starten Sie den Collector und überprüfen Sie dessen Verbindung sowie die jüngsten Aktivitäten.

Das Konto muss Zugriff auf die Quelle haben. Je nach Rolle sind unterschiedliche Ereignisse sichtbar; das Protokoll gibt wieder, was das jeweilige Konto empfangen hat.

Für einen Fall, der das gesamte Konto umfasst, wählen Sie **„Quellen“ → „Beobachtungsumfang“ → „Untersuchungsmodus“**, überprüfen Sie die Einstellungen und klicken Sie auf **„Umfang speichern**“. Die [vollständige Anleitung zur Untersuchung](https://phishdestroy.github.io/TgWitness/de/docs/cases/) deckt alle sichtbaren Chat-Typen, den alten Verlauf, Personenprofile, verweisende Chats und die Übergabe von Beweismitteln ab.

## Überprüfen Sie den gesamten Pfad

Senden Sie in einer von Ihnen kontrollierten Testgruppe eine eindeutige Nachricht von einem anderen Konto, bearbeiten Sie diese und löschen Sie sie anschließend. Bestätigen Sie alle drei Ereignisse im Protokoll, [exportieren Sie den Datensatz anschließend und überprüfen Sie](https://phishdestroy.github.io/TgWitness/de/docs/exports/) ihn.

Der Status „Verbunden“ bestätigt die Verbindung. Eine erfasste Testnachricht bestätigt, dass ein bestimmtes Ereignis diesen Arbeitsbereich erreicht hat.

## Ein weiteres Konto hinzufügen

Erstellen Sie unter **„Konten“** einen weiteren Arbeitsbereich und wiederholen Sie die Einrichtung. Bewahren Sie den Fingerabdruck des Signaturschlüssels jedes Kontos auf, damit Sie dessen Exporte später identifizieren können.
