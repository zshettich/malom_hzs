import turtle


class Tablahzs:
    def __init__(self):
        self.positions = [0] * 24
        self.coords = self.create_coords_hzs()
        self.adjacency = self.create_adjacency_hzs()

    def create_coords_hzs(self):
        # A sorrend a következő minden négyzeten:
        # 0: Bal-Fent, 1: Közép-Fent, 2: Jobb-Fent
        # 3: Bal-Közép, 4: Jobb-Közép
        # 5: Bal-Lent, 6: Közép-Lent, 7: Jobb-Lent
        coords = []
        outer_size = 300
        middle_size = 200
        inner_size = 100

        for size in [outer_size, middle_size, inner_size]:
            half = size // 2
            coords.append((-half, half))  # 0: TL
            coords.append((0, half))  # 1: TM
            coords.append((half, half))  # 2: TR
            coords.append((-half, 0))  # 3: ML
            coords.append((half, 0))  # 4: MR
            coords.append((-half, -half))  # 5: BL
            coords.append((0, -half))  # 6: BM
            coords.append((half, -half))  # 7: BR

        return coords

    def create_adjacency_hzs(self):
        # Az indexek a create_coords_hzs sorrendje alapján:
        # Külső kör: 0-7, Középső: 8-15, Belső: 16-23
        adjacency = {}

        # Külső kör (0-7)
        adjacency[0] = [1, 3]
        adjacency[1] = [0, 2, 9]  # 9 a középső kör fenti középső pontja
        adjacency[2] = [1, 4]
        adjacency[3] = [0, 5, 11]  # 11 a középső kör bal oldali pontja
        adjacency[4] = [2, 7, 12]  # 12 a középső kör jobb oldali pontja
        adjacency[5] = [3, 6]
        adjacency[6] = [5, 7, 14]  # 14 a középső kör lenti középső pontja
        adjacency[7] = [4, 6]

        # Középső kör (8-15)
        adjacency[8] = [9, 11]
        adjacency[9] = [8, 10, 1, 17]  # Kapcsolódik kifelé (1) és befelé (17)
        adjacency[10] = [9, 12]
        adjacency[11] = [8, 13, 3, 19]  # Kapcsolódik kifelé (3) és befelé (19)
        adjacency[12] = [10, 15, 4, 20]  # Kapcsolódik kifelé (4) és befelé (20)
        adjacency[13] = [11, 14]
        adjacency[14] = [13, 15, 6, 22]  # Kapcsolódik kifelé (6) és befelé (22)
        adjacency[15] = [12, 14]

        # Belső kör (16-23)
        adjacency[16] = [17, 19]
        adjacency[17] = [16, 18, 9]  # Kapcsolódik kifelé (9)
        adjacency[18] = [17, 20]
        adjacency[19] = [16, 21, 11]  # Kapcsolódik kifelé (11)
        adjacency[20] = [18, 23, 12]  # Kapcsolódik kifelé (12)
        adjacency[21] = [19, 22]
        adjacency[22] = [21, 23, 14]  # Kapcsolódik kifelé (14)
        adjacency[23] = [20, 22]

        return adjacency

    def get_neighbors_hzs(self, pos):
        return self.adjacency.get(pos, [])

    def get_position_from_click_hzs(self, x, y):
        for i, (cx, cy) in enumerate(self.coords):
            # Kicsit növeltem az érzékelési távolságot a kényelemért
            if abs(x - cx) < 30 and abs(y - cy) < 30:
                return i
        return None


def draw_board_hzs(board):
    turtle.speed(0)
    turtle.hideturtle()

    # Ha már van rajz, ne villogjon, csak a bábukat frissítsük,
    # de a turtle.clear() miatt a main-ben úgyis törlődik minden.
    # Itt csak a tábla kirajzolása történik.

    outer_size = 300
    middle_size = 200
    inner_size = 100

    for size in [outer_size, middle_size, inner_size]:
        draw_square_hzs(size)

    draw_lines_hzs(outer_size, middle_size, inner_size)

    for i, (x, y) in enumerate(board.coords):
        turtle.penup()
        turtle.goto(x, y)
        if board.positions[i] == 0:
            turtle.color("lightgray")  # Világosabb szürke, hogy jobban látszódjon
            turtle.dot(15)
        elif board.positions[i] == 1:
            turtle.color("red")
            turtle.dot(30)
        elif board.positions[i] == 2:
            turtle.color("blue")
            turtle.dot(30)


def draw_square_hzs(size):
    turtle.penup()
    half = size // 2
    turtle.goto(-half, half)
    turtle.pendown()
    turtle.color("black")
    turtle.pensize(3)
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)
    turtle.pensize(1)


def draw_lines_hzs(outer, middle, inner):
    # Felső összekötő
    turtle.penup()
    turtle.goto(0, outer // 2)
    turtle.pendown()
    turtle.goto(0, inner // 2)

    # Alsó összekötő
    turtle.penup()
    turtle.goto(0, -outer // 2)
    turtle.pendown()
    turtle.goto(0, -inner // 2)

    # Bal összekötő
    turtle.penup()
    turtle.goto(-outer // 2, 0)
    turtle.pendown()
    turtle.goto(-inner // 2, 0)

    # Jobb összekötő
    turtle.penup()
    turtle.goto(outer // 2, 0)
    turtle.pendown()
    turtle.goto(inner // 2, 0)