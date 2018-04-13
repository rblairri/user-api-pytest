#!/usr/bin/python

import pytest
import requests
import uuid

HOST = "http://someuserapi/"


def randomInput():
    return uuid.uuid4().hex


@pytest.mark.parametrize('user, password, expectCode', [
    (randomInput(), "password", 200),
    (randomInput(), "", 400),
    ("", "", 400)])
def test_newUser(user, password, expectCode):
    path = HOST + "newUser"
    response = requests.post(path, data={"user": user, "password": password})
    assert response.status_code == expectCode


def test_newUser_userAlreadyExists():
    user = randomInput()
    password = "password"
    expectCode = 401
    path = HOST + "newUser"
    requests.post(path, data={"user": user, "password": password})
    response = requests.post(path, data={"user": user, "password": password})
    assert response.status_code == expectCode


def test_login():
    user = randomInput()
    password = "password"
    expectCode = 200
    path = HOST + "newUser"
    requests.post(path, data={"user": user, "password": password})
    path = HOST + "login"
    response = requests.get(path, headers={"user": user, "password": password})
    assert response.status_code == expectCode


@pytest.mark.parametrize('user, password, expectCode', [
    ("wronguser", "password", 401),
    (randomInput(), "wrongpassword", 401),
    ("wronguser", "wrongpassword", 401),
    ("", "", 400)])
def test_login_wrongInput(user, password, expectCode):
    path = HOST + "login"
    response = requests.get(path, headers={"user": user, "password": password})
    assert response.status_code == expectCode


def test_Logout():
    user = randomInput()
    password = "password"
    expectCode = 200
    path = HOST + "newUser"
    requests.post(path, data={"user": user, "password": password})
    path = HOST + "login"
    response = requests.get(path, headers={"user": user, "password": password})
    sessionId = response.json()["sessionId"]
    path = HOST + "logout"
    response = requests.get(path, headers={"user": user,
                                           "sessionid": sessionId})
    assert response.status_code == expectCode
