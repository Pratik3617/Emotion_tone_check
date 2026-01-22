# Emotion-Aware Tone & Risk Analyzer

A production-grade NLP + GenAI service that analyzes emotional tone in text, evaluates communication risk, and suggests safer rewrites using a **hybrid rule-based + LLM architecture**.

This project is designed to help prevent misunderstandings, escalation, and unintended aggression in written communication (e.g., workplace messages, emails, chats).

---

## Key Features

* **Multi-label emotion detection** (28 emotions)
* **Tone aggregation** (positive / neutral / negative)
* **Risk calibration** using business rules
* **Hybrid rewrite engine**

  * Rules/templates for medium risk
  * **LLM-powered rewrites for high-risk messages**
* **FastAPI service** with validation & error handling
* **End-to-end tests** (pipeline + API)
* **Dockerized deployment**
* **Production logging**
* Designed for **safe, explainable GenAI usage**

---

## System Design (High Level)

```
Input Text
   ↓
Emotion Classification Model
   ↓
Tone Aggregation
   ↓
Risk Scoring (rules + keywords)
   ↓
Rewrite Decision Gate
   ├── Low Risk    → No rewrite
   ├── Medium Risk → Template-based rewrite
   └── High Risk   → LLM-generated rewrite (guarded)
```

> The LLM is **never called blindly**.
> Deterministic rules decide *when* and *how* generation is allowed.

---

## ✨ Example

### Input

```json
{
  "text": "Please fix this immediately, this is unacceptable."
}
```

### Output

```json
{
  "tone": "negative",
  "risk_level": "high",
  "suggested_rewrite": "I’m concerned about this issue and would appreciate a quick update so we can resolve it together.",
  "requires_attention": true
}
```

---


## Tech Stack

* **Python 3.10**
* **PyTorch**
* **Hugging Face Transformers**
* **FastAPI**
* **Pydantic**
* **Docker**
* **pytest**
* **OpenAI API** (for rewrite generation)

---


## Running Locally

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Set environment variable

```bash
export OPENAI_API_KEY="your_api_key_here"
```

### 3️⃣ Start API

```bash
uvicorn app.main:app --reload
```

### 4️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## Running Tests

```bash
pytest
```

Tests include:

* Pipeline behavior tests
* API contract tests
* Validation edge cases

---

## Docker

### Build image

```bash
docker build -t emotion-tone-check .
```

### Run container

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY="your_api_key_here" \
  emotion-tone-check

```

Access:

```
http://localhost:8000/docs
```

---


## What This Project Demonstrates

* Applied NLP
* Safe & explainable GenAI integration
* Production API design
* Testing strategy for ML systems
* Clean separation of concerns
* Real-world engineering tradeoffs

---

## 🔮 Future Improvements

* Context-aware rewrites (work / personal)
* Style control (formal / casual)
* Confidence scoring for rewrites
* Rate limiting
* CI/CD (GitHub Actions)
* UI demo

---

## 📄 License

MIT License

---
