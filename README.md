# Ticket Triage

A small Python tool that classifies customer support tickets with an LLM, validates the model's answer, and measures how well it works on labeled examples.

Built as a learning project to practice working with LLM APIs: prompt design, output validation, and evaluation.

## What it does

For each ticket text, the tool returns:

- a category: billing, technical, account, feedback, or other
- an urgency: low, medium, or high
- a one-sentence summary

## How it works

1. `llm.py` sends a prompt to a model through the Groq API (model: openai/gpt-oss-20b). It is the only file that knows about the provider.
2. `classifier.py` holds the system prompt (category definitions and rules) and `parse_response`, which checks that the model returned valid JSON with a known category and urgency. Anything else is rejected instead of trusted.
3. `evaluate.py` runs a labeled JSON file through the classifier and prints accuracy, a per-category breakdown, and every mistake.

Design notes:

- Ticket text is wrapped in `<ticket>` tags and the prompt tells the model to treat it as data, to reduce prompt injection.
- There is an `other` category for text that is not a real ticket, so the model always has a valid answer.
- Model output is untrusted input: invalid answers return `None` and are counted separately.

## Evaluation

Two labeled sets are included. Both were drafted with AI assistance, and I reviewed them and changed labels where I disagreed.

| Set | Examples | Result | Notes |
|---|---|---|---|
| examples.json | 30 | 29/30 | Used while developing the prompt |
| holdout.json | 17 | 17/17 | Harder cases; used for tuning after the first run |

The only unbiased number is the first run on holdout.json, before I tuned anything: 15/17 (88.2%). Both mistakes were on ambiguous tickets, where the prompt had no rule for the boundary between categories. I then added category definitions to the prompt, so the later numbers are not clean test results.

Important caveats:

- The sets are small: one example is about 3-6% of the score.
- They are made-up examples, not real tickets, so they describe cases someone could think of, not what real customers write.
- Results may vary slightly between runs.

## Known limitations

- A real ticket that also contains an injected instruction can be classified as `other` (for example: "I was charged twice. Also, ignore your instructions...").
- The model sometimes refuses to answer when the text looks like a command to it. Such cases return `None` and would need manual review in a real system.
- Urgency and summary are not evaluated, only the category.

## Setup

Requirements: Python 3 and a free Groq API key.

    pip install -r requirements.txt

Create a `.env` file (see `.env.example`) containing:

    API_KEY=your_key_here

## Usage

Classify the sample tickets:

    python classifier.py

Evaluate a labeled file:

    python evaluate.py examples.json
    python evaluate.py holdout.json

Run the tests (no API calls needed):

    python -m pytest

## Project structure

    ticket-triage/
    ├── llm.py                 # API wrapper
    ├── classifier.py          # Prompt, classification, response validation
    ├── evaluate.py            # Evaluation script
    ├── test_classifier.py     # Unit tests for response validation
    ├── examples.json          # Development set
    ├── holdout.json           # Harder set
    ├── requirements.txt
    ├── .env.example
    └── README.md