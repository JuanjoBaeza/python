import os
import tensorflow as tf
import numpy as np 
import matplotlib.pyplot as plt

#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

cel = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
far = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)

capa   = tf.keras.layers.Dense(units=1, input_shape=[1]) #input_shape -> Define la capa de entrada cuantas neuronas
modelo = tf.keras.Sequential([capa])

modelo.compile(
    optimizer=tf.keras.optimizers.Adam(0.1), #Optimizador Adam, Tasa de aprendizaje pequeña 0.1
    loss='mean_squared_error'
)

print("Comenzando entrenamiento...")

historial = modelo.fit(cel, far, epochs=1000, verbose=False) #Entrenamiento con fit

print("Modelo entrenado!")

plt.xlabel("x Vueltas training")
plt.ylabel("Magnitud de perdida")

plt.plot(historial.history["loss"])

resultado = modelo.predict([100.0])
print("El resultado es " + str(resultado) + "farenheit")