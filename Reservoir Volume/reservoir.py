import numpy as np
import os
import glob

def read_data(directory, fn_prefix, fn_suffix, ftype, delimiter):
    if directory.endswith("/") or directory.endswith("\\") is True:
        file_list = glob.glob(directory + "*." + ftype.strip("."))
    else:
        file_list = glob.glob(directory + "/*." + ftype.strip("."))
    file_content_dict = {}
    for file in file_list:
        raw_file_name = file.split("/")[-1].split("\\")[-1].split(".csv")[0]
        try:
            int(raw_file_name.strip(fn_prefix).strip(fn_suffix))
        except ValueError:
            dict_key = raw_file_name.strip(fn_prefix).strip(fn_suffix)
        with open(file, mode="r") as f:
            f_content = f.read()
            rows = f_content.strip("\n").split("\n").__len__()
            cols = f_content.strip("\n").split("\n")[0].strip(delimiter).split(delimiter).__len__()
            data_array = np.empty((rows, cols), dtype=np.float32)
            for iteration, line in enumerate(f_content.strip("\n").split("\n")):
                line_data = []
                for e in line.strip(delimiter).split(delimiter):
                    try:
                        line_data.append(np.float32(e))
                    except ValueError:
                        line_data.append(np.nan)
                data_array[iteration] = np.array(line_data)
        file_content_dict.update({dict_key: data_array})
    return file_content_dict

if __name__ == "__main__":
    # LOAD DATA
    file_directory = os.path.abspath("") + "\\flows\\"
    daily_flow_dict = read_data(directory=file_directory, ftype="csv",
                                fn_prefix="daily_flows_", fn_suffix="",
                                delimiter=";")
    print(daily_flow_dict[1995])