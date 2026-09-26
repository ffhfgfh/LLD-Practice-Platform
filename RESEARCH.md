# RESEARCH.md — Low-Level Design (LLD) Practice & Evaluation Research

## 1. Executive Summary & Problem Context

Software engineering interviews and professional career progression place heavy emphasis on **Low-Level Design (LLD) and Object-Oriented Design (OOD)**. While algorithmic platforms (e.g., LeetCode, HackerRank, Codeforces) have standardized practice for Data Structures & Algorithms (DSA), practicing Low-Level Design remains fragmented, unstructured, and devoid of rapid feedback loops.

Learners preparing for LLD interviews typically face three core challenges:
1. **Subjectivity & Ambiguity**: Unlike DSA where automated unit tests provide a binary pass/fail signal, LLD problems have multiple valid structural solutions with nuanced trade-offs (e.g., choosing between Strategy vs State pattern, or deciding where to encapsulate payment workflows).
2. **Lack of Explainable Feedback**: Traditional preparation involves passively reading static blog posts, GitHub repositories, or YouTube videos. When learners attempt to write their own designs, they have no mechanism to evaluate Single Responsibility Principle (SRP) violations, God Object risks, dangling abstractions, or missing concurrency edge cases.
3. **Improper Practice Tools**: General UML diagramming tools (Lucidchart, Draw.io) focus on visual aesthetics rather than semantic domain modeling, while general text editors lack structural validation against problem requirements.

---

## 2. Analysis of Existing Approaches

| Category | Existing Solutions | Strengths | Critical Gaps in LLD Context |
| :--- | :--- | :--- | :--- |
| **Algorithmic Practice Platforms** | LeetCode, HackerRank, CodeSignal | Objective evaluation, automated test runner, instant feedback, clear problem statements. | Binary pass/fail mindset fails in architecture; cannot evaluate object relationships, class cohesion, or design patterns. |
| **Static LLD Preparation Resources** | GitHub Repos (e.g., *ts-lld*, *awesome-lld*), Grokking OOD, YouTube channels | Comprehensive reference solutions for canonical problems (Parking Lot, Elevator, Vending Machine). | Passive consumption without interactive active-recall practice; no critique on learner's own design attempts; outdated code samples. |
| **Visual Diagramming Tools** | Lucidchart, Draw.io, PlantUML, Eraser.io | Great for visual representation and exportable architectural diagrams. | Pure drawing canvases with zero semantic evaluation, no requirement coverage verification, and no automated feedback. |
| **General AI Code Review Tools** | ChatGPT, GitHub Copilot, Cursor | Qualitative commentary and natural language reasoning. | High hallucination risk, inconsistent evaluation criteria, lack of structured domain category scoring, and no iterative attempt history tracking. |

---

## 3. Key Observations & Design Insights

### Observation 1: The Fallacy of Binary Pass/Fail in Architecture
In Low-Level Design, multiple design topologies can be correct depending on stated constraints and trade-offs. For instance, in a Parking Lot system:
- Modeling `SpotAllocation` inside `ParkingLot` is acceptable for a monolithic single-gate prototype.
- Extracting `SpotAllocationStrategy` with `NearestSpotStrategy` and `LowestFloorFirstStrategy` is superior for enterprise multi-floor commercial complexes.

An effective LLD evaluation platform must not grade designs as binary pass/fail. Instead, it must grade across **orthogonal architectural dimensions** (Requirements Coverage, Responsibility Assignment, Abstraction Quality, SOLID Principles, Extensibility, Edge Cases) with textual reasoning explaining *why* a particular refactoring improves cohesion.

### Observation 2: Deterministic Verification is Essential for Ground Truth
Relying solely on LLMs for grading creates non-deterministic inconsistency (the same solution might receive an 85 on Monday and a 65 on Tuesday). Conversely, deterministic static analysis can reliably verify:
- Presence of required domain entities and explicit responsibilities.
- Integrity of relationship references (catching dangling references to non-existent classes).
- Polymorphism and interface declarations.
- Keyword and entity coverage against stated problem requirements.

### Observation 3: AI is Best Utilized for Qualitative Reasoning
While deterministic checks enforce structural discipline, Large Language Models excel at semantic nuance:
- Evaluating whether a responsibility description genuinely represents a single reason to change.
- Identifying subtle coupling risks (e.g., `ParkingLot` directly handling card payment gateway hardware).
- Suggesting actionable, human-like refactorings (*"Extract PaymentService to decouple monetary transactions from physical spot state"*).

---

## 4. Product Direction & Value Proposition

Based on these research findings, the **LLD Practice Platform** was architected around four core pillars:

1. **Active Iterative Practice Workflow**:
   - Structured domain collection (Classes, Responsibilities, Methods, Attributes, Relationships, Interfaces, Architecture summary, Design patterns) paired with live Mermaid diagram rendering.
   - Immutable attempt history enabling learners to review past attempts and "Try Again" without losing historical progress.

2. **Dual-Layer Evaluation Engine (Composite Evaluator)**:
   - **Deterministic Engine**: Runs first to generate reliable baseline facts, requirement matching, and structural integrity scores.
   - **AI Reasoning Layer**: Plugs in via an abstract interface to provide qualitative design critique, SOLID guidance, and actionable next steps.

3. **Graceful Fault Tolerance**:
   - If AI APIs timeout or have no credentials, the system automatically falls back to deterministic analysis, guaranteeing the learner never loses their submission or encounters a broken UI.

4. **Explainability Over Scoring**:
   - Scores are paired with detailed textual rationales, concrete strengths ("What you did well"), improvement areas ("Areas for growth"), and explicit entity-targeted refactoring suggestions.
