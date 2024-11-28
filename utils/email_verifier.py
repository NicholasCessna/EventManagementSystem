import requests

class EmailVerifier:
    @staticmethod
    def verify(email):
        # Use an API like ZeroBounce to verify the email
        API_URL = "https://api.zerobounce.net/v2/validate"
        API_KEY = "9d3c368da9654fd7b4b6bb1285b7"
        
        

        params = {
            "api_key": API_KEY,
            "email": email
        }

        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("status") == "valid" 
        return False