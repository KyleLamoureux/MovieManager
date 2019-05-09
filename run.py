#!/usr/bin/env python3

import config
import os

from gmail_handler import *
from sheets import Sheets

def main():
    manager = Sheets('client_secret.json')
    email = GmailHandler(config.USERNAME, config.PASSWORD)
    movie_data = email.retrieve_email()
    if movie_data:
        manager.reformat_data('temp', movie_data)
        manager.add_new_movies('temp.json')
        if email.alert_email():
            os.remove('temp.json')

if __name__ == '__main__':
    main()
