import tensorflow as tf
import numpy as np


class Genome:
    def __init__(self, name, t=0):
        self.name= name
        self.type = t
        self.model =  model = tf.keras.models.Sequential()
        
        self.input = tf.keras.layers.Dense(8, kernel_initializer='random_uniform', bias_initializer='zeros' ,activation="relu")
        self.model.add(self.input)
        
        self.output = tf.keras.layers.Dense(2, kernel_initializer='random_uniform', bias_initializer='zeros', activation="softmax")
        self.model.add(self.output)

        self.model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


    def training(self,x,y):
        self.model.fit(x, y, epochs=5)

    def eval(self,x, y):
        self.model.evaluate(x,y)

    def run(self, x):
        return self.model.predict(x)

    def resume(self):
        self.model.summary()

    def save(self, name):
        model_json = self.model.to_json()
        with open(name+"_model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.model.save_weights(name+".h5")
        print("Saved model to disk")

    def load_save(self, json_file, weight_file):
        json_file = open(json_file, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.model = tf.keras.models.model_from_json(loaded_model_json)
        # load weights into new model
        self.model.load_weights(weight_file)
        print("Loaded model from disk")


