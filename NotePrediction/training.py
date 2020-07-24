import keras
import numpy as np
import pandas as pd
from keras.callbacks import ModelCheckpoint

INPUT_LENGTH = 50
DROPPED_LABELS = ['velocity', 'time']

dataframe = pd.read_csv('traindata.csv', names=['note', 'velocity', 'time'])
dataframe.drop(labels=DROPPED_LABELS, axis='columns', inplace=True)

X = []
Y = []

index = 0
while len(dataframe) > INPUT_LENGTH:
    input = dataframe.head(INPUT_LENGTH).to_numpy()
    label = np.array(dataframe.iloc[INPUT_LENGTH])
    dataframe = dataframe.tail(len(dataframe) - INPUT_LENGTH)
    X.append(input)
    Y.append(label)

X = np.array(X)
Y = np.array(Y)

N_SAMPLES = X.shape[0]

permutation = np.random.permutation(len(X))
X = X[permutation, :, :]
Y = Y[permutation, :]

Y_binary = keras.utils.to_categorical(Y)

from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Activation


optimizer = keras.optimizers.RMSprop(
    learning_rate=0.001,
    rho=0.94,
    epsilon=1e-07
)

model = Sequential()
model.add(Dense(108))
model.add(LSTM(
        134,
        dropout=0.06,
        input_shape=(X.shape[1], X.shape[2]),
        return_sequences=True
    ))
model.add(Dropout(0.10))
model.add(LSTM(
        106,
        dropout=0.10,
        return_sequences=True))
model.add(Dropout(0.10))
model.add(LSTM(
        88,
        dropout=0.05))
model.add(Dropout(0.08))
model.add(Dense(Y_binary.shape[1]))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='Adam')

filepath = 'models/model.{epoch:02d}-{loss:.5f} input_' + str(INPUT_LENGTH) + '.h5'
checkpoint = ModelCheckpoint(
    filepath,
    monitor='loss',
    verbose=0,
    save_best_only=True,
    mode='min'
)

callbacks_list = [checkpoint]
history = model.fit(X, Y_binary, epochs=400, workers=4, shuffle=True, batch_size=12, callbacks=callbacks_list)

pd.DataFrame(history.history).to_csv('history.csv')