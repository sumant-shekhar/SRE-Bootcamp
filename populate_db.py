import requests

url = "http://172.18.0.3:4000/v1/api/students/"
# data = [
#     {"name": "Alice", "email": "alice@example.com", "age": 20},
#     {"name": "Bob", "email": "bob@example.com", "age": 22},
#     {"name": "Charlie", "email": "charlie@example.com", "age": 21}
# ]
for i in range(1, 51):
    name = f"Student {i}"
    email = f"student{i}@example.com"
    age = 20 + (i % 10)

    data = {"name": name, "email": email, "age": age}

    response = requests.post(url, json=data)
    print(response.json())