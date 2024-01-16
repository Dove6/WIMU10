# Eksperyment - miary bazujące na akordach

W ramach projektu zostały zaproponowane dwie miary wysokościowe/harmoniczne bazujące na akordach.
Ostatecznie te miary przyjęły postać dwóch statysyk:
- histogramu akordów
- macierzy przejść akordów


## Opis opracowanych metryk

Poniżej opisano oraz przedstawiono działanie zaimplementowanych metryk.
Prezentacja metryk została dokonana dla uwtoru o tytule "L.v.Beethoven 3mov - Piano Sonata No.4 in Eb Major Op.7" (jest to utwór o numerze indeksu 151 w zbiorze danych MusicNet).
Powtórzenie wyników poniższej prezentacji jest możliwe za pomocą polecenia `python -m notebooks.chords_showcase`.

### Histogram akordów

Funkcja:
<details><summary>chords_histogram</summary>
Argumenty:
- `track` - badana ścieżka (obiekt typu `muspy.Track`),
- `readable_output` - w jakim formacie zwrócić akordy (obecnie obsługiwana jest format liczbowy MIDI oraz notacja klawiszowa na pianinie [wartości: 'midi', 'piano']),
- `error_frame` - odstęp jaki może nastąpić pomiędzy poszczególnymi pojedyńczymi nutami by nadal zostały zidentyfikowane jako jeden akord (podawany w impulsach zegarowych). Ze względu na to, że nuty jednego akordu mogą zostać zanotowane z lekkimi opóźnieniami (ze względu na styl grania danej osoby, sposób w jaki został przekonwertowany utwór do MIDI,błąd ludzki lub sprzętowy), wartość ta została wprowadzona by zaniechać identyfikacji kilku mniejszych akordów, gdzie znajduje się jeden pojedynczy akord.
</details>

Histogram akordów pozwala na łatwiejszą analizę typu oraz częstości występowania poszczególnych akordów w utworze. Korzystanie z metryki umożliwia sprawniejszą identyfikację utworów z nienaturalnym, odstępującym od normy rozkładem.

![a](../images/chords/experiment-chord_histogram.png)
&nbsp;*<span id="rys-1">Rys. 1</span>. Przykład histogramu akordów wyliczonego dla utworu nr 151 ze zbioru MusicNet*


### Macierz przejść akordów
Funkcja:
<details><summary>chords_transition_matrix</summary>
Argumenty:
- `track` - badana ścieżka (obiekt typu `muspy.Track`),
- `readable_output` - w jakim formacie zwrócić akordy (obecnie obsługiwana jest format liczbowy MIDI oraz notacja klawiszowa na pianinie [wartości: 'midi', 'piano']),
- `error_frame` - odstęp jaki może nastąpić pomiędzy poszczególnymi pojedyńczymi nutami by nadal zostały zidentyfikowane jako jeden akord (podawany w impulsach zegarowych). Ze względu na to, że nuty jednego akordu mogą zostać zanotowane z lekkimi opóźnieniami (ze względu na styl grania danej osoby, sposób w jaki został przekonwertowany utwór do MIDI,błąd ludzki lub sprzętowy), wartość ta została wprowadzona by zaniechać identyfikacji kilku mniejszych akordów, gdzie znajduje się jeden pojedynczy akord.
</details>


Macierz przejść akordów przedstawia graficznie prawdopodbieństwa przejścia z jednego akordu do nastepnego (prawdopodobieństwo podane od w skali 0. do 1.). Kolorowe punkty na mapie reprezentują przejście z  akordu na skali 'Y' do znajdującego się odpowiednieka na skali 'X'. Akordy rozpoznane najwcześniej znajdują się na początku układu współrzędnych, natomiast najpóźniej rozpoznane są na ich krańcach.
![a](../images/chords/experiment-chord_transition.png)
&nbsp;*<span id="rys-2">Rys. 2</span>. Przykład macierzy przejść akordów wyliczonej dla utworu nr 151 ze zbioru MusicNet*



## Wyniki metryk dla wygenerowanych danych

