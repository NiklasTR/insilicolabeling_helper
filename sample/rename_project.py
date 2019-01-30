# This function renames flatfield corrected images so they can be normalized and fed into the ISL algorithm
import sys
import numpy as np
import pandas as pd
import os
from string import ascii_uppercase
import datetime

#from definition import CONFIG_PATH

def read_original_files(dir, file_extension = 'tiff', pattern_name = "CCLF", pattern_extension = ".png"):
    # access dir and read filenames
    file = pd.Series(os.listdir(dir))

    # scoop up previously processed directories
    if file.str.contains(pattern_name).sum() > 0 and file.str.contains(pattern_extension).sum() > 0:
        print("Directory already processed")
        status = "processed"
        return status

    # keep files that match pattern
    file = file[file.str.endswith(file_extension)]
    # turn array into DataFrame
    file_df = pd.DataFrame(file)
    file_df.columns = ['original_name']
    file_df['condition'] = dir.split('/')[-1]       # I set the superior directory to be the condition
    return(file_df)


def extract_original_files_project(df):

    f_ch = lambda x: x["original_name"].split("_")[-2]
    f_fl = lambda x: x["original_name"].split("_")[-3][1:]


    df = df.assign(channel_n = df.apply(f_ch, axis=1),
                    #row = df.original_name.str.slice(1,3),
                    #col = df.original_name.str.slice(4,6),
                    tile_computation = df.apply(f_fl, axis=1),
                    )

    return(df)


def transform_original_files_project(df, ch1, ch2, ch3, ch4):

    f_wl = lambda x: x["original_name"].split("_")[-4]

    df = df.assign(well = df.apply(f_wl, axis=1),
                   channel = df.apply(translate_channel, axis = 1, ch1 = ch1, ch2 = ch2, ch3 = ch3, ch4 = ch4))
    df = df.assign(isl_name = df.apply(supply_isl_name, axis = 1, experiment_descriptor = "None"))

    return(df)


def translate_channel(df_row, ch1, ch2, ch3, ch4):
    if ch3 == "CE" and ch4=="TMRM":
        dict = {"ch1" : "DPC",
                "ch2" : "BRIGHTFIELD",
                "ch3" : "MAP2_CONFOCAL",     # This channel is CELLEVENT most of the time
                "ch4" : "TUJ1_WIDEFIELD"}
    if ch3 == "CD45" and ch4=="TMRM":
        dict = {"ch1" : "DPC",
                "ch2" : "BRIGHTFIELD",
                "ch3" : "ISLET_WIDEFIELD",     # This channel is CELLEVENT most of the time
                "ch4" : "TUJ1_WIDEFIELD"}
    return(dict[df_row['channel_n']])
    #ISLET_WIDEFIELD = CD45
	#TUJ1_WIDEFIELD = TMRM
	#MAP2_CONFOCAL = CellEvent



def build_isl_name(lab = "CCLF", condition = "unknown",year = "2019",month = "00",day = "00",minute = "0",well = "Z00",
                   tile_computation = "00", channel = "UNKNOWN",is_mask = "false"):
    # I create some date and time variables for consistency
    dt = datetime.datetime.now()
    string = 'lab-{0},condition-{1},acquisition_date,year-{2},month-{3},day-{4},minute-{5},well-{6},tile_computation-{7},depth_computation-MAXPROJECT,channel-{8},is_mask-{9}.tiff' \
    .format(lab, condition, dt.year, dt.month, dt.day, dt.minute, well, tile_computation, channel, is_mask)
    return(string)

def supply_isl_name(df_row, experiment_descriptor = "None"):
    return(build_isl_name(well = df_row['well'],
        tile_computation = df_row['tile_computation'],
        channel = df_row['channel'],
        condition = df_row['condition']))

def change_name(df_row, dir):
    os.rename(os.path.join(dir, df_row['original_name']), os.path.join(dir, df_row['isl_name']))
    return()


def rename_file(path, ch1, ch2, ch3, ch4):
    #dir = os.path.join(os.getcwd(), path)
    dir = path

    tmp = read_original_files(dir)

    if not isinstance(tmp, pd.DataFrame):
        channel = "empty"
        return(channel)

    tmp = extract_original_files_project(tmp)
    tmp = transform_original_files_project(tmp, ch1, ch2, ch3, ch4)

    tmp.apply(change_name, axis = 1, dir = dir)
    # I create a log of my rename operation
    tmp.to_csv("rename_file_log.csv")
    print("renamed files in: {0}" .format(dir))

    channel_return = tmp['channel'][0]
    return(channel_return)

def __main_manual():
    path = sys.argv[1]
    rename_file(path)

if __name__ == '__main__':
    __main_manual()
