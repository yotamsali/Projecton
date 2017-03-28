import numpy
from carcnn import carcnn
from keras.models import save_model

SIZE = [120,70]

from images import fetch_images

dataset = fetch_images('images',target_name='label',data_name='data',transpose_data=True,data_home='/home/yovelrom/PycharmProjects/Projecton')
#data = numpy.reshape(dataset['data'],(26706,3,120,70))
#data = data[:,np.newaxis,:,:]
print(dataset['data'].shape)
#dataset['data'] = numpy.transpose(dataset['data'])

dataset['data'] = numpy.reshape(dataset['data'],(10000,120,70,3))
print("1")
#dataset['data'] = (dataset['data'])[:,:,:,np.newaxis]
print("1")
#(trainData,testData,trainLabels,testLabels) = train_test_split(dataset['data']/255.0,dataset['target'],test_size=0.33)

print("1")





#trainLabels = np_utils.to_categorical(trainLabels,1)
print("1")
#testLabels = np_utils.to_categorical(testLabels,1)
print("1")

print("compiling")


model = carcnn.build(120,70,3,1)

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the model
model.fit(dataset['data'], dataset['target'], nb_epoch=10, batch_size=20)



save_model(model,'/home/yovelrom/PycharmProjects/Projecton/avivtut')

