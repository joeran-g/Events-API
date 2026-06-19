import requests
import time

BASE_URL = "http://localhost:5000/api"
UNIQUE_USERNAME = f"user_{int(time.time())}"

# Unit tests

def test_health_endpoint_returns_healthy():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_register_user_creates_new_user():
    data={
        "username": UNIQUE_USERNAME,
        "password": "password"
    }
    register_response = requests.post(f"{BASE_URL}/auth/register", json=data)
    assert register_response.status_code == 201

def test_login_returns_jwt_token():
    login_response = requests.post(f"{BASE_URL}/auth/login", json={"username": UNIQUE_USERNAME, "password": "password"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def get_jwt_token():
    token_response = requests.post(f"{BASE_URL}/auth/login", json={"username": UNIQUE_USERNAME, "password": "password"})
    return token_response.json().get("access_token")

def test_create_public_event_requires_auth_and_succeeds_with_token():
    event_data = {
                "id": 1,
                "title": "Python Meetup",
                "description": "Monthly Python developer meetup",
                "date": "2026-01-15T18:00:00",
                "location": "Tech Hub, Room 101",
                "capacity": 50,
                "is_public": True
                }
    token = get_jwt_token()
    create_response = requests.post(f"{BASE_URL}/events", json=event_data, headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == 201

def test_register_for_public_event():
    event_id = 1
    token = get_jwt_token()
    json_data = {"attending": True}
    rsvps_response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=json_data, headers={"Authorization": f"Bearer {token}"})
    assert rsvps_response.status_code == 201

# Fehler/Randfall-integrationstests
def test_register_duplicate_username_returns_400():
    data = {
        "username": UNIQUE_USERNAME,
        "password": "password"
    }
    requests.post(f"{BASE_URL}/auth/register", json=data)
    duplicate_response = requests.post(f"{BASE_URL}/auth/register", json=data)
    assert duplicate_response.status_code == 400

def test_create_event_without_authentication_returns_401():
    event_data = {
        "id": 2,
        "title": "JavaScript Workshop",
        "description": "Web development workshop",
        "date": "2026-02-20T19:00:00",
        "location": "Tech Hub, Room 202",
        "capacity": 30,
    }
    create_response = requests.post(f"{BASE_URL}/events", json=event_data)
    assert create_response.status_code == 401

def create_private_event():
    event_data = {
                "id": 2,
                "title": "Private Meetup",
                "description": "Monthly Private developer meetup",
                "date": "2026-01-15T18:00:00",
                "location": "Tech Hub, Room 111",
                "capacity": 5,
                "is_public": False
                }
    token = get_jwt_token()
    create_response = requests.post(f"{BASE_URL}/events", json=event_data, headers={"Authorization": f"Bearer {token}"})

def test_rsvp_without_authentication_returns_401():
    create_private_event()
    event_id = 2
    json_data = {"attending": True}
    rsvps_response = requests.post(f"{BASE_URL}/rsvps/event/{event_id}", json=json_data)
    assert rsvps_response.status_code == 401

def test_login_with_invalid_credentials_returns_401():
    login_response = requests.post(f"{BASE_URL}/auth/login", json={"username": "nonexistent_user", "password": "wrong_password"})
    assert login_response.status_code == 401

def test_create_event_with_invalid_token_returns_401():
    event_data = {
            "id": 3,
            "title": "Python Meetup",
            "description": "Monthly Python developer meetup",
            "date": "2026-01-15T18:00:00",
            "location": "Tech Hub, Room 101",
            "capacity": 50,
            }
    token = get_jwt_token()
    create_response = requests.post(f"{BASE_URL}/events", json=event_data, headers={"Authorization": f"Bearer invalid_token"})
    assert create_response.status_code != 201