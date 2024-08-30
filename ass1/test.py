#!/usr/bin/python3
import numpy as np

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
    return np.array(grid)  # Convert to NumPy array

direction = [(0, -1), (-1, 0), (0, 1), (1, 0)]
maximum_bridge = 3

def check_valid_cell(data, i, j):
    n, m = data.shape
    return 0 <= i < n and 0 <= j < m

def count_bridges(data, i, j, d):
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    if not check_valid_cell(data, ni, nj):
        return 0
    bridge_index = data[ni, nj]
    if isinstance(bridge_index, int) and bridge_index > 0:
        return min(maximum_bridge, bridge_index)
    return 0

def calculate_temporary_bridge_count(data, i, j, d):
    bridge_index = count_bridges(data, i, j, d)
    if bridge_index == maximum_bridge:
        return 0
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    while check_valid_cell(data, ni, nj) and data[ni, nj] == bridge_index:
        ni += direction[d][0]
        nj += direction[d][1]
    if not check_valid_cell(data, ni, nj):
        return 0
    adjacent_bridge_sum = sum(count_bridges(data, ni, nj, nd) for nd in range(4))
    return min(maximum_bridge - bridge_index, data[ni, nj] - adjacent_bridge_sum)

def establish_bridge(data, i, j, d, num):
    bridge_index = count_bridges(data, i, j, d)
    new_bridge_index = bridge_index + num
    ni = i + direction[d][0]
    nj = j + direction[d][1]
    while check_valid_cell(data, ni, nj) and data[ni, nj] == bridge_index:
        data[ni, nj] = new_bridge_index
        ni += direction[d][0]
        nj += direction[d][1]

def append_confirmed_bridge(data):
    found = False
    n, m = data.shape
    for i in range(n):
        for j in range(m):
            if isinstance(data[i, j], int) and data[i, j] > 0:
                exsit = [count_bridges(data, i, j, d) for d in range(4)]
                potential = [calculate_temporary_bridge_count(data, i, j, d) for d in range(4)]
                if sum(potential) != 0:
                    if sum(potential) + sum(exsit) == data[i, j]:
                        found = True
                        for d in range(4):
                            establish_bridge(data, i, j, d, potential[d])
                    else:
                        remain_bn = data[i, j] - sum(exsit)
                        min_bridge = min(p for p in potential if p > 0)
                        min_bridge = min(min_bridge, remain_bn - 2) if sum(potential) + 2 >= data[i, j] else min_bridge
                        for d in range(4):
                            if potential[d] > 0:
                                establish_bridge(data, i, j, d, min_bridge)
    return found

def solve_the_game(data):
    data_tmp = data.copy()
    while True:
        if not append_confirmed_bridge(data):
            break
    correct_flag = True
    n, m = data.shape
    for i in range(n):
        for j in range(m):
            if isinstance(data[i, j], int) and data[i, j] > 0:
                exsit = sum(count_bridges(data, i, j, d) for d in range(4))
                if exsit != data[i, j]:
                    correct_flag = False
                    break
    if correct_flag:
        for row in data:
            print(''.join(str(chr(ord('a') + cell - 10) if isinstance(cell, int) and cell >= 10 else ' ' if cell == 0 else cell) for cell in row))
        return True

    for i in range(n):
        for j in range(m):
            if isinstance(data[i, j], int) and data[i, j] > 0:
                exsit = sum(count_bridges(data, i, j, d) for d in range(4))
                if exsit < data[i, j]:
                    for d in range(4):
                        if calculate_temporary_bridge_count(data, i, j, d) > 1:
                            establish_bridge(data, i, j, d, 1)
                            if solve_the_game(data):
                                return True
                            establish_bridge(data, i, j, d, -1)
    data[:] = data_tmp[:]
    return False

input_map = retrieve_game_data()
print(input_map)
solve_the_game(input_map)
