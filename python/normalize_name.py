import numpy as np
import os

from skimage import data, img_as_float
from skimage import exposure
from skimage import io

from sklearn.preprocessing import StandardScaler

dir = os.path.join(os.getcwd(), 'local_data/703_cd45/sk2/raw')
file = np.array(os.listdir(dir))
channel = "ch3"

# I select the brightfield images that show my pattern
# I nest list comprehension, np arrays to create my final list
brightfield_path = file[np.array([channel in i for i in file])]

# I add the full path
joined_list = []
for i in np.ndarray.tolist(brightfield_path):
    joined = os.path.join(dir, i)
    joined_list.append(joined)

#I collapse the list into the standard input format for image collections
joined_list
':'.join(joined_list)

image_coll = io.imread_collection(joined_list)

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
    image_scaled.append(mat_ms)



###### dab
mat_m.std()
mat_m.mean()
mat_ms.max()
joined_list
len(image_coll)
type(image_coll[0])
standardized_data = StandardScaler().fit_transform(data)
