def test_trainer_router_registered(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200

    paths = response.json()["paths"]

    assert "/trainer/learners" in paths
    assert "/trainer/learner/{learner_id}/engagement" in paths
    assert "/trainer/learner/{learner_id}/skill-development" in paths
    assert "/trainer/learner/{learner_id}/assessment-analytics" in paths
    assert "/trainer/learner/{learner_id}/certification-status" in paths