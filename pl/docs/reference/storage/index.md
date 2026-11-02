# Przechowywanie i odzyskiwanie

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/storage/

Kopie zapasowe, przenoszenie starszych plików do chmury, kopie objęte funkcją Object Lock oraz odzyskiwanie danych na nowym komputerze.

Panel dzieli zadania na trzy kategorie:

| Zadanie | Jak to działa |
| --- | --- |
| Twórz kopie zapasowe | Skopiuj podpisany dziennik, punkty kontrolne, zachowane pliki i eksporty w kolejce do skonfigurowanej lokalizacji docelowej S3. |
| Darmowa przestrzeń lokalna | Skopiuj wybrane starsze załączniki do S3 lub zdalnego serwera w chmurze rclone, wczytaj je w całości, zweryfikuj zaszyfrowane bajty, a następnie usuń zweryfikowaną kopię lokalną. |
| Zachowaj kopię dowodową | Skonfiguruj funkcję S3 Object Lock i sprawdź zwracany status retencji. Usługa musi potwierdzić żądany tryb i datę. |

Zwolnienie miejsca nigdy nie powoduje usunięcia ani nadpisania podpisanego dziennika. Każdy załącznik zachowuje swój oryginalny tag SHA-256 oraz potwierdzenie odzyskania. Opcjonalna kompresja gzip odbywa się przed szyfrowaniem z uwierzytelnieniem. Nazwy plików w chmurze nie zawierają nazw użytkowników Telegrama, identyfikatorów czatów ani oryginalnych nazw załączników. Jeden załącznik może mieć rozmiar do 32 GiB.

Sama odpowiedź na przesłanie pliku nie stanowi zgody na jego usunięcie. TgWitness pobiera cały zaszyfrowany obiekt i weryfikuje jego rozmiar, a SHA-256 zapisuje potwierdzenie, a następnie ponownie sprawdza lokalne bajty tuż przed usunięciem. Niepowodzenie przesłania, różnica w odczycie lub anulowany transfer powodują, że plik lokalny pozostaje na swoim miejscu. Jeśli włączona kopia zapasowa dowodów nie skopiowała jeszcze tego pliku, usunięcie również czeka na to.

## Połącz miejsce docelowe

W **menu Dodatki → Pamięć i miejsce na dysku → Zarządzaj pamięcią** wybierz zadanie i miejsce docelowe, zapisz je, a następnie wybierz **opcję Test przesyłania i pobierania**. Test polega na przesłaniu małego losowego pliku testowego i odczytaniu go z powrotem. Nie wykorzystuje on treści z Telegrama.

W przypadku S3 należy użyć rzeczywistego punktu końcowego, regionu i zasobnika dostawcy. Wasabi, Backblaze, Cloudflare R2 i inne kompatybilne usługi korzystają z tych samych ustawień S3. Sama kompatybilność z API nie oznacza obsługi funkcji Object Lock. Tryb zarządzania może pozwalać upoważnionemu administratorowi na pominięcie okresu przechowywania; tryb zgodności ma inne ograniczenia. Przed poleganiem na okresie przechowywania należy sprawdzić zwracany status funkcji Object Lock.

W przypadku miejsca docelowego rclone należy utworzyć jedno zdalne konto, korzystając z konfiguracji dostawcy w rclone, a następnie wkleić sekcję tego zdalnego konta `[name]` sekcję tego serwera zdalnego do panelu. Zainstalowany moduł pomocniczy obsługuje MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud oraz innych dostawców wyświetlanych w selektorze. Dane uwierzytelniające są zapisywane w zaszyfrowanym sejfie tego obszaru roboczego. Odświeżenia OAuth są zapisywane z powrotem w sejfie. Dane uwierzytelniające nie są dodawane do zdarzeń dziennika ani uwzględniane w plikach do odzyskiwania.

Narzędzie pomocnicze jest instalowane w obszarze roboczym, z przypiętą wersją i SHA-256. Nie jest on dodawany do ścieżki systemowej PATH. Pliki konfiguracyjne i pliki robocze są plikami tymczasowymi w ramach tego obszaru roboczego. Zdalne połączenia oparte na poleceniach i plikach lokalnych są odrzucane. rclone wymaga obecnie jawnie wybranej trasy **Direct** dla żądań zewnętrznych. Należy używać natywnej pamięci masowej S3 dla trasy SOCKS5 lub HTTP obszaru roboczego; rclone nie omija w sposób cichy niedostępnej trasy.

## Zachowaj plik odzyskiwania

