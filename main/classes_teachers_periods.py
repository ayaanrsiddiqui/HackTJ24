import random

classes = dict()
teachers = dict()
classrooms = list()

with open('classes.txt', 'r') as file:
    for line in file:
        classes[line.strip()] = list()

with open('teacherNames.txt', 'r') as file:
    for line in file:
        teachers[line.strip()] = list()

with open('classrooms.txt', 'r') as file:
    for line in file:
        classrooms.append(line.strip())

teachers_teaching_class = [list(teachers.keys())[i:i+3] for i in range(0, len(teachers), 3)]
for idx, cls in enumerate(classes):
    classes[cls] = teachers_teaching_class[idx]

for teacher in teachers:
    blue_day_periods = [1, 2, 3, 4]
    red_day_periods = [5, 6, 7]
    random.shuffle(blue_day_periods)
    random.shuffle(red_day_periods)
    for idx, period in enumerate(blue_day_periods):
        if idx < 3: teachers[teacher].append(period)
    for idx, period in enumerate(red_day_periods):
        if idx < 2: teachers[teacher].append(period)
    teachers[teacher].sort()

classes_teachers_periods = list()
idx = 0
for cls in classes:
    for teacher in classes[cls]:
        for period in teachers[teacher]:
            classes_teachers_periods.append(f"{cls}, {teacher}, Period {period}, Room {classrooms[idx]}")
        idx += 1

with open('classes_teachers_periods.txt', 'w') as f:
    print(classes_teachers_periods, file=f)