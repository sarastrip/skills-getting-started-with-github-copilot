import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Swim Club",
            "Art Studio",
            "Drama Club",
            "Science Olympiad",
            "Debate Team"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_contains_activity_details(self, client):
        # Arrange
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        activity = data["Chess Club"]
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_adds_participant_successfully(self, client, sample_email, sample_activity):
        # Arrange
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[sample_activity]["participants"].copy()

        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 200
        assert sample_email in response.json()["message"]
        
        # Verify the participant was added
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[sample_activity]["participants"]
        assert sample_email in updated_participants
        assert len(updated_participants) == len(initial_participants) + 1

    def test_signup_duplicate_rejected(self, client, sample_email, sample_activity):
        # Arrange
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Act
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_nonexistent_activity_returns_404(self, client, sample_email):
        # Arrange
        nonexistent_activity = "Nonexistent Activity Club"

        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": sample_email}
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/participants/{email} endpoint"""

    def test_unregister_removes_participant_successfully(self, client, sample_email, sample_activity):
        # Arrange
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]

        # Verify the participant was removed
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[sample_activity]["participants"]
        assert sample_email not in updated_participants

    def test_unregister_nonexistent_participant_returns_400(self, client, sample_activity):
        # Arrange
        nonexistent_email = "nonexistent@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{sample_activity}/participants/{nonexistent_email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"].lower()

    def test_unregister_from_nonexistent_activity_returns_404(self, client, sample_email):
        # Arrange
        nonexistent_activity = "Nonexistent Activity Club"

        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/participants/{sample_email}"
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_unregister_multiple_times_fails_on_second_attempt(self, client, sample_email, sample_activity):
        # Arrange
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": sample_email}
        )

        # Act - First unregister (should succeed)
        first_response = client.delete(
            f"/activities/{sample_activity}/participants/{sample_email}"
        )

        # Act - Second unregister (should fail)
        second_response = client.delete(
            f"/activities/{sample_activity}/participants/{sample_email}"
        )

        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 400


class TestRootEndpoint:
    """Test suite for GET / endpoint"""

    def test_root_redirects_to_index(self, client):
        # Arrange
        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]
