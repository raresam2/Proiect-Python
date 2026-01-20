Biblioteci necesare:

tkinter(interfata grafica)
sqlite3(baza de date)
date time(gestionarea datelor calendaristice)


Fisiere cod:
app.py

Executati comanda:
python app.py


Metodologie de lucru:
Am vizionat diverse tutorial pe yt,w3schools.Am folosit w3schools si documentatia oficiala Python pentru a intelege sintaxa corecta a limbajului si comenzile sql de baza.Am urmarit tutoriale video pe YouTube specifice pentru biblioteca Tkinter, pentru a intelege cum functioneaza sistemul de ferestre, cum se aranjeaza elementele (pack vs grid) si cum se preiau datele de la utilizator.




Youtube tutorial:
https://www.youtube.com/watch?v=JeznW_7DlB0
https://www.youtube.com/watch?v=ZDa-Z5JzLYM&t=16s
https://www.youtube.com/watch?v=GzMvimgJIDM&list=PLA1FTfKBAEX73xlgzMb4jzjBSCGp0Rpto&index=54
https://www.youtube.com/watch?v=twxE0dEp3qQ
https://www.youtube.com/watch?v=tJpVkTqT9YQ
https://www.youtube.com/watch?v=byHcYRpMgI4
https://www.youtube.com/watch?v=rwjeizJmw84&list=PLhTE7-JU1rhY5HUX-w0D8sU4ehM1_nOnJ&index=4
https://www.youtube.com/watch?v=X5yyKZpZ4vU
https://www.w3schools.com/python/python_class_init.asp
https://www.w3schools.com/python/python_classes.asp
https://www.w3schools.com/python/python_class_methods.asp
https://www.w3schools.com/python/python_class_properties.asp
https://www.w3schools.com/python/python_class_self.asp


Probleme intampinate si solutiile acestora:

1)Trebuia sa calculez veniturile si cheltuielile in luna in curs, nu pentru tot istoricul
SOLUTIE:
Am folosit functia datetime()now().strftime("%Y-%m"), pentru a obtine prefixul lunii curente si am folosit WILDCARD-UL "%" impreuna cu operatorul "LIKE"

2)Daca utilizatorul introducea text in loc de numar in campul 'Suma', aplicatia se bloca (crash) cu o eroare de tip ValueError.
SOLUTIE:
Am implementat blocuri de tip try...except ValueError. Daca conversia float() esueaza, in loc sa se opreasca programul, afisez o fereastra messagebox.showerror care avertizeaza utilizatorul sa introduca o suma valida.

3)Dupa ce adaugam o tranzactie, etichetele cu 'Venituri totale' sau 'Balanta' ramaneau neschimbate pana la repornirea aplicatiei.
SOLUTIE:
Am creat o metoda dedicata actualizeaza_statistici() pe care o apelez manual imediat dupa ce o tranzactie este salvata cu succes in baza de date. Astfel, utilizatorul vede impactul tranzactiei instantaneu.

4)Cand faceam interogarea SQL pentru filtrarea dupa data (SELECT ... WHERE data LIKE ?), primeam o eroare de tip ProgrammingError. Motivul era ca scriam parametrul intre paranteze (luna_curenta + '%'), iar Python interpreta asta ca un simplu string in paranteze, nu ca un tuplu necesar pentru SQL.
SOLUTIE:
Am invatat ca in Python, pentru a crea un tuplu cu un singur element, este obligatoriu sa pun o virgula la final. Am corectat sintaxa in: (luna_curenta + '%', )

5)Acelasi lucru ca in problema NR.4, cand incercam sa salvez suma in baza de date folosind comanda cursor.execute(..., (suma)), primeam o eroare. Problema era ca Python il interpreta  doar ca pe un numar pus intre paranteze, nu ca pe un tuplu
SOLUTIE:
am schimbat sintaxa pt un tuplu cu un singur element, adica : "(suma,)", introducand virgula# Proiect-Python
