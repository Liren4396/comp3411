#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Data Structure:

Grid Representation: The input grid is initially stored as a list of strings (str_list). 
After processing, it is converted into a list of lists, 
where each character is represented by its corresponding integer value. 
This list of lists serves as the main data structure to represent the grid.

Direction Vectors: The direction list stores tuples 
representing the four cardinal directions: up, left, down, and right. 
These vectors are used to navigate adjacent cells in the grid.

Bridge Character Mappings: Dictionaries (horizontal and vertical) are used to map bridge numbers 
to their corresponding characters and vice versa. 
This mapping is utilized when converting between bridge numbers and characters.

Temporary Data Storage: When processing the grid or during bridge establishment, 
temporary lists are created to store intermediate results.
For example, exsit and potential lists are used to store information 
about existing bridges and potential bridges in certain directions.

Function Return Values: Several functions return integer values representing bridge counts or status.
 These return values are used to make decisions and update the game state.

Algorithm Overview: 
The program utilizes a backtracking approach combined with iterative bridge 
establishment and validation to find the solution. 
It keeps track of temporary changes to the game board and reverts them if needed. 
The algorithm ensures that the game board follows the rules of bridge construction between islands.


Design Decisions: 
The program uses lists to represent the grid and bridges, 
making it easy to manipulate and validate the game state. 
It also employs dictionaries for mapping bridge characters to their corresponding numeric values, 
enhancing readability and maintainability.
'''

def retrieve_game_data():
    grid = []

    try:
        while True:
            temp_str = input().strip()
            if not temp_str:
                break
            grid.append([int(c) if c.isdigit() else (ord(c) - ord('a') + 10) for c in temp_str])
    except EOFError:
        pass

    row = len(grid)
    col = len(grid[0])
    for i in range(row):
        for j in range(col):
            if grid[i][j] == -41:
                grid[i][j] = 0
    return grid


'''
def retrieve_game_data():
    # Initialize an empty list to store the input grid
    grid = []
    
    # Read input until EOFError (no more input)
    try:
        # Read the first line of input
        temp_str = input()
        grid.append(list(temp_str))

        # Read subsequent lines until EOFError
        while True:
            temp_str = input()
            if not temp_str:
                break  # Exit the loop if input is empty (EOFError)
            grid.append(list(temp_str))

    except EOFError:
        pass  # Reached end of file, stop reading input

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '.':
                grid[i][j] = 0
            elif grid[i][j] == 'a':
                grid[i][j] = 10
            elif grid[i][j] =='b':
                grid[i][j] = 11
            elif grid[i][j] == 'c':
                grid[i][j] = 12
            else:
                grid[i][j] = int(grid[i][j])

    return grid
