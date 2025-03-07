from collections import namedtuple
from math import sqrt
from random import randrange

pref_matrix = [[4, 2, 1, 1, 4, 1, 1, 0, 0, 0, 3, 2, 3, 1, 0],
               [4, 3, 4, 0, 3, 2, 1, 0, 3, 0, 0, 3, 4, 3, 4],
               [3, 4, 1, 1, 2, 2, 4, 2, 3, 0, 0, 2, 4, 3, 3],
               [2, 3, 0, 3, 4, 2, 2, 4, 4, 0, 1, 2, 3, 2, 0],
               [2, 2, 4, 4, 4, 4, 3, 0, 3, 0, 0, 3, 4, 2, 3],
               [2, 3, 1, 0, 2, 0, 2, 1, 3, 0, 0, 4, 3, 2, 1],
               [3, 2, 2, 1, 1, 2, 3, 1, 1, 0, 4, 2, 0, 4, 2],
               [3, 2, 4, 3, 4, 2, 0, 4, 3, 0, 1, 0, 1, 3, 1],
               [4, 1, 1, 0, 4, 1, 3, 4, 2, 0, 4, 0, 0, 2, 0],
               [0, 0, 1, 1, 0, 3, 0, 4, 3, 0, 4, 0, 1, 3, 1],
               [2, 3, 0, 2, 3, 3, 4, 2, 2, 0, 1, 2, 0, 3, 3],
               [4, 1, 2, 0, 3, 3, 2, 2, 4, 0, 0, 0, 1, 0, 1],
               [0, 4, 1, 1, 1, 1, 0, 2, 0, 0, 4, 1, 4, 0, 4],
               [3, 1, 3, 2, 0, 1, 2, 4, 3, 0, 1, 4, 3, 4, 4],
               [0, 4, 2, 2, 1, 2, 2, 4, 1, 0, 3, 2, 2, 4, 2]]
# pref_matrix = [[randrange(0, 5) for _ in range(15)] for _ in range(15)]
User = namedtuple('User', ['row', 'column'])
USERS = {i: f'U{i + 1}' for i in range(len(pref_matrix))}
PRODUCTS = {p: f'P{p + 1}' for p in range(len(pref_matrix))}
BORDER = 0.7  # порог отбора близких пользователей

print('Дана матрица предпочтений:')
print(*pref_matrix, sep='\n')


def del_user(matrix, user_id):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            if j not in user_id:
                row.append(matrix[i][j])
        if row:
            result.append(row)
    return result


def rebuilding_matrix(matrix, ignore_users):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            if j not in ignore_users:
                row.append(matrix[i][j])
        result.append(row)
    return result


def fill_vector():
    result_vector = {}
    for i in range(len(pref_matrix)):
        tagA = 'U' + str(i + 1)
        for j in range(len(pref_matrix[i])):
            result_vector.setdefault(tagA, []).append(pref_matrix[j][i])
    return result_vector


def result_user_vectors():
    result = {}
    for A in fill_vector():
        nom = 0
        denomA = 0
        denomB = 0
        for B in fill_vector():
            if A[1] != B[1]:
                for pair in zip(fill_vector()[A], fill_vector()[B]):
                    nom += (pair[0] * pair[1])
                    denomA += pair[0] ** 2
                    denomB += pair[1] ** 2
                if A + B and B + A not in result:
                    result[A + B] = (nom / (sqrt(denomA) * sqrt(denomB)))
    return result


print()
print('Пользователь А = U1')
del_users_ind = []
prudcts_rec_for_users = []

for i in range(len(pref_matrix)):
    for j in range(len(pref_matrix[i])):
        if j == 0 and pref_matrix[i][j] == 0:
            product_rec_for_user_A = User(i, j)  # запоминаем строку и столбец пользователя А
            prudcts_rec_for_users.append(product_rec_for_user_A)

for index, val in enumerate(pref_matrix[product_rec_for_user_A.row]):
    if val == 0 and index != product_rec_for_user_A.column:
        del_users_ind.append(index)

new_perf_matrix = del_user(pref_matrix,
                           del_users_ind)  # # редуцируем матрицу предпочтений, удаляем пользователей, у которых не оценен товар пользователя А

# print('Редуцированная матрица предпочтений:', *new_perf_matrix, sep='\n')

cosine_similarity = result_user_vectors()  # вычисляем косинусное подобие по оставшимся пользователям

cosine_similarity_matrix = [[0] * len(new_perf_matrix) for i in
                            range(len(new_perf_matrix))]  # создаём и заполняем матрицу ближайших пользователей
for key in cosine_similarity:
    i, j = (int(ind) - 1 for ind in key.replace('U', ' ').strip().split())
    cosine_similarity_matrix[i][j], cosine_similarity_matrix[j][i] = cosine_similarity[key], cosine_similarity[key]

