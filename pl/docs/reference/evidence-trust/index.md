# Dowody i zaufanie

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence-trust/

Co mogą potwierdzić eksporty, nagrania wideo, archiwa internetowe i podpisane zapisy oraz w jaki sposób urządzenie gromadzące wpływa na ich wiarygodność.

Eksport, zrzut ekranu lub nagranie mogą stanowić przydatny dowód. Jego wiarygodność zależy od sposobu, w jaki został zebrany, zachowany i potwierdzony. **Prawidłowy skrót lub podpis weryfikuje zapisany materiał; nie potwierdza on jednak samodzielnie, że urządzenie zbierające otrzymało autentyczną treść źródłową.** Ta granica dotyczy również TgWitness.

Niniejszy przewodnik oddziela weryfikację techniczną od oceny prawnej. Dokumentacja produktu oraz poniższe przepisy prawne zostały zweryfikowane 1 listopada 2026 r.; porównanie Hunchly opisuje opublikowaną dokumentację, a nie nowy audyt produktu.

## Gdzie zaufanie wkracza w proces przechwytywania

Schemat blokowy · Konto i usługa Telegram → Klient, przeglądarka i system operacyjny; Klient, przeglądarka i system operacyjny → Eksport, nagranie wideo lub zrzut ekranu; Eksport, nagranie wideo lub zrzut ekranu → Skróty i podpisy kolektora; Skróty i podpisy kolektora → Suma kontrolna zachowana przez niezależną stronę · Konto i usługaTelegram · Klient, przeglądarka isystem operacyjny · Eksport, nagraniewideo lub zrzut ekranu · Skróty i podpisykolektora · Suma kontrolnazachowana przezniezależną stronę

**Schemat w formie tekstowej**

1. Konto i usługa Telegram → Klient, przeglądarka i system operacyjny
2. Klient, przeglądarka i system operacyjny → Eksport, nagranie wideo lub zrzut ekranu
3. Eksport, nagranie wideo lub zrzut ekranu → Skróty i podpisy kolektora
4. Skróty i podpisy kolektora → Suma kontrolna zachowana przez niezależną stronę

Model zagrożenia zakłada tutaj, że osoba atakująca lub operator może zmienić środowisko gromadzenia danych przed zatwierdzeniem dowodów. Jest to analiza warunkowa, a nie twierdzenie, że konkretne urządzenie lub produkt zostały naruszone.

Oficjalny klient i szyfrowane połączenie pomagają chronić normalne użytkowanie. Nie sprawiają one jednak, że otaczający system operacyjny, przeglądarka lub wyświetlacz są z samych w sobie godne zaufania. Jeśli treść zostanie zastąpiona po odszyfrowaniu, ale przed przechwyceniem, eksportujący może ją poprawnie zapisać, a podpisujący może ją poprawnie podpisać. Żadna z tych operacji nie wymaga uszkodzonego algorytmu skrótu ani sfałszowanego podpisu.

Film nagrany na tym samym urządzeniu może zarejestrować tę samą zastępczą prezentację. Oddzielna kamera może potwierdzić to, co wyświetlał ekran, ale sam ekran nie potwierdza autentyczności tego, co dostarczył Telegram. Podobnie, pasujące pliki HTML, JSON, zrzuty ekranu i logi przeglądarki z jednego kontrolowanego środowiska mogą wykazywać tę samą usterkę. Ich zgodność stanowi użyteczny kontekst; nie jest to automatycznie niezależne potwierdzenie.

## Co wnosi każda forma dowodu

