# Przeglądaj archiwum

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/archive/

Znajdź wiadomość. Sprawdź źródło. Zbuduj sprawę.

Narzędzia te są dostępne w aktualnej gałęzi głównej. Wersja przenośna 0.7.0 jest starsza od nich; w tym przypadku należy pobrać kod źródłowy.

01**Przedstaw historię**

Załaduj poprzednie wiadomości z włączonych źródeł do obszaru roboczego.

02**Śledź źródła**

Przeszukaj archiwum i otwórz zapisaną wiadomość powiązaną z każdym wynikiem.

03**Zadbaj o jasność przekazania informacji**

Zapisz swoją analizę osobno i wyeksportuj obok niej podpisane dowody.

Zarejestrowane dane, rozpoznany tekst oraz wnioski analityków pozostają wyraźnie rozdzielone.

## Wczytaj poprzednie wiadomości

1. **Źródła** otwarte – przejrzyj aktywne czaty i rozpocznij obserwację.
2. Wybierz opcję **„Załaduj pełną historię**”. Proces wykorzystuje listę źródeł wybraną w danym momencie.
3. W razie potrzeby należy korzystać z funkcji **„Wstrzymaj historię”** i **„Wznów historię**”. Po ponownym uruchomieniu należy wyraźnie wznowić działanie.
4. Sprawdź wyniki dla poszczególnych źródeł oraz kolejkę załączników. Zapisz podpisany raport z postępów wraz z eksportem dowodów.

Spowoduje to wypełnienie obszaru roboczego dostępnymi wiadomościami. Eksport w formacie HTML/JSON dla poszczególnych czatów jest odrębną operacją. [Historia i szczegóły dotyczące odzyskiwania danych](https://phishdestroy.github.io/TgWitness/pl/docs/reference/history/).

## Najpierw wyszukaj, a potem zdecyduj o wykorzystaniu sztucznej inteligencji

1. Otwórz **opcję „Zapytaj archiwum**”. Wybierz obszar roboczy, czaty i okres obserwacji.
2. Wyszukaj frazę, domenę lub identyfikator wiadomości. Otwórz pasujący wpis wraz z jego zapisanymi wersjami.
3. W przypadku analizy opartej na sztucznej inteligencji administrator najpierw konfiguruje dostawcę. Należy przejrzeć **dane wysyłane do modelu** i odznaczyć niepotrzebne fragmenty przed zatwierdzeniem żądania.
4. Sprawdź zwrócone cytaty. Zapisz odpowiedź jako raport i dodaj własne poprawki lub uwagi.

Wyszukiwanie odbywa się lokalnie, bez wykorzystania sztucznej inteligencji. Raporty analityczne zawierają odniesienia do źródeł oraz historię zmian; są one oddzielone od podpisanego dziennika. [Konfiguracja dostawcy i raporty](https://phishdestroy.github.io/TgWitness/pl/docs/reference/analysis/).

## Wybierz odpowiednie połączenie

| Zadanie | Otwórz | Konfiguracja |
| --- | --- | --- |
| Przeczytaj wybrane rozmowy z klienta opartego na sztucznej inteligencji | **Integracje → MCP** | [Zainstaluj dodatek MCP, wygeneruj token o ograniczonym zakresie i połącz klienta](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/) |
| Rozpoznawanie tekstu w zapisanych plikach multimedialnych | Rekord `media.saved` → **Rozpoznaj załącznik** | [Skonfiguruj lokalny proces roboczy Docker oraz wymagane pliki językowe i modelowe](https://phishdestroy.github.io/TgWitness/pl/docs/reference/media-analysis/) |
| Wysyłaj zdarzenia do n8n lub systemu SIEM | **Integracje → Webhooki wychodzące** | [Dodaj odbiorcę, zweryfikuj HMAC i usuń duplikaty identyfikatorów zdarzeń](https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/) |

**Który token dostępu należy umieścić w którym miejscu?**

Dostęp do panelu jest przeznaczony dla osób analizujących sprawę. Użytkownicy z połączeniami MCP otrzymują oddzielne tokeny archiwum tylko do odczytu. Odbiornik webhooków korzysta z własnego klucza tajnego HMAC. Żadna z tych opcji nie wymaga pliku sesji Telegramu.

[Udostępnij dostęp do panelu](https://phishdestroy.github.io/TgWitness/pl/docs/access/) lub [skonfiguruj klienta MCP](https://phishdestroy.github.io/TgWitness/pl/docs/reference/mcp/).

## Przedstawienie źródeł i wniosków

Przechowuj zweryfikowany raport analityczny wraz z podpisanym plikiem ZIP zawierającym dowody. Raport wyjaśnia Twoją interpretację źródeł; plik ZIP pozwala odbiorcy zweryfikować zapisany zapis w oparciu o niezależny, zaufany odcisk cyfrowy i punkt kontrolny.

[Eksportowanie i weryfikacja](https://phishdestroy.github.io/TgWitness/pl/docs/exports/) · [Przeprowadź kompleksowe dochodzenie](https://phishdestroy.github.io/TgWitness/pl/docs/cases/)