Wybierz opcję **„Zapisz plik odzyskiwania** po skopiowaniu plików” i przechowuj go w miejscu oddzielnym od instalacji. Zawiera on klucz deszyfrujący oraz podpisane potwierdzenia obiektów, więc traktuj go jak kopię zapasową klucza prywatnego. Oryginalną konfigurację zdalną oraz dane uwierzytelniające miejsca docelowego również przechowuj oddzielnie. Plik odzyskiwania utworzony przed późniejszym skopiowaniem nie zawiera potwierdzenia tego późniejszego pliku.

Odcisk palca klucza podpisującego powinien być już wcześniej zapisany oddzielnie. Podpis sprawdzany wyłącznie względem klucza zawartego w tym samym pliku nie pozwala ustalić, do kogo należy dany plik odtworzeniowy.

Aby naprawić brakujące potwierdzenia przechowywania w istniejącym obszarze roboczym, otwórz opcję **„Odzyskaj pliki z zapisanego pliku odzyskiwania**” i wybierz plik. Panel sprawdza podpis i wymaga tego samego klucza podpisującego obszar roboczy. Nie zezwala na zastąpienie innego klucza przechowywania. Następnie wybierz opcję **„Przywróć wszystkie pliki**”. Przywracanie wstrzymuje działanie automatycznej reguły przechowywania, dzięki czemu następny zaplanowany cykl nie usunie od razu przywróconych plików. Ponownie włącz regułę po zakończeniu pracy z lokalnymi kopiami.

Funkcja przywracania weryfikuje tekst zaszyfrowany, uwierzytelnia odszyfrowanie, w razie potrzeby dekompresuje i sprawdza oryginalny tekst jawny SHA-256 przed umieszczeniem pliku w `media/`. Uszkodzony obiekt zdalny nigdy nie zastępuje pliku lokalnego. Istniejący plik lokalny zawierający inne bajty jest zachowywany do wglądu, a nie nadpisywany.

## Przywracanie po utracie instalacji

Zainstaluj TgWitness na innym komputerze. Użyj prywatnego pliku odzyskiwania, oddzielnie zarejestrowanego odcisku palca oraz oryginalnych danych uwierzytelniających do serwisu docelowego:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

W przypadku S3 `--credentials` odwołuje się do prywatnego pliku JSON z `access_key` oraz `secret_key`; podpisany plik odzyskiwania dostarcza ustawienia miejsca docelowego. Polecenie korzysta z bezpośredniego połączenia zewnętrznego i pobiera przypięty program pomocniczy , gdy wymaga tego zdalny serwer rclone. Odrzuca istniejący katalog wyjściowy.

Odzyskane oryginalne bajty są zapisywane do `recovered-attachments/media/`o nazwach zgodnych z ich identyfikatorami SHA-256. `recovery-log.jsonl` jest niepodpisanym zapisem operacji odzyskiwania. Polecenie to nie odtwarza utraconego podpisanego dziennika ani jego klucza podpisu. W tym celu należy zachować pełną kopię zapasową obszaru roboczego. Plik odzyskiwania pamięci masowej nie jest pełną kopią zapasową obszaru roboczego .

## Bot operatora i powiadomienia o zakończeniu

Bot Telegramu należy do operatora. Utwórz go za pomocą BotFather i ustaw w panelu jego token, czat docelowy oraz wyraźnie określone dozwolone identyfikatory użytkowników Telegramu. Zarówno nadawca, jak i czat muszą się zgadzać. Przekazywane wiadomości i polecenia od innych botów są ignorowane.

`/status` oraz `/stats` są dostępne w domyślnym trybie wyświetlania wyłącznie statusów. Opcjonalny tryb kontroli dodaje `/pause`, `/resume` oraz `/copy`. `/copy` wywołuje skonfigurowane zadanie przechowywania; nie oznacza to, że zdalne przesyłanie zostało już zakończone. Polecenia nie mogą przekazywać dowolnych adresów URL, plików ani programów powłoki.

Należy korzystać z oddzielnych ustawień powiadomień dla alertów i zakończenia zadań. Powiadomienia o zakończeniu rozróżniają eksport konta z brakami od eksportu kompletnego oraz pokazują historię i liczbę zapisów. Fragmenty wiadomości nie są uwzględniane, chyba że zostaną osobno włączone w ustawieniach powiadomień. Selektor usług jest generowany na podstawie faktycznego katalogu zainstalowanych aplikacji Apprise, a nie stałego zestawu przykładowych dostawców.
