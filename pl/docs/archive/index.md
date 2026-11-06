# Telegram · Przeglądaj archiwum

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/archive/

Znajdź wiadomość. Sprawdź źródło. Zbuduj sprawę.

01**Przedstaw historię**

Pobierz do przestrzeni dawne wiadomości z włączonych źródeł.

02**Śledź źródła**

Szukaj, a potem otwieraj zapisaną wiadomość za każdym wynikiem.

03**Zadbaj o jasność przekazania informacji**

Twoja analiza w jednym pliku, podpisane dowody obok.

Zarejestrowane dane, rozpoznany tekst oraz wnioski analityków pozostają wyraźnie rozdzielone.

## Wczytaj poprzednie wiadomości

1. **Źródła → Czaty w zakresie**: sprawdź włączone czaty i uruchom obserwację.
2. **Wczytaj całą historię**. Bierze listę źródeł w obecnym stanie.
3. **Wstrzymaj historię** / **Wznów historię** w dowolnej chwili. Po restarcie wznów ręcznie.
4. Sprawdź wynik dla każdego źródła i kolejkę pobierania, a podpisany raport postępu zachowaj razem z eksportem.

Tak wypełnia się przestrzeń. Eksport pojedynczego czatu do HTML/JSON to osobna sprawa. [Szczegóły](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/).

## Najpierw wyszukaj, a potem zdecyduj o wykorzystaniu sztucznej inteligencji

1. **Dziennik** szuka lokalnie, z filtrami źródła i czasu.
2. Wyszukaj frazę lub domenę, otwórz wpis i jego wersje.
3. Do AI administrator ustawia dostawcę w **Integracjach**. Potem **Zapytaj archiwum**: wybierz czaty i okres, obejrzyj **Dane wysyłane do modelu** i odznacz to, co nie powinno wyjść.
4. Sprawdź cytaty, zapisz odpowiedź jako raport i dodaj swoje notatki.

Wyszukiwanie nie potrzebuje AI. Raporty trzymają źródła i poprawki osobno od podpisanego dziennika. [Konfiguracja dostawcy](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/).

## Wybierz odpowiednie połączenie

| Zadanie | Otwórz | Konfiguracja |
| --- | --- | --- |
| Pozwolić klientowi AI czytać wybrane czaty | **Integracje → MCP** | [Zainstaluj MCP, utwórz ograniczony token, połącz](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/) |
| Rozpoznawanie tekstu w zapisanych plikach multimedialnych | Rekord `media.saved` → **Rozpoznaj załącznik** | [Skonfiguruj lokalny worker Dockera](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/) |
| Wysyłaj zdarzenia do n8n lub systemu SIEM | **Integracje → Webhooki wychodzące** | [Dodaj odbiorcę, sprawdzaj HMAC, odrzucaj zduplikowane ID](https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/) |

**Który token dostępu należy umieścić w którym miejscu?**

Dostęp do panelu jest dla ludzi. MCP ma własne tokeny tylko do odczytu, webhooki własny sekret HMAC. Żaden z nich nie potrzebuje sesji Telegrama.

[Udostępnij dostęp do panelu](https://phishdestroy.github.io/TgWitness/pl/docs/access/) lub [skonfiguruj klienta MCP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/).

## Przedstawienie źródeł i wniosków

Połóż raport obok podpisanego ZIP. Raport to Twoje odczytanie źródeł, ZIP to to, co sprawdza odbiorca.

[Eksportowanie i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/exports/) · [Przeprowadź kompleksowe dochodzenie](https://phishdestroy.github.io/TgWitness/pl/docs/cases/)
