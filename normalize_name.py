import numpy as np
import os
import png

from skimage import data, img_as_float
from skimage import exposure
from skimage import io

from sklearn.preprocessing import StandardScaler

dir = os.path.join(os.getcwd(), 'local_data/703_cd45/sk2/raw')
file = np.array(os.listdir(dir))
channel = "ch3"

# I select the brightfield images that show my pattern
# I nest list comprehension, np arrays to create my final list
brightfield_path = np.sort(file[np.array([channel in i for i in file])])

# I add the full path
joined_list = []
for i in np.ndarray.tolist(brightfield_path):
    joined = os.path.join(dir, i)
    joined_list.append(joined)

# I create a list of output filenames
scale_path = []
for i in range(len(brightfield_path)):
    scale_path.append('scale_' + brightfield_path[i])



#I collapse the list into the standard input format for image collections
collapsed_list = ':'.join(joined_list)

image_coll = io.imread_collection(collapsed_list)

###### dev
target_std = 0.125
target_mean = 0.5

image_scaled = []
for i in range(len(image_coll)):
    #image_scaled.append(StandardScaler().fit_transform(image_coll[i]))
    #I rescale
    mat_ms = target_mean + (image_coll[i] - image_coll[i].mean()) * (target_std/image_coll[i].std())
    #I trim
    mat_ms[mat_ms > 1] = 1
    mat_ms[mat_ms < 0] = 0
    #I store
    #image_scaled.append(mat_ms)
    #I store directly to file using the file names I know already
    io.imsave(scale_path[i], mat_ms)
    #png.from_array(mat_ms)
