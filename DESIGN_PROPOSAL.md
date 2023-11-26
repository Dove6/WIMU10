# Opracowanie nowych metryk do ewaluacji muzyki symbolicznej w formacie MIDI

Temat realizowany przez zespół nr 10 w składzie:

- Moroz Bartłomiej,
- Motyka Jakub,
- Sygocki Dawid,
- Walczak Jan.

## Planowana funkcjonalność programu

Program ma przyjąć formę otwartoźródłowej biblioteki do języka Python.
Decyzję taką podjęliśmy ze względu na potencjalne wykorzystanie w kodzie modeli uczenia maszynowego. Integracja takiego kodu z narzędziem wyłącznie konsolowym byłaby niepraktyczna.
API biblioteki składać się będzie z zestawu funkcji do oceny jakości muzyki w formacie MIDI [^back1999].

Repozytorium zawierać będzie również przykładowy program (skrypt) konsolowy prezentujący sposób korzystania z API.
Program pozwalał będzie na wyznaczenie metryk dla wybranych plików w trybie wsadowym.

### Oferowane metryki (propozycje, pomysły)

1. Jednym z kierunków badania będzie wykorzystanie łańcuchów Markova do oceny powtarzalności [^dai2022] wewnątrz utworu.
   Zainspirujemy się analizą łańcuchów DNA, aby uwzględnić przerwy pomiędzy fragmentami utworu oraz wariacje takie jak wprowadzenie ozdobników, nut pośrednich, rozdrobnienie rytmu, itp.
   Łańcuchy Markova zostały już wykorzystane w dziedzinie MIR przy uczeniu i ocenianiu modelu [^chi2020] poprzez próbkowanie Gibbsa.
   Samopodobieństwo możemy sprawdzać pod względem:
   - *melodycznym* - ogólna powtarzalność wysokości i rytmu dźwięków, szczególnie w sekcji perkusyjnej,
   - *dynamicznym* - spójność głośności na przestrzeni utworu:
     - ta sama ogólna głośność przez cały utwór lub przynajmniej w jego sekcjach,
     - powtarzalność schematów zmiany głośności w powiązaniu z elementami utworu (np. pod koniec każdego zdania),
   - *agogicznym* - spójność tempa, jw.,
   - *harmonicznym* - podobieństwo pochodów akordów (po "skwantyzowaniu" melodii do akordów); można uwzględnić zmiany klucza i badać akordy nie bezwględnie, ale jako stopnie tonacji,
2. Zauważyliśmy, że zbiór statystycznych metryk obecnych w MusPy [^dong2020] [^yang2020] jest niewielkich rozmiarów i można go potencjalnie rozszerzyć. Sugerując się m.in. [^ji2020] [^xiong2023], proponujemy wstępnie następujące miary:
   - *wysokościowa/harmoniczna* - histogram klas akordów występujących w formie melodycznej (sekwencyjnie) i harmonicznej (wielogłosowo, jako współbrzmienie);
     trudność polega na dopasowywaniu akordów zależnie od przyjętej granularności
     (czy bierzemy pod uwagę strukturę utworu i dopasowujemy akord na takt lub miarę, czy może przetwarzamy sekwencję w następujących po sobie grupach nutowych niezależnie od ich wartości rytmicznej i umiejscowienia),
   - *wysokościowa/harmoniczna* - macierz przejść między klasami akordów na podstawie miary wyżej opisanej, analogicznie do istniejącej już w MusPy metryki histogramu wysokości i macierzy przejść między wysokościami;
     dopasowane klasy akordów nie muszą jednak bezpośrednio sąsiadować - mogą być rozdzielone pojedynczymi nutami (problem taki nie występuje we wspomnianej metryce z MusPy),
   - *rytmiczna* - podsumowanie liczby synkop (przesunięć akcentu na "słabą" część taktu),
     potencjalnie również w formie histogramu, bo istnieje ograniczona liczba wzorców (np. szesnastka + ósemka + szesnastka),
   - *rytmiczna* - alternatywa do miary poprzedniej, czyli ile razy dłuższa nuta przypada na "silną" część taktu,
   - *wysokościowa/harmoniczna* liczba zmian tonacji;
     wymaga wpierw wykrycia tonacji - można się wspomóc metazdarzeniem zmiany znaków przykluczowych (`FF 59 02`) zdefiniowanym w standardzie MIDI, ale nie jest to równoważne ani nawet jednoznaczne,
   - *dynamiczna* - liczba zmian głośności: stopniowych (crescendo, decresendo; sąsiedztwo głośności zbliżonych, np. p -> mp) oraz nagłych (sąsiedztwo głośności skrajnych, np. p -> f; akcenty),
     z podziałem na instrumenty lub całościowo dla utworu;
     podział na sekcje o danej głośności utrudnia fakt, że każde zdarzenie Note On definiuje ją osobno,
   - *agogiczna* - liczba zmian w tempie (metazdarzenie `FF 51 03`);
     na poziomie MIDI "ogólne" zmiany tempa są nieodróżnialne od chwilowych przyspieszeń lub spowolnień (accel., rit., fermata), ale można próbować je sklasyfikować ze względu na długość oraz umiejscowienie,
   - *rytmiczna* - liczba zmian metrum (metazdarzenie `FF 58 04`),
     pytaniem pozostaje, czy istnieją modele generatywne, które zmiany metrum wspierają.

