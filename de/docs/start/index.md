# In wenigen Minuten loslegen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/start/

Sehen Sie sich zunächst ein Beispiel an. Verbinden Sie anschließend Ihr eigenes Konto.

## Schauen Sie sich ohne Konto um

Laden Sie das Projekt herunter oder klonen Sie es, installieren Sie **Python 3.11 oder höher** und führen Sie die Demo aus. Der Launcher erstellt eine lokale Umgebung und installiert die festgelegten Abhängigkeiten.

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

Der Browser öffnet einen Arbeitsbereich mit fiktiven Nachrichten. Öffnen Sie eine Unterhaltung, vergleichen Sie eine Bearbeitung und überprüfen Sie einen Export. Der Demo-Modus stellt keine Verbindung zu Telegram her.

![TgWitness-Konversationsansicht mit Beispielnachrichten](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

Ein Beispiel-Arbeitsbereich. Ihr eigenes Protokoll beginnt separat.

## Richten Sie Ihren eigenen Arbeitsbereich ein

Beenden Sie den Demo-Vorgang und verwenden Sie anschließend den normalen Launcher:

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

Öffnen Sie die vom Launcher angezeigte lokale Adresse. Geben Sie, falls dazu aufgefordert, den **Panel-Zugriffstoken** aus der im Terminal genannten lokalen Datei ein. Dadurch wird TgWitness freigeschaltet; dies ist unabhängig von der Anmeldung bei Telegram.

## Erfassen Sie Ihre erste Nachricht

1. [Verbinden Sie ein eigens dafür vorgesehenes Telegram-Konto.](https://phishdestroy.github.io/TgWitness/de/docs/accounts/)
2. Wählen Sie eine Gruppe oder einen Kanal aus, auf den das Konto Zugriff hat, und starten Sie anschließend die Überwachung.
3. Senden Sie eine neue Nachricht in einer Testgruppe, die Sie verwalten, und überprüfen Sie, ob diese im Protokoll erscheint.

Befolgen Sie für eine Serverinstallation die Anweisungen unter [„Keep it running](https://phishdestroy.github.io/TgWitness/de/docs/server/)“.
