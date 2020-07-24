# ClassicalMusicGenerator

How it works:
1. prepares data from .MIDI files from /resources directory
2. trains LSTM neural network in predicting next note
3. network is returning table of prediction from given notes, then next note is generated using Quantile function
