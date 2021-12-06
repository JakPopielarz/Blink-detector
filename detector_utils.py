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
        self.signals = np.array([500]*len(self.y))
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



def thresholding_algo(y, lag, threshold, influence):
    signals = np.array([500]*len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1000
            else:
                signals[i] = 0

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])
        else:
            signals[i] = 500
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag+1):i+1])
            stdFilter[i] = np.std(filteredY[(i-lag+1):i+1])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))

class TestDetector2():
    def __init__(self, array, lag, threshold, influence):
        self.y = list(array)
        self.lag = lag
        self.threshold = threshold
        self.influence = influence
        self.signals = [0] * len(self.y)
        self.filteredY = np.array(self.y).tolist()
        self.avgFilter = [0] * len(self.y)
        self.stdFilter = [0] * len(self.y)
        self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
        self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()

    def thresholding_algo(self, new_values):
        self.y.append(new_values)
        i = len(self.y) - 1
        if i < self.lag:
            return 0
        elif i == self.lag:
            self.signals = [0] * len(self.y)
            self.filteredY = np.array(self.y).tolist()
            self.avgFilter = [0] * len(self.y)
            self.stdFilter = [0] * len(self.y)
            self.avgFilter[self.lag] = np.mean(self.y[0:self.lag]).tolist()
            self.stdFilter[self.lag] = np.std(self.y[0:self.lag]).tolist()
            return 0

        self.signals += [0]
        self.filteredY += [0]
        self.avgFilter += [0]
        self.stdFilter += [0]

        if abs(self.y[i] - self.avgFilter[i - 1]) > self.threshold * self.stdFilter[i - 1]:
            if self.y[i] > self.avgFilter[i - 1]:
                self.signals[i] = 1
            else:
                self.signals[i] = -1

            self.filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * self.filteredY[i - 1]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
        else:
            self.signals[i] = 0
            self.filteredY[i] = self.y[i]
            self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
            self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])

        return self.signals
