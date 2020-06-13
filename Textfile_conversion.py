my_file = open("textfile.txt")

all_the_lines = my_file.readlines()

items = []

for i in all_the_lines:
    items.append(i)
print(items)

new_items = [x[:-1] for x in items]
print(new_items)


import os
path = os.getcwd()
path = path + "/textfile.txt"

print path