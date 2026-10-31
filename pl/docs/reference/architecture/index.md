# Architektura

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/architecture/

Elementy składowe: moduł zbierający, panel, dziennik, moduły robocze oraz moduł „witness”, a także sposób przepływu danych między nimi.

Jeden proces w języku Python obsługuje panel FastAPI oraz dowolną liczbę izolowanych obszarów roboczych, z których każdy posiada klienta konta użytkownika Telethon. Baza danych SQLite przechowuje podpisany dziennik zdarzeń z możliwością wyłącznie dodawania wpisów oraz zmienne ustawienia operacyjne. W zaszyfrowanym sejfie przechowywane są dane uwierzytelniające API, obiekt StringSession oraz klucz podpisujący. Interfejs użytkownika stanowi zwykły pakiet plików HTML/CSS/JavaScript: nie jest wymagana kompilacja w środowisku Node, korzystanie z sieci CDN ani pobieranie interfejsu użytkownika w czasie wykonywania.

| Moduł | Odpowiedzialność |
| --- | --- |
| collector.py | Autoryzacja, wybór okien dialogowych, aktualizacje, migawki, kolejka multimediów, monitorowanie połączeń |
| interactions.py / telegram_client.py | Wyraźnie określone działania paneli, podpisane potwierdzenia, trwałe identyfikatory żądań oraz polityka ponownych prób wywołań zwrotnych i dołączania w ramach danego zadania |
| message_content.py | Porównanie widocznych wiadomości, z wyłączeniem metadanych dotyczących dostępu do sieci transportowej |
| workers.py | Należy poczekać na zakończenie pracy procesów eksportujących pliki przed przeprowadzeniem operacji czyszczenia po anulowaniu |
| store.py | Transakcje WAL, uporządkowany łańcuch zdarzeń, filtry zapytań, ustawienia operacyjne |
| security.py | Tworzenie plików prywatnych, zaszyfrowany sejf, podpisywanie algorytmem Ed25519, blokada pojedynczego procesu |
| evidence.py | Eksport pełnego dziennika, pliki pochodne, punkty kontrolne, weryfikacja załączników |
| verify.py | Samodzielny weryfikator tylko do odczytu (biblioteka standardowa + kryptografia): archiwa, zakres, dzienniki świadków i posty na kanałach, pliki profilowe |
| app.py | Uwierzytelnione API, cykl życia, walidacja żądań, panel statyczny |
| profiles.py | Kolektory obsługujące wiele kont, kontroler wspólnego dostępu, cykl życia dostosowany do poszczególnych obszarów roboczych |
| access.py | Dotacje o określonym zakresie, sprawdzanie uprawnień, ograniczenia adresów IP, limity sesji oraz konsola administratora |
| proxy_catalog.py | Zrzuty ekranu z kanałów publicznych, kontrole transmisji, wspólna pula serwerów proxy oraz selekcja oparta na stanie sprawności |
| provenance.py | Podpisane pomiary tożsamości, kodu i zależności w trakcie procesu pozyskiwania danych |
| network.py | Zweryfikowane ścieżki dla poszczególnych obszarów roboczych; status i dowody poddane redakcji; opcje przesyłania danych w ramach Telethon |
| sessions.py | Konwersja zweryfikowanych schematów bazy danych Telethon w formacie SQLite do trybu tylko do odczytu w trybie offline |
| account_import.py | Wykrywanie i normalizacja w pamięci obsługiwanych plików kont oraz plików JSON |
| tdata.py | Ograniczony, nowoczesny czytnik plików ZIP TData, weryfikacja sum kontrolnych i odszyfrowania, bez wyodrębniania danych |
| doctor.py | Lokalne testy gotowości bez gromadzenia danych, logowania ani instalacji pakietów |
| download.py | Uwierzytelniony eksport strumieniowy z możliwością pobrania, z ograniczonymi operacjami odczytu i bez nadpisywania danych |
| monitoring.py | Zweryfikowane zasady dotyczące zdarzeń w poszczególnych obszarach roboczych oraz reguły dotyczące załączników w zależności od typu, udostępniane przez osoby odpowiedzialne za obsługę, statusy oraz podpisane potwierdzenia odbioru |
| scope.py | Zakres monitorowania (wybrane czaty, folder Telegramu, całe konto), typy źródeł, wykluczenia, poziomy ponownej weryfikacji |
| dossier.py | Profile użytkowników dla poszczególnych czatów tworzone na podstawie zapisanych danych: fakty wraz z odniesieniami do zapisów, skróty SHA-256/pHash awatarów, ekstrakcja wzmianek |
| witness_api.py | Tokeny świadków z prawem tylko do odczytu oraz podpisany nagłówek dziennika, który mogą pobrać |
| witness.py | Niezależny proces świadectwa: własny klucz i dziennik, weryfikacja tożsamości, podpisane posty na kanałach, eksport |
| alerts.py | Powiadomienia w aplikacji Apprise oraz lista powiadomień na panelu |
| logging_config.py | Rejestrowanie w konsoli oraz rotacyjna diagnostyka serwera w przypadku uruchomień bez okien graficznych |
| static/ | Interfejs dostosowujący się do różnych urządzeń, lokalna brama dostępu, filtry, szczegóły, eksport danych, konfiguracja konta |
| demo.py | Wyraźnie oznaczony dziennik syntetyczny, oddzielony od rzeczywistych danych |

