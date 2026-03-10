from functools import reduce
n = [1, 2, 3, 4]
r = map(lambda x: x**2, n)
print(*list(r))

a = [1, 2, 3, 4, 5]
p = filter(lambda x: x % 2 == 0, a)
print(*list(p))

b = [1, 2, 3, 4, 5]
o = reduce(lambda q, w: q * w, b)
print(o)