import logging
import os
from fun import *
from grains import GrainReader
from hec import *
from mpm import *


def get_char_grain_size(file_name=str, D_char=str):
    grain_info = GrainReader(file_name)
    return grain_info.size_classes["size"][D_char]


def calculate_mpm(hec_df, D_char):
    # create dictionary with relevant information about bed load transport with void lists
    mpm_dict = {
            "River Sta": [],
            "Scenario": [],
            "Q (m3/s)": [],
            "Phi (-)": [],
            "Qb (kg/s)": []
    }

    # extract relevant hydraulic data from HEC-RAS output file
    Froude = hec_df["Froude # Chl"]
    h = hec_df["Hydr Depth"]
    Q = hec_df["Q Total"]
    Rh = hec_df["Hydr Radius"]
    Se = hec_df["E.G. Slope"]
    u = hec_df["Vel Chnl"]

    for i, sta in enumerate(list(hec_df["River Sta"])):
        if not str(sta).lower() == "nan":
            logging.info("PROCESSING PROFILE {0} FOR SCENARIO {1}".format(str(hec_df["River Sta"][i]), str(hec_df["Profile"][i])))
            mpm_dict["River Sta"].append(hec_df["River Sta"][i])
            mpm_dict["Scenario"].append(hec_df["Profile"][i])
            section_mpm = MPM(grain_size=D_char,
                              Froude=Froude[i],
                              water_depth=h[i],
                              velocity=u[i],
                              Q=Q[i],
                              hydraulic_radius=Rh[i],
                              slope=Se[i])
            mpm_dict["Q (m3/s)"].append(Q[i])
            mpm_dict["Phi (-)"].append(section_mpm.phi)
            b = hec_df["Flow Area"][i] / h[i]
            mpm_dict["Qb (kg/s)"].append(section_mpm.add_dimensions(b))
    return pd.DataFrame(mpm_dict)


def main():
    pass


@log_actions
def main():
    # get characteristic grain size = D84
    print(os.path.abspath("../.."))
    D_char = get_char_grain_size(file_name=os.path.abspath("../..") + "\\grains.csv",
                                 D_char="D84")
    hec_file = os.path.abspath("../..") + "\\HEC-RAS\\output.xlsx"
    hec = HecSet(hec_file)
    logging.info(hec.hec_data.head())

    mpm_results = calculate_mpm(hec.hec_data, D_char)
    mpm_results.to_excel(os.path.abspath("../..") + "\\bed_load_mpm.xlsx")


if __name__ == '__main__':
    main()
