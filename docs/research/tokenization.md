# Tokenizacja

...

## Cel

* Zbadanie różnic pomiędzy tokenizatorami MIDI udostępnionymi w bibliotece [MidiTok][miditok] poprzez
porównanie długości sekwencji wyjściowych oraz wydajności (potrzebnego czasu pracy),
* Zbadanie wpływu metod tokenizacji na wydajność [Byte Pair Encoding][bpe],
* Porównanie zalet i wad BPE na praktycznym przykładzie.

## Omówienie

### Dostępne tokenizatory

W ramach [MidiTok][miditok] dostępne jest 9 tokenizatorów o wspólnym interfejsie.

* [REMI][remi][^huang2020] (2020) - ...
* [REMIPlus][remiplus][^rutte2022] (2022) - ...
* [MIDI-Like][midilike][^oore2018] (2018) - ...
* [TSD][tsd] - ...
* [Structured][structured][^huang2020] - ...
* [CPWord][cpword][^hsiao2021] (2021) - ...
* [Octuple][octuple][^zeng2021] (2021) - ...
* [MuMIDI][mumidi][^ren2020] (2020) - ...
* [MMM][mmm][^ens2020] (2020) - ...

### [Byte Pair Encoding][bpe]

[MidiTok][miditok] udostępnia gotową implementację
[Byte Pair Encoding][bpe], techniki kompresji sekwencji tokenów (głównie wykorzystywana w NLP)
polegającej na wykrywaniu często występujących par tokenów i zastępowaniu ich nowymi pojedynczymi
tokenami[^sennrich2016].
BPE pozwala na znaczną redukcję długości sekwencji wejściowych, a więc przyspieszenie inferencji
modeli.
W pracy badającej zastosowanie BPE w generowaniu muzyki symbolicznej[^fradet2023], wyniki z
modeli generacyjnych wykorzystujących tokenizatory z BPE okazały się bardziej atrakcyjne dla
ankietowanych słuchaczy w porównaniu z modelami korzystającymi z innych technik, takich jak
*embedding pooling*.

:::{admonition} Uwaga
:class: danger
:name: tip-bpe
[Byte Pair Encoding][bpe] nie jest dostępne dla niektórych tokenizatorów: [CPWord][cpword],
[Octuple][octuple] i [MuMIDI][mumidi], ponieważ wykorzystują *embedding pooling*.
:::

## Metodyka

