# Fill in this file with the authentication code from the Webex Teams exercise
import requests
import json

access_token = 'ODRjMjc4M2QtMWVhMy00N2RhLTg3YzAtYWFjMjJkMTMyYTA4ZDZlYzU4NTktMzc2_PE93_27f882c3-50be-433d-96e5-4dceb2514eab'
url = 'https://webexapis.com/v1/people/me'
headers = {
    'Authorization': 'Bearer {}'.format(access_token)
}
res = requests.get(url, headers=headers)
print(json.dumps(res.json(), indent=4))

