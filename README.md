**SWARM INTELLIGENCE**

**Algorytmy rojowe**

**Marta Maślankowska **

**Daniel Popek **

**1. Benchmarki **

Korzystano z benchmarków, jakimi są Ackley i Rastrigin. W ostatecznym
porównaniu zostały przedstawione również wyniki dla Schwefela, ale
jedynie jako dodatek.

**Ackley**![](.//media/image30.png)

![](.//media/image45.png)

**Rastrigin**

![](.//media/image33.png)![](.//media/image58.png)

**Schwefel**![](.//media/image15.png)![](.//media/image21.png)

Schwefel tym różni się od dwóch pierwszych funkcji, że minimum nie
posiada w środku układu współrzędnych, ale na skraju swojej dziedziny.

Funkcje wymienione są w kolejności od “najłatwiejszej” do
“najtrudniejszej” - tzn, że Ackley jest dość łatwym benchmarkiem dla
algorytmów i minimum znajdowane jest dość szybko.

**2. Opis działania algorytmu PSO **

## 1\. Idea algorytmu:

Jest wiele osobników, którzy posiadają swoje położenie w przestrzeni
N-wymiarowej i prędkość w tej przestrzeni ( w każdym wymiarze). Osobnik
zna swoje najlepsze położenie względem funkcji kosztu ( minimalizujące
jej wartość) oraz najlepsze globalne położenie stada.

W każdej iteracji położenie cząsteczek generowane jest w oparciu o nowo
wyliczaną prędkość. Prędkość zależy od:

  - > prędkości w chwili poprzedniej ważonej współczynnikiem inercji
    > (współczynnik W à wpływa on na eksplorację)

<!-- end list -->

  - > położenia względem własnego optimum(p): zmierzamy tam zgodnie ze
    > współczynnikiem cp Î\[0,2\] i dodatkowo współczynnikiem rpÎ\[0,1\]
    > wprowadzającym element losowości

<!-- end list -->

  - > położenia względem dotychczasowego najlepszego optimum stada (g, z
    > analogicznymi współczynnikami cg i rg)

Dodatkowo współczynnik inercji może zmniejszać się wraz z numerem
iteracji – balansuje to wówczas eksplorację i eksploatację (zmniejsza
eksplorację pod koniec działania algorytmu)

## 2\. Wzory

> a) Aktualizacja pozycji :

*x(t+1)=x(t)+v(t+1)*

> b) Aktualizacja prędkości:

*vi(t+1)=w\*v(t) +cp\*rp\*(pi(t)-xi(t)) + cg\*rg\*(g(t)-xi(t))*

## 3\. Parametry:

> **-w**-współczynnik inercji: stały lub zmienny w zależności od
> iteracji - wpływa na eksplorację
> 
> **-cp**-współczynnik zbieżności do lokalnego optimum – wpływa na
> eksploatację
> 
> **-cg**-współczynnik globalnego optimum – wpływa na eksplorację i
> eksploatację globalnego minimum

## 4\. Pseudokod algorytmu

> a) Każdą cząstkę zainicjować- nadać pozycję z dziedziny xi(0)~Uniform
> 
> b) Pozycję pi(0) ustalić jako wartość początkową xi(0)
> 
> c) Znaleźć globalne minimum g(0)
> 
> d) Nadać prędkość każdej cząstecze z rozkładu
> Uniform~(-(Dmax-Dmin),(Dmax-Dmin))
> 
> e) Do wyczerpania iteracji:
> 
> Dla każdej cząstki i:
> 
> \-wylosuj rp i rg ~Uniform(0,1)
> 
> \-zaktualizuj vi(t+1)
> 
> \-zaktualizuj xi(t+1)
> 
> \-jeżeli pozycja jest lepsza niż lokalne optimum p, zaktualizuj
> optimum lokalne
> 
> \-zaktualizuj optimum globalne

# 3\. Opis działania algorytmy CSO

## 3.1. Idea algorytmu:

Rój kotów działa w dwóch trybach: czuwania i ścigania. Koty w trybie
czuwania obserwują powoli przez większość czasu okolicę i przesuwają się
do obserwowanych pozycji spokojnie, Koty w trybie ścigania ofiarę
(najlepszą dotyczchasową pozycję). Występują w znacznej mniejszoći.

