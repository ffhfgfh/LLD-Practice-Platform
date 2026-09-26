import pytest
from rest_framework.test import APIClient
from rest_framework import status
from core.models import LLDProblem, ProblemRequirement, PracticeAttempt
from core.domain.enums import Difficulty, AttemptStatus

@pytest.mark.django_db
class TestLLDPlatformAPI:
    @pytest.fixture(autouse=True)
    def setup_api(self):
        self.client = APIClient()
        self.problem = LLDProblem.objects.create(
            slug="vending-machine-api-test",
            title="Vending Machine API Test",
            difficulty=Difficulty.EASY.value,
            summary="A test vending machine problem",
            problem_statement="Problem details",
            constraints=["Test constraint"],
            expected_design_considerations=["State pattern"],
            hints=["Hint 1"]
        )
        ProblemRequirement.objects.create(
            problem=self.problem,
            req_code="REQ-1",
            title="Product Selection",
            description="Allow product selection",
            keywords=["Product", "Item", "selectProduct"],
            order=1
        )

    def test_get_problems_list(self):
        response = self.client.get('/api/problems/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
        problem_data = next(p for p in response.data if p['slug'] == self.problem.slug)
        assert problem_data['title'] == self.problem.title
        assert problem_data['requirements_count'] == 1

    def test_get_problem_by_slug(self):
        response = self.client.get(f'/api/problems/{self.problem.slug}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == self.problem.title
        assert len(response.data['requirements']) == 1

    def test_create_attempt_api(self):
        response = self.client.post('/api/attempts/', {'problem_id': str(self.problem.id)}, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == AttemptStatus.DRAFT.value
        assert response.data['attempt_number'] == 1
        assert response.data['solution'] is not None

    def test_save_draft_api(self):
        # Create attempt
        create_resp = self.client.post('/api/attempts/', {'problem_id': str(self.problem.id)}, format='json')
        attempt_id = create_resp.data['id']

        # Save draft
        draft_payload = {
            "solution": {
                "summary": "Vending machine architecture using State pattern.",
                "assumptions_and_tradeoffs": "Coin inventory is finite.",
                "design_patterns_used": ["State"],
                "mermaid_diagram": "classDiagram\n    VendingMachine --> State\n",
                "classes": [
                    {
                        "name": "VendingMachine",
                        "responsibility": "Context object holding current state and inventory.",
                        "attributes": [],
                        "methods": [{"name": "selectItem", "returnType": "void", "params": "string code"}],
                        "relationships": []
                    }
                ]
            }
        }
        save_resp = self.client.put(f'/api/attempts/{attempt_id}/', draft_payload, format='json')
        assert save_resp.status_code == status.HTTP_200_OK
        assert save_resp.data['solution']['summary'] == "Vending machine architecture using State pattern."
        assert len(save_resp.data['solution']['classes']) == 1

    def test_submit_and_evaluate_attempt_api(self):
        # Create and fill attempt
        create_resp = self.client.post('/api/attempts/', {'problem_id': str(self.problem.id)}, format='json')
        attempt_id = create_resp.data['id']

        self.client.put(f'/api/attempts/{attempt_id}/', {
            "solution": {
                "summary": "Complete vending machine design with State Pattern and Money management.",
                "assumptions_and_tradeoffs": "Exact change fallback supported.",
                "design_patterns_used": ["State", "Strategy"],
                "mermaid_diagram": "classDiagram\n    VendingMachine *-- Product\n",
                "classes": [
                    {
                        "name": "VendingMachine",
                        "responsibility": "Central state machine coordinator.",
                        "methods": [{"name": "selectProduct", "returnType": "void"}],
                        "relationships": []
                    },
                    {
                        "name": "Product",
                        "responsibility": "Represents items available in rack inventory.",
                        "attributes": [{"name": "price", "type": "double"}],
                        "relationships": []
                    }
                ]
            }
        }, format='json')

        # Submit attempt
        submit_resp = self.client.post(f'/api/attempts/{attempt_id}/submit/', {'evaluator_type': 'rule_based'}, format='json')
        assert submit_resp.status_code == status.HTTP_200_OK
        assert submit_resp.data['status'] == AttemptStatus.COMPLETED.value
        assert submit_resp.data['evaluation'] is not None
        assert submit_resp.data['evaluation']['overall_score'] > 0
        assert len(submit_resp.data['evaluation']['feedback_items']) > 0

    def test_history_and_dashboard_api(self):
        # Trigger dashboard
        dash_resp = self.client.get('/api/dashboard/')
        assert dash_resp.status_code == status.HTTP_200_OK
        assert 'stats' in dash_resp.data
        assert 'recent_attempts' in dash_resp.data
        assert 'recommended_problems' in dash_resp.data

        # Trigger history
        hist_resp = self.client.get('/api/history/')
        assert hist_resp.status_code == status.HTTP_200_OK
        assert isinstance(hist_resp.data, list)
