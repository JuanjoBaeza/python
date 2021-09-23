# python 3.6
import numpy as np
import tensorflow as tf
from tensorflow.python.client import device_lib
from timeit import default_timer as timer

model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer=tf.compat.v1.train.AdamOptimizer(0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])


def random_one_hot_labels(shape):
    n, n_class = shape
    classes = np.random.randint(0, n_class, n)
    tmp_labels = np.zeros((n, n_class))
    tmp_labels[np.arange(n), classes] = 1
    return tmp_labels


data = np.random.random((1000, 32))
labels = random_one_hot_labels((1000, 10))

durations = []
for i in range(10):  # run N times
    start = timer()
    model.fit(data, labels, epochs=50, batch_size=32)
    durations.append(timer() - start)

print(f"tf.version.VERSION = {tf.version.VERSION}")
print(f"tf.keras.__version__ = {tf.keras.__version__}")
devices = device_lib.list_local_devices()  # this may allocate all GPU memory ?!
print(f"devices = {[x.name for x in devices]}")
print(f"model.fit durations: {durations}")