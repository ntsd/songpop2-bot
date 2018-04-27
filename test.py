from dejavu import Dejavu
from dejavu.recognize import MicrophoneRecognizer

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "root",
        "passwd": '', 
        "db": 'songpop',
    }
}
djv = Dejavu(config)

djv.fingerprint_directory("mp3", [".mp3"])

song = djv.recognize(MicrophoneRecognizer, seconds=10)
print(song)