Opisane wyżej metryki można wyliczyć dla istniejących utworów reprezentujacych różne gatunki (niżej opisany zbiór danych nr 1) i na podstawie wyników próbować klasyfikować utwory wygenerowane (zbiór danych nr 2).
Podobnie jak w algorytmie "Inception Score", wysoka niejednoznaczność klasyfikacji pojedynczego utworu mogłaby oznaczać słabą "ostrość" reprezentowanego przez niego gatunku, a więc słabą jakość.
Uważać trzeba na przypadki szczególne - mieszanie gatunków w obrębie pojedynczego utworu, gatunki pośrednie lub niedookreślone.

Ponadto, możemy próbować przekształcić powyższe metryki na dwustopniowe lub trzystopniowe miary subiektywne (jakość dobra - zła oraz brak wpływu metryki na ocenę).
Jesteśmy w stanie dokonać badań statystycznych polegających na ocenie wycinka zbiorów danych w obrębie naszego zespołu.
Badania takie miałyby na celu określenie akceptowalnych i nieakceptowalnych zakresów wartości wyznaczonych metryk.

## Zbiory danych

Zgrubny podział zbiorów danych:

0. ręcznie spreparowane minimalne dane testowe do sprawdzania poprawności działania metryk,
1. istniejące utwory w MIDI (podzbiór katalogu oferowanego w ramach MusPy),
2. utwory w MIDI wygenerowane z użyciem istniejących, wytrenowanych modeli uczenia maszynowego (technologia GAN [^dong2017] lub Transformer [^huang2018]).

Dla obu zbiorów wyznaczymy wartości metryk opracowanych przez nas, jak i obecnych już w MusPy (celem porównania).

### Analiza wybranych zbiorów danych dostępnych w MusPy
Przy analizie zbiorów danych ustaliliśmy następujące ograniczenia:
* zbiory muszą być dostępne poprzez interfejs MusPy,
* interesują nas tylko utwory w formacie MIDI,
* nie uwzględniamy chorałów i hymnów.
W ten sposób otrzymaliśmy listę pięciu zbiorów danych nadających się do naszego zadania, których analizę zamieszczamy poniżej. Zagadnienia, które uznaliśmy za ważne, to:
* jakość plików MIDI/transkrypcji,
* sposób pozyskania danych,
* rozmiar zbioru danych,
* rodzaj muzyki,
* liczba instrumentów/kanałów,
* ewentualna potrzeba dodatkowego przetwarzania,
* popularność/wykorzystanie w innych pracach.

