# https://jinja.palletsprojects.com/en/3.1.x/
from string import Template

message = Template("$first_name zjadl dzis $count paczkow")

info = [
    ("Adam", 10),
    ("Kacper", 20)
]
for first_name, count in info:
    text = message.substitute(first_name=first_name, count=count)
    print(text)