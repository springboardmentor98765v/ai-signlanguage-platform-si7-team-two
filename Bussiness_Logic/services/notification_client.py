import requests

BASE_URL = "http://localhost:8000"


def send_notification(
    user_id,
    title,
    message,
):
    payload = {
        "user_id": str(user_id),
        "title": title,
        "message": message,
    }

    try:
        response = requests.post(
            f"{BASE_URL}/notifications/",
            json=payload,
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except requests.RequestException as e:
        print(f"Notification API Error: {e}")
        return None