from typing import List
from core.domain.interfaces import SubmissionValidator
from core.domain.models import DomainSolution, DomainProblem

class DefaultSubmissionValidator(SubmissionValidator):
    """
    Standard submission validator enforcing Low-Level Design domain rules before evaluation.
    Collects all validation errors comprehensively without early termination.
    """

    def validate(self, solution: DomainSolution, problem: DomainProblem) -> List[str]:
        errors: List[str] = []

        if not solution:
            errors.append("No solution submitted.")
            return errors

        # Validate classes presence
        if not solution.classes or len(solution.classes) == 0:
            errors.append("At least one class or interface entity must be defined in your solution.")
        else:
            # Validate class names and responsibilities
            empty_names = [idx + 1 for idx, c in enumerate(solution.classes) if not c.name.strip()]
            if empty_names:
                errors.append(f"Classes at position(s) {empty_names} are missing a class name.")

            empty_resps = [c.name or f"Class #{idx+1}" for idx, c in enumerate(solution.classes) if len(c.responsibility.strip()) < 8]
            if empty_resps:
                errors.append(f"Entities ({', '.join(empty_resps[:4])}) must have a clear Single Responsibility explanation (min 8 characters).")

            # Check for circular/self relationships
            for c in solution.classes:
                for rel in c.relationships:
                    if rel.target.strip() == c.name.strip() and rel.type in ['INHERITANCE', 'COMPOSITION']:
                        errors.append(f"Class '{c.name}' cannot have a self-{rel.type.lower()} relationship to itself.")

        # Validate solution summary
        if not solution.summary or len(solution.summary.strip()) < 20:
            errors.append("Please provide a solution summary (minimum 20 characters) explaining the overall architecture and data flow.")

        return errors
