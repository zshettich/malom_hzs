import turtle
import random
from malomtabla_hzs import Tablahzs, draw_board_hzs
from jatekos_hzs import Playerrankhzs
from idozites_hsz import start_timer_hzs, get_elapsed_hzs, wait_seconds_hzs

screen = turtle.Screen()
screen.setup(800, 900)
screen.title("Malom játék – HZS - ZAJDU4")
screen.tracer(0)

board = Tablahzs()
player_rank = Playerrankhzs()
current_player = 1
phase = "placing"
selected_pos = None
start_time = start_timer_hzs()
pieces_placed = {1: 0, 2: 0}
computer_thinking = False


def draw_info_hzs():
    turtle.penup()
    turtle.goto(0, 380)
    turtle.color("black")
    phase_text = "Lerakás" if phase == "placing" else "Mozgatás"
    player_text = "Te (Piros)" if current_player == 1 else "Gép (Kék)"
    elapsed = int(get_elapsed_hzs(start_time))

    p1_count = count_pieces_hzs(board, 1)
    p2_count = count_pieces_hzs(board, 2)
    fly_text = ""
    if phase == "moving":
        if p1_count == 3: fly_text += " (Te repülhetsz!)"
        if p2_count == 3: fly_text += " (Gép repülhet!)"

    turtle.write(f"Fázis: {phase_text} | Játékos: {player_text} | Idő: {elapsed} mp{fly_text}",
                 align="center", font=("Arial", 16, "bold"))


def draw_game_hzs():
    turtle.clear()
    draw_board_hzs(board)
    draw_info_hzs()
    screen.update()


def check_mill_hzs(board, pos, player):
    mills = [
        [0, 1, 2], [5, 6, 7],
        [8, 9, 10], [13, 14, 15],
        [16, 17, 18], [21, 22, 23],
        [0, 3, 5], [2, 4, 7],
        [8, 11, 13], [10, 12, 15],
        [16, 19, 21], [18, 20, 23],
        [1, 9, 17], [3, 11, 19], [4, 12, 20], [6, 14, 22]
    ]

    for mill in mills:
        if pos in mill:
            if all(board.positions[p] == player for p in mill):
                return True
    return False


def can_move_hzs(board, player):
    if count_pieces_hzs(board, player) == 3:
        return any(p == 0 for p in board.positions)

    for i, p in enumerate(board.positions):
        if p == player:
            for neighbor in board.get_neighbors_hzs(i):
                if board.positions[neighbor] == 0:
                    return True
    return False


def count_pieces_hzs(board, player):
    return sum(1 for p in board.positions if p == player)


def get_computer_move_hzs():
    if phase == "placing":
        empty_positions = [i for i, p in enumerate(board.positions) if p == 0]

        for pos in empty_positions:
            board.positions[pos] = 2
            if check_mill_hzs(board, pos, 2):
                board.positions[pos] = 0
                return pos
            board.positions[pos] = 0

        for pos in empty_positions:
            board.positions[pos] = 1
            if check_mill_hzs(board, pos, 1):
                board.positions[pos] = 0
                return pos
            board.positions[pos] = 0

        if empty_positions:
            return random.choice(empty_positions)

    elif phase == "moving":
        computer_pieces = [i for i, p in enumerate(board.positions) if p == 2]
        valid_moves = []

        is_computer_flying = len(computer_pieces) == 3

        if is_computer_flying:
            empty_spots = [i for i, p in enumerate(board.positions) if p == 0]
            for piece_pos in computer_pieces:
                for target in empty_spots:
                    valid_moves.append((piece_pos, target))
        else:
            for piece_pos in computer_pieces:
                for neighbor in board.get_neighbors_hzs(piece_pos):
                    if board.positions[neighbor] == 0:
                        valid_moves.append((piece_pos, neighbor))

        for move_from, move_to in valid_moves:
            board.positions[move_from] = 0
            board.positions[move_to] = 2
            if check_mill_hzs(board, move_to, 2):
                board.positions[move_from] = 2
                board.positions[move_to] = 0
                return (move_from, move_to)
            board.positions[move_from] = 2
            board.positions[move_to] = 0

        if valid_moves:
            return random.choice(valid_moves)

    return None


def computer_remove_piece_hzs():
    # Ez a függvény most már csak akkor hívódik meg, ha VAN levehető bábu
    player_pieces = [i for i, p in enumerate(board.positions) if p == 1]

    non_mill_pieces = []
    for pos in player_pieces:
        if not check_mill_hzs(board, pos, 1):
            non_mill_pieces.append(pos)

    if non_mill_pieces:
        rem = random.choice(non_mill_pieces)
        board.positions[rem] = 0
    # Nincs "elif player_pieces", mert ha minden malomban van, nem vehet le semmit!


def has_removable_piece_hzs(opponent):
    """Megnézi, hogy van-e az ellenfélnek olyan bábuja, ami NINCS malomban."""
    opponent_pieces = [i for i, p in enumerate(board.positions) if p == opponent]
    for p in opponent_pieces:
        if not check_mill_hzs(board, p, opponent):
            return True  # Van levehető bábu
    return False  # Minden bábu malomban van


