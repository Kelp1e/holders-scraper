import requests

url = "https://api.trongrid.io/v1/assets"

headers = {"accept": "application/json"}
params = {"limit": "200"}

tokens = requests.get(url, headers=headers, params=params)

for token in tokens.json().get("data"):
    response = requests.get(f"https://api.trongrid.io/v1/assets/{token.get('id')}")
    print(response.json())
