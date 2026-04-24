# 🎵 VibeFinder Lite — Applied AI Music Recommender

## Project Overview

This repo extends the original Module 1-3 project, **Music Recommender Simulation**, into a polished applied AI system. The original base project was a content-based recommender that scored songs by energy, mood, acousticness, and genre.

Base project: **Music Recommender Simulation** from Modules 1-3.

The new version is an agentic music recommendation assistant that:

- uses the **Claude API** to parse natural language listening requests into structured preferences,
- retrieves candidate songs from a structured catalog,
- scores and ranks songs with multi-step reasoning,
- validates results with a confidence score and guardrails, and
- uses Claude to generate a natural language explanation of why each playlist was recommended.

This project remains grounded in the original song catalog from `data/songs.csv` while adding a more interactive AI workflow.

## What’s Included

- `src/claude_client.py` — Claude API integration: mood parsing (structured output) and recommendation explanation (streaming)
- `src/recommender.py` — core scoring, mode-based ranking, and diversity penalty
- `src/system.py` — agentic request parser, retrieval, validation, and confidence scoring
- `src/main.py` — command-line entrypoint with both profile-driven and natural-language agent demos
- `src/evaluator.py` — reliability harness for synthetic intent tests
- `app.py` — polished Streamlit web UI with Claude-powered natural language tab
- `tests/test_recommender.py` — baseline recommender unit tests
- `tests/test_system.py` — agent parsing and recommendation tests
- `data/songs.csv` — enriched song catalog with mood, tags, and listening context
- `model_card.md` — system documentation and ethical notes
- `reflection.md` — lessons learned and reliability findings

## Architecture Overview

The system is designed around four core components:

1. **Claude Intent Parser** (`src/claude_client.py` + `src/system.py`) — sends the user's natural language request to `claude-opus-4-7` with a structured JSON output schema to extract mood, energy, genre, context, and other preferences. Falls back to keyword matching if the API key is not set.
2. **Retriever** (`RecommendationAgent.retrieve_relevant_songs`) — selects candidate songs using metadata and keyword matching.
3. **Recommender** (`src/recommender.py`) — scores candidates with weighted features, applies diversity penalties, and ranks the top songs.
4. **Claude Explanation** (`src/claude_client.py`) — after ranking, calls Claude via streaming to write a warm 2–3 sentence explanation of why the playlist matches the user's request.

A validation step checks alignment with the requested mood or context and adjusts recommendations if needed.

## Feature Coverage

This project implements the full rubric for the final applied AI system:

- **Claude API Integration**: natural language mood input is parsed by `claude-opus-4-7` using structured outputs (Pydantic schema), and Claude generates a personalized explanation for each recommendation result.
- **Retrieval-Augmented Generation (RAG)**: the system retrieves relevant song documents from the catalog and custom genre notes before ranking recommendations.
- **Agentic Workflow**: the system plans, retrieves, scores, ranks, validates, and reports confidence for each recommendation request.
- **Specialized Model**: the recommender supports specialized listening profiles such as study, party, workout, relax, and night.
- **Reliability Testing**: the repository includes unit tests and a synthetic evaluator harness that measures alignment, confidence, and retrieval behavior.

## Stretch Features

The project also includes stretch enhancements for extra points:

- **RAG Enhancement**: custom external genre notes in `data/genre_notes.csv` are used as a second document source for retrieval.
- **Agentic Workflow Enhancement**: the system exposes retrieval and validation steps, including intermediate document retrieval, scoring, and mood-first fallback behavior.
- **Fine-Tuning / Specialization**: listening situation profiles adjust model weights for study, party, workout, relax, and night use cases.
- **Tone / Response Style Adaptation**: the agent can detect company, friendly, or casual tone cues and adapt recommendation phrasing accordingly.
- **Test Harness / Evaluation Script**: `src/evaluator.py` runs predefined requests and reports pass/fail outcomes, confidence levels, and alignment notes.

## Core AI Features

- **Claude API — Structured Mood Parsing**: natural language input (e.g. "I'm feeling nostalgic and melancholic tonight") is sent to `claude-opus-4-7` with a Pydantic JSON schema, which returns validated structured preferences (mood, energy, genre, context, tags). The system prompt is prompt-cached to reduce latency on repeated requests. Falls back to keyword matching if `ANTHROPIC_API_KEY` is not set.
- **Claude API — Recommendation Explanation**: after ranking songs, Claude streams a 2–3 sentence explanation of why the playlist fits the user's request. Shown in the "Why these songs?" section of the web app.
- **Retrieval-Augmented Generation (RAG)**: the agent retrieves relevant song documents from the catalog and custom genre notes before scoring, grounding recommendations in retrieved metadata, mood tags, context, and external genre guidance.
- **Agentic Workflow**: the system parses the request, retrieves candidate documents, scores songs, ranks them, and validates the final output with confidence checks.
- **Specialized Model Behavior**: tuned recommendation profiles are applied for study, party, workout, relax, and night listening situations.
- **Reliability System**: the evaluation harness runs synthetic natural-language cases and reports mood/context alignment and confidence for each case.

```mermaid
flowchart TD
    A[User Request] --> B[Claude Intent Parser\nclaude-opus-4-7]
    B --> C[Candidate Retriever]
    C --> D[Scoring Engine]
    D --> E[Ranking + Diversity Filter]
    E --> F[Validation + Confidence]
    F --> G[Claude Explanation\nstreaming]
    G --> H[User Output]
    subgraph Reliability
      I[Evaluation Harness]
    end
    H --> I
```

![System Architecture](assets/system_diagram.png)

## Setup Instructions

