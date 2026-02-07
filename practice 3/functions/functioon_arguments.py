def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

def function(fname, lname):
  print(fname + " " + lname)

function("Emil", "Refsnes")

def Country(country = "Norway"):
  print("I am from", country)

Country("Sweden")
Country("India")
Country()
Country("Brazil")

def Pet(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

Pet(animal = "dog", name = "Buddy")

def Me(animal, name, age):
  print("I have a", age, "year old", animal, "named", name)

Me("dog", name = "Buddy", age = 5)