Moduły obsługi obserwacji są rejestrowane przed nawiązaniem połączenia. Gromadzenie danych na żywo jest ograniczone przez tożsamość aktywnego klienta, wyraźny stan działania, włączone źródła lub zakres obserwacji (tryby folderowe lub obejmujące całe konto dodają nową rozmowę jako źródło przy jej pierwszej aktualizacji) oraz zasady dotyczące zdarzeń. Odrzuceni i zastąpieni klienci nie mogą przekazywać aktualizacji na żywo. Surowe reakcje i aktualizacje członkostwa zachowują ograniczenia widoczności. Treść przychodzącej wiadomości oraz związane z nią zadanie trwałego nośnika są zapisywane łącznie. Zadania zachowują oryginalny deskryptor TL i wiążą jego skrót z podpisaną obserwacją wiadomości. Semantyka nadawcy, edytora i usuwającego jest rozdzielona.

Każdy obszar roboczy obsługuje jedno konto i posiada własny katalog oraz tożsamość podpisującą. Główny obszar roboczy pozostaje w katalogu głównym ze względu na kompatybilność; dodatkowe obszary robocze znajdują się w katalogu profiles/<id>/. Całą instalacją zarządza jeden token typu „bearer”; obszary robocze nie stanowią oddzielnych podmiotów autoryzacyjnych. Blokady procesów chronią katalogi; blokady bazy danych serializują wstawianie zdarzeń. Każde dodanie jest zapisywane synchronicznie do dziennika WAL bazy SQLite w trybie pełnej synchronizacji. Wyzwalacze aktualizacji/usuwania zdarzeń uniemożliwiają zwykłe edycje w aplikacji; administratorzy systemu plików pozostają w granicach strefy zaufania.

Autoryzacja API odbywa się za pomocą tokenu typu „bearer”. Operacje logowania są serializowane i ograniczone czasowo. Przesyłanie danych z konta podlega dedykowanemu limitowi 12 MiB dla zakodowanego treści oraz limitowi 8 MiB dla zdekodowanego pliku; zwykłe żądania API zachowują limit 16 KiB. Konwersja przebiega w wątku roboczym, przechowuje przesłane dane w pamięci i zwraca znormalizowane dane wejściowe do uwierzytelnionej przeglądarki. Logowanie za pomocą kodu QR obejmuje kandydata dla danego obszaru roboczego, krótkotrwały identyfikator, zadanie oczekujące oraz wyraźne anulowanie. Tylko zaakceptowana autoryzacja staje się aktywnym klientem. Funkcja Telegram FloodWait zwraca wartość Retry-After; dane uwierzytelniające oraz surowe komunikaty o błędach RPC nie są ujawniane w komunikatach o błędach API. Eksporty przebiegają poza asynchroniczną pętlą zdarzeń i są serializowane dla poszczególnych obszarów roboczych. Przesyłają one strumieniowo stabilną migawkę odczytu i mogą współistnieć z trwającym zapisem do dziennika WAL. Kolektory obszarów roboczych współdzielą pętlę procesową/zdarzeniową.

Aktualne migawki historii i aktualizacje na żywo mogą się nakładać. Obie stanowią odrębne obserwacje, oznaczone źródłem; duplikaty nie są automatycznie zwijane. Nie stosuje się żadnych wnioskowań na podstawie brakujących identyfikatorów, sfabrykowanego usuniętego tekstu, wymuszonego wyliczania członków ani automatycznego dołączania do grup. Nie jest to wdrażane.

Aby zapoznać się z wyjaśnieniami przeznaczonymi dla operatorów, proszę zapoznać się z [opisem działania procesu gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/) oraz [formatami kont i sesji](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/).

Konfiguracja sieciowa znajduje się w zaszyfrowanym sejfie. Zastosowanie trasy powoduje zamknięcie starych klientów i anulowanie niedokończonych procesów logowania; późniejsze połączenia korzystają z tej trasy bez bezpośredniego rozwiązania awaryjnego. Nowa instalacja z kluczem zewnętrznym generuje klucz Fernet dla każdego obszaru roboczego za pomocą algorytmu HKDF-SHA256 na podstawie pliku klucza głównego oraz zapisanej losowej wartości solującej. Zapewnia to ochronę kluczy w oddzielnym miejscu od katalogu danych, a nie w postaci zwykłego tekstu w dzienniku lub treściach multimedialnych.

Lokalny wpis demonstracyjny wykorzystuje oddzielnie wygenerowaną zdolność procesową, nigdy skonfigurowany token panelu. Wydanie i akceptacja wymagają wyraźnego trybu demonstracyjnego, syntetycznego katalogu głównego bez dodatkowych obszarów roboczych ani autoryzowanej sesji, pętli zwrotnej peer/Host, braku nagłówków przekierowujących przez serwer proxy oraz braku żądań przeglądarki międzydomenowych. Aktywne interfejsy API zachowują uwierzytelnianie typu „bearer” i odrzucają zmiany w gromadzeniu danych w trybie demonstracyjnym.
