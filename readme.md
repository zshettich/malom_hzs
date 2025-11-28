# Malom Játék – HZS

## Hallgató adatai
- **Név:** Hettich Zsolt  
- **Neptun kód:** ZAJDU4  
- **Tantárgy:** Szkript nyelvek – Python  
- **Monogram:** HZS  

---

## Projekt leírása
A projekt egy klasszikus **Malom)** játék Pythonos, grafikus megvalósítása.  
A játékos a számítógép ellen játszik, a grafikai felület és az interakciók a **turtle** modul segítségével valósulnak meg.

A program kezeli a Malom három fázisát:

1. **Lerakás** – a játékosok felváltva helyezik le a 9-9 bábut.  
2. **Mozgatás** – a bábuk szomszédos mezőre léphetnek.  
3. **Repülés** – ha valakinek csak 3 bábuja marad, bárhová léphet.  

A játék tartalmaz:

- malomképzés vizsgálatát,  
- szabályos bábulevételt,  
- győzelmi feltételek ellenőrzését,  
- egyszerű, de taktikus mesterséges intelligenciát (AI),  
- játékidő mérését és eredmények tárolását.  

---

# Modulok és a modulokban használt függvények

## Tanult modulok

### `turtle` – grafikus felület, eseménykezelés
Használt funkciók többek között:

- `turtle.Screen()` – grafikus ablak  
- `screen.onclick()` – egérkattintások kezelése  
- `screen.onkey()` – billentyűk kezelése  
- `turtle.write()` – szöveg kiírása  
- `turtle.dot()` – bábu megjelenítése  
- `turtle.goto()` – koordinátakezelés  
- `turtle.clear()` / `turtle.update()` – kirajzolás frissítése  

### `time`
- `time.time()` – időmérés  
- `time.sleep()` – várakozás animációkhoz  

### `random`
- AI döntésekhez (pl. ha nincs taktikus lépés, véletlenszerű választás)

---

## Bemutatandó modul

### `turtle`
A grafikus játék teljes megvalósítása a `turtle` modulra épül:

- táblanégyzetek kirajzolása  
- összekötő vonalak  
- bábuk (piros / kék) kirajzolása  
- kijelölések és információs szövegek megjelenítése  
- eseményvezérlés egérrel és billentyűzettel  

---

## Saját modulok

### 1. `malomtabla_hzs.py`
A tábla struktúráját és kirajzolását tartalmazza.

**Osztály: `Tablahzs`**

- 24 mező koordinátái (`coords`)  
- szomszédsági lista (`adjacency`)  
- bábu-állapotok (`positions`)  
- mező meghatározása kattintásból:  
  - `get_position_from_click_hzs(x, y)`  

**Függvények:**

- `draw_board_hzs(board)` – tábla és bábuk kirajzolása  
- `draw_square_hzs(size)` – egy négyzet megrajzolása  
- `draw_lines_hzs(outer, middle, inner)` – összekötő vonalak rajzolása  

---

### 2. `idozites_hzs.py`
Időkezelő segédfüggvényeket tartalmaz:

- `start_timer_hzs()` – játékidő indítása  
- `get_elapsed_hzs(start)` – eltelt idő kiszámítása  
- `wait_seconds_hzs(seconds)` – rövid késleltetés (AI animációkhoz, üzenetekhez)  

---

### 3. `jatekos_hzs.py`

**Osztály: `Playerrankhzs`**

A korábbi játékok eredményeit tárolja és rendezi.

**Főbb metódusok:**

- `add_result_hzs(time, winner)` – eredmény rögzítése  
- `get_sorted_results_hzs()` – eredmények rendezése idő alapján  
- `get_results_text_hzs()` – formázott, több soros eredménylista előállítása (játékidő, győztes, helyezés)  

---

# Főprogram – `main.py`

A játék teljes logikáját tartalmazza, többek között:

- játékfázisok váltása (lerakás, mozgatás, repülés)  
- emberi lépések kezelése: `on_click(x, y)`  
- mesterséges intelligencia (AI) lépései:  
  - `computer_turn_hzs()` – AI körének indítása  
  - `get_computer_move_hzs()` – AI döntéslogika  
- malomképzés ellenőrzése:  
  - `check_mill_hzs(board, pos, player)`  
- bábulevétel szabályosan:  
  - `remove_piece_player_hzs(x, y)`  
  - `computer_remove_piece_hzs()`  
- ellenőrzés, hogy van-e levehető bábu:  
  - `has_removable_piece_hzs(opponent)`  
- győztes megállapítása:  
  - `check_winner_hzs()`  
  - `end_game_hzs(winner)` – eredmény kiírása, ranglista megjelenítése  
- új játék / kilépés:  
  - `restart_game_hzs()`  
  - `exit_game_hzs()`  

A grafikus tartalom frissítését a `draw_game_hzs()` végzi, amely rajzoltatja a táblát és az információs sorokat (aktuális fázis, játékos, idő, repülési lehetőség).

---

# Indítás

A program futtatása:

```bash
python main.py
