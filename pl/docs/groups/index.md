# Zarządzanie grupą kont

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/groups/

Zarządzaj jednocześnie kilkoma kontami do gromadzenia danych, zachowując odrębność zapisów i tożsamości podpisującej dla każdego konta.

Grupa kont łączy w jednym widoku roboczym status połączenia, elementy sterujące obserwacją, wspólne ustawienia oraz funkcje eksportu. Jest to przydatne, gdy kilka kont dotyczy tego samego dochodzenia lub wymaga spójnej konfiguracji operacyjnej.

## Otwórz przegląd grupy

W sekcji „**Konta**” otwórz grupę. Każde konto pokazuje swój stan obserwacji, trasę połączenia, najnowsze zmierzone opóźnienie trasy w momencie pomyślnego zakończenia bieżącej kontroli oraz ostatnią zapisaną wiadomość. Linki **„Wymaga uwagi”** odsyłają do kont, które wymagają działania; **opcja „Napraw”** otwiera odpowiedni obszar roboczy i panel sterowania.

**Funkcje „Uruchom wszystko”** i **„Wstrzymaj wszystko”** działają na kwalifikujących się kontach po potwierdzeniu. **Ustawienia grupowe** udostępniają wybrane ustawienia; konta z własnymi wartościami zachowują je do momentu, aż zdecydujesz się je zastąpić.

### Sprawdź zmianę trasy w całej grupie

Przykład syntetyczny · przykładowe zadania i wyniki

1. **Wybierz.** Wybierz grupę i sprawdź, które konta ulegną zmianie.
2. **Przygotowanie.** Należy zachować odrębną ścieżkę dla danego konta, gdy powinno ono pozostać oddzielne.
3. **Sprawdź.** Przetestuj proponowane połączenie i przeanalizuj wyniki pomiarów.
4. **Zgłoś się.** Przed zapisaniem sprawdź wszystko jeszcze raz i przejrzyj wynik dla każdego konta.

#### Zespół ds. sprawy

Kolektor kanałów · Kolektor grup · Konto referencyjne

3 oddzielne obszary robocze

#### Przejrzany wybór

Dwa konta wybierają proponowaną ścieżkę.

Konto referencyjne zachowuje własną ścieżkę.

#### Kontrola przygotowawcza

Kolektor kanałów: czas przesyłania w Telegramie 84 ms

Kolektor grupowy: czas przesyłania w Telegramie 91 ms

Podane liczby są fikcyjnymi wartościami podanymi wyłącznie w celach ilustracyjnych.

#### Wyniki aplikacji

Kolektor kanałów: trasa zapisana, obserwacja wznowiona.

Kolektor grupowy: ponowna kontrola zakończyła się niepowodzeniem, przywrócono poprzednie ustawienia.

Konto referencyjne: zachowano własną ścieżkę.

## Zmiana ścieżki z uwzględnieniem etapu weryfikacji

1. Wybierz opcję **„Zmień trasę grupy**”, a następnie wybierz typ połączenia i ustawienia.
2. Wybierz **opcję „Przeglądaj wybór**”. Przejrzyj wymienione konta i ich indywidualne nadpisania tras.
3. Wybierz opcję **„Przygotuj i sprawdź**”. Sprawdzanie wykorzystuje nowy kanał transmisji Telegram; obsługiwane trasy HTTP zgłaszają również wynik kontroli wyjściowej HTTPS.
4. Należy wybrać opcję **„Zastosuj zaznaczone połączenia”** i sprawdzić wyniki dla każdego konta. Wcześniej uruchomiona obserwacja jest wznawiana tam, gdzie aplikacja zakończyła się powodzeniem; konta nieaktywne pozostają nieaktywne.

Opóźnienie opisuje zmierzoną czasowo konfigurację połączenia z Telegramem. Sprawdzenie adresu IP wyjściowego opisuje tę trasę w momencie rejestracji. Autoryzacja konta i stan obserwacji mają swoje własne wskaźniki; zmiana grupy może zakończyć się różnymi wynikami w zależności od konta.

## Należy stosować nakładające się uprawnienia dostępu

**W sekcji „Czat z kilkoma kontami”**wyświetlane są wspólne źródła oraz zakres obserwacji dostępny w obszarze roboczym. Kwalifikujące się kanały i supergrupy mogą korzystać z **opcji** **„Eksportuj z … kontami”**, aby podzielić proces pozyskiwania historii jednego czatu. Czat prywatny i zwykłe grupy pozostają przy koncie początkowym, ponieważ numery ich wiadomości należą do historii tego konta.

## Eksportuj grupę jako pakiet

**Grupa eksportująca** tworzy jeden plik ZIP zawierający podpisany eksport każdego konta oraz podpisaną listę tych plików. Oryginalne tożsamości i odciski palców obszaru roboczego pozostają dostępne do weryfikacji. Należy stworzyć narrację obejmującą różne konta, korzystając z tych odniesień; pojedyncza, scalona oś czasu jest nadal tworzona oddzielnie.

Przejdź do [projektowania raportu](https://phishdestroy.github.io/TgWitness/pl/docs/reports/), [tablicy sprawy w obszarze roboczym](https://phishdestroy.github.io/TgWitness/pl/docs/case-board/) lub [weryfikacji eksportu](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).