Współczynnik MR (mixture ratio) reguluje liczbę kotów w trybie ścigania.
Powinien przyjmować względnie niską wartość, co odzwierciedla leniwą
naturę kotów.

Intuicyjnie tryb ścigania( tracing mode) odpowiada eksploracji a tryb
czuwania (seeking mode) odpowiada esklpoatacji.

## 3.2.Tryb czuwania (seeking mode) - parametry

\-SMP (seeking memory pool) – liczba punktów obserwowanych w przestrzeni
przez koty

\-CDC (counts of dimentions to change) – liczba wymiarów aktualnej
pozycji, które ulegając „mutacji” tworzą nowe punkty do obeserwowania

\-SRD (seeking range of selected dimention) – procent mutacji wartości
danego wymiaru; nowa wartość jest losowana z rozkładu Uniform~(old –
SRD\*old, old+SRD\*old)

\-SPC (self-position considering) – parametr boolowski wskazujący na to,
czy stara pozycja kota, będzie uwzględnona w puli pozycji kandydujących

## 3.3. Algorytm zmiany pozycji w trybie czuwania (seeking mode)

> a) Utwórz SMP (lub SMP-1 w przypadku SPC=True) kopii aktualnej pozycji
> 
> b) Zmień CDC wymiarów w każdej z pozycji kandudujących losując wartość
> zgodnie z SRD
> 
> c) Policz wartość funkcji dopasowania (straty) dla każdego kandydata
> 
> d) Oblicz prawdopodobieństwo wyboru każdego kandydata :

\- jeżeli wartość funkcji jest taka sama – wszystkie prawdopodobieństwa
ustaw na 1

\- jeżeli wartości funkcji różnią się – oblicz prawdopodobieństwo wg
wzoru

Pi=|Fi-Fmax|/Fmax-Fmin

> e) Znormalizuj prawdopodobieństwa, i wybierz pozycję losując z
> rozkładu Categorical zgodnie z zadanymi wartościami prawdopodobieństw

## 3.4.Algorytm dla trybu ścigania

a) zaktualizuj prędkość kotów :

vi(t+1)=vi+r\*C\*\[x\_best(t)-x(t)\]

b) zaktualizuj pozycję kota:

x(t+1)=x(t)+v(t+1)

## 3.5. Pętla algorytmu

a) Utwórz N kotów

b) Rozlokuj koty równomiernie po dziedzinie przestrzeni poszukiwań

c) Ustaw MR\*N kotów w tryb ścigania

d) Oceń pozycję kotów i zapamiętaj globalne optimum

e) Przemieść każdego kota zgodnie z tym w jakim jest trybie

f) Punkty c…e powtarzaj aż do wyczerpania iteracji

# 4\. Opis działania algorytmu pszczelego 

## 4.1. Idea algorytmu

Algorytm został zainspirowany pszczołami. Można je podzielić na trzy
grupy, mające różne zadanie. Przede wszystkim wyróżniamy pszczoły
*employee*, które szukają punktów z jedzeniem (minimum lokalnych
funkcji). Następnie dają one znać pszczołom *onlookers*, które
proporcjonalnie do ilości jedzenia znalezionego przez pierwszą grupę
pszczół, dolatują w pewne ich otoczenie, zwiedzając obiecujące okolice.

Pszczoły przelatują między swoimi pozycjami tak, aby *employes*
znajdowały się zawsze w lokalnym minimum, a *onlookers* eksplorowały
najbliższą okolicę.

Gdy jednak pewien *employer* nie odnajdzie dobrego siedliska jedzenia i
przez długi czas nie poprawi swojej pozycji, losowo wysyłany jest on w
inne miejsce w celach eksploracyjnych – takie pszczoły nazywamy
*scout*-ami.

## 4.2. Parametry

  - **liczba pszczół**  
    zakres - liczby naturalne  
    Choć istnieją 3 rodzaje pszczół, w samym algorytmie wyróżniamy tylko
    dwie – *employes*, które zamieniają się czasem w *scout* oraz
    *onlookers*. Musimy zatem testować liczność obu rodzajów pszczół i
    ich stosunku względem siebie.

  - **limit**  
    zakres - liczba iteracji  
    Parametr określający po jakim czasie bezczynności (niezmienienia
    pozycji pszczoły), pszczoła powinna stać się *scout*-em.

  - **sąsiedztwo = neighbourhood**  
    zakres - od 0 do 1  
    Pewna procentowa wartość wskazująca na promień okolicy pszczoły
    *employer*, do którego dolatują pszczoły *onlooker*.

