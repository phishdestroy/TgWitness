# Wczytaj historię źródła

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/

Pobieraj poprzednie wiadomości z włączonych źródeł, wstrzymuj i wznawiaj proces oraz weryfikuj podpisany raport z postępów.

**Aktualna wersja główna:** dostępna ze źródła; nie zawarta w przenośnej wersji zapoznawczej 0.7.0.

W sekcji **„Źródła**” przejrzyj włączone czaty, rozpocznij obserwację, a następnie wybierz opcję **„Załaduj pełną historię**”. Operacja ta ustala listę źródeł i wczytuje dostępne wiadomości z przeszłości do sekcji „Czaty” oraz do podpisanego dziennika obserwacji. Pliki multimedialne wykorzystują istniejące ustawienia załączników oraz trwałą kolejkę pobierania. Jest to odrębna funkcja od podpisanego eksportu w formacie JSON/HTML dla poszczególnych czatów.

Aby zebrać dane z całego konta, wybierz **opcję „Całe konto”**, rozpocznij obserwację, aby załadować listę źródeł, a następnie przejrzyj tę listę przed rozpoczęciem tworzenia historii. Nadal obowiązuje limit listy okien dialogowych (domyślnie 1 000, można go dostosować w sekcji „Parametry”). Pomyślne przeprowadzenie operacji nie oznacza, że wszystkie rozmowy na koncie zostały uwzględnione. Czaty wykryte lub włączone później wymagają ponownego uruchomienia operacji.

## Wstrzymywanie, wznawianie i wyniki częściowe

- **Wstrzymanie historii** powoduje zatrzymanie odczytu. **Kontynuacja historii** wznawia odczyt od ostatniej zapisanej wiadomości w każdym źródle; ponowne uruchomienie aplikacji również powoduje wstrzymanie procesu do momentu jego wznowienia. Najpierw należy wznowić obserwację. Wznowienie wymaga użycia tego samego konta Telegram.
- Obserwacja wiadomości, operacja na załączniku i zatwierdzenie pozycji kursora odbywają się w ramach jednej transakcji. Wznowione uruchomienie nie powtarza już zatwierdzonych obserwacji. Obserwacja na żywo lub oddzielne, jawnie uruchomione zadanie mogą niezależnie obserwować tę samą wiadomość.
- Każde źródło ustala górną granicę identyfikatorów wiadomości przy pierwszym odczycie. Nowsze wiadomości należą do bieżącej obserwacji, a nie do pozostałych stron historycznych tego źródła.
- Źródła niedostępne oraz źródła wyłączone podczas pozyskiwania danych pozostają widoczne jako nieudane lub pominięte. Pozostałe źródła działają dalej; ogólny wynik jest niekompletny.
- Opóźnienia FloodWait uwzględniają ustawiony czas odczekiwania dla danego konta. Limity czasu transmisji oraz brak miejsca na dysku powodują wstrzymanie działania programu przy zachowaniu pozycji kursora. Działanie wznawiane jest po usunięciu przyczyny.
- **Zakończenie biegu historii** zachowuje zapisane obserwacje. Nie usuwa ich ani nie anuluje pobrań załączników już umieszczonych w kolejce. Nowy bieg ponownie odczytuje włączone źródła.

Operacja uzupełniania historii dotyczy wyłącznie odczytów historii. Załączniki mogą pozostać w toku, nie powiodć się lub zostać wykluczone przez skonfigurowaną politykę. Należy sprawdzić potwierdzenia odbioru multimediów w dzienniku oraz w kolejce załączników; jedynie zakończone potwierdzenie odbioru z zachowanymi bajtami stanowi zapisany załącznik. Operacja historii jest wyraźnym żądaniem utworzenia migawki i jest oddzielna od przełączników wybierających kategorie przyszłych zdarzeń na żywo.

## Przesyłanie i weryfikacja

Zapisz **podpisany raport z postępów**, a następnie skorzystaj z opcji **„Eksportuj dowody”**, aby pobrać dziennik i zapisane załączniki. Późniejszy eksport dowodów może zawierać dodatkowe zapisy; raport wiąże swoje liczniki z prefiksem dziennika z momentu jego utworzenia. Uruchom weryfikator z zaufanej kopii tej wersji:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Należy niezależnie przechowywać oczekiwany odcisk palca klucza podpisującego. Weryfikator sprawdza podpis raportu, archiwum dowodów, punkt kontrolny raportu, plan źródłowy, konto oraz liczbę zapisanych/niedostępnych wiadomości. Bez `--evidence` sprawdza jedynie podpisany raport i jego wewnętrzną spójność. Fazy postępu, tytuły, wskaźniki i podsumowania załączników są podpisanymi oświadczeniami podmiotu gromadzącego dane, a nie niezależnie odtworzonymi przez niniejsze narzędzie do sprawdzania raportów. Weryfikator dowodów nadal sprawdza zarchiwizowane bajty multimediów.

Ani podpisanie, ani uzupełnienie dostępnej historii nie potwierdza pochodzenia z Telegrama, atomowej migawki ani kompletności historycznej. Wiadomości mogą ulec zmianie podczas odczytu; usunięte wiadomości, niewidoczne zmiany pośrednie oraz tajne czaty nie są odzyskiwane. Operator kontrolujący klucz podpisujący może sfałszować dziennik, zanim pojawią się zewnętrzne potwierdzenia. W celu zapewnienia udokumentowanych właściwości wykrywania manipulacji należy korzystać z oddzielnie przechowywanych punktów kontrolnych lub niezależnego świadka.

Kursor pozyskiwania danych odzwierciedla stan lokalnego obszaru roboczego. Samo przywrócenie pliku ZIP z dowodami nie powoduje przywrócenia oczekującego zadania pozyskiwania danych ani sesji Telegramu. Należy zachować kopię zapasową obszaru roboczego, jeśli wymagana jest kontynuacja pierwotnego zadania.
