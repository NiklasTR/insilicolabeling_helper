# This function renames flatfield corrected images so they can be normalized and fed into the ISL algorithm
import sys
import numpy as np
import pandas as pd
import os
from string import ascii_uppercase
import datetime
import shutil

#from definition import CONFIG_PATH

def read_original_files(dir, file_extension = 'tiff', pattern_name = "CCLF", pattern_extension = "png"):
    # access dir and read filenames
    # dir = "/Users/nrindtor/bucket/flatfield/000012070903_2019-01-10T20_04_27-Measurement_3/000012070903_2019-01-10T20_04_27-Measurement_3-sk1-A01-f01-ch3/"
    file = pd.Series(os.listdir(dir))

    # scoop up previously processed directories
    if file.str.contains(pattern_name).sum() > 0 and file.str.contains(pattern_extension).sum() > 0:
        print("Directory already processed")
        status = "processed"
        return status
    # scoop up renamed but unnormalized directories
    elif file.str.contains(pattern_name).sum() > 0:
        print("Directory already renamed")
        status = "renamed"
        return status

    else:
        # keep files that match pattern
        file = file[file.str.endswith(file_extension)]
        # turn array into DataFrame
        file_df = pd.DataFrame(file)
        file_df.columns = ['original_name']
        file_df['condition'] = dir.split('/')[-1]       # I set the superior directory to be the condition
        return(file_df)


def row_col_to_well(df_row):
    return(ascii_uppercase[int(df_row['row'])-1] + df_row['col'])

def format_z_depth(df_row):
    return(int(df_row['z_depth_string'])-1)

def extract_original_files(df):
    df = df.assign(channel_n = df.original_name.str.slice(13,16),
                    row = df.original_name.str.slice(1,3),
                    col = df.original_name.str.slice(4,6),
                    tile_computation = df.original_name.str.slice(7,9),
                    z_depth_string = df.original_name.str.slice(10,12),
                    timepoint = df.original_name.str.slice(17,19),
                    )
    return(df)


def transform_original_files(df, ch1, ch2, ch3, ch4):
    df = df.assign(well = df.apply(row_col_to_well, axis = 1),
                   channel = df.apply(translate_channel, axis = 1, ch1 = ch1, ch2 = ch2, ch3 = ch3, ch4 = ch4),
                   z_depth = df.apply(format_z_depth, axis = 1))
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
                   tile_computation = "00", z_depth = "00",channel = "UNKNOWN",is_mask = "false"):
    # I create some date and time variables for consistency
    dt = datetime.datetime.now()
    string = 'lab-{0},condition-{1},acquisition_date,year-{2},month-{3},day-{4},minute-{5},well-{6},tile_computation-{7},z_depth-{8},channel-{9},is_mask-{10}.tiff' \
    .format(lab, condition, dt.year, dt.month, dt.day, dt.minute, well, tile_computation, z_depth, channel, is_mask)
    return(string)

def supply_isl_name(df_row, experiment_descriptor = "None"):
    return(build_isl_name(well = df_row['well'],
        tile_computation = df_row['tile_computation'],
        z_depth = df_row['z_depth'],
        channel = df_row['channel'],
        condition = df_row['condition']))

def change_name(df_row, dir):
    #os.rename(os.path.join(dir, df_row['original_name']), os.path.join(dir, df_row['isl_name']))
    shutil.copy2(os.path.join(dir, df_row['original_name']), os.path.join(dir, df_row['isl_name']))
    return()


def rename_file(path, ch1, ch2, ch3, ch4):
    #dir = os.path.join(os.getcwd(), path)
    dir = path

    tmp = read_original_files(dir)

    if not isinstance(tmp, pd.DataFrame):
        if tmp == "processed":
            channel = "processed"
            return(channel)
        elif tmp == "renamed":
            channel = "renamed"
            return(channel)

    tmp = extract_original_files(tmp)
    tmp = transform_original_files(tmp, ch1, ch2, ch3, ch4)

    tmp.apply(change_name, axis = 1, dir = dir)
    # I create a log of my rename operation
    tmp.to_csv("rename_file_log.csv")
    print("renamed files in: {0}" .format(dir))
    return(tmp['channel'][1])

def __main_manual():
    path = sys.argv[1]
    rename_file(path)

if __name__ == '__main__':
    __main_manual()

#for debugging:
#dir = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test/703__2018-11-07T20_55_16-Measurement_1-sk2-A05-f07-ch2'
#ch1="DPC"
#ch2="BRIGHTFIELD"
#ch3="CE"
#ch4="TMRM"
