# Fill in this file with the code to get room details from the Webex Teams exercise
import requests

access_token = 'ODRjMjc4M2QtMWVhMy00N2RhLTg3YzAtYWFjMjJkMTMyYTA4ZDZlYzU4NTktMzc2_PE93_27f882c3-50be-433d-96e5-4dceb2514eab'
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vOWRkMDZhZTAtNWYzMi0xMWVmLThkZmUtNmQ1NjBkNjI3NzNi'
url = 'https://webexapis.com/v1/rooms/{}/meetingInfo'.format(room_id)
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
res = requests.get(url, headers=headers)
print(res.json())
