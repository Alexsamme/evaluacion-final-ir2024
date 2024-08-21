# Fill in this file with the messages code from the Webex Teams exercise
import requests

access_token = 'ODRjMjc4M2QtMWVhMy00N2RhLTg3YzAtYWFjMjJkMTMyYTA4ZDZlYzU4NTktMzc2_PE93_27f882c3-50be-433d-96e5-4dceb2514eab'
room_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL1JPT00vOWRkMDZhZTAtNWYzMi0xMWVmLThkZmUtNmQ1NjBkNjI3NzNi'
#message = 'Hello **mundo xD**!!'
#message = "tengo hambre"
emoji = " \ud83d\ude42 \ud83d\ude1b \ud83d\ude44"
#message = "tengo hambre" + emoji
message = 'Hello **mundo xD**!!' + emoji
url = 'https://webexapis.com/v1/messages'
headers = {
    'Authorization': 'Bearer {}'.format(access_token),
    'Content-Type': 'application/json'
}
params = {'roomId': room_id, 'markdown': message}
res = requests.post(url, headers=headers, json=params)
print(res.json())
