import rename
import normalize

import os
import pandas as pd
import sys

def process_dir(path, ch1, ch2, ch3, ch4):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory
    path=directory of interest with .tiff files
    channel=channel that
    """
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test/703__2018-11-07T20_55_16-Measurement_1-sk2-A05-f07-ch2'
    #renaming
    channel = rename.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    if channel == "BRIGHTFIELD":
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_brightfield(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(image_channel_path)
    else:
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_flourescent(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(path)

def __main_manual(path=sys.argv[1], ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM", pattern = "Measurement"):
    # creating list of dirs
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test'
    dir_list = os.listdir(path)
    dir_list = [i for i in dir_list if pattern in i]
    for dir in dir_list:
        path_joined = os.path.join(path, dir)
        process_dir(path_joined, ch1=sys.argv[2], ch2=sys.argv[3], ch3=sys.argv[4], ch4=sys.argv[5])

if __name__ == '__main__':
    __main_manual()
