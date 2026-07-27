## Speech System (Updated)

Current pipeline:

Microphone
↓
Voice Activity Detection (WebRTC VAD)
↓
Audio Capture
↓
Whisper Speech Recognition (GPU accelerated)
↓
Command Handler
↓
Response Generation
↓
Text To Speech (pyttsx3)


Components:

- speech_recognizer.py
    - Uses OpenAI Whisper
    - Running on CUDA GPU
    - Current model: Whisper small

- voice_detector.py
    - Uses WebRTC VAD
    - Detects speech start and end
    - Replaces fixed duration recording

- speech_speaker.py
    - Uses pyttsx3
    - Converts responses into voice


Hardware acceleration:

GPU:
RTX 4050

Framework:
PyTorch CUDA

Status:
Working