def computer_turn_hzs():
    global current_player, pieces_placed, phase, computer_thinking

    if computer_thinking:
        return

    computer_thinking = True
    screen.onclick(None)
    turtle.ontimer(lambda: execute_computer_move_hzs(), 500)


def execute_computer_move_hzs():
    global current_player, pieces_placed, phase, computer_thinking

    move = get_computer_move_hzs()

    if phase == "placing" and move is not None:
        board.positions[move] = 2
        pieces_placed[2] += 1
        made_mill = check_mill_hzs(board, move, 2)

        # Malom kezelése
        if made_mill:
            draw_game_hzs()
            turtle.penup()
            turtle.goto(0, 350)

            # Ellenőrizzük, levehet-e bábut
            if has_removable_piece_hzs(1):
                turtle.color("blue")
                turtle.write("Gép malmot képzett! Levett egy bábut.", align="center", font=("Arial", 16, "bold"))
                screen.update()
                wait_seconds_hzs(0.8)
                computer_remove_piece_hzs()
            else:
                turtle.color("orange")
                turtle.write("Gép malmot képzett, de minden bábud védett!", align="center", font=("Arial", 16, "bold"))
                screen.update()
                wait_seconds_hzs(1.5)

        if pieces_placed[1] == 9 and pieces_placed[2] == 9:
            phase = "moving"

        current_player = 1
        draw_game_hzs()
        check_winner_hzs()
        computer_thinking = False
        screen.onclick(on_click)

    elif phase == "moving" and move is not None:
        move_from, move_to = move
        board.positions[move_from] = 0
        board.positions[move_to] = 2
        made_mill = check_mill_hzs(board, move_to, 2)

        if made_mill:
            draw_game_hzs()
            turtle.penup()
            turtle.goto(0, 350)

            if has_removable_piece_hzs(1):
                turtle.color("blue")
                turtle.write("Gép malmot képzett! Levett egy bábut.", align="center", font=("Arial", 16, "bold"))
                screen.update()
                wait_seconds_hzs(0.8)
                computer_remove_piece_hzs()
            else:
                turtle.color("orange")
                turtle.write("Gép malmot képzett, de minden bábud védett!", align="center", font=("Arial", 16, "bold"))
                screen.update()
                wait_seconds_hzs(1.5)

        current_player = 1
        draw_game_hzs()
        check_winner_hzs()
        computer_thinking = False
        screen.onclick(on_click)
    else:
        computer_thinking = False
        screen.onclick(on_click)


def on_click(x, y):
    global current_player, phase, selected_pos, pieces_placed

    if computer_thinking or current_player == 2:
        return

    pos = board.get_position_from_click_hzs(x, y)
    if pos is None:
        if selected_pos is not None:
            selected_pos = None
            draw_game_hzs()
        return

    if phase == "placing":
        if board.positions[pos] == 0:
            board.positions[pos] = current_player
            pieces_placed[current_player] += 1

            if check_mill_hzs(board, pos, current_player):
                # Ellenőrzés: Van-e levehető bábu az ellenfélnél?
                if has_removable_piece_hzs(2):
                    draw_game_hzs()
                    turtle.penup()
                    turtle.goto(0, 350)
                    turtle.color("red")
                    turtle.write("MALOM! Kattints egy KÉK bábura a levételhez!", align="center",
                                 font=("Arial", 16, "bold"))
                    screen.update()
                    screen.onclick(None)
                    screen.onclick(lambda x, y: remove_piece_player_hzs(x, y))
                    return
                else:
                    # Nincs levehető bábu -> Kiírjuk és folytatjuk
                    draw_game_hzs()
                    turtle.penup()
                    turtle.goto(0, 350)
                    turtle.color("orange")
                    turtle.write("MALOM! De az ellenfél minden bábuja védett!", align="center",
                                 font=("Arial", 16, "bold"))
                    screen.update()
                    wait_seconds_hzs(1.5)
                    # Folytatjuk a kört váltással, mintha nem lett volna levétel

            if pieces_placed[1] == 9 and pieces_placed[2] == 9:
                phase = "moving"

            current_player = 2
            draw_game_hzs()
            if not check_winner_hzs():
                computer_turn_hzs()

    elif phase == "moving":
        if selected_pos is None:
            if board.positions[pos] == current_player:
                selected_pos = pos
                draw_game_hzs()
                turtle.penup()
                turtle.goto(board.coords[pos][0], board.coords[pos][1])
                turtle.color("yellow")
                turtle.dot(10)
                screen.update()
        else:
            if pos == selected_pos:
                selected_pos = None
                draw_game_hzs()
            elif board.positions[pos] == 0:
                player_pieces_count = count_pieces_hzs(board, 1)
                is_flying = (player_pieces_count == 3)
                is_neighbor = pos in board.get_neighbors_hzs(selected_pos)

                if is_neighbor or is_flying:
                    board.positions[pos] = current_player
                    board.positions[selected_pos] = 0
                    selected_pos = None

                    if check_mill_hzs(board, pos, current_player):
                        if has_removable_piece_hzs(2):
                            draw_game_hzs()
                            turtle.penup()
                            turtle.goto(0, 350)
                            turtle.color("red")
                            turtle.write("MALOM! Kattints egy KÉK bábura a levételhez!", align="center",
                                         font=("Arial", 16, "bold"))
                            screen.update()
                            screen.onclick(None)
                            screen.onclick(lambda x, y: remove_piece_player_hzs(x, y))
                            return
                        else:
                            draw_game_hzs()
                            turtle.penup()
                            turtle.goto(0, 350)
                            turtle.color("orange")
                            turtle.write("MALOM! De az ellenfél minden bábuja védett!", align="center",
                                         font=("Arial", 16, "bold"))
                            screen.update()
                            wait_seconds_hzs(1.5)

                    current_player = 2
                    draw_game_hzs()
                    if not check_winner_hzs():
                        computer_turn_hzs()
                else:
                    draw_game_hzs()
                    turtle.penup()
                    turtle.goto(0, 350)
                    turtle.color("red")
                    turtle.write("Csak szomszédos mezőre léphetsz (még nincs 3 bábud)!", align="center",
                                 font=("Arial", 12, "bold"))
                    screen.update()
                    turtle.ontimer(lambda: draw_game_hzs(), 1200)

            elif board.positions[pos] == current_player:
                selected_pos = pos
                draw_game_hzs()
                turtle.penup()
                turtle.goto(board.coords[pos][0], board.coords[pos][1])
                turtle.color("yellow")
                turtle.dot(10)
                screen.update()


