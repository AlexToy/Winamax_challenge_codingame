import sys
import copy


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

class Ball:
    def __init__(self, x, y, shoot_distance):
        self.x = x
        self.y = y
        self.shoot_distance = shoot_distance
        self.typ = "Ball"

    def print_pos(self):
        print(self, self.typ, " pos : ", self.x, ";", self.y, " shoot : ", self.shoot_distance, file=sys.stderr,
              flush=True)


class Hole:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.typ = "Hole"

    def print_pos(self):
        print(self, self.typ, " pos : ", self.x, ";", self.y, file=sys.stderr, flush=True)


def print_map(field_map):
    print("######## MAP #########", file=sys.stderr, flush=True)
    for column in field_map:
        print(column, file=sys.stderr, flush=True)
    print("######## MAP #########", file=sys.stderr, flush=True)


def print_result_map(final_map, width, height):
    for y in range(height):
        for x in range(width):
            if final_map[y][x] == "X" or final_map[y][x] == "H":
                final_map[y][x] = "."

    for column in final_map:
        for char in column:
            print(char, end='')
        print()


def find_balls_and_holes(green_map):
    x = -1
    y = -1
    list_balls = []
    list_holes = []
    for column in green_map:
        y = y + 1
        x = -1
        for char in column:
            x = x + 1
            if char.isdigit():
                new_ball = Ball(x, y, int(char))
                list_balls.append(new_ball)
            elif char == "H":
                new_hole = Hole(x, y)
                list_holes.append(new_hole)
    return list_balls, list_holes


def check_path(pole, ball, field_map):
    if pole == "north":
        for i in range(ball.shoot_distance - 1):
            if field_map[ball.y - (i + 1)][ball.x] != "." and field_map[ball.y - (i + 1)][ball.x] != "X":
                print("Ball or hole on the way !", file=sys.stderr, flush=True)
                return False
    elif pole == "east":
        for i in range(ball.shoot_distance - 1):
            if field_map[ball.y][ball.x + (i + 1)] != "." and field_map[ball.y][ball.x + (i + 1)] != "X":
                print("Ball or hole on the way !", file=sys.stderr, flush=True)
                return False
    elif pole == "south":
        for i in range(ball.shoot_distance - 1):
            if field_map[ball.y + (i + 1)][ball.x] != "." and field_map[ball.y + (i + 1)][ball.x] != "X":
                print("Ball or hole on the way !", file=sys.stderr, flush=True)
                return False
    elif pole == "west":
        for i in range(ball.shoot_distance - 1):
            if field_map[ball.y][ball.x - (i + 1)] != "." and field_map[ball.y][ball.x - (i + 1)] != "X":
                print("Ball or hole on the way !", file=sys.stderr, flush=True)
                return False
    return True


def try_north_shoot(ball, hole, field_map, width_field, height_field):
    print(" --> Try North : ", ball.shoot_distance, file=sys.stderr, flush=True)
    print("Target : ", ball.x, ";", ball.y - ball.shoot_distance, file=sys.stderr, flush=True)
    update_field_map = copy.deepcopy(field_map)
    update_ball = Ball(ball.x, ball.y, ball.shoot_distance)

    if ball.y - ball.shoot_distance >= 0:
        if check_path("north", ball, field_map):
            arrival_case = field_map[ball.y - ball.shoot_distance][ball.x]
            arrival_case_x = ball.x
            arrival_case_y = ball.y - ball.shoot_distance
            print("Arrival case : ", arrival_case, file=sys.stderr, flush=True)
            if arrival_case == ".":
                # Mettre à jour carte et la pos de la balle puis continuer
                for i in range(update_ball.shoot_distance):
                    update_field_map[update_ball.y - i][update_ball.x] = "^"
                update_ball.y = update_ball.y - update_ball.shoot_distance
                update_ball.shoot_distance = update_ball.shoot_distance - 1

                # Carry on with a copy of map and ball
                run_status, update_map = run(update_ball, hole, update_field_map, width_field, height_field)
                if run_status:
                    return True, update_map

            elif arrival_case == "H":
                if arrival_case_x == hole.x and arrival_case_y == hole.y:
                    for i in range(update_ball.shoot_distance):
                        update_field_map[update_ball.y - i][update_ball.x] = "^"
                    print("-- Ball find the hole --", arrival_case, file=sys.stderr, flush=True)
                    print_map(update_field_map)

                    # Send a copy of map
                    return True, update_field_map
                else:
                    print("Is not the good hole", file=sys.stderr, flush=True)

    else:
        print("Arrival case is over the limit", file=sys.stderr, flush=True)

    return False, field_map


