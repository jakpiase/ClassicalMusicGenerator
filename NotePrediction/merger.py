import os
from mido import MidiFile, MidiTrack, Message

ACCEPTED_TYPES = ['note_on']

def isMessageAccepted(msg):
    return msg.type in ACCEPTED_TYPES

def isTrackEmpty(track):
    for msg in track:
        if isMessageAccepted(msg):
            return False
    return True

def getTimeLength(track):
    length = 0
    for msg in track:
        if msg.type in ACCEPTED_TYPES + ['control_change']:
            length += msg.time
    return length

def getMaxLength(midiFile):
    maxLength = 0
    for track in midiFile.tracks:
        trackLength = getTimeLength(track)
        if trackLength > maxLength:
            maxLength = trackLength
    return maxLength


MODE = 'train2'

FILE_PATH = os.path.join('resources', MODE)

tracks = []
maxTracks = 0

for file in os.listdir(FILE_PATH):
    filepath = os.path.join(FILE_PATH, file)
    emptyTrackMask = [(0 if isTrackEmpty(track) else 1) for track in MidiFile(filepath).tracks]
    maxTracks = max(sum(emptyTrackMask), maxTracks)
print("Max tracks: ", maxTracks)



mainMidiFile = MidiFile(type=1)
mainTracks = [MidiTrack() for i in range(maxTracks)]



for file in os.listdir(FILE_PATH):
    filepath = os.path.join(FILE_PATH, file)
    print("Current file: ", filepath)
    midiFile = MidiFile(filepath)
    maxTimeLength = getMaxLength(midiFile)
    index = 0
    for track in midiFile.tracks:
        if isTrackEmpty(track):
            continue

        for msg in track:
            if isMessageAccepted(msg):
                mainTracks[index].append(msg)
            elif msg.type == 'control_change':
                mainTracks[index].append(Message('note_on', note=100, velocity=0, time=msg.time))
        dif = maxTimeLength - getTimeLength(track)
        if dif != 0:
            mainTracks[index].append(Message('note_on', note=100, velocity=0, time=dif))
        index += 1

    for emptyTrackIndex in range(index + 1, maxTracks):
        mainTracks[emptyTrackIndex].append(Message('note_on', note=100, velocity=0, time=maxTimeLength))

for track in mainTracks[:1]:
    mainMidiFile.tracks.append(track)
mainMidiFile.save('fullTrack.mid')

file = open(MODE + 'data.csv', 'w')
for msg in mainTracks[0]:
    if not msg.is_meta:
        if msg.time > 0:
            output = f"{msg.note},{msg.velocity},{msg.time}\n"
            file.write(output)


for track in mainMidiFile.tracks:
    print(getTimeLength(track))



#data
track = mainMidiFile.tracks[0]