Z powodu nieścisłego zdefiniowania przez autorów algorytmu ABC
szczegółów dotyczących funkcji dotyczącej określania sąsiedztwa
pszczoły *employer*, zaimplementowaliśmy kilka różnych rozwiązań, z
których każde opiera się na wybranej (okolicznej) pozycji pszczoły
*employer* i w większości również na pozycji losowo wybranej innej
pszczoły *employer*; a także na wartości parametru neighbourhood.
Pozycja pszczoły *onlooker* wyliczana jest na podstawie:

1\. różnicy pozycji pomiędzy dwoma wybranymi pszczołami *employee*
(oczywiście w okolicy tej dedykowanej) o wartości równej parametrowi
neighbourhood  
\[*simply*\]

2\. różnicy pozycji pomiędzy dwoma wybranymi pszczołami *employee* o
wartości wylosowanej z rozkładu jednostajnego z zakresu (-neighbourhood,
neighbourhood) \[*randomly by neighbour*\]

3\. podobnie do rozwiązania 2., ale ze znormalizowaną różnicą między
pozycjami pszczół \[*uniformly by neighbour*\]

4\. podobnie do rozwiązania 2., ale bez sugerowania się pozycją drugiej
pszczoły (w odniesieniu tylko do wybranego *employee*)  
\[*uniformly by neighbourhood*\]

5\. podobnie do rozwiązania 1., ale wybierając losową liczbę wymiarów,
względem których będziemy rozlokowywać pszczoły *onlooker  
*\[*choosing random dimensions*\]

## 4.3. Pseudokod

a) Rozlokuj losowo N pszczół *employee*

b) Oceń pozycję pszczół i zapamiętaj najlepszy wynik

c) Proporcjonalnie do jakości pozycji pszczół (z proporcjonalnym
prawdopodobieństwem) rozlokuj pszczoły *onlookers* w sąsiedztwie
*employers*

d) Oceń pozycję pszczół *onlookers*

e) Jeśli jakaś pszczoła *onlooker* znajduje się w lepszej pozycji niż
*employer* z jej otoczenia, zamień ich pozycje

f) Jeśli jakaś pszczoła *employer* nie zmieniła swojej pozycji od
zadanej liczby iteracji (limit), zamień ją w *scout*-a i zmień losowo
pozycję

# 5.Badania wpływu liczby iteracji na wyniki PSO, CSO, ABC

Wszystkie badania zostały wykonane trzykrotnie, a przedstawione wyniki
są ich uśrednieniem.

## 

## 5.1 Wpływ liczby iteracji na skuteczność działania PSO

Przyjęte parametry:

  - 50 ptaków

  - 200 iteracji

  - w=0.5

  - cp=0.7,
> cg=0.7

