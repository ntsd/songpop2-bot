import numpy as np
import soundfile as sf
import pyaudio
import time

class AddSong:
    default_chunksize   = 8192
    default_format      = pyaudio.paInt16
    default_channels    = 2
    default_samplerate  = 44100

    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.data = []
        self.channels = AddSong.default_channels
        self.chunksize = AddSong.default_chunksize
        self.samplerate = AddSong.default_samplerate
        self.recorded = False
        self.filename = 'temp.mp3'

    def start_recording(self, channels=default_channels,
                        samplerate=default_samplerate,
                        chunksize=default_chunksize):
        self.chunksize = chunksize
        self.channels = channels
        self.recorded = False
        self.samplerate = samplerate

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()

        self.stream = self.audio.open(
            format=self.default_format,
            channels=channels,
            rate=samplerate,
            input=True,
            frames_per_buffer=chunksize,
        )

        self.data = [[] for i in range(channels)]

    def process_recording(self):
        data = self.stream.read(self.chunksize)
        nums = np.fromstring(data, np.int16)
        for c in range(self.channels):
            self.data[c].extend(nums[c::self.channels])

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        self.recorded = True

    def record(self, seconds=10):
        self.start_recording()
        for i in range(0, int(self.samplerate / self.chunksize
                              * seconds)):
            self.process_recording()
        self.stop_recording()
        
    def save(self):
        with sf.SoundFile(self.filename, mode='x', samplerate=self.samplerate,
                  channels=self.channels, subtype=None) as file:
            for i in self.data:
                file.write(i)

if __name__ == '__main__':
    addSong = AddSong()
    addSong.record(10)
    addSong.save()
