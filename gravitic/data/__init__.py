""" 
Definitions of data blocks
"""

from gwpy.timeseries import TimeSeries
import pickle

class DetectorData:
    """
    This class is designed to help to fetch detector data for analysis.
    """

    def __init__(self, start, end):
        self.data = TimeSeries.fetch_open_data('H1', start, end)
