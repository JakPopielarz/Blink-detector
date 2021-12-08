import numpy as np

# adapted from https://stackoverflow.com/a/22640362/6029703 and https://gist.github.com/ximeg/587011a65d05f067a29ce9c22894d1d2

class Detector():
    def __init__(self, y_data, threshold):
        self.y = y_data
        self.threshold = threshold

        self.signals = [500]*len(y_data)

        self.filtered_y = np.array(y_data)
        self.mean_avg_filter = np.mean(self.filtered_y)
        self.mean_std_filter = np.std(self.filtered_y)

    def calibrate(self):
        self.filtered_y = np.array(self.y)
        
        self.mean_avg_filter = np.mean(self.filtered_y)
        self.mean_std_filter = np.std(self.filtered_y)

    def detect(self, number_of_new_points):
        self.signals += [0] * number_of_new_points
        while len(self.signals) > len(self.y):
            self.signals.pop(0)
    
        for i in range(len(self.y)-number_of_new_points, len(self.y)):
            if abs(self.y[i] - self.mean_avg_filter) > self.threshold * self.mean_std_filter:
                if self.y[i] > self.mean_avg_filter:
                    self.signals[i] = 1000
            else:
                self.signals[i] = 500

        return np.asarray(self.signals)
