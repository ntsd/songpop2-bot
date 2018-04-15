import sounddevice as sd
import soundfile as sf
import tempfile
import queue
import sys

list_devices=1
samplerate=44100 #None
filename=None
channels=2
device=1
subtype=None

if list_devices: #show list of device
    print(sd.query_devices())
if samplerate is None:
    device_info = sd.query_devices(device, 'input')
    # soundfile expects an int, sounddevice provides a float:
    samplerate = int(device_info['default_samplerate'])
if filename is None:
    filename = tempfile.mktemp(prefix='rec_unlimited_',
                                    suffix='.wav', dir='')
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

# Make sure the file is opened before recording anything:
with sf.SoundFile(filename, mode='x', samplerate=samplerate,
                  channels=channels, subtype=subtype) as file:
    with sd.InputStream(samplerate=samplerate, device=device,
                        channels=channels, callback=callback):
        print('#' * 80)
        print('press Ctrl+C to stop the recording')
        print('#' * 80)
        while True:
            print(len(q.get()))
            file.write(q.get())
