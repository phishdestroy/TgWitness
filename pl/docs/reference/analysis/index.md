# Analiza archiwum

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/

Przeszukuj zapisane wiadomości, przeglądaj dane wprowadzone przez sztuczną inteligencję i przechowuj raporty analityczne wraz z odniesieniami do źródeł.

**Aktualna wersja główna:** należy skorzystać z kopii źródłowej; przenośna wersja zapoznawcza 0.7.0 nie zawiera jeszcze tej funkcji.

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Aby wyszukiwać lokalnie bez AI, użyj widoku **Dziennik**. Aby korzystać z funkcji **Zapytaj archiwum**, najpierw włącz i skonfiguruj dostawcę w sekcji **Integracje**. Selektor obszaru roboczego służy do wyboru konta, a formularz do wyboru czatów i okresu obserwacji. Wyszukiwanie fragmentów odbywa się lokalnie. Dokładna fraza lub domena zawęża wyszukiwanie, a identyfikator wiadomości pozwala pobrać zapisane wersje. Przejrzyj fragmenty i otwórz powiązane wpisy w dzienniku lub ich kontekst. Nie jest używana baza danych wektorowa ani nie są wykonywane automatyczne działania w Telegramie.

## Dostawcy i zgoda

Sztuczna inteligencja jest domyślnie wyłączona w każdym obszarze roboczym. Tylko główny administrator może skonfigurować model, punkt końcowy, zaszyfrowany klucz API, limity kontekstu/wyników, limit czasu oraz dzienny limit żądań. Klucz nigdy nie jest zwracany do przeglądarki. Pozostaw pole klucza puste, aby zachować bieżący klucz, lub wyraźnie go usuń.

Ollama korzysta ze swojego udokumentowanego [punktu końcowego `/api/chat`](https://docs.ollama.com/api/chat) z wyjściem JSON bez strumieniowania. Jego domyślny adres to `http://127.0.0.1:11434` na serwerze TgWitness. Operator może go zmienić, używając `TGWITNESS_AI_LOCAL_ENDPOINT`; nie jest to adres kontrolowany przez model. Zainstaluj wybrany model samodzielnie. TgWitness nie pobiera go automatycznie.

Kompatybilny dostawca powinien posiadać adres URL bazowy kończący się na `/v1` oraz obsługiwać [protokół uzupełniania czatu](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, tryb odpowiedzi JSON, `max_completion_tokens` oraz `choices[0].message.content`. Usługi nieposiadające tych pól nie są obsługiwane. Testowanie połączenia polega na wysyłaniu syntetycznego tekstu i wlicza się do limitu żądań.

Każde żądanie korzysta ze skonfigurowanej w obszarze roboczym trasy zewnętrznej. Zablokowana trasa lub MTProxy przeznaczony wyłącznie dla Telegrama powoduje błąd; nie ma możliwości bezpośredniej ponownej próby. Celowo skonfigurowany lokalny adres Ollama pozwala na prywatny punkt docelowy, przy jednoczesnym korzystaniu z wybranej trasy. W przypadku innych prywatnych usług obowiązuje istniejąca opcja włączenia prywatnego punktu docelowego na poziomie serwera. Panel wyświetla faktycznie skonfigurowany punkt końcowy.

Przed wygenerowaniem **dane przesłane do modelu** zawierają żądanie: pytanie, zaznaczone fragmenty, rodzaje zdarzeń, czasy obserwacji i znaczniki zasięgu. Sesje Telegramu, pola surowe, klucze dostawców, bajty załączników oraz pełny dziennik nie stanowią części tego kontekstu. Odznacz niechciane źródła, a następnie wyraźnie zatwierdź przetwarzanie. Zewnętrzni dostawcy mogą przechowywać przesłane treści zgodnie z własnymi zasadami. Lokalne wykonanie oznacza, że punkt końcowy jest lokalny; nie stanowi to gwarancji co do zachowania niezależnie skonfigurowanej usługi.

Na całym świecie mogą występować maksymalnie dwa równoczesne żądania do dostawcy, a jedno na przestrzeń roboczą. Podgląd wygasa po dziesięciu minutach i pozwala wygenerować jedną odpowiedź. Wyświetlane są zgłoszone przez dostawcę liczby tokenów; szacunkowy koszt pojawia się tylko wtedy, gdy skonfigurowano zarówno taryfy wejściowe, jak i wyjściowe. Nieudane próby również zużywają dzienny limit żądań. Automatyczne ponowne próby nie powodują dodatkowego zużycia limitu.

## Źródła i ograniczenia

Funkcja wyszukiwania analizuje zapisany tekst wiadomości za pomocą ograniczonego wyszukiwania leksykalnego. Zwraca maksymalnie 24 źródła i zaznacza skrócone fragmenty lub niekompletne zestawy wyników. Okres odnosi się do **czasu obserwacji**, a nie do twierdzenia, że historia Telegrama jest kompletna. Zdarzenia obejmujące cały obszar roboczy są wyłączone z dostępu ograniczonego do czatu. Brakujące dane są opisane jako „nie znalezione w dostępnym archiwum”.

Model nie otrzymuje żadnych narzędzi. Jego identyfikatory źródłowe są porównywane z wybranymi rekordami, skróty są ponownie sprawdzane, a cytowane ciągi znaków muszą występować w tych rekordach. Nieznane identyfikatory, zmienione cytaty i niepotwierdzone twierdzenia powodują odrzucenie odpowiedzi. Aplikacja tworzy linki; adresy URL generowane przez model nie są wykorzystywane jako źródła. Kontrole te potwierdzają istnienie źródła i dokładność cytatu, a nie prawdziwość wniosku. Przed wykorzystaniem wniosków należy je zweryfikować w oparciu o zapisy.

## Raporty

Zapisz zweryfikowaną odpowiedź jako oddzielny raport analityczny. Zawiera on podsumowanie modelu, chronologię zdarzeń, wyodrębnione linki i identyfikatory, zapisy edycji/usunięć, ograniczenia zakresu oraz skróty zdarzeń źródłowych. Dołączone są informacje o dostawcy, modelu, punkcie końcowym, czasie oraz wersji szablonu zapytania. Żadne tożsamości nie są automatycznie łączone.

Poprawki i notatki analityków są przechowywane oddzielnie od podsumowania modelu. Raporty są przechowywane w zaszyfrowanych plikach pochodnych, a indeks znajduje się poza podpisanym strumieniem zdarzeń; oryginalne zdarzenia i multimedia pozostają niezmienione. Tylko właściciel lub administrator może otworzyć raport, a dostęp do źródła jest ponownie sprawdzany. Pobieranie wymaga również uprawnień do eksportu. Wersja 1 nie podpisuje raportów ani nie sugeruje, że wnioski modelu stanowią zweryfikowane dowody. Limity: 100 raportów na obszar roboczy i 100 poprawek analityków na raport.

Informacje na temat ręcznego rozpoznawania tekstu (OCR) i transkrypcji można znaleźć w sekcji [„Przetwarzanie multimediów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/)”. Informacje na temat dostępu dla klientów można znaleźć w sekcji [„MCP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/)”.
