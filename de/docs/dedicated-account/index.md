# Verwenden Sie ein separates Konto. Niemals Ihr Hauptkonto.

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/dedicated-account/

Bitte lesen Sie dies, bevor Sie ein Konto verbinden

Unsere Empfehlung, Ihr Hauptkonto nicht zu verwenden, ist kein Scherz. Es ist die Realität.

Hauptkonto

- Ihr eigener App-Hash: 99 % abgemeldet
- Sperren allein aufgrund eines niedrigen Vertrauensniveaus kommen häufig vor
- Die Verwendung davon ist eine wirklich dumme Idee

Zusätzliches Konto für öffentliche Paare

- Über eine Million Konten wurden über diese Paare registriert
- Die Paare bestehen seit mehr als 5 Jahren
- Niemand kann über diese Ihre Daten einsehen

01

## Warum nicht Ihr Hauptkonto?

Dies sind korrekte Informationen. Wir wissen genau, wo die Fallstricke dieser Probleme liegen.

1. ### Ihr eigener App-Hash: 99 % abgemeldet

   Wenn Sie sich von einem Konto aus, auf das Sie keinen Zugriff haben, bei my.telegram.org anmelden, um einen App-Hash zu erhalten, und anschließend eine Anfrage über diesen App-Hash stellen, bedeutet dies mit einer Wahrscheinlichkeit von 99 %, dass das Konto abgemeldet ist. Sie können dies überprüfen.
2. ### Sperren allein aufgrund eines niedrigen Vertrauensniveaus kommen häufig vor

   Konten werden allein deshalb gesperrt, weil Telegram ihnen nicht vertraut, und solche Sperrungen kommen häufig vor. Auch dies können Sie überprüfen. Die Verwendung Ihres eigenen Kontos ist eine wirklich dumme Idee.
