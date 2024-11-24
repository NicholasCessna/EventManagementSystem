import requests

class EmailVerifier:
    @staticmethod
    def verify(email):
        # Use an API like ZeroBounce to verify the email
        API_URL = "https://api.zerobounce.net/v2/validate"
        API_KEY = "712403cd2fdd4885afa1c1694e00cace"

        params = {
            "api_key": API_KEY,
            "email": email
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "valid" 
        return False