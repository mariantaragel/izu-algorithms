import sys
import math

DIRECTIONS = [
    (-1, -1), # LU
    (0, -1), # U
    (1, -1), # RU
    (-1, 0), # L
    (1, 0), # R
    (-1, 1), # LD
    (0, 1), # D
    (1, 1), # RD
]

def get_neighbors(map, point, goal):
    neighbors = []
    for i in DIRECTIONS: # try all directions
        pos = [point[0][0] + i[0], point[0][1] + i[1]]
        if map[pos[1]][pos[0]] == 'Z':
            continue
        gcost = map[pos[1]][pos[0]] + point[1] # distance from the start
        hcost = heuristic(pos, goal) # estimated distance to the end
        neighbor = (pos, gcost, round(hcost, 2), round(gcost + hcost, 2), [point[0][0], point[0][1]])
        neighbors.append(neighbor)
    return neighbors

def print_result(array, start, goal):
    print("++++ RESULT:")
    path = []
    index = is_point_in_array(goal, array)
    path.append(array[index][0])
    while array[index][4] != "NULL":
        index = is_point_in_array(array[index][4], array)
        path.insert(0, array[index][0]) # insterting at the beginning of the final path
    for i in path:
        print(i)

def is_point_in_array(pos, array):
    index = 0
    for i in array:
        if i[0] == pos:
            return index
        index += 1
    return -1

def heuristic(curr_pos, goal):
    return math.sqrt((curr_pos[0] - goal[0]) ** 2 + (goal[1] - curr_pos[1]) ** 2)

def print_array(array):
    for i in array:
        print_node(i)

def print_node(node):
    print(str(node[0]) + ", " + str(node[3]) + ", " + str(node[4]))

def print_map(map):
    for i in map:
        for j in i:
            print(str(j) + " ", end="")
        print()

def a_star(map, start, goal):
    open = []
    closed = []
    open.append(start)
    num = 1

    while(open):
        print("----------------------")
        print("Iteration: " + str(num))
        print("++++ OPEN:")
        print_array(open)
        print("++++ CLOSED:")
        print_array(closed)

        min = ([0, 0], 0, sys.maxsize, sys.maxsize + 0, None)
        for i in open:
            if i[3] < min[3]:
                min = i
        
        print("++++ CUR_NODE:")
        print(str(min[0]) + " " + str(min[1]) + " " + str(min[2]) + " " + str(min[3]))

        open.remove(min)
        closed.append(min)

        if min[0] == goal:
            print_result(closed, start, goal)
            break

        neighbors = get_neighbors(map, min, goal)
        for i in neighbors:
            if is_point_in_array(i[0], closed) >= 0:
                continue

            index = is_point_in_array(i[0], open)
            if index >= 0:
                if i[3] < open[index][3]:
                    open[index] = i
            else:
                open.append(i)
        num += 1

if __name__ == "__main__":
    map = [
        [  8 ,  9 ,  9 ,  9 ,  9 ,  3 ,  9 ,  6 ,  7 ,  8 ],
        [  8 ,  9 , 'Z', 'Z', 'Z',  3 ,  9 ,  6 ,  7 ,  8 ],
        [  6 ,  9 , 'Z',  2 ,  5 ,  3 ,  8 ,  5 ,  7 ,  8 ],
        [  7 ,  9 , 'Z',  6 ,  4 ,  3 ,  8 ,  7 ,  5 ,  8 ],
        [ 'Z', 'Z', 'Z', 'Z', 'Z',  3 , 'Z', 'Z', 'Z', 'Z'], # numbers represents distance to get there from neighboring cells
        [  9 ,  9 , 'Z',  8 ,  3 ,  9 ,  9 , 'Z',  8 ,  9 ], # 'Z' is wall
        [  9 ,  9 , 'Z',  9 ,  3 ,  4 ,  2 , 'Z',  7 ,  7 ],
        [  9 ,  9 , 'Z',  9 ,  3 ,  7 ,  8 , 'Z',  8 ,  7 ],
        [  9 ,  9 ,  9 ,  9 ,  3 ,  9 ,  8 ,  7 ,  7 ,  8 ],
        [  9 ,  9 ,  7 ,  6 ,  3 ,  7 ,  9 ,  8 ,  9 ,  9 ],
    ]
    start = [6, 6]
    goal = [3, 2]

    print("++++ START:")
    print(start)
    print("++++ END:")
    print(goal)
    print("++++ MAP:")
    print_map(map)

    init = (start, 0, heuristic(start, goal), heuristic(start, goal) + 0, "NULL")
    a_star(map, init, goal)