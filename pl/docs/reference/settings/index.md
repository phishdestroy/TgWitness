# Telegram · Pierwsza konfiguracja i ustawienia

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/settings/

Kreator konfiguracji, cele, poziomy interfejsu, trasy połączeń oraz ustawienia współdzielone przez grupę kont.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Pierwsze kroki](https://phishdestroy.github.io/TgWitness/pl/docs/reference/quickstart/)

![Pierwsze kroki](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Konta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/) · [Połączenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/connection/) · [Dostęp](https://phishdestroy.github.io/TgWitness/pl/docs/reference/access/)

Nowy obszar roboczy otwiera się `/first-run`: język i strefa czasowa, poziom interfejsu, cel, połączenie, Telegram i czaty. Każda odpowiedź jest zapisywana na serwerze natychmiast po zmianie, więc odświeżenie strony powoduje kontynuację tego samego kroku. Ostatni ekran wyświetla listę odpowiedzi i umożliwia powrót do dowolnej z nich.

Język, strefa czasowa IANA, motyw i poziom są przechowywane dla każdego operatora i każdego obszaru roboczego. Ustawieniami domyślnymi są język przeglądarki, strefa czasowa urządzenia, motyw systemowy oraz prosty interfejs. Zmiana języka nie powoduje utraty sesji panelu. Czas w podpisanym dzienniku nigdy się nie zmienia.

`/settings` Edytuje te same zapisy co kreator. Wyszukiwanie obejmuje główne pola, parametry oraz rozszerzone formularze; ukryte pole można otworzyć bez zmiany poziomu. Poziomy zmieniają jedynie to, co jest wyświetlane: serwer samodzielnie sprawdza uprawnienia. Ustawienia kolekcji oraz pierwsze połączenie należą do administratora obszaru roboczego.

| Poziom | Pola | Pasek boczny |
| --- | --- | --- |
| Proste | Tylko to, co niezbędne | Strona główna, Czaty, Zmiany, Archiwa, Ustawienia |
| Standard | Typowe ustawienia wraz z objaśnieniami | Dodano sekcje „Case Board”, „Konta” i „Dostęp” |
| Ekspert | Wszystkie pola, ograniczenia i szczegóły techniczne | Dodano sekcje: Źródła, Dodatki, Zapytaj archiwum, Parametry, Konto, Dziennik systemowy oraz Integracje |

W [przewodniku po panelu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/panel/) opisano każdą sekcję.

## Cele

| Cel | Kolekcja | Pliki | Usługi zewnętrzne | Adres serwera |
| --- | --- | --- | --- | --- |
| Kopia archiwalna | Wyłączone; opcja **„Start”** uruchamia eksport | Zdjęcia o rozmiarze do 20 MB | Wyłącz | Automatyczne |
| Śledź czaty | Ciągłe | Zdjęcia i filmy o długości do 60 sekund / rozmiarze do 20 MB | Sygnatury czasowe i powiadomienia o problemach | Automatyczne |
| Dowody | Ciągłe | Wszystkie pliki o rozmiarze do 1 GB | Sygnatury czasowe, drand, powiadomienia | Nie, ukryj to |

Jako dowód zaleca się kopię poza serwisem, bota świadka oraz weryfikację kodu. Adresy przechowywania i powiadomień wymagają najpierw określenia miejsca docelowego. Funkcja komunikująca się z usługą zewnętrzną prosi o zezwolenie na żądania spoza Telegrama; wyłączenie tej opcji powoduje jednocześnie wyłączenie znaczników czasu, powiadomień oraz kopii poza serwisem.

Zmiana wartości docelowej najpierw pokazuje różnicę, a zmiany wprowadzone ręcznie można zachować. Pole, które różni się od wartości docelowej, jest oznaczone **jako „Zmienione przez Ciebie”** i można je przywrócić. Wersja ustawień zapobiega nadpisaniu zmiany dokonanej w innej zakładce przez sprawdzoną różnicę.

## Połączenie

**Automatic** najpierw próbuje połączyć się z publicznymi serwerami MTProxy, następnie z WARP, a na końcu próbuje nawiązać bezpośrednie połączenie – to ostatnie rozwiązanie stosuje się tylko wtedy, gdy adres serwera może zostać ujawniony. Automatic i WARP mogą instalować komponenty z weryfikacją skrótu oraz rejestrować serwer w Cloudflare. WARP korzysta z istniejącego menedżera wgcf/wireproxy oraz lokalnego portu SOCKS5; tabela routingu systemu nie ulega zmianie. Gdy potrzebne są usługi zewnętrzne, Automatic preferuje WARP zamiast MTProxy.

Twój własny serwer proxy obsługuje `tg://proxy`, `socks5://`, `http://` i `https://`. Certyfikat proxy HTTPS jest sprawdzany przed wysłaniem do niego danych uwierzytelniających.

Sprawdzenie połączenia jest ważne przez pięć minut i jest powiązane z trasą, polityką oraz odpowiedziami z kreatora; zmiana któregokolwiek z tych elementów wymaga nowego sprawdzenia. Dostępna jest opcja **kontynuowania bez sprawdzania**, która nie zastępuje logowania do Telegrama. Wybrana trasa jest ponownie sprawdzana w tle, a funkcja „Automatycznie” ponownie uruchamia swój łańcuch po utracie połączenia. Gdy żadne publiczne proxy nie odpowiada, licznik zmienia kolor na czerwony wraz z akcjami WARP i ponownego sprawdzenia .

## Grupy kont

Konta w grupie mają wspólne ustawienia. Otwórz **opcję „Konta” → „Grupy i wspólne ustawienia” → „Wspólne ustawienia**” lub **„Ustawienia grupy”** na stronie ustawień konta.

Grupa współdzieli cel, zapisane pliki, znaczniki czasu, drand, powiadomienia o problemach, kopię poza serwisem, żądania spoza Telegrama, tryb IP, zakres rejestracji, harmonogram ponownej weryfikacji, reguły powiadomień, ustawienia raportów, parametry oraz trasę połączenia. Adresy powiadomień, dane uwierzytelniające proxy i dane logowania pozostają przypisane do poszczególnych kont, podobnie jak rozpoczynanie i wstrzymywanie gromadzenia danych.

- Każdy członek obserwuje grupę. W ustawieniach można wybrać wartość 🔗 **z grupy** lub ✏️ **własną wartość**; opcja **„Powrót do wartości grupy”** przywraca wartość z grupy.
- Zmiana zawiera listę kont, których dotyczy (**dotyczy 2 z 3 kont**) i pyta o zgodę dla każdego konta przed zastąpieniem jego wartości. Konta, dla których opcja nie została zaznaczona, zachowują swoje wartości.
- Parametr, którego grupa nie udostępnia, pozostaje **w stanie „Nieudostępniony”: każde konto zachowuje swoją własną wartość,** dopóki nie naciśniesz przycisku **„Udostępnij tę wartość**”.
- **Kopiowanie ustawień z jednego konta** powoduje, że wartości wybranego konta stają się wartościami grupy.
- Konto przeniesione do grupy otrzymuje pytanie: **„Przyjąć wartości grupy?”.** W przeciwnym razie zachowuje własne wartości, oznaczone symbolem ✏️. Konta dodane później zaczynają z wartościami grupy.
- Konto obserwacyjne zachowuje swój adres IP do momentu wstrzymania działania.

Każda zmiana jest rejestrowana w podpisanym dzienniku głównego obszaru roboczego oraz każdego członka, do którego ta zmiana dociera. Usunięcie grupy powoduje zachowanie jej kont i ich aktualnych wartości.

Strona grupy `/groups/<id>` pokazuje członków, sprawy wymagające uwagi oraz czaty, które są widoczne dla kilku kont. Zobacz [grupy kont](https://phishdestroy.github.io/TgWitness/pl/docs/reference/accounts/#bulk-import-and-account-groups).

## Istniejące obszary robocze

W obszarze roboczym z aktywną sesją lub wcześniej zakończoną konfiguracją kreator nie jest wyświetlany. Jego wartości nie są zastępowane przez cel podczas ładowania strony. Ukrycie pola nie wyłącza tej funkcji ani nie usuwa jej wartości.

Szacunkowa wielkość i czas obejmują do trzech wybranych czatów i do 20 wiadomości z każdego z nich. Jest to wartość orientacyjna: nie uwzględnia ona limitów serwisu Telegram, prędkości danego serwera ani plików w poszczególnych czatach.
