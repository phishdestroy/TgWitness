# Wdrożenie o wysokim poziomie bezpieczeństwa

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/

Zabezpieczony serwer działający 24 godziny na dobę, 7 dni w tygodniu, w chmurze Hetzner lub Phala Cloud, bramka DNS oraz testy, które może powtórzyć strona trzecia.

Podpisany dziennik potwierdza, że zapisy nie zostały zmienione **po** podpisaniu. W poważnych przypadkach kolejnym pytaniem jest to, czy ktoś mógł manipulować danymi **przed** ich podpisaniem: kto uruchomił moduł zbierający dane, na jakim komputerze oraz czy ktoś się do niego zalogował. Ten opcjonalny tryb wdraża moduł zbierający dane w taki sposób, aby strona trzecia mogła to sprawdzić, korzystając z zapisów przechowywanych przez dostawcę usług w chmurze i Cloudflare, a nie opierając się wyłącznie na słowie operatora.

Zwykłe korzystanie z wersji lokalnej i Docker pozostaje bez zmian. Nic tutaj nie działa, dopóki nie wdrożysz za pomocą `python -m tgwitness.cloud`, a kolektor odczytuje dane z hosta tylko wtedy, gdy wdrożenie ustawia `TGWITNESS_ASSURANCE`.

Schemat blokowy · Operator → Serwer, zapora sieciowa bez reguł przychodzących (API dostawcy); Operator → Tunel i DNS (API Cloudflare); Serwer, zapora sieciowa bez reguł przychodzących → Tunel i DNS (tylko wychodzące); Serwer, zapora sieciowa bez reguł przychodzących → Klucz podpisujący utworzony na serwerze; Verifier, tokeny tylko do odczytu → Dziennik dostawcy i zapora sieciowa; Verifier, tokeny tylko do odczytu → Adres łącznika tunelowego i ruch przychodzący; Verifier, tokeny tylko do odczytu → Podpisane oświadczenie /api/assurance; Verifier, tokeny tylko do odczytu → Plik ZIP z dowodami · Operator · Verifier, tokeny tylko doodczytu · Serwer, zapora sieciowabez reguł przychodzących · Dziennik dostawcy i zaporasieciowa · Adres łącznika tunelowegoi ruch przychodzący · Podpisane oświadczenie/api/assurance · Plik ZIP z dowodami · Tunel i DNS · Klucz podpisującyutworzony na serwerze · API dostawcy · API Cloudflare · tylko wychodzące

**Schemat w formie tekstowej**

1. Operator → Serwer, zapora sieciowa bez reguł przychodzących (API dostawcy)
2. Operator → Tunel i DNS (API Cloudflare)
3. Serwer, zapora sieciowa bez reguł przychodzących → Tunel i DNS (tylko wychodzące)
4. Serwer, zapora sieciowa bez reguł przychodzących → Klucz podpisujący utworzony na serwerze
5. Verifier, tokeny tylko do odczytu → Dziennik dostawcy i zapora sieciowa
6. Verifier, tokeny tylko do odczytu → Adres łącznika tunelowego i ruch przychodzący
7. Verifier, tokeny tylko do odczytu → Podpisane oświadczenie /api/assurance
8. Verifier, tokeny tylko do odczytu → Plik ZIP z dowodami

## Co może sprawdzić weryfikator

| Twierdzenie | Jak to jest sprawdzane | Prowadzona przez |
| --- | --- | --- |
| Serwer został utworzony za pośrednictwem API dostawcy w znanym momencie | Obiekt serwera i jego utworzenie w dzienniku dostawcy | Dostawca |
| Nikt nie korzystał ze ścieżek dostępu dostawcy | Dziennik żądań konsoli, odzyskiwanie, resetowanie hasła, odbudowa, ISO, obrazy, kopie zapasowe | Dostawca |
| Nie udało się nawiązać połączenia | Zapora dostawcy nie zawiera żadnych reguł przychodzących; połączenia SSH są ukrywane od pierwszego uruchomienia | Dostawca (zapora sieciowa), host (SSH) |
| Dostęp do panelu jest możliwy wyłącznie poprzez tunel | Ruch przychodzący przez tunel jest przekierowywany wyłącznie do panelu; łącznik działa z adresu serwera | Cloudflare |
| To właśnie to oprogramowanie działa | Podpisany skrót drzewa źródłowego kolektora jest równy kopii rozwijanej wersji wdrożonego commitu | Collector, zsynchronizowany z Git |
| Klucz podpisujący został utworzony na tym serwerze | Klucz podpisuje oświadczenie zawierające identyfikator serwera dostawcy oraz skrót otrzymanego pliku cloud-init | Collector, zweryfikowany przez dostawcę |
| Dziennik należy do tego klucza i serwera | Każdy proces rozpoczynający się w dowodzie ZIP zawiera pomiar hosta dla tego serwera | Dowody ZIP |

