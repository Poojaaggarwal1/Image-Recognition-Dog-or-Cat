
#Force google colab to switch to high ram mode. Run it only once. 
a = []
while(1):
    a.append('1')
#Also change runtime type to enable GPU from menu.

##This block is only for access of files using google drive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

import cv2;
import matplotlib.pyplot as plt
import numpy as np;
from random import shuffle;
import cv2;
from random import shuffle;
from tqdm import tqdm;
import tensorflow;
from tensorflow.keras import layers;
from tensorflow.keras import Model;
from tensorflow.keras.optimizers import SGD;
from tensorflow.keras.callbacks import TensorBoard;
IMAGE_SIZE = 75;

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)
train_Data_File = drive.CreateFile({'id': '1S2Hv1_3FDi5lBGBU-4CMzQs_pPNDBthC'});
test_Data_File = drive.CreateFile({'id': '14Ih1ZbzYasw5Sir57qKuBRmM0rvvaDxW'});

#This block takes 6-10 minutes to load the training data.
train_Data_File.GetContentFile('Cat_Dog_Train_Data.npy');
train_Data = np.load('Cat_Dog_Train_Data.npy', allow_pickle=True)

train_Data.shape
#No of training images, First columns is of images and second is of labels

from google.colab import files
files.download('Cat_Dog_Train_Data.npy')

test_Data_File.GetContentFile('Cat_Dog_Test_Data.npy');
test_Data = np.load('Cat_Dog_Test_Data.npy', allow_pickle= True)



test_Data.shape
#No of test images, First columns is of images and second is of labels

#Show some training images with labels
count = 0;
Num_of_Images = 20;
plt.figure(figsize=(20,20))
for i in np.random.randint(1000, size = Num_of_Images):
  count = count+1;
  plt.subplot(Num_of_Images/4,4, count);
  plt.imshow(train_Data[i][0])
  P = train_Data[i][1];
  if(P[0]>P[1]):
      plt.title('cat')
  else:
      plt.title('dog');

# Our input feature map is 75x75x3: 75x75 for the image pixels, and 3 for
# the three color channels: R, G, and B
img_input = layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))      

# First convolution extracts 16 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(16, 3, activation='relu')(img_input)          #convolution with 16 filters of 3 * 3 [ padding = 0 , strides  = 1 (since not specified anything )]
x = layers.MaxPooling2D(2)(x)

# Second convolution extracts 32 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(32, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Third convolution extracts 64 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(64, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Second convolution extracts 128 filters that are 3x3
# Convolution is followed by max-pooling layer with a 2x2 window
x = layers.Conv2D(128, 3, activation='relu')(x)
x = layers.MaxPooling2D(2)(x)

# Flatten feature map to a 1-dim tensor so we can add fully connected layers
x = layers.Flatten()(x)

# Create a fully connected layer with ReLU activation and 512 hidden units
x = layers.Dense(512, activation='relu')(x)

# Create output layer with a two nodes and softmax activation
output = layers.Dense(2, activation='softmax')(x)

# Create model:
model = Model(img_input, output)

model.summary()

model.compile(loss='binary_crossentropy',
              optimizer= 'adam',
              metrics=['acc']);

train_Data.shape

X_train = np.array([i[0] for i in tqdm(train_Data)]);
print("shape before " , X_train.shape)

# Prepare the data for the training by separating X and Y vectors.
X_train = np.array([i[0] for i in tqdm(train_Data)]);
print("shape before " , X_train.shape)
X_train = X_train.reshape(-1,IMAGE_SIZE, IMAGE_SIZE,3);
Y_train = np.array([i[1] for i in train_Data]);
print( "Shape after "  , X_train.shape , Y_train.shape)
X_test = np.array([i[0] for i in tqdm(test_Data)]);
X_test = X_test.reshape(-1,IMAGE_SIZE, IMAGE_SIZE,3);
Y_test = np.array([i[1] for i in test_Data]);

Y_train.shape

model.fit(X_train,Y_train, batch_size =64, epochs = 10,verbose=1, validation_data=(X_test, Y_test))

import matplotlib.pyplot as plt

#Show some random test images with their predictions as title.
count = 0;
Num_of_Images = 20;
plt.figure(figsize=(20,20))
for i in np.random.randint(500, size = Num_of_Images):
  count = count+1;
  plt.subplot(Num_of_Images/4,4, count);
  plt.imshow(X_test[i].reshape(IMAGE_SIZE, IMAGE_SIZE,3))
  P = model.predict(X_test[i].reshape(1,IMAGE_SIZE, IMAGE_SIZE,3))
  P = np.array(P);
  if(P[0,0]>P[0,1]):
      plt.title('cat')
  else:
      plt.title('dog')

