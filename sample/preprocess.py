import rename_project
import rename_stack
import normalize

import os
import pandas as pd
import sys

def process_dir_stack(path, ch1, ch2, ch3, ch4, keep_stack):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory of stacked images
    path=directory of interest with .tiff files
    """
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test/703__2018-11-07T20_55_16-Measurement_1-sk2-A05-f07-ch2'
    #renaming
    channel = rename_stack.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    if channel == keep_stack and channel != "empty":
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_brightfield(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(image_channel_path)
    else:
        print("Skipped directory or received images that did not match the keep_stack pattern.")

def process_dir_project(path, ch1, ch2, ch3, ch4, avoid_project):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory of a single projected image
    path=directory of interest with .tiff files
    """
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test/703__2018-11-07T20_55_16-Measurement_1-sk2-A05-f07-ch2'
    #renaming
    channel = rename_project.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    if channel != avoid_project and channel != "empty":
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_flourescent(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(image_channel_path)
    else:
        print("Skipped directory or received images that did not match the keep_project pattern")

def __main_manual(path=sys.argv[1], ch1=sys.argv[2], ch2=sys.argv[3], ch3=sys.argv[4], ch4=sys.argv[5], pattern = "Measurement", keep_stack = "BRIGHTFIELD"):
    # ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    # creating list of dirs
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test'
    pattern = sys.argv[6]
    dir_list = os.listdir(path)
    dir_list = [i for i in dir_list if pattern in i]
    #I define a dictionary of channels
    channel_dict = {"ch1" : ch1,
                    "ch2" : ch2,
                    "ch3" : ch3,
                    "ch4" : ch4}
    d_inverted={v:k for k,v in channel_dict.items()}
    pattern_stack = d_inverted[keep_stack]
    #I only keep stacks for the directory list and run the loop
    dir_list_stack = [i for i in dir_list if pattern_stack in i]
    for dir in dir_list_stack:
        path_joined = os.path.join(path, dir)
        process_dir_stack(path_joined, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, keep_stack=keep_stack)
    # I treat everything else as a projection
    dir_list_project = [i for i in dir_list if pattern_stack not in i]
    for dir in dir_list_project:
        path_joined = os.path.join(path, dir)
        process_dir_project(path_joined, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, avoid_project=keep_stack)





if __name__ == '__main__':
    __main_manual()