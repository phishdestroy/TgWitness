# Lokalne rozpoznawanie tekstu (OCR) i transkrypcja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/

Rozpoznawanie przechwyconych obrazów i plików audio za pomocą lokalnego modułu roboczego; zachowanie powiązania tekstu wyodrębnionego z plikiem źródłowym.

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Otwórz wpis w dzienniku `media.saved`, wybierz opcję **„Rozpoznaj załącznik**”, a następnie wybierz „OCR” lub „transkrypcja” w sekcji **„Zapytaj archiwum**”. Przetwarzanie odbywa się ręcznie i lokalnie. Nie ma trybu mediów w chmurze ani automatycznego przesyłania. Oryginalne bajty załącznika i plik `media_sha256` pozostają niezmienione; rozpoznany tekst jest wyraźnie oznaczony jako wynik rozpoznawania maszynowego i przechowywany oddzielnie wraz z skrótem źródłowym, wersją silnika/modelu, językiem, parametrami oraz czasem zakończenia. Transkrypcje zachowują zwrócone znaczniki czasu.

Przeszukuj te wyniki, korzystając z **funkcji „Wyszukaj rozpoznany tekst”** oraz filtra OCR/transkrypcji. Jest to oddzielne wyszukiwanie danych pochodnych; nie przekształca ono automatycznie wyników rozpoznania maszynowego w oryginalny tekst z Telegrama ani nie dodaje go do podpisanych zdarzeń.

## Skonfiguruj opcjonalnego pracownika

Wersja 1 wymaga hosta z systemem Linux z lokalnym demonem Docker. W przypadku instalacji w systemie Windows narzędzie TgWitness można uruchomić w środowisku maszyny wirtualnej z systemem Linux lub WSL z własnym lokalnym demonem. Panel nigdy sam nie odszyfrowuje zaufanych załączników.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Ustaw te zmienne w środowisku usługi TgWitness i uruchom ją ponownie. Domyślnym gniazdem demona jest `/var/run/docker.sock`; w przypadku wdrożeń bez uprawnień roota można ustawić `TGWITNESS_DOCKER_SOCKET`. Moduł roboczy wyraźnie korzysta z tego gniazda Unix, a nie ze zdalnego kontekstu Docker. Nie należy udostępniać interfejsu API Docker użytkownikom panelu ani montować jego gniazda wewnątrz kontenera rozpoznawania.

W celu transkrypcji należy osobno zainstalować model Whisper zgodny z CTranslate2, a następnie ustawić `TGWITNESS_WHISPER_MODEL_DIR` na jego katalog. Moduł roboczy ładuje go za pomocą `local_files_only=True`; wybrany model i dane wejściowe są montowane w trybie tylko do odczytu. Zobacz [dokumentację silnika dotyczącą ładowania modeli](https://github.com/SYSTRAN/faster-whisper). Dostarczony obraz OCR zawiera dane szkoleniowe w języku angielskim i rosyjskim. W razie potrzeby dodaj kolejny język do swojego obrazu; kody języków są zgodne z [interfejsem CLI Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Podczas przetwarzania nie są pobierane żadne modele. Proces kompilacji/pobierania plików instalacyjnych może wymagać połączenia z siecią; w każdym rzeczywistym kontenerze rozpoznawania połączenie sieciowe jest wyłączone. Zainstaluj obraz przed jego włączeniem; środowisko uruchomieniowe korzysta z `--pull=never`.

## Ograniczenia i odzyskiwanie danych

Kontener działa jako użytkownik bez uprawnień specjalnych, z katalogiem głównym tylko do odczytu, ograniczonymi uprawnieniami, `no-new-privileges` , jednym procesorem, 2 GiB pamięci, limitem PID oraz ograniczonym tymczasowym systemem plików. Zamontowana jest wyłącznie zweryfikowana kopia wybranego pliku oraz opcjonalny katalog modelu. Baza danych kolektora, skarbiec i sesja nie są montowane. [Flagi środowiska uruchomieniowego Docker](https://docs.docker.com/reference/cli/docker/container/run/) egzekwują te ograniczenia; pozostaje to granicą kontenera, a nie enklawą sprzętową.

Pliki są ograniczone do 50 MiB, obrazy do 20 milionów pikseli, pliki audio do 30 minut o znanym czasie trwania, a przetwarzanie do pięciu minut. W danym momencie działa tylko jeden procesor, przy maksymalnie 20 zadaniach w kolejce/w trakcie wykonywania i 100 zadaniach zachowanych na obszar roboczy. Anulowanie zatrzymuje kontener; ponowna próba tworzy nowe zadanie powiązane z poprzednią próbą. Przerwane zadania są oznaczane po ponownym uruchomieniu. Przetwarzanie może zakończyć się niepowodzeniem, gdy model nie mieści się w skonfigurowanych limitach; nie działa on w tle bez izolacji.
