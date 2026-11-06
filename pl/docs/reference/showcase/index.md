# Telegram · Publiczna prezentacja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/showcase/

Publikuj zapisane wiadomości z wybranych kanałów publicznych oraz podpisane migawki za pomocą linków z terminem ważności i możliwością cofnięcia.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Wdrażanie i przywracanie](https://phishdestroy.github.io/TgWitness/pl/docs/reference/deployment/)

![Wdrażanie i przywracanie](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Opcja **„Dostęp → Publiczna prezentacja”** tworzy oddzielną stronę tylko do odczytu przy użyciu istniejącego systemu tokenów dostępu. Odczytuje ona zapisane obserwacje instalacji. Nie uruchamia kolektora, nie loguje się do Telegrama ani nie uzyskuje dostępu do kanału dla odwiedzającego.

## Opublikuj stronę

1. Zapisz profil źródłowy dla każdego kanału publicznego, który chcesz wyświetlić. Kanał musi posiadać publiczną nazwę użytkownika w swoim najnowszym zapisanym profilu; grupy i czaty prywatne nie kwalifikują się.
2. Otwarty **dostęp → Publiczna prezentacja** (lub `/showcase-manage.html`) jako administrator.
3. Wybierz kanały z maksymalnie 16 obszarów roboczych, wprowadź tytuł strony publicznej i wybierz okres ważności linku: 1, 7 lub 30 dni. Wewnętrzne etykiety obszarów roboczych nie są publikowane. Można uwzględnić maksymalnie 64 kanały.
4. Sprawdź tekst wybranych kanałów pod kątem publikacji, a następnie kliknij **„Podgląd wybranych rekordów**”. Podgląd wykorzystuje tę samą projekcję po stronie serwera, co strona dla odwiedzających.
5. Kliknij **„Utwórz link do prezentacji**”. Skopiuj link, póki jest widoczny. Otwórz go w osobnej przeglądarce, aby sprawdzić stronę odbiorcy przed jej udostępnieniem.

Link zawiera token dostępu w fragmencie adresu URL. Strona usuwa ten fragment przed wysłaniem żądań do API i zamienia go na sesję przeglądarki. Każdy, kto posiada ten link, może otworzyć wybrany materiał do momentu wygaśnięcia lub cofnięcia uprawnień. Nowe linki umożliwiają 100 równoczesnych sesji, z których każda trwa maksymalnie jedną godzinę. Istniejące mechanizmy kontroli dostępu mogą również egzekwować ograniczenia adresowe i limity logowań za pośrednictwem interfejsu API grant. Standardowy dostęp recenzenta to odrębny tryb, który nadal obejmuje pierwotnie dozwolone wiadomości i pliki.

## Co widzą odwiedzający

| Widoczne | Utrzymywane jako prywatne |
| --- | --- |
| Wybrane nazwy kanałów publicznych, nazwy użytkowników oraz daty obserwacji profili | Tożsamości kont, wewnętrzne etykiety obszarów roboczych oraz niewybrane źródła |
| Przechwycony tekst i każda zapisana edycja | Ustrukturyzowane identyfikatory nadawców, nazwiska, nazwy użytkowników, numery telefonów i wartości profilowe |
| Uwagi dotyczące usunięcia wraz z wcześniej zapisanym tekstem, o ile jest on dostępny | Załączniki, awatary, miniatury, nazwy plików i oryginalne dane |
| Oznaczenia informujące, że autor/profil lub załącznik został zarejestrowany | Metadane dotyczące przekazywania i odpowiedzi, trasy sieciowe, adresy IP oraz dane uwierzytelniające |
| Liczba zdarzeń na wybranych kanałach, aktualne przełączniki kolekcji, sygnał kontrolny oraz interwał punktów kontrolnych | Elementy sterujące kolekcjami oraz standardowe interfejsy API do eksportu dowodów |
| Odcisk podpisu, punkt kontrolny dziennika i dowód spójności | Klucze podpisujące i sesje w Telegramie |

**Tekst wiadomości publicznych nie jest automatycznie anonimizowany.** Imię i nazwisko, wzmianka, numer telefonu lub link umieszczony w wiadomości pozostają częścią tego tekstu. `Redacted`Dotyczy to ustrukturyzowanych pól autora/profilu. Przed opublikowaniem sprawdź faktycznie wybraną treść, w tym zachowane edycje i usunięcia.

Kwalifikowalność odzwierciedla **najnowszy zapisany profil źródłowy**, a nie aktualne wyszukiwanie w Telegramie. Jeśli kolejny profil nie zawiera już nazwy użytkownika kanału publicznego, nowe żądania wykluczają ten kanał. Należy odświeżyć profile źródłowe, gdy zmieni się widoczność publiczna. Czytelnicy mogą już posiadać zapisane materiały, które otrzymali wcześniej.

Oryginalne podpisane zapisy pozostają niezmienione. Wyświetlana projekcja jest podpisywana osobno i zawiera skróty odwołujące się do oryginalnych zapisów. Podpis projekcji uwierzytelnia wyświetlany zapis; nie jest to podpis oryginalnego zdarzenia na zredagowanych bajtach.

## Sprawdź podpisy i ciągłość

Rozwiń **opcję „Fingerprint & signed checkpoint”** i pobierz migawkę. Po odświeżeniu strony pobierany plik zawiera poprzednią migawkę przeglądarki oraz dowód spójności Merkle’a między granicami dzienników. Automatyczne odświeżanie odbywa się raz na minutę, gdy strona jest widoczna i wyświetla pierwszą stronę obserwacji.

Po zainstalowaniu TgWitness sprawdź pobrany plik w trybie offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Odcisk palca musi pochodzić z oddzielnego, zaufanego źródła. Aby porównać go z migawką, którą sam zachowałeś, użyj `--previous earlier.json`; spowoduje to zastąpienie poprzedniej migawki zawartej w pobranym pliku. Aktualny dowód musi rozpoczynać się od tej zachowanej granicy. Uwierzytelnieni klienci mogą zażądać tego dowodu za pomocą `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Krótszy dziennik zwraca kod HTTP 409 zamiast cicho resetować granicę.

Podpisany punkt kontrolny jest zapisywany w **całym dzienniku kolektora**, łącznie z liczbą zapisów i nieprzejrzystym skrótem nagłówka. Wyświetlane liczby wiadomości odnoszą się wyłącznie do wybranych kanałów publicznych. Strona nigdy nie wyświetla zawartości innych dzienników. Są to liczby zdarzeń, a nie liczby unikalnych wiadomości. Ustawienia opisują aktualną konfigurację, a nie każdy wcześniejszy interwał rejestracji.

Weryfikacja podpisu i spójności pozwala wykryć zmiany w stosunku do zachowanego granicy. Nie obejmuje ona samodzielnego przeliczania podpisanych liczników, poświadczania pochodzenia z Telegrama, potwierdzania nieprzerwanego przechwytywania danych ani zastępowania niezależnego świadka. W tym celu należy skorzystać z [weryfikatora dowodów](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [niezależnego świadka](https://phishdestroy.github.io/TgWitness/pl/docs/reference/witness/) oraz [zapisu w skali testowej](https://phishdestroy.github.io/TgWitness/pl/docs/reference/verification/). Instalacje syntetyczne są wyraźnie oznaczone jako syntetyczne.

## Cofnij uprawnienia lub udostępnij stronę

Użyj **opcji „Cofnij”** w menedżerze prezentacji lub w istniejącej sekcji **„Dostęp**”, aby zamknąć link i zakończyć wszystkie związane z nim sesje. Odwiedzający usuwa wyświetlane zapisy, gdy żądanie wykryje, że dostęp został zakończony. Termin ważności i uprawnienia są sprawdzane przy każdym żądaniu. Uprawnień do prezentacji nie można przekształcić na miejscu w zwykły dostęp do panelu; aby zmienić tryb, należy utworzyć nowe uprawnienie.

Strona jest udostępniana za pośrednictwem istniejącego adresu HTTPS instalacji. Opublikowanie linku nie powoduje otwarcia nowego portu, utworzenia tunelu ani zmiany DNS. Kod HTML i API pozostają na instalacji użytkownika. Odwiedzający prezentację nie może korzystać ze zwykłych interfejsów API dotyczących wiadomości, profilu, multimediów, eksportu ani zarządzania w ramach tego dostępu.
