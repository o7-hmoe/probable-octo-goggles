import glob
import os
import numpy as np
from scipy.signal import argrelextrema
from scipy.signal import find_peaks

def plot_storage_curve(array_1d, min_indices, max_indices, min_values, max_values):
    """
    Plots SD_line (1d-numpy array) and markers of local maxima and minima
    :param array_1d: np.array (1xn) of the SD line
    :param min_indices: np.array (1xi) of indices (positions in SD line array) of local maxima
    :param max_indices: np.array (1xj) of indices (positions in SD line array) of local minima
    :param min_values: np.array (1xi) of values (of SD line array) of local maxima
    :param max_values: np.array (1xj) of values (of SD line array) of local maxima
    :return: show and save plot in script directory as SD_curve.png
    """
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as font_manager
    # set font properties
    hfont = {'family': 'normal',
             'weight': 'normal',
             'size': 10,
             'style': 'normal',
             'fontname': 'Arial'}
    font = font_manager.FontProperties(family=hfont['fontname'],
                                       weight=hfont['weight'],
                                       style=hfont['style'],
                                       size=hfont['size'])
    # create plot
    x_values = list(range(1, array_1d.size + 1))
    fig = plt.figure(figsize=(6, 3), dpi=150, facecolor='w', edgecolor='k')
    axe = fig.add_subplot(1, 1, 1)
    axe.plot(x_values, array_1d, linestyle='-', color="slategrey", label='storage line')

    # plot extrema
    axe.plot(min_indices, min_values, linestyle="None", color="darkred",
             marker="v", markersize=4, label='Local minima')
    axe.plot(max_indices, max_values, linestyle="None", color="limegreen",
             marker="^", markersize=4, label='Local maxima')

    # Define axis labels and legend
    axe.set_xlabel("time (months)", **hfont)
    axe.set_ylabel("storage volume (million m³)", **hfont)
    axe.legend(loc='upper left', prop=font, facecolor='w', edgecolor='gray', framealpha=1, fancybox=0)

    # Set grid
    axe.grid(color='gray', linestyle='-', linewidth=0.2)
    axe.set_ylim((0, int(np.nanmax(array_1d) * 1.1)))
    axe.set_xlim((0, array_1d.size + 1))

    # Output plot
    plt.savefig("storage_curve.png", bbox_inches='tight')
    plt.show()


def read_data(directory="", fn_prefix="", fn_suffix="", ftype="csv", delimiter=";"):
    """
    The function reads flows from files and converts to a dictionary.
    :param directory:
    :param fn_prefix:
    :param fn_suffix:
    :param ftype:
    :param delimiter:
    :return:
    """

    if directory.endswith("/") or directory.endswith("\\"):
        file_list = glob.glob(directory + "*." + ftype.strip("."))
    else:
        file_list = glob.glob(directory + "/*." + ftype.strip("."))

    file_content_dict = {}

    for file in file_list:
        # generate key for dictionary entry
        raw_file_name = file.split("/")[-1].split("\\")[-1].split(".csv")[0]

        try:
            dict_key = int(raw_file_name.strip(fn_prefix).strip(fn_suffix))
        except ValueError:
            dict_key = raw_file_name.strip(fn_prefix).strip(fn_suffix)

        # read file contents
        with open(file, mode="r") as f:
            f_content = f.read()
            rows = f_content.strip("\n").split("\n").__len__()  # strips new lines then determines length
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


def daily2monthly(daily_flow_series):
    daily_flow_series = np.transpose(daily_flow_series)  # easier to iterative 12 x 31 than 31 x 12
    monthly_stats = []
    for daily_flows_per_month in daily_flow_series:
        monthly_stats.append(np.nansum(daily_flows_per_month * 24 * 3600) / 10**6)
    return np.array(monthly_stats)


def sequent_peak(in_vol_series, out_vol_target):
    # create storage-difference SD dictionary
    SD_dict = {}

    for year, monthly_volume in in_vol_series.items():
        # add a new dictionary entry for every year
        SD_dict.update({year: []})
        for month_no, in_vol in enumerate(monthly_volume):
            # append one list entry per month (i.e., In_m - Out_m)
            SD_dict[year].append(in_vol - out_vol_target[month_no])

    SD_line = []
    for year in SD_dict.keys():
        for vol in SD_dict[year]:
            SD_line.append(vol)

    storage_line = np.cumsum(SD_line)

    # Find local maxima and minima using find_peaks
    # Find_peaks returns two outputs, indicies and properties. Here we use , _ to ignore the properties
    # returned by the find_peaks function.
    max_indices, _ = find_peaks(storage_line)
    min_indices, _ = find_peaks(-storage_line)

    max_volumes = storage_line[max_indices]
    min_volumes = storage_line[min_indices]

    plot_storage_curve(storage_line, min_indices, max_indices, min_volumes, max_volumes)

    required_storage = 0.0
    for i, vol in enumerate(max_volumes):
        try:
            if (vol - min_volumes[i]) > required_storage:
                required_storage = vol - min_volumes[i]
        except IndexError:
            print("Reached end of storage line.")
    return required_storage


if __name__ == "__main__":
    # LOAD DATA
    file_directory = os.path.abspath("") + "\\flows\\"
    daily_flow_dict = read_data(directory=file_directory, ftype="csv",
                                fn_prefix="daily_flows_", fn_suffix="",
                                delimiter=";")
    try:
        print(daily_flow_dict[1979])
    except KeyError:
        print("Oh no, something went wrong - check your code.")

    # CONVERT DAILY TO MONTHLY DATA
    monthly_vol_dict = {}
    for year, flow_array in daily_flow_dict.items():
        monthly_vol_dict.update({year: daily2monthly(flow_array)})
    print(monthly_vol_dict[1979])

    # MAKE ARRAY OF MONTHLY SUPPLY VOLUMES (IN MILLION CMS)
    monthly_supply = np.array([1.5, 1.5, 1.5, 2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 3.0, 2.0, 1.5])

    # GET REQUIRED STORAGE VOLUME FROM SEQUENT PEAK ALGORITHM
    required_storage = sequent_peak(in_vol_series=monthly_vol_dict, out_vol_target=monthly_supply)
    print("The required storage volume is %0.2f million CMS." % required_storage)
