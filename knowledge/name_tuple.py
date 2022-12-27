from collections import namedtuple

User = namedtuple("Usser", "name surname")
adam = User("Adam", "Grenda")

print(adam.name)
print(adam[1])

# adam.name = "Seba" # niemodyfikowalne