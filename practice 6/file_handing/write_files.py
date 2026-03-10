with open("practice 6/file_handing/demofile.txt", "a") as f:
  f.write("Now the file has more content!")
with open("practice 6/file_handing/demofile.txt") as f:
  print(f.read())

with open("practice 6/file_handing/demofile.txt", "w") as f:
  f.write("Woops! I have deleted the content!")
with open("practice 6/file_handing/demofile.txt") as f:
  print(f.read())

  f = open("MyFile", "x")