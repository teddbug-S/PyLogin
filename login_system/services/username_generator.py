import random
from string import digits
import re

def generate_username(firstname, lastname, namelist):
    templates = [
        '{name}_{digit}',
        '{name}{digit}',
        '{name1}{digit}{name2}',
        '{name1}_{digit}{name2}',
        '{name1}{digit}_{name2}',
        '{name1}.{digit}_{name1}',
        '{name1}_{name2}.{digit}'
    ]
    mapping = {
        'name': random.choice(names := [firstname.lower(), lastname.lower()]),
        'digit': ''.join(random.sample(digits, random.randint(1, 4))),
        'name1': random.choice(names),
        'name2': random.choice(names)
    }

    def avoid_dup(username):
        for name in names:
           if len(re.findall(f'{name}', username)) >= 2:
               return False
        else:
            return True

    username = random.choice(templates).format_map(mapping)
    while not avoid_dup(username) and username not in namelist:
        username = generate_username(firstname, lastname, namelist)
    return username


def generate_names(firstname, lastname, namelist, count):
    usernames = []
    for _ in range(count):
        usernames.append(generate_username(firstname, lastname, namelist))
    return usernames
