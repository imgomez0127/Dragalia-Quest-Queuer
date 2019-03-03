import os
import time
import numpy as np
import pandas
from PIL import Image
import pyscreenshot as ImageGrab
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten,Reshape
from ImageProcessor import ImageProcessor 

class ConvNet(keras.Sequential):
    def __init__(self, boxname, convLayerAmt, denseLayersAmt):
        super().__init__()
        self.__boxname = boxname
        self.__convLayerAmt = convLayerAmt
        self.__denseLayersAmt = denseLayersAmt
        self.__imageShape = 0
        self.__filePath = "./" + self.__boxname + "Examples"
        self.__imageLabels = []
        self.__images = self.__processImages()
        self.__kernelSize = 3
        self.__kernelChannels = 3
        self.__poolingSize = 2
    @property
    def boxname(self):
        return self.__boxname
    
    @property
    def convLayerAmt(self):
        return self.__convLayerAmt

    @convLayerAmt.setter
    def convLayerAmt(self,convLayerAmt):
        self.__convLayerAmt = convLayerAmt
    
    @property
    def denseLayersAmt(self):
        return self.__denseLayersAmt
    
    @denseLayersAmt.setter
    def denseLayersAmt(self,denseLayersAmt):
        self.__denseLayersAmt = denseLayersAmt
    
    @property
    def imageShape(self):
        return self.__imageShape
    
    @imageShape.setter
    def imageShape(self,imageShape):
        self.__imageShape = imageShape
    
    @property
    def filePath(self):
        return self.__filePath
    
    @property
    def images(self):
        return self.__images    

    @property
    def imageLabels(self):
        return self.__imageLabels

    def __processImages(self):
        processor = ImageProcessor(self.__filePath)     
        processedImages = processor.processFolderImages()
        if(len(processedImages) == 0):
            raise ValueError("There are no images in that folder")
        self.__imageLabels = list(processor.imageClasses)
        self.__imageShape = processedImages[0].shape
        return processedImages 
    def __computeFlattenSize(self):
        pass
    def BuildConvNet(self):
        self.add(Reshape((60,150,3)))
        for _ in range(self.__convLayerAmt):
            self.add(Conv2D(self.__kernelChannels,self.__kernelSize,
                             padding="valid"))
            self.add(MaxPooling2D(self.__poolingSize))
        self.add(Flatten())
        for i in range(self.__denseLayersAmt):
            self.add(Dense(1000,activation = "relu", use_bias=True))
        self.add(Dense(1,activation="softmax"))
        return self.layers

if __name__ == "__main__": 
    yeet = ConvNet("autobox",4,5)
    yeet.BuildConvNet()
    yeet.compile(optimizer = keras.optimizers.Adam(lr=.01),loss="categorical_crossentropy",metrics=["accuracy"])
    yeet.fit(np.asarray(yeet.images),np.asarray(yeet.imageLabels),epochs=1,batch_size=1)
    print(np.array(yeet.images[0]).shape)
    print(yeet.predict(np.reshape(yeet.images[0],(1,60,150,3))))
    print(yeet.imageLabels[0])
    yeet.summary()