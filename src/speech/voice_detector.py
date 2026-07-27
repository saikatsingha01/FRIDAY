import sounddevice as sd
import webrtcvad
import wave
import collections
import time
import numpy as np


SAMPLE_RATE = 16000
CHANNELS = 1

FRAME_DURATION = 30

FRAME_SIZE = int(
    SAMPLE_RATE * FRAME_DURATION / 1000
)


# 0 = least aggressive
# 3 = most aggressive
vad = webrtcvad.Vad(2)


SILENCE_LIMIT = 15

PADDING_FRAMES = 14


def normalize_audio(frames):

    audio = np.frombuffer(
        b"".join(frames),
        dtype=np.int16
    )


    # Convert to float
    audio = audio.astype(
        np.float32
    )


    max_value = np.max(
        np.abs(audio)
    )


    if max_value > 0:

        # Normalize volume
        audio = audio / max_value

        # Prevent clipping while boosting
        audio = audio * 0.8


    audio = np.int16(
        audio * 32767
    )


    return audio.tobytes()



def save_audio(frames, filename="temp.wav"):

    print("Saving audio...")


    processed_audio = normalize_audio(
        frames
    )


    with wave.open(filename, "wb") as wf:

        wf.setnchannels(
            CHANNELS
        )

        wf.setsampwidth(
            2
        )

        wf.setframerate(
            SAMPLE_RATE
        )

        wf.writeframes(
            processed_audio
        )


    print(
        "Audio saved:",
        filename
    )



def listen():

    print("\nListening...")


    ring_buffer = collections.deque(
        maxlen=PADDING_FRAMES
    )


    audio_frames = []


    triggered = False

    silence_counter = 0



    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_SIZE,
        channels=CHANNELS,
        dtype="int16"
    ) as stream:


        # Allow microphone initialization
        time.sleep(0.3)



        while True:


            frame, _ = stream.read(
                FRAME_SIZE
            )


            frame_bytes = bytes(
                frame
            )


            speech = vad.is_speech(
                frame_bytes,
                SAMPLE_RATE
            )



            if not triggered:


                ring_buffer.append(
                    frame_bytes
                )


                if speech:

                    triggered = True


                    audio_frames.extend(
                        ring_buffer
                    )


                    ring_buffer.clear()



            else:


                audio_frames.append(
                    frame_bytes
                )


                if speech:

                    silence_counter = 0

                else:

                    silence_counter += 1



                if silence_counter > SILENCE_LIMIT:

                    break



    save_audio(
        audio_frames
    )


    print(
        "Recording finished."
    )


    return "temp.wav"