Repositář pro projekt z VVP.

Autor: Ondřej Kučera KUC0436
Projekt: Vizualizace třídících algoritmů

Stručný popis
Tento projekt se zabývá vizualizací vybraných běžných třídících algoritmů, např. bubble sort a quick sort. Každý třídící algoritmus bude implementován ve vlastní třídě dědící z rodičovské třídy. Po zavolání metody třídění vrátí metoda objekt s informacemi o tom, co se má zobrazit v dalším kroku animace. Data ke třídění budou ve formátu seznamu čísel, uložených v listu nebo v souboru. Výstupem bude animace vytvořená knihovnou Matplotlib.Animation.

Specifikace
    • Implementovat abstraktní rodičovskou třídu Sort obsahující několik základních konstruktorů, metod a atributů.
    • Implementovat jednotlivé třídy dědící ze Sort, z nichž každá bude obsahovat vlastní metodu na třídění. Konkrétně se jedná minimálně o tyhle algoritmy:
        1. Bubble sort
        2. Insertion sort
        3. Selection sort
        4. Quick sort
        5. Merge sort
    • Třídící metoda po každém zavolání vrátí informace o tom, co se má zobrazit v dalším kroku animace. To bude zejména list částečně seřazených čísel a dále například indexy prvků, které se porovnávají nebo které už seřazené jsou.
    • Třída Sort bude obsahovat metodu animate, která vrátí objekt animace z knihovny Matplotlib.Animation. Metoda bude mít parametry jako např. rychlost animace.
    • Výstupem bude animace sloupcového grafu, kde data určují výšky sloupců. 