def try_east_shoot(ball, hole, field_map, width_field, height_field):
    print(" --> Try East : ", ball.shoot_distance, file=sys.stderr, flush=True)
    print("Target : ", ball.x + ball.shoot_distance, ";", ball.y, file=sys.stderr, flush=True)
    update_field_map = copy.deepcopy(field_map)
    update_ball = Ball(ball.x, ball.y, ball.shoot_distance)

    if ball.x + ball.shoot_distance < width_field:
        if check_path("east", ball, field_map):
            arrival_case = field_map[ball.y][ball.x + ball.shoot_distance]
            arrival_case_x = ball.x + ball.shoot_distance
            arrival_case_y = ball.y
            print("Arrival case : ", arrival_case, file=sys.stderr, flush=True)
            if arrival_case == ".":
                # Mettre à jour carte et la pos de la balle puis continuer
                for i in range(update_ball.shoot_distance):
                    update_field_map[update_ball.y][update_ball.x + i] = ">"
                update_ball.x = update_ball.x + update_ball.shoot_distance
                update_ball.shoot_distance = update_ball.shoot_distance - 1

                # Carry on with a copy of map and ball
                run_status, update_map = run(update_ball, hole, update_field_map, width_field, height_field)
                if run_status:
                    return True, update_map

            elif arrival_case == "H":
                # print("Hole find", arrival_case, file=sys.stderr, flush=True)
                if arrival_case_x == hole.x and arrival_case_y == hole.y:
                    for i in range(update_ball.shoot_distance):
                        update_field_map[update_ball.y][update_ball.x + i] = ">"
                    print("-- Ball find the hole --", arrival_case, file=sys.stderr, flush=True)
                    print_map(update_field_map)

                    return True, update_field_map
                else:
                    print("Is not the good hole", file=sys.stderr, flush=True)
    else:
        print("Arrival case is over the limit", file=sys.stderr, flush=True)

    return False, field_map


def try_south_shoot(ball, hole, field_map, width_field, height_field):
    print(" --> Try South : ", ball.shoot_distance, file=sys.stderr, flush=True)
    print("Target : ", ball.x, ";", ball.y + ball.shoot_distance, file=sys.stderr, flush=True)
    update_field_map = copy.deepcopy(field_map)
    update_ball = Ball(ball.x, ball.y, ball.shoot_distance)

    if ball.y + ball.shoot_distance < height_field:
        if check_path("south", ball, field_map):
            arrival_case = field_map[ball.y + ball.shoot_distance][ball.x]
            arrival_case_x = ball.x
            arrival_case_y = ball.y + ball.shoot_distance
            print("Arrival case : ", arrival_case, file=sys.stderr, flush=True)
            if arrival_case == ".":
                # Mettre à jour carte et la pos de la balle puis continuer
                for i in range(update_ball.shoot_distance):
                    update_field_map[update_ball.y + i][update_ball.x] = "v"
                update_ball.y = update_ball.y + update_ball.shoot_distance
                update_ball.shoot_distance = update_ball.shoot_distance - 1

                run_status, update_map = run(update_ball, hole, update_field_map, width_field, height_field)
                if run_status:
                    return True, update_map

            elif arrival_case == "H":
                if arrival_case_x == hole.x and arrival_case_y == hole.y:
                    for i in range(update_ball.shoot_distance):
                        update_field_map[update_ball.y + i][update_ball.x] = "v"
                    print("-- Ball find the hole --", arrival_case, file=sys.stderr, flush=True)
                    print_map(update_field_map)

                    return True, update_field_map
                else:
                    print("Is not the good hole", file=sys.stderr, flush=True)
    else:
        print("Arrival case is over the limit", file=sys.stderr, flush=True)

    return False, field_map


