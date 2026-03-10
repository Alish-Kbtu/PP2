a = ["apple", "pineapple", "banana", "orange"]
for x, y in enumerate(a):
    print(x+1, y)

names = ["Bob", "John", "Alice", "Tom"]
scores = [90, 85, 70, 55]
for x, y in zip(names, scores):
    print(x, y)