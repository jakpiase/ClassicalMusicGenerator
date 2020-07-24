from keras.models import load_model
import pandas as pd
import numpy as np
from mido import MidiFile, MidiTrack, Message
import random

model = load_model('../Wygenerowane pliki/model v9 loss 0.72367 input 50.h5')


INPUT_LENGTH = 50   #Liczba nut wejściowych - musi być zgodna z modelem.
SHIFT_DATA = 1200   #Początek utworu testowego
TICKS = 600     #Tyle nut zostanie wygenerowanych


#Następna nuta generowana jest na podstawie odwrotnej dystrybuanty macierzy przewidywań
def getNote(predictionVector):
    rand = random.random()
    for index, val in enumerate(np.cumsum(predictionVector)):
        if val > rand:
            return index
    return index


DROPPED_LABELS = ['velocity', 'time']
dataframe = pd.read_csv('testdata.csv', names=['note', 'velocity', 'time'])
dataframe.drop(labels=DROPPED_LABELS, axis='columns', inplace=True)

X = dataframe.head(INPUT_LENGTH + SHIFT_DATA).tail(INPUT_LENGTH).to_numpy()
Result = np.empty([TICKS, 1])

for i in range(TICKS):
    prediction = model.predict([[X]])
    note = getNote(prediction)
    print(max(max(prediction)))
    print(note)
    print("-------")
    X[0:INPUT_LENGTH - 1, :] = X[1:INPUT_LENGTH, :]
    X[INPUT_LENGTH - 1, :] = note
    Result[i, :] = note

midiFile = MidiFile(type=1)
midiTrack = MidiTrack()
for i in range(TICKS):
    note = int(Result[i, 0])
    print(note)
    time = 160
    velocity = 120
    midiTrack.append(Message('note_on', note=note, velocity=velocity, time=time))


midiFile.tracks.append(midiTrack)
midiFile.save('generated music.mid')
