class Teacher():
    def __init__(self,name,room_number,periods):
        self.name = name
        self.room_number = room_number
        self.periods = periods #periods teaching
class Class():
    def __init__(self,name,number,maxcapacity,is_required):
        self.name = name
        self.number = number
        self.max_capacity = maxcapacity
        self.students = []
        self.is_required = is_required
class DesiredSchedule():
    def __init__(self,wants,secondary):
        self.wants = wants
        self.secondary = secondary

    def dist(self,otherSchedule):
        out = 0
        for i in otherSchedule:
            if i in self.wants:
                out += 1
            elif i in self.secondary:
                out += 0.5
            else:
                out += 0
        return out


def cost(currentSchedule,desiredSchedule,distMatrix):
    cost = 0
    for i in currentSchedule:
        cost += desiredSchedule.dist(currentSchedule)
    for i in range(len(currentSchedule)-1):
        cost += distMatrix[currentSchedule[i]][currentSchedule[i+1]]
    return cost
