import numpy as np

# adapted from https://stackoverflow.com/a/22640362/6029703 and https://gist.github.com/ximeg/587011a65d05f067a29ce9c22894d1d2

class Detector():
    """
    Signal analyzer class. It's supposed to operate in near-real-time and detect
    peaks in the passed data.
    """
    def __init__(self, y_data, threshold):
        """
        Initialize Detector object.

        Parameters
        ----------
        y_data : list of int
            Array of data points to be analyzed. 
        threshold : int
            Multiple of standard deviation above signal mean. Any data point
            above this threshold will be considered a peak.
        """
        self.y = y_data
        self.threshold = threshold

        # signals is a list of detection results. If value is 500, nothing was detected.
        # If value is larger than 500, a peak was detected.
        self.signals = [500]*len(y_data)

        # set of parameters used to detect peaks
        self.filtered_y = np.array(y_data)
        self.mean_avg_filter = np.mean(self.filtered_y)
        self.mean_std_filter = np.std(self.filtered_y)

        # parameters used during calibration - list and flag.
        self.calibration_y = []
        self.calibrating = False
        self.border = -100

    def gather_calibration_data(self, gathering_method):
        """
        Save data to a list. This list's intended use is calibration only.

        This method will repeatedly call gathering_method (while calibrating flag is true) and
        save what it returns to the calibration data list.

        Parameters
        ----------
        gathering_method : function returning list of int
        """
        while self.calibrating:
            gathered_data = gathering_method()
            # filter the list returned by gathering_method, so that it only contains 
            # values bigger than or equal 0
            gathered_data = list(filter(lambda x: (x >= 0), gathered_data))
            # add the filtered data to calibration dataset
            self.calibration_y += gathered_data
    
    def calibrate(self):
        """
        Calculate mean and standard deviation based on data gathered during calibration.
        """
        self.filtered_y = np.array(self.calibration_y)
        
        # calculate mean and standard deviation
        self.mean_avg_filter = np.mean(self.filtered_y)
        self.mean_std_filter = np.std(self.filtered_y)

        # clear the calibration array - no need to waste space
        self.calibration_y = []
        # calculate the actual threshold of peak detection - mean + standard deviation * specified multiple
        self.border = self.threshold*self.mean_std_filter+self.mean_avg_filter

    def detect(self, number_of_new_points):
        """
        Analyze the signal to check if a peak was present.

        Parameters
        ----------
        number_of_new_points : int
            Number of points which have been added to data point array since last analysis.
        
        Returns
        ------
        list of int
            Array containing current detection results for the whole data point array.
        """

        # add new data points to result array
        self.signals += [500] * number_of_new_points
        # only a specified number of points can be in the data point array, so detection results 
        # should always have the same length - new points have been added at the end, so delete
        # oldest points, from the front
        while len(self.signals) > len(self.y):
            self.signals.pop(0)
    
        # there's no need to iterate through the whole data point array - the old points have been checked already
        # therefor iterate only through the part with new points (added since last analysis)
        for i in range(len(self.y)-number_of_new_points, len(self.y)):
            if abs(self.y[i] - self.mean_avg_filter) > self.threshold * self.mean_std_filter:
                # if point value exceeds the border value ("upwards")
                if self.y[i] > self.mean_avg_filter:
                    # set the correct point in results to a "high" value
                    self.signals[i] = 1000
            else:
                # else set it to "normal" value
                self.signals[i] = 500

        return np.asarray(self.signals)
