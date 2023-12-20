Domyślna konfiguracja tokenizatorów:
Tokenizator|Czas trwania|Sum. l. tokenów|Śr. l. tok. na utw.|
-----------|------------|---------------|-------------------|
REMI       |      18:40 |      25609001 |          20069.75 |
REMIPlus   |      18:47 |      33005326 |          25866.24 |
MIDI-Like  |      18:38 |      27683849 |          21695.81 |
TSD        |      18:30 |      25259075 |          19795.51 |
Structured |      18:22 |      28158348 |          22067.67 |
CPWord     |      21:18 |      11529827 |           9035.91 |
Octuple    |      19:46 |       7039587 |           5516.92 |
MuMIDI     |      18:47 |      61069161 |          47859.84 |
MMM        |      17:44 |      25843073 |          20253.19 |

Konfiguracja z maksymalną liczbą typów tokenów:
Tokenizator|Czas trwania|Sum. l. tokenów|Śr. l. tok. na utw.|Zmiana     |
-----------|------------|---------------|-------------------|-----------|
REMI       |      20:02 |      27505955 |          21556.39 |     +7.4% |
REMIPlus   |      20:43 |      34570154 |          27092.60 |     +4.7% |
MIDI-Like  |      20:58 |      28404955 |          22260.94 |     +2.6% |
TSD        |      21:00 |      26111058 |          20463.21 |     +3.4% |
Structured |      18:12 |      28158348 |          22067.67 |       +0% |
CPWord     |      25:33 |      11531100 |           9036.91 |      +<1% |
Octuple    |      20:13 |       7039587 |           5516.92 |       +0% |
MuMIDI     |      21:49 |      76830938 |          60212.33 |    +25.8% |
MMM        |      20:18 |      25870241 |          20274.48 |      +<1% |

Byte Pair Encoding (domyślna tokenizacja), vocab_size=500
Tokenizator|Czas trwania|Sum. l. tokenów|Śr. l. tok. na utw.|Zmiana     |
-----------|------------|---------------|-------------------|-----------|
REMI       |      02:50 |      17941505 |          14060.74 |    -30.0% |
REMIPlus   |      06:52 |      19156670 |          15013.06 |    -42.0% |
MIDI-Like  |      03:19 |      21322928 |          16710.76 |    -23.0% |
TSD        |      02:48 |      16411012 |          12861.29 |    -35.0% |
Structured |      04:28 |      16735686 |          13115.74 |    -40.6% |
CPWord     |        N/A |           N/A |               N/A |       N/A |
Octuple    |        N/A |           N/A |               N/A |       N/A |
MuMIDI     |        N/A |           N/A |               N/A |       N/A |
MMM        |      03:09 |      16506871 |          12936.42 |    -36.1% |

Byte Pair Encoding ("maksymalna" tokenizacja), vocab_size=1500
Tokenizator|Czas trwania|Sum. l. tokenów|Śr. l. tok. na utw.|Zmiana     |
-----------|------------|---------------|-------------------|-----------|
REMI       |      04:30 |      16270492 |          12751.17 |    -36.5% |
REMIPlus   |      09:43 |      17089939 |          13393.37 |    -48.2% |
MIDI-Like  |      05:10 |      17884298 |          14015.91 |    -35.4% |
TSD        |      03:52 |      14450541 |          11324.88 |    -42.8% |
Structured |      04:51 |      13796644 |          10812.42 |    -51.0% |
CPWord     |        N/A |           N/A |               N/A |       N/A |
Octuple    |        N/A |           N/A |               N/A |       N/A |
MuMIDI     |        N/A |           N/A |               N/A |       N/A |
MMM        |      03:37 |      13927012 |          10914.59 |    -46.1% |