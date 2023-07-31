import requests

url = "https://api.trongrid.io/v1/assets/TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

headers = {"accept": "application/json"}

response = requests.get(url, headers=headers)

print(response.text)