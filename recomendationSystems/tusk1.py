from math import sqrt

pref_matrix = [[5, 4, 5, 3, 5],
               [5, 5, 5, 3, 5],
               [5, 4, 4, 2, 5],
               [5, 3, 5, 0, 3],
               [5, 0, 5, 0, 0],
               [4, 5, 5, 3, 1]]

print('Дана матрица предпочтений:')
print()
print('   ', 'u1', 'u2', 'u3', 'u4', 'u5')
for row in range(len(pref_matrix)):
    print('p' + str(row + 1), pref_matrix[row])
print()


def fill_vector(criteries):
    result_vector = {}
    if criteries == 'u':
        for i in range(5):
            tagA = 'U' + str(i + 1)
            for j in range(6):
                result_vector.setdefault(tagA, []).append(pref_matrix[j][i])
        return result_vector
    elif criteries == 'p':
        for i in range(6):
            tagA = 'P' + str(i + 1)
            for j in range(5):
                result_vector.setdefault(tagA, []).append(pref_matrix[i][j])
        return result_vector


vectors = {'u': fill_vector('u'), 'p': fill_vector('p')}


def result_user_product_vectors():
    product_and_user_vectors = []
    for c in ['u', 'p']:
        result = {}
        for A in fill_vector(c):
            nom = 0
            denomA = 0
            denomB = 0
            for B in fill_vector(c):
                if A[1] != B[1]:
                    for pair in zip(vectors[c][A], vectors[c][B]):
                        nom += (pair[0] * pair[1])
                        denomA += pair[0] ** 2
                        denomB += pair[1] ** 2
                    # print(A + B, nom, sqrt(denomA), sqrt(denomB), nom / (sqrt(denomA) * sqrt(denomB)))
                    result[A + B] = (nom / (sqrt(denomA) * sqrt(denomB)))
        product_and_user_vectors.append(result)
    return product_and_user_vectors


print('Общее косинусное подобие по пользователям:', result_user_product_vectors()[0])
print()
print('Общее косинусное подобие по продуктам:', result_user_product_vectors()[1])
print()

close_user = max(result_user_product_vectors()[0].items(), key=lambda x: x[1])
close_product = max(result_user_product_vectors()[1].items(), key=lambda x: x[1])
print(
    f'Наиболее близкими пользователями являются пользователи {close_user[0][:2]} и {close_user[0][2:]} со значением векторного подобия = {close_user[1]}')
print(
    f'Наиболее близкими продуктами являются продукты {close_product[0][:2]} и {close_product[0][2:]} со значением векторного подобия = {close_product[1]}')

for row in result_user_product_vectors()[0].items():
    print(row)