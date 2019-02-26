import os
import sys

# this code can currenlty be run only once - it can not process files which have already been re

def identify_files(path, input_extension = 'tif'):
    #legacy renaming
    dir = path
    #dir = '/Users/nrindtor/bucket/flatfield/000012070903_2019-01-10T20_04_27-Measurement_3/000012070903_2019-01-10T20_04_27-Measurement_3-sk1-A01-f01-ch3'
    #dir = sys.argv[1]
    #for local:
    #dir = '/Users/nrindtor/rapid_dev/insilico-labeling/703_cd45/cd45_projection/'
    #channel = "CD45"
    #path = 'local_data/703_cd45/named' #/Users/nrindtor/bucket/flatfield/703__2018-11-07T20_55_16-Measurement_1-sk2-A01-f07-ch2
    #dir = os.path.join(os.getcwd(), path)
    file_list = os.listdir(dir)     # I only keep .tiff images in my list
    image_channel_path = [i for i in file_list if input_extension in i]
    return(image_channel_path)

def create_output_filename(path, image_channel_path, projection_tag = "-maxproject", file_extension = ".tiff", exclude_tag = "lab-CCLF"):
    #legacy renaming
    dir = path
    # I create a list of output filenames
    rename_path = []
    #i = 0

    exclude_list = [i for i in image_channel_path if exclude_tag in i]
    if len(exclude_list) > 0:
        print("skipping directory")
        return()

    if len(exclude_list) == 0:
        for i in range(len(image_channel_path)):
            new_name = image_channel_path[i].split(',')[1][10:]
            new_name = new_name + projection_tag + file_extension #trimming the file ending
            joined_new_name = os.path.join(dir, new_name)
            rename_path.append(joined_new_name)

        return(rename_path)

# different from rename module
def rename_file(dir, image_channel_path, rename_path):

    if len(image_channel_path) != len(rename_path):
        return()
    else:
        for i in range(len(image_channel_path)):
            os.rename(os.path.join(dir, image_channel_path[i]), os.path.join(dir, rename_path[i]))
            print("reverted the file %s to %s" % (image_channel_path[i], rename_path[i]))
        return()

def revert_file_name(dir):
    image_channel_path = identify_files(dir)
    rename_path = create_output_filename(dir, image_channel_path)

    rename_file(dir, image_channel_path, rename_path)

def __main_manual(path=sys.argv[1], pattern = sys.argv[2]):
    # ch1="DPC", ch2="BRIGHTFIELD", ch3="CE", ch4="TMRM"
    # creating list of dirs
    #path = '/Users/nrindtor/GitHub/isl_preprocess/local_data/test'
    dir_list = os.listdir(path)
    dir_list = [i for i in dir_list if pattern in i]

    #print(dir_list)

    for dir in dir_list:
        path_joined = os.path.join(path, dir)
        revert_file_name(path_joined)


if __name__ == '__main__':
    __main_manual()
