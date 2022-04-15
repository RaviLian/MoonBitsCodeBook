import os
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.datasets import mnist

os.environ['TFF_CPP_MIN_LOG_LEVEL'] = '2'

(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(-1, 28 * 28).astype("float32") / 255.0
x_test = x_test.reshape(-1, 28 * 28).astype("float32") / 255.0

# print(x_train.shape)  # (60000, 784)
# Functional API
inputs = keras.Input(shape=784)
x = layers.Dense(512, activation='relu')(inputs)
x = layers.Dense(256, activation='relu')(x)
outputs = layers.Dense(10, activation='softmax')(x)
model = keras.Model(inputs=inputs, outputs=outputs)


# print(model.summary())
model.compile(
    loss=keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    optimizer=keras.optimizers.Adam(lr=0.0001),
    metrics=["accuracy"]
)

model.fit(x_train, y_train, batch_size=32, epochs=1)
model.evaluate(x_test, y_test, batch_size=32)


model = keras.Model(inputs=model.inputs,
                    outputs=[model.layers[-2].output])
feature = model.predict(x_train)
print(feature.shape)


