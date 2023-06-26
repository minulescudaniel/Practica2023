## Proiectul

  Scopul acestui script Python este de a căuta și extrage informații de pe web, utilizând un API de la Google. 
Scriptul va permite utilizatorului să introducă un termen de căutare și va returna rezultatele relevante, extrăgând informații precum titluri, 
descrieri sau URL-uri de pe paginile web găsite în rezultate.


 `Se vor folosi urmatoarele biblioteci: google-api-python-client, pandas, playwright, beautifulsoup4, csv, datetime, tkinter(GUI), schedule, time și requests`

# UPDATE 20/06/2023: 
- Am folosit Google Custom Search API pentru a ma ajuta in a folosi link-urile gasite in functie de un keyword sau string

- Am folosit BeautifulSoup pentru a extrage din documentul HTML informatiile necesare

# UPDATE 21/06/2023:
- Am reorganizat codul (extragerea pretului si a informatiilor pe selectoare CSS)

- Cautare pe elemente

# UPDATE 22/06/2023:
- Afisare mai buna a rezultatelor

- Stocarea preturilor in fisier csv

# UPDATE 23/06/2023:
- Implementarea unui price history

- Implementarea unui plot dedicat cu dropdown menu

- Implementarea unei interfete simple

# UPDATE 26/06/2023
- Implementarea unui time scheduler pentru a rula codul automat la un interval de timp
