# LLD Practice Platform 🏗️

> **Interactive Low-Level Design (LLD) Mastery & Interview Preparation Platform**
> Practice canonical object-oriented design problems, structure classes and responsibilities, visualize Mermaid class diagrams, receive explainable deterministic and AI-assisted feedback across 9 design dimensions, and iterate through attempt history.

---

## 🌟 Key Highlights & Features

- **End-to-End Learner Journey**:
  `Choose Problem` &rarr; `View Requirements` &rarr; `Start Attempt` &rarr; `Design Solution` &rarr; `Submit` &rarr; `Evaluation` &rarr; `Explainable Feedback` &rarr; `Review History` &rarr; `Try Again`.
- **10 Canonical Seeded LLD Challenges**:
  1. **Parking Lot System** (Medium, ~45m) — Multi-vehicle types, spot sizing, multi-floor capacity, automated ticketing gates, dynamic pricing strategies, spot allocation algorithms.
  2. **Elevator System** (Hard, ~60m) — Multi-car elevator bank, internal/external hall calls, SCAN/LOOK dispatching strategy, motion state machine, door & weight sensors.
  3. **Vending Machine System** (Easy, ~30m) — Product inventory slots, state-driven transaction execution, multi-denomination cash balance, optimal coin change calculation, transaction rollbacks.
  4. **Library Management System** (Medium, ~45m) — Abstract Book vs physical BookItem copies, membership tiers & borrowing quotas, FIFO hold queues, fine calculation strategies, catalog search.
  5. **Splitwise (Expense Sharing System)** (Medium, ~45m) — Multi-user groups, Equal/Exact/Percentage splits, real-time balance sheets, min-cash-flow debt simplification graph algorithm.
  6. **Movie Ticket Booking (BookMyShow)** (Hard, ~60m) — Cinema halls, tiered seat layouts, high-concurrency temporary seat locking with TTL, dynamic pricing, and payment confirmation.
  7. **Snake and Ladder Board Game** (Easy, ~30m) — Configurable $N$-cell board, polymorphic jump entities (Snakes/Ladders), pluggable dice rolling strategies, FIFO player turn rotation.
  8. **Automated Teller Machine (ATM)** (Medium, ~45m) — Hardware abstraction, state-pattern session lifecycle, Chain of Responsibility cash note dispensing ($100, $50, $20, $10), PIN lockout.
  9. **Rate Limiter & API Throttling Library** (Hard, ~60m) — Pluggable throttling algorithms (Token Bucket, Sliding Window Counter), multi-tier client quotas, thread-safe atomic execution.
  10. **Chess Game Engine** (Hard, ~60m) — 8x8 board, polymorphic piece movement rules (King, Queen, Rook, Bishop, Knight, Pawn), move validation, check/checkmate detection, and Command-pattern move history.
- **Rich Practice Workspace**:
  - **Class Design Studio**: Add/edit/remove classes, single responsibilities (SRP), typed methods, attributes, and relationships (Composition, Aggregation, Inheritance, Implementation).
  - **Live Mermaid Class Diagram**: Live SVG rendering of class diagrams with an instant **"Sync from Classes"** generator.
  - **Architecture & Trade-offs**: Free-form request lifecycle explanation, assumptions, and multi-select design pattern pills (Strategy, Factory, Observer, State, Singleton, Command, etc.).
- **Dual-Layer Explainable Evaluation**:
  - **Deterministic Engine (`RuleBasedEvaluator`)**: Evaluates 8 static checks (requirements keyword coverage, God class detection, interface polymorphism, relationship integrity, SOLID compliance, edge cases).
  - **AI Reasoning Layer (`AIEvaluator`)**: Plugs into Google Gemini or OpenAI to provide deep qualitative critique, nuance on coupling/cohesion, and actionable recommendations (*"Move payment processing from ParkingLot to PaymentService because..."*).
  - **Graceful Fallback (`CompositeEvaluator`)**: Automatically falls back to deterministic analysis if AI APIs are unconfigured or fail—learner work is never lost.
- **Attempt History & Progression**:
  - Immutable past attempts.
  - Grouped attempts by problem with comparative score progression and "Try Again" re-attempts.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons, Mermaid.js, Axios, React Router v7 |
| **Backend** | Python 3.13, Django 6, Django REST Framework, Django CORS Headers |
| **Database** | SQLite (default for development/demo) / PostgreSQL ready |
| **Evaluation** | Abstract `SolutionEvaluator` supporting `RuleBasedEvaluator`, `AIEvaluator` (Gemini / OpenAI), and `CompositeEvaluator` |
| **Testing** | Pytest, Pytest-Django, Vite build runner |

---

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup

```bash
# Navigate to backend (or project root with virtual environment)
cd backend

# Create and activate virtual environment (Windows)
python -m venv venv
.\venv\Scripts\activate

# (Linux / macOS)
# python3 -m venv venv
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations and seed LLD problems
python manage.py makemigrations core
python manage.py migrate
python manage.py seed_data

# Start Django development server (runs on http://127.0.0.1:8000)
python manage.py runserver
```

### 2. Frontend Setup

In a separate terminal window:

```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite development server (runs on http://localhost:5173)
npm run dev
```

Open your browser at **`http://localhost:5173`**.

---

## ⚙️ Environment Variables Configuration

Copy `.env.example` to `.env` in the root or `backend/` directory:

```env
# Django Settings
SECRET_KEY=django-insecure-lld-practice-platform-secret-key-2026
DEBUG=True

# Evaluator Provider Configuration
# Options: 'composite' (default), 'rule_based', 'gemini', 'openai'
EVALUATOR_TYPE=composite

# AI Provider API Keys (Optional - deterministic evaluation works even if empty)
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# AI Model Overrides
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4o-mini
```

