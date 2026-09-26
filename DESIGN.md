# DESIGN.md — LLD Practice Platform Architecture & Domain Design

## 1. System Overview & Architecture

The **LLD Practice Platform** is built as a clean, modular, and testable monolithic web application. It bridges the gap between passive LLD study and active engineering interview practice by combining structured object-oriented design authoring with explainable deterministic and AI-powered feedback.

```mermaid
flowchart TD
    subgraph Frontend["Frontend (React 19 + TypeScript + Vite + Tailwind CSS)"]
        UI_Dash["Dashboard & Catalog"]
        UI_Studio["Practice Workspace (Class Studio + Mermaid + Flow)"]
        UI_Eval["Feedback & Evaluation Breakdown"]
        UI_Hist["Attempt History & Comparison"]
    end

    subgraph REST_API["REST API Layer (Django REST Framework)"]
        API_Problems["/api/problems/"]
        API_Attempts["/api/attempts/ (:id, submit, evaluate)"]
        API_History["/api/history/"]
        API_Dashboard["/api/dashboard/"]
    end

    subgraph Service_Layer["Application Service Layer"]
        AttemptService["AttemptService (Lifecycle, Drafts, Immutability)"]
        EvalService["EvaluationService (Orchestration & State Transitions)"]
    end

    subgraph Evaluator_Engine["Evaluator Subsystem (Strategy & Composite Pattern)"]
        EvaluatorInterface["<<interface>> SolutionEvaluator"]
        RuleBasedEvaluator["RuleBasedEvaluator (Deterministic Static Analysis)"]
        AIEvaluator["AIEvaluator (Gemini / OpenAI Provider Bridge)"]
        CompositeEvaluator["CompositeEvaluator (Blended Scoring & Graceful Fallback)"]
    end

    subgraph Persistence["Storage Layer (SQLite / PostgreSQL)"]
        DB_Problems[(LLDProblem & Requirements)]
        DB_Attempts[(PracticeAttempt & Solution & ClassDesign)]
        DB_Evaluations[(Evaluation & FeedbackItem)]
    end

    Frontend -->|HTTP / JSON| REST_API
    REST_API --> Service_Layer
    Service_Layer --> Evaluator_Engine
    Service_Layer --> Persistence
    Evaluator_Engine -.-> EvaluatorInterface
    CompositeEvaluator --> RuleBasedEvaluator
    CompositeEvaluator --> AIEvaluator
```

---

## 2. The Core Learner Journey

```mermaid
sequenceDiagram
    autonumber
    actor Learner
    participant UI as React Frontend
    participant API as REST API / Services
    participant Eval as Evaluator Engine
    participant DB as Database

    Learner->>UI: Select LLD Problem (e.g. Parking Lot)
    UI->>API: GET /api/problems/parking-lot/
    API-->>UI: Return Requirements, Constraints & Hints
    
    Learner->>UI: Click "Start New Attempt"
    UI->>API: POST /api/attempts/ (problem_id)
    API->>DB: Create PracticeAttempt(status=DRAFT, attempt_number=N)
    API-->>UI: Return Attempt ID & Initial Solution Shell
    
    Learner->>UI: Define Classes, Responsibilities, Methods & Flow
    UI->>API: PUT /api/attempts/:id/ (Save Draft)
    API->>DB: Update Solution & ClassDesign records
    
    Learner->>UI: Click "Submit & Evaluate"
    UI->>API: POST /api/attempts/:id/submit/
    API->>API: Validate completeness (classes > 0, SRP non-empty, summary > 20 chars)
    API->>DB: Set status = SUBMITTED -> EVALUATING
    API->>Eval: Execute CompositeEvaluator(solution, problem)
    Eval->>Eval: 1. RuleBasedEvaluator (8 deterministic checks)
    Eval->>Eval: 2. AIEvaluator (LLM reasoning & qualitative review)
    Eval-->>API: DomainEvaluationResult
    API->>DB: Save Evaluation & FeedbackItem records; status = COMPLETED
    API-->>UI: Return Completed Attempt & Evaluation
    
    UI-->>Learner: Display Scores, Strengths, Growth Areas & Actionable Steps
    Learner->>UI: Click "Try Again"
    UI->>API: POST /api/attempts/ (creates Attempt #N+1 without mutating old attempt)
```

---

## 3. Domain Model Design

The core domain is structured around clean data classes and interfaces located in `backend/core/domain/`, decoupled from framework-specific ORM concerns.

### 3.1 Domain Entities