def try_west_shoot(ball, hole, field_map, width_field, height_field):
    print(" --> Try West : ", ball.shoot_distance, file=sys.stderr, flush=True)
    print("Target : ", ball.x - ball.shoot_distance, ";", ball.y, file=sys.stderr, flush=True)
    update_field_map = copy.deepcopy(field_map)
    update_ball = Ball(ball.x, ball.y, ball.shoot_distance)

    if ball.x - ball.shoot_distance >= 0:
        if check_path("west", ball, field_map):
            arrival_case = field_map[ball.y][ball.x - ball.shoot_distance]
            arrival_case_x = ball.x - ball.shoot_distance
            arrival_case_y = ball.y
            print("Arrival case : ", arrival_case, file=sys.stderr, flush=True)
            if arrival_case == ".":
                # Mettre à jour carte et la pos de la balle puis continuer
                for i in range(update_ball.shoot_distance):
                    update_field_map[update_ball.y][update_ball.x - i] = "<"
                update_ball.x = update_ball.x - update_ball.shoot_distance
                update_ball.shoot_distance = update_ball.shoot_distance - 1

                run_status, update_map = run(update_ball, hole, update_field_map, width_field, height_field)
                if run_status:
                    return True, update_map

            elif arrival_case == "H":
                if arrival_case_x == hole.x and arrival_case_y == hole.y:
                    for i in range(update_ball.shoot_distance):
                        update_field_map[update_ball.y][update_ball.x - i] = "<"
                    print("-- Ball find the hole --", arrival_case, file=sys.stderr, flush=True)
                    print_map(field_map)

                    return True, update_field_map
                else:
                    print("Is not the good hole", file=sys.stderr, flush=True)
    else:
        print("Arrival case is over the limit", file=sys.stderr, flush=True)

    return False, field_map


def run(ball, hole, field_map, width_field, height_field):
    if ball.shoot_distance > 0:
        print("-- New RUN ---", file=sys.stderr, flush=True)
        print_map(field_map)

        north_status, new_map = try_north_shoot(ball, hole, field_map, width_field, height_field)
        if north_status:
            return True, new_map

        west_status, new_map = try_west_shoot(ball, hole, field_map, width_field, height_field)
        if west_status:
            return True, new_map

        south_status, new_map = try_south_shoot(ball, hole, field_map, width_field, height_field)
        if south_status:
            return True, new_map

        east_status, new_map = try_east_shoot(ball, hole, field_map, width_field, height_field)
        if east_status:
            return True, new_map

    else:
        print("-- Shoot distance 0 ---", file=sys.stderr, flush=True)

    return False, field_map


def try_hole(list_ball, index_ball, list_holes, field_map, width_field, height_field):
    print("--- New ball ---", file=sys.stderr, flush=True)
    for hole in list_holes:
        print("--- New hole ---", file=sys.stderr, flush=True)
        hole_status, new_map = run(list_ball[index_ball], hole, field_map, width_field, height_field)

        if hole_status and list_ball[index_ball] == list_balls[-1]:
            return True, new_map
        elif hole_status:
            index_remove_hole = list_holes.index(hole)
            update_list_holes = copy.deepcopy(list_holes)
            del update_list_holes[index_remove_hole]
            status, update_map = try_hole(list_ball, index_ball + 1, update_list_holes, new_map, width_field, height_field)
            if status:
                return True, update_map

    return False, field_map

# ---- Loop ----#

map_f = []
list_balls = []
list_holes = []
width_field, height_field = 40, 8

list_rows = []
row0 = ".XXX.5XX4H5............4H..3XXH.2.HX3..."
list_rows.append(row0)
row1 = "XX4.X..X......3.....HH.2X.....5.....4XX."
list_rows.append(row1)
row2 = "X4..X3.X......H...5.....XXXXXXX2.HX2..H."
list_rows.append(row2)
row3 = "X..XXXXX.....H3.H.X..22X3XXH.X2X...2HHXH"
list_rows.append(row3)
row4 = ".X.X.H.X........X3XH.HXX.XXXXX.H..HX..2."
list_rows.append(row4)
row5 = "X.HX.X.X....HH....X3.H.X.....H..XXXX3..."
list_rows.append(row5)
row6 = "X..X.H.X.43......XXH....HXX3..H.X2.HX2.."
list_rows.append(row6)
row7 = ".XHXXXXX..H3H...H2X.H..3X2..HXX3H.2XXXXH"
list_rows.append(row7)


for row in list_rows:
    line_map = []
    for j in row:
        line_map.append(j)
    map_f.append(line_map)
    del line_map

# Get positions of balls and holes
list_balls, list_holes = find_balls_and_holes(map_f)
for index, ball in enumerate(list_balls):
    print("Ball ", index, " : ", ball.x, ";", ball.y, file=sys.stderr, flush=True)

# Print the field
print_map(map_f)

status, final_map = try_hole(list_balls, 0, list_holes, map_f, width_field, height_field)
if status:
    print_result_map(final_map, width_field, height_field)

