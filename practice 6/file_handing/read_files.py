f = open("practice 6/file_handing/demofile.txt")
print(f.read())

with open("practice 6/file_handing/demofile.txt") as f:
  print(f.read())

f = open("practice 6/file_handing/demofile.txt")
print(f.readline())
print(f.readline())
f.close()

with open("practice 6/file_handing/demofile.txt") as f:
  print(f.read(5))

with open("practice 6/file_handing/demofile.txt") as f:
    for x in f:
        print(x)