| Materiały | Przydatny wkład | Pozostałe pytania |
| --- | --- | --- |
| Eksport z aplikacji Telegram Desktop | Rozmowy i wybrane multimedia w formie czytelnej dla człowieka lub maszynowo czytelnej | Kto sprawował kontrolę nad plikami klienta i eksportu oraz co było dostępne, a co wykluczone? |
| Zrzut ekranu lub nagranie ekranu | Widoczny kontekst, sekwencja działań i sposób prezentacji | Czy prezentacja wiernie odzwierciedla źródło oraz to, co wydarzyło się poza zakresem nagrania? |
| Lokalne archiwum internetowe, w tym MHTML | Treść strony i powiązane zasoby do późniejszej analizy | Co przeglądarka dostarczyła do archiwizatora i kto kontrolował tę przeglądarkę? |
| Archiwum podpisane przez zbierającego | Zmiany w podpisanych bajtach można wykryć w odniesieniu do zaufanego klucza i zachowanego odniesienia | Kto kontrolował klucz podpisujący i dane wejściowe przed podpisaniem? |
| Niezależnie zachowany punkt kontrolny lub zweryfikowany znacznik czasu | Zachowany skrót lub punkt kontrolny do porównania z późniejszym zgłoszeniem | Które bajty i granice są objęte certyfikatem oraz co faktycznie poświadcza strona niezależna? |

