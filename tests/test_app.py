from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    route = "/"

    # Act
    response = client.get(route, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_payload_shape():
    # Arrange
    route = "/activities"

    # Act
    response = client.get(route)
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success_for_existing_activity():
    # Arrange
    activity_name = "Drama Club"
    email = "aaa-signup-success@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}


def test_signup_fails_for_duplicate_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up"}


def test_signup_fails_for_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "aaa-unknown@mergington.edu"
    route = f"/activities/{activity_name}/signup"

    # Act
    response = client.post(route, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_success_for_existing_participant():
    # Arrange
    activity_name = "Art Studio"
    email = "aaa-unregister-success@mergington.edu"
    signup_route = f"/activities/{activity_name}/signup"
    unregister_route = f"/activities/{activity_name}/participants"
    client.post(signup_route, params={"email": email})

    # Act
    response = client.delete(unregister_route, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}


def test_unregister_fails_for_missing_participant():
    # Arrange
    activity_name = "Soccer Team"
    email = "aaa-not-registered@mergington.edu"
    route = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(route, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}


def test_unregister_fails_for_unknown_activity():
    # Arrange
    activity_name = "Unknown Activity"
    email = "aaa-missing-activity@mergington.edu"
    route = f"/activities/{activity_name}/participants"

    # Act
    response = client.delete(route, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}