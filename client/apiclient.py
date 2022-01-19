import os
import requests
import sys
import logging
from dataclasses import asdict


class APIClient():
    def __init__(self, creds):
        self.creds = creds
        self.signin()

    def signin(self):
        url = os.getenv("SIGNIN_ENDPOINT")
        headers = {
            'Content-type': 'application/json'
        }
        body = {
        'username': self.creds["username"],
        'password': self.creds["password"]
        }

        response = requests.post(url=url, json=body, headers=headers)
        response_json = response.json()
        if response.status_code == 200:
            logging.info(response_json["message"])
            self.token = response_json["content"]["token"]
        else:
            logging.error(response_json["message"])
            sys.exit(1)
    
    def update_student(self, student):
        url = os.getenv("UPDATE_ENDPOINT") + student.roll_no
        headers = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.put(url=url, json=asdict(student), headers=headers)
        response_json = response.json()
        if response.status_code == 200:
            logging.info(response_json["message"])
        elif response.status_code == 401:
            logging.info("Signing in")
            self.signin()
        else:
            logging.error(response_json["message"])
            logging.info(response_json["content"])
