# Tokenizacja

...

## Dostępne tokenizatory

...

:::{admonition} Uwaga
:class: danger
:name: tip-bpe
[Byte Pair Encoding][bpe] nie jest dostępne dla niektórych tokenizatorów: [CPWord][cpword], [Octuple][octuple], [MuMIDI][mumidi].
:::

## Metodyka

Tokenizacje przeprowadzono dla każdego tokenizatora w czterech konfiguracjach, [jeżeli to było możliwe](#tip-bpe):

* Domyślna - z [domyślnymi parametrami tokenizatorów](https://miditok.readthedocs.io/en/latest/bases.html#miditok.TokenizerConfig) w [MidiTok][miditok],
* Maksymalna - z dodatkowymi parametrami (poniżej) pozwalającymi na uzyskanie większej liczby typów tokenów,
* Domyślna z [Byte Pair Encoding][bpe]. Parametr [`vocab_size`][vcb_size] dla [BPE][bpe] ustawiono na 500,
* Maksymalna z [Byte Pair Encoding][bpe]. Parametr [`vocab_size`][vcb_size] dla [BPE][bpe] ustawiono na 1500.

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

Dodatkowo, dla każdej konfiguracji tokenizacji podano procentową zmianę sumy liczby tokenów względem domyślnej konfiguracji.
Wartości dodatnie oznaczają przyrost liczby tokenów, a wartości ujemne spadek.

Wszystkie procesy tokenizacji zostały przeprowadzone na tej samej maszynie.

## Odtwarzalność

Środowisko badawcze:

* Wersja języka Python: 3.10.2
* Implementacja interpretera Python: CPython
* Wersja biblioteki [`MidiTok`][miditok]: 2.1.8
* Wersja biblioteki [`MusPy`][muspy]: 0.5.0

:::{admonition} Informacja
:class: tip
Pełną listę zależności można znaleźć w pliku [`requirements.txt`](https://github.com/Dove6/WIMU10/tree/main/requirements.txt) w repozytorium projektu.
:::

Skrypty, które wykorzystano do przeprowadzenia badań, dostępne są w repozytorium projektu pod ścieżką
[`/notebooks/tokenizers/`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/).
Należy uruchomić je w następującej kolejności:

1. [`run_tokenizers.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/run_tokenizers.py)
2. [`run_bpe.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/run_bpe.py)
3. [`get_statistics.py`](https://github.com/Dove6/WIMU10/tree/main/notebooks/tokenizers/get_statistics.py)

## Wyniki tokenizacji

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

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana     |
|-------------------------|--------------------|---------------|-----------------------|-----------|
|[REMI][remi]             |              20:02 |      27505955 |              21556.39 |     +7.4% |
|[REMIPlus][remiplus]     |              20:43 |      34570154 |              27092.60 |     +4.7% |
|[MIDI-Like][midilike]    |              20:58 |      28404955 |              22260.94 |     +2.6% |
|[TSD][tsd]               |              21:00 |      26111058 |              20463.21 |     +3.4% |
|[Structured][structured] |              18:12 |      28158348 |              22067.67 |       +0% |
|[CPWord][cpword]         |              25:33 |      11531100 |               9036.91 |      +<1% |
|[Octuple][octuple]       |              20:13 |       7039587 |               5516.92 |       +0% |
|[MuMIDI][mumidi]         |              21:49 |      76830938 |              60212.33 |    +25.8% |
|[MMM][mmm]               |              20:18 |      25870241 |              20274.48 |      +<1% |

### Domyślna tokenizacja, [Byte Pair Encoding][bpe]

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana     |
|-------------------------|--------------------|---------------|-----------------------|-----------|
|[REMI][remi]             |              02:50 |      17941505 |              14060.74 |    -30.0% |
|[REMIPlus][remiplus]     |              06:52 |      19156670 |              15013.06 |    -42.0% |
|[MIDI-Like][midilike]    |              03:19 |      21322928 |              16710.76 |    -23.0% |
|[TSD][tsd]               |              02:48 |      16411012 |              12861.29 |    -35.0% |
|[Structured][structured] |              04:28 |      16735686 |              13115.74 |    -40.6% |
|[CPWord][cpword]         |                N/A |           N/A |                   N/A |       N/A |
|[Octuple][octuple]       |                N/A |           N/A |                   N/A |       N/A |
|[MuMIDI][mumidi]         |                N/A |           N/A |                   N/A |       N/A |
|[MMM][mmm]               |              03:09 |      16506871 |              12936.42 |    -36.1% |

### Maksymalna tokenizacja, [Byte Pair Encoding][bpe]

|Tokenizator              |Czas trwania [mm:ss]|Sum. l. tokenów|Śr. l. tokenów na utwór|Zmiana     |
|-------------------------|--------------------|---------------|-----------------------|-----------|
|[REMI][remi]             |              04:30 |      16270492 |              12751.17 |    -36.5% |
|[REMIPlus][remiplus]     |              09:43 |      17089939 |              13393.37 |    -48.2% |
|[MIDI-Like][midilike]    |              05:10 |      17884298 |              14015.91 |    -35.4% |
|[TSD][tsd]               |              03:52 |      14450541 |              11324.88 |    -42.8% |
|[Structured][structured] |              04:51 |      13796644 |              10812.42 |    -51.0% |
|[CPWord][cpword]         |                N/A |           N/A |                   N/A |       N/A |
|[Octuple][octuple]       |                N/A |           N/A |                   N/A |       N/A |
|[MuMIDI][mumidi]         |                N/A |           N/A |                   N/A |       N/A |
|[MMM][mmm]               |              03:37 |      13927012 |              10914.59 |    -46.1% |

## Analiza wyników

...

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