# Assignments for CS146S: The Modern Software Developer

This is the home of the assignments for [CS146S: The Modern Software Developer](https://themodernsoftware.dev), taught at Stanford University fall 2025.

## Repo Setup
These steps work with Python 3.12.

1. Install Anaconda
   - Download and install: [Anaconda Individual Edition](https://www.anaconda.com/download)
   - Open a new terminal so `conda` is on your `PATH`.

2. Create and activate a Conda environment (Python 3.12)
   ```bash
   conda create -n cs146s python=3.12 -y
   conda activate cs146s
   ```

3. Install Poetry
   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```

4. Install project dependencies with Poetry (inside the activated Conda env)
   From the repository root:
   ```bash
   poetry install --no-interaction
   ```

   ## New: AI Extraction Feature

   This app now supports extracting action items from notes using **AI LLMs** (Large Language Models)!
   
   - **Heuristic Extraction**: The original rule-based extraction remains available.
   - **AI LLM Extraction (Llama 3 via Ollama)**: You can leverage an AI model to extract action items, often with higher accuracy and flexibility for natural language inputs.

   In the web UI, try both “Extract (Heuristic)” and “Extract (AI LLM)” to compare approaches.

   ### API Endpoints

   - `POST /action-items/extract`
     - Extract action items from the given text (heuristic rules).
   - `POST /action-items/extract-llm`
     - Extract action items using the Llama 3 model via Ollama backend.

   Be sure that you have [Ollama](https://ollama.com/) installed and running with the appropriate model (`llama3`) for LLM extraction to work.
