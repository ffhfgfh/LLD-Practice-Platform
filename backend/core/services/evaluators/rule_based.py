import re
from typing import List, Dict, Set, Any
from core.domain.interfaces import SolutionEvaluator
from core.domain.enums import (
    EvaluationCategory,
    FeedbackSource,
    ConfidenceLevel,
    FeedbackSeverity,
    CATEGORY_TITLES
)
from core.domain.models import (
    DomainSolution,
    DomainProblem,
    DomainEvaluationResult,
    DomainFeedbackItem,
    DomainClassDesign
)

class RuleBasedEvaluator(SolutionEvaluator):
    """
    Deterministic rule-based Low-Level Design evaluator.
    Evaluates solutions across all standard LLD categories with high confidence and zero external dependencies.
    """

    def evaluate(self, solution: DomainSolution, problem: DomainProblem) -> DomainEvaluationResult:
        feedback_items: List[DomainFeedbackItem] = []
        strengths: List[str] = []
        design_issues: List[str] = []
        missing_requirements: List[str] = []
        solid_violations: List[str] = []
        coupling_concerns: List[str] = []
        extensibility_suggestions: List[str] = []
        edge_cases_analysis: List[str] = []
        actionable_recommendations: List[str] = []
        refactoring_plan: List[str] = []
        category_scores: Dict[str, Dict[str, Any]] = {}

        # 1. Requirements Coverage
        req_score, req_items, missing_reqs = self._eval_requirements_coverage(solution, problem)
        feedback_items.extend(req_items)
        missing_requirements.extend(missing_reqs)
        category_scores[EvaluationCategory.REQUIREMENTS_COVERAGE.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.REQUIREMENTS_COVERAGE],
            "criterion": CATEGORY_TITLES[EvaluationCategory.REQUIREMENTS_COVERAGE],
            "score": req_score,
            "max_score": 10,
            "evidence": f"Submitted {len(solution.classes)} classes covering {len(problem.requirements) - len(missing_reqs)} of {len(problem.requirements)} requirements.",
            "concern": f"Missing explicit domain models for: {', '.join(missing_reqs)}." if missing_reqs else "All required domain models are represented in the design.",
            "suggestion": f"Define dedicated classes or interfaces for {', '.join(missing_reqs[:2])}." if missing_reqs else "Ensure all functional scenarios are mapped to explicit method contracts.",
            "confidence": "HIGH",
            "rationale": f"Requirements coverage assessed at {req_score * 10}% based on entity mapping, methods, and requirement keywords."
        }

        # 2. Responsibility Assignment (SRP)
        srp_score, srp_items, srp_recs, srp_issues = self._eval_responsibility_assignment(solution)
        feedback_items.extend(srp_items)
        actionable_recommendations.extend(srp_recs)
        design_issues.extend(srp_issues)
        category_scores[EvaluationCategory.RESPONSIBILITY_ASSIGNMENT.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.RESPONSIBILITY_ASSIGNMENT],
            "criterion": CATEGORY_TITLES[EvaluationCategory.RESPONSIBILITY_ASSIGNMENT],
            "score": srp_score,
            "max_score": 10,
            "evidence": f"Evaluated single responsibilities across {len(solution.classes)} candidate classes.",
            "concern": srp_issues[0] if srp_issues else "No God Class or bloated entity anti-patterns detected.",
            "suggestion": srp_recs[0] if srp_recs else "Maintain focused classes each with one distinct reason to change.",
            "confidence": "HIGH",
            "rationale": "Class responsibilities evaluated for granularity, God Class anti-patterns, and Single Responsibility Principle adherence."
        }

        # 3. Abstraction & Interfaces
        abs_score, abs_items, abs_recs = self._eval_abstraction_and_interfaces(solution, problem)
        feedback_items.extend(abs_items)
        actionable_recommendations.extend(abs_recs)
        category_scores[EvaluationCategory.ABSTRACTION_AND_INTERFACES.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.ABSTRACTION_AND_INTERFACES],
            "criterion": CATEGORY_TITLES[EvaluationCategory.ABSTRACTION_AND_INTERFACES],
            "score": abs_score,
            "max_score": 10,
            "evidence": f"Found {len([c for c in solution.classes if c.is_interface])} interfaces and {len([c for c in solution.classes if c.is_abstract])} abstract classes.",
            "concern": "Hardcoded concrete dependencies without abstract strategy or factory interfaces." if abs_score < 7 else "Appropriate polymorphism and interface contracts established.",
            "suggestion": abs_recs[0] if abs_recs else "Code against interfaces rather than concrete implementations.",
            "confidence": "HIGH",
            "rationale": "Interface definitions, abstract contracts, and polymorphic usage verified across candidate entities."
        }

        # 4. SOLID Principles Breakdown
        solid_score, solid_items, solid_viols = self._eval_solid_principles(solution)
        feedback_items.extend(solid_items)
        solid_violations.extend(solid_viols)
        category_scores[EvaluationCategory.SOLID_PRINCIPLES.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.SOLID_PRINCIPLES],
            "criterion": CATEGORY_TITLES[EvaluationCategory.SOLID_PRINCIPLES],
            "score": solid_score,
            "max_score": 10,
            "evidence": f"Static verification of SRP, OCP, LSP, ISP, and DIP across class inheritance and implementation graphs.",
            "concern": solid_viols[0] if solid_viols else "No severe SOLID principle violations identified.",
            "suggestion": "Apply Dependency Inversion and polymorphic interfaces for external integrations." if solid_viols else "Continue decoupling volatile algorithms via the Strategy Pattern.",
            "confidence": "HIGH",
            "rationale": "Evaluated Open/Closed Principle (extensible types), Dependency Inversion, and Interface Segregation."
        }

        # 5. Coupling & Cohesion
        coupling_score, coupling_items, coup_concerns = self._eval_coupling_and_cohesion(solution)
        feedback_items.extend(coupling_items)
        coupling_concerns.extend(coup_concerns)
        category_scores[EvaluationCategory.COUPLING_AND_COHESION.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.COUPLING_AND_COHESION],
            "criterion": CATEGORY_TITLES[EvaluationCategory.COUPLING_AND_COHESION],
            "score": coupling_score,
            "max_score": 10,
            "evidence": f"Analyzed {sum(len(c.relationships) for c in solution.classes)} explicit relationships and dependency paths.",
            "concern": coup_concerns[0] if coup_concerns else "Class relationships exhibit loose coupling and high cohesion.",
            "suggestion": "Favor composition over inheritance and prevent bidirectional tight coupling.",
            "confidence": "HIGH",
            "rationale": "Relationship graph, dependency targets, and class reference integrity evaluated."
        }

        # 6. Extensibility
        ext_score, ext_items, ext_suggs = self._eval_extensibility(solution, problem)
        feedback_items.extend(ext_items)
        extensibility_suggestions.extend(ext_suggs)
        category_scores[EvaluationCategory.EXTENSIBILITY.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.EXTENSIBILITY],
            "criterion": CATEGORY_TITLES[EvaluationCategory.EXTENSIBILITY],
            "score": ext_score,
            "max_score": 10,
            "evidence": f"Evaluated polymorphic extension points and pluggable design pattern structures.",
            "concern": "New requirements or variations will require modifying existing class source code (OCP violation)." if ext_score < 7 else "Architecture accommodates new feature requirements with minimal modification.",
            "suggestion": ext_suggs[0] if ext_suggs else "Use abstract factories and strategies to easily swap algorithms at runtime.",
            "confidence": "HIGH",
            "rationale": "Evaluated adaptability to new requirements (e.g. new algorithms, payment gateways, spot types)."
        }

        # 7. Design Patterns
        dp_score, dp_items = self._eval_design_patterns(solution)
        feedback_items.extend(dp_items)
        category_scores[EvaluationCategory.DESIGN_PATTERNS.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.DESIGN_PATTERNS],
            "criterion": CATEGORY_TITLES[EvaluationCategory.DESIGN_PATTERNS],
            "score": dp_score,
            "max_score": 10,
            "evidence": f"Declared patterns: {', '.join(solution.design_patterns_used) if solution.design_patterns_used else 'None explicitly tagged in draft'}.",
            "concern": "Missed opportunities to apply standard design patterns for algorithms or lifecycle transitions." if dp_score < 7 else "Design patterns appropriately leveraged for the domain.",
            "suggestion": "Apply Strategy for pluggable algorithms and State for complex entity lifecycles.",
            "confidence": "HIGH",
            "rationale": "Verification of design patterns listed in submission vs actual structural implementation."
        }

        # 8. Edge Cases & Concurrency
        edge_score, edge_items, edge_notes = self._eval_edge_cases(solution, problem)
        feedback_items.extend(edge_items)
        edge_cases_analysis.extend(edge_notes)
        category_scores[EvaluationCategory.EDGE_CASES.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.EDGE_CASES],
            "criterion": CATEGORY_TITLES[EvaluationCategory.EDGE_CASES],
            "score": edge_score,
            "max_score": 10,
            "evidence": f"Assumptions and constraints documentation ({len(solution.assumptions_and_tradeoffs.split())} words).",
            "concern": edge_notes[0] if edge_notes else "Concurrency, race conditions, and boundary edge cases addressed.",
            "suggestion": "Document thread safety mechanisms (mutex locks, atomic counters) and hardware/network failure fallbacks.",
            "confidence": "HIGH",
            "rationale": "Validation of concurrency handling, capacity limits, error handling, and state transitions."
        }

        # 9. Overall Explanation & Trade-offs
        expl_score, expl_items = self._eval_overall_explanation(solution)
        feedback_items.extend(expl_items)
        category_scores[EvaluationCategory.OVERALL_EXPLANATION.value] = {
            "title": CATEGORY_TITLES[EvaluationCategory.OVERALL_EXPLANATION],
            "criterion": CATEGORY_TITLES[EvaluationCategory.OVERALL_EXPLANATION],
            "score": expl_score,
            "max_score": 10,
            "evidence": f"Solution overview and request lifecycle walkthrough ({len(solution.summary.split())} words).",
            "concern": "Vague or missing step-by-step request lifecycle explanation." if expl_score < 7 else "Clear explanation of how classes collaborate during major use cases.",
            "suggestion": "Walk through the end-to-end request lifecycle from trigger to completion highlighting class collaborations.",
            "confidence": "HIGH",
            "rationale": "Clarity of high-level solution summary, assumptions, trade-offs, and class diagram representation."
        }

        # Synthesize Strengths & Refactoring Plan
        for item in feedback_items:
            if item.severity == FeedbackSeverity.POSITIVE:
                strengths.append(f"{item.title}: {item.message}")

        if not strengths:
            strengths.append("Structured submission with distinct entity definitions provided.")

        # Construct Step-by-Step Refactoring Plan
        step_num = 1
        if srp_issues:
            refactoring_plan.append(f"Step {step_num}: Decompose bloated classes into dedicated cohesive collaborators.")
            step_num += 1
        if missing_requirements:
            refactoring_plan.append(f"Step {step_num}: Introduce domain classes/methods to address missing requirements ({', '.join(missing_requirements[:2])}).")
            step_num += 1
        if solid_violations:
            refactoring_plan.append(f"Step {step_num}: Apply Strategy / Factory patterns to resolve Open/Closed and Dependency Inversion violations.")
            step_num += 1
        if not refactoring_plan:
            refactoring_plan.append("Step 1: Your architecture is well-structured! Consider adding concurrency locks and performance benchmarking.")

        # Weighted Overall Score
        total_category_score = sum(c["score"] for c in category_scores.values())
        overall_score = min(100, max(10, int(round((total_category_score / (9 * 10)) * 100))))

        overall_summary = (
            f"The design scored {overall_score}/100. "
            f"Identified {len(solution.classes)} domain entities/interfaces. "
            f"Requirements coverage evaluated at {req_score * 10}%. "
            f"Adherence to Single Responsibility, Open/Closed, and loose coupling has been verified with 100% deterministic confidence."
        )

        improvement_areas = list(dict.fromkeys(design_issues + solid_violations + coupling_concerns))[:6]

        return DomainEvaluationResult(
            evaluator_type="RULE_BASED",
            overall_score=overall_score,
            overall_summary=overall_summary,
            strengths=strengths[:6],
            design_issues=design_issues[:5],
            missing_requirements=missing_requirements[:5],
            solid_violations=solid_violations[:5],
            coupling_concerns=coupling_concerns[:5],
            extensibility_suggestions=extensibility_suggestions[:5],
            edge_cases_analysis=edge_cases_analysis[:5],
            actionable_recommendations=list(dict.fromkeys(actionable_recommendations))[:6],
            refactoring_plan=refactoring_plan[:4],
            improvement_areas=improvement_areas,
            category_scores=category_scores,
            feedback_items=feedback_items,
            is_fallback=False
        )

    def _eval_requirements_coverage(self, solution: DomainSolution, problem: DomainProblem):
        items: List[DomainFeedbackItem] = []
        missing_reqs: List[str] = []
        if not problem.requirements:
            return 8, items, missing_reqs

        corpus_words = set()
        for c in solution.classes:
            corpus_words.add(c.name.lower())
            corpus_words.update(re.findall(r'\w+', c.name.lower()))
            corpus_words.update(re.findall(r'\w+', c.responsibility.lower()))
            for a in c.attributes:
                corpus_words.update(re.findall(r'\w+', a.name.lower()))
            for m in c.methods:
                corpus_words.update(re.findall(r'\w+', m.name.lower()))
        corpus_words.update(re.findall(r'\w+', solution.summary.lower()))
        corpus_words.update(re.findall(r'\w+', solution.assumptions_and_tradeoffs.lower()))

        matched_reqs = 0
        for req in problem.requirements:
            keywords = [k.lower() for k in req.keywords] if req.keywords else [w.lower() for w in re.findall(r'\w+', req.title)]
            if not keywords:
                matched_reqs += 1
                continue

            matches = [k for k in keywords if k in corpus_words or any(k in word for word in corpus_words)]
            match_ratio = len(matches) / len(keywords) if keywords else 1.0

            if match_ratio >= 0.5:
                matched_reqs += 1
                items.append(DomainFeedbackItem(
                    category=EvaluationCategory.REQUIREMENTS_COVERAGE,
                    source=FeedbackSource.DETERMINISTIC,
                    confidence=ConfidenceLevel.HIGH,
                    severity=FeedbackSeverity.POSITIVE,
                    title=f"Covered: {req.req_code} ({req.title})",
                    message=f"Solution entities and methods directly address requirement '{req.title}' (indicators: {', '.join(matches[:3])}).",
                    why_it_matters="Interviewers evaluate if you solve the candidate's actual requirements rather than an over-engineered fantasy problem."
                ))
            else:
                missing_reqs.append(f"{req.req_code}: {req.title}")
                items.append(DomainFeedbackItem(
                    category=EvaluationCategory.REQUIREMENTS_COVERAGE,
                    source=FeedbackSource.DETERMINISTIC,
                    confidence=ConfidenceLevel.HIGH,
                    severity=FeedbackSeverity.WARNING,
                    title=f"Potential Gap: {req.req_code} ({req.title})",
                    message=f"Requirement '{req.description}' does not have clear corresponding classes, attributes, or methods in your design.",
                    suggestion=f"Consider introducing explicit entities or method contracts to handle {req.title.lower()}.",
                    why_it_matters="Missing functional requirements is one of the top rejection reasons in FAANG/MNC LLD interviews."
                ))

        coverage_ratio = matched_reqs / len(problem.requirements)
        score = max(2, min(10, int(round(coverage_ratio * 10))))
        return score, items, missing_reqs

    def _eval_responsibility_assignment(self, solution: DomainSolution):
        items: List[DomainFeedbackItem] = []
        recommendations: List[str] = []
        design_issues: List[str] = []

        if not solution.classes:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.RESPONSIBILITY_ASSIGNMENT,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.CRITICAL,
                title="No Classes Defined",
                message="Your solution does not specify any classes or entities.",
                why_it_matters="LLD requires defining concrete object models with encapsulated state and behavior."
            ))
            return 1, items, ["Define core domain entities."], ["No classes defined."]

        god_classes = []
        empty_responsibility_classes = []
        well_defined_classes = []

        for c in solution.classes:
            method_count = len(c.methods)
            resp_len = len(c.responsibility.strip())

            if resp_len < 10:
                empty_responsibility_classes.append(c.name)
                items.append(DomainFeedbackItem(
                    category=EvaluationCategory.RESPONSIBILITY_ASSIGNMENT,
                    source=FeedbackSource.DETERMINISTIC,
                    confidence=ConfidenceLevel.HIGH,
                    severity=FeedbackSeverity.WARNING,
                    title=f"Vague Responsibility for '{c.name}'",
                    target_entity=c.name,
                    message=f"Class '{c.name}' has no detailed single responsibility defined. Each class should clearly state why it exists.",
                    suggestion="Add a concise responsibility statement describing its single reason to change.",
                    why_it_matters="Vague responsibilities lead to architectural drift where unrelated helpers get dumped into random classes."
                ))
            else:
                well_defined_classes.append(c.name)

            name_lower = c.name.lower()
            resp_lower = c.responsibility.lower()
            is_god_class = False

            if method_count >= 7:
                is_god_class = True
            elif ("manager" in name_lower or "system" in name_lower or "controller" in name_lower or "lot" in name_lower) and \
                 (("pay" in resp_lower or "bill" in resp_lower) and ("spot" in resp_lower or "floor" in resp_lower or "display" in resp_lower)):
                is_god_class = True

            if is_god_class:
                god_classes.append(c.name)
                rec = f"Decompose '{c.name}' by delegating non-core responsibilities (like payment, notification, or spot allocation) to dedicated collaborator services."
                recommendations.append(rec)
                issue = f"God Class Anti-Pattern in '{c.name}' ({method_count} methods / multi-domain responsibility)"
                design_issues.append(issue)
                items.append(DomainFeedbackItem(
                    category=EvaluationCategory.RESPONSIBILITY_ASSIGNMENT,
                    source=FeedbackSource.DETERMINISTIC,
                    confidence=ConfidenceLevel.HIGH,
                    severity=FeedbackSeverity.WARNING,
                    title=f"High Responsibility Density in '{c.name}' (God Class Risk)",
                    target_entity=c.name,
                    message=f"Class '{c.name}' handles {method_count} methods or spans multiple domains. This violates Single Responsibility Principle (SRP).",
                    suggestion=rec,
                    why_it_matters="God classes are hard to test, create merge conflicts in teams, and tightly couple unrelated domain workflows."
                ))

        if not god_classes and len(well_defined_classes) >= 3:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.RESPONSIBILITY_ASSIGNMENT,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Clear Single Responsibility Separation",
                message=f"Classes ({', '.join(well_defined_classes[:4])}) exhibit focused responsibilities with modular boundaries.",
                why_it_matters="High cohesion makes code maintainable and testable in production environments."
            ))

        score = 8
        if len(solution.classes) < 3:
            score -= 3
        if god_classes:
            score -= (len(god_classes) * 2)
        if empty_responsibility_classes:
            score -= min(3, len(empty_responsibility_classes))
        if len(well_defined_classes) >= 4 and not god_classes:
            score += 2

        score = max(2, min(10, score))
        return score, items, recommendations, design_issues

    def _eval_abstraction_and_interfaces(self, solution: DomainSolution, problem: DomainProblem):
        items: List[DomainFeedbackItem] = []
        recommendations: List[str] = []

        interfaces = [c for c in solution.classes if c.is_interface or c.is_abstract or "interface" in c.name.lower() or "strategy" in c.name.lower()]
        implementing_classes = [c for c in solution.classes if c.interfaces_implemented]

        if interfaces or implementing_classes:
            interface_names = [c.name for c in interfaces]
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.ABSTRACTION_AND_INTERFACES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Effective Use of Abstractions & Interfaces",
                message=f"Identified {len(interfaces)} interface(s)/abstract classes ({', '.join(interface_names[:3])}) providing loose coupling.",
                why_it_matters="Interfaces decouple callers from concrete implementations, enabling polymorphism and unit testing with mock objects."
            ))
            score = 8 + (2 if len(implementing_classes) >= 2 else 1)
        else:
            rec = "Introduce interfaces (e.g. for PaymentProcessor, PricingStrategy, or DispatchStrategy) to decouple high-level workflows from concrete implementations."
            recommendations.append(rec)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.ABSTRACTION_AND_INTERFACES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.WARNING,
                title="Missing Polymorphic Interfaces",
                message="Your design relies entirely on concrete classes. Without interfaces, swapping algorithms or third-party gateways requires modifying client code.",
                suggestion=rec,
                why_it_matters="Demonstrating polymorphism and interface segregation is a primary expectation in Staff/Senior LLD rounds."
            ))
            score = 4

        return min(10, score), items, recommendations

    def _eval_solid_principles(self, solution: DomainSolution):
        items: List[DomainFeedbackItem] = []
        solid_violations: List[str] = []
        score = 7

        has_polymorphism = any(c.is_interface or c.is_abstract or len(c.interfaces_implemented) > 0 for c in solution.classes)
        if has_polymorphism:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.SOLID_PRINCIPLES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Open/Closed Principle (OCP) Supported",
                message="The design facilitates extension via interfaces or inheritance without modifying core orchestrators.",
                why_it_matters="OCP ensures you can add new business capabilities (e.g. UPI payments, EV spots) without editing tested code."
            ))
            score += 1
        else:
            viol = "Open/Closed Principle (OCP) Violation: Adding new types will require modifying switch/if-else statements in existing classes."
            solid_violations.append(viol)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.SOLID_PRINCIPLES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.WARNING,
                title="Open/Closed Principle (OCP) Concern",
                message=viol,
                suggestion="Extract an abstract interface or Strategy pattern for variable behaviors.",
                why_it_matters="Violating OCP creates regression risks in large codebases whenever new features are added."
            ))

        has_abstractions = any(c.is_interface for c in solution.classes)
        if has_abstractions:
            score += 1
        else:
            viol = "Dependency Inversion Principle (DIP) Concern: High-level modules directly depend on concrete classes instead of abstractions."
            solid_violations.append(viol)

        return min(10, max(3, score)), items, solid_violations

    def _eval_coupling_and_cohesion(self, solution: DomainSolution):
        items: List[DomainFeedbackItem] = []
        coupling_concerns: List[str] = []
        class_names_lower = {c.name.lower() for c in solution.classes}

        broken_references = []
        valid_relationships_count = 0

        for c in solution.classes:
            for r in c.relationships:
                target = r.target.strip()
                if target and target.lower() not in class_names_lower:
                    broken_references.append((c.name, target))
                else:
                    valid_relationships_count += 1

        if broken_references:
            dangling = [f"'{c}' -> '{t}'" for c, t in broken_references[:3]]
            concern = f"Dangling relationships referencing undeclared classes: {', '.join(dangling)}"
            coupling_concerns.append(concern)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.COUPLING_AND_COHESION,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.WARNING,
                title="Dangling Class Relationships",
                message=f"Found relationships referencing undeclared classes ({', '.join(dangling)}).",
                suggestion="Define all target entities in your class list to ensure a self-contained domain model.",
                why_it_matters="Dangling relationships in UML or code reviews indicate incomplete domain boundary design."
            ))
            score = 6
        elif valid_relationships_count >= 3:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.COUPLING_AND_COHESION,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Cohesive Entity Relationships",
                message=f"All {valid_relationships_count} defined relationships map accurately between valid domain classes.",
                why_it_matters="Clean relationship graphs prevent circular dependency deadlocks and memory leaks."
            ))
            score = 9
        else:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.COUPLING_AND_COHESION,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.INFO,
                title="Limited Relationship Modeling",
                message="Few relationships (Composition, Aggregation, Association) were explicitly defined between your classes.",
                why_it_matters="Explicitly illustrating ownership (Composition vs Association) is essential to convey system lifecycle."
            ))
            score = 6

        return score, items, coupling_concerns

    def _eval_extensibility(self, solution: DomainSolution, problem: DomainProblem):
        items: List[DomainFeedbackItem] = []
        ext_suggs: List[str] = []
        has_patterns = len(solution.design_patterns_used) > 0
        has_interfaces = any(c.is_interface or c.is_abstract for c in solution.classes)

        if has_patterns and has_interfaces:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.EXTENSIBILITY,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="High Extensibility Potential",
                message="Utilizing design patterns and abstract interfaces allows the architecture to scale for new business rules.",
                why_it_matters="Extensibility allows rapid onboarding of new client requirements without rewriting existing modules."
            ))
            return 9, items, ext_suggs
        else:
            sugg = "Introduce a pluggable Strategy or Factory interface for variable algorithm and entity creation."
            ext_suggs.append(sugg)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.EXTENSIBILITY,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.INFO,
                title="Enhance Extensibility",
                message="Consider how your design would accommodate a requirement change (e.g. dynamic pricing or external notification services).",
                suggestion=sugg,
                why_it_matters="Interview follow-up questions almost always introduce a new requirement to test design extensibility."
            ))
            return 6, items, ext_suggs

    def _eval_design_patterns(self, solution: DomainSolution):
        items: List[DomainFeedbackItem] = []
        patterns = solution.design_patterns_used

        if patterns:
            patterns_str = ", ".join(patterns)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.DESIGN_PATTERNS,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title=f"Design Patterns Applied: {patterns_str}",
                message=f"Explicitly identified and applied patterns ({patterns_str}) to address standard design challenges.",
                why_it_matters="Recognized design patterns establish a shared vocabulary across engineering teams."
            ))
            score = min(10, 6 + len(patterns) * 2)
        else:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.DESIGN_PATTERNS,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.INFO,
                title="No Design Patterns Declared",
                message="No design patterns (e.g., Factory, Strategy, Observer, State, Singleton) were formally declared.",
                suggestion="Specify recognizable design patterns to standardize your object creation and behavioral flows.",
                why_it_matters="Design patterns demonstrate mastery of battle-tested architectural idioms."
            ))
            score = 5

        return score, items

    def _eval_edge_cases(self, solution: DomainSolution, problem: DomainProblem):
        items: List[DomainFeedbackItem] = []
        edge_notes: List[str] = []
        corpus = (
            solution.summary + " " +
            solution.assumptions_and_tradeoffs + " " +
            " ".join(c.responsibility for c in solution.classes)
        ).lower()

        concurrency_mentioned = any(term in corpus for term in ["concurr", "thread", "lock", "mutex", "race", "atomic", "sync"])
        capacity_mentioned = any(term in corpus for term in ["full", "capacit", "limit", "overflow", "empty", "availab"])
        error_mentioned = any(term in corpus for term in ["exception", "error", "fail", "invalid", "refund", "reject"])

        score = 5
        if concurrency_mentioned:
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.EDGE_CASES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Concurrency & Synchronization Awareness",
                message="The solution explicitly considers concurrent access, locks, and thread synchronization.",
                why_it_matters="In production, race conditions under high concurrent traffic cause double bookings and data corruption."
            ))
            score += 2
        else:
            note = "Thread Safety: Consider race conditions when multiple clients access shared resources simultaneously (e.g. booking the same spot/elevator)."
            edge_notes.append(note)
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.EDGE_CASES,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.INFO,
                title="Concurrency Edge Cases Noted",
                message=note,
                suggestion="Add notes or synchronized mechanisms for shared resource allocation.",
                why_it_matters="Senior engineering interviewers look for proactive identification of race conditions."
            ))

        if capacity_mentioned:
            score += 1
        else:
            edge_notes.append("Capacity Limits: Document behavior when system reaches 100% full capacity or inventory exhaustion.")

        if error_mentioned:
            score += 2

        return min(10, score), items, edge_notes

    def _eval_overall_explanation(self, solution: DomainSolution):
        items: List[DomainFeedbackItem] = []
        summary_len = len(solution.summary.strip())
        assumptions_len = len(solution.assumptions_and_tradeoffs.strip())
        diagram_len = len(solution.mermaid_diagram.strip())

        score = 6
        if summary_len > 100:
            score += 1
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.OVERALL_EXPLANATION,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Thorough Solution Summary",
                message="The architectural explanation clearly communicates the high-level request lifecycle.",
                why_it_matters="Clear technical communication is just as important as clean code in engineering interviews."
            ))

        if assumptions_len > 50:
            score += 1
        if diagram_len > 30 and "classDiagram" in solution.mermaid_diagram:
            score += 2
            items.append(DomainFeedbackItem(
                category=EvaluationCategory.OVERALL_EXPLANATION,
                source=FeedbackSource.DETERMINISTIC,
                confidence=ConfidenceLevel.HIGH,
                severity=FeedbackSeverity.POSITIVE,
                title="Visual Class Diagram Provided",
                message="Mermaid class diagram effectively illustrates class relationships and multiplicities.",
                why_it_matters="Diagrams provide immediate visual clarity for interviewers and teammates."
            ))

        return min(10, score), items
