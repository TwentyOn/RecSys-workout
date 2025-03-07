from random import randrange

pref_matrix = [[randrange(0, 5) for _ in range(15)] for _ in range(15)]
PRODUCTS = {p: f'P{p + 1}' for p in range(len(pref_matrix))}

print(PRODUCTS)