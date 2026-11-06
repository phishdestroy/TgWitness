# Telegram · Wczytaj historię źródła

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/

Pobieraj poprzednie wiadomości z włączonych źródeł, wstrzymuj i wznawiaj proces oraz weryfikuj podpisany raport z postępów.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Kolekcja](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Zbiór](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

W sekcji **Źródła** przejrzyj włączone czaty, wstrzymaj obserwację, wybierz opcję Standard API lub eksport Takeout, a następnie wybierz **Załaduj pełną historię**. Uruchomienie ustala tę listę źródeł i wczytuje dostępne wiadomości z przeszłości do sekcji Czaty oraz do podpisanego dziennika obserwacji. Pliki multimedialne wykorzystują istniejące ustawienia załączników oraz trwałą kolejkę pobierania. Jest to odrębne od podpisanego eksportu JSON/HTML dla poszczególnych czatów.

W celu zebrania danych z całego konta wybierz **opcję Całe konto**, rozpocznij obserwację, aby załadować listę źródeł, a następnie przejrzyj tę listę przed rozpoczęciem tworzenia historii. Nadal obowiązuje limit listy okien dialogowych (domyślnie 1,000, regulowany w sekcji Parametry). Pomyślne uruchomienie nie gwarantuje, że wszystkie okna dialogowe konta zostały uwzględnione. Czaty wykryte lub włączone później wymagają ponownego uruchomienia. Wstrzymaj obserwację przed rozpoczęciem tworzenia historii; w danym momencie można pozyskiwać dane tylko z jednego konta.

Wybierz od jednego do pięciu modułów przetwarzających załączniki oraz zdecyduj, czy zachować dostępne ostatnie działania i porównać wcześniej zapisane wersje. Pobieranie danych może wymagać zatwierdzenia w Telegramie oraz określonego przez serwer czasu oczekiwania. Opcje te pozostają niezmienne po wznowieniu. Zobacz [zachowanie uzupełniania danych oraz umowę dowodową](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md), aby uzyskać szczegóły dotyczące transportu, ponownych prób i zaufania.

## Wstrzymywanie, wznawianie i wyniki częściowe

- **Historia wstrzymania** przerywa odczyt. **Historia kontynuacji** wznawia od ostatniej zatwierdzonej wiadomości w każdym źródle; ponowne uruchomienie aplikacji również powoduje wstrzymanie działania do momentu wznowienia. Wzniesienie wymaga tego samego nieaktywnego konta w Telegramie.
- Obserwacja wiadomości, operacja na załączniku i zatwierdzenie pozycji kursora odbywają się w ramach jednej transakcji. Wznowione uruchomienie nie powtarza już zatwierdzonych obserwacji. Obserwacja na żywo lub oddzielne, jawnie uruchomione zadanie mogą niezależnie obserwować tę samą wiadomość.
- Każde źródło (każdy podzielony zakres Telegramu w Takeout) ustala górny identyfikator wiadomości przy pierwszym odczycie. Nowsze wiadomości należą do bieżącej obserwacji, a nie do pozostałych stron historycznych tego źródła.
- Źródła niedostępne oraz źródła wyłączone podczas pozyskiwania danych pozostają widoczne jako nieudane lub pominięte. Pozostałe źródła działają dalej; ogólny wynik jest niekompletny.
- Opóźnienia FloodWait uwzględniają zapisany czas odczekiwania dla konta. W przypadku przejściowych awarii podejmowane są ponowne próby maksymalnie pięć razy; wyczerpanie limitów i brak miejsca na dysku powodują wstrzymanie działania przy zachowaniu pozycji kursora.
- **Zakończenie biegu historii** zachowuje zapisane obserwacje. Nie usuwa ich ani nie anuluje zadań dołączania plików za pomocą standardowego API. Zakończenie funkcji Takeout oznacza pozostałe pliki Takeout jako pominięte; wstrzymanie pozwala na ich wznowienie. Nowy bieg odczytuje ponownie włączone źródła.

Operacja uzupełniania historii dotyczy wyłącznie odczytów historii. Załączniki mogą pozostać w toku, nie powiodć się lub zostać wykluczone przez skonfigurowaną politykę. Należy sprawdzić potwierdzenia odbioru multimediów w dzienniku oraz w kolejce załączników; jedynie zakończone potwierdzenie odbioru z zachowanymi bajtami stanowi zapisany załącznik. Operacja historii jest wyraźnym żądaniem utworzenia migawki i jest oddzielna od przełączników wybierających kategorie przyszłych zdarzeń na żywo.

## Przesyłanie i weryfikacja

Zapisz **podpisany raport z postępów**, a następnie skorzystaj z opcji **„Eksportuj dowody”**, aby pobrać dziennik i zapisane załączniki. Późniejszy eksport dowodów może zawierać dodatkowe zapisy; raport wiąże swoje liczniki z prefiksem dziennika z momentu jego utworzenia. Uruchom weryfikator z zaufanej kopii tej wersji:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Należy zachować oczekiwany odcisk palca klucza podpisu jako oddzielny element. Weryfikator sprawdza podpis raportu, archiwum dowodów, punkt kontrolny raportu, plan źródłowy, konto oraz liczbę zapisanych/niedostępnych wiadomości. Nowe przebiegi wiążą również postęp źródła i opcje z podpisanymi zdarzeniami kursora. Bez `--evidence` sprawdza jedynie podpisany raport i jego wewnętrzną spójność. Starsze pola postępu i podsumowania załączników pozostają podpisanymi oświadczeniami kolektora. Weryfikator dowodów sprawdza zarchiwizowane bajty multimediów.

Ani podpisanie, ani zakończenie dostępnej historii nie potwierdza pochodzenia z Telegrama, atomowej migawki ani historycznej kompletności. Wiadomości mogą ulegać zmianom podczas odczytu; usunięte wiadomości oraz pośrednie edycje poza dostępnymi ostatnimi działaniami oraz tajnymi czatami nie są odzyskiwane. Operator kontrolujący klucz podpisujący może sfałszować dziennik, zanim pojawią się zewnętrzne zobowiązania. W celu zapewnienia udokumentowanych właściwości wykrywania manipulacji należy stosować oddzielnie przechowywane punkty kontrolne lub niezależnego świadka.

Kursor pozyskiwania danych odzwierciedla stan lokalnego obszaru roboczego. Samo przywrócenie pliku ZIP z dowodami nie powoduje przywrócenia oczekującego zadania pozyskiwania danych ani sesji Telegramu. Należy zachować kopię zapasową obszaru roboczego, jeśli wymagana jest kontynuacja pierwotnego zadania.