3. ### Kopierte Sitzungsschlüssel können widerrufen werden

   Die gleichzeitige Nutzung eines importierten TData- oder Sitzungsschlüssels in Telegram Desktop und TgWitness kann den Fehler `AUTH_KEY_DUPLICATED` auslösen. Telegram widerruft dann diese Autorisierung; beide Kopien erfordern eine erneute Anmeldung. Auch ein eigens dafür eingerichtetes Konto verhindert das nicht.

   Beenden Sie den ursprünglichen Client vollständig und lassen Sie ihn geschlossen, während Sie dessen importierte Sitzung nutzen. Für die parallele Nutzung melden Sie sich per Telefon oder QR bei TgWitness an, um eine separate Autorisierung zu erstellen; andere separat autorisierte Clients können angemeldet bleiben.

   [Lesen Sie die Warnung zum Importieren der Sitzung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de#session-warning)

Telegram-Dokumentation

- [Fehler beim Abmelden: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [Erstellen eines eigenen App-Hashs: Abrufen der `api_id`](https://core.telegram.org/api/obtaining_api_id)

02

## Warum TgWitness über öffentliche App-Hash-/App-ID-Paare funktioniert

Aus diesem Grund haben wir TgWitness auf öffentlichen App-Hash-/App-ID-Paaren aufgebaut. Nach unserer Logik ist die Wahrscheinlichkeit von Sperren bei diesen Paaren geringer: Mehr als eine Million Telegram-Konten wurden über diese Paare registriert, und viele verschiedene Programme arbeiten mit ihnen. Unserer Logik zufolge ist dies besser, als direkt mit einem persönlichen App-Hash zu arbeiten: Diese Paare bestehen mit Sicherheit seit mehr als fünf Jahren.

### Ihr eigenes neues Schlüsselpaar

Erstellt auf my.telegram.org über das Konto.

- Etwa 99 % der Konten sind abgemeldet
- Eine neue Anwendung, ein Konto

### Öffentliche Schlüsselpaare des Pools

Dieselben API-Paare, die auch viele andere Programme verwenden.

- Über eine Million registrierte Konten
- Viele verschiedene Programme
- Seit mehr als 5 Jahren tätig

### Warum niemand über diese Paare etwas von Ihnen sehen kann

- #### Das Paar ist ein Name, kein Schlüssel

  Telegram fragt die API-ID und den API-Hash ab, wenn sich ein Programm verbindet und wenn es einen Anmeldecode anfordert. Diese identifizieren die Anwendung und gewähren keinerlei Zugriff auf ein Konto; in der Dokumentation von Telethon wird darauf hingewiesen, dass ein solches Paar mit jeder beliebigen Telefonnummer funktioniert.
- #### Ihr Sitzungsschlüssel verlässt niemals Ihren Server

  Bei der Anmeldung wird durch einen Diffie-Hellman-Austausch zwischen Ihrem TgWitness und Telegram ein Autorisierungsschlüssel erstellt; der Schlüssel selbst wird niemals übertragen. Laut der Telegram-Dokumentation wird der Schlüssel nach der Autorisierung dem Nutzer zugeordnet, und jeder Aufruf mit diesem Schlüssel wird als dieser Nutzer ausgeführt. Andere Programme mit demselben Schlüsselpaar verfügen über eigene Schlüssel und können Ihren nicht verwenden.
- #### Der Datenverkehr wird mit Ihrem Schlüssel verschlüsselt

  Jede Anfrage und Antwort wird mit dem Autorisierungsschlüssel der Sitzung verschlüsselt, nicht mit dem API-Hash. Die Kenntnis des API-Hashs ermöglicht keine Entschlüsselung.
- #### Der Inhaber eines Paares sieht nichts

  Telegram verfügt über keine Methode, um Konten, Sitzungen oder Nachrichten anhand der API-ID aufzulisten. Der Inhaber eines Paares sieht auf my.telegram.org lediglich seine eigenen App-Einstellungen.
- #### Nur Ihr Konto erkennt, um welche App es sich handelt

  Unter „Einstellungen → Geräte“ Ihres eigenen Kontos werden für jede Sitzung der App-Name und die API-ID, das Gerät, die IP-Adresse sowie die Daten aufgeführt. Niemand sonst erhält diese Liste.

Telegram-Dokumentation

- [Benutzerautorisierung: Der Schlüssel wird zum Benutzer](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [Erstellen eines Autorisierungsschlüssels](https://core.telegram.org/mtproto/auth_key)
- [MTProto-Verschlüsselung](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Was ein Sitzungsprotokoll enthält](https://core.telegram.org/constructor/authorization)
- [Abrufen der api_id](https://core.telegram.org/api/obtaining_api_id)
- [Der Open-Source-Code der Telegram-Apps](https://telegram.org/apps#source-code)

Bibliotheken und Diskussionen

- [Telethon: Anmelden](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: Offizielle App-APIs](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: Sollte der „api_hash“ geheim gehalten werden?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Die entsprechenden Paare in anderen Programmen7

Die API-Paare der offiziellen Telegram-Apps sind öffentlich und in viele unabhängige Programme und Bibliotheken eingebaut:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Forum-Liste offizieller App-Paare, veröffentlicht zur Registrierung von Konten

03

## Möglichkeiten zur Erstellung eines zusätzlichen Kontos

Ein Telegram-Konto benötigt eine Telefonnummer, an die der Anmeldecode gesendet wird. Wählen Sie diese entsprechend der gewünschten Lebensdauer des Kontos aus.

- Beste Wahl

  ### Prepaid-SIM oder eSIM

  ********

  Letzte

  Solange Sie es immer auf dem neuesten Stand halten

  Bitte beachten Sie

  Am zuverlässigsten: Telegram akzeptiert echte Mobilfunknummern am besten. Eine Nummer, die der Netzbetreiber zurücknimmt, wird an jemand anderen vergeben.
- ### App für virtuelle Rufnummern

  ********

  Letzte

  Solange die App die Rufnummer für Sie reserviert

  Bitte beachten Sie

  Telegram kann eine virtuelle Nummer ablehnen, den Code nicht zustellen oder das neue Konto sofort einschränken; manche Apps ziehen nicht genutzte Nummern wieder zurück.
- ### Nummernvermietung

  ********

  Letzte

  Die Mietdauer

  Bitte beachten Sie

  Nach Ablauf der Mietdauer erhält der nächste Kunde die Rufnummer.
- ### Einmalige Aktivierung

  ********

  Letzte

  Ein Code

  Bitte beachten Sie

  Die Nummer wird sofort in den Pool zurückgeführt, oft zusammen mit einer Historie früherer Besitzer. Legen Sie als Erstes das Cloud-Passwort fest.

Wer auch immer die Nummer später besitzt, kann einen Anmeldecode anfordern. Ein Cloud-Passwort (zweistufige Verifizierung) verhindert, dass sich diese Person anmeldet; ohne dieses Passwort gehört das Konto dem nächsten Inhaber der Nummer.

Telegram-Dokumentation

- [Spam-FAQ: Virtuelle Nummern und frühere Inhaber](https://telegram.org/faq_spam)
- [Zweistufige Verifizierung](https://core.telegram.org/api/srp)

### Gemietete +888-Nummern (Fragment)

Einige Marktplätze und Dienste bieten die vorübergehende Anmietung der offiziellen +888-Nummern von Telegram über Fragment an.

Ungefährer Preis: 20 US-Dollar pro Tag.

- Sie können ein Konto direkt in Telegram Web oder Telegram Desktop registrieren.
- Sie können Konten unter der angegebenen Nummer löschen und neue anlegen.
- Diese Konten unterliegen in der Regel weniger Betrugsschutzprüfungen, bieten jedoch keine Immunität oder besondere Privilegien.

Die Nummer gehört nicht Ihnen. Nach Ablauf der Mietdauer kann der Eigentümer sie zurückfordern. Legen Sie umgehend ein Cloud-Passwort fest und betrachten Sie das Konto nicht als langfristig.

Es ist nach wie vor zuverlässiger, wenn Sie die Nummer +888 selbst besitzen oder eine Prepaid-SIM-Karte verwenden, über die Sie die Kontrolle haben.

### Fertigkonten von Marktplätzen

Einige Marktplätze (zum Beispiel G2G oder Z2U) verkaufen vorgefertigte Telegram-Konten – neu, mit Alterung oder mit Sitzungsdateien.

- [G2G: Telegram-Kontoangebote](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Telegram-Kontoangebote](https://www.z2u.com/telegram/accounts-5-15140)

VERWENDEN SIE NIEMALS IHR HAUPTKONTO! Ein auf diese Weise eingerichtetes separates Konto ist immer noch sicherer, als Ihr primäres Telegram-Konto in TgWitness einzurichten.

#### Warnhinweise vor dem Kauf

- Dies verstößt gegen die Nutzungsbedingungen von Telegram.
- Viele Konten wurden massenhaft registriert (Auto-Reg) oder weisen eine unbekannte Historie auf.
- Einige Verkäufer verfügen möglicherweise noch über einen Wiederherstellungszugang.
- Konten aus solchen Märkten werden häufig später gesperrt oder eingeschränkt.
- Vermeiden Sie Marktplätze, auf denen offen Stealer, Phishing-Tools oder eindeutig gestohlene Konten verkauft werden.
- Der Kauf eines Kontos – selbst eines, das als „Auto-Reg“ beworben wird – von Plattformen, die offen Phishing-Tools, Stealer, gestohlene Sitzungen oder Konten verkaufen, verstößt nicht nur gegen die Nutzungsbedingungen von Telegram, sondern auch gegen die Gesetze der meisten Länder. Dies kann Ihre Beweise später ungültig machen. Wählen Sie sorgfältig aus.

#### Wenn Sie diese Option nutzen

1. Behandeln Sie den Account als Einweg-Account.
2. Beenden Sie alle anderen Sitzungen, richten Sie ein Cloud-Passwort ein und ändern Sie unverzüglich die Wiederherstellungsmethoden.
3. Verwenden Sie 2–3 Konten von verschiedenen Anbietern oder Konten, die Sie selbst registriert haben.

**Premium, Löschung und die siebentägige Verzögerung**

Verfügt das Konto über „Premium“, kann eine Person mit Zugriff auf die Telefonnummer das Konto nicht sofort löschen. Sie erhalten eine Benachrichtigung und haben sieben Tage Zeit, bevor die Löschung erfolgt.

Dies ist wichtig, da Ihre Untersuchung von diesem Konto abhängt: Sie haben Zeit, einen Ersatz vorzubereiten.

**Neue Konten und API-Zugangsdaten**

Wenn Sie Ihre eigene „api_id“/„api_hash“ von einem neuen Konto beziehen und verwenden, das Sie selbst mit einer Nummer aus einem SMS-Dienst registriert haben, wird das Konto bei der ersten API-Anfrage oder Sitzungsautorisierung abgemeldet. Bitte berücksichtigen Sie dies bei der Planung einer Untersuchung.

04

## Erstellen des Kontos

Von einer Nummer bis zum ersten aufgezeichneten Chat.

1. ### Erhalten Sie eine Nummer

   Eine Prepaid-SIM-Karte oder eSIM, wenn das Konto langfristig bestehen soll; eine gemietete Karte oder eine einmalige Aktivierung für einen kurzfristigen Auftrag. Die Dienste sind unten aufgeführt.
2. ### Registrieren Sie sich getrennt von Ihrem Hauptkonto

   Registrieren Sie sich in der offiziellen Telegram-App auf einem separaten Gerät, Emulator oder Telefonprofil, nicht neben Ihrem Hauptkonto.
3. ### Sichern Sie es mit einem Cloud-Passwort

   Legen Sie umgehend ein Cloud-Passwort und eine Wiederherstellungs-E-Mail-Adresse fest, die nirgendwo sonst verwendet werden.
4. ### Schließen Sie die Datenschutzeinstellungen

   Telefonnummer **„Niemand“**, „Finden Sie mich über meine Nummer“, **„Meine Kontakte**“, „Zuletzt gesehen“, Profilfotos und Biografie: **„Niemand“** oder **„Meine Kontakte“**; deaktivieren Sie die Kontaktsynchronisierung.
5. ### Verhindern Sie, dass es sich selbst zerstört

   Stellen Sie die Selbstlöschfunktion des Kontos auf den längsten Zeitraum ein, damit ein gestopptes TgWitness Ihnen nicht den Verlust des Kontos verursacht.
6. ### Verleihen Sie dem Ganzen ein neutrales Profil

   Keine Namen, Fotos, Benutzernamen oder Biografien aus Ihren anderen Konten, keine persönlichen Kontakte.
7. ### Lassen Sie es sich erst einmal einlaufen

   Treten Sie zunächst täglich nur einigen Chats bei. Neue Konten, die es überstürzen, werden zunächst eingeschränkt.
8. ### Geben Sie keine Informationen an Bots weiter

   Klicken Sie bei einem Bot niemals auf „Telefonnummer teilen“ oder „Standort teilen“. Öffnen Sie Links und Mini-Apps über ein VPN oder einen Proxy auf diesem Gerät.
9. ### Verbinden Sie es mit TgWitness

   Stellen Sie in Ihrem eigenen Arbeitsbereich über **„Konto → QR-Code**“ eine Verbindung her und klicken Sie anschließend auf **„Quellen → Untersuchungsmodus**“. In der App führen Sie Ihre Aktionen durch, TgWitness dient der Aufzeichnung.

Telegram-Dokumentation

- [Zweistufige Verifizierung](https://core.telegram.org/api/srp)
- [Datenschutzeinstellungen](https://core.telegram.org/api/privacy)
- [Selbstlöschung des Kontos](https://core.telegram.org/method/account.setAccountTTL)

05

## Nummerndienste

Ausgangspunkte. Länder, Preise und die Frage, ob Telegram eine Nummer akzeptiert, ändern sich häufig; bitte überprüfen Sie dies vor der Zahlung.

### Prepaid-SIM und eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Prepaid

  PayGo-Tarif, sehr günstig
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Prepaid
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Prepaid
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Prepaid
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Apps für virtuelle Rufnummern 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Nur in den USA; für die Registrierung ist eine US-Telefonnummer erforderlich
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Die Nummer wird zurückgenommen, wenn Sie sie nicht verwenden.
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Andere Länder
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - Kostenpflichtig

  Mit einer Testphase
- [Hushedhushed.com](https://hushed.com)

  - Viele Länder
  - Kostenpflichtig

  Günstig
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Europäische Mobilfunknummern in einer App
- [Sonetelsonetel.com](https://sonetel.com)

  - Viele Länder
  - Kostenlose Rufnummer
- [Zadarmazadarma.com](https://zadarma.com)

  - Viele Länder

  Virtuelle Nummern

### Anzahl der Anmietungen und Aktivierungen: 12

Die Mietnummer bleibt über Wochen oder Monate hinweg gültig. Bei einer einmaligen Aktivierung erhalten Sie einen einmaligen Code: Legen Sie das Cloud-Passwort unmittelbar nach der Registrierung fest.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Vermietung
  - Aktivierungen
- [SMSPVAsmspva.com](https://smspva.com)

  - Vermietung
  - Aktivierungen
- [5SIM5sim.net](https://5sim.net)

  - Vermietung
  - Aktivierungen
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Vermietung
  - Einmalig
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Vermietung
  - Aktivierungen
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Vermietung
  - Aktivierungen
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Vermietung
  - Aktivierungen
- [365SMS365sms.org](https://365sms.org)

  - Vermietung
  - Aktivierungen
- [SIMSMSsimsms.org](https://simsms.org)

  - Vermietung
  - Aktivierungen
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Einmalig
- [SMS-MANsms-man.com](https://sms-man.com)

  - Einmalig
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Einmalig
