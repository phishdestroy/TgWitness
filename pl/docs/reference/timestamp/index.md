# Sygnatury czasowe

Canonical page: https://phishdestroy.github.io/TgWitness/pl/docs/reference/timestamp/

Sygnatury czasowe zgodne z RFC 3161 dla podpisanych punktów kontrolnych: jakie dane są przesyłane do organu certyfikującego oraz w jaki sposób weryfikowana jest odpowiedź.

TgWitness przygotowuje żądania zgodne z RFC 3161 i weryfikuje odpowiedzi od podmiotu uprawnionego do nadawania znaczników czasu (TSA). Ta procedura ręczna nie obejmuje ani wyboru podmiotu TSA, ani przesyłania danych; tryb dowodowy wykonuje obie te czynności zgodnie z harmonogramem ([format dowodowy](https://phishdestroy.github.io/TgWitness/pl/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Przygotowane żądanie **nie** stanowi **jeszcze dowodu w postaci znacznika czasu**.

## Co potwierdza ten dowód

Schemat blokowy · Uwagi dotyczące konta → Łańcuch SHA-256 i podpisy Ed25519; Łańcuch SHA-256 i podpisy Ed25519 → Podpisany punkt kontrolny; Podpisany punkt kontrolny → Skrót z dokładnością do bajta oraz losowy nonce; Skrót z dokładnością do bajta oraz losowy nonce → Żądanie zgodne z RFC 3161; Żądanie zgodne z RFC 3161 → Niezależna agencja TSA; Niezależna agencja TSA → Podpisana odpowiedź TSA; Podpisany punkt kontrolny → Weryfikacja danych, wartości nonce oraz wyraźne zaufanie do urzędu certyfikacji (CA); Podpisana odpowiedź TSA → Weryfikacja danych, wartości nonce oraz wyraźne zaufanie do urzędu certyfikacji (CA) · Uwagi dotyczące konta · Łańcuch SHA-256 ipodpisy Ed25519 · Podpisany punktkontrolny · Skrót z dokładnościądo bajta oraz losowynonce · Żądanie zgodne z RFC3161 · Niezależna agencja TSA · Podpisana odpowiedźTSA · Weryfikacja danych,wartości nonce orazwyraźne zaufanie dourzędu certyfikacji(CA)

**Schemat w formie tekstowej**

1. Uwagi dotyczące konta → Łańcuch SHA-256 i podpisy Ed25519
2. Łańcuch SHA-256 i podpisy Ed25519 → Podpisany punkt kontrolny
3. Podpisany punkt kontrolny → Skrót z dokładnością do bajta oraz losowy nonce
4. Skrót z dokładnością do bajta oraz losowy nonce → Żądanie zgodne z RFC 3161
5. Żądanie zgodne z RFC 3161 → Niezależna agencja TSA
6. Niezależna agencja TSA → Podpisana odpowiedź TSA
7. Podpisany punkt kontrolny → Weryfikacja danych, wartości nonce oraz wyraźne zaufanie do urzędu certyfikacji (CA)
8. Podpisana odpowiedź TSA → Weryfikacja danych, wartości nonce oraz wyraźne zaufanie do urzędu certyfikacji (CA)

Podpis kolektora wiąże zapisy z jego kluczem. Wiarygodna odpowiedź TSA może potwierdzić, że konkretny punkt kontrolny istniał w podanym przez TSA czasie. Punkt kontrolny może następnie powiązać prefiks dziennika. Nie ustala to jednak czasu każdej czynności w Telegramie ani prawdziwości zarejestrowanej treści.

## Procedura

1. Należy zachować odcisk klucza kolektora za pośrednictwem oddzielnego, zaufanego kanału. Klucz pochodzący wyłącznie z badanego pliku ZIP nie jest wystarczający do identyfikacji kolektora.
2. W **sekcji Eksportuj → Przygotuj żądanie znacznika czasu** proszę pobrać plik ZIP z żądaniem dla wybranego obszaru roboczego. Proszę rozpakować pliki `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` oraz `README.txt`. Proszę nie zmieniać bajtów punktu kontrolnego.
3. Proszę wybrać TSA odpowiedni do danego dochodzenia. Proszę przesłać plik `timestamp.tsq`, korzystając z udokumentowanej metody, a plik `application/timestamp-query` – w przypadku usługi HTTP. Proszę zapisać oryginalną odpowiedź binarną jako plik `timestamp.tsr` wraz z punktem końcowym, czasem pobrania oraz wynikiem żądania. Żądanie zawiera skrót i licznik losowy zamiast samych wiadomości; metadane sieciowe nadal ujawniają treść żądania.
4. Należy uzyskać zaufany certyfikat główny niezależnie od treści odpowiedzi, a także wszelkie wymagane certyfikaty pośrednie. Certyfikat zawarty w odpowiedzi nie staje się zaufany wyłącznie z tego powodu, że się tam znajduje.
5. Z poziomu zaufanej instalacji TgWitness proszę zweryfikować:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

W razie potrzeby proszę dodać `--intermediates tsa-intermediates.pem` lub `--openssl /path/to/openssl`. OpenSSL musi obsługiwać `ts`. W systemie Windows narzędzie weryfikacyjne przeszukuje również standardową instalację Git. OpenSSL w wersji 3.5.9 został przetestowany lokalnie przy użyciu syntetycznego certyfikatu CA/TSA.

1. Proszę wyeksportować plik ZIP z podpisanym dziennikiem po osiągnięciu punktu kontrolnego, tak aby zawierał on ten prefiks. Proszę zweryfikować przy użyciu niezależnie znanego odcisku palca:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Należy zachować plik ZIP, punkt kontrolny, żądanie, odpowiedź, łańcuch certyfikatów, wyniki weryfikacji oraz zapis przekazania poza kolektorem. Weryfikację należy powtórzyć w momencie odbioru.

Aby przygotować zapytanie na podstawie zapisanego punktu kontrolnego:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Proces przygotowania standaryzuje format JSON i dołącza odpowiedni punkt kontrolny do archiwum. Należy wykorzystać **bajty punktu kontrolnego z tego archiwum** do weryfikacji TSA, nawet jeśli plik wejściowy zawierał inne znaki spacji.

## Granice weryfikacji

| Sprawdź | Obecne działanie |
| --- | --- |
| Dane | Wartość SHA-256 dokładnych bajtów punktu kontrolnego musi być zgodna z odpowiedzią |
| Zapytanie | W przypadku algorytmu `--request` weryfikowane są oryginalne zapytanie oraz wartość nonce |
| Podpis TSA | OpenSSL weryfikuje podpis oraz łańcuch certyfikatów aż do wskazanej instytucji certyfikującej (CA) |
| Podpis zbierającego | Oddzielnie zweryfikowane przez weryfikatora dziennika przy użyciu przypiętego klucza |
| Unieważnienie | Brak automatycznego pobierania plików OCSP/CRL |
| Długoterminowa ważność | Brak weryfikacji archiwalnej po wygaśnięciu certyfikatu |
| Zaplanowane przesłanie | Tryb dowodowy, domyślnie wyłączony |

`--request` jest technicznie opcjonalny, jednak jego pominięcie uniemożliwia weryfikację oryginalnego wartości nonce. Aby procedura przebiegła w całości, wynik `request_checked` musi być prawdziwy. Weryfikacja certyfikatu odbywa się zgodnie z zasadami i czasem weryfikacji zainstalowanego pakietu OpenSSL. Długoterminowe przechowywanie wymaga odrębnej polityki dotyczącej certyfikatów i dowodów unieważnienia.

Ważny podpis kryptograficzny nie stanowi automatycznie kwalifikowanego znacznika czasu ani ustalenia dotyczącej dopuszczalności dowodowej. Jeśli operator sfabrykował obserwacje przed naniezieniem znacznika czasu, TSA zakotwicza te bajty; nie potwierdza to jednak ich prawdziwości.

## Rejestr przekazania

Należy zarejestrować identyfikator sprawy, nadawcę i odbiorcę, czas przesłania w formacie UTC oraz jego źródło, cel, nazwy plików/wartości SHA-256, odcisk palca kolektora, zakres sekwencji, znane luki, wersję weryfikatora oraz wynik weryfikacji. Proszę podpisać i przechowywać ten zapis niezależnie, zgodnie z procedurami obowiązującymi w Państwa organizacji. System rejestracji dowodów obsługujący wielu użytkowników nie jest zaimplementowany w TgWitness.

W trakcie opracowywania nie nawiązano kontaktu z żadnym niezależnym podmiotem TSA działającym w trybie rzeczywistym. W ramach testów lokalnych tworzony jest syntetyczny podmiot CA/TSA w celu sprawdzenia zgodności oraz odrzucenia zmienionych danych, wartości nonce lub certyfikatu CA.
