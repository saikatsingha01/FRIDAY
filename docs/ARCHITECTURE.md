# Friday Architecture

## Overall Pipeline

Microphone
↓
Voice Activity Detection (WebRTC VAD)
↓
Audio Capture
↓
Whisper Speech Recognition (CUDA GPU)
↓
Text Processing
↓
Brain Layer
↓
Command Handler / Memory / Context Reasoning
↓
Response Generator
↓
Text To Speech
↓
Speaker


---

# Speech System

Current pipeline:

Microphone
↓
Voice Activity Detection (WebRTC VAD)
↓
Audio Capture
↓
Whisper Speech Recognition (GPU accelerated)
↓
Text Processing
↓
Brain
↓
Response Generation
↓
Text To Speech


---

# Core Components

## speech_recognizer.py

Purpose:
- Converts speech into text.
- Uses OpenAI Whisper.
- Runs entirely on CUDA.

Current Model:
Whisper Small

Status:
Working


---

## voice_detector.py

Purpose:
- Detects when the user starts speaking.
- Detects when speech ends.
- Eliminates fixed recording duration.

Library:
WebRTC VAD

Status:
Working


---

## speech_speaker.py

Purpose:
- Converts text into speech.

Current Engine:
pyttsx3

Status:
Working

Future:
Replace with neural TTS.


---

## process.py

Purpose:
- Cleans raw Whisper output.
- Removes punctuation.
- Normalizes user input.


---

## input_validator.py

Purpose:
- Rejects empty or invalid speech.
- Prevents accidental processing.


---

## context_manager.py

Purpose:
Stores recent conversations.

Current Features:
- Rolling conversation history
- Short-term context storage
- Context retrieval


---

## context_reasoner.py

Purpose:
Finds previous conversations related to the current user message.

Current Features:
- Keyword matching
- Recent conversation lookup

Future:
Semantic similarity search using embeddings.


---

## memory_manager.py

Purpose:
Stores and retrieves long-term memories.

Current Features:
- Automatic memory storage
- Category detection
- Importance scoring
- Memory recall
- Memory deletion


---

## brain.py

Purpose:

Acts as Friday's central reasoning layer.

Current Responsibilities:

- Receives processed user input
- Searches relevant conversation context
- Searches long-term memory
- Chooses whether memory or commands should answer
- Routes requests appropriately

Current Flow:

Input
↓
Context Search
↓
Memory Search
↓
Command Handling
↓
Response Generation


Future Responsibilities:

- LLM reasoning
- Planning
- Decision making
- Multi-step thinking
- Tool selection


---

## response_generator.py

Purpose:

Converts internal objects into natural language.

Current Status:

Basic formatting.

Future:

- Emotional tone
- Personality
- Dynamic wording
- Context-aware responses


---

## command_handler.py

Purpose:

Handles deterministic commands.

Current Features:

- Greetings
- Identity
- Memory commands
- Forget commands
- Skill routing


Future:

Only responsible for deterministic actions.

Reasoning will remain inside Brain.


---

# Hardware Acceleration

GPU

RTX 4050

Framework

PyTorch CUDA

Whisper

CUDA Accelerated

Status

Working


---

# Current Architecture Status

Completed

✓ Voice Activity Detection

✓ Whisper GPU Inference

✓ Speech Pipeline

✓ Long-term Memory

✓ Context Memory

✓ Context Reasoner

✓ Brain Layer

✓ Response Generator Foundation

✓ Automatic Memory Evaluation

✓ Memory Recall Routing


In Progress

• Natural response formatting

• Conversation reasoning

• LLM Integration


Future

• Semantic memory retrieval

• Embedding search

• Personality engine

• Emotion engine

• Planning engine

• Tool reasoning

• Autonomous decision making