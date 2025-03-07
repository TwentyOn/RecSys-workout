from math import sqrt
from random import randrange

pref_matrix = [[4, 3, 1, 0, 0, 1, 2, 2, 4, 2, 2, 2, 3, 3, 1],
               [4, 0, 3, 4, 3, 0, 1, 4, 1, 2, 1, 1, 2, 2, 3],
               [3, 2, 0, 4, 1, 0, 3, 0, 0, 4, 4, 0, 3, 0, 3],
               [1, 0, 1, 3, 4, 1, 3, 0, 3, 2, 4, 0, 1, 2, 1],
               [0, 4, 1, 0, 3, 0, 0, 0, 3, 1, 4, 0, 1, 1, 2],
               [2, 1, 3, 2, 2, 3, 0, 4, 3, 0, 4, 1, 2, 4, 2],
               [1, 4, 1, 4, 1, 0, 4, 0, 3, 3, 1, 4, 2, 0, 3],
               [4, 1, 1, 4, 2, 3, 3, 0, 3, 4, 2, 3, 3, 3, 3],
               [1, 1, 4, 4, 2, 3, 2, 4, 0, 1, 3, 4, 4, 0, 0],
               [3, 2, 3, 0, 1, 4, 1, 1, 4, 4, 4, 4, 0, 1, 1],
               [3, 4, 1, 0, 4, 0, 0, 3, 3, 4, 1, 2, 2, 3, 3],
               [3, 3, 0, 0, 2, 1, 4, 2, 2, 2, 4, 4, 2, 3, 3],
               [1, 3, 2, 3, 1, 2, 1, 2, 3, 2, 3, 1, 4, 1, 1],
               [0, 1, 2, 4, 2, 0, 4, 3, 0, 4, 4, 0, 0, 4, 2],
               [2, 1, 3, 0, 4, 0, 3, 3, 1, 2, 0, 4, 2, 0, 3]]
# pref_matrix = [[randrange(0, 5) for _ in range(15)] for _ in range(15)]
USERS = {i: f'U{i + 1}' for i in range(len(pref_matrix))}
PRODUCTS = {p: f'P{p + 1}' for p in range(len(pref_matrix))}
BORDER = 0.7  # порог отбора близких товаров


def show_matrix(matrix, rows, cols):
    print('   ', *cols.values())
    for i in range(len(matrix)):
        print(list(rows.values())[i].ljust(3), matrix[i])
    print()


print('Дана матрица предпочтений:')
show_matrix(pref_matrix, rows=PRODUCTS, cols=USERS)


def del_product(matrix, product_id):
    result = []
    for i in range(len(matrix)):
        if i in product_id:
            result.append(matrix[i])
    return result


def rebuilding_matrix(matrix, ignore_products):
    result = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix[i])):
            if j not in ignore_products:
                row.append(matrix[i][j])
        result.append(row)
    return result


def fill_vector():
    result_vector = {}
    for i in range(len(pref_matrix)):
        tagA = 'P' + str(i + 1)
        for j in range(len(pref_matrix[i])):
            result_vector.setdefault(tagA, []).append(pref_matrix[i][j])
    return result_vector


def result_product_vectors():
    result = {}
    for A in fill_vector():
        nom = 0
        denomA = 0
        denomB = 0
        for B in fill_vector():
            if A[1:] != B[1:]:
                for pair in zip(fill_vector()[A], fill_vector()[B]):
                    nom += (pair[0] * pair[1])
                    denomA += pair[0] ** 2
                    denomB += pair[1] ** 2
                if A + B and B + A not in result:
                    result[A + B] = (nom / (sqrt(denomA) * sqrt(denomB)))
    return result


cosine_similarity = result_product_vectors()  # косинусное сходство по продуктам

cosine_similarity_matrix = [[0] * len(pref_matrix) for i in
                            range(len(pref_matrix))]  # создаём ближайших пользователей
for key in cosine_similarity:  # заполняем матрицу ближайших пользователей
    i, j = (int(ind) - 1 for ind in key.replace('P', ' ').strip().split())
    cosine_similarity_matrix[i][j], cosine_similarity_matrix[j][i] = cosine_similarity[key], cosine_similarity[key]
# print('Косинусное сходство по продуктам:')
# show_matrix(cosine_similarity_matrix, rows=PRODUCTS, cols=PRODUCTS)

close_products = set()  # заполняем и запоминаем близких пользователей
for i in range(len(cosine_similarity_matrix)):
    for j in range(len(cosine_similarity_matrix[i])):
        if cosine_similarity_matrix[i][j] >= BORDER:
            if (j, i) not in close_products and (i, j) not in close_products:
                close_products.add((i, j))

close_products_pref_matrix = del_product(pref_matrix, [i[1] for i in
                                                       close_products])  # Усеченная матрица предпочтений наиболее близких товаров
close_products_cosine_similatiry = del_product(cosine_similarity_matrix, [i[1] for i in
                                                                          close_products])  # усеченная матрица косинусного сходства

racos = 0  # произведение суммы оценок на косинусное подобие из матрицы близких товаров
for i in range(len(close_products_pref_matrix)):
    if 0 in close_products_pref_matrix[i]:
        multisumma = 0  # Сумма произведений оценок товара к косинусному сходству товаров
        sum_cos_i_j = 0  # Сумма косинусных сходств
        user_ind = close_products_pref_matrix[i].index(0)  # индекс пользователя с 0-м рейтингом товара
        target = PRODUCTS[list(close_products)[i][1]]  # тег товара с 0-м рейтингом
        print(f'Расчет для пользователя: [{USERS[user_ind]}]. Неоцененный продукт:', [target])
        for j in range(len(close_products_pref_matrix)):
            if close_products_pref_matrix[j][user_ind] != 0:
                rating = close_products_pref_matrix[j][user_ind]
                # print(PRODUCTS[list(close_products)[i][1]], PRODUCTS[list(close_products)[j][1]])
                if PRODUCTS[list(close_products)[i][1]] != PRODUCTS[list(close_products)[j][1]]:
                    try:
                        cos_i_j = cosine_similarity[
                            PRODUCTS[list(close_products)[i][1]] + PRODUCTS[list(close_products)[j][1]]]
                    except:
                        cos_i_j = cosine_similarity[
                            PRODUCTS[list(close_products)[j][1]] + PRODUCTS[list(close_products)[i][1]]]
                    multisumma += rating * cos_i_j
                    sum_cos_i_j += cos_i_j
        # print(f'Сумма произведений для продукта {target}: {multisumma}')
        # print(f'Сумма косинусов для продукта {target}: {sum_cos_i_j}')
        Prai = multisumma / sum_cos_i_j  # возможная оценка пользователя неоцененному товару
        print(f'Возможная оценка [Prai] пользователя неоцененному товару [{target}]: {multisumma / sum_cos_i_j}')
        if Prai > 3:
            print(f'Prai > 3. Решение: пользователю [{USERS[user_ind]}] рекомендовать продукт [{target}]')
        else:
            print(f'Prai < 3. Решение: пользователю [{USERS[user_ind]}] не рекомендовать продукт [{target}]')
        print()

    # print('sum', sum(close_products_pref_matrix[i][j] for i in
    #           range(len(close_products_pref_matrix)) for j in range(len(close_products_pref_matrix[i])) if j == user_ind))
