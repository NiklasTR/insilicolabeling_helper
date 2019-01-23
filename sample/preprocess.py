import rename
import normalize

import os
import pandas as pd
import sys

def process_dir(path, channel, phrase='None'):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory
    path=directory of interest with .tiff files
    channel=channel that
    """
    #renaming
    rename.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    channel_list = [ch1, ch2, ch3, ch4]
    phrase_list = [phrase]
    # I keep channels that are actually called, there are more elegant ways to do this
    channel_list = np.setdiff1d(channel_list,phrase_list) 

    for channel in channel_list
    if channel == "BRIGHTFIELD":
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_brightfield(image_channel_path, scale_path)
        #delete renamed leftover
        normalize.clean(image_channel_path)
    else:
        image_channel_path = normalize.identify_files(path, channel = channel)
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_flourescent(image_channel_path, scale_path)
        #delete renamed leftover
        normalize.clean(image_channel_path)

def __main_manual(path=sys.argv[1], ch1='None', ch2='None', ch3='None', ch4='None'):
    # creating list of dirs
    dir_list = os.listdir(dir)
    for dir in dir_list:
        process_dir(dir, ch1=sys.argv[2], ch2=sys.argv[3], ch3=sys.argv[4], ch4=sys.argv[5])

if __name__ == '__main__':
    __main_manual()
