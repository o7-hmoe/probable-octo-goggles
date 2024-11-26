import pandas as pd


class GrainReader:
    def __init__(self, csv_file_name="grains.csv", delimiter=","):
        self.sep = delimiter
        self.size_classes = pd.DataFrame
        self.get_grain_data(csv_file_name)

    def get_grain_data(self, csv_file_name):
        self.size_classes = pd.read_csv(csv_file_name,
                                        names=["classes", "size"],
                                        skiprows=[0],
                                        sep=self.sep,
                                        index_col=["classes"])