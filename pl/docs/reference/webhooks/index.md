# Wychodzące webhooki

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/webhooks/

Wysyłaj zdarzenia z określonym zakresem do odbiorców HTTPS z podpisami HMAC, ponownymi próbami i statusem dostarczenia.

**Aktualna wersja główna:** należy skorzystać z kopii źródłowej; przenośna wersja zapoznawcza 0.7.0 nie zawiera jeszcze tej funkcji.

[Przewodnik po procesie pracy](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Otwórz **sekcję „Integracje” → „Webhooki wychodzące”** w wybranym obszarze roboczym. Dodaj odbiornik HTTPS, wybierz zdarzenia związane z kolekcjonerem/multimediami/eksportem oraz opcjonalnie wybierz czaty dla nowych obserwacji i zmian. Tekst wiadomości jest domyślnie wyłączony. Włączenie fragmentów dodaje maksymalnie 1 000 znaków do zdarzeń związanych ze zmianami w wiadomościach; surowe pola Telegramu i dane uwierzytelniające nigdy nie są wysyłane.

Wprowadź klucz tajny HMAC jednorazowo do chronionej konfiguracji odbiorcy. Jest on zaszyfrowany w skarbcu TgWitness i nie można go odzyskać z panelu. Usuń i utwórz ponownie miejsce docelowe, aby je zmienić. **Wyślij** do**syntetycznych** kolejek **testowych** wiadomość bez treści czatu; odśwież status dostarczenia, aby sprawdzić wynik.

Dostarczanie rozszerza istniejącą pętlę powiadomień wraz z Apprise. Wykorzystuje trasę zewnętrzną obszaru roboczego oraz istniejące ograniczenia dotyczące prywatnych miejsc docelowych. Nie ma bezpośredniego rozwiązania awaryjnego ani przekierowania. Adresy URL nie mogą zawierać danych uwierzytelniających, ciągów zapytania ani fragmentów; adresy prywatne wymagają zgody na poziomie serwera, a nie ustawienia, które użytkownik panelu może ominąć.

## Dane użytkowe i podpis

Schemat: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Każdy ładunek zawiera `event_id`, `timestamp`, `workspace`, `type`, `synthetic` oraz liczniki. Zdarzenia oparte na dzienniku zawierają swoją sekwencję i skrót. Zakończenie pełnego eksportu oraz testy syntetyczne są zdarzeniami dostarczenia, bez fikcyjnego odniesienia do podpisanego dziennika. Powiadomienia o usunięciu wiadomości w Telegramie oraz `missing_on_recheck` pozostają odrębnymi typami.

Nagłówek `X-TgWitness-Signature` to `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Oblicz HMAC dla dokładnych bajtów `timestamp + "." + raw_request_body`, używając wyświetlonego klucza tajnego jako bajtów w formacie UTF-8. Porównaj podpisy w stałym czasie przed przetworzeniem lub podjęciem działań na treści wiadomości. Odrzuć sygnatury czasowe, które różnią się o więcej niż pięć minut od czasu lokalnego. Sygnatura czasowa jest odświeżana przy każdej próbie dostarczenia wiadomości.

Należy używać `event_id` jako klucza idempotencji w trwałej pamięci, z atomowym ograniczeniem unikalności przed wystąpieniem efektów ubocznych. Sam prawidłowy podpis nie zapobiega ponownemu odtworzeniu ostatniego żądania. Przetworzone identyfikatory należy przechowywać co najmniej przez cały okres ponownych prób; należy je przechowywać dłużej, jeśli odbiorca może ponownie przetworzyć zapisane zdarzenia.

## Ponowne próby

Dostarczanie zdarzeń jest trwale kolejkowane przed żądaniami HTTP. Stosowana jest semantyka „co najmniej raz” : utracone potwierdzenie lub ponowne uruchomienie może spowodować ponowne dostarczenie zdarzenia z tym samym identyfikatorem. Przewidziano osiem prób z wykładniczym opóźnieniem, zaczynającym się od 15 sekund i ograniczonym do jednej godziny. Warunkiem powodzenia jest otrzymanie odpowiedzi 2xx. Zadania, których limit prób został wyczerpany, pozostawiają widoczny błąd; dostarczenie nie jest gwarantowane po zakończeniu ponownych prób.

Kolejka mieści 1 000 dostaw. Gdy jest pełna, skanowanie zdarzeń dziennika zostaje wstrzymane i wznowione po zwolnieniu miejsca. Zakończenie pełnego eksportu, którego nie można umieścić w kolejce, powoduje wyświetlenie widocznego błędu kolejki. W ramach każdego przebiegu powiadomień podejmowanych jest do pięciu prób wysłania, a zachowywanych jest 100 ostatnich zapisów prób. Usunięcie miejsca docelowego powoduje również usunięcie oczekujących wysyłek.

## Przykład n8n

Zaimportuj [przykładowy przepływ pracy](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Jest on nieaktywny i nie zawiera żadnych poufnych danych ani działań następczych. Ustaw `TGWITNESS_WEBHOOK_SECRET` w środowisku roboczym n8n, zezwól na dostęp do tego środowiska oraz zezwól na użycie wbudowanej funkcji `crypto` dla węzła Code. W przykładzie wykorzystano opcję raw-body węzła Webhook, sprawdzono podpis i aktualność oraz potwierdzono zweryfikowane zdarzenia. Jest to zgodne z [udokumentowaną implementacją](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) tego węzła.

Przed dodaniem zapisów lub powiadomień do systemu SIEM należy dodać trwałą pamięć idempotentną, indeksowaną za pomocą klucza `event_id`. Należy ograniczyć edycję przepływów pracy w n8n oraz okres przechowywania dzienników wykonania zgodnie z danymi, które zdecydowano się wysłać. TgWitness nie dodaje żadnych poleceń przychodzących.
