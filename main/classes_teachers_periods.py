import random

classes = dict()
teachers = dict()
classrooms = list()

with open('classes.txt', 'r') as file:
    for line in file:
        classes[line.strip()] = list()

with open('teacherNamesUpdated.txt', 'r') as file:
    for line in file:
        teachers[line.strip()] = list()

with open('classrooms.txt', 'r') as file:
    for line in file:
        classrooms.append(line.strip())

teachers_teaching_class = [list(teachers.keys())[i:i+3] for i in range(0, len(teachers), 3)]
for idx, cls in enumerate(classes):
    classes[cls] = list(teachers.keys())[idx]

for i in range(2):
    periods = {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2}
    for teacher in teachers:
        pers = teachers[teacher] if teachers[teacher] else [1, 2, 3, 4, 5, 6, 7]
        planning_period = random.choice(list(set(list(periods.keys())) & set(pers)))
        periods[planning_period] -= 1
        if periods[planning_period] == 0: del periods[planning_period]
        teachers[teacher] = [i for i in pers if i != planning_period]

classes_teachers_periods = list()
idx = 0
for cls in classes:
    teacher = classes[cls]
    for period in teachers[teacher]:
        classes_teachers_periods.append(f"{cls}, {teacher}, Period {period}, Room {classrooms[idx]}")
    idx += 1

with open('main/classes_teachers_periods.txt', 'w') as f:
    print(classes_teachers_periods, file=f)