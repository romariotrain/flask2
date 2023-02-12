import requests

response = requests.post('http://127.0.0.1:5000/users',
                         json={'username': 'user4', 'password' : '123456',})


response2 = requests.post('http://127.0.0.1:5000/post',
                         json={'header' : '8', 'description' : 'test1', 'owner' : 'user1'})


response4 = requests.delete('http://127.0.0.1:5000/post/11')
response5 = requests.get('http://127.0.0.1:5000/post/11')
response3 = requests.get('http://127.0.0.1:5000/user/8')


print(response4.status_code, response4.text)

print(response2.status_code, response2.text)