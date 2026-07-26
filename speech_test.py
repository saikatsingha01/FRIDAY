import sounddevice as sd
from scipy.io.wavfile import write

sample_rate = 16000
duration = 5

print("Speak now...")

audio = sd.rec(
    int(sample_rate * duration),
    samplerate=sample_rate,
    channels=1,
    dtype="int16"
)

sd.wait()

write("temp.wav", sample_rate, audio)

print("Audio saved as temp.wav")