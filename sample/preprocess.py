import rename_project
import rename_stack
import normalize

import os
import pandas as pd
import sys
#parallel execution
import multiprocessing
from functools import partial
from contextlib import contextmanager

def process_dir_stack(dir, path, ch1, ch2, ch3, ch4, keep_stack):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory of stacked images
    path=directory of interest with .tiff files
    """
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test/703__2018-11-07T20_55_16-Measurement_1-sk2-A05-f07-ch2'
    path = os.path.join(path, dir)
    #renaming
    channel = rename_stack.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    if channel == keep_stack and channel != "processed":
        image_channel_path = normalize.identify_files(path, channel = "CCLF") #hardcoding this variable as it is not necessary for the code to function
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_brightfield(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(image_channel_path)
    else:
        print("Skipped directory or received images that did not match the keep_stack pattern")

def process_dir_project(dir, path, ch1, ch2, ch3, ch4, avoid_project):         #, ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    """
    renames and normalizes directory of a single projected image
    path=directory of interest with .tiff files
    """
    #path = '/home/ubuntu/bucket/flatfield/000012048903__2019-02-05T20_27_41-Measurement_1/000012048903__2019-02-05T20_27_41-Measurement_1-sk1-A01-f01-ch2'
    path = os.path.join(path, dir)
    #renaming
    channel = rename_project.rename_file(path, ch1, ch2, ch3, ch4)
    #normalizing
    if channel != avoid_project and channel != "processed":
        image_channel_path = normalize.identify_files(path, channel = "CCLF")
        scale_path = normalize.create_output_filename(path, image_channel_path)
        normalize.normalize_convert_flourescent(path,image_channel_path, scale_path)
        #delete renamed leftover
        #normalize.clean(image_channel_path)
    else:
        print("Skipped directory or received images that did not match the keep_project pattern")

if __name__ == '__main__':
    path=sys.argv[1]
    ch1=sys.argv[2]
    ch2=sys.argv[3]
    ch3=sys.argv[4]
    ch4=sys.argv[5]
    pattern = "Measurement"
    pattern = sys.argv[6]
    keep_stack = "BRIGHTFIELD"
    keep_segmentation = "DPC"
    # define number of cores
    number_of_workers = multiprocessing.cpu_count()
    #number_of_workers = 
    # creating list of dirs
    #path = '/home/ubuntu/bucket/flatfield/000012048903__2019-02-05T20_27_41-Measurement_1/'
    print("listing directories")
    dir_list = os.listdir(path)
    dir_list = [i for i in dir_list if pattern in i]
    #I define a dictionary of channels
    channel_dict = {"ch1" : ch1, "ch2" : ch2, "ch3" : ch3,"ch4" : ch4}
    d_inverted={v:k for k,v in channel_dict.items()}
    pattern_stack = d_inverted[keep_stack]
    # I don't want segmentation data
    pattern_segmentation = d_inverted[keep_segmentation]
    #I only keep stacks for the directory list and run the loop
    dir_list_stack = [i for i in dir_list if pattern_stack in i]
    print("start processing")

    # I define a small helper function that only takes one input
    #def stack_helper(dir):
    #    print("received input dir")

    #    process_dir_stack(path_joined, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, keep_stack=keep_stack)
    #    print("processed input dir")
    # for loop - deprecated
    #for dir in dir_list_stack:
    #    stack_helper(dir)
    with multiprocessing.Pool(number_of_workers) as p:
        print("received input dir")
        p.map(partial(process_dir_stack, path = path, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, keep_stack=keep_stack), dir_list_stack) #(partial(merge_names, b='Sons'), names)

    # I treat everything else as a projection
    dir_list_project = [i for i in dir_list if pattern_stack not in i]
    dir_list_project = [i for i in dir_list_project if pattern_segmentation not in i]

    with multiprocessing.Pool(number_of_workers) as p:
        print("received input dir")
        p.map(partial(process_dir_project, path = path, ch1=ch1, ch2=ch2, ch3=ch3, ch4=ch4, avoid_project=keep_stack), dir_list_stack) #(partial(merge_names, b='Sons'), names)
