from collections import defaultdict

matrix = [[1, 0, 0, 0, 2, 0],
          [0, 0, 3, 4, 0, 0],
          [0, 0, 0, 0, 0, 0],
          [0, 0, 0, 8, 0, 5],
          [0, 0, 0, 0, 0, 0],
          [0, 7, 1, 0, 0, 6]]

pref_matrix = [[5, 4, 5, 0, 5],
               [5, 5, 5, 0, 5],
               [5, 4, 4, 0, 5],
               [4, 3, 4, 0, 3],
               [0, 0, 0, 0, 0],
               [4, 5, 5, 0, 1]]

result = {}
n, m = len(matrix), len(matrix[1])  # размерность матрицы


def format_1():
    value = [matrix[i][j] for i in range(n) for j in range(m) if matrix[i][j]]  # список ненулевых значений
    row = [i for i in range(n) for j in range(m) if matrix[i][j]]  # строка значения
    col = [j for i in range(n) for j in range(m) if matrix[i][j]]  # колонка значения
    result = {'value': value, 'row': row, 'col': col}
    return result


def format_2():
    value = [matrix[i][j] for i in range(n) for j in range(m) if matrix[i][j]]
    col = [j for i in range(n) for j in range(m) if matrix[i][j]]
    RowIndex = [0]
    for i in range(n):
        amount = sum(map(lambda x: 1 if x > 0 else 0, matrix[i]))  # подсчет кол-ва значений > 0
        RowIndex.append(RowIndex[-1] + amount)
    result = {'value': value, 'col': col, 'RowIndex': RowIndex}
    return result


def format_3():
    num_amout = len(max([list(filter(lambda x: x > 0, [matrix[i][j] for j in range(m)])) for i in range(n)],
                        key=len))  # максимальная размерность строки с исключенными нулевыми значениями
    value, column = [], []
    # цикл поиска и добавления значений > 0
    for i in range(n):
        val, col = [], []
        for j in range(m):
            if matrix[i][j]:
                val.append(matrix[i][j]), col.append(j)
        if len(val) < num_amout:
            for amount in range(num_amout - len(val)):
                val.append(0)
        if len(col) < num_amout:
            for amount in range(num_amout - len(col)):
                col.append(0)
        value.append(val), column.append(col)

    result = {'value': value, 'column': column}
    return result


def format_4():
    result = []
    dels_items = []  # список, в который добавляются удаленные продукты/пользователи

    dels_users = defaultdict(int)  # ведение подсчета нулевых оценок пользователя
    dels_products = defaultdict(int)  # ведение подсчета нулевых оценок продукта
    for i in range(len(pref_matrix)):
        row = []
        R = 3.5
        for j in range(len(pref_matrix[i])):
            # если значение не нулевое и строка не удалена
            if pref_matrix[i][j] and i not in [p for p in range(6) if sum(pref_matrix[p]) / len(pref_matrix[p]) < R]:
                row.append(pref_matrix[i][j])  # добавляем значение в результирующую матрицу
            else:  # иначе увеличиваем счетчик пустого рейтинга для пользователя/продукта
                dels_products[i] += 1
                dels_users[j] += 1
                if dels_products[i] == 5:
                    dels_items.append(f'P{j + 1}')
                if dels_users[j] == 6:
                    dels_items.append(f'U{j + 1}')

        if row:
            result.append(row)

    dels_items.extend([f'P{p + 1}' for p in range(6) if sum(pref_matrix[p]) / len(
        pref_matrix[p]) < R])  # расширяем список игнорируемых продуктов, продуктами где рейтинг < R = 3.5
    return result, dels_items


def show_result(format):
    if type(format) == dict:
        for mark in format:
            if len(format) == 3:
                print(f'{mark}: {format[mark]}')
            else:
                print(f'{mark} matrix')
                for row in format[mark]:
                    print(row)
                print('-' * len(mark + 'matrix'))
    else:
        print('Матрица предпочтений 0', '', sep='\n')
        p_title, u_title = ['P' + str(i) for i in range(1, 7)], ['U' + str(i) for i in range(1, 6)]
        print('   ', *u_title)
        for i in range(len(pref_matrix)):
            print(p_title[i], pref_matrix[i])
        print('-' * 20)
        print('Матрица предпочтений 1', '', sep='\n')
        p_title = ['P' + str(i) for i in range(1, 6) if 'P' + str(i) not in format[1]]
        print('    ', end='')
        for u_title in ['U' + str(i) for i in range(1, 6) if 'U' + str(i) not in format[1]]:
            print(u_title, end=' ')
        print()
        for i in range(len(format[0])):
            print(p_title[i], format[0][i])


print('Формат хранения 1', '', sep='\n')
show_result(format_1())
print('-' * 35)
print('Формат хранения 2', '', sep='\n')
show_result(format_2())
print('-' * 35)
print('Формат хранения 3', '', sep='\n')
show_result(format_3())
print('-' * 35)
print('Формат хранения 4', '', sep='\n')
show_result(format_4())
