import os
os.remove("practice 6/file_handing/demofile.txt")

if os.path.exists("demofile.txt"):
  os.remove("practice 6/file_handing/demofile.txt")
else:
  print("The file does not exist")

