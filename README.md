# Voice Assistant

## Install
```export OPENAI_API_KEY='MY_API_KEY'```
```bash setup.sh```

May require installing portaudio . eg ```brew install portaudio```
First time running, TTS will download a model.

## Notes
Run Main.py and when you see "Waiting for key phrase", say "question". What the STT model thinks you said will be printed if it doesn't respond. If it hears "question", it will speak "I'm listening". For some reason, there's a slight delay between it finishing saying "I'm listening" and recording the question so wait a moment or look for the log "say question now". It will speak saying "Was your question: what colour is the sky?" and if you reply "yes", it will ask ChatGPT and respond with the answer. If you reply "no", it will return to waiting for the key phrase.

