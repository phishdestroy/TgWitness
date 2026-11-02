# Hochsichere Bereitstellung

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/

Ein gesicherter 24/7-Server bei Hetzner oder Phala Cloud, Gateway-DNS und Überprüfungen, die von Dritten wiederholt werden können.

Ein signiertes Protokoll belegt, dass die Aufzeichnungen **nach** der Signierung nicht verändert wurden. Bei schwerwiegenden Fällen stellt sich als Nächstes die Frage, ob jemand die Daten **vor** der Signierung manipulieren konnte: Wer hat den Collector betrieben, auf welchem Rechner, und hat sich jemand dort angemeldet? Dieser optionale Modus stellt den Collector so bereit, dass ein Dritter dies überprüfen kann – anhand von Aufzeichnungen, die vom Cloud-Anbieter und von Cloudflare gespeichert werden, anstatt sich auf die Aussage des Betreibers zu verlassen.

Die normale Nutzung lokal und mit Docker bleibt unverändert. Hier läuft nichts, es sei denn, Sie führen eine Bereitstellung mit `python -m tgwitness.cloud`, und der Collector liest seinen Host nur, wenn die Bereitstellung `TGWITNESS_ASSURANCE`.

Ablaufdiagramm · Operator → Server, Firewall ohne Eingangsregeln (Anbieter-API); Operator → Tunnel und DNS (Cloudflare-API); Server, Firewall ohne Eingangsregeln → Tunnel und DNS (nur ausgehend); Server, Firewall ohne Eingangsregeln → Auf dem Server erstellter Signaturschlüssel; Verifier, schreibgeschützte Token → Anbieterprotokoll und Firewall; Verifier, schreibgeschützte Token → Adresse des Tunnel-Konnektors und Ingress; Verifier, schreibgeschützte Token → Signierte /api/assurance-Erklärung; Verifier, schreibgeschützte Token → Beweismaterial-ZIP · Operator · Verifier,schreibgeschützte Token · Server, Firewall ohneEingangsregeln · Anbieterprotokoll undFirewall · Adresse desTunnel-Konnektors undIngress · Signierte/api/assurance-Erklärung · Beweismaterial-ZIP · Tunnel und DNS · Auf dem Server erstellterSignaturschlüssel · Anbieter-API · Cloudflare-API · nur ausgehend

**Diagramm als Text**

1. Operator → Server, Firewall ohne Eingangsregeln (Anbieter-API)
2. Operator → Tunnel und DNS (Cloudflare-API)
3. Server, Firewall ohne Eingangsregeln → Tunnel und DNS (nur ausgehend)
4. Server, Firewall ohne Eingangsregeln → Auf dem Server erstellter Signaturschlüssel
5. Verifier, schreibgeschützte Token → Anbieterprotokoll und Firewall
6. Verifier, schreibgeschützte Token → Adresse des Tunnel-Konnektors und Ingress
7. Verifier, schreibgeschützte Token → Signierte /api/assurance-Erklärung
8. Verifier, schreibgeschützte Token → Beweismaterial-ZIP

## Was ein Prüfer überprüfen kann

| Behauptung | Wie dies überprüft wird | Verwaltet von |
| --- | --- | --- |
| Der Server wurde zu einem bekannten Zeitpunkt über die API des Anbieters erstellt. | Das Server-Objekt und dessen Erstellung im eigenen Protokoll des Anbieters | Anbieter |
| Niemand hat die Zugriffspfade des Anbieters genutzt | Protokoll von Konsolenanfragen, Rettungsmaßnahmen, Passwortzurücksetzungen, Neuinstallationen, ISO-Dateien, Images und Backups | Anbieter |
| Es konnte keine Verbindung hergestellt werden | Die Firewall des Anbieters hat keine Regeln für eingehenden Datenverkehr; SSH wird ab dem ersten Start ausgeblendet. | Anbieter (Firewall), Host (SSH) |
| Das Panel ist ausschließlich über den Tunnel erreichbar | Der Tunnel-Ingress leitet ausschließlich an das Panel weiter; der Connector läuft von der Serveradresse aus. | Cloudflare |
| Genau diese Software läuft | Der signierte Hash des Quellcode-Baums des Collectors entspricht einem Checkout des bereitgestellten Commits | Collector, abgeglichen mit Git |
| Der Signaturschlüssel wurde auf diesem Server erstellt | Der Schlüssel signiert eine Erklärung, in der die Server-ID des Anbieters und der Hash des empfangenen „cloud-init“ angegeben sind. | Collector, vom Anbieter überprüft |
| Das Journal gehört zu diesem Schlüssel und diesem Server | Jeder Prozessstart im Evidenz-ZIP enthält die Host-Messung für diesen Server | Beweismaterial ZIP |

