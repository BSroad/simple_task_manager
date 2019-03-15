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


def create_user():
    create_user_data = {"username":"Tom", "email": "tom@google.com",
                        "password": "wepofR$#$FRF44f4"}
    r = requests.post(BASE_URL + '/crud_user/', json=create_user_data)
    print(r.text)

def update_user():
    update_user_data = {"username" : "Bobr", "email": "roooo@tut.by"}
    r = requests.put(BASE_URL + '/crud_user/', json=update_user_data)
    print(r.text)

def get_user():
    get_user_data = {"username" : "Bobr", "email": "roooo@tut.by"}
    r = requests.get(BASE_URL + '/crud_user/', json=get_user_data)
    print(r.text)


def delete_user():
    delete_user_data = {"username" : "Bobr", "email": "roooo@tut.by"}
    r = requests.delete(BASE_URL + '/crud_user/', json=delete_user_data)
    print(r.text)


# Test requests CRUD employee
def create_employee():
    create_employee_data = {"user_internal": "Cooper", "is_manager": True,
                        "is_developer": False}
    r_4 = requests.post(BASE_URL + '/create_new_employee/',
                        json=create_employee_data)
    print(r_4.text)


def update_employee():
    update_employee_data = {"username": "Max", "email": "roooo@tut.by", "is_developer": False}
    r = requests.put(BASE_URL + '/crud_employee/', json=update_employee_data)
    print(r.text)


def get_employee():
    get_employee_data = {"username": "Tom", "email": "tom@google.com"}
    r = requests.put(BASE_URL + '/crud_employee/',
                         json=get_employee_data)
    print(r.text)


def delete_employee():
    delete_employee_data = {"username": "Max", "email": "roooo@tut.by"}
    r = requests.delete(BASE_URL + '/crud_user/',
                            json=delete_employee_data)
    print(r.text)

# Test requests CRUD project
def create_project():
    create_project_data = {"title": "Project Test", "description": "Test description, description", }
    r = requests.post(BASE_URL + '/crud_project/',
                        json=create_project_data)
    print(r.text)

def get_project():
    get_project_data = {"title": "Project Test", "description": "Test description, description",}
    r = requests.get(BASE_URL + '/crud_project/',
                         json=get_project_data)
    print(r.text)


def update_project():
    update_project_data = {"title": "Project Test",
                           "description": "Test description, description...",}
    r = requests.put(BASE_URL + '/crud_project/',
                         json=update_project_data)
    print(r.text)


def delete_project():
    delete_project_data = {"title": "Project Test",
                           "description": "Test description, description...",}
    r = requests.delete(BASE_URL + '/crud_project/',
                            json=delete_project_data)
    print(r.text)

# get_all_tasks()
# get_devs()
# get_projects()
# create_employee()
# create_user()
# update_user()
# delete_user()
# update_employee()
# get_employee()
# delete_employee()
# create_project()
# get_project()
# update_project()
delete_project()