Pomiary hosta (nasłuchujące procesy SSH i inne procesy, bieżące sesje, logowania w `wtmp`, uruchomienie systemu) są zgłaszane przez sam moduł zbierający i podpisywane przy każdym uruchomieniu procesu oraz w `host.state` zapisów za każdym razem, gdy ulegną zmianie. Użytkownik z uprawnieniami roota na serwerze mógłby je sfałszować; dane te wspierają zapisy dostawcy i Cloudflare, a nie zastępują je.

## Dostawcy

| `--provider` | Dane uwierzytelniające | Dostęp tylko do odczytu dla weryfikatora | Dziennik dostawcy dla weryfikatora | Przechowywane w celu |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Token odczytu tego samego projektu | Działania serwera i zapory sieciowej | O ile zasoby te istnieją |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Osobisty token dostępu tylko do odczytu | Akcje Droplet | Dopóki Droplet istnieje |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` zakresy tylko do odczytu | Zdarzenia związane z kontami, wersje reguł zapory sieciowej | 90 dni |
| `vultr` | `VULTR_API_KEY` | Użytkownik z uprawnieniami do odczytu oraz `activity_logs` uprawnieniem | Dziennik aktywności konta (metoda, ścieżka, podmiot) | 30 dni, a przy subskrypcji dziennika audytowego – dłużej |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | Historia zdarzeń w CloudTrail | 90 dni |
| `phala` | `PHALA_CLOUD_API_KEY` | Klucz API tego samego obszaru roboczego | Zmiany w aplikacji: modyfikacje kodu i środowiska, ponowne uruchomienia, aktualizacje systemu operacyjnego | Chociaż aplikacja istnieje |
| `generic` | brak | brak | brak: **poświadczone samodzielnie** | – |

Dla każdej sprawy należy używać dedykowanego projektu, zespołu, konta lub subkonta: dzięki temu dostęp tylko do odczytu weryfikatora wyświetla wyłącznie to wdrożenie. Dane uwierzytelniające są odczytywane z `--provider-token-file` lub z powyższej zmiennej, nigdy z wiersza poleceń. W przypadku AWS plik zawiera `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; region to `--location`.

W każdym raporcie zaznaczono, czego nie pokazują zapisy poszczególnych dostawców. Krótko mówiąc: Hetzner rejestruje żądania konsoli; konsola odzyskiwania DigitalOcean, Lish/Glish firmy Linode oraz konsola internetowa Vultr nie są rejestrowane jako takie, więc uprawnienia roota są zablokowane przy pierwszym uruchomieniu, a logowanie do konsoli wymagałoby zresetowania hasła lub zmiany trybu rozruchu, co jest rejestrowane. Vultr zwraca adres konsoli na każdy klucz, który może odczytać instancję; ani zapis, ani raport tego nie przechowują.

## Poufna maszyna wirtualna w chmurze Phala Cloud (Intel TDX)