close_users = set()  # заполняем и запоминаем близких пользователей
for i in range(len(cosine_similarity_matrix)):
    for j in range(len(cosine_similarity_matrix[i])):
        if cosine_similarity_matrix[i][j] >= BORDER:
            if i == 0 or j == 0 and (j, i) not in close_users and (i, j) not in close_users:
                close_users.add((i, j))
print('dsda', close_users)
new_cosine_similarity_matrix = del_user(cosine_similarity_matrix,
                                        del_users_ind)  # редуцируем матрицу косинусного подобия
cos_sim_pref_matrix = [
    [new_perf_matrix[i][j] for j in range(len(new_perf_matrix[i])) if j in (i[1] for i in close_users)] for i in
    range(len(new_perf_matrix))]  # матрица предпочтений по близким пользователям

print('Удаленные пользователи с неоценненным товаром пользователя А', [USERS[i] for i in del_users_ind])
# print('Косинусное сходство:', *cosine_similarity_matrix, sep='\n')
print('Порог отбора близких пользователей =', BORDER)

rating_A = [new_perf_matrix[i][j] for j in range(len(new_perf_matrix[i])) for i in range(len(new_perf_matrix)) if
            j == product_rec_for_user_A.column and pref_matrix[i][
                j] > 0]  # получаем оценки пользователя A по остальным продуктам
average_rating = sum(rating_A) / len(rating_A)  # средний рейтинг по другим товарам для пользователя А
print('Средний  рейтинг по товарам пользователя А', average_rating)
# print('близкие пользователи', close_users)
print()

print('Матрица предпочтений по близким пользователям к пользователю А:')
print('    ', *[USERS[u[1]] for u in sorted(close_users, key=lambda t: t[1])])
p_count = 1
for row in cos_sim_pref_matrix:
    print(f'P{p_count}'.ljust(3), row)
    p_count += 1

print()
print('Начало расчета прогнозируемой оценки для неоцененных товаров пользователя А...')
print('Средний рейтинг оцененных товаров пользователя А: Ra = ', average_rating)
print()
# цикл расчета рекомендаций по всем нулевым товарам пользователя А
for t in prudcts_rec_for_users:
    print(f'Неоценнный товар P{t.row + 1}')
    another_rating = [cos_sim_pref_matrix[i][j] for j in range(len(cos_sim_pref_matrix[i])) for i in
                      range(len(cos_sim_pref_matrix)) if
                      i == t.row and j != t.column and cos_sim_pref_matrix[i][
                          j] > 0]  # оценки данного продукта по другим пользователям
    another_average_rating = sum(another_rating) / len(
        another_rating)  # средний рейтинг других пользователей по неоцененному товару пользователя А

    print(f'Средний рейтинг товара P{t.row + 1} по остальным пользователям', another_average_rating)

    numerator = 0  # числитель формулы расчета прогнозируемой оценки - отклонение конкретная оценка пользователя U из близких пользователей для товара i от среднего рейтинга товара * весовой коэффициент кос.подобия
    sum_cosab = 0  # сумма весовых коэффициентов косинусного подобия хар-щая близость польз-ля с оценкой товара i к польз-лю А

    for j in range(len(new_cosine_similarity_matrix[0])):  # цикл для расчета вышеопределенных переменных
        numerator += (new_perf_matrix[t.row][j] - another_average_rating) * new_cosine_similarity_matrix[t.row][j]
        sum_cosab += cosine_similarity_matrix[t.row][j]

    Prai = average_rating + (numerator / sum_cosab)  # расчет прогнозируемой оценки

    print('Прогнозируемая оценка Prai =', Prai)
    if Prai > average_rating:
        print('Prai > Ra')
        print(f'Решение: рекомендовать пользователю {USERS[product_rec_for_user_A[1]]} товар P{t.row + 1}')
    else:
        print('Prai < Ra')
        print('Решение не рекомендовать пользователю товар')
    print()

max_average = (max(sum(a) / len(a) for a in pref_matrix))  # расчет максимального рейтинга товара
for i in range(len(pref_matrix)):  # цикл для поиска товара с максимальным рейтингом
    if sum(pref_matrix[i]) / len(pref_matrix[i]) == max_average:
        best_product = f'P{i + 1}'

no_rating_users = []

for i in range(len(pref_matrix)):  # цикл для поиска пользователей, которые не оценили ни один товар
    sum_row = 0
    for j in range(len(pref_matrix[i])):
        sum_row += pref_matrix[j][i]
    if sum_row == 0:
        no_rating_users.append(i)  # запоминаем индекс пользователя без рейтинга

if no_rating_users:
    print('Присутствуют пользователи без оцененных товаров:', *[f'U{u + 1}' for u in no_rating_users])
    print('Решение рекомендовать данным пользователям товар с максимальным рейтингом', best_product)
