# Konwerter MIDI -> ABC

Pobierz [midi2abc](https://github.com/sshlien/abcmidi).
Upewnij się, że nazywa się `midi2abc.exe` i znajduje się w tym katalogu.

# [Model CLaMP](./model/README.md)

# Uruchomienie

Wymagany Python 3.9.X.

## Generowanie zanurzenia dla wszystkich utworów

```
py -3.9 -m notebooks.clamp.create_embeddings
```

Wyniki operacji znajdą się w `data/raw/maestro/maestro-v3.0.0-embeddings`.

## Obliczanie statystyk

```
py -3.9 -m notebooks.clamp.statistics
```

Wyniki zostaną wyświetlone na konsoli.
