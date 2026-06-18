# Analiza varijacija u trenucima pomračenja kod eklipsno dvojnih sistema i statistička analiza parametara potencijalnog trećeg tela u sistemu

![MASS-UBMATF](https://img.shields.io/badge/MASS--UBMATF-Astrostatistics_2026-blue)

## Kratak opis projekta
Ovaj projekat se bavi analizom $O-C$ (*Observed minus Calculated*) dijagrama eklipsno dvojnih zvezdanih sistema sa ciljem detekcije varijacija u njihovim trenucima pomračenja. Glavni fokus je identifikacija efekta svetlosnog kašnjenja (engl. *Light-Time Effect - LTE*) koji ukazuje na prisustvo orbitalnog kretanja oko zajedničkog centra mase sa potencijalnim trećim telom (zvezdom koja nije dovoljno sjajna da bismo je primetili pri posmatranjima krive sjaja).

Program učitava podatke o trenucima pomračenja eklipsno dovjnih sistema, konstruiše OC dijagrame, vrši frekventnu analizu pomoću Lomb-Scargle periodograma radi pronalaska periodičnosti, odnosno pretpostavljene vrednosti orbitalnog perioda trećeg tela, a zatim nelinearno fituje (`scipy.optimize.curve_fit`) podatke sa OC dijagrama funkcijom svetlosnog kašnjenja. Iz fita izvlači orbitalne parametare trećeg tela (vreme prolaska kroz perihel, period, ekscentricitet, asini, argument perihela i šift po y osi). Koristeći bootstrap metodu određuje neodređenosti parametara dobijenih fitovanjem. Nakon toga računa minimalnu masu trećeg tela i neodređenost bootstrap metodom.

---

## Struktura repozitorijuma
* `Podaci/` - Folder koji sadrži CSV fajlove sa trenucima pomračenja za 259 sistema (veličina ~3.4MB).
* `funkcije.py` - Modularni Python fajl u kojem su definisane sve matematičke i astronomske funkcije (uključujući `OC_trece_telo`) koje se koriste u analizi.
* `demo_sample.ipynb` - **Glavni notebook za prezentaciju**. Pokreće kompletnu analizu uživo za jedan reprezentativni sistem i učitava pre-izračunate statistike.
* `full_run_results.ipynb` - Notebook sa sačuvanim izlazima koji prikazuje izvršavanje koda za sve sisteme u bazi (vreme izvršavanja ~45 minuta).
* `Rezultati.csv` - Tabela sa generisanim finalnim parametrima i fitovanim vrednostima za sve sisteme, dobijena iz pokretanja fajla `full_run_results.ipynb`.
* `requirements.txt` - Spisak svih potrebnih Python paketa za pokretanje i testiranje koda.

---

## Uputstvo za pokretanje i reprodukciju

### 1. Instalacija okruženja
Pre pokretanja notebook-ova, potrebno je instalirati sve zavisnosti iz `requirements.txt` fajla. 

### 2. Pokretanje
Otvoriti `demo_sample.ipynb` i pokrenuti Restart & Run All”.