- The Lakh MIDI Dataset [^raffel2016dataset] [^raffel2016] - Największy z dostępnych zbiorów danych. Zawiera 176 581 różnych utworów w formacie MIDI (>5000h), 45 tys. z których znalazło dopasowanie w wpisach z zestawu danych "Million Song Dataset" [^bertin-mahieux2011]. Zbiór zawiera wyłącznie pliki pobrane z Internetu z publicznie dostępnych źródeł. Przy zbieraniu których nie stosowano żadnej kontroli jakości, w konsekwencji znajdują się w nim także pliki o niepoprawnym formacie, wyjątkowo krótkie lub niskiej jakości. Na podstawie tego zestawu danych powstał zestaw "Lakh Pianoroll Dataset" [^dong2017dataset] [^dong2017], który po oczyszczeniu zawiera 174 154 plików. Ten zestaw został później wykorzystany w wytrenowaniu modelu MuseGAN [^dong2017].
- MAESTRO [^hawthorne2018] - Zestaw zawierający 1282 utworów (~201h) muzyki klasycznej na fortepian. Udostępnia zarówno pliki w formacie MIDI, jak również ich odpowiedniki w formacie WAV oraz metadane w formacie CSV i JSON zawierające informacje o artystach, czasy trwania oraz nazwy utworów. Zbiór powstał przy współpracy z organizatorami konkursu "International Piano-e-Competition", podczas którego wszystkie utwory były wykonywane na fortepianach Yamaha Disklavier nagrywających MIDI. Autorzy nie podają informacji o wcześniejszym przetworzeniu danych, a artykuły wykorzystujące MAESTRO [^bittner2022] nie wskazują na to, że jest one potrzebna do pracy z zestawem.
- NES-MDB (Nintendo Entertainment System Music Database) [^donahue2018] - Zestaw składający się z 5278 różnych utworów (~46h) zebranych z 397 gier na konsolę NES (Nintendo Entertainment System). Pliki MIDI zostały otrzymane przez konwersję z natywnego dla NES formatu muzyki (instrukcji wbudowanego czterokanałowego syntezatora dźwięku). W porównaniu z pozostałymi zestawami danych, bardzo mała ilość artykułów wykorzystuje NES-MDB.
- MusicNet [^thickstun2017] - Zbiór 330 wieloinstrumentalnych utworów muzyki klasycznej (~30h) zawierający pliki MIDI, WAV, CSV (utwory w postaci etykiet nut) i metadane. W skład wchodzą utwory następujących kompozytorów: Bach, Beethoven, Faure, Brahms, Haydn, Cambini, Dvorak, Mozart oraz Schubert. Pliki MIDI to publicznie dostępne, ręcznie wykonane transkrypcje zapisu nutowego. W artykule "MT3: Multi-Task Multitrack Music Transcription" [^gardner2022] w zestawieniu z kilkoma innymi zestawami danych (MAESTROv3 [^hawthorne2018], Slakh2100 [^manilow2019], Cerberus4 [^manilow2020], GuitarSet [^xi2018], URMP [^li2018]) dla zestawu MusicNet osiągnięto najniższe wyniki, wspominając o niewielkim rozmiarze materiału uczącego i złym wyrównaniu w czasie nagrań i etykiet. Druga z wymienionych wad nie ma dla nas znaczenia, ponieważ operujemy wyłącznie na reprezentacji symbolicznej.
- EMOPIA (A Multi-Modal Pop Piano Dataset For Emotion Recognition and Emotion-based Music Generation) [^hung2021] - Zestawienie 1087 fragmentów 387 utworów (~11h), skupione na postrzeganiu emocji w muzyce popowej/filmowej na pianino. Wszystkie fragmenty zostały przydzielone do jednej z czterech grup na podstawie ich pozytywności ("valence") oraz pobudzenia ("arousal"). Transkrypcję z audio do MIDI otrzymano przy wykorzystaniu modelu AI [^kong2020].

## Planowany zakres eksperymentów