Host-Messwerte (SSH-Listener und -Prozesse, aktuelle Sitzungen, Anmeldungen am `wtmp`, den Systemstart) werden vom Collector selbst gemeldet und bei jedem Prozessstart sowie bei `host.state` Aufzeichnungen, sobald sie sich ändern. Ein Root-Benutzer auf dem Server könnte sie fälschen; sie unterstützen die Aufzeichnungen des Anbieters und von Cloudflare, anstatt diese zu ersetzen.

## Anbieter

| `--provider` | Anmeldedaten | Schreibgeschützter Zugriff für Verifier | Anbieterprotokoll für den Verifizierer | Aufbewahrt für |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Lese-Token desselben Projekts | Server- und Firewall-Maßnahmen | Solange die Ressourcen vorhanden sind |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Schreibgeschütztes persönliches Zugriffstoken | Droplet-Aktionen | Solange das Droplet existiert |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` Schreibgeschützte Bereiche | Kontoereignisse, Versionen von Firewall-Regeln | 90 Tage |
| `vultr` | `VULTR_API_KEY` | Benutzer mit Lesezugriff und der `activity_logs` Berechtigung | Aktivitätsprotokoll des Kontos (Methode, Pfad, Akteur) | 30 Tage, länger mit einem Abonnement für das Audit-Protokoll |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail-Ereignisverlauf | 90 Tage |
| `phala` | `PHALA_CLOUD_API_KEY` | Ein API-Schlüssel desselben Arbeitsbereichs | Anwendungsaktualisierungen: Änderungen am Code und an der Umgebung, Neustarts, Betriebssystem-Upgrades | Solange die Anwendung existiert |
| `generic` | keine | keine | keine: **selbstbeglaubigt** | – |

Verwenden Sie für jeden Fall ein eigenes Projekt, Team, Konto oder Unterkonto: Der schreibgeschützte Zugriff des Prüfers zeigt dann nur diese Bereitstellung an. Anmeldedaten werden aus `--provider-token-file` oder der oben genannten Variablen, niemals aus der Befehlszeile. Bei AWS enthält die Datei die Angabe `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; die Region ist `--location`.

Was die Protokolle der einzelnen Anbieter nicht anzeigen können, wird in jedem Bericht vermerkt. Kurz gesagt: Hetzner protokolliert Konsolenanfragen; die Recovery-Konsole von DigitalOcean, Lish/Glish von Linode und die Webkonsole von Vultr werden als solche nicht protokolliert, sodass der Root-Zugang beim ersten Start gesperrt ist und eine Konsolenanmeldung eine Passwortzurücksetzung oder eine Änderung der Startkonfiguration erfordern würde, was protokolliert wird. Vultr gibt die Konsolenadresse an jeden Schlüssel zurück, der die Instanz lesen kann; weder der Datensatz noch der Bericht speichern diese.

## Vertrauliche VM auf der Phala Cloud (Intel TDX)

