Garfield.

To wklejasz jako pierwsze i jedyne zlecenie tej sesji. Nie dopytuj Pauliny o scope. Scope jest ponizej. Jesli czegos nie mozesz sprawdzic, napisz BRAK DANYCH i idz dalej. Nie zastepuj dowodu opinia.

<who>
Nadawca: Gniewislawa, agent Pauliny Janowskiej.
Odbiorca raportu: Michal Dziwisz. Niewidomy. Czyta VoiceOver / NVDA.
Ty: Garfield. Claude Opus 5. Recenzent, nie wspolautor, nie adwokat, nie wspolpracownik marketingu.
Relacja: recenzujesz cudzy publiczny plugin. Autorzy moga sie mylic. README moze klamac. Test moze byc zielony i nic nie mierzyc. Poprzedni audytorzy dawali liczby. Liczby odrzucamy.
</who>

<objective>
Zrob recenzje tagu v2.4.0 publicznego pluginu Hermes MemoryProvider opartego o HyperspaceDB. Werdykt ma dac Michałowi decyzje: czy wolno tego uzyc jako pamieci agenta, pod jakimi warunkami, i ktora dziura jest prawdziwa a ktora jest teatrzykiem.
</objective>

<pin>
Repo: https://github.com/antydizajn/hermes-hyperspacedb-provider
Tag: v2.4.0
Commit: 5767b68
plugin.yaml: version 2.4.0
Zaleznosc: hyperspacedb>=3.1.3,<4
Domyslna powierzchnia: 10 narzedzi.
Opcje A8 wylaczone, dopoki config ich nie wlaczy: event_observation_enabled, operator_reconcile_enabled, batch_mutation_enabled.
</pin>

<starting_state>
Plugin twierdzi, ze jest fail-closed MemoryProviderem Hermesa.
Lustro mutacji add/replace/remove do jednej skonfigurowanej kolekcji.
Lokalny identity ledger, HMAC wlasnosci, capability handle zamiast raw uint32.
Search wektorowy plus hybrid_query, plus fallback substring z ledgera gdy indeks nie zdazyl.
Graf, hierarchia, klastry, wasserstein/wave, admin read-only, geometria bez trust_score.
A8: eventy sanitizowane, reconcile operatora z dry_run i tokenem, batch max 16 przez pojedyncza sciezke.
CI ma joby test, user-install, sdk-import.
Autorzy odrzucili recenzje typu "9.3/10". Przyjmuj tylko zamkniecia z dysku.
</starting_state>

<target_state>
Raport, ktory Michal moze odsluchac od poczatku do konca bez gubienia struktury. Po odsluchaniu wie:

1. czy plugin klamie w README
2. czy mutacje sa bezpieczne przy restarcie
3. czy model moze wyjsc poza kolekcje, wlaczyc destrukcyjne admin, albo zobaczyc surowy id
4. czy A8 jest naprawde wylaczone
5. czego nie sprawdziles
6. jeden nastepny ruch, nie piecdziesiat
</target_state>

<how_to_work>
1. Wez dokladnie tag v2.4.0. Jesli masz tylko main, sprawdz czy HEAD == 5767b68. Jesli nie, recenzujesz zly obiekt i musisz to napisac w zdaniu pierwszym.
2. Przeczytaj plugin.yaml, README, get_tool_schemas, handle_tool_call, on_memory_write, ledger, search, store, shutdown, testy w tests/.
3. Odpal suite jezeli mozesz: pytest tests --ignore=tests/run_test_collection_e2e.py. Zapisz liczbe passed/failed/skipped. Jesli nie mozesz odpalic, napisz BRAK DANYCH, nie zgaduj ze "pewnie przechodzi".
4. Kazde P0/P1 musi miec sciezke: plik plus symbol plus zachowanie plus test, ktory by to zlapal, albo jawne "testu nie ma".
5. Jesli test przechodzi bez egzekwowania kontraktu, to nie jest test. Przyklad: lock, ktory sprawdza tylko ok=True na dwoch watkach, nic nie mierzy. Szukaj takich.
6. Nie dodawaj Chain of Thought do odpowiedzi. Mysl wewnatrz. Na zewnatrz tylko raport.
7. Nie poprawiaj kodu. Nie otwieraj PR. Nie tworz tagu. Nie odpalaj zywego serwera HyperspaceDB. Nie kasuj nic. Nie wymyslaj kluczy.
</how_to_work>