Telegram dokumentuje swój eksport z aplikacji Desktop jako kopię offline w formacie HTML/JSON, a interfejs API Takeout jako sposób na pobranie wybranych danych konta. Opisy te nie zawierają podpisu Telegramu na ostatecznym wyeksportowanym archiwum, który odbiorca mógłby zweryfikować. Nasze wnioski ograniczają się do tych udokumentowanych mechanizmów eksportu; nie jest to twierdzenie, że dowody z Telegramu nie mają wartości prawnej.[Eksport z aplikacji Telegram Desktop](https://telegram.org/blog/export-and-more),[interfejs API Takeout](https://core.telegram.org/api/takeout).

To samo rozróżnienie dotyczy żądań w tle, wpisów w pamięci podręcznej i dzienników sieciowych. Mogą one ujawniać niespójności i pomóc w potwierdzeniu autentyczności zbioru. Ich złożoność sama w sobie nie pozwala ustalić, kto je stworzył. Niezależnie prowadzone archiwum lub oddzielnie uzyskany zapis usługowy wprowadza inne źródło do porównania, z zastrzeżeniem własnych ograniczeń dotyczących gromadzenia i przechowywania.

## Hunchly ilustruje tę samą granicę

Dokumentacja Hunchly opisuje haszowanie SHA-256 przechwyconych treści MHTML, zdjęć i załączników wraz z niezależną weryfikacją skrótu. Wyjaśnia również, dlaczego zmodyfikowany plik z nowo obliczonym skrótem może przejść tę weryfikację, oraz wskazuje na podpisy i potwierdzenie źródła jako dodatkowe środki kontroli.[Hunchly: haszowanie treści, zdjęć i załączników](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Opublikowany *Przewodnik dotyczący dowodów*, wersja 1.0 z dnia 17 października 2018 r., opisuje generowane lokalnie klucze GPG i podpisy dla przechwytywania MHTML. Wyraźnie wskazuje on dostęp do lokalnego klucza prywatnego jako sposób ponownego podpisania zmodyfikowanego materiału. Jest to udokumentowane ograniczenie zaufania, a nie dowód na istnienie nieujawnionego aktualnego luki w zabezpieczeniach. W przewodniku stwierdza się również, że przechwytywanie MHTML odbywa się w przeglądarce Chrome. Opisanie serwisu Hunchly jako opierającego się wyłącznie na reputacji badacza pomijałoby te techniczne środki kontroli.[Przewodnik dowodowy serwisu Hunchly, sekcje 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

To, czy materiały zebrane za pomocą konkretnego produktu zostały dopuszczone w sprawie, zależy od odpowiedniej decyzji i okoliczności. Nie wypowiadamy się tutaj na temat tego, jak często sądy akceptują Hunchly lub TgWitness, ani na temat tego, czy którykolwiek z tych produktów cieszy się ogólną aprobatą sądów.

## Co wnosi TgWitness i gdzie kończy się jego ochrona

TgWitness rejestruje obserwacje w podpisanym, połączonym dzienniku i udostępnia eksporty, które odbiorca może zweryfikować. Zachowane punkty kontrolne, sygnatury czasowe oraz oddzielny świadek zapewniają recenzentom odniesienia wykraczające poza aktualne pliki podmiotu gromadzącego dane. Pomagają one ujawnić zmiany w wcześniej zatwierdzonych zapisach. Zapisy dotyczące zakresu oraz wyraźne wyniki gromadzenia danych pomagają wyjaśnić, co zostało uchwycone, a co nie.[Format dowodów i przekazywanie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/), [zakres gromadzenia danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/collection/).

Istotny jest moment ewentualnej zamiany:

1. **Po podpisaniu, bez dostępu do klucza podpisującego:** zmiana podpisanego rekordu lub pliku powiązanego z manifestem spowoduje niepowodzenie weryfikacji przez zaufanego weryfikatora i klucz.
2. **W przypadku klucza kolektora, po zachowaniu niezależnego punktu kontrolnego:** dziennik zastępczy może zawierać ważne nowe podpisy, ale zmieniony prefiks nie przejdzie porównania z tym wcześniejszym punktem kontrolnym. Punkt kontrolny przechowywany wyłącznie na tym samym kontrolowanym urządzeniu może zostać zastąpiony wraz z dziennikiem. Zapisy wykraczające poza zachowaną granicę wymagają osobnego zakresu.
3. **Zanim punkt kontrolny obejmujący obserwację zostanie niezależnie zachowany:**błędne dane wejściowe mogą zostać pomyślnie podpisane i zakotwiczone, w tym nowe rekordy dodane po wcześniejszym punkcie kontrolnym. Wynikowy punkt kontrolny lub sygnatura czasowa nadal obejmuje te błędne rekordy; nie potwierdza to jednak ich prawdziwości.

Świadek TgWitness odbiera podpisane punkty kontrolne kolektora; nie odczytuje on samodzielnie podstawowej rozmowy w Telegramie. Jego klucz i zachowane zapisy müssen być weryfikowane oddzielnie. Gdy cały przesłany dziennik muss zostać poświadczony, należy skorzystać z[procedury przekazania wymagającej ostatecznej granicy eksportu](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/#require-a-witnessed-export-boundary). Zwykły test integralności może nadal zgłaszać niepoświadczoną końcówkę.

Zweryfikowana odpowiedź zgodna z RFC 3161 może potwierdzić, że punkt kontrolny istniał w czasie podanym przez organ. Nie potwierdza ona jednak, kiedy wiadomość w Telegramie została wysłana ani czy jej treść była prawdziwa. Samo przygotowane żądanie lub dołączony plik odpowiedzi nie są wystarczające. Podczas weryfikacji eksportu za pomocą `tgwitness.verify` sprawdzenie dołączonych podpisów TSA wymaga wyraźnie zaufanego urzędu certyfikacji (CA) poprzez `--tsa-ca`. Potwierdzenia OpenTimestamps wymagają niezależnej weryfikacji `ots verify`, wraz z uaktualnieniem dowodów w razie potrzeby. [Procedura znakowania czasem](https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

W ramach [przechwytywania GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) tymczasowy hostowany runner gromadzi komunikaty. Poświadczenie wiąże archiwum z zatwierdzonym przepływem pracy. Tryb ten nadal opiera się na zaufaniu do serwisu GitHub, zatwierdzonego oprogramowania i zależności, narzędzia pomocniczego/przeglądarki oraz tunelu. Nie jest to poufny sprzęt, podpis Telegramu ani dowód na to, że nikt nie uzyskał dostępu do hosta. Lokalne, podpisane potwierdzenie uruchomienia jest również pomiarem opartym na własnych danych, a nie poświadczeniem sprzętowym.

## Waga prawna zależy od podstawy

Cztery pytania powinny pozostać odrębne: czy element jest tym, za co się podaje, czy przesłane bajty są zgodne z zachowanym zapisem, czy treść potwierdza podane fakty oraz czy obowiązujące przepisy zezwalają na jego wykorzystanie. Kontrola kryptograficzna dotyczy jedynie części tej podstawy.

W postępowaniach federalnych w USA zasada 901 określa sposoby uwierzytelniania dowodów, w tym zeznania świadków posiadających odpowiednią wiedzę oraz dowody dotyczące procesu lub systemu. Zasady 902(13) i 902(14) określają procedury poświadczania niektórych elektronicznych dokumentów i kopii wraz z wymogami proceduralnymi. W uwagach komisji rozróżnia się uwierzytelnianie od kwestii takich jak pogłoska, istotność i przypisanie. Sam podpis programowy nie stanowi poświadczenia przez uprawnioną osobę, o którym mowa w tych przepisach.[Federalna zasada dowodowa 901](https://www.law.cornell.edu/rules/fre/rule_901),[Federalna zasada dowodowa 902](https://www.law.cornell.edu/rules/fre/rule_902).

W przypadku gdy ma zastosowanie kanadyjska ustawa o dowodach (Evidence Act), sekcja 31.1 dotyczy uwierzytelniania dokumentów elektronicznych. Sekcja 31.2 wiąże zasadę najlepszego dowodu z integralnością systemu lub mającym zastosowanie domniemaniem; sekcja 31.3 określa okoliczności, w których istnieje domniemanie integralności. Są to zdefiniowane warunki dowodowe, a nie ogólne domniemanie, że każdy licencjonowany śledczy lub produkt komercyjny jest nieomylny. [Kanadyjska ustawa o dowodach, art. 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Przykłady te nie rozstrzygają kwestii dopuszczalności w innej jurysdykcji ani w konkretnej sprawie. Kontrole techniczne powinny być stosowane spójnie w odniesieniu do materiałów potwierdzających lub podważających zarzut. Niniejszy przewodnik nie zawiera twierdzenia, że dowody oskarżenia są zasadniczo łatwiejsze do dopuszczenia niż dowody obrony.

## Przygotuj dokument, który będzie mógł ocenić ktoś inny

- Opisz konto, urządzenie zbierające dane, operatora, wersję oprogramowania, uprawnienia dostępu, wybrany zakres i okres gromadzenia danych. Odnotuj przerwy i ewentualne naruszenia bezpieczeństwa, zamiast traktować pomyślną weryfikację podpisu jako test na obecność złośliwego oprogramowania.
- Zachowaj oryginalne pakiety oraz zapisy transferów, skróty i źródło czasu. Zachowaj odcisk klucza i punkty kontrolne za pośrednictwem oddzielnego, zaufanego kanału. Zweryfikuj rzeczywisty zakres świadków lub znaczników czasu przed opisaniem ich w raporcie.
- Poszukaj niezależnego potwierdzenia odpowiedniego do danego twierdzenia: zapisów innego uczestnika, niezależnego zrzutu ekranu lub legalnie uzyskanych zapisów serwisu. Wyjaśnij ich niezależność i ograniczenia; sama zgodność między kopiami nie jest wystarczająca.
- Zachowaj istotny kontekst. Wskaż pominięte pliki, niedostępną historię oraz ocenzurowane fragmenty. W razie potrzeby przygotuj [oddzielną, zredukowanąwersję ujawnionych danych](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)i opisz jej przekształcenia, nie przedstawiając jej jako pełnego oryginału.
- Przekaż odbiorcy instrukcje weryfikacyjne oraz materiały niezbędne do przeprowadzenia tych kontroli. Zadbaj o to, aby obserwacje, ustalenia techniczne i wnioski analityka były wyraźnie rozróżnialne.

W przypadku konkretnego przekazania należy podać skrót archiwum, zaufany klucz, wynik weryfikacji oraz dokładną granicę objętą zasięgiem zewnętrznym. Należy osobno opisać autentyczność źródła, przypisanie do konta, kompletność oraz wnioski prawne. Dzięki temu kolejny recenzent otrzyma konkretne twierdzenia do zbadania.
