#!/bin/bash

# Start Ollama in the background.
OLLAMA_HOST=0.0.0.0 /bin/ollama serve &

# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve Ollama model..."
ollama pull qwen3:4b    # thinking model
ollama pull gemma3:4b   # vision model
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid