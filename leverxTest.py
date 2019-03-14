import requests

USER = "i_am_superuser"
PASSWORD = "Qwerty12345"
BASE_URL = "http://127.0.0.1:8000"

def get_devs():
    r = requests.get(BASE_URL + '/developers_list/')
    print(r.text)

def get_projects():
    r_2 = requests.get(BASE_URL + '/all_projects/')
    print(r_2.text)

def get_all_tasks():
    r_3 = requests.get(BASE_URL + '/all_tasks/')
    print(r_3.text)

def create_employee():
    create_user_data = {"user_internal": "Cooper", "is_manager": True,
                        "is_developer": False}
    r_4 = requests.post(BASE_URL + '/create_new_employee/',
                        json=create_user_data)
    print(r_4.text)

def create_user():
    create_user_data = {"username":"Bobr", "email":"borg@google.com", "password":"wepofR$#$FRF44f4"}
    r = requests.post(BASE_URL + '/create_new_user/', json=create_user_data)
    print(r.text)

def update_user():
    update_user_data = {"username" : "Bobr", "email":"roooo@tut.by"}
    r = requests.patch(BASE_URL + '/update_user/', json=update_user_data)
    print(r.text)

# get_all_tasks()
# get_devs()
# get_projects()
# create_employee()

#create_user()

update_user()