def remove_piece_player_hzs(x, y):
    global current_player, phase
    pos = board.get_position_from_click_hzs(x, y)
    opponent = 2

    if pos is not None and board.positions[pos] == opponent:
        # Szigorú ellenőrzés: Ha malomban van, SOHA nem vehető le
        if check_mill_hzs(board, pos, opponent):
            draw_game_hzs()
            turtle.penup()
            turtle.goto(0, 350)
            turtle.color("red")
            turtle.write("Ez a bábu malomban van! Nem veheted le!", align="center", font=("Arial", 16, "bold"))
            turtle.goto(0, 320)
            turtle.write("(Keress olyat, ami nincs malomban...)", align="center", font=("Arial", 14, "bold"))
            screen.update()
            return

        # Ha nem volt malomban, levesszük
        board.positions[pos] = 0
        current_player = 2
        screen.onclick(None)
        screen.onclick(on_click)
        draw_game_hzs()

        if not check_winner_hzs():
            computer_turn_hzs()


def check_winner_hzs():
    for player in [1, 2]:
        opponent = 2 if player == 1 else 1

        if phase == "moving" and count_pieces_hzs(board, opponent) < 3:
            end_game_hzs(player)
            return True

        if phase == "moving" and not can_move_hzs(board, opponent):
            end_game_hzs(player)
            return True
    return False


def end_game_hzs(winner):
    global computer_thinking
    computer_thinking = True
    screen.onclick(None)

    elapsed = int(get_elapsed_hzs(start_time))
    player_rank.add_result_hzs(elapsed, winner)

    turtle.clear()
    turtle.penup()
    turtle.goto(0, 100)
    turtle.color("red" if winner == 1 else "blue")
    winner_text = "TE NYERTÉL!" if winner == 1 else "A GÉP NYERT!"
    turtle.write(winner_text, align="center", font=("Arial", 36, "bold"))

    turtle.goto(0, 50)
    turtle.color("black")
    turtle.write(f"Idő: {elapsed} mp", align="center", font=("Arial", 24, "bold"))

    turtle.goto(0, -50)
    results_text = player_rank.get_results_text_hzs()
    turtle.write(results_text, align="center", font=("Arial", 12, "normal"))

    turtle.goto(0, -250)
    turtle.color("green")
    turtle.write("Új játék? (Nyomd meg az 'I' betűt)\nKilépés? (Nyomd meg az 'N' betűt)", align="center",
                 font=("Arial", 16, "bold"))

    screen.update()
    screen.onkey(restart_game_hzs, "i")
    screen.onkey(exit_game_hzs, "n")
    screen.listen()


def restart_game_hzs():
    global board, current_player, phase, selected_pos, start_time, pieces_placed, computer_thinking
    board = Tablahzs()
    current_player = 1
    phase = "placing"
    selected_pos = None
    start_time = start_timer_hzs()
    pieces_placed = {1: 0, 2: 0}
    computer_thinking = False

    screen.clear()
    screen.tracer(0)
    screen.onclick(on_click)
    screen.listen()
    draw_game_hzs()


def exit_game_hzs():
    turtle.bye()


draw_game_hzs()
screen.onclick(on_click)
screen.listen()
turtle.mainloop()