import os
import json
import re
import requests
from typing import Optional
from django.conf import settings
from core.domain.interfaces import SolutionEvaluator
from core.domain.enums import (
    EvaluationCategory,
    FeedbackSource,
    FeedbackSeverity,
    CATEGORY_TITLES
)
from core.domain.models import (
    DomainSolution,
    DomainProblem,
    DomainEvaluationResult,
    DomainFeedbackItem
)
from core.services.evaluators.base import (
    AIProviderException,
    InvalidEvaluationOutputException
)

class AIEvaluator(SolutionEvaluator):
    """
    LLM-powered Low-Level Design Evaluator supporting DeepSeek, OpenAI, and Google Gemini.
    Provides in-depth qualitative evaluation, SOLID reasoning, and actionable feedback.
    """

    def __init__(self, api_key: Optional[str] = None, provider: Optional[str] = None, model: Optional[str] = None):
        self.gemini_key = api_key or getattr(settings, 'GEMINI_API_KEY', '') or os.getenv('GEMINI_API_KEY', '')
        self.openai_key = api_key or getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
        self.deepseek_key = api_key or getattr(settings, 'DEEPSEEK_API_KEY', '') or os.getenv('DEEPSEEK_API_KEY', '')
        self.custom_base_url = getattr(settings, 'AI_BASE_URL', '') or os.getenv('AI_BASE_URL', '')

        # Auto-detect active provider
        if provider:
            self.provider = provider.lower()
        elif self.deepseek_key:
            self.provider = "deepseek"
        elif self.openai_key:
            self.provider = "openai"
        elif self.gemini_key:
            self.provider = "gemini"
        else:
            self.provider = "none"

        # Model selection
        if model:
            self.model = model
        elif self.provider == "deepseek":
            self.model = getattr(settings, 'DEEPSEEK_MODEL', 'deepseek-chat')
        elif self.provider == "gemini":
            self.model = getattr(settings, 'GEMINI_MODEL', 'gemini-1.5-flash')
        else:
            self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o-mini')

    def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
        if self.provider == "none":
            raise AIProviderException("No AI API key configured (DEEPSEEK_API_KEY, OPENAI_API_KEY, or GEMINI_API_KEY missing).")

        prompt = self._build_evaluation_prompt(solution, problem)
        
        try:
            if self.provider == "deepseek":
                raw_response = self._call_deepseek(prompt)
            elif self.provider == "gemini":
                raw_response = self._call_gemini(prompt)
            elif self.provider == "openai":
                raw_response = self._call_openai(prompt)
            else:
                raise AIProviderException(f"Unsupported AI provider: {self.provider}")
            
            return self._parse_ai_response(raw_response)
        except Exception as e:
            if isinstance(e, (AIProviderException, InvalidEvaluationOutputException)):
                raise
            raise AIProviderException(f"AI evaluation request failed: {str(e)}")

    def _build_evaluation_prompt(self, solution: DomainSolution, problem: DomainProblem) -> str:
        classes_data = []
        for c in solution.classes:
            classes_data.append({
                "name": c.name,
                "is_interface": c.is_interface,
                "is_abstract": c.is_abstract,
                "responsibility": c.responsibility,
                "attributes": [{"name": a.name, "type": a.type, "visibility": a.visibility} for a in c.attributes],
                "methods": [{"name": m.name, "return_type": m.return_type, "params": m.params, "visibility": m.visibility} for m in c.methods],
                "relationships": [{"target": r.target, "type": r.type, "multiplicity": r.multiplicity} for r in c.relationships],
                "interfaces_implemented": c.interfaces_implemented
            })

        reqs_data = [{"code": r.req_code, "title": r.title, "description": r.description} for r in problem.requirements]

        prompt_dict = {
            "task": "You are a Principal Software Engineer and Staff LLD Interviewer evaluating a candidate's Low-Level Design submission.",
            "problem": {
                "title": problem.title,
                "difficulty": problem.difficulty.value,
                "problem_statement": problem.problem_statement,
                "requirements": reqs_data,
                "constraints": problem.constraints,
                "expected_design_considerations": problem.expected_design_considerations
            },
            "candidate_submission": {
                "summary": solution.summary,
                "assumptions_and_tradeoffs": solution.assumptions_and_tradeoffs,
                "design_patterns_used": solution.design_patterns_used,
                "mermaid_diagram": solution.mermaid_diagram,
                "classes": classes_data
            },
            "instructions": (
                "Evaluate the submission across 9 categories. Be constructive, explain *why* something can be improved, "
                "and give concrete, actionable design suggestions (e.g. 'Move payment responsibility to a dedicated PaymentService strategy because...'). "
                "Respond ONLY with a valid JSON object matching the requested schema."
            )
        }

        schema_format = """
Respond with a JSON object strictly adhering to this rubric structure (criterion -> score -> evidence -> concern -> suggestion -> confidence):
{
  "overall_score": 85,
  "overall_summary": "Comprehensive explanation of the design's strengths and areas for evolution.",
  "strengths": ["Strengths 1", "Strengths 2"],
  "improvement_areas": ["Improvement 1", "Improvement 2"],
  "actionable_recommendations": [
    "Move X from ClassA to ClassB because...",
    "Introduce Strategy pattern for Y to decouple..."
  ],
  "category_scores": {
    "requirements_coverage": {
      "criterion": "Requirements Coverage",
      "score": 9,
      "max_score": 10,
      "evidence": "Candidate defined ParkingLot, Spot, Ticket classes covering REQ-1 through REQ-4.",
      "concern": "No class or method models dynamic pricing calculations for REQ-5.",
      "suggestion": "Introduce a PricingStrategy interface with FlatRateStrategy and HourlyStrategy.",
      "confidence": "HIGH",
      "rationale": "Strong coverage of core entities with a minor gap in dynamic pricing."
    },
    "responsibility_assignment": {
      "criterion": "Responsibility Assignment (SRP)",
      "score": 8,
      "max_score": 10,
      "evidence": "ParkingLot class contains 8 methods spanning spot search, ticketing, and barrier hardware.",
      "concern": "ParkingLot acts as a God Object with multiple reasons to change.",
      "suggestion": "Extract PaymentService and GateController to uphold Single Responsibility Principle.",
      "confidence": "HIGH",
      "rationale": "Good class granularity overall but central facade is slightly bloated."
    },
    "abstraction_and_interfaces": {
      "criterion": "Abstraction & Interfaces",
      "score": 8,
      "max_score": 10,
      "evidence": "Defined PaymentProcessor and AllocationStrategy interfaces.",
      "concern": "Vehicle hierarchy is concrete without abstract vehicle contracts.",
      "suggestion": "Convert Vehicle into an abstract base class with polymorphic getDimension() methods.",
      "confidence": "HIGH",
      "rationale": "Appropriate interfaces defined for primary volatile behaviors."
    },
    "solid_principles": {
      "criterion": "SOLID Principles Adherence",
      "score": 8,
      "max_score": 10,
      "evidence": "Strategy pattern used for spot allocation upholds Open/Closed Principle.",
      "concern": "Direct dependency on concrete CashPaymentProcessor violates Dependency Inversion.",
      "suggestion": "Inject PaymentProcessor interface into ExitGate via constructor injection.",
      "confidence": "HIGH",
      "rationale": "Solid adherence to OCP and SRP with a minor DIP violation in gate flow."
    },
    "coupling_and_cohesion": {
      "criterion": "Coupling & Cohesion",
      "score": 8,
      "max_score": 10,
      "evidence": "ParkingFloor encapsulates spots tightly with minimal leaky abstractions.",
      "concern": "Bi-directional reference between Spot and Ticket creates unnecessary coupling.",
      "suggestion": "Remove Ticket reference from Spot; keep relationship unidirectional.",
      "confidence": "HIGH",
      "rationale": "High internal cohesion across floor and spot models."
    },
    "extensibility": {
      "criterion": "Extensibility & Modularity",
      "score": 9,
      "max_score": 10,
      "evidence": "Pluggable allocation strategies allow new algorithms without modifying ParkingLot.",
      "concern": "Adding electric charging spots will require updating spot type switches.",
      "suggestion": "Use factory pattern or polymorphism for spot capabilities.",
      "confidence": "HIGH",
      "rationale": "Excellent extensibility for new business rules."
    },
    "design_patterns": {
      "criterion": "Design Patterns & Best Practices",
      "score": 8,
      "max_score": 10,
      "evidence": "Strategy pattern and Observer pattern correctly declared and structured.",
      "concern": "Singleton pattern on ParkingLot makes multi-facility scaling difficult.",
      "suggestion": "Prefer dependency injection over static singleton instances for testability.",
      "confidence": "HIGH",
      "rationale": "Patterns applied solve genuine domain problems."
    },
    "edge_cases": {
      "criterion": "Edge Cases, Concurrency & Failure Modes",
      "score": 7,
      "max_score": 10,
      "evidence": "Trade-offs section notes in-memory mutex locking for concurrent gates.",
      "concern": "Does not handle hardware barrier communication timeout or full capacity edge cases.",
      "suggestion": "Document fallback behavior when all floors reach 100% capacity.",
      "confidence": "MEDIUM",
      "rationale": "Good initial concurrency considerations; expand on hardware fault tolerance."
    },
    "overall_explanation": {
      "criterion": "Architecture Explanation & Trade-offs",
      "score": 9,
      "max_score": 10,
      "evidence": "Clear walkthrough of entry gate to exit gate lifecycle in summary text.",
      "concern": "Assumptions do not specify whether parking fee grace periods exist.",
      "suggestion": "Document assumptions on lost ticket handling and grace periods.",
      "confidence": "HIGH",
      "rationale": "Well-articulated request lifecycle walkthrough and architectural trade-offs."
    }
  },
  "feedback_items": [
    {
      "category": "responsibility_assignment",
      "severity": "WARNING",
      "title": "God Class Risk in ParkingLot",
      "message": "ParkingLot is managing spot allocation, payment calculation, and gate operations.",
      "target_entity": "ParkingLot",
      "suggestion": "Extract PaymentService and GateController."
    }
  ]
}
"""
        return f"{json.dumps(prompt_dict, indent=2)}\n\n{schema_format}"

    def _call_deepseek(self, prompt: str) -> str:
        base_url = self.custom_base_url or "https://api.deepseek.com/chat/completions"
        if not base_url.endswith("/chat/completions"):
            base_url = base_url.rstrip("/") + "/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.deepseek_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert LLD evaluator. Respond only in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = requests.post(base_url, headers=headers, json=payload, timeout=25)
        if resp.status_code != 200:
            raise AIProviderException(f"DeepSeek API returned status {resp.status_code}: {resp.text}")
        
        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            raise AIProviderException("DeepSeek returned empty choices.")
        
        return choices[0].get("message", {}).get("content", "")

    def _call_gemini(self, prompt: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json"
            }
        }
        resp = requests.post(url, json=payload, timeout=25)
        if resp.status_code != 200:
            raise AIProviderException(f"Gemini API returned status {resp.status_code}: {resp.text}")
        
        data = resp.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise AIProviderException("Gemini returned empty candidate list.")
        
        text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        return text

    def _call_openai(self, prompt: str) -> str:
        base_url = self.custom_base_url or "https://api.openai.com/v1/chat/completions"
        if not base_url.endswith("/chat/completions"):
            base_url = base_url.rstrip("/") + "/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert LLD evaluator. Respond only in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2
        }
        resp = requests.post(base_url, headers=headers, json=payload, timeout=25)
        if resp.status_code != 200:
            raise AIProviderException(f"OpenAI API returned status {resp.status_code}: {resp.text}")
        
        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            raise AIProviderException("OpenAI returned empty choices.")
        
        return choices[0].get("message", {}).get("content", "")

    def _parse_ai_response(self, raw_text: str) -> DomainEvaluationResult:
        cleaned_text = raw_text.strip()
        if cleaned_text.startswith("```"):
            cleaned_text = re.sub(r"^```(?:json)?", "", cleaned_text)
            cleaned_text = re.sub(r"```$", "", cleaned_text).strip()

        try:
            data = json.loads(cleaned_text)
        except Exception as e:
            raise InvalidEvaluationOutputException(f"Could not parse AI response as JSON: {str(e)}\nRaw: {raw_text[:200]}")

        overall_score = data.get("overall_score", 75)
        overall_summary = data.get("overall_summary", "Evaluation complete.")
        strengths = data.get("strengths", [])
        improvement_areas = data.get("improvement_areas", [])
        actionable_recommendations = data.get("actionable_recommendations", [])
        
        raw_category_scores = data.get("category_scores", {})
        formatted_category_scores = {}
        for cat in EvaluationCategory:
            cat_data = raw_category_scores.get(cat.value, {})
            formatted_category_scores[cat.value] = {
                "title": CATEGORY_TITLES.get(cat, cat.value),
                "criterion": cat_data.get("criterion", CATEGORY_TITLES.get(cat, cat.value)),
                "score": int(cat_data.get("score", 7)),
                "max_score": int(cat_data.get("max_score", 10)),
                "evidence": cat_data.get("evidence", ""),
                "concern": cat_data.get("concern", ""),
                "suggestion": cat_data.get("suggestion", ""),
                "confidence": cat_data.get("confidence", "HIGH"),
                "rationale": cat_data.get("rationale", "")
            }

        feedback_items: list[DomainFeedbackItem] = []
        for item in data.get("feedback_items", []):
            try:
                category_enum = EvaluationCategory(item.get("category", EvaluationCategory.OVERALL_EXPLANATION.value))
            except ValueError:
                category_enum = EvaluationCategory.OVERALL_EXPLANATION

            try:
                severity_enum = FeedbackSeverity(item.get("severity", FeedbackSeverity.INFO.value))
            except ValueError:
                severity_enum = FeedbackSeverity.INFO

            feedback_items.append(DomainFeedbackItem(
                category=category_enum,
                source=FeedbackSource.AI_SUGGESTION,
                severity=severity_enum,
                title=item.get("title", "AI Design Feedback"),
                message=item.get("message", ""),
                target_entity=item.get("target_entity"),
                suggestion=item.get("suggestion")
            ))

        return DomainEvaluationResult(
            evaluator_type=f"AI_{self.provider.upper()}",
            overall_score=overall_score,
            overall_summary=overall_summary,
            strengths=strengths,
            improvement_areas=improvement_areas,
            actionable_recommendations=actionable_recommendations,
            category_scores=formatted_category_scores,
            feedback_items=feedback_items,
            is_fallback=False,
            raw_response=raw_text
        )
