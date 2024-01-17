# WIMU10 - Opracowanie nowych metryk do ewaluacji muzyki symbolicznej w formacie MIDI

Zespół w składzie:

- Moroz Bartłomiej,
- Motyka Jakub,
- Sygocki Dawid,
- Walczak Jan.

[*Design proposal*](DESIGN_PROPOSAL.md)
[Dokumentacja online](https://dove6.github.io/WIMU10/)

## Raporty

- [Metryki harmoniczne utworów](https://dove6.github.io/WIMU10/research/chords-metrics.html): miary opisujące właściwości harmoniczne utworu,
- [Metryki dynamiczne utworów](https://dove6.github.io/WIMU10/research/dynamics-metrics.html): miary opisujące właściwości dynamiczne utworu [![Open in Colab](https://camo.githubusercontent.com/f5e0d0538a9c2972b5d413e0ace04cecd8efd828d133133933dfffec282a4e1b/68747470733a2f2f636f6c61622e72657365617263682e676f6f676c652e636f6d2f6173736574732f636f6c61622d62616467652e737667)](https://colab.research.google.com/github/Dove6/WIMU10/blob/main/notebooks/colab_dynamics_metrics.ipynb),
- [Embeddingi CLaMP](https://dove6.github.io/WIMU10/research/embeddings.html): eksperyment poszukujący zależności pomiędzy utworami w embeddingach z modelu [CLaMP](https://github.com/microsoft/muzic/tree/main/clamp),
- [Sampodobieństwo utworów](https://dove6.github.io/WIMU10/research/self_similarity.html): pierwszy, testowy eksperyment z badaniem samopodobieństwa wewnątrz utworów,
- [Tokenizatory MidiTok](https://dove6.github.io/WIMU10/research/tokenization.html): eksperyment porównujący różne tokenizatory w [MidiTok](https://miditok.readthedocs.io/en/latest/) i wpływ Byte Pair Encoding na wynik tokenizacji.

## Użytkowanie

Stworzenie wirtualnego środowiska i zainstalowanie zależności:

```sh
python -m venv .venv
.venv/Scripts/activate  # `Activate.ps1` jeżeli PowerShell, `activate.bat` jeżeli wiersz polecenia
python -m pip install -r requirements.txt
```

Uruchamianie skryptów:

```sh
.venv/Scripts/activate  # `Activate.ps1` jeżeli PowerShell, `activate.bat` jeżeli wiersz polecenia
python -m notebooks.<katalog>.<plik>
```

Pobieranie zbiorów danych MusPy:

```sh
.venv/Scripts/activate  # `Activate.ps1` jeżeli PowerShell, `activate.bat` jeżeli wiersz polecenia
python -m setup_dataset <nazwa>  # Nazwa zbioru danych małymi literami
```

Lokalne budowanie dokumentacji:

```sh
cd docs
make html  # Lub `.\make.bat html`, jeżeli Make nie jest zainstalowany (tylko Windows)
```

## Struktura projektu

- `data/`: Katalog na pobrane lub przetworzone zbiory danych,
- `docs/`: Konfiguracja generatora dokumentacji Sphinx i pliki dokumentacji projektu,
  - `api/`: Dokumentacja API,
  - `research/`: Raporty z eksperymentów,
  - `conf.py`: Plik konfiguracyjny Sphinx,
  - `DESIGN_PROPOSAL.md`: *Design proposal* projektu,
- `images/`: Katalog na rysunki i wykresy dołączane do dokumentacji,
- `notebooks/`: Skrypty do eksperymentów,
  - `chords_*`: Pliki do metryk harmonicznych,
  - `dynamics_*`: Plik do metryk dynamicznych,
  - `clamp/`: Eksperyment o embeddingach CLaMP,
  - `tokenizers/`: Eksperyment o tokenizatorach MidiTok,
  - `self_similarity/`: Eksperyment o samopowtarzalności utworów,
- `tests/`: Katalog na testy modułu i dane testowe,
- `wimu10/`: Moduł zawierający funkcje do obliczania metryk.

## Stopień zrealizowania harmonogramu

- 23.10 - 27.10 - etap 1 ✔️: zgłoszenie propozycji rozwiązania, wstępna ogólna konfiguracja środowiska,
- 30.10 - 03.11  
  06.11 - 10.11  
  13.11 - 17.11
  20.11 - 24.11 - etap 2 ✔️: postęp analizy literaturowej, konfiguracja środowiska eksperymentalnego,  
- 27.11 - 01.12  
  04.12 - 08.12  
  11.12 - 15.12 - ✔️ implementacja metryk, wypróbowanie metryk dla zestawów danych,
- 18.12 - 22.12  
  03.01 - 05.01 - ⏳ analiza wyników metryk oraz ich porównanie wraz z wynikami innych metryk,
- 08.01 - 12.01  
  15.01 - 19.01 - ❌ sprawdzenie potencjalnych współzależności między metrykami naszymi a już istniejącymi,
- 22.01 - 26.01 - ✔️ etap finałowy

## Stopień zrealizowania zakresu (i późniejszych alternatyw)

- Prototyp pierwszego etapu:
  - Badanie powtarzalności/samopodobieństwa utworu: ✔️,
- Oryginalnie proponowane metryki:
  - *wysokościowa/harmoniczna* (przejścia akordów): ✔️,
  - *rytmiczna* (synkopy): ❌,
  - *wysokościowa/harmoniczna* (zmiany tonacji): ❌,
  - *dynamiczna* (zmiany głośności): ✔️,
  - *agogiczna* (zmiany tempa): ❌,
  - *rytmiczna* (zmiany metrum): ❌,
- Później zaproponowane:
  - MIDI, ABC i model CLaMP:
    - Konwersja MIDI -> ABC: ✔️,
    - Otrzymanie/Zbadanie embeddingów: ✔️,
  - Porównanie tokenizatorów MidiTok: ✔️,
    - Ilościowe: ✔️,
    - Jakościowe: ❌,
    - Wydajnościowe: ✔️,
  - Zbadanie wpływu Byte Pair Encoding na tokenizatory: ✔️,
  - Sprawdzenie/Zastosowanie AquaTK: ❌,
  - Porównywanie zbiorów danych:
    - MAESTRO: ✔️,
    - MusicNet: ✔️.
