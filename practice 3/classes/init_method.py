class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Person("Emil", 36)
print(p1.name)
print(p1.age)

class Perso:
  pass
p1 = Perso()
p1.name = "Tobias"
p1.age = 25
print(p1.name)
print(p1.age)

class Pers:
  def __init__(self, name, age):
    self.name = name
    self.age = age
p1 = Pers("Linus", 28)
print(p1.name)
print(p1.age)

class Per:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age
p1 = Per("Emil")
p2 = Per("Tobias", 25)
print(p1.name, p1.age)
print(p2.name, p2.age)

class Pe:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country
p1 = Pe("Linus", 30, "Oslo", "Norway")
print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)