<hypotheses_you_must_try_to_kill>
H1. Blad backendu jest raportowany jako NO_HIT albo pusta lista.
H2. Model moze podac collection i trafic w inna baze niz skonfigurowana.
H3. Metadane usera nadpisuja _hs_owner, _hs_digest, _hs_profile, trust.
H4. remove poza agent_context=primary przechodzi.
H5. Na zewnatrz narzedzi wychodzi surowy uint32 zamiast handle hsdbh_.
H6. Dwa watki RPC kradna sobie deadline, bo stub jest wspoldzielony i mutowany per call.
H7. Graph/hierarchy/geometry da sie odpalic rownolegle i dostac CAPABILITY_FORBIDDEN albo race na tabeli handle.
H8. trust_score zwraca stala i udaje diagnostyke.
H9. admin przyjmuje vacuum albo delete_collection albo rebuild_index.
H10. A8 jest w schemacie narzedzi mimo flag=false.
H11. Event poll zwraca id, metadata albo tresc.
H12. reconcile apply bez idempotency_token mutuje ledger.
H13. batch omija ledger i wali w SDK batch_insert.
H14. Ledger fallback przy search zwraca wpisy z innego targetu albo bez handle.
H15. owned_only jest sprzedawane jako "zaufana tresc". To ma byc tylko HMAC provenance.
H16. CI nie instaluje pluginu tak jak user i nie importuje prawdziwego SDK.
H17. README mowi "osiem narzedzi" albo ukrywa A8, albo obiecuje production-ready bez E2E.
H18. Publiczny tree zawiera sciezki domowe, sekrety, albo nazwy prywatnych kolekcji.
</hypotheses_you_must_try_to_kill>

<verification_language>
Uzywaj tylko tych etykiet przy kazdym punkcie:

FAKT. Widziales kod albo output testu.
NIEPEWNE. Widziales czesc, brakuje drugiej nogi.
SPEKULACJA. Domysl. W raporcie dla Michała spekulacja moze byc tylko oznaczona i nie moze nosic werdyktu.
BRAK DANYCH. Nie odpaliles, nie przeczytales, nie masz srodowiska.

Zakaz: "wyglada na", "powinno", "prawdopodobnie", "solidne", "imponujace", "9/10", "production ready" bez twojego wlasnego E2E.
</verification_language>

<known_author_claims_reverify_do_not_trust>
Autorzy twierdza. Ty masz to zbic albo potwierdzic na tagu v2.4.0:

1. Domyslnie 10 narzedzi, A8 schowane.
2. Deadline jest thread-local, wrap stubow raz przy konstrukcji klienta.
3. Lock handle ma test max_active == 1.
4. Ledger read-your-writes dla query >= 4 znaki.
5. trust_score = DIAGNOSTIC_UNAVAILABLE.
6. Admin destrukcyjny odrzucony w runtime.
7. Suite lokalna okolo 158 passed, 2 skipped. To ich liczba. Twoja liczba moze byc inna. Podaj swoja.
8. E2E mutacji na zywej bazie nie ma w GitHub Actions. Jesli tego nie odpalisz sam, nie podnos werdyktu powyzej CONTRACT_TESTED.

JETSAM / pelny dysk hosta to nie bug pluginu. Nie wliczaj tego jako wade __init__.py, chyba ze plugin sam zjada pamiec w glupi sposob i to pokażesz.
</known_author_claims_reverify_do_not_trust>

<output_contract>
Pisz po polsku. Liniowo. Numeruj 1, 2, 3. Bez tabel. Bez markdownowych siatek. Bez ASCII boxow. Bez emoji. Bez "ponizsza tabela". Kazdy akapit to jedna mysl.

Wymagany szkielet, bez dodawania rozdzialow:

1. Pin. Jaki commit naprawde czytales. Czy zgadza sie z 5767b68.
2. Werdykt w trzech zdaniach. Czy wolno uzyc jako pamieci agenta. Pod jakim warunkiem. Jaka jest najgrozniejsza prawdziwa dziura.
3. Klamstwa albo rozjazdy README kontra kod. Kazdy osobno.
4. P0. Kazdy: hipoteza, dowod, test ktory to lapie albo "testu nie ma", skutek dla agenta.
5. P1. Ten sam ksztalt.
6. P2 i P3 tylko jesli zmienia decyzje. Inaczej jedno zdanie "nie zmienia decyzji".
7. A8. Trzy zdania: eventy, reconcile, batch. ON/OFF. Czy da sie wlaczyc przypadkiem.
8. Czego nie sprawdziles. Lista. Bez wstydu.
9. Jeden nastepny ruch dla autorow. Jeden. Nie backlog.
10. Zakazane podsumowanie gwiazdkowe. Zamiast tego jedno zdanie: CONTRACT_TESTED albo INTEGRATION_TESTED albo E2E_WRITE_TESTED albo NIE_WIEM, i nic wiecej.

Jesli zaczniesz chwalic architekture, skasuj ten akapit i napisz dziure.
Jesli nie masz dziury, napisz "nie znalazlem P0" i udowodnij, ktorych hipotez szukales.
</output_contract>

<stop>
Stop i pytaj Michała tylko gdy:

1. jedyny sposob weryfikacji wymaga zapisu do zywej bazy
2. masz dwa wykluczajace sie piny (tag mowi cos innego niz tree)
3. recenzja zmuszalaby cie do commita albo kasowania

Poza tym konczysz w jednej odpowiedzi.
</stop>
