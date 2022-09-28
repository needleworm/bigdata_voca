import data_reader
from tensorflow import keras
import numpy as np

EPOCHS = 50

pgw_xlsx = "pgw.xlsx"
sn_xlsx = "sunung.xlsx"

file_names = [pgw_xlsx, sn_xlsx]

dr = data_reader.DataReader2(13, file_names)

model = keras.Sequential([
    keras.layers.Bidirectional(keras.layers.LSTM(64, return_sequences=True)),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(1, activation='relu'),
])

model.compile(optimizer="adam", metrics=["logcosh"], loss="logcosh")
#model.compile(optimizer="adam", metrics=["mse"], loss="mse")

print("\n\n************ TRAINING START ************ ")
early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
history = model.fit(x=dr.train_X, y=dr.train_Y, epochs=EPOCHS,
                    validation_data=(dr.test_X, dr.test_Y),
                    callbacks=[early_stop])

data_reader.draw_graph(model(dr.test_X), dr.test_Y, history)


print("\n\n************ Prediction START ************ ")
result = model.predict(x=dr.predict_X) * 100