> **Note**: If no `GEMINI_API_KEY` or `OPENAI_API_KEY` is provided, the platform automatically runs in deterministic evaluation mode. Zero configuration required to test the complete user journey!

---

## 🧪 Running Automated Tests

Run backend unit and integration tests using pytest:

```bash
# Run all tests in backend
.\venv\Scripts\pytest backend -v
```

### Test Coverage Summary:
- `test_evaluators.py`: Unit tests for `RuleBasedEvaluator`, God class detection, `CompositeEvaluator` fallback, and `SolutionEvaluator` abstraction substitution.
- `test_services.py`: Tests for `AttemptService` lifecycle, draft saving, submission validation, attempt immutability rules, and state transitions.
- `test_api.py`: Integration tests for `/api/problems/`, `/api/attempts/`, draft saving, submit & evaluate endpoint, history, and dashboard.

To test the frontend TypeScript build:

```bash
cd frontend
npm run build
```

---

## 📡 REST API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/dashboard/` | High-level learner statistics, recent attempts, recommended problems |
| `GET` | `/api/problems/` | List all problems (supports `?difficulty=` and `?search=`) |
| `GET` | `/api/problems/:id/` | Get full problem statement, requirements, constraints, hints |
| `POST` | `/api/attempts/` | Create a new practice attempt (`{ "problem_id": "..." }`) |
| `GET` | `/api/attempts/:id/` | Retrieve attempt with solution, class designs, and evaluation |
| `PUT` | `/api/attempts/:id/` | Save draft solution & classes (only allowed while in `DRAFT` state) |
| `POST` | `/api/attempts/:id/submit/` | Validate and submit attempt; executes evaluation immediately |
| `POST` | `/api/attempts/:id/evaluate/` | Retry evaluation on a submitted/failed attempt |
| `GET` | `/api/evaluations/:id/` | Get detailed evaluation results and feedback items |
| `GET` | `/api/history/` | Get all past attempts grouped by problem |

---

## 📂 Project Structure

```
project2/
├── backend/
│   ├── lld_platform/          # Django project settings & root URLs
│   ├── core/
│   │   ├── domain/            # Pure domain layer (models, enums, interfaces)
│   │   │   ├── enums.py       # Difficulty, AttemptStatus, EvaluationCategory
│   │   │   ├── models.py      # Dataclasses: DomainProblem, DomainSolution, etc.
│   │   │   └── interfaces.py  # SolutionEvaluator interface
│   │   ├── models.py          # Django ORM models
│   │   ├── serializers.py     # DRF serializers
│   │   ├── views.py           # REST API endpoints & ViewSets
│   │   ├── urls.py            # API routing
│   │   ├── services/          # Service layer
│   │   │   ├── attempt_service.py     # Attempt lifecycle & immutability
│   │   │   ├── evaluation_service.py  # Evaluation orchestration
│   │   │   └── evaluators/            # Strategy implementations
│   │   │       ├── base.py
│   │   │       ├── rule_based.py      # Deterministic 8-pass evaluator
│   │   │       ├── ai_evaluator.py    # Gemini & OpenAI evaluator
│   │   │       ├── composite_evaluator.py
│   │   │       └── factory.py
│   │   ├── management/commands/
│   │   │   └── seed_data.py   # Seeder for 4 complete LLD problems
│   │   └── tests/             # Automated test suite
│   ├── manage.py
│   ├── pytest.ini
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── types/             # TypeScript interfaces
│   │   ├── services/          # Typed API client
│   │   ├── components/
│   │   │   ├── layout/        # Navbar, Footer, Layout
│   │   │   ├── common/        # Badge, Button, Card, Spinner, ErrorAlert, StatCard
│   │   │   ├── problems/      # ProblemCard, RequirementsList, Details
│   │   │   ├── practice/      # ClassCard, ClassEditorModal, MermaidViewer, Architecture
│   │   │   ├── evaluation/    # ScoreCard, CategoryScores, Strengths, FeedbackList
│   │   │   └── history/       # AttemptHistoryCard, AttemptComparisonModal
│   │   ├── pages/             # Dashboard, ProblemList, ProblemDetail, Practice, Feedback, History
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
├── README.md
├── RESEARCH.md
├── DESIGN.md
├── AI_USAGE.md
└── .env.example
```

---

## 🎯 Verification & Demonstration Walkthrough

1. **Dashboard (`/`)**: View overview stats, recommended problems, and click **"Practice Now"** on Parking Lot.
2. **Problem Requirements (`/problems/parking-lot`)**: Review vehicle types, spot types, multi-floor constraints, design considerations, and hints. Click **"Start New Attempt"**.
3. **Practice Studio (`/practice/:attemptId`)**:
   - Add classes (e.g. `ParkingLot`, `ParkingSpot`, `Vehicle`, `SpotAllocationStrategy`).
   - Click **"Sync from Classes"** on the Mermaid Diagram tab to generate UML automatically.
   - Enter solution explanation and select design pattern pills (e.g. `Strategy`, `Factory`).
   - Click **"Save Draft"** &rarr; notice saved status.
   - Click **"Submit & Evaluate"**.
4. **Explainable Feedback (`/attempts/:attemptId/feedback`)**:
   - View overall score and 9-category breakdown.
   - Read **"What You Did Well"**, **"Areas for Growth"**, and **"Actionable Next Steps"**.
   - Filter feedback by **Deterministic Checks** vs **AI Suggestions**.
   - Click **"Review Submitted Solution"** to compare your solution with the feedback.
5. **Attempt History (`/attempts`)**:
   - View your attempts grouped by problem.
   - Click **"Try Again"** to launch Attempt #2 without overwriting Attempt #1.
#   L L D - P r a c t i c e - P l a t f o r m  
 