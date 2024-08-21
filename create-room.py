# Fill in this file with the code to create a new room from the Webex Teams exercise
import requests

access_token = 'ODRjMjc4M2QtMWVhMy00N2RhLTg3YzAtYWFjMjJkMTMyYTA4ZDZlYzU4NTktMzc2_PE93_27f882c3-50be-433d-96e5-4dceb2514eab'
url = 'https://webexapis.com/v1/rooms'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params={'title': 'Evaluación Final IR.2024'}
res = requests.post(url, headers=headers, json=params)
print(res.json())
