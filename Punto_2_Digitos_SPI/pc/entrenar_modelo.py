import tensorflow as tf
from tensorflow.keras import layers, models
(xtr,ytr),(xte,yte)=tf.keras.datasets.mnist.load_data()
xtr=xtr.astype("float32")/255; xte=xte.astype("float32")/255
xtr=xtr[...,None]; xte=xte[...,None]
m=models.Sequential([
 layers.Input((28,28,1)),
 layers.Conv2D(32,3,activation="relu"), layers.MaxPooling2D(),
 layers.Conv2D(64,3,activation="relu"), layers.MaxPooling2D(),
 layers.Flatten(), layers.Dense(128,activation="relu"), layers.Dropout(.4),
 layers.Dense(10,activation="softmax")
])
m.compile(optimizer="adam",loss="sparse_categorical_crossentropy",metrics=["accuracy"])
m.fit(xtr,ytr,epochs=5,batch_size=128,validation_split=.1)
print("Evaluacion:",m.evaluate(xte,yte,verbose=0))
m.save("modelo_mnist_cnn.h5")