Gdy `--provider phala` kolektor działa w poufnej maszynie wirtualnej Intel TDX w [chmurze Phala Cloud](https://phala.com/), zarządzanej przez dstack. Host i pracownicy Phala nie mają dostępu do jej pamięci, a procesor podpisuje poświadczenie dotyczące tego, co uruchomiło się na maszynie. Weryfikator nie opiera się wyłącznie na zapewnieniach Phala: `tgwitness.tdx` samodzielnie sprawdza każde poświadczenie, aż do przypiętego certyfikatu Intel SGX Root CA, w oparciu o listy unieważnień firmy Intel oraz podpisane przez nią dane platformy, i odrzuca maszyny, które można debugować lub migrować.

| Wpis do raportu | Co pokazuje |
| --- | --- |
| `tdx_binding` | Poświadczenie obejmuje podpisane oświadczenie zbierającego oraz losową wartość niniejszego żądania. |
| `tdx_quote` | Firma Intel potwierdza ważność certyfikatu; certyfikat jest przyznawany wyłącznie wtedy, gdy Intel oceni platformę jako aktualną. |
| `tdx_compose_hash` | RTMR3, odtwarzany z dziennika zdarzeń dstack, mierzy liczbę operacji tworzenia wiadomości w aplikacji zgłaszanych przez moduł zbierający dane |
| `tdx_compose` | Ten kod jest bajt po bajcie identyczny z kodem wygenerowanym przez wdrożony commit: pliki źródłowe są przypisane na podstawie skrótu, oba obrazy na podstawie skrótu, nie ma żadnego innego kodu |
| `tdx_identity` | Poświadczenie pochodzi z wdrożonej aplikacji i instancji, przy użyciu kluczy z systemu KMS firmy Phala oraz zaszyfrowanego dysku |
| `tdx_os` | W przypadku `--tdx-measurements`, MRTD i RTMR0-2 są równe wartościom obliczonym na podstawie obrazu systemu operacyjnego dstack (`dstack-mr measure --json`) |

Każde uruchomienie kolektora zarejestrowane w dzienniku zawiera takie poświadczenie, więc `verify --evidence` sprawdza każdy uruchomienie. Lista wersji aplikacji Phala służy jako dziennik dostawcy: jeśli kompozytor uległ zmianie po wdrożeniu, raport kończy się niepowodzeniem.

W panelu wybierz opcję **„Poufna maszyna wirtualna · Phala Cloud”** w sekcji **„Dodatki** → **Serwer 24/7”** i wklej klucz API Phala Cloud; szybki tunel działa tak samo jak na Hetznerze. Z wiersza poleceń:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` odczytuje certyfikaty i listy unieważnionych certyfikatów firmy Intel z pliku zamiast pobierać je bezpośrednio od firmy Intel. Usługa Gateway DNS nie jest tutaj dostępna: Phala nie posiada zapory dostawcy dla ruchu wychodzącego.

Poświadczenie nie wyklucza istnienia luki w module TDX firmy Intel lub w mikrokodzie, ani fizycznego dostępu do magistrali pamięci. Ktokolwiek kontroluje aplikację na koncie Phala, może wdrożyć kolejny kompozyt; pojawia się on jako nowa wersja z nowym skrótem kompozytu. Host kontroluje źródło czasu urządzenia oraz sieć.

## Zanim zaczniesz

1. Strefa Cloudflare, jej identyfikator konta oraz token API z uprawnieniami **Cloudflare Tunnel Edit**, **Zone Read** i **DNS Edit**, podany wraz z `--cloudflare-token-file` lub `CLOUDFLARE_API_TOKEN`. Dla weryfikatora: **odczyt tunelu Cloudflare**, **odczyt DNS** oraz, w przypadku dziennika audytowego, **odczyt ustawień konta**. Bez domeny [szybki tunel](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#quick-tunnel-without-a-domain) nie wymaga żadnej z tych rzeczy.
2. Dane uwierzytelniające dostawcy z uprawnieniami do zapisu w dedykowanym projekcie; `lock` korzysta z tego samego:

   - Hetzner: token API z uprawnieniami do odczytu i zapisu;
   - DigitalOcean: osobisty token dostępu z uprawnieniami do zapisu;
   - Linode: osobisty token dostępu z `linodes`, `firewall` oraz `events` zakresami odczytu/zapisu;
   - Vultr: klucz API dedykowanego konta lub subkonta;
   - AWS: dozwolone są poświadczenia IAM `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` oraz `ec2:RevokeSecurityGroupIngress`.
3. Commit do uruchomienia. Tag wydania jest jednokrotnie rozpoznawany jako odpowiadający mu commit za pomocą `git ls-remote`; serwer otrzymuje zawsze wyłącznie 40-znakowy commit.

## Z panelu

Na własnym komputerze opcja **„Dodatki” → „Serwer 24/7”** uruchamia to samo `deploy` dla Hetznera w trzech krokach: wybierz Europę lub Stany Zjednoczone, wklej token Hetznera (odczyt i zapis), a następnie sprawdź typ serwera, miesięczną cenę, adres i wersję, które panel znalazł na podstawie tego tokenu. Nic nie zostanie utworzone przed potwierdzeniem. Panel pokazuje każdy krok, `deploy` zgłasza, a następnie adres, token panelu i odcisk palca klucza podpisu. Bez domeny serwer otrzymuje [szybki tunel](https://phishdestroy.github.io/TgWitness/pl/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; opcja **Twoje serwery → Znajdź aktualny adres** wyszukuje go ponownie po ponownym uruchomieniu. Aby uzyskać stały adres pod własną domeną, otwórz **Opcjonalne · własna domena** i dodaj token Cloudflare (przygotowany link wybiera opcje Odczyt strefy , Edycja DNS oraz Edycja tunelu Cloudflare).

Tokeny są przesyłane wraz z każdym żądaniem z karty przeglądarki do elementu TgWitness na tym samym komputerze i nie są nigdzie zapisywane; zapis wdrożenia, zredagowany plik cloud-init, token panelu oraz, w przypadku szybkiego tunelu, klucz adresu są przechowywane w `deployments/NAME` w katalogu danych. Panel udostępnia to wyłącznie głównemu administratorowi poprzez bezpośrednie połączenie typu loopback (`127.0.0.1`, bez nagłówków proxy ani tunelu); panel dostępny przez sieć wyświetla zamiast tego polecenia . Domyślną wersją jest tag wydania uruchomionego panelu, ustalany za pośrednictwem API GitHub. Lokalizacja, typ serwera i cena pochodzą z API Hetznera: `cpx22` tam, gdzie jest dostępna, w przeciwnym razie najtańszy typ x86 z co najmniej 2 GB pamięci.

## Szybki tunel bez domeny

`--quick-tunnel` zastępuje `--zone`, `--cloudflare-account` oraz `--panel-host`; nie jest wymagane żadne konto ani token Cloudflare:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Na serwerze usługa cloudflared otwiera [szybki tunel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) do panelu: losowy `https://….trycloudflare.com` adres, który zmienia się przy każdym ponownym uruchomieniu cloudflared lub serwera. Niewielka usługa na serwerze publikuje każdy adres w losowym temacie ntfy.sh , podpisując go (HMAC-SHA256) kluczem przechowywanym wyłącznie w katalogu wdrożeniowym (`address-key.txt`), i powtarza to co trzy godziny, ponieważ ntfy.sh przechowuje posty przez 12. `deploy` i **Find aktualny adres** akceptują wyłącznie podpisane posty, więc sfałszowany post nie może przekierować Ciebie i Twojego tokenu panelu na adres należący do kogoś innego. Temat znajduje się w rejestrze oraz w opublikowanym pliku cloud-init: każdy, kto je posiada, może odczytać aktualny adres, który nadal wymaga podania tokenu panelu. Serwer nie utrzymuje żadnego portu przychodzącego w żadnym przypadku.

Koszt: żadne konto Cloudflare nie przechowuje danych dotyczących szybkiego tunelu, więc `verify` raportuje, że tunel, łącznik i sprawdzanie DNS są niedostępne, a wynik to w najlepszym razie `incomplete`; zapisy dostawcy, zapora sieciowa, podpisane oświadczenie, pomiary hosta oraz porównanie instalatorów są sprawdzane jak zwykle. Porównanie bajtów z instalatorem referencyjnym wymaga wdrożonego commitu, który już zna `--quick-tunnel`; pobranie wersji 0.7.0 kompiluje instalator domeny i zgłasza różnicę. Cloudflare nie udziela gwarancji dostępności szybkich tuneli, zezwala na 200 żądań w toku i nie obsługuje zdarzeń Server-Sent Events, więc aktualizacje panelu na żywo (wersje po 0.7.0) mogą nie docierać przez tunel i konieczne jest ponowne załadowanie widoku; ta część nie została przetestowana. W przypadku , który musi działać niezawodnie, użyj własnej domeny.

## Wdrożenie

Najpierw sprawdź wszystko, co zostanie wysłane. `plan` nie wysyła żadnych żądań do dostawcy ani do Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Następnie należy przeprowadzić wdrożenie przy użyciu tych samych opcji i danych uwierzytelniających:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Typy serwerów na początek: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` oraz `--image` domyślnie na system Ubuntu 24.04 każdego dostawcy w regionie europejskim.

`--repository` pobiera commit z innego repozytorium Git dostępnego przez https, bez podawania danych uwierzytelniających w adresie URL (domyślnie `https://github.com/phishdestroy/TgWitness.git`). `deploy` akceptuje również `--out` inny katalog wdrożeniowy (domyślnie `deployments/NAME`; katalog, w którym znajduje się już wdrożenie, jest odrzucany) oraz `--wait`, czas w minutach, przez który należy czekać na podpisane oświadczenie kolektora: od 1 do 240, domyślnie 20 lub 60 dla `generic`.

Polecenie:

1. tworzy tunel Cloudflare, którego ruch przychodzący przekierowuje nazwę hosta panelu do panelu oraz, jeśli została podana, nazwę hosta świadka do `/api/witness/head` i `/api/assurance` wyłącznie;
2. tworzy rekordy CNAME z serwerem proxy dla tych nazw hostów, odrzucając nazwy, które już istnieją;
3. tworzy zaporę dostawcy bez reguł przychodzących oraz serwer za nią bez klucza SSH, bez kopii zapasowych, bez agenta konsoli oraz z cloud-init, który maskuje SSH, blokuje uprawnienia roota, instaluje `cloudflared`, pobiera dokładnie ten commit, sprawdza go i uruchamia TgWitness jako wzmocnioną usługę systemd;
4. oczekuje na podpisane oświadczenie kolektora i sprawdza, czy wymienia ono ten serwer oraz skrót tego pliku cloud-init.

`deployments/case-2026-11/` Następnie zawiera:

| Plik | Spis treści | Udostępnić? |
| --- | --- | --- |
| `deployment.json` | Identyfikatory, skróty, wykonane wywołania API (metoda, ścieżka, status) oraz pierwsze podpisane oświadczenie | Tak, za pomocą weryfikatora |
| `cloud-init.redacted.yaml` | Dokładna konfiguracja `cloud-init`, w której dwa klucze tajne zostały zastąpione przez `REDACTED` | Tak |
| `panel-token.txt` | Token panelu | Nie |

Hasło administratora dostawcy, token tunelu oraz token panelu nigdy nie są zapisywane `deployment.json`. Opublikuj odcisk palca kolektora podany na końcu za pośrednictwem kanału, nad którym nie masz wyłącznej kontroli, na przykład kanału świadka lub wiadomości do odbiorcy.

Zaloguj się do Telegrama przy `https://case.example.org` za pomocą tokenu panelu, zgodnie z [instrukcją obsługi konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/). Działania panelu są rejestrowane w podpisanym dzienniku; nie są to sesje SSH. [Świadek](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/) może odpytywać `https://case-witness.example.org`.

Nie ma połączenia SSH: jeśli uruchomienie początkowe zakończy się niepowodzeniem, kolektor nigdy nie odpowie. Należy usunąć serwer i wdrożyć go ponownie lub skorzystać z wdrożenia debugowania, aby znaleźć przyczynę.

### Sekrety w danych użytkownika

Cloud-init przechowuje dwa klucze tajne: token panelu oraz token tunelu Cloudflare. Klucz podpisujący nie znajduje się wśród nich; jest on generowany na serwerze. Hetzner, DigitalOcean i Linode nie zwracają danych użytkownika za pośrednictwem swoich interfejsów API. Vultr zwraca je każdemu kluczowi, który ma uprawnienia do odczytu instancji, a EC2 poprzez `DescribeInstanceAttribute`. W przypadku AWS należy przekazać weryfikatorowi wyłącznie trzy działania wymienione w tabeli, nigdy `ec2:Describe*`. W przypadku Vultr należy założyć, że klucz weryfikatora może odczytać oba tokeny. Token tunelu pozwala komuś uruchomić drugi łącznik: `verify` zgłasza każdy łącznik, który nie znajduje się na serwerze, a oświadczenia kolektora nie mogą być w ten sposób sfałszowane, ponieważ każde z nich podpisuje nowe wyzwanie. W przypadku `--quick-tunnel` drugim sekretem jest klucz adresu: ktokolwiek go odczyta, może opublikować fałszywy adres, który panel zaakceptowałby.

W publicznym oświadczeniu kolekcjonera pominięto adres serwera oraz źródła logowań; oba te elementy pozostają w podpisanym dzienniku.

## Debugowanie wdrożenia i blokada

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` Utrzymuje SSH dla jednego klucza z jednego adresu lub małej sieci, maksymalnie /24 dla IPv4 lub /48 dla IPv6. `KEY` jest już zarejestrowany u dostawcy: nazwa lub identyfikator klucza SSH w projekcie Hetzner, identyfikator lub odcisk palca klucza SSH w zespole DigitalOcean, nazwa użytkownika Linode, którego klucze SSH w profilu są dodane do konta root, identyfikator klucza SSH na koncie Vultr lub nazwa pary kluczy EC2 w danym regionie. Te opcje nie mają zastosowania do `generic`. Taki wdrożenie jest rejestrowane jako `debug` i **nigdy nie** jest zgłaszana jako o wysokim poziomie bezpieczeństwa. Po zakończeniu uruchom `sudo tgwitness-lock` jako ostatnie polecenie ostatniej sesji SSH, a następnie:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Zapora sieciowa traci wszystkie reguły przychodzące. Raporty pokazują następnie, kiedy połączenie SSH było dozwolone, a kiedy zostało zamknięte; okno to pozostaje widoczne.

## Usuń wdrożenie

`destroy` usuwa serwer i jego zaporę sieciową, zidentyfikowane na podstawie etykiety wdrożenia, tak aby wdrożenie, które zakończyło się niepowodzeniem w połowie, również zostało usunięte, a następnie rekordy DNS wskazujące na jego tunel oraz sam tunel. Dziennik serwera i klucz podpisujący są usuwane wraz z nim: najpierw należy wyeksportować dowody. Zapis pozostaje, oznaczony `removed`, wraz z wywołaniami API dotyczącymi usunięcia.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Usuwanie za pośrednictwem API jest zaimplementowane dla Hetznera. W przypadku innych dostawców `destroy` należy najpierw zatrzymać proces przed usunięciem czegokolwiek i podać nazwę etykiety do usunięcia w konsoli dostawcy. Ręcznie zainstalowany serwer (`generic`) traci jedynie swój tunel i rekordy DNS. Szybkie wdrożenie tunelu nie wymaga tokena Cloudflare: tunel kończy się na serwerze, a jego posty wygasają z serwisu ntfy.sh w ciągu 12 godzin.

## Dowolny serwer (z własnym certyfikatem)

`--provider generic` dotyczy serwera zakupionego lub zainstalowanego ręcznie. `deploy` tworzy tunel i DNS, zapisuje `install.sh` (prywatny) oraz `install.redacted.sh` (w celu publikacji), a następnie czeka. Skopiuj `install.sh` na świeżo zainstalowany serwer z systemem Ubuntu 24.04 i uruchom go tam:

```
sudo bash install.sh
```

Rejestruje on stan hosta w momencie działania (loginy, konta, `authorized_keys`, gniazda nasłuchujące, usługi, zaplanowane zadania, pakiety), instaluje commit, włącza zaporę sieciową hosta, usuwa się, maskuje SSH i kończy sesję. Raport dotyczący takiego serwera jest w najlepszym razie **SAMOŚWIADCZĄCY**: osoba, która uruchomiła instalator, miała przedtem uprawnienia roota, a weryfikatorowi nie jest dostępny żaden zapis dostawcy. Jest to jednak lepsze niż serwer o nieznanym pochodzeniu: spis zasobów, skrót instalatora i każde późniejsze logowanie są podpisane.

## Zweryfikuj

Weryfikator potrzebuje `deployment.json`opublikowanego instalatora, danych uwierzytelniających tylko do odczytu oraz, w idealnym przypadku, kopii commit’u i dowodu ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Weryfikator żąda w danym momencie wszystkich wartości od dostawców i Cloudflare; zapis dostarcza jedynie identyfikatory, o które należy zapytać. Kod wyjścia wynosi 0 dla **PASS**, 1 dla **FAIL** oraz 2 dla **REVIEW**, **INCOMPLETE** lub **SELF-ATTESTED**. `--fingerprint` powinien pochodzić z niezależnego kanału; bez niego klucz jest porównywany wyłącznie z rekordem operatora. `python verify.py` nadal weryfikuje sam dowód ZIP, tak jak w sekcji [„Dowody](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)”.

Działania dostawcy są klasyfikowane: tworzenie i uruchomienie w ciągu 30 minut od utworzenia są akceptowane; konsola, ratowanie, resetowanie hasła, odbudowa, ISO, obrazy, migawki, kopie zapasowe, Systems Manager, EC2 Instance Connect oraz otwarcia zapory sieciowej kończą się niepowodzeniem; działania związane z zasilaniem oraz wszystko, czego nie przewidziano, są oznaczane do weryfikacji. Nieznane działanie nigdy nie przechodzi niezauważone.

## Raport dotyczący przekazania dowodów

`--report report.md` tworzy raport w formacie Markdown, a `report.json` obok niego:

1. wynik, odcisk klucza kolektora, wdrożenie, dostawca, zatwierdzenie, serwer, zapora sieciowa, tunel;
2. każda kontrola wraz ze statusem i źródłem (API dostawcy, API Cloudflare, oświadczenie kolektora, dziennik dowodów);
3. dziennik dostawcy zawierający ocenę każdej czynności oraz, o ile dostawca to odnotowuje, podmiot wykonujący czynność;
4. punkty końcowe Cloudflare przechowujące połączenia tunelu, konfigurację oraz dziennik audytowy;
5. podpisane oświadczenie kolekcjonera;
6. co raport potwierdza, a czego nie;
7. polecenia umożliwiające odtworzenie tego stanu oraz element SHA-256 każdego przekazanego pliku.

Przekaż raport, `report.json`, `deployment.json`opublikowany instalator oraz dowody ZIP. Przygotuj raport jak najwcześniej: logi dostawców są przechowywane przez ograniczony czas.

## Cloudflare jako zewnętrzny świadek

Wszystko tutaj jest opcjonalne. Serwer działa nawet bez konta Cloudflare, a dwa z tych rozwiązań działają już dzisiaj:

| Co | Co pokazuje | W TgWitness |
| --- | --- | --- |
| Szybki tunel lub tunel w Twojej domenie | Dostęp do panelu jest możliwy wyłącznie poprzez tunel | Kreator serwera – patrz wyżej |
| drand relay `drand.cloudflare.com` | zapisy po rundzie drand są nowsze od tego: dziennik był tworzony na bieżąco | tryb dowodowy, **Więcej świadków**, brak konta ([format](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Powiadomienia o stanie tunelu | gdy tunel nie działał, za pośrednictwem e-maila lub webhooka z Cloudflare | skonfiguruj je w panelu Cloudflare |
| Gateway DNS (`--gateway-dns`lub **Cloudflare Gateway DNS** w kreatorze) | każda nazwa wyszukiwana przez serwer, na którą Cloudflare odpowiadało przez TLS; zapora Hetznera nie pozwala DNS na dostęp do niczego innego; czy polityka bramy mogłaby przepisać odpowiedzi | Hetzner, bezpłatny plan Zero Trust, bez domeny; `verify` sprawdza zaporę sieciową, lokalizację, rejestrowanie, zasady, zapytania serwera oraz dziennik audytowy; tryb dowodowy kopiuje dziennik do rejestru |
| Brama z jednym klientem Cloudflare na serwerze, czyli zapora wychodząca, która zezwala wyłącznie na ruch przez Cloudflare | każde połączenie nawiązane przez serwer, a nie tylko DNS | jeszcze nie stworzono |
| Dostęp przed panelem | kto i kiedy zalogował się do panelu | nie zostało jeszcze wdrożone: wymaga własnej domeny |
| Rejestrowanie poleceń SSH | każde polecenie w sesji debugowania | jeszcze nie stworzono |

Logpush, który przechowywałby własną kopię Cloudflare w R2, jest funkcją dostępną w wersji Enterprise: w bezpłatnym planie Cloudflare odpowiada `logpush is not enabled for this account`. Dziennik bramy Gateway jest tam przechowywany przez 24 godziny, więc tryb dowodowy kopiuje go do podpisanego dziennika (**dziennik bramy Cloudflare Gateway zawierający zapytania DNS tego serwera**, token tylko do odczytu z uprawnieniem „Account Analytics Read”).

Bez planu Zero Trust konto ma jedną lokalizację DNS. Gdy Cloudflare odrzuca inną, serwer udostępnia istniejącą, a jego zapytania są rozróżniane na podstawie adresu; filtr ten wymaga również uprawnień Zero Trust PII Read i `destroy` pozostawia wspólną lokalizację. Jedno zapytanie do dziennika obejmuje maksymalnie trzy godziny, więc odczyt kopii i `verify` odczyt odbywa się w trzygodzinnych przedziałach.

DNS bramy obejmuje systemowy serwer nazw. DNS przez HTTPS na porcie 443 do innego serwera nazw oraz połączenia z adresami, których nie można nigdzie znaleźć (na przykład centra danych Telegrama), nie są rejestrowane w jego dzienniku.

Cloudflare nie ma wglądu w szyfrowanie Telegrama, inne urządzenia powiązane z kontem Telegram (lista urządzeń w trybie dowodowym rejestruje je po stronie Telegrama) ani hiperwizor dostawcy.

1 listopada 2026 r. usługa Gateway DNS działała w połączeniu z rzeczywistą chmurą Hetzner Cloud oraz darmowym kontem Cloudflare: Hetzner zaakceptował reguły ruchu wychodzącego, na serwerze zainstalowano wersję v0.7.0, przy czym każde wyszukiwanie przechodziło przez Gateway za pośrednictwem protokołu TLS, szybki tunel działał pomimo tej zapory sieciowej, a `verify` odczytał 19 nazw serwera z Cloudflare (serwery lustrzane Ubuntu i Hetzner, GitHub, PyPI, NTP, tunel, ntfy.sh). Panel skopiował 36 zapytań z ośmiu okien do dziennika i `verify.py` podsumował je bez żadnych luk; `destroy` usunął serwer i zaporę sieciową oraz opuścił wspólną lokalizację.

## Czego to nie potwierdza

- Dostawca i jego pracownicy zarządzają hiperwizorem, dyskami i siecią.
- Wyniki pomiarów serwera są zgłaszane samodzielnie przez moduł zbierający dane.
- Wcześniejsze wersje reguł zapory sieciowej nie znajdują się we wszystkich logach dostawców; jedynie Linode przechowuje wersje reguł.
- Nie zawiera żadnych nowych informacji na temat autentyczności wiadomości; zobacz sekcję [„Dowody](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/)”.

## Przetestowano tutaj

Logika wdrażania, blokowania i weryfikacji jest objęta automatycznymi testami przeprowadzanymi na symulowanych interfejsach API Hetzner, DigitalOcean, Linode, Vultr, EC2/CloudTrail i Cloudflare, zbudowanych na podstawie ich opublikowanych dokumentacji API, a także podpisywanie żądań AWS zgodnie z opublikowanymi przykładami AWS. `tools/check_cloud_wizard.py` uruchamia kreatora serwera panelu w ten sam sposób, z domeną oraz z szybkim tunelem. `tools/check_tdx.py` weryfikuje prawdziwe poświadczenia Intel TDX z dcap-qvl i dstack aż do certyfikatu głównego firmy Intel (źródła w [tools/tdx/README.md](https://github.com/phishdestroy/TgWitness/blob/main/tools/tdx/README.md)); `tools/check_phala.py`uruchamia wdrożenie, weryfikację, dziennik, niszczenie oraz kreatora panelu w symulowanym środowisku Phala Cloud, którego poświadczenia pochodzą z sfałszowanej infrastruktury PKI wzorowanej na infrastrukturze firmy Intel. Ścieżka Phala nie została jeszcze przetestowana w samym środowisku Phala Cloud.

1 listopada 2026 r. szybka ścieżka tunelowa działała w oparciu o prawdziwą **chmurę Hetzner** (Norymberga, `cpx22`, TgWitness v0.7.0), prawdziwym serwisem ntfy.sh oraz serwisem GitHub, zarówno z poziomu panelu, jak i kodu:

- sprawdzenie ceny, a następnie utworzenie za pomocą przycisków na panelu: serwer uruchamia się po 13 sekundach, podpisane oświadczenie z pasującymi skrótami instancji i instalatora pojawia się po około dwóch minutach;
- własny panel serwera otwarty pod adresem trycloudflare.com, który zaakceptował token panelu; bez tokenu zwraca kod 401;
- po ponownym uruchomieniu za pośrednictwem API Hetznera serwer opublikował nowy podpisany adres; **funkcja „Find the current address”** znalazła go, stary adres przestał odpowiadać, klucz podpisujący pozostał bez zmian; niepodpisany wpis w temacie ntfy.sh został zignorowany;
- `verify` w odniesieniu do API Hetznera: serwer, zapora sieciowa bez reguł przychodzących, oświadczenie, powiązanie, pomiary hosta, uruchamianie oraz hash źródłowy wydania v0.7.0 przeszły pomyślnie; testy Cloudflare były niedostępne, jak opisano powyżej; instalator różnił się od tego, który kompiluje wersję v0.7.0, i był identyczny bajt po bajcie z tym, który kompiluje kod tej wersji;
- Usunięcie z panelu spowodowało usunięcie dokładnie tego serwera i zapory sieciowej, które były oznaczone w ramach wdrożenia; inne serwery i zapory sieciowe w tym samym projekcie pozostały nienaruszone.

Nie testowano jeszcze na prawdziwych kontach: wdrożenie pod własną domeną (tunel Cloudflare i DNS), u innych dostawców, wdrożenie debugujące oraz `lock`, konto Telegram na takim serwerze, oraz aktualizacje na żywo późniejszych wersji poprzez szybki tunel. Sprawdź pierwsze wdrożenie u każdego dostawcy za pomocą `plan`, wdrożenie debugujące oraz `verify` zanim zaczniesz na nim polegać w konkretnej sprawie.
