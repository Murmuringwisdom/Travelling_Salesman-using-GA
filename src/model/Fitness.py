class Fitness:
    def __init__(self, path):
        self.path = path
        self.distance = 0
        self.fitness = 0.0

    def lengthPath(self):
        if self.distance == 0:
            path_length = 0
            for i in range(0, len(self.path)):
                from_city = self.path[i]
                if i + 1 < len(self.path):
                    to_city = self.path[i + 1]
                else:
                    to_city = self.path[0]
                path_length += from_city.distance(to_city)
            self.distance = path_length
        return self.distance

    def fitnessPath(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.lengthPath())
        return self.fitness
