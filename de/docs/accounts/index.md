# Telegram · Ein Konto verbinden

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/accounts/

Ein Arbeitsbereich = ein Konto, sein Journal und sein Schlüssel.

## Wählen Sie Ihre Anmeldemethode

**Konten** → Arbeitsbereich hinzufügen → Verbindungseinstellungen. Nehmen Sie dafür ein separates Konto.

- **QR-Code:** über den Bildschirm „Geräte“ in Telegram scannen und bestätigen.
- **Telefonnummer:** Nummer, Code, dann das 2FA-Passwort, falls vorhanden.
- **Sitzungsimport:** Ihre eigene Sitzungsdatei oder Telegram-Desktop-Daten.

Nutzen Sie ein eingebautes API-Profil oder Ihre eigene API ID samt Hash. Es kennzeichnet nur die App, meldet Sie nicht an und verbirgt nichts.

**Benötigen Sie zunächst einen Proxy?**

Sie können [die Verbindungsroute vor der Anmeldung auswählen und testen](https://phishdestroy.github.io/TgWitness/de/docs/proxies/). Jedes Konto verfügt über eine eigene Route.

## Wählen Sie aus, was Sie überwachen möchten

1. Wählen Sie die Chats, Gruppen oder Kanäle, die Sie brauchen.
2. Prüfen Sie die Erfassungseinstellungen, Medien eingeschlossen.
3. Starten Sie und prüfen Sie Verbindung und jüngste Aktivität.

Das Konto muss Zugriff haben. Admins und Mitglieder sehen Unterschiedliches, das Journal zeigt, was dieses Konto bekommen hat.

Das ganze Konto? **Quellen → Beobachtungsumfang → Ermittlungsmodus**, prüfen, **Umfang speichern**. Komplette Anleitung: [ein ganzes Konto untersuchen](https://phishdestroy.github.io/TgWitness/de/docs/cases/).

## Überprüfen Sie den gesamten Pfad

Schicken Sie in Ihrer Testgruppe eine Nachricht von einem anderen Konto, bearbeiten und löschen Sie sie. Alle drei Ereignisse sollten im Journal erscheinen. Dann [exportieren und prüfen](https://phishdestroy.github.io/TgWitness/de/docs/exports/).

„Verbunden“ heißt, die Verbindung steht. Eine erfasste Testnachricht heißt, Ereignisse kommen wirklich an.

## Ein weiteres Konto hinzufügen

Neuer Arbeitsbereich unter **Konten**, gleiche Schritte. Notieren Sie den Schlüssel-Fingerabdruck jedes Kontos, damit Sie Exporte später auseinanderhalten.
