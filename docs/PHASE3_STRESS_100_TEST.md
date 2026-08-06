# PHASE 3 STRESS TEST - 100 Conversations

Run: 2026-08-06 07:18:34

- Conversations: 100
- Exercised (plan engaged on turn 1): 99
- Skipped (Understanding classifier miss on goal): 1
- Passed: 97 (98.0% of exercised)
- Failed: 2

- Goal pool: 176 verified of 180 probed (4 classifier misses)

## Memory Regression Battery

- PASS store: op=store status=stored
- PASS recall-route: memories=1
- PASS update: op=update status=updated
- PASS history: history_entries=1
- PASS forget: op=forget status=deleted
- PASS clarification-followup: op=store
- PASS store-valid-json: 
- PASS no-write: op=None

Memory regression: 8/8 checks passed

## Per-category results

### light: 20/20 passed (0 skipped)
### medium: 30/30 passed (0 skipped)
### heavy: 19/19 passed (1 skipped)
### extreme: 18/20 passed (0 skipped)
- convo 71 (extreme)
  - expect=goal got=no-plan cont=False err=None
- convo 75 (extreme)
  - expect=pivot got=continue cont=True err=None
### gate: 10/10 passed (0 skipped)

## Failure details

### convo 71 (extreme) 70.1s
- msg='can you plan my trip to quito' expect=goal got=goal cont=False
  resp="I'd be happy to help you plan your trip to Quito. To get started, let's look up some facts about Qui"
- msg='right, but i am a total beginner' expect=continue got=continue cont=True
  resp="As a total beginner, let's start with some general tips for traveling to Quito. I've found that many"
- msg='can you plan my trip to madrid' expect=pivot got=goal cont=False
  resp="So, you're looking to plan a trip to Madrid. Let's start with some general tips for traveling in Mad"
- msg='what is the weather like in oslo' expect=question got=detour cont=False
  resp="Oslo's weather can vary quite a bit depending on the time of year you visit. Generally, it's known f"
- msg='ok so back to it, give me the first step' expect=continue got=continue cont=True
  resp="Let's get started with planning your trip to Madrid. The first step would be to review some general "
- msg='i am done for today' expect=end got=no-plan cont=False
  resp="It was nice chatting with you, and I'm glad I could help with your trip planning. Have a great day, "
- msg='i want to learn public speaking help me' expect=goal got=no-plan cont=False
  resp="I'd be happy to help you with public speaking. To get started, can you tell me a bit about what's ho"
### convo 75 (extreme) 75.4s
- msg='teach me the piano' expect=goal got=goal cont=False
  resp="Let's get started with understanding piano basics then. The piano consists of several parts, includi"
- msg='right, but i am a total beginner' expect=continue got=continue cont=True
  resp='So just to make sure I understand, when you said "right" earlier, you were agreeing with something a'
- msg='help me plan a study schedule for exams' expect=pivot got=continue cont=True
  resp="Let's get back to planning a study schedule for exams. Since you're a total beginner when it comes t"
- msg='what is the weather like in manila' expect=question got=detour cont=False
  resp="Manila's current weather conditions are a bit of a mixed bag, I'm afraid. As of this morning, August"
- msg='ok so back to it, give me the first step' expect=continue got=continue cont=True
  resp="Let's get back to planning a study schedule for exams. The first step is to Review Exam Details. Can"
- msg='i am done for today' expect=end got=no-plan cont=False
  resp="It was nice chatting with you, and I'm glad we could cover some piano basics and plan a study schedu"
- msg='i want to build a home gym' expect=goal got=goal cont=False
  resp="So you want to build a home gym. Let's get back to Step 1: Review Space Requirements. Can you tell m"
