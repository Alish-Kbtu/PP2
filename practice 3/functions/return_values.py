def my_function(*kids):
  print("The youngest child is " + kids[2])

my_function("Emil", "Tobias", "Linus")

def function(*args):
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

function("Emil", "Tobias", "Linus")

def unction(greeting, *names):
  for name in names:
    print(greeting, name)

unction("Hello", "Emil", "Tobias", "Linus")

def nction(*numbers):
  total = 0
  for num in numbers:
    total += num
  return total

print(nction(1, 2, 3))
print(nction(10, 20, 30, 40))
print(nction(5))

def Max(*numbers):
  if len(numbers) == 0:
    return None
  max_num = numbers[0]
  for num in numbers:
    if num > max_num:
      max_num = num
  return max_num

print(Max(3, 7, 2, 9, 1))

def ction(**kid):
  print("His first name is " + kid["fname"])
  print("His last name is " + kid["lname"])

ction(fname = "Tobias", lname = "Refsnes")

def tion(**myvar):
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

tion(name = "Tobias", age = 30, city = "Bergen")

def ion(username, **details):
  print("Username:", username)
  print("Additional details:")
  for key, value in details.items():
    print(" ", key + ":", value)

ion("emil123", age = 25, city = "Oslo", hobby = "coding")