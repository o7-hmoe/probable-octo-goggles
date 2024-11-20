import pandas as pd


class HecSet:
    def __init__(self, xlsx_file_name="output.xlsx"):
        self.hec_data = pd.DataFrame
        self.get_hec_data(xlsx_file_name)

    def get_hec_data(self, xlsx_file_name):
        self.hec_data = pd.read_excel(xlsx_file_name,
                                     skiprows=[1],
                                     header=[0])