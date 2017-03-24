import scipy.io as io
import numpy as np
from scipy import misc
from cv2 import resize
from sklearn import datasets
from sklearn.datasets.base import Bunch
import os
import numbers
import scipy as sp
from os.path import join, exists

"""
mldata_descr_ordering = np.zeros((2,),dtype=np.object)
mldata_descr_ordering[0] = 'data'
mldata_descr_ordering[1] = 'label'
image = misc.imread('/home/yovelrom/Downloads/cutImages/clip1/1.jpg')
image = resize(image,(120,70))
a =np.reshape(image,(1,3*120*70))
b= np.array([1])

io.savemat('images',{'data':a,'label':b , 'mldata_descr_ordering':mldata_descr_ordering})
"""


def fetch_images(dataname, target_name='label', data_name='data',
                 transpose_data=True, data_home=None):


    if not exists(data_home):
        print("home not found")

    matlab_name = dataname + '.mat'
    filename = join(data_home, matlab_name)

    # if the file does not exist, download it
    if not exists(filename):
        print("file doesnt exist")

    # load dataset matlab file
    with open(filename, 'rb') as matlab_file:
        matlab_dict = io.loadmat(matlab_file, struct_as_record=True)

    # -- extract data from matlab_dict

    # flatten column names
    col_names = [str(descr[0])
                 for descr in matlab_dict['mldata_descr_ordering'][0]]

    # if target or data names are indices, transform then into names
    if isinstance(target_name, numbers.Integral):
        target_name = col_names[target_name]
    if isinstance(data_name, numbers.Integral):
        data_name = col_names[data_name]

    # rules for making sense of the mldata.org data format
    # (earlier ones have priority):
    # 1) there is only one array => it is "data"
    # 2) there are multiple arrays
    #    a) copy all columns in the bunch, using their column name
    #    b) if there is a column called `target_name`, set "target" to it,
    #        otherwise set "target" to first column
    #    c) if there is a column called `data_name`, set "data" to it,
    #        otherwise set "data" to second column

    dataset = {'DESCR': 'mldata.org dataset: %s' % dataname,
               'COL_NAMES': col_names}

    # 1) there is only one array => it is considered data
    if len(col_names) == 1:
        data_name = col_names[0]
        dataset['data'] = matlab_dict[data_name]
    # 2) there are multiple arrays
    else:
        for name in col_names:
            dataset[name] = matlab_dict[name]

        if target_name in col_names:
            del dataset[target_name]
            dataset['target'] = matlab_dict[target_name]
        else:
            del dataset[col_names[0]]
            dataset['target'] = matlab_dict[col_names[0]]

        if data_name in col_names:
            del dataset[data_name]
            dataset['data'] = matlab_dict[data_name]
        else:
            del dataset[col_names[1]]
            dataset['data'] = matlab_dict[col_names[1]]

    # set axes to scikit-learn conventions
    if transpose_data:
        dataset['data'] = dataset['data'].T
    if 'target' in dataset:
        if not sp.sparse.issparse(dataset['target']):
            dataset['target'] = dataset['target'].squeeze()

    return Bunch(**dataset)


fetch_images('images',target_name='label',data_name='data',transpose_data=True,data_home='/home/yovelrom/PycharmProjects/Projecton')