1. Zbadamy graniczne oraz umiarkowane wartości niektórych metryk poprzez spreparowanie plików MIDI o odpowiedniej charakterystyce.
   W przypadku łańcuchów Markova zależy nam na wartościach dla braku powtarzalności, stuprocentowej powtarzalności oraz umiarkowanej powtarzalności w postaci znanych form okresowych utworów (ABA, ABA', AABA, ABAC, itd.)
2. Dla wybranych zbiorów danych porównamy metryki z MusPy z naszymi.
   Sprawdzimy, czy są od siebie zależne, tzn. czy kierunek zmiany obu metryk jest skorelowany.
3. (opcjonalnie) Zbadamy, jak mają się wartości metryk na wybranych utworach do naszych odczuć.
   Zrobimy to w sposób porównawczy, prezentując badanej osobie dwa utwory o różnych wartościach metryk.
   Potencjalnie wykorzystamy do oceny skalę Likerta z ogólnymi stwierdzeniami postaci "Utwór nr 1 brzmi lepiej niż utwór nr 2".

## Planowany stack technologiczny

Język programowania: Python  
Język opisu: Markdown

Docelowy format: biblioteka.

Narzędzia:

- środowisko wirtualne - venv,
- linter, autoformatowanie - ruff,
- przetwarzanie - numpy, MusPy,
- testowanie - pytest,
- dokumentacja - Sphinx,
- interfejs konsolowy - argparse,
- rejestrowanie zdarzeń - logging,
- wizualizacja - matplotlib.

## Harmonogram i planowany postęp

- 23.10 - 27.10 - etap 1: zgłoszenie propozycji rozwiązania, wstępna ogólna konfiguracja środowiska,
- 30.10 - 03.11  
  06.11 - 10.11  
  13.11 - 17.11
  20.11 - 24.11 - etap 2: postęp analizy literaturowej, konfiguracja środowiska eksperymentalnego,  
- 27.11 - 01.12  
  04.12 - 08.12  
  11.12 - 15.12 - implementacja metryk, wypróbowanie metryk dla zestawów danych,
- 18.12 - 22.12  
  03.01 - 05.01 - analiza wyników metryk oraz ich porównanie wraz z wynikami innych metryk,
- 08.01 - 12.01  
  15.01 - 19.01 - sprawdzenie potencjalnych współzależności między metrykami naszymi a już istniejącymi,
- 22.01 - 26.01 - etap finałowy

## Bibliografia

[^back1999]: ["Standard MIDI-File Format Spec. 1.1, updated", David Back, 1999](https://www.music.mcgill.ca/~ich/classes/mumt306/StandardMIDIfileformat.html)
[^dai2022]: ["What is missing in deep music generation? A study of repetition and structure in popular music", Shuqi Dai & Huiran Yu & Roger B. Dannenberg, 2022](https://arxiv.org/abs/2209.00182)  
[^chi2020]: ["Generating Music with a Self-Correcting Non-Chronological Autoregressive Model", Wayne Chi et al., 2020](https://arxiv.org/abs/2008.08927)  
[^dong2020]: ["MusPy: A toolkit for symbolic music generation", Hao-Wen Dong et al., 2020](https://arxiv.org/abs/2008.01951)  
[^yang2020]: ["On the evaluation of generative models in music", Li-Chia Yang & Alexander Lerch, 2020](https://www.researchgate.net/publication/328728367_On_the_evaluation_of_generative_models_in_music)  
[^ji2020]: ["A Comprehensive Survey on Deep Music Generation: Multi-level Representations, Algorithms, Evaluations, and Future Directions", Shulei Ji & Jing Luo & Xinyu Yang, 2020](https://arxiv.org/abs/2011.06801)  
[^xiong2023]: ["A Comprehensive Survey for Evaluation Methodologies of AI-Generated Music", Zeyu Xiong et al., 2023](https://arxiv.org/abs/2308.13736)  
[^dong2017]: ["MuseGAN: Multi-track Sequential Generative Adversarial Networks for Symbolic Music Generation and Accompaniment", Hao-Wen Dong et al., 2017](https://arxiv.org/abs/1709.06298)  
[^huang2018]: ["Music Transformer: Generating music with long-term structure", Cheng-Zhi Anna Huang et al., 2018](https://arxiv.org/abs/1809.04281)  
[^raffel2016dataset]: ["The Lakh MIDI Dataset", Collin Raffel, accessed 14.11.2023](https://colinraffel.com/projects/lmd/)
[^raffel2016]: ["Learning-Based Methods for Comparing Sequences, with Applications to Audio-to-MIDI Alignment and Matching", Collin Raffel, 2016](https://academiccommons.columbia.edu/doi/10.7916/D8N58MHV)
[^dong2017dataset]: ["Lakh Pianoroll Dataset", Hao-Wen Dong et al., accessed 17.11.2023](https://salu133445.github.io/lakh-pianoroll-dataset/)
[^hawthorne2019]: ["Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset", Curtis Hawthorne et al., 2019](https://openreview.net/forum?id=r1lYRjC9F7)
[^bittner2022]: ["A Lightweight Instrument-Agnostic Model for Polyphonic Note Transcription and Multipitch Estimation", Rachel M. Bittner et al., 2022](https://arxiv.org/abs/2203.09893)
[^donahue2018]: ["The NES Music Database: A multi-instrumental dataset with expressive performance attributes", Donahue et al., 2018](https://arxiv.org/abs/1806.04278)
[^thickstun2017]: ["Learning Features of Music from Scratch", John Thickstun et al., 2017](https://arxiv.org/abs/1611.09827)
[^gardner2022]: ["MT3: Multi-Task Multitrack Music Transcription", Josh Gardner et al., 2022](https://arxiv.org/abs/2111.03017v4)
[^hung2021]: ["EMOPIA: A Multi-Modal Pop Piano Dataset For Emotion Recognition and Emotion-based Music Generation", Hsiao-Tzu Hung et al., 2021](https://arxiv.org/abs/2108.01374)
[^bertin-mahieux2011]: ["The Million Song Dataset", Thierry Bertin-Mahieux, 2011](https://academiccommons.columbia.edu/doi/10.7916/D8NZ8J07)
[^manilow2019]: ["Cutting Music Source Separation Some Slakh: A Dataset to Study the Impact of Training Data Quality and Quantity", Ethan Manilow et al., 2019](https://arxiv.org/abs/1909.08494)
[^manilow2020]: ["Simultaneous Separation and Transcription of Mixtures with Multiple Polyphonic and Percussive Instruments", Ethan Manilow et al., 2020](https://arxiv.org/abs/1910.12621)
[^xi2018]: [Guitarset: A Dataset for Guitar Transcription, Qingyang Xi et al., 2018](https://archives.ismir.net/ismir2018/paper/000188.pdf)
[^li2018]: ["Creating a multi-track classical music performance dataset for multi-modal music analysis: Challenges, insights, and applications", Bochen Li et al., 2018](https://labsites.rochester.edu/air/publications/li2018creating.pdf)
[^kong2020]: ["High-resolution Piano Transcription with Pedals by Regressing Onset and Offset Times", Qiuqiang Kong et al., 2020](https://arxiv.org/abs/2010.01815)
