a = int(input())
def squr(n):
    for i in range(n + 1):
        yield str(i ** 2)
print(",".join(squr(a)))

def even(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield str(i)
print(",".join(even(a)))

b = int(input())
def twelve(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield str(i)
print(",".join(twelve(b)))

c, d = map(int, input().split())
def squares(c, d):
    for i in range(c, d + 1):
        yield str(i ** 2)
print(",".join(squares(c, d)))

e = int(input())
def down(n):
    while n >= 0:
        yield str(n)
        n -= 1
print(",".join(down(e)))