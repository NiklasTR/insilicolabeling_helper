import numpy as np
import os
import png

from skimage import data, img_as_float
from skimage import exposure
from skimage import io

#from sklearn.preprocessing import StandardScaler
import scipy.misc
import imageio
import re

channel = "BRIGHTFIELD"
path = 'local_data/703_cd45/named'
file_extension = 'png'

target_std = 0.125 #
target_mean = 0.5 #32767.5 #
max_num = 1#65535
min_num = 0

dir = os.path.join(os.getcwd(), path)
file = np.array(os.listdir(dir))

# I select the image_channel images that show my pattern
# I nest list comprehension, np arrays to create my final list
image_channel_path = np.sort(file[np.array([channel in i for i in file])])

# I add the full path
joined_list = []
for i in np.ndarray.tolist(image_channel_path):
    joined = os.path.join(dir, i)
    joined_list.append(joined)

# I create a list of output filenames
scale_path = []
for i in range(len(image_channel_path)):
    num = re.search(r'(z_depth-)(\d*)', image_channel_path[i]).group(2)
    num = int(num)-1
    tmp = re.sub(r'depth-\d*', "depth-"+ str(num), image_channel_path[i])
    scale_path.append(tmp[:-4] + file_extension)

#I collapse the list into the standard input format for image collections
collapsed_list = ':'.join(joined_list)

#I load data
image_coll = io.imread_collection(collapsed_list)

#I scale and save data
image_scaled = []
for i in range(len(image_coll)):
    #image_scaled.append(StandardScaler().fit_transform(image_coll[i]))
    tmp = image_coll[i]
    #tmp = tmp.astype(np.uint16)
    #I rescale
    mat_ms = target_mean + (tmp - tmp.mean()) * (target_std/tmp.std())
    #I trim
    mat_ms[mat_ms > max_num] = max_num
    mat_ms[mat_ms < min_num] = min_num
    #mat_ms = mat_ms.astype(np.int16)
    mat_ms = mat_ms*65535
    mat_ms = mat_ms.astype(np.uint16)
    #I store
    imageio.imwrite(uri = scale_path[i], im = mat_ms)
