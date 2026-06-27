import requests

# url = "http://127.0.0.1:5000/v1/api/students/"
url = "http://localhost:4000/v1/api/students/"

for i in range(1, 51):
    name = f"Student {i}"
    email = f"student{i}@example.com"
    age = 20 + (i % 10)

    data = {"name": name, "email": email, "age": age}

    response = requests.post(url, json=data)
    print(response.json())