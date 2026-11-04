# Zarządzanie grupą kont

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/groups/

Prowadź kilka kont razem — każde nadal z własnymi wpisami i kluczem.

Grupa zbiera na jednym ekranie stan połączeń, start/pauzę, wspólne ustawienia i eksporty. Wygodne, gdy kilka kont pracuje nad jedną sprawą.

## Otwórz przegląd grupy

Otwórz grupę w **Kontach**. Przy każdym koncie widać stan, trasę, opóźnienie i ostatnią zapisaną wiadomość. **Wymaga uwagi** wymienia te z problemami, **Napraw** prowadzi prosto do nich.

**Uruchom wszystkie** / **Wstrzymaj wszystkie** pytają przed działaniem. **Ustawienia grupy** są wspólne, ale własne wartości konta zostają, dopóki ich nie zastąpisz.

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

1. **Zmień trasę grupy**, wybierz typ i ustawienia.
2. **Przejrzyj wybór**: które konta się zmienią, a które mają własną trasę.
3. **Przygotuj i sprawdź** testuje świeże połączenie z Telegramem i, gdzie się da, wyjściowy IP.
4. **Zastosuj sprawdzone połączenie** i obejrzyj każdy wynik. Działające konta wznowią pracę, bezczynne takie zostaną.

Opóźnienie to czas nawiązania połączenia z Telegramem, wyjściowy IP to to, co trasa pokazała podczas sprawdzenia. Wyniki mogą się różnić między kontami.

## Należy stosować nakładające się uprawnienia dostępu

**Czaty widziane przez kilka kont** pokazują wspólne źródła i ich pokrycie. Kanały i supergrupy można eksportować kilkoma kontami naraz przez **Eksportuj … kontami**. Czaty prywatne i zwykłe grupy nie: tam numery wiadomości są osobne dla każdego konta.

## Eksportuj grupę jako pakiet

**Eksportuj grupę** daje jeden ZIP z podpisanym eksportem każdego konta i podpisaną ich listą. Każde zachowuje własny odcisk do weryfikacji. Wspólną chronologię nadal budujesz sam.

Dalej: [raporty](https://phishdestroy.github.io/TgWitness/pl/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/pl/docs/case-board/), [weryfikacja eksportów](https://phishdestroy.github.io/TgWitness/pl/docs/exports/).
