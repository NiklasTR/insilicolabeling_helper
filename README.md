# insilicolableing_helper

This repository provides functions to rescale and format cellprofiler output files for use in the in-silico-labeling model published by the Google Science Accelerator. 

## preprocess.py

The central function is in the *preprocess.py* module. Calling the function from the command line comes with necessary arguments: 

* path to the directory of images with distributed cellprofiler output
* 4 channel names in order of their numbering 
* a key phrase to identify data that has not yet been processed

python /home/ubuntu/bucket/isl_preprocess/sample/preprocess.py /home/ubuntu/bucket/flatfield/000012070903_2019-01-10T20_04_27-Measurement_3/ "DPC" "BRIGHTFIELD" "CE" "TMRM" "Measurement"

## revert.py (deprecated)

In case the original file name needs to be restored after renaming, this function can revert the original names. 

It takes the path to the directories and a pattern of directories that will be processed. The function has only been used on individual flourscence images. 

python /home/ubuntu/bucket/isl_preprocess/sample/revert.py '/home/ubuntu/bucket/flatfield/000012070903_2019-01-10T20_04_27-Measurement_3' 'ch3'