Do testów zostały wygenerowane trzy zbiory danych z wykorzystaniem różnych narzędzi, m.in.:
- GiantMusicTransformer (przykłady zostały wygenerowane dla różnych wartości temperatury: 0.9, 0.15, 1.0),
- MidiRandomizer (narzędzie do generowania losowych plików MIDI),
- TensorFlow-RNN (przykłady zostały wygenerowane dla różnych wartości temperatury: 0.25, 2.0, 3.0 oraz 10.0),
Wygenerowane dane znajdują sie w katalogu `.data\generated\` w odpowiednych subfolderach (`gmt` dla GiantMusicTransformer, `mr` dla MidiRandomizer oraz `tf_rnn` dla TensorFlow-RNN)

Wyniki dla każdego z wygenerowanych zestawów można odtworzyć za pomocą odpowiedniego polecenia:
- GiantMusicTransformer -> `python -m notebooks.chords_analysis gtm`
- MidiRandomizer -> `python -m notebooks.chords_analysis md`
- TensorFlow-RNN -> `python -m notebooks.chords_analysis tf_rnn`


W przypadku danych z MidiRandomizer oraz TensorFLow-RNN wszystkie wyniki wyglądały identycznie:

![a](../images/chords/exp_analysis_tf_rnn.png)
&nbsp;*<span id="rys-3">Rys. 3</span>. Macierz przejść i histogram akordów dla pliku 'tf_rnn-000.mid'*


W żadnym z wygenerowanych plików dla obu zbiorów nie zostały wykryte akordy. W obu przypadakach utwory są generowane dźwięk po dźwięku, na wskutek czego nie dochodzi w żadnym momencie do wielobrzmienia.


W przypadku zestawu GiantMusicTransformer pojawiło sie kilka bardziej nadających się do analizy przypadków. W miarę możliwości dla każdego z nich będzie określona jakość utworu oraz jak to jest powiązane z wynikami metryk. 

Utwór `gmt-009.mid` charakteryzuje brakiem struktury i spoistości. Akordy się odgrywane w sposób całkowicie losowy. Jest to w dużej mierze zauważalne również w wynikach metryk. W macierzy przejść jest zauważalna jedna przękątna linia z minimalną ilością 'przejść' dziejących się poza nią. Na histogramie natomiast widać rozkład płaski, gdzie znaczna większość akordów pojawia się tylko raz. Przykładami danych o podobnej charakterystyce dźwięku oraz podobnych wynikach metryk były: `gmt-002.mid`, `gmt-010.mid` oraz `gmt-011.mid`.
![a](../images/chords/exp_analysis_gmt_random.png)
&nbsp;*<span id="rys-4">Rys. 4</span>. Macierz przejść i histogram akordów dla pliku 'gmt-009.mid'*

W przypadku `gmt-000.mid` można klarowanie słyszeć zdominowanie utworu przez jeden akord, gdzie pozostałych praktycznie nie słychać. Wynikowa macierz przejść utraciła przekątną linię 'przejść' w zamian za znacznie większą różnorodność. Na histogramie natomiast widać rozkład jednomodalny, gdzie jeden akord pojawia się o wiele częściej niż pozostałe (prawie o rząd wielkośći). Utworami posiadającymi podobny charakter oraz identyczne wyniki metryk były: `gmt-003.mid` oraz `gmt-001.mid`.
![a](../images/chords/exp_analysis_gmt_outnumbers.png)
&nbsp;*<span id="rys-5">Rys. 5</span>. Macierz przejść i histogram akordów dla pliku 'gmt-000.mid'*

Bardziej ekstremalnym przypadkiem utworów zdominowanych przez jeden akord są `gmt-004.mid`, `gmt-005.mid` oraz `gmt-006.mid`, gdzie grany jest praktycznie tylko jeden akord.  
![a](../images/chords/exp_analysis_gmt_one.png)
&nbsp;*<span id="rys-6">Rys. 6</span>. Macierz przejść i histogram akordów dla pliku 'gmt-004.mid'*


Najlepiej brzmiącym wygenerowanym utworem był `gmt-008.mid`(dla wartości 'temperature: 1.0'). Z wszystkich danych wygenerowanych przy pomocy 'GiantMusicTransformer', ten charakteryzował się największa spoistością. Najbardziej brzmiał jak rzeczywiste utwory. Struktura wyników dla tego utworu jest również bardzo zbliżona do utworów ze zbioru MusicNet. W macierzy przejść duże skupienie 'przejść' jest widoczne na przękatnej, z lekkimi wariacjami odbywającymi się co kilka akordów. W przypadku histogramu można sugerować istnienie rozkładu wielomodalnego. Żaden z akordów pojedyńczo nie dominuje utworu oraz nie istnieje tak duża losowość brzmienia jak w przypadku utworów z rozkładem płaskim. 
![a](../images/chords/exp_analysis_gmt_best.png)
&nbsp;*<span id="rys-7">Rys. 7</span>. Macierz przejść i histogram akordów dla pliku 'gmt-008.mid'*



#### Wnioski

- Obie metryki znacznie lepiej sprawują się w łącznej analizie utworów niż osobno. 
- Pojawienie sie w histogramie rozkładu płaskiego może sugerować dużą losowość i brak spoistości w utworze.
- Znaczne zatracenie na macierzy przejść lini przekątnej lub dla histogramu pojawienie się rozkładu jednomodalnego sugerują zdominowanie utworu przez pojedyńczy akord.
