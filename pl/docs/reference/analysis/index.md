# Telegram · Analiza archiwum

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/

Przeszukuj zapisane wiadomości, przeglądaj dane wprowadzone przez sztuczną inteligencję i przechowuj raporty analityczne wraz z odniesieniami do źródeł.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dochodzenie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/investigation/)

![Dochodzenie](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Użyj **dziennika** do wyszukiwania lokalnego bez sztucznej inteligencji; [wyszukiwanie pełnotekstowe](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/) (podgląd) dopasowuje formy słów, frazy, domeny i nazwy użytkowników z symbolem @. Aby skorzystać z funkcji **„Zapytaj archiwum”**, najpierw włącz i skonfiguruj dostawcę w sekcji **„Integracje**”. Selektor obszaru roboczego pozwala wybrać konto; formularz pozwala wybrać czaty i okres obserwacji. Wyszukiwanie odbywa się lokalnie. Dokładna fraza lub domena zawęża wyniki; identyfikator wiadomości pozwala uzyskać zapisane wersje. Przejrzyj fragmenty i otwórz ich wpisy w dzienniku lub kontekst. Nie ma bazy danych wektorowej ani automatycznych działań w Telegramie.

## Dostawcy i zgoda

Sztuczna inteligencja jest domyślnie wyłączona w każdym obszarze roboczym. Tylko główny administrator może skonfigurować model, punkt końcowy, zaszyfrowany klucz API, limity kontekstu/wyników, limit czasu oraz dzienny limit żądań. Klucz nigdy nie jest zwracany do przeglądarki. Pozostaw pole klucza puste, aby zachować bieżący klucz, lub wyraźnie go usuń.

Ollama korzysta ze swojego udokumentowanego [punktu końcowego `/api/chat`](https://docs.ollama.com/api/chat) z wyjściem JSON bez strumieniowania. Jego domyślny adres to `http://127.0.0.1:11434` na serwerze TgWitness. Operator może go zmienić, używając `TGWITNESS_AI_LOCAL_ENDPOINT`; nie jest to adres kontrolowany przez model. Zainstaluj wybrany model samodzielnie. TgWitness nie pobiera go automatycznie.

Kompatybilny dostawca powinien posiadać adres URL bazowy kończący się na `/v1` oraz obsługiwać [protokół uzupełniania czatu](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, tryb odpowiedzi JSON, `max_completion_tokens` oraz `choices[0].message.content`. Usługi nieposiadające tych pól nie są obsługiwane. Testowanie połączenia polega na wysyłaniu syntetycznego tekstu i wlicza się do limitu żądań.

Każde żądanie korzysta ze skonfigurowanej trasy zewnętrznej obszaru roboczego. Zablokowana trasa lub MTProxy przeznaczony wyłącznie dla Telegramu powoduje błąd; nie ma bezpośredniej próby ponownej realizacji. Celowo skonfigurowany lokalny adres Ollama pozwala na prywatny punkt docelowy. Punkt końcowy AI typu loopback wymaga zewnętrznej trasy typu „Direct” obszaru roboczego; trasy proxy są odrzucane przed transmisją. W przypadku innych usług prywatnych obowiązuje istniejąca opcja wyboru prywatnego miejsca docelowego na poziomie serwera. Podgląd pokazuje punkt końcowy i trasę zewnętrzną, w tym host proxy, jeśli ma to zastosowanie. Zmiana tej trasy wymaga nowego podglądu.

Przed wygenerowaniem **dane przesłane do modelu** zawierają żądanie: pytanie, zaznaczone fragmenty, rodzaje zdarzeń, czasy obserwacji i znaczniki zasięgu. Sesje Telegramu, pola surowe, klucze dostawców, bajty załączników oraz pełny dziennik nie stanowią części tego kontekstu. Odznacz niechciane źródła, a następnie wyraźnie zatwierdź przetwarzanie. Zewnętrzni dostawcy mogą przechowywać przesłane treści zgodnie z własnymi zasadami. Lokalne wykonanie oznacza, że punkt końcowy jest lokalny; nie stanowi to gwarancji co do zachowania niezależnie skonfigurowanej usługi.

Na całym świecie mogą występować maksymalnie dwa równoczesne żądania do dostawcy, a jedno na przestrzeń roboczą. Podgląd wygasa po dziesięciu minutach i pozwala wygenerować jedną odpowiedź. Wyświetlane są zgłoszone przez dostawcę liczby tokenów; szacunkowy koszt pojawia się tylko wtedy, gdy skonfigurowano zarówno taryfy wejściowe, jak i wyjściowe. Nieudane próby również zużywają dzienny limit żądań. Automatyczne ponowne próby nie powodują dodatkowego zużycia limitu.

## Źródła i ograniczenia

Wyszukiwanie korzysta z [indeksu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#ask-the-archive-and-mcp) [pełnotekstowego](https://phishdestroy.github.io/TgWitness/pl/docs/reference/search/#ask-the-archive-and-mcp), gdy jest on kompletny: najlepsze dopasowania w wybranych czatach, z uwzględnieniem form słownych. Zapytania dotyczące ostatnich zmian lub wersji jednej wiadomości, a także wyszukiwania podczas tworzenia indeksu, wykorzystują ograniczone wyszukiwanie leksykalne najnowszych rekordów. Podgląd określa nazwę metody. Wynik wyszukiwania zwraca maksymalnie 24 źródła; długie teksty są skracane wokół dopasowania. Skrócone fragmenty i niekompletne zestawy wyników są oznaczone. Okres ten odnosi się do **czasu obserwacji**, a nie do twierdzenia, że historia Telegrama jest kompletna. Zdarzenia o zasięgu całego obszaru roboczego są wyłączone z dostępu ograniczonego do czatu. Brakujące dane są opisane jako „nie znalezione” w dostępnym archiwum.

Model nie otrzymuje żadnych narzędzi. Jego identyfikatory źródłowe są porównywane z wybranymi rekordami, skróty są ponownie sprawdzane, a cytowane ciągi znaków muszą występować w tych rekordach. Nieznane identyfikatory, zmienione cytaty i niepotwierdzone twierdzenia powodują odrzucenie odpowiedzi. Aplikacja tworzy linki; adresy URL generowane przez model nie są wykorzystywane jako źródła. Kontrole te potwierdzają istnienie źródła i dokładność cytatu, a nie prawdziwość wniosku. Przed wykorzystaniem wniosków należy je zweryfikować w oparciu o zapisy.

## Raporty

Zapisz zweryfikowaną odpowiedź jako oddzielny raport analityczny. Zawiera on podsumowanie modelu, chronologię zdarzeń, wyodrębnione linki i identyfikatory, zapisy edycji/usunięć, ograniczenia zakresu oraz skróty zdarzeń źródłowych. Dołączone są informacje o dostawcy, modelu, punkcie końcowym, czasie oraz wersji szablonu zapytania. Żadne tożsamości nie są automatycznie łączone.

Poprawki i notatki analityków są przechowywane oddzielnie od podsumowania modelu. Raporty są przechowywane w zaszyfrowanych plikach pochodnych, a indeks znajduje się poza podpisanym strumieniem zdarzeń; oryginalne zdarzenia i multimedia pozostają niezmienione. Tylko właściciel lub administrator może otworzyć raport, a dostęp do źródła jest ponownie sprawdzany. Pobieranie wymaga również uprawnień do eksportu. Wersja 1 nie podpisuje raportów ani nie sugeruje, że wnioski modelu stanowią zweryfikowane dowody. Limity: 100 raportów na obszar roboczy i 100 poprawek analityków na raport.

Informacje na temat ręcznego rozpoznawania tekstu (OCR) i transkrypcji można znaleźć w sekcji [„Przetwarzanie multimediów](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/)”. Informacje na temat dostępu dla klientów można znaleźć w sekcji [„MCP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/)”.
