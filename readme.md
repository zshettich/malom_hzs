# Malom Játék – HZS

## Hallgató adatai
* **Név:** Hettich Zsolt
* **Neptun kód:** ZAJDU4
* **Tantárgy:** Szkript nyelvek Python
* **Monogram:** HZS

## Feladat leírása
A projekt egy klasszikus **Malom (Nine Men's Morris)** társasjáték megvalósítása Python nyelven, grafikus felülettel. A játékot a felhasználó a számítógép ellen játssza.

A program kezeli a játék három fázisát:
1.  **Lerakás:** A játékosok felváltva helyezik le a bábuiakat.
2.  **Mozgatás:** A bábuk szomszédos mezőre léphetnek.
3.  **Repülés (Flying):** Ha valamelyik félnek már csak 3 bábuja maradt, bárhová léphet a táblán.

A játék implementálja a malomképzés szabályait (bábu levétele), figyeli a szabályos lépéseket, és méri a játékidőt. A számítógép ellenfél (AI) képes védekezni és támadni is, valamint felismeri a saját repülési lehetőségét.

## Indítás
A program indítása a `main.py` fájl futtatásával történik:
```bash
python main.py