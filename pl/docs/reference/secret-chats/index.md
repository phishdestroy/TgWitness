# Telegram · Ciche czaty: implementacja i demonstracja

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/secret-chats/

Zapoznaj się z oddzielną implementacją funkcji Secret Chat, wypróbuj fikcyjny interfejs i przejrzyj pozostałe usterki.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentacja](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Stan sprawdzony 6 listopada 2026 r.:** istnieje osobna implementacja Secret Chat w fazie rozwoju. Nie została ona scalona z opublikowaną gałęzią `main` w wersji `3d23e52b647b`. Zwykły kolektor i eksport Takeout nie gromadzą danych z Secret Chat. Interaktywny scenariusz na stronie internetowej demonstruje interfejs przy użyciu fikcyjnych danych; nie umożliwia on komunikacji w Telegramie.

## Gdzie znajduje się implementacja

Commit `0e60f88e` dodał **Sources → Pseudo-secret** w lokalnej gałęzi rozwojowej `fix/panel-routes-sessions`. Sprawdzona migawka to `bb8788fb685c`. Jej implementacja obejmuje `tgwitness/secret_chats.py`, trasy aplikacji, `tgwitness/static/views/secret-chats.js` oraz dedykowane testy.

Opcjonalny dodatek `secret-chats` w tej gałęzi wykorzystuje [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), przypisany do `d87bf037b90060383c7b704d8a06ebb98c621c6f`. Biblioteka implementuje protokół czatu typu end-to-end serwisu Telegram w oparciu o istniejącą autoryzację Telethon dla danego konta. Sama instalacja tej biblioteki nie dodaje brakującej integracji do `main`.

## Jak działa interfejs programistyczny

| Działanie | Zarejestrowane zachowanie |
| --- | --- |
| Rozpocznij czat, podając nazwę użytkownika lub identyfikator użytkownika | Wyślij zaproszenie; drugi uczestnik musi je zaakceptować. |
| Przyjmij przychodzące żądanie | TgWitness staje się punktem końcowym odbiorczym dla tej rozmowy. Automatyczna akceptacja jest oddzielnym ustawieniem, domyślnie wyłączonym. |
| Wysyłanie lub odbieranie wiadomości | Należy dodać wychodzący lub przychodzący rekord typu `secret_chat.message` i wyświetlić go w wątku. |
| Otrzymaj załącznik | Należy je odszyfrować, zapisać ich bajty według SHA-256 oraz zarejestrować `secret_chat.file`. |
| Otrzymaj powiadomienie o upływie czasu lub usunięciu | Należy odnotować komunikat i zachować wcześniej zebrane treści. |
| Przejrzyj rozmowę | Wyświetlaj wiadomości, pliki, powiadomienia oraz wizualizację klucza. Otwarta karta odświeża się co cztery sekundy. |

W kompilacji deweloperskiej zawierającej tę integrację operator włącza moduł dla wybranego konta i łączy się z nim. Rozpoczęcie, akceptacja i wysyłanie wymagają uprawnienia do interakcji oraz wyłączenia ochrony konta w trybie tylko do odczytu. Drugi uczestnik musi zaakceptować nową rozmowę wychodzącą. Te elementy sterujące nie występują w opublikowanej aplikacji w powyższej wersji.

Uwzględnione są wyłącznie czaty utworzone lub zaakceptowane przez tę sesję TgWitness. Istniejące tajne czaty na telefonie pozostają na tym urządzeniu. Import sesji nie dostarcza ich oddzielnych kluczy szyfrujących. Materiały kluczy tajnych czatów i liczniki są przechowywane w skarbcu obszaru roboczego; zachowane wiadomości i odszyfrowane pliki podlegają standardowym zabezpieczeniom pamięci masowej obszaru roboczego.

## Prezentacja na stronie internetowej

Scenariusz „**Try Secret Chat**” na stronie internetowej przedstawia fikcyjną rozmowę. Pozwala on czytelnikowi zainicjować żądanie, zasymulować jego przyjęcie, wysłać przykładową wiadomość, otrzymać z góry ustaloną odpowiedź i plik oraz sprawdzić licznik czasu i powiadomienie o usunięciu. Przychodzące żądanie można również przyjąć. Elementy sterujące wyraźnie oznaczają symulowane działania drugiej strony.

Ten scenariusz działa w pamięci przeglądarki. Zresetowanie lub ponowne załadowanie strony powoduje jego wyczyszczenie. Nie loguje się, nie łączy się z Telegramem, nie tworzy rzeczywistych kluczy szyfrujących ani nie zmienia podpisanych plików próbnych do pobrania. Wyświetlane przez niego komunikaty nie stanowią podpisanych dowodów. Scenariusz ten ilustruje zamierzoną interakcję; nie potwierdza on, że implementacja programistyczna jest gotowa.

## Sprawdzenia i pozostałe usterki

Pięć istniejących testów obejmuje trwałość klucza szyfrującego, cykl życia i zapisy wiadomości, politykę akceptacji wiadomości przychodzących, wysyłanie w trybie tylko do odczytu oraz eksport załączników. Zostały one pomyślnie przeprowadzone w odniesieniu do przypiętej biblioteki podczas przeglądu z 6 listopada. Trzy dodatkowe testy syntetyczne odtworzyły usterki w tej samej migawce:

| Wyniki | Konsekwencja |
| --- | --- |
| Zamknięcie omija `read_only` | Ścieżka zamknięcia może wykonać zdalne działanie, gdy interakcje powinny zostać zablokowane. |
| Wykrywanie duplikatów przeszukuje wyłącznie najnowsze rekordy z 500 | Starsze odtworzenie może spowodować utworzenie duplikatu po ponownym uruchomieniu. |
| Nieudane pobranie załącznika powoduje usunięcie jego oczekującego wpisu | Przejściowa awaria powoduje utratę zadania ponownej próby. |

Są to otwarte usterki, odnotowane również w opublikowanym audycie . Pięć pomyślnie zakończonych testów nie obejmuje tych błędów. W ramach przeglądu wykorzystano syntetyczne środowiska robocze oraz symulowano operacje Telegrama; nie powtórzono rzeczywistego nawiązania połączenia ani nie oceniono wdrożenia w środowisku produkcyjnym.