Tokenizacje przeprowadzono na zbiorze danych [MAESTRO][maestro][^hawthorne2018] dla każdego tokenizatora w czterech
konfiguracjach, jeżeli to było możliwe[{sup}`*`](#tip-bpe):

* Domyślna - z [domyślnymi parametrami tokenizatorów](https://miditok.readthedocs.io/en/latest/bases.html#miditok.TokenizerConfig) w [MidiTok][miditok],
* Maksymalna - z dodatkowymi parametrami (poniżej) pozwalającymi na uzyskanie większej liczby typów tokenów,
* Domyślna + [Byte Pair Encoding][bpe]. Parametr [`vocab_size`][vcb_size] dla BPE ustawiono na 500,
* Maksymalna + [Byte Pair Encoding][bpe]. Parametr [`vocab_size`][vcb_size] dla BPE ustawiono na 1500.

```py
config = miditok.TokenizerConfig(
    use_chords=True,
    use_rests=True,
    use_tempos=True,
    use_time_signatures=True,
    use_sustain_pedals=True,
    use_pitch_bends=True,
)
```

Dla każdej konfiguracji tokenizacji, dla każdego tokenizatora zebrano następujące informacje:

* Czas trwania procesu tokenizacji,
* Suma tokenów we wszystkich utworach,
* Średnia liczba tokenów na utwór.

Dodatkowo, dla każdej konfiguracji tokenizacji podano procentową zmianę sumy liczby tokenów
względem domyślnej konfiguracji.
Wartości dodatnie oznaczają przyrost liczby tokenów, a wartości ujemne spadek.

Wszystkie procesy tokenizacji zostały przeprowadzone na tej samej maszynie.

## Odtwarzalność

Środowisko badawcze:

* Wersja języka Python: 3.10.2
* Implementacja interpretera Python: CPython
* Wersja biblioteki [`MidiTok`][miditok]: 2.1.8
* Wersja biblioteki [`MusPy`][muspy]: 0.5.0
* Wersja zbioru danych [MAESTRO][maestro]: 2.0.0

:::{admonition} Informacja
:class: tip
Pełną listę zależności można znaleźć w pliku [`requirements.txt`](https://github.com/Dove6/WIMU10/tree/main/requirements.txt)
w repozytorium projektu.
:::

Skrypty, które wykorzystano do przeprowadzenia badań, dostępne są w repozytorium projektu pod
ścieżką [`/notebooks/tokenizers/`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/).
Należy uruchomić je w następującej kolejności:

1. [`tokenize.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/tokenize.py)
2. [`bpe.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/bpe.py)
3. [`bpe_var_voc.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/bpe_var_voc.py)
4. [`statistics.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/statistics.py)

## Wyniki

### Domyślna tokenizacja

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|
|-------------------------|--------------------|---------------|-----------------------|
|[REMI][remi]             |              18:40 |      25609001 |              20069.75 |
|[REMIPlus][remiplus]     |              18:47 |      33005326 |              25866.24 |
|[MIDI-Like][midilike]    |              18:38 |      27683849 |              21695.81 |
|[TSD][tsd]               |              18:30 |      25259075 |              19795.51 |
|[Structured][structured] |              18:22 |      28158348 |              22067.67 |
|[CPWord][cpword]         |              21:18 |      11529827 |               9035.91 |
|[Octuple][octuple]       |              19:46 |       7039587 |               5516.92 |
|[MuMIDI][mumidi]         |              18:47 |      61069161 |              47859.84 |
|[MMM][mmm]               |              17:44 |      25843073 |              20253.19 |

### Maksymalna tokenizacja

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana[{sup}`?`](#tip-zmiana) |
|-------------------------|--------------------|---------------|-----------------------|-------|
|[REMI][remi]             |              20:02 |      27505955 |              21556.39 | +7.4% |
|[REMIPlus][remiplus]     |              20:43 |      34570154 |              27092.60 | +4.7% |
|[MIDI-Like][midilike]    |              20:58 |      28404955 |              22260.94 | +2.6% |
|[TSD][tsd]               |              21:00 |      26111058 |              20463.21 | +3.4% |
|[Structured][structured] |              18:12 |      28158348 |              22067.67 |   +0% |
|[CPWord][cpword]         |              25:33 |      11531100 |               9036.91 |  +<1% |
|[Octuple][octuple]       |              20:13 |       7039587 |               5516.92 |   +0% |
|[MuMIDI][mumidi]         |              21:49 |      76830938 |              60212.33 |+25.8% |
|[MMM][mmm]               |              20:18 |      25870241 |              20274.48 |  +<1% |

### Domyślna tokenizacja, [Byte Pair Encoding][bpe]

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana[{sup}`?`](#tip-zmiana) |
|-------------------------|--------------------|---------------|-----------------------|-------|
|[REMI][remi]             |              03:02 |      15897898 |              12459.17 |-37.9% |
|[REMIPlus][remiplus]     |              07:10 |      16936156 |              13272.85 |-48.7% |
|[MIDI-Like][midilike]    |              03:53 |      18532471 |              14523.88 |-33.1% |
|[TSD][tsd]               |              02:58 |      14699582 |              11520.05 |-41.8% |
|[Structured][structured] |              04:16 |      14869314 |              11653.07 |-47.2% |
|[CPWord][cpword]         |                N/A |           N/A |                   N/A |   N/A |
|[Octuple][octuple]       |                N/A |           N/A |                   N/A |   N/A |
|[MuMIDI][mumidi]         |                N/A |           N/A |                   N/A |   N/A |
|[MMM][mmm]               |              03:13 |      14818454 |              11613.21 |-42.7% |

### Maksymalna tokenizacja, [Byte Pair Encoding][bpe]

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana[{sup}`?`](#tip-zmiana) |
|-------------------------|--------------------|---------------|-----------------------|-------|
|[REMI][remi]             |              03:55 |      17436890 |              13665.27 |-31.9% |
|[REMIPlus][remiplus]     |              08:20 |      18545390 |              14534.00 |-43.8% |
|[MIDI-Like][midilike]    |              04:11 |      19668473 |              15414.16 |-29.0% |
|[TSD][tsd]               |              03:14 |      15506756 |              12152.63 |-38.6% |
|[Structured][structured] |              04:15 |      14869314 |              11653.07 |-47.2% |
|[CPWord][cpword]         |                N/A |           N/A |                   N/A |   N/A |
|[Octuple][octuple]       |                N/A |           N/A |                   N/A |   N/A |
|[MuMIDI][mumidi]         |                N/A |           N/A |                   N/A |   N/A |
|[MMM][mmm]               |              03:10 |      14883832 |              11664.45 |-42.4% |

### Domyślna tokenizacja, [Byte Pair Encoding][bpe], różny rozmiar słowozbioru

|Rozmiar słowozbioru|Tokenizator             |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana[{sup}`?`](#tip-zmiana) |
|-------------------|------------------------|--------------------|---------------|-----------------------|-------|
|               500 |[REMI][remi]            |              02:38 |      17941505 |              14060.74 |-29.9% |
|              1000 |[REMI][remi]            |              03:14 |      15897898 |              12459.17 |-37.9% |
|              1500 |[REMI][remi]            |              03:22 |      14850838 |              11638.59 |-42.0% |
|              2000 |[REMI][remi]            |              03:35 |      14153797 |              11092.32 |-44.7% |
|              3000 |[REMI][remi]            |              04:20 |      13149400 |              11220.76 |-48.7% |

### Maksymalna tokenizacja, [Byte Pair Encoding][bpe], różny rozmiar słowozbioru

|Rozmiar słowozbioru|Tokenizator             |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana[{sup}`?`](#tip-zmiana) |
|-------------------|------------------------|--------------------|---------------|-----------------------|-------|
|               500 |[REMI][remi]            |              03:14 |      19780309 |              15501.81 |-22.8% |
|              1000 |[REMI][remi]            |              04:05 |      17436890 |              13665.27 |-31.9% |
|              1500 |[REMI][remi]            |              04:16 |      16270492 |              12751.17 |-36.5% |
|              2000 |[REMI][remi]            |              04:43 |      15473773 |              12126.78 |-39.6% |
|              3000 |[REMI][remi]            |              05:45 |      14317688 |              11220.76 |-44.1% |

:::{admonition} Informacja
:class: tip
:name: tip-zmiana
Kolumna `Zmiana` podaje procentową zmianę sumarycznej liczby tokenów względem domyślnej tokenizacji
bez BPE.
:::

## Analiza wyników

...

## Bibliografia

[^huang2020]: ["Pop Music Transformer: Beat-Based Modeling and Generation of Expressive Pop Piano Compositions", Yu-Siang Huang & Yi-Hsuan Yang, 2020](https://doi.org/10.1145/3394171.3413671)
[^rutte2022]: ["FIGARO: Generating Symbolic Music with Fine-Grained Artistic Control", Dimitri von Rütte et. al., 2022](https://doi.org/10.48550/arXiv.2201.10936)
[^oore2018]: ["This Time with Feeling: Learning Expressive Musical Performance", Sageev Oore et.al., 2018](https://doi.org/10.48550/arXiv.1808.03715)
[^hsiao2021]: ["Compound Word Transformer: Learning to Compose Full-Song Music over Dynamic Directed Hypergraphs", Wen-Yi Hsiao et. al., 2021](https://doi.org/10.1609/aaai.v35i1.16091)
[^zeng2021]: ["MusicBERT: Symbolic Music Understanding with Large-Scale Pre-Training", Mingliang Zeng et. al., 2021](https://doi.org/10.48550/arXiv.2106.05630)
[^ren2020]: ["PopMAG: Pop Music Accompaniment Generation", Yi Ren et. al., 2020](https://doi.org/10.48550/arXiv.2008.07703)
[^ens2020]: ["MMM : Exploring Conditional Multi-Track Music Generation with the Transformer", Jeff Ens & Philippe Pasquier, 2020](https://doi.org/10.48550/arXiv.2008.06048)
[^sennrich2016]: ["Neural Machine Translation of Rare Words with Subword Units", Rico Sennrich, Barry Haddow & Alexandra Birch, 2016](https://doi.org/10.48550/arXiv.1508.07909)
[^fradet2023]: ["Byte Pair Encoding for Symbolic Music", Nathan Fradet et.al., 2023](https://doi.org/10.48550/arXiv.2301.11975)
[^hawthorne2018]: ["Enabling Factorized Piano Music Modeling and Generation with the MAESTRO Dataset", Curtis Hawthorne et.al., 2019](https://openreview.net/forum?id=r1lYRjC9F7)

[maestro]: https://magenta.tensorflow.org/datasets/maestro
[miditok]: https://miditok.readthedocs.io/en/latest/
[muspy]: https://salu133445.github.io/muspy/
[remi]: https://miditok.readthedocs.io/en/latest/tokenizations.html#remi
[remiplus]: https://miditok.readthedocs.io/en/latest/tokenizations.html#remiplus
[midilike]: https://miditok.readthedocs.io/en/latest/tokenizations.html#midi-like
[tsd]: https://miditok.readthedocs.io/en/latest/tokenizations.html#tsd
[structured]: https://miditok.readthedocs.io/en/latest/tokenizations.html#structured
[cpword]: https://miditok.readthedocs.io/en/latest/tokenizations.html#cpword
[octuple]: https://miditok.readthedocs.io/en/latest/tokenizations.html#octuple
[mumidi]: https://miditok.readthedocs.io/en/latest/tokenizations.html#mumidi
[mmm]: https://miditok.readthedocs.io/en/latest/tokenizations.html#mmm
[bpe]: https://miditok.readthedocs.io/en/latest/bpe.html
[vcb_size]: https://miditok.readthedocs.io/en/latest/bpe.html#methods
