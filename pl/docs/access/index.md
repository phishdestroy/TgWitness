# Przedstaw proszę przypadek

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/access/

Udostępnijcie sprawę, której ktoś potrzebuje. Resztę zachowajcie pod kontrolą.

01**Proszę wybrać dowód**

Proszę wybrać całe obszary robocze konta lub poszczególne zarejestrowane czaty.

02**Proszę wybrać działania**

Należy przyznać uprawnienia do przeglądania, eksportowania lub konkretne uprawnienia operacyjne, których dana osoba potrzebuje.

03**Ustal granice**

Wygeneruj osobisty token z terminem ważności, limitami sesji oraz opcjonalnymi ograniczeniami dotyczącymi adresów IP.

Zakres gromadzenia danych określa, co jest rejestrowane. Zakres dostępu określa, co dana osoba może zobaczyć i zrobić.

## Przyznaj komuś dostęp

1. Zaloguj się jako administrator i otwórz sekcję **„Dostęp**”.
2. Proszę podać nazwę konta oraz wybrać obszary robocze i czaty.
3. Proszę zachować **opcję „Wyświetl”** dla recenzenta. Proszę dodać **opcję „Eksportuj”,** jeśli recenzent ma pobrać zapisy.
4. Proszę ustawić ograniczenia, a następnie kliknąć przycisk **„Utwórz dostęp**”.
5. Proszę skopiować wyświetlony jednorazowy token. Proszę przesłać go prywatnie wraz z adresem panelu.
6. Przed przekazaniem prosimy o sprawdzenie, czy strona wyświetla się poprawnie w osobnej sesji przeglądarki.

## Zacznij od zadania, które muszą wykonać

| Osoba | Dostęp | Wynik |
| --- | --- | --- |
| Recenzent | Wybrane rozmowy; tylko do wglądu | Proszę zapoznać się z zarejestrowaną rozmową bez wprowadzania zmian w zebranych danych. |
| Analityk | Wybrane rozmowy; przeglądanie i eksportowanie | Proszę przejrzeć i pobrać zapisy niezbędne do prowadzenia sprawy. |
| Operator | Wybrane całe obszary robocze; źródła i zbiór | Zarządzaj obserwowanymi danymi oraz uruchamiaj lub zatrzymuj moduły zbierające dane. |

Są to konfiguracje, które Państwo wybierają, a nie stałe role. Ustawienia dotyczące całego konta oraz pełne eksporty dziennika pozostają niedostępne w ramach dostępu ograniczonego do czatu, nawet jeśli włączono inne uprawnienie. Dostęp do całego obszaru roboczego obejmuje również przyszłe konta.

## W każdej chwili mogą Państwo zmienić zdanie

Proszę edytować uprawnienia dostępu, aby zmienić zakres działań, jakie mogą być wykonywane w kolejnych żądaniach. Proszę zakończyć jedną sesję lub cofnąć cały dostęp, aby zakończyć wszystkie sesje. Plików, które zostały już pobrane, nie można odzyskać. Zakończenie sesji panelowej nie powoduje zatrzymania gromadzenia danych.

**Ograniczenia dotyczące sesji i adresów IP**

Ogranicz liczbę sesji równoległych i pomyślnych logowań, ustaw bezwzględną datę zakończenia, zezwól na określone adresy IP lub podsieci albo powiązaj dostęp z adresem używanym podczas pierwszego logowania. Wygasanie sesji jest uzależnione od braku aktywności; wyświetlanie otwartego panelu liczy się jako aktywność. Proszę sprawdzić adres klienta wyświetlany przez aplikację, gdy działa ona za serwerem proxy lub tunelem.

**Klucz główny i dziennik aktywności**

Administrator przechowuje token panelu głównego. Użytkownicy z przyznanym dostępem nie mogą zarządzać uprawnieniami innych osób ani otwierać konsoli administratora. Konsola wyświetla bieżącą aktywność procesów we wszystkich obszarach roboczych; podpisane zapisy dostępu przechowują zdarzenia związane z przyznaniem uprawnień i sesjami bez wykorzystania tokenów. Obszary robocze współdzielą proces hosta i nie izolują danych od administratora serwera.

Należy wykorzystać [pełny opis uprawnień](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/) dla wszystkich siedmiu uprawnień, reguł sesji oraz ograniczeń administratora.