Der `--provider phala` läuft der Collector in einer vertraulichen Intel-TDX-Virtual-Machine auf [Phala Cloud](https://phala.com/), die von dstack verwaltet wird. Der Host und die Mitarbeiter von Phala können dessen Speicher nicht auslesen, und der Prozessor signiert eine Bescheinigung darüber, was die Maschine beim Booten geladen hat. Der Verifizierer verlässt sich nicht blind auf die Angaben von Phala: `tgwitness.tdx` er überprüft jede Bescheinigung selbst, bis hin zur festgesteckten Intel SGX Root CA, anhand der Sperrlisten von Intel und der von Intel signierten Plattformdaten und lehnt Maschinen ab, die debuggt oder migriert werden können.

| Eintrag erstellen | Was es zeigt |
| --- | --- |
| `tdx_binding` | Die Bescheinigung umfasst die signierte Erklärung des Erfassers und den Zufallswert dieser Anfrage. |
| `tdx_quote` | Intel bürgt für die Bescheinigung; sie wird nur erteilt, wenn Intel die Plattform als auf dem neuesten Stand bewertet. |
| `tdx_compose_hash` | RTMR3, das aus dem dstack-Ereignisprotokoll wiedergegeben wird, misst die App-Composes, die der Collector meldet. |
| `tdx_compose` | Dieser Code entspricht Byte für Byte dem Code, der aus dem bereitgestellten Commit erstellt wird: Quelldateien sind über ihren Hash-Wert, beide Bilder über ihren Digest-Wert festverknüpft; es gibt keinen weiteren Code. |
| `tdx_identity` | Die Bescheinigung stammt von der bereitgestellten Anwendung und Instanz, wobei Schlüssel aus dem KMS von Phala und einer verschlüsselten Festplatte verwendet werden. |
| `tdx_os` | Mit `--tdx-measurements`entsprechen MRTD und RTMR0-2 den Werten, die aus dem dstack-OS-Image berechnet wurden (`dstack-mr measure --json`) |

Jeder im Protokoll aufgezeichnete Start des Collectors enthält eine solche Bescheinigung, sodass `verify --evidence` jeder Start überprüft wird. Phalas Liste der Anwendungsrevisionen dient als Anbieterprotokoll: Wenn sich die Kompositionsfunktion nach der Bereitstellung geändert hat, schlägt der Bericht fehl.

Wählen Sie im Panel **Vertrauliche virtuelle Maschine · Phala Cloud** unter **Extras** → **Server 24/7** und fügen Sie einen Phala-Cloud-API-Schlüssel ein; der Quick-Tunnel funktioniert wie bei Hetzner. Über die Befehlszeile:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` Liest Intels Zertifikate und Sperrlisten aus einer Datei aus, anstatt sie von Intel herunterzuladen. Gateway-DNS ist hier nicht verfügbar: Phala verfügt über keine Provider-Firewall für ausgehenden Datenverkehr.

Eine Bescheinigung kann einen Fehler im TDX-Modul oder im Mikrocode von Intel sowie physischen Zugriff auf den Speicherbus nicht ausschließen. Wer auch immer die Anwendung im Konto von Phala kontrolliert, kann ein weiteres „Compose“ bereitstellen; dies erscheint als neue Revision mit einem neuen „Compose“-Hash. Der Host kontrolliert die Zeitquelle und das Netzwerk des Rechners.

## Bevor Sie beginnen

1. Eine Cloudflare-Zone, deren Konto-ID sowie ein API-Token mit den Berechtigungen **„Cloudflare Tunnel Edit“**, **„Zone Read“** und **„DNS Edit“**, bereitgestellt mit `--cloudflare-token-file` oder `CLOUDFLARE_API_TOKEN`. Für den Prüfer: **„Cloudflare Tunnel Read“**, **„DNS Read“** und, für das Audit-Protokoll, **„Account Settings Read**“. Ohne Domain benötigt ein [Quick-Tunnel](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#quick-tunnel-without-a-domain) nichts davon.
2. Anmeldedaten eines Anbieters mit Schreibzugriff auf ein dediziertes Projekt; `lock` verwendet dasselbe:

   - Hetzner: API-Token mit Lese- und Schreibberechtigung;
   - DigitalOcean: persönliches Zugriffstoken mit Schreibzugriff;
   - Linode: persönliches Zugriffstoken mit `linodes`, `firewall` sowie `events` Lese-/Schreibberechtigungen;
   - Vultr: API-Schlüssel eines dedizierten Kontos oder Unterkontos;
   - AWS: IAM-Anmeldedaten zulässig `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` und `ec2:RevokeSecurityGroupIngress`.
3. Der auszuführende Commit. Ein Release-Tag wird einmalig auf seinen Commit aufgelöst mit `git ls-remote`; der Server erhält immer nur den 40-Zeichen-Commit.

## Aus dem Panel

Auf Ihrem eigenen Computer führt **„Extras → Server 24/7“** dasselbe `deploy` für Hetzner in drei Schritten: Wähle Europa oder die Vereinigten Staaten aus, füge einen Hetzner-Token (Lese- und Schreibzugriff) ein und überprüfe anschließend den Servertyp, den monatlichen Preis, die Adresse und die Version, die das Panel mit diesem Token ermittelt hat. Es wird nichts erstellt, bevor du bestätigst. Das Panel zeigt jeden Schritt an, wie `deploy` er meldet, anschließend die Adresse, das Panel-Token und den Fingerabdruck des Signaturschlüssels. Ohne Domain erhält der Server einen [Schnelltunnel](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **unter „Ihre Server“ → „Aktuelle Adresse suchen“** wird diese nach einem Neustart erneut abgerufen. Für eine feste Adresse unter Ihrer eigenen Domain öffnen Sie **„Optional · Ihre eigene Domain** “ und fügen ein Cloudflare-Token hinzu (der vorbereitete Link wählt „Zone lesen“, „DNS bearbeiten“ und „Cloudflare-Tunnel bearbeiten“ aus).

Die Tokens werden bei jeder Anfrage vom Browser-Tab an TgWitness auf demselben Computer übertragen und nirgendwo gespeichert; der Bereitstellungsdatensatz, das redigierte „cloud-init“, das Panel-Token und, bei einem Schnell-Tunnel, der Adressschlüssel werden `deployments/NAME` im Datenverzeichnis gespeichert. Das Panel bietet dies nur dem Hauptadministrator über eine direkte Loopback-Verbindung an (`127.0.0.1`, keine Proxy- oder Tunnel-Header); ein über ein Netzwerk erreichbares Panel zeigt stattdessen die Befehle an . Die Version ist standardmäßig auf das Release-Tag des laufenden Panels gesetzt, das über die GitHub-API ermittelt wird. Standort, Servertyp und Preis stammen aus der Hetzner-API: `cpx22` sofern dort angeboten, andernfalls der günstigste x86-Typ mit mindestens 2 GB Arbeitsspeicher.

## Schneller Tunnel ohne Domain

`--quick-tunnel` ersetzt `--zone`, `--cloudflare-account` und `--panel-host`; es ist kein Cloudflare- Konto oder -Token erforderlich:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Auf dem Server öffnet „cloudflared“ einen [schnellen Tunnel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) zum Panel: eine zufällige `https://….trycloudflare.com` Adresse, die sich ändert, sobald „cloudflared“ oder der Server neu gestartet wird. Ein kleiner Dienst auf dem Server veröffentlicht jede Adresse in einem zufälligen „ntfy.sh“- Thema, signiert (HMAC-SHA256) mit einem Schlüssel, der ausschließlich im Deployment-Verzeichnis gespeichert ist (`address-key.txt`) und wiederholt dies alle drei Stunden, da ntfy.sh Beiträge 12 Stunden lang aufbewahrt. `deploy` und **„Find the current address“** akzeptieren nur signierte Beiträge, sodass ein gefälschter Beitrag dich und dein Panel-Token nicht an die Adresse einer anderen Person weiterleiten kann. Das Thema ist im Protokoll und im veröffentlichten cloud-init enthalten: Wer auch immer darüber verfügt, kann die aktuelle Adresse ablesen, die weiterhin nach dem Panel-Token fragt. Der Server hält in keinem Fall einen eingehenden Port offen.

Was es kostet: Da kein Cloudflare-Konto Aufzeichnungen über einen Quick-Tunnel führt, `verify` werden der Tunnel, der Connector und die DNS-Prüfung als nicht verfügbar gemeldet, und das Ergebnis ist bestenfalls `incomplete`; die Anbieteraufzeichnungen, die Firewall, die signierte Erklärung, die Host-Messungen und der Installationsvergleich werden wie gewohnt geprüft. Der Byte-Vergleich mit dem Referenz-Installer erfordert einen bereitgestellten Commit, der bereits weiß, `--quick-tunnel`; ein 0.7.0-Checkout erstellt den Domain-Installer und meldet den Unterschied. Cloudflare gewährt für Quick-Tunnel keine Verfügbarkeitsgarantie, erlaubt 200 laufende Anfragen und überträgt keine „Server-Sent Events“, sodass die Live-Aktualisierungen des Panels (Versionen ab 0.7.0) möglicherweise nicht über einen Quick-Tunnel ankommen und eine Ansicht neu geladen werden muss; dieser Aspekt wurde noch nicht getestet. Für einen Fall, der beständig sein muss, verwenden Sie Ihre eigene Domain.

## Bereitstellen

Sehen Sie sich zunächst alles an, was gesendet wird. `plan` Es werden keine Anfragen an Provider oder Cloudflare gestellt:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Stellen Sie das Tool anschließend mit denselben Optionen und den Anmeldedaten bereit:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Servertypen für den Einstieg: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` und `--image` standardmäßig auf Ubuntu 24.04 des jeweiligen Anbieters in einer europäischen Region.

`--repository` Übernimmt den Commit aus einem anderen https-Git-Repository, ohne Anmeldedaten in der URL (standardmäßig `https://github.com/phishdestroy/TgWitness.git`). `deploy` akzeptiert auch `--out` für ein anderes Bereitstellungsverzeichnis (Standard `deployments/NAME`; ein Verzeichnis, das bereits eine Bereitstellung enthält, wird abgelehnt) und `--wait`, die Anzahl der Minuten, die auf die signierte Bestätigung des Collectors gewartet werden soll: 1 bis 240, Standard 20 oder 60 für `generic`.

Der Befehl:

1. Erstellt einen Cloudflare-Tunnel, dessen Ingress den Hostnamen des Panels an das Panel weiterleitet und, falls angegeben, den Hostnamen des Witness an `/api/witness/head` und `/api/assurance` nur;
2. Erstellt Proxy-CNAME-Einträge für diese Hostnamen und lehnt Namen ab, die bereits existieren;
3. Erstellt eine Provider-Firewall ohne eingehende Regeln und einen Server dahinter ohne SSH-Schlüssel, ohne Backups, ohne Konsolen-Agent und mit „cloud-init“, das SSH maskiert, Root sperrt, `cloudflared`, genau den Commit abruft, diesen überprüft und TgWitness als abgesicherten systemd-Dienst startet;
4. wartet auf die signierte Erklärung des Collectors und überprüft, ob darin dieser Server und der Hash dieses „cloud-init“ genannt werden.

`deployments/case-2026-11/` Enthält dann:

| Datei | Inhalt | Teilen? |
| --- | --- | --- |
| `deployment.json` | IDs, Hashes, die durchgeführten API-Aufrufe (Methode, Pfad, Status) und die erste signierte Aussage | Ja, mit dem Verifizierer |
| `cloud-init.redacted.yaml` | Das genaue „cloud-init“-Skript, bei dem die beiden Geheimnisse durch `REDACTED` | Ja |
| `panel-token.txt` | Das Panel-Token | Nein |

Das Root-Passwort des Anbieters, das Tunnel-Token und das Panel-Token werden niemals gespeichert `deployment.json`. Veröffentlichen Sie den am Ende angezeigten Fingerabdruck des Collectors über einen Kanal, den Sie nicht allein kontrollieren, beispielsweise einen Witness-Kanal oder eine Nachricht an den Empfänger.

Melden Sie sich bei Telegram unter `https://case.example.org` mit dem Panel-Token an, wie in der [Anleitung zum Konto beschrieben](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/). Panel-Aktionen werden im signierten Protokoll aufgezeichnet; es handelt sich dabei nicht um SSH-Sitzungen. Ein [Witness](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) kann abfragen `https://case-witness.example.org`.

Es gibt kein SSH: Wenn der Bootstrap-Vorgang fehlschlägt, antwortet der Collector nicht. Löschen Sie den Server und führen Sie die Bereitstellung erneut durch oder verwenden Sie eine Debug-Bereitstellung, um die Ursache zu ermitteln.

### Geheimnisse in den Benutzerdaten

Das „cloud-init“ enthält zwei Geheimnisse: das Panel-Token und das Cloudflare-Tunnel-Token. Der Signaturschlüssel gehört nicht dazu; er wird auf dem Server erstellt. Hetzner, DigitalOcean und Linode geben keine Nutzerdaten über ihre API zurück. Vultr gibt sie an jeden Schlüssel zurück, der die Instanz lesen kann, und EC2 über `DescribeInstanceAttribute`. Bei AWS sollten Sie dem Verifizierer nur die drei Aktionen aus der Tabelle gewähren, niemals `ec2:Describe*`. Bei Vultr ist davon auszugehen, dass der Schlüssel des Verifizierers beide Token lesen kann. Ein Tunnel-Token ermöglicht es jemandem, einen zweiten Connector auszuführen: `verify` meldet jeden Connector, der sich nicht auf dem Server befindet, und die Aussagen des Collectors können auf diese Weise nicht gefälscht werden, da jede einzelne eine neue Challenge signiert. Bei `--quick-tunnel` dem zweiten Geheimnis handelt es sich stattdessen um den Adressschlüssel: Wer ihn liest, kann eine falsche Adresse posten, die das Panel akzeptieren würde.

In der öffentlichen Erklärung des Erfassers werden die Serveradresse und die Quellen der Anmeldungen nicht genannt; beides verbleibt im signierten Protokoll.

## Debug-Bereitstellung und Sperre

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` Verwaltet SSH für einen Schlüssel von einer Adresse oder einem kleinen Netzwerk, höchstens ein /24 für IPv4 oder ein /48 für IPv6. `KEY` ist bereits beim Anbieter registriert: der Name oder die ID eines SSH-Schlüssels im Hetzner-Projekt, die ID oder der Fingerabdruck eines SSH-Schlüssels im DigitalOcean-Team, ein Linode-Benutzername, dessen Profil-SSH-Schlüssel zu „root“ hinzugefügt wurden, die ID eines SSH-Schlüssels im Vultr-Konto oder der Name eines EC2-Schlüsselpaars in der Region. Diese Optionen gelten nicht für `generic`. Eine solche Bereitstellung wird als `debug` und wird **niemals** als „High-Assurance“ gemeldet. Wenn Sie fertig sind, führen Sie `sudo tgwitness-lock` als letzten Befehl der letzten SSH-Sitzung aus und gehen Sie anschließend wie folgt vor:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Die Firewall verliert jede eingehende Regel. Berichte zeigen dann an, wann SSH zugelassen war und wann es geschlossen wurde; dieses Fenster bleibt sichtbar.

## Bereitstellung entfernen

`destroy` Löscht den Server und seine Firewall, die anhand des Labels der Bereitstellung identifiziert werden, sodass auch eine Bereitstellung, die auf halbem Weg fehlgeschlagen ist, entfernt wird, sowie anschließend die DNS-Einträge, die auf den Tunnel verweisen, und den Tunnel selbst. Das Journal und der Signaturschlüssel des Servers werden ebenfalls gelöscht: Exportieren Sie zuvor die Beweismittel. Der Datensatz bleibt erhalten und wird `removed`, mit den API-Aufrufen der Entfernung.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Die Löschung über die API ist für Hetzner implementiert. Bei anderen Anbietern `destroy` wird vor dem Löschen angehalten und das zu löschende Label in der Konsole des Anbieters benannt. Ein manuell installierter Server (`generic`) verliert lediglich seinen Tunnel und seine DNS-Einträge. Eine schnelle Tunnel-Bereitstellung benötigt kein Cloudflare-Token: Der Tunnel endet beim Server, und die Beiträge verfallen bei ntfy.sh innerhalb von 12 Stunden.

## Beliebiger Server (selbstzertifiziert)

`--provider generic` gilt für einen Server, der gekauft oder manuell installiert wurde. `deploy` Erstellt den Tunnel und die DNS-Einträge, schreibt `install.sh` (privat) und `install.redacted.sh` (zur Veröffentlichung) und wartet. Kopieren `install.sh` auf einen frisch installierten Ubuntu 24.04-Server und führen Sie es dort aus:

```
sudo bash install.sh
```

Es erfasst den Host in seinem ursprünglichen Zustand (Anmeldungen, Konten, `authorized_keys`, empfangende Sockets, Dienste, geplante Aufgaben, Pakete), installiert den Commit, aktiviert die Host-Firewall, löscht sich selbst, maskiert SSH und beendet die Sitzung. Der Bericht für einen solchen Server ist bestenfalls **SELBSTBESCHEINIGT**: Wer auch immer das Installationsprogramm ausgeführt hat, verfügte zuvor über Root-Rechte, und dem Prüfer steht kein Anbieterprotokoll zur Verfügung. Es ist dennoch besser als ein ungeklärter Server: Die Bestandsliste, der Hash des Installationsprogramms und jede spätere Anmeldung sind signiert.

## Überprüfen

Der Prüfer benötigt `deployment.json`den veröffentlichten Installer, schreibgeschützte Zugangsdaten und, im Idealfall, einen Checkout des Commits sowie einen Nachweis ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Jeder Anbieter und jeder Cloudflare-Wert wird vom Verifizierer zu diesem Zeitpunkt angefordert; der Datensatz liefert lediglich die IDs, nach denen gefragt werden soll. Der Exit-Code lautet 0 für **„PASS“**, 1 für **„FAIL“** und 2 für **„REVIEW“**, **„INCOMPLETE“** oder **„SELF-ATTESTED**“. `--fingerprint` sollte von einem unabhängigen Kanal stammen; ohne diesen wird der Schlüssel nur mit dem Datensatz des Betreibers verglichen. `python verify.py` überprüft den Nachweis ZIP weiterhin selbst, wie in [„Evidence“ beschrieben](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/).

Anbieteraktionen werden klassifiziert: Erstellung und Start innerhalb von 30 Minuten nach der Erstellung werden akzeptiert; Konsole, Rettung, Passwortzurücksetzung, Neuinstallation, ISO, Images, Snapshots, Backups, Systems Manager, EC2 Instance Connect und Firewall-Öffnungen werden abgelehnt; Stromversorgungsaktionen und alles Unerwartete werden zur Überprüfung markiert. Eine unbekannte Aktion wird niemals unbemerkt durchgelassen.

## Bericht zur Übergabe von Beweismitteln

`--report report.md` schreibt den Markdown-Bericht und `report.json` daneben:

1. Ergebnis, Fingerabdruck des Collector-Schlüssels, Bereitstellung, Anbieter, Commit, Server, Firewall, Tunnel;
2. jede Überprüfung mit ihrem Status und ihrer Quelle (Anbieter-API, Cloudflare-API, Collector-Auszug, Beweisjournal);
3. das Anbieterprotokoll mit der Bewertung jeder Aktion und, sofern vom Anbieter erfasst, dem Ausführenden;
4. die Cloudflare-Endpunkte, die die Verbindungen, die Konfiguration und das Audit-Protokoll des Tunnels enthalten;
5. die signierte Erklärung des Sammlers;
6. Was der Bericht feststellt und was nicht;
7. Befehle zur Reproduktion sowie das SHA-256-Element jeder Datei, die ihm übergeben wurde.

Übergeben Sie den Bericht, `report.json`, `deployment.json`, das veröffentlichte Installationsprogramm und die Beweismittel ZIP. Erstellen Sie den Bericht frühzeitig: Die Protokolle der Anbieter werden nur für einen begrenzten Zeitraum aufbewahrt.

## Cloudflare als externer Zeuge

Alles hier ist optional. Auch ohne Cloudflare-Konto läuft der Server weiterhin, und zwei davon sind derzeit in Betrieb:

| Was | Was es zeigt | In TgWitness |
| --- | --- | --- |
| Schnelltunnel oder der Tunnel Ihrer Domain | Das Panel ist ausschließlich über den Tunnel erreichbar. | Der Server-Assistent, siehe oben |
| drand-Relay `drand.cloudflare.com` | Die Einträge nach einer „drand“-Runde sind neuer als dieser: Das Tagebuch wurde fortlaufend verfasst. | Beweismodus, **Weitere Zeugen**, kein Konto ([Format](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Benachrichtigungen zum Tunnelstatus | wenn der Tunnel ausgefallen war, per E-Mail oder Webhook von Cloudflare | Richten Sie diese im Cloudflare-Dashboard ein |
| Gateway-DNS (`--gateway-dns`oder **Cloudflare Gateway DNS** im Assistenten) | Jeder Name, den der Server abgefragt hat, wurde von Cloudflare über TLS beantwortet; die Hetzner-Firewall lässt keine anderen DNS-Zugriffe zu; ob eine Gateway-Richtlinie Antworten umschreiben könnte | Hetzner, kostenloser Zero-Trust-Tarif, keine Domain; `verify` überprüft die Firewall, den Standort, die Protokollierung, die Richtlinien, die Serverabfragen und das Audit-Protokoll; der „Evidence-Modus“ kopiert das Protokoll in das Journal |
| Gateway zum Cloudflare One-Client auf dem Server, eine ausgehende Firewall, die nur Cloudflare zulässt | jede vom Server hergestellte Verbindung, nicht nur DNS | noch nicht implementiert |
| Zugriff vor dem Panel | Wer hat sich wann im Panel angemeldet? | noch nicht implementiert: erfordert eine eigene Domain |
| Protokollierung von SSH-Befehlen | Jeder Befehl in einer Debug-Sitzung | noch nicht implementiert |

„Logpush“, das eine eigene Kopie von Cloudflare in R2 speichern würde, ist eine Enterprise-Funktion: Im kostenlosen Tarif antwortet Cloudflare `logpush is not enabled for this account`. Das Gateway-Protokoll bleibt dort 24 Stunden lang erhalten, sodass es im „Evidence Mode“ in das signierte Journal kopiert wird (**das Protokoll des Cloudflare Gateways über die DNS-Abfragen dieses Servers**, ein schreibgeschütztes Token mit „Account Analytics Read“).

Ohne einen Zero-Trust-Plan hat ein Konto einen DNS-Standort. Wenn Cloudflare einen weiteren ablehnt, nutzt der Server den bestehenden, und seine Abfragen werden anhand ihrer Adresse unterschieden; dieser Filter benötigt ebenfalls „Zero Trust PII Read“ und `destroy` hinterlässt einen gemeinsam genutzten Standort. Eine Protokollabfrage erstreckt sich über höchstens drei Stunden, sodass das Kopieren und `verify` Lesen des Tages in Drei-Stunden-Fenstern.

„Gateway DNS“ umfasst den System-Resolver. DNS über HTTPS auf Port 443 zu einem anderen Resolver sowie Verbindungen zu einer Adresse, die nirgendwo nachgeschlagen wird (zum Beispiel zu den Rechenzentren von Telegram), werden nicht im Protokoll erfasst.

Cloudflare hat keinen Einblick in die Verschlüsselung von Telegram, in andere Geräte des Telegram-Kontos (die Geräteliste im „Evidence Mode“ erfasst diese von Telegram-Seite aus) oder in den Hypervisor des Anbieters.

Am 1. November 2026 lief Gateway DNS gegen die echte Hetzner-Cloud und ein kostenloses Cloudflare-Konto: Hetzner akzeptierte die ausgehenden Regeln, der Server installierte v0.7.0, wobei jede Abfrage über Gateway via TLS lief, der Quick-Tunnel funktionierte durch diese Firewall hindurch, und `verify` las die 19 Namen des Servers von Cloudflare zurück (Ubuntu- und Hetzner-Mirrors, GitHub, PyPI, NTP, den Tunnel, ntfy.sh). Das Panel kopierte 36 Abfragen in acht Fenstern in ein Protokoll und `verify.py` fasste sie lückenlos zusammen; `destroy` entfernte den Server und die Firewall und verließ den gemeinsamen Standort.

## Was damit nicht festgelegt wird

- Der Anbieter und seine Mitarbeiter verwalten den Hypervisor, die Festplatten und das Netzwerk.
- Die Host-Messwerte werden vom Collector selbst gemeldet.
- Frühere Inhalte von Firewall-Regeln sind nicht in jedem Provider-Protokoll enthalten; nur Linode speichert Regelversionen.
- Es enthält keine neuen Informationen zur Authentizität von Nachrichten; siehe [„Evidence](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)“.

## Hier getestet

Die Logik für Bereitstellung, Sperrung und Verifizierung wird durch automatisierte Tests anhand simulierter Hetzner-, DigitalOcean-, Linode-, Vultr-, EC2/CloudTrail- und Cloudflare-APIs abgedeckt, die auf der Grundlage der veröffentlichten API-Referenzen erstellt wurden, sowie durch die Signierung von AWS-Anfragen gemäß den von AWS veröffentlichten Beispielen. `tools/check_cloud_wizard.py` führt den Server-Assistenten des Panels auf dieselbe Weise aus, mit einer Domain und mit einem Schnell-Tunnel. `tools/check_tdx.py` überprüft echte Intel-TDX-Attestationen aus dcap-qvl und dstack bis hin zum Intel-Stammzertifikat (Quellen in [tools/tdx/README.md](https://github.com/phishdestroy/TgWitness/blob/main/tools/tdx/README.md)); `tools/check_phala.py`führt die Befehle „deploy“, „verify“, „journal“, „destroy“ sowie den Panel-Assistenten auf einer simulierten Phala Cloud aus, deren Zertifikate aus einer gefälschten, der von Intel nachempfundenen PKI stammen. Der Phala-Pfad wurde noch nicht auf der Phala Cloud selbst getestet.

Am 1. November 2026 lief der „Quick Tunnel Path“ gegen echtes **Hetzner Cloud** (Nürnberg, `cpx22`, TgWitness v0.7.0), echtes ntfy.sh und GitHub, sowohl über das Bedienfeld als auch über den Code:

- Preisüberprüfung, anschließend Erstellung über die Schaltflächen des Panels: Server läuft nach 13 Sekunden, signierte Erklärung mit übereinstimmenden Instanz- und Installer-Hashes nach etwa zwei Minuten;
- Das servereigene Panel wurde über die Adresse trycloudflare.com geöffnet und akzeptierte das Panel-Token; ohne das Token gibt es den Status 401 zurück;
- Nach einem Neustart über die Hetzner-API veröffentlichte der Server eine neue signierte Adresse. **Die aktuelle Adresse** wurde gefunden, die alte Adresse reagierte nicht mehr, der Signaturschlüssel blieb gleich; ein nicht signierter Beitrag zu einem ntfy.sh-Thema wurde ignoriert;
- `verify` in Bezug auf die API von Hetzner: Server, Firewall ohne eingehende Regeln, Statement, Bindung, Host-Messungen, Boot sowie der Quell-Hash eines v0.7.0-Checkouts wurden bestanden; die Cloudflare- Prüfungen waren, wie oben beschrieben, nicht verfügbar; der Installer unterschied sich von dem, den v0.7.0 erstellt, und stimmte Byte für Byte mit dem überein, den der Code dieser Version erstellt;
- Durch das Löschen aus dem Panel wurden genau der Server und die Firewall entfernt, die mit der Bereitstellung gekennzeichnet waren; andere Server und Firewalls im selben Projekt blieben davon unberührt.

Noch nicht mit echten Konten getestet: eine Bereitstellung unter Ihrer eigenen Domain (Cloudflare-Tunnel und DNS), die anderen Anbieter, eine Debug-Bereitstellung und `lock`, ein Telegram-Konto auf einem solchen Server sowie die Live-Updates späterer Versionen über einen Quick-Tunnel. Überprüfen Sie die erste Bereitstellung bei jedem Anbieter mit `plan`, einer Debug-Bereitstellung und `verify` , bevor Sie sich in einem Fall darauf verlassen.
