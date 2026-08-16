import requests


class IntegrationService:
    """Communication with the business-logic microservice."""

    BUSINESS_LOGIC_URL = "http://127.0.0.1:8002"

    @staticmethod
    def get_certificate_eligibility(user_id):
        response = requests.get(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/certificates/{user_id}/eligibility"
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def issue_certificate(user_id, learner_name):
        response = requests.post(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/certificates/{user_id}/issue",
            params={"learner_name": learner_name},
        )
        response.raise_for_status()
        return response.content

    @staticmethod
    def get_progress_report(user_id):
        response = requests.get(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/progress-report/{user_id}"
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def download_progress_report(user_id, learner_name):
        response = requests.get(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/progress-report/{user_id}/pdf",
            params={"learner_name": learner_name},
        )
        response.raise_for_status()
        return response.content
