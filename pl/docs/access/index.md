# Telegram · Przedstaw proszę przypadek

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/access/

Udostępnijcie sprawę, której ktoś potrzebuje. Resztę zachowajcie pod kontrolą.

01**Proszę wybrać dowód**

Całe przestrzenie albo pojedyncze czaty.

02**Proszę wybrać działania**

Podgląd, eksport albo tylko potrzebne operacje.

03**Ustal granice**

Osobisty token z terminem ważności, limitem sesji i regułami IP, jeśli chcesz.

Zakres gromadzenia danych określa, co jest rejestrowane. Zakres dostępu określa, co dana osoba może zobaczyć i zrobić.

## Przyznaj komuś dostęp

1. Jako administrator otwórz **Dostęp**.
2. Nadaj nazwę, wybierz przestrzenie i czaty.
3. Recenzentowi wystarczy **Podgląd**. Do pobierania dodaj **Eksport**.
4. Proszę ustawić ograniczenia, a następnie kliknąć przycisk **„Utwórz dostęp**”.
5. Skopiuj token (pokazywany raz) i wyślij go prywatnie razem z adresem panelu.
6. Najpierw sprawdź, co ta osoba zobaczy, w osobnej sesji przeglądarki.

## Zacznij od zadania, które muszą wykonać

| Osoba | Dostęp | Wynik |
| --- | --- | --- |
| Recenzent | Wybrane rozmowy; tylko do wglądu | Czyta czat, nie może niczego zmienić. |
| Analityk | Wybrane rozmowy; przeglądanie i eksportowanie | Czyta i pobiera to, czego potrzebuje sprawa. |
| Operator | Wybrane całe obszary robocze; źródła i zbiór | Decyduje, co obserwować, uruchamia i zatrzymuje kolektory. |

To tylko przykłady, nie stałe role. Dostęp ograniczony do czatów nigdy nie dostaje ustawień konta ani pełnych eksportów dziennika. Dostęp do wszystkich przestrzeni obejmuje konta dodane później.

## W każdej chwili mogą Państwo zmienić zdanie

Zmieniaj dostęp kiedy chcesz, działa od następnego żądania. Zakończ jedną sesję albo odwołaj wszystko. Już pobranych plików nie da się cofnąć. Zbieranie działa dalej.

**Ograniczenia dotyczące sesji i adresów IP**

Ogranicz równoległe sesje i logowania, ustaw datę końca, zezwól na IP lub podsieci albo przypnij do IP pierwszego logowania. Ważność liczy się według bezczynności, otwarty panel liczy się jako aktywny. Za proxy sprawdź, jaki IP klienta widzi aplikacja.

**Klucz główny i dziennik aktywności**

Główny token zostaje u administratora. Wydany dostęp nie może zarządzać cudzym dostępem ani otwierać konsoli administratora. Zmiany dostępu i sesje są podpisywane w dzienniku, bez tokenów. Administrator serwera nadal widzi wszystko.

Wszystkie siedem uprawnień i zasady sesji: [dokumentacja dostępu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/).
