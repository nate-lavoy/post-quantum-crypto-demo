import requests

# Base URL of your FastAPI app
BASE_URL = "http://127.0.0.1:8000"  # Replace with your actual base URL if different

# Test user credentials
email = "am123@gmail.com"
password = "am123"

# Step 1: Sign up a new user
def signup():
    url = f"{BASE_URL}/signup"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print("Signup successful:", response.json())
    elif response.status_code == 400:
        print("Signup failed (email already registered):", response.json())
    else:
        print("Signup failed:", response.status_code, response.json())

# Step 2: Log in to get an access token
def login():
    url = f"{BASE_URL}/login"
    data = {"email": email, "password": password}
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        print("Login successful. Access token:", access_token)
        return access_token
    else:
        print("Login failed:", response.status_code, response.json())
        return None

# Step 3: Access the /me endpoint using the access token
def get_current_user(access_token):
    url = f"{BASE_URL}/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        print("User info retrieved successfully:", response.json())
    else:
        print("Failed to retrieve user info:", response.status_code, response.json())

# Execute the flow
if __name__ == "__main__":
    # Step 1: Sign up (optional, skip if user already exists)
    signup()
    
    # Step 2: Log in to get an access token
    token = login()
    
    # Step 3: Use the token to access protected resources
    if token:
        get_current_user(token)