> ![](.//media/image57.png)![](.//media/image29.png)![](.//media/image5.png)![](.//media/image7.png)

## 5.2. Wpływ liczby iteracji na skuteczność działania CSO

Przyjęte parametry:

  - 50 ptaków

  - 200 iteracji

  - MR=0.1, C=0.5

  - SMP=40, SRD=0.6

  - SPC=True, CRD=2

## ![](.//media/image51.png)![](.//media/image28.png)

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 

## 5.3 Wpływ liczby iteracji na skuteczność działania ABC

Przyjęte parametry:

  - 50 pszczół employers

  - 200 pszczół onlookers

  - limit zależny od liczby iteracji (liczba iteracji do potęgi ⅔)

  - sąsiedztwo = 0.2

  - funkcja sąsiedztwa: *choosing random dimensions*

**Funkcje 2-wymiarowe**

Widać, że dla benchmarku Ackley wyniki są dużo lepsze, bo nawet dla
zaledwie 50 iteracji osiągana jest bardzo dobra skuteczność. ABC z
funkcją Rastrigin radzi sobie również dobrze, aczkolwiek potrzebuje już
więcej czasu, aby sensownie zbiec do
minimum.![](.//media/image9.png)![](.//media/image42.png)

**Funkcje wielowymiarowe**

Przetestowaliśmy działanie tego algorytmu nie tylko dla 2-wymiarowych
funkcji, ale również dla więcej. Bowiem im więcej wymiarów, tym
trudniejsze zadanie optymalizacji.

![](.//media/image61.png)![](.//media/image14.png)

# 

# 

# 

# 

# 

# 

# 

Znów ABC na Ackley poradził sobie zdecydowanie lepiej. Potwierdziła się
także hipoteza, że im więcej wymiarów, tym wolniej zbiega; a na
trudniejszych benchmarkach (takich jak Rastrigin) ostateczny wynik nawet
przy dużej liczbie iteracji może nie być satysfakcjonujący. Warto byłoby
zatem zapewne przebadać więcej parametrów i ustalić te optymalne.

# 6.Wyniki wpływu liczby osobników na wyniki algorytmów 

## 6.1 Wpływ liczby ptaków na działanie PSO

![](.//media/image4.png)![](.//media/image22.png)

## 6.2 Wpływ liczby kotów na działanie CSO

![](.//media/image6.png)![](.//media/image55.png)

##   

## 6.3 Wpływ liczby pszczół (employers i onlookers) na działanie ABC

W pracy, w której zaproponowano ABC, korzystano zazwyczaj z takiej samej
liczby pszczół obu rodzajów. My przebadaliśmy jednak jaki wpływ ma
zmniejszanie ich liczby oraz jakie znaczenie ma stosunek liczby pszczół
employee do onlooker.

**Stała liczba pszczół *employee* i zmieniająca się liczba pszczół
*onlooker***

  - liczba pszczół employee - 10 (wykres zwykły oraz przybliżony)

Widzimy, że dla funkcji Ackley już przy zaledwie 10 pszczołach employee
skuteczność jest bardzo duża - wykres po prawej jest przybliżeniem
lewego wykresu dla wartości od 0 do 1e-7. Oczywiście im więcej pszczół
onlooker, tym lepsza
skuteczność.![](.//media/image54.png)![](.//media/image63.png)

  - liczba pszczół employee - 10 oraz 100

Dla funkcji Rastrigin tendencje wyglądają podobnie, jednak od razu
widać, że 10 pszczół employee to za mało, nawet przy ogromnej liczbie
pszczół onlooker. Przy 100 pszczołach employee jest już zdecydowanie
lepiej.![](.//media/image44.png)![](.//media/image34.png)

**Stała liczba pszczół *onlooker* i zmieniająca się liczba pszczół
*employee***

  - liczba pszczół onlooker - 10 oraz 100

W tym przypadku tendencje są zupełnie inne, niż poprzednio. Dla małej
liczby pszczół onlooker algorytm radzi sobie najgorzej przy dużej
liczbie empolyed. Im mniejsza liczba pszczół onlooker, tym zdaje się być
lepiej. Przy zwiększaniu employed, jest dużo lepiej  
(i uzyskiwane są znacznie lepsze wynik), jednak zbyt duża liczba
employed wciąż nie jest zbyt
dobra.![](.//media/image41.png)![](.//media/image25.png)

  - liczba pszczół onlooker - 10 oraz
    100![](.//media/image53.png)![](.//media/image56.png)

O dziwo w przypadku funkcji Rastrigin, zależność już nie jest taka
oczywista. Wcale nie najlepsza jest jak najmniejsza liczba pszczół
employee. Dla 10 onlookers, najlepiej przedstawia się gdzieś między 25,
a 100; natomiast dla 100 onlookers, w okolicy 50-200.

**WNIOSEK**

Widzimy zatem, że wcale nie można powiedzieć, że im więcej pszczół, tym
lepiej. Oczywiście - zwiększenie liczby employers, przy zwiększaniu
onlookers daje bardzo dobre wyniki, jednak należy zachować pewną
równowagę przy zależności w drugą stronę. Widać, że im więcej
onlookers, tym lepiej, ale im więcej employers, tym niekoniecznie.
Skłaniać się zatem możemy do ustawiania liczby pszczół np. w stosunku
1:2 czy 1:5, ale nie 3:1 czy 5:1 (employers:onlookers; nie odwrotnie).

# 

# 

# 7.Badania wpływu parametrów specyficznych dla PSO 

# 7.1 Badanie wpływu współczynnika inercji W 

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów W,
CP, CG dla 50 cząstek w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru W.

![](.//media/image8.png)

![](.//media/image19.png)

Dla zakresu wartości 0.1 - 0.7 :

![](.//media/image3.png)

**Wniosek:**

Wraz ze wzrostem wartości parametru rośnie tempo eksploracji
przestrzeni. Do pewnego momentu może być to korzystne – wzrost
przyspiesza odnalezienie globalnego minimum. Jednak zbyt duży
współczynnik inercji uniemożliwia eksploatację – musi być odpowiednio
mały, aby cząstki mogły zbiec.

# 

# 7.2 Badanie wpływu współczynnika CP (związanego z lokalnym optimum)

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów W,
CP, CG dla 50 cząstek w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru CP.

![](.//media/image43.png)

![](.//media/image23.png)

Ogólnie wraz ze wzrostem **cp**, rośnie jakość algorytmu PSO – parametr
wpływa na eksploatację optimów lokalnych, aż w końcu – eksploatację
globalnego optimum.

**7.3. Badanie wpływu współczynnika CG (związanego z globalnym
optimum)**

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów W,
CP, CG dla 50 cząstek w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru CG.

![](.//media/image26.png)

![](.//media/image2.png)

Wzrost parametru **cg** wpływa do pewnego momentu korzystnie na wyniki
algorytmu – odpowiednia ekspoloracja jest potrzeba do zbliżenia się do
minimum globalnego. Zbyt duża wartość parametru może jednak uniemożliwić
eksploatację globalnego optimum.

![](.//media/image31.png)

Globalnie najlepszą parą parametrów dla funkcji Ackleya okazuje się
cg,cp=(0.7,0.7).

**7.4.Najlepsze kombinacje paramterów**

W tabelach podano 10 najlepszych kombinacji trójki parametrów w, cp i cg
dla 50 ptaków w roju i 200 iteracji.

| **W** | **CP** | **CG** | **ACKLEY** |
| ----- | ------ | ------ | ---------- |
| 0,1   | 0,2    | 1,5    | 4,44E-16   |
| 0,1   | 0,2    | 2      | 4,44E-16   |
| 0,1   | 0,2    | 2,5    | 4,44E-16   |
| 0,1   | 0,2    | 3      | 4,44E-16   |
| 0,1   | 0,7    | 1,5    | 4,44E-16   |
| 0,1   | 0,7    | 2      | 4,44E-16   |
| 0,1   | 0,7    | 2,5    | 4,44E-16   |
| 0,1   | 0,7    | 3      | 4,44E-16   |
| 0,1   | 1,5    | 1,5    | 4,44E-16   |
| 0,1   | 1,5    | 2      | 4,44E-16   |

| **W** | **CP** | **CG** | **RASTRIGIN** |
| ----- | ------ | ------ | ------------- |
| 0,1   | 0,2    | 1,5    | 0             |
| 0,1   | 0,2    | 2,5    | 0             |
| 0,1   | 0,7    | 2      | 0             |
| 0,1   | 0,7    | 2,5    | 0             |
| 0,1   | 1,5    | 1,5    | 0             |
| 0,1   | 1,5    | 2,5    | 0             |
| 0,1   | 1,5    | 3      | 0             |
| 0,1   | 2      | 1,5    | 0             |
| 0,1   | 2      | 2      | 0             |
| 0,1   | 2,5    | 1,5    | 0             |

# 8.Badania wpływu parametrów specyficznych dla CSO 

# 

#  8.1 Badanie wpływu współczynnika mieszania MR 

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów
MR, C, SMP,SRD dla 50 kotów w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla
MR.

# ![](.//media/image1.png)

#  

# 

# W przypadku funkcji Ackley najlepszą wartością współczynnika zmieszania jest 0.1, co intuicyjnie odpowiada idei algorytmu CSO, w którym liczba eksplorujących kotów w trybie ścigania powinna być mniejsza.

#  ![](.//media/image52.png)

# W przpadku funkcji Rastrigin najlepszą globalnie wartością parametru Mixtrue Rate okazuje się 0.6. Może mieć to związek z większym stopniem skomplikowania benchmarku – potrzebna jest większa eksploracja przestrzeni.

#  8.2. Badanie wpływu parametru SMP (liczby kandydatów w trybie czuwania)

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów
MR, C, SMP,SRD dla 50 kotów w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru
SMP.

#  ![](.//media/image48.png)

![](.//media/image37.png)

# Wniosek: 

# Wzrost wartości parametru SMP wpływa korzystnie na osiągane wyniki. Kolekcja potencjalnych kolejnych pozycji kotów w trybie czuwania wzrasta, przez co szansa na znalezienie lepszej pozycji staje się większa.

#  

# 8.3. Badanie wpływu parametru C (współczynnika zbiegania do optimum globalnego w trybie ścigania)

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów
MR, C, SMP,SRD dla 50 kotów w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru
C.

#  ![](.//media/image27.png)

#  

#  ![](.//media/image32.png)

#  

# Wniosek:

# Wzorst wartości parametru C wpływa korzystnie na osiągane wyniki – im parametr jest większy tym algorytm zbiega szybciej w kierunku globalnego optimum. 

# 8.4. Badanie wpływu parametru SRD (współczynnika mutacji w trybie czuwania)

Badania przeprowadzono dla wszystkich możliwych kombinacji parametrów
MR, C, SMP,SRD dla 50 kotów w roju i przy 200 iteracjach, a następnie
uśredniono wyniki dla parametru
SRD.

#  ![](.//media/image18.png)

#  ![](.//media/image12.png)

#  

#  

# Wniosek:

# 

# Można stąd wnioskować, że zbyt duża wartość parametru SRD odpowiadająca za stopień mutacji danej cechy jest niekorzystna, co jest zrozumiałe: im większa jest wartość SRD tym eksploatacja jest mniej dokładna. 

# 8.5. Najelpsze kombinacje paramterów

W tabelach przedstawiono 10 najlepszych kombinacji parametrów dla badań
prowadzonych dla 200 iteracji i 50 kotów.

| **MR** | **C** | **SMP** | **SRD** | **Ackley**  |
| ------ | ----- | ------- | ------- | ----------- |
| 0,1    | 0,5   | 40      | 0,6     | 2,15162E-08 |
| 0,1    | 1,5   | 40      | 0,6     | 3,82932E-08 |
| 0,1    | 2     | 10      | 0,6     | 1,49424E-07 |
| 0,1    | 3     | 5       | 0,6     | 1,55133E-07 |
| 0,1    | 1     | 5       | 0,6     | 1,05661E-06 |
| 0,1    | 3     | 20      | 0,6     | 2,43801E-06 |
| 0,1    | 2     | 40      | 0,5     | 2,46761E-06 |
| 0,1    | 1     | 40      | 0,6     | 2,68405E-06 |
| 0,1    | 1     | 10      | 0,6     | 2,7937E-06  |
| 0,1    | 0,5   | 10      | 0,5     | 3,29837E-06 |

| **MR** | **C** | **SMP** | **SRD** | **Rastrigin** |
| ------ | ----- | ------- | ------- | ------------- |
| 0,1    | 1,5   | 5       | 0,5     | 5,45E-11      |
| 0,1    | 2     | 5       | 0,4     | 9,68E-10      |
| 0,1    | 1,5   | 40      | 0,5     | 1,27E-09      |
| 0,1    | 2     | 20      | 0,5     | 1,55E-08      |
| 0,1    | 1     | 10      | 0,5     | 1,91E-08      |
| 0,1    | 2     | 5       | 0,5     | 4,00E-08      |
| 0,1    | 1,5   | 10      | 0,4     | 6,22E-08      |
| 0,1    | 1     | 5       | 0,5     | 9,74E-08      |
| 0,1    | 0,5   | 10      | 0,5     | 9,88E-08      |
| 0,1    | 1     | 5       | 0,4     | 2,81E-07      |

# Wniosek:

Parametry są od siebie zależne. Badania prowadzone dla każdego z
parametru z osobna nie mają przełożenia na parametry, dla których osiąga
się rzeczywiste najlepsze wartości.

# 9\. Badania wpływu parametrów specyficznych dla ABC

## 9.1 Badanie wpływu wielkości sąsiedztwa (neighbourhood)

Ustalone stałe parametry:

  - limit - 100

  - funkcja sąsiedztwa - choosing random dimensions

  - liczba pszczół - 50 employee, 200 onlookers![](.//media/image62.png)

Widać, że najlepsze wyniki osiągane są dla dużej eksploracji, czyli
sąsiedztwa równego 0.5.![](.//media/image24.png)

## 9.2 Badanie wpływu wielkości parametru limit (liczby iteracji)

Ustalone stałe parametry:

  - neighbourhood (sąsiedztwo) - 0.5

  - funkcja sąsiedztwa - choosing random dimensions

  - liczba pszczół - 50 employee, 200
    onlookers![](.//media/image36.png)![](.//media/image35.png)

Dla funkcji Rastrigin po około 50 iteracji niezależnie od wartości limit
osiągana była dokładność większa niż 1e-15, przez co wszystkie wyniki
zostały zapisane jako 0.

Dla funkcji Ackley natomiast widać, że najszybciej zbiegła przy wartości
limit 50 lub 100.

## 9.3 Badanie wpływu rodzaju funkcji sąsiedztwa

Ustalone stałe parametry:

  - neighbourhood (sąsiedztwo) - 0.25

  - limit - zależny od liczby iteracji

  - liczba pszczół - 50 employee, 200 onlookers

Dla Ackley wyraźnie widać, że jedna funkcja sąsiedztwa zostaje w tyle,
natomiast pozostałe radzą sobie bardzo dobrze - najszybciej jednak
zbiega ta najprostsza.![](.//media/image20.png)![](.//media/image13.png)

Widać, że Rastrigin jest bardziej uniezależniony od rodzaju funkcji (co
widać, że wartości osiągniętych dla tego benchmarku), ale też nie osiąga
aż tak dobrych wyników - jedynie dla najprostszej funkcji udaje mu się
osiągnąć dobrą skuteczność; pozostałe zostają w
tyle.![](.//media/image60.png)![](.//media/image17.png)

# 10\. Porównanie wyników dla PSO, CSO oraz ABC

Wszystkie badania zostały przeprowadzone zarówno dla zaledwie 100
iteracji w 2 wymiarach oraz dla 1000 iteracji w 10 wymiarach.

We wszystkich przypadkach też liczba osobników wynosiła
250.

## 10.1 Wyniki PSO

![](.//media/image46.png)![](.//media/image11.png)![](.//media/image47.png)

Dla wszystkich funkcji PSO działa bardzo dobrze - nawet dla tak trudnej,
jak Schwefel. Dodatkową zaletą jest szybkie działanie, w porównaniu do
pozostałych algorytmów.

Widać, że we wszystkich przypadkach dla funkcji 2-wymiarowej PSO udaje
się zbiec bardzo blisko optimum już przy 10 iteracji algorytmu.

## 10.2 Wyniki CSO

![](.//media/image40.png)![](.//media/image39.png)

Widać już inną tendencję, niż w PSO, bo średnia grupy nie zbiega już tak
samo, jak lider.

## 10.3 Wyniki ABC![](.//media/image16.png)![](.//media/image59.png)

Dla benchmarku Ackley widać, że ABC zbiega bardzo szybko, nawet dla
wielu wymiarów.

Dla Rastrigin również uzyskane wyniki są bardzo dobre. Przy 2 wymiarach
bardzo szybko udaje się dojść do wartości funkcji mniejszej niż 1e-15
(co objawia się jako 0), a dla 10 wymiarów szybkość zbiegania do 0 jest
niewiele gorsza od dużo prostszej funkcji
Ackley.![](.//media/image38.png)![](.//media/image49.png)![](.//media/image50.png)![](.//media/image10.png)

Dla najtrudniejszej funkcji Schwefel dopiero dla większej liczby
wymiarów ABC osiąga nieco gorszy wynik, bo zaledwie 0.2. Dla 2 wymiarów
radzi sobie natomiast tak samo dobrze.

# 10.4 Porównanie algorytmów

Porównanie najlepszych wyników algorytmów dla 100 iteracji i zbliżonej
liczby
osobników:

|         | **l. osobników** | **Ackley** | **Rastrigin** | **Schwefel** |
| ------- | ---------------- | ---------- | ------------- | ------------ |
| **PSO** | 250              | 4.44e-16   | \> 1e-15      | 2,27e-13     |
| **CSO** | 250              | 6.82e-06   | 5.15e-07      | 1,030        |
| **ABC** | 250 (w sumie)    | 2,2e-14    | \> 1e-15      | 5,7e-13      |
