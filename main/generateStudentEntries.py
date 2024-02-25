import random

classes = list()

with open('classes.txt', 'r') as file:
    for line in file:
        classes.append(line.strip())

students = list()

for i in range(900):
    cls = classes.copy()
    first_choices = list()
    second_choices = list()
    for j in range(7):
        first_choice = random.sample(cls, 1)[0]
        second_choice = random.sample([i for i in cls if i != first_choice], 1)[0]
        cls.remove(first_choice)
        first_choices.append(first_choice)
        second_choices.append(second_choice)
    students.append((first_choices, second_choices))

with open("test_student_entries.txt", "w") as f:
    print(students, file=f)