'''


direction = [(0,-1),(-1, 0),(0,1),(1,0)]
maximum_bridge = 3


def convert_number_to_bridge(d, num):
    horizontal = {1: '-', 2: '=', 3: 'E'}
    vertical = {1: '|', 2: '"', 3: '#'}
    if d % 2 == 0:
        return horizontal.get(num, 0)
    else:
        return vertical.get(num, 0)


def check_valid_cell(data, i, j):
    n = len(data)
    if n == 0:
        return False
    m = len(data[0])
    if i >= 0 and i < n and j >= 0 and j < m:
        return True
    return False
 
def count_bridges(data, i, j, d):
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    if not check_valid_cell(data, ni, nj):
        return 0
    horizontal = {'-': 1, '=': 2, 'E': 3}
    vertical = {'|': 1, '"': 2, '#': 3}
    if isinstance(data[ni][nj], int) and data[ni][nj] > 0:
        return 0
    if d % 2 == 0:
        return horizontal.get(data[ni][nj], 0)
    else:
        return vertical.get(data[ni][nj], 0)


def calculate_temporary_bridge_count(data, i, j, d):
    bridge_index = count_bridges(data, i, j, d)
    if bridge_index == maximum_bridge:
        return 0
    bnch = convert_number_to_bridge(d % 2, bridge_index)
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    while check_valid_cell(data, ni, nj) and data[ni][nj] == bnch:
        ni = ni + direction[d][0]
        nj = nj + direction[d][1]
    if not check_valid_cell(data, ni, nj):
        return 0
    if isinstance(data[ni][nj], int) and data[ni][nj] > 0:
        exsit_bn = 0
        for nd in range(4):
            exsit_bn += count_bridges(data, ni, nj, nd)
        return min(maximum_bridge - bridge_index, data[ni][nj] - exsit_bn)
    return 0

def establish_bridge(data, i ,j, d, num):
    bridge_index = count_bridges(data, i, j, d)
    new_bridge_index = bridge_index + num
    bnch = convert_number_to_bridge(d % 2, bridge_index)
    nbnch = convert_number_to_bridge(d % 2, new_bridge_index)
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    while check_valid_cell(data, ni, nj) and data[ni][nj] == bnch:
        data[ni][nj] = nbnch
        ni = ni + direction[d][0]
        nj = nj + direction[d][1]
 
def determine_min_bridge_for_all_directions(potential, remain_bn):
    pot = [x for x in potential if x > 0]
    if remain_bn == sum(potential):
        return max(min(pot), 0)
    if remain_bn + 1 == sum(potential):
        return max(min(pot) - 1, 0)
    if remain_bn + 2 == sum(potential):
        return max(min(pot) - 2, 0)
    return 0
 
def append_confirmed_bridge(data):
    n = len(data)
    if n == 0:
        return
    m = len(data[0])
    found = False
    for i in range(0, n):
        for j in range(0, m):
            if isinstance(data[i][j], int) and  0 < data[i][j]:
                exsit = []
                potential = []
                for d in range(0,4):
                    exsit.append(count_bridges(data, i, j, d))
                    # print(exsit)
                    potential.append(calculate_temporary_bridge_count(data, i, j, d))
                    # print(potential)
                if sum(potential) != 0:
                    if sum(potential) + sum(exsit) == data[i][j]:
                        found = True
                        for d in range(0, 4):
                            establish_bridge(data, i, j, d, potential[d])
                    else:
                        remain_bn = data[i][j] - sum(exsit)
                        min_bridge = determine_min_bridge_for_all_directions(potential, remain_bn)
                        for d in range(0, 4):
                            if potential[d] > 0:
                                establish_bridge(data, i, j, d, min_bridge)
    return found
 
 
def solve_the_game(data):
    # Create a temporary copy of the game data
    data_tmp = [row[:] for row in data]

    # Loop until all confirmed bridges are appended
    while True:
        # If no confirmed bridges are appended, exit the loop
        if not append_confirmed_bridge(data):
            break
    # Flag to track correct solution
    correct_flag = True
    n = len(data)
    m = len(data[0])
    # Check if each cell has the correct number of bridges
    for i in range(0, n):
        for j in range(0, m):
            if isinstance(data[i][j], int) and  0 < data[i][j]:
                exsit = 0
                for d in range(0,4):
                    exsit += count_bridges(data, i, j, d)
                if exsit != data[i][j]:
                    correct_flag = False
                    break
    # If all cells have the correct number of bridges, return True
    if correct_flag:
        # Print the game board after all bridges are appended
        for row in data:
            print(''.join(str(chr(ord('a') + cell - 10) if isinstance(cell, int) and cell >= 10 else ' ' if cell == 0 else cell) for cell in row))
        return True
    # If some cells have fewer bridges than required, attempt to add more bridges
    n = len(data)
    m = len(data[0])
    for i in range(0, n):
        for j in range(0, m):
            if isinstance(data[i][j], int) and  0 < data[i][j]:
                exsit = 0
                for d in range(0,4):
                    exsit += count_bridges(data, i, j, d)
                # If there are fewer bridges than required, try adding more bridges
                if exsit < data[i][j]:
                    for d in range(0,4):
                        # If adding bridges is possible, recursively call solve_the_game
                        if calculate_temporary_bridge_count(data, i, j, d) > 1:
                            establish_bridge(data, i, j, d, 1)
                            if solve_the_game(data):
                                return True
                            establish_bridge(data, i, j, d, -1)
    # Restore original game data and return False if no solution is found
    data = [row[:] for row in data_tmp]
    return False

input_map = retrieve_game_data()
solve_the_game(input_map)