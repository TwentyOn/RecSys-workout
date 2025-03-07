import sys

# методы хранения матриц предпочтений

"""matrix = [[0, 0.95, 0.9, 0.85, 0.8],
          [0, 0, 0.75, 0.7, 0.65],
          [0, 0, 0, 0.6, 0.8],
          [0, 0, 0, 0, 0.7],
          [0, 0, 0, 0, 0]]"""

matrix = [[0, 0.88, 0.93, 0.87, 0.87],
          [0, 0, 0.88, 0.85, 0.86],
          [0, 0, 0, 0.88, 0.86],
          [0, 0, 0, 0, 0.83],
          [0, 0, 0, 0, 0]]

users = {0: 'U1', 1: 'U2', 2: 'U3', 3: 'U4', 4: 'U5'}
r = 0.85
union_users = ['U1']


def maximum_and_index(matrix):
    maximum, ind = 0, tuple()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] > maximum:
                maximum, ind = matrix[i][j], (i, j)
    return maximum, ind


def del_user(matrix, user_id):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            if i != user_id[1] and j != user_id[1]:
                row.append(matrix[i][j])
        if row:
            result.append(row)
    return result


def rebuilding_users(users_dict, user_index):
    del users_dict[user_index]
    result = {}
    key = 0
    for value in users_dict.values():
        result[key] = value
        key += 1
    return result


def show_matrix(matrix):
    print()
    for i in range(len(matrix)):
        print(matrix[i])
    print()

count_iteration = 1
while True:
    if maximum_and_index(matrix)[0] >= r:
        maximum, ind_max = maximum_and_index(matrix)
        matrix = del_user(matrix, ind_max)
        print(f'Итерация {count_iteration}. Перестройка матрицы расстояний:')
        print(f'{union_users[-1]} и {users[ind_max[1]]} объединены по расстоянию {maximum} >= R = {r}')
        count_iteration += 1
        union_users.append(f'({union_users[-1]}, {users[ind_max[1]]})')
        users = rebuilding_users(users, ind_max[1])
        show_matrix(matrix)
        print('-' * 50)
    else:
        print('-' * 50, 'Завершено', sep='\n')
        break