```mermaid
classDiagram
    class DomainProblem {
        +String id
        +String slug
        +String title
        +Difficulty difficulty
        +String problem_statement
        +List~String~ constraints
        +List~String~ expected_design_considerations
        +List~DomainRequirement~ requirements
    }

    class DomainRequirement {
        +String req_code
        +String title
        +String description
        +String category
        +List~String~ keywords
    }

    class DomainSolution {
        +String summary
        +String assumptions_and_tradeoffs
        +List~String~ design_patterns_used
        +String mermaid_diagram
        +List~DomainClassDesign~ classes
    }

    class DomainClassDesign {
        +String name
        +String responsibility
        +Boolean is_interface
        +Boolean is_abstract
        +List~DomainAttribute~ attributes
        +List~DomainMethod~ methods
        +List~DomainRelationship~ relationships
        +List~String~ interfaces_implemented
    }

    class DomainEvaluationResult {
        +String evaluator_type
        +int overall_score
        +String overall_summary
        +List~String~ strengths
        +List~String~ improvement_areas
        +List~String~ actionable_recommendations
        +Map category_scores
        +List~DomainFeedbackItem~ feedback_items
        +Boolean is_fallback
    }

    DomainProblem *-- DomainRequirement
    DomainSolution *-- DomainClassDesign
```

---

## 4. Evaluator Architecture (Strategy & Composite Pattern)

To ensure the platform never hardcodes vendor lock-in or breaks when AI credentials are absent, evaluation is built around the **Dependency Inversion Principle (DIP)**:

```python
class SolutionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
        pass
```

### 4.1 Evaluation Implementations
1. **`RuleBasedEvaluator` (Deterministic Engine)**:
   - Evaluates 8 deterministic passes:
     - *Requirements Keyword & Semantic Mapping* (checks entity/method coverage against stated requirements).
     - *Single Responsibility Principle & God Class Detection* (identifies classes handling excessive methods or orthogonal domains).
     - *Abstraction & Interface Utilization* (verifies polymorphic contracts and interface implementation).
     - *SOLID Principles Compliance* (checks OCP, LSP, ISP, and DIP indicators).
     - *Coupling & Cohesion Analysis* (detects dangling class references where targets are missing).
     - *Design Pattern Verification* (validates claimed patterns against structural classes).
     - *Edge Cases & Concurrency Notes* (scans for race condition/locking considerations).
     - *Overall Architecture Explanation Clarity*.
2. **`AIEvaluator` (Qualitative Reasoning)**:
   - Provider-agnostic bridge supporting Google Gemini (`gemini-1.5-flash`) and OpenAI (`gpt-4o-mini`).
   - Sends structured prompt containing candidate classes, methods, relationships, diagram, and requirements.
   - Enforces strict JSON schema output mapping directly to `DomainEvaluationResult`.
3. **`CompositeEvaluator` (Hybrid Orchestrator)**:
   - Executes `RuleBasedEvaluator` for baseline ground truth.
   - Executes `AIEvaluator` inside a guarded try-except block.
   - Merges results (40% deterministic + 60% AI reasoning), deduplicates strengths and recommendations, and tags every finding with `DETERMINISTIC` or `AI_SUGGESTION`.
   - **Graceful Fallback**: If AI fails, times out, or has no API key, it seamlessly returns the deterministic result with `is_fallback=True`, ensuring learner work is never lost.

---

## 5. Attempt Lifecycle & Immutability

Practice attempts follow a strict state machine:

```mermaid
stateDiagram-v2
    [*] --> DRAFT: Create Attempt
    DRAFT --> DRAFT: Save Draft (PUT /api/attempts/:id/)
    DRAFT --> SUBMITTED: Submit (POST /api/attempts/:id/submit/)
    SUBMITTED --> EVALUATING: Evaluation Triggered
    EVALUATING --> COMPLETED: Successful Evaluation
    EVALUATING --> FAILED: Unexpected Error
    FAILED --> EVALUATING: Retry Evaluation (POST /api/attempts/:id/evaluate/)
    COMPLETED --> [*]: Immutable Past Attempt
```

### Immutability Invariant
Once an attempt transitions out of `DRAFT`, any subsequent `PUT` or `PATCH` request to modify classes or solution text is rejected with HTTP 400 (`"Cannot modify attempt in SUBMITTED/COMPLETED state. Submitted attempts are immutable."`).

To practice again, the learner uses the **Try Again** action, which instantiates a new `PracticeAttempt` with `attempt_number = N + 1` for the same problem. This preserves historical learning progression.

---

## 6. Key Architectural Trade-offs

| Decision | Chosen Approach | Alternative Considered | Engineering Rationale |
| :--- | :--- | :--- | :--- |
| **Architecture Topology** | Modular Monolith | Microservices (Auth, Evaluator, Problems) | A focused 2-day MVP prioritized domain correctness, explainable feedback, and fast local development over distributed microservice complexity. |
| **Evaluator Concurrency** | Synchronous service execution with fast LLM timeouts (25s) | Celery / Redis asynchronous worker queue | Avoids heavy Redis/worker dependencies for local evaluation while keeping the service layer decoupled so workers can be introduced later with zero view changes. |
| **Class Diagram Representation** | Mermaid JS markdown rendering + auto-sync from structured classes | Drag-and-drop canvas (e.g. React Flow / Fabric.js) | Structured classes guarantee semantic data for static evaluation, while Mermaid provides immediate, code-like visualization without high canvas complexity. |
| **Data Normalization** | Relational `LLDProblem`, `PracticeAttempt`, `Solution`, `ClassDesign`, `Evaluation`, and `FeedbackItem` | Single JSON Document in MongoDB | Relational integrity ensures strong querying, cascading deletion of attempts, and precise feedback item categorization. |
