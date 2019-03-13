import requests

r = requests.get('http://127.0.0.1:8000/developers_list/')
print(r.text)

r_2 = requests.get('http://127.0.0.1:8000/all_projects/')
print(r_2.text)

r_3 = requests.get('http://127.0.0.1:8000/all_tasks/')
print(r_3.text)