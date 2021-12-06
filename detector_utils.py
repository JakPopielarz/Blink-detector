import numpy as np

# Implementation of algorithm from https://stackoverflow.com/a/22640362/6029703, adapted from https://gist.github.com/ximeg/587011a65d05f067a29ce9c22894d1d2

class Detector():
    def __init__(self, y_data, lag, threshold, influence):
        self.y = y_data
        self.lag = lag
        self.threshold = threshold
        self.influence = influence

        self.filtered_y = np.array(y_data)
        self.avg_filter = [0]*len(y_data)
        self.std_filter = [0]*len(y_data)
        self.avg_filter[self.lag - 1] = np.mean(y_data[0:self.lag])
        self.std_filter[self.lag - 1] = np.std(y_data[0:self.lag])
        self.signals = np.array([500]*len(y_data))

    def detect(self):
        # self.signals = np.array([500]*len(self.y))
        self.add_zero(self.signals)
        self.avg_filter = [0]*len(self.y)
        self.std_filter = [0]*len(self.y)
        self.avg_filter[self.lag - 1] = np.mean(self.y[0:self.lag])
        self.std_filter[self.lag - 1] = np.std(self.y[0:self.lag])
        self.filtered_y = np.array(self.y)

        for i in range(self.lag, len(self.y)):
            if abs(self.y[i] - self.avg_filter[i-1]) > self.threshold * self.std_filter [i-1]:
                if self.y[i] > self.avg_filter[i-1]:
                    self.signals[i] = 1000
                else:
                    self.signals[i] = 0

                self.filtered_y[i] = self.influence * self.y[i] + (1 - self.influence) * self.filtered_y[i-1]
                self.avg_filter[i] = np.mean(self.filtered_y[(i-self.lag+1):i+1])
                self.std_filter[i] = np.std(self.filtered_y[(i-self.lag+1):i+1])
            else:
                self.signals[i] = 500
                self.filtered_y[i] = self.y[i]
                self.avg_filter[i] = np.mean(self.filtered_y[(i-self.lag+1):i+1])
                self.std_filter[i] = np.std(self.filtered_y[(i-self.lag+1):i+1])

        return np.asarray(self.signals)

    def add_zero(self, array):
        array += [0]
        while len(array) > len(self.y):
            array.pop(0)

