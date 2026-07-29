import requests


class IntegrationService:
    """
    Handles communication between the Backend
    and the Business Logic microservice.
    """

    BUSINESS_LOGIC_URL = "http://127.0.0.1:8002"

    # -----------------------------
    # Certificate APIs
    # -----------------------------

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
            params={
                "learner_name": learner_name,
            },
        )

        response.raise_for_status()

        return response.content

    # -----------------------------
    # Progress Report APIs
    # -----------------------------

    @staticmethod
    def get_progress_report(user_id):
        response = requests.get(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/progress-report/{user_id}"
        )

        if response.status_code != 200:
            raise requests.exceptions.HTTPError(
                response.text,
                response=response
            )

        return response.json()

    @staticmethod
    def download_progress_report(user_id, learner_name):
        response = requests.get(
            f"{IntegrationService.BUSINESS_LOGIC_URL}/progress-report/{user_id}/pdf",
            params={
                "learner_name": learner_name,
            },
        )

        response.raise_for_status()

        return response.content