1. Create and activate a Python environment.
2. Install requirements:

```bash
pip install -r requirements.txt
```

3. Set your Anthropic API key (required for Claude-powered parsing and explanations):

```bash
export ANTHROPIC_API_KEY=your_key_here
```

> Without this key the app still works — it falls back to keyword-based parsing and skips the AI explanation.

4. Run the main app:

```bash
python3 -m src.main
```

5. Run tests:

```bash
python3 -m pytest -q
```

6. Run the reliability evaluator:

```bash
python3 -m src.evaluator
```

7. Run the interactive web app:

```bash
streamlit run app.py
```

## Sample Interactions

### Profile-based recommendations

Run the main app:

```bash
python3 -m src.main
```

Example output from the core profile-based runner:

```text
================================================================================
🎵 High-Energy Pop - Top 5 Recommendations
================================================================================

📋 User Profile:
   • Mood: HAPPY
   • Energy Level: 0.9 (0=chill, 1=intense)
   • Preference: ELECTRONIC
   • Favorite Genre: POP
   • Era: 2020s
   • Scoring Mode: balanced

--------------------------------------------------------------------------------
Rank | Title                    | Artist             | Genre        | Mood      | Score  
-----------------------------------------------------------------------------------------
1    | Sunrise City             | Neon Echo          | pop          | happy     | 0.887  
2    | Electric Dream           | Synth Wave         | house        | happy     | 0.825  
3    | Rooftop Lights           | Indigo Parade      | indie pop    | happy     | 0.765  
```

### Natural language recommendations

The new agent also supports requests like:

- `Recommend upbeat party music for a happy listener who loves electronic pop and bright energy.`
- `I want calm study songs with a chill mood and dreamy textures for coffee work.`
- `Give me intense workout tracks with strong rock or pop energy and aggressive mood tags.`
- `Find sad but powerful night music that is emotional and vocal-heavy.`

Example output for a natural language request:

```text
Request: Recommend upbeat party music for a happy listener who loves electronic pop and bright energy.
Mode: genre-first
Confidence: 0.87
1. Sunrise City by Neon Echo (pop, happy) - 0.887
2. Electric Dream by Synth Wave (house, happy) - 0.825
```

### Reliability evaluator output

Run the synthetic reliability test:

```bash
python3 -m src.evaluator
```

Example summary:

```text
RELIABILITY EVALUATION SUMMARY
--------------------------------
Case 1: Recommend upbeat party music for a happy listener who loves electronic pop and bright energy.
  Top song: Sunrise City
  Mood match: True | Context match: True | Confidence: 0.87 | Passed: True

Case 2: I want calm study songs with a chill mood and dreamy textures for coffee work.
  Top song: Midnight Coding
  Mood match: True | Context match: True | Confidence: 0.67 | Passed: True

Case 3: Give me intense workout tracks with strong rock or pop energy and aggressive mood tags.
  Top song: Gym Hero
  Mood match: True | Context match: True | Confidence: 0.87 | Passed: True

Case 4: Find sad but powerful night music that is emotional and vocal-heavy.
  Top song: Midnight Blues
  Mood match: True | Context match: True | Confidence: 0.60 | Passed: False

3/4 cases fully passed the reliability check.
```
## Design Decisions

- **Agentic workflow**: I built a parser/retriever/validator pipeline to make the recommendation process explicit and debuggable.
- **Retrieval step**: song metadata is used as the knowledge source, making recommendations grounded in the catalog rather than a purely template-based response.
- **Confidence scoring**: each result includes a simple confidence estimate based on top-song alignment with requested mood/context.
- **Guardrails**: the system checks the first recommendation and retries with a mood-first fallback if needed.

## Reliability and Testing

The project includes:

- unit tests for basic recommender behavior and request parsing
- an evaluation harness in `src/evaluator.py` that runs synthetic intent cases
- confidence scoring to quantify how well the recommendations align with intent
- logging for fallback behavior and retrieval decisions

Example summary from the evaluator:

- 4 synthetic cases were tested
- 3/4 cases passed the mood/context and confidence checks
- the system reports when the top song is not a strong match and uses fallback validation

## Testing Summary

- `pytest -q` passed all current tests.
- `python3 -m src.main` produces profile-based recommendations, agentic natural-language output, and confidence scores.
- `python3 -m src.evaluator` runs a synthetic reliability harness and reports pass/fail alignment for mood, context, and confidence.

## Reflection

This project taught me how a simple recommendation model can be extended into an AI system by adding retrieval and validation. The biggest gain was making the decision flow visible: parse intent, fetch candidates, score, and check alignment. It also highlighted the importance of transparency when the dataset is small — the system can only be as reliable as the catalog it uses.

## Presentation & Portfolio

- GitHub project: https://github.com/kneha07/applied-ai-music-system
- Loom walkthrough: https://www.loom.com/share/4190bc0d238745ada35a814a835d8754
- This video should show the system running end-to-end, including:
  - profile-based recommendation output
  - natural language agent request output
  - reliability evaluator summary
  - the system diagram and design rationale

### Portfolio Reflection

This project shows that I can take a prototype recommender from a course assignment and turn it into a complete applied AI system. I designed the pipeline to be explainable, added retrieval and agentic validation layers, and built a real interactive web app for demonstration. It also shows I care about reliability and responsible design by including testing, confidence scoring, and explicit documentation of limitations.

## Next Improvements

- add more songs and richer metadata to improve coverage
- support conversational feedback loops so Claude can ask clarifying questions
- add an embedding-based retriever for deeper semantic matching
- use Claude tool use to let the agent query